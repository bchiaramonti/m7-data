#!/usr/bin/env python3
"""
compute_auto_layout.py — Auto-layout deterministico para BPMN 2.0.

Recebe um JSON de input seguindo templates/input-schema.tmpl.json, e gera um
JSON de layout com bounds (x, y, width, height) de cada shape (pool, lane, node)
e waypoints de cada edge.

Algoritmo: ver references/auto-layout-algorithm.md.
Stdlib only — sem dependencias externas.

Uso:
    python3 compute_auto_layout.py input.json > layout.json

Exit codes:
    0  sucesso
    1  erro (JSON invalido, ciclo nao-resolvivel, etc.)
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict, deque

# ─────────────────────────────────────────────────────────────────────
# Constantes geometricas (ver references/auto-layout-algorithm.md § 1)
# ─────────────────────────────────────────────────────────────────────

H_SPACING = 150
V_SPACING = 100
LEFT_MARGIN = 80
TOP_MARGIN = 50
POOL_HEADER_HEIGHT = 30
LANE_HEADER_WIDTH = 30
POOL_X = 160
POOL_Y = 0
INTER_POOL_GAP = 60

# Dimensoes dos elementos
EVENT_W, EVENT_H = 36, 36
TASK_W, TASK_H = 100, 80
SUBPROC_W, SUBPROC_H = 120, 80
GATEWAY_W, GATEWAY_H = 50, 50
DATA_STORE_W, DATA_STORE_H = 50, 50    # cilindro
DATA_OBJECT_W, DATA_OBJECT_H = 36, 50  # documento

# Categorias de tipo
EVENT_PREFIXES = ("startEvent", "intermediateEvent", "endEvent")
GATEWAY_SUFFIX = "Gateway"
DATA_TYPES = ("dataStoreReference", "dataObjectReference")


def element_size(node_type: str) -> tuple[int, int]:
    """Retorna (width, height) baseado no tipo BPMN do node."""
    if any(node_type.startswith(p) for p in EVENT_PREFIXES):
        return (EVENT_W, EVENT_H)
    if node_type.endswith(GATEWAY_SUFFIX):
        return (GATEWAY_W, GATEWAY_H)
    if node_type in ("subProcess", "adHocSubProcess"):
        return (SUBPROC_W, SUBPROC_H)
    if node_type == "dataStoreReference":
        return (DATA_STORE_W, DATA_STORE_H)
    if node_type == "dataObjectReference":
        return (DATA_OBJECT_W, DATA_OBJECT_H)
    return (TASK_W, TASK_H)


def is_boundary_event(node: dict) -> bool:
    """Boundary events tem attachedTo e nao entram em layout normal."""
    return bool(node.get("attachedTo"))


def is_child_of_subprocess(node: dict) -> bool:
    """Tools dentro de adHocSubProcess tem 'parent' apontando para o sub-process."""
    return bool(node.get("parent"))


def is_data_reference(node: dict) -> bool:
    """DataStoreReference / DataObjectReference: layout especial (centralizado na lane)."""
    return node.get("type") in DATA_TYPES


# ─────────────────────────────────────────────────────────────────────
# Passo 1 — Topological sort (rank assignment)
# ─────────────────────────────────────────────────────────────────────

def assign_ranks(nodes: list[dict], edges: list[dict]) -> dict[str, int]:
    """
    Atribui rank a cada node, baseado na distancia maxima a partir dos start events.

    Boundary events e tools de sub-process nao recebem rank (herdam posicao).
    Loops detectados: rank do retorno e fixado na primeira visita.
    """
    # Map id -> node, edges saintes
    node_by_id = {n["id"]: n for n in nodes}
    outgoing: dict[str, list[str]] = defaultdict(list)
    incoming: dict[str, list[str]] = defaultdict(list)

    for e in edges:
        if e["type"] != "sequenceFlow":
            continue
        outgoing[e["source"]].append(e["target"])
        incoming[e["target"]].append(e["source"])

    # Filtrar nodes elegiveis para layout (excluir boundary, child-of-subprocess, data references)
    layoutable = [
        n for n in nodes
        if not is_boundary_event(n) and not is_child_of_subprocess(n) and not is_data_reference(n)
    ]
    layoutable_ids = {n["id"] for n in layoutable}

    # Start events
    start_events = [n for n in layoutable if n["type"].startswith("startEvent")]
    if not start_events:
        # Fallback: usar nodes sem incoming
        start_events = [n for n in layoutable if not incoming.get(n["id"])]
    if not start_events:
        raise ValueError("No start event found. Process needs at least one node without incoming edges.")

    ranks: dict[str, int] = {}
    queue: deque[str] = deque()
    for s in start_events:
        ranks[s["id"]] = 0
        queue.append(s["id"])

    # BFS iterativo com max-rank semantics
    visit_count: dict[str, int] = defaultdict(int)
    MAX_VISITS = 100  # protecao contra cycles patologicos

    while queue:
        n_id = queue.popleft()
        visit_count[n_id] += 1
        if visit_count[n_id] > MAX_VISITS:
            continue
        for target_id in outgoing.get(n_id, []):
            if target_id not in layoutable_ids:
                continue
            candidate = ranks[n_id] + 1
            if target_id not in ranks or candidate > ranks[target_id]:
                # Para evitar loop infinito, so propaga se diferenca e razoavel
                if target_id in ranks and candidate > ranks[target_id] + 10:
                    continue
                ranks[target_id] = candidate
                queue.append(target_id)

    # Nodes nao alcancados a partir de start: assign rank 0 (orfaos)
    for n in layoutable:
        if n["id"] not in ranks:
            ranks[n["id"]] = 0

    return ranks


# ─────────────────────────────────────────────────────────────────────
# Passos 2-6 — Coordenadas de pools, lanes, nodes
# ─────────────────────────────────────────────────────────────────────

def compute_layout(input_data: dict) -> dict:
    """
    Funcao principal. Retorna dict com chaves: pools, lanes, nodes, edges.
    Cada elemento tem (x, y, width, height) ou waypoints.
    """
    pools = input_data["pools"]
    nodes = input_data["nodes"]
    edges = input_data.get("edges", [])

    # Filtrar nodes elegiveis para layout principal
    layoutable_nodes = [
        n for n in nodes
        if not is_boundary_event(n) and not is_child_of_subprocess(n) and not is_data_reference(n)
    ]
    boundary_nodes = [n for n in nodes if is_boundary_event(n)]
    child_nodes = [n for n in nodes if is_child_of_subprocess(n)]
    data_ref_nodes = [n for n in nodes if is_data_reference(n)]

    # ─ Passo 1 ─ ranks
    ranks = assign_ranks(nodes, edges)

    # ─ Passo 2 ─ agrupar por (lane, rank)
    lane_rank_nodes: dict[str, dict[int, list[str]]] = defaultdict(lambda: defaultdict(list))
    for n in layoutable_nodes:
        lane_rank_nodes[n["lane"]][ranks[n["id"]]].append(n["id"])

    # ─ Passo 3 ─ alturas das lanes
    lane_heights: dict[str, int] = {}
    lane_id_to_pool: dict[str, str] = {}
    lane_id_to_name: dict[str, str] = {}
    for pool in pools:
        for lane in pool["lanes"]:
            lid = lane["id"]
            lane_id_to_pool[lid] = pool["id"]
            lane_id_to_name[lid] = lane["name"]
            ranks_in_lane = lane_rank_nodes[lid]
            if not ranks_in_lane:
                lane_heights[lid] = 120
            else:
                max_nodes_in_rank = max(len(ids) for ids in ranks_in_lane.values())
                lane_heights[lid] = max(max_nodes_in_rank * V_SPACING, 120)

    # ─ Passo 4 ─ posicionar pools e lanes verticalmente
    layout_pools: list[dict] = []
    layout_lanes: list[dict] = []

    current_pool_y = POOL_Y
    for pool in pools:
        pool_lanes = pool["lanes"]
        pool_height = POOL_HEADER_HEIGHT + sum(lane_heights[l["id"]] for l in pool_lanes)

        # Calcular max_rank no pool para definir width
        max_rank_in_pool = 0
        for lane in pool_lanes:
            for r, ids in lane_rank_nodes[lane["id"]].items():
                if ids:
                    max_rank_in_pool = max(max_rank_in_pool, r)
        pool_width = LANE_HEADER_WIDTH + LEFT_MARGIN + (max_rank_in_pool + 1) * H_SPACING + LEFT_MARGIN

        # Adicionar pool
        layout_pools.append({
            "id": pool["id"],
            "x": POOL_X,
            "y": current_pool_y,
            "width": pool_width,
            "height": pool_height,
        })

        # Adicionar lanes (Y crescente dentro do pool)
        # IMPORTANTE: lane.x = pool.x + LANE_HEADER_WIDTH e lane.width = pool.width - LANE_HEADER_WIDTH
        # Isso reserva uma faixa de LANE_HEADER_WIDTH (30px) na borda esquerda do pool exclusiva
        # para o label vertical do pool. Sem esse inset, label do pool e labels das lanes se
        # sobrepoem na mesma faixa vertical (issue corrigido em v1.2.2).
        current_lane_y = current_pool_y + POOL_HEADER_HEIGHT
        for lane in pool_lanes:
            lh = lane_heights[lane["id"]]
            layout_lanes.append({
                "id": lane["id"],
                "x": POOL_X + LANE_HEADER_WIDTH,
                "y": current_lane_y,
                "width": pool_width - LANE_HEADER_WIDTH,
                "height": lh,
            })
            current_lane_y += lh

        current_pool_y += pool_height + INTER_POOL_GAP

    # Map lane_id -> bounds para usar nos nodes
    lane_bounds = {l["id"]: l for l in layout_lanes}
    pool_bounds = {p["id"]: p for p in layout_pools}

    # ─ Passo 5 ─ posicionar nodes
    layout_nodes: list[dict] = []

    for n in layoutable_nodes:
        w, h = element_size(n["type"])
        rank = ranks[n["id"]]
        lane = lane_bounds[n["lane"]]
        pool = pool_bounds[n["pool"]]

        # X: baseado no rank
        x = pool["x"] + LANE_HEADER_WIDTH + LEFT_MARGIN + (rank * H_SPACING) - w // 2

        # Y: centralizado na lane, distribuido se multiplos nodes no mesmo rank
        nodes_aqui = lane_rank_nodes[n["lane"]][rank]
        idx = nodes_aqui.index(n["id"])
        total = len(nodes_aqui)

        lane_center = lane["y"] + lane["height"] // 2
        first_y = lane_center - ((total - 1) * V_SPACING) // 2
        y = first_y + (idx * V_SPACING) - h // 2

        layout_nodes.append({
            "id": n["id"],
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "type": n["type"],
        })

    # Boundary events: posicionar relativo ao hospedeiro
    layout_node_by_id = {ln["id"]: ln for ln in layout_nodes}
    for b in boundary_nodes:
        host = layout_node_by_id.get(b["attachedTo"])
        if not host:
            continue
        bw, bh = element_size(b["type"])
        layout_nodes.append({
            "id": b["id"],
            "x": host["x"] + host["width"] - bw // 2,
            "y": host["y"] + host["height"] - bh // 2,
            "width": bw,
            "height": bh,
            "type": b["type"],
        })

    # DataStoreReferences / DataObjectReferences: posicionar centralizados na lane,
    # com offset horizontal entre multiplas refs na mesma lane (evita overlap).
    # NUNCA permitir bounds identicos entre 2 refs (mesmo se apontam para mesmo dataStore global).
    refs_per_lane: dict[str, int] = defaultdict(int)
    for d in data_ref_nodes:
        lane = lane_bounds.get(d["lane"])
        if not lane:
            continue
        dw, dh = element_size(d["type"])
        idx = refs_per_lane[d["lane"]]
        refs_per_lane[d["lane"]] += 1
        # Centralizar verticalmente na lane; espacar horizontalmente se >1 na mesma lane
        DATA_REF_GAP = 80
        center_x = lane["x"] + lane["width"] // 2 - dw // 2
        x = center_x + (idx * DATA_REF_GAP) - ((refs_per_lane[d["lane"]] - 1) * DATA_REF_GAP) // 2
        y = lane["y"] + lane["height"] // 2 - dh // 2
        layout_nodes.append({
            "id": d["id"],
            "x": x,
            "y": y,
            "width": dw,
            "height": dh,
            "type": d["type"],
        })

    # Tools dentro de adHocSubProcess: posicionar em grid 2x2 ou 3x2 dentro do parent
    for c in child_nodes:
        parent = layout_node_by_id.get(c["parent"])
        if not parent:
            continue
        # Grid 3 colunas
        siblings = [n for n in child_nodes if n.get("parent") == c["parent"]]
        idx = siblings.index(c)
        cols = 3
        col = idx % cols
        row = idx // cols

        TOOL_W, TOOL_H = 80, 60
        TOOL_GAP = 20
        x = parent["x"] + 20 + col * (TOOL_W + TOOL_GAP)
        y = parent["y"] + 40 + row * (TOOL_H + TOOL_GAP)
        layout_nodes.append({
            "id": c["id"],
            "x": x,
            "y": y,
            "width": TOOL_W,
            "height": TOOL_H,
            "type": c["type"],
        })

    layout_node_by_id = {ln["id"]: ln for ln in layout_nodes}

    # ─ Passo 7 ─ waypoints
    layout_edges: list[dict] = []
    for e in edges:
        source = layout_node_by_id.get(e["source"])
        target = layout_node_by_id.get(e["target"])
        if not source or not target:
            continue

        # Saida pelo lado direito do source
        wp1_x = source["x"] + source["width"]
        wp1_y = source["y"] + source["height"] // 2

        # Entrada pelo lado esquerdo do target
        wp2_x = target["x"]
        wp2_y = target["y"] + target["height"] // 2

        # Loop-back: target.x < source.x → sair pela direita com offset lateral, subir, atravessar, descer
        if target["x"] < source["x"]:
            host_lane = next(
                (l for l in layout_lanes if l["id"] == [n for n in nodes if n["id"] == e["source"]][0]["lane"]),
                None,
            )
            if host_lane:
                top_y = host_lane["y"] - 20
                # Offset lateral de 30px alem da borda direita do source
                # Evita kink visual colado no node — da "respiro" antes da virada vertical
                LOOP_LATERAL_OFFSET = 30
                exit_x = source["x"] + source["width"] + LOOP_LATERAL_OFFSET
                target_center_x = target["x"] + target["width"] // 2
                source_mid_y = source["y"] + source["height"] // 2
                waypoints = [
                    {"x": source["x"] + source["width"], "y": source_mid_y},  # sai pela direita
                    {"x": exit_x, "y": source_mid_y},                          # offset lateral
                    {"x": exit_x, "y": top_y},                                  # sobe
                    {"x": target_center_x, "y": top_y},                         # atravessa horizontal
                    {"x": target_center_x, "y": target["y"]},                   # desce ate borda superior do target
                ]
            else:
                waypoints = [{"x": wp1_x, "y": wp1_y}, {"x": wp2_x, "y": wp2_y}]
        elif abs(wp1_y - wp2_y) > 10:
            # Cross-lane: adicionar waypoint intermediario
            mid_x = (wp1_x + wp2_x) // 2
            waypoints = [
                {"x": wp1_x, "y": wp1_y},
                {"x": mid_x, "y": wp1_y},
                {"x": mid_x, "y": wp2_y},
                {"x": wp2_x, "y": wp2_y},
            ]
        else:
            # Linha reta horizontal
            waypoints = [
                {"x": wp1_x, "y": wp1_y},
                {"x": wp2_x, "y": wp2_y},
            ]

        layout_edges.append({
            "id": e["id"],
            "waypoints": waypoints,
        })

    return {
        "pools": layout_pools,
        "lanes": layout_lanes,
        "nodes": layout_nodes,
        "edges": layout_edges,
    }


# ─────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────

def main() -> int:
    if len(sys.argv) < 2:
        print("Uso: python3 compute_auto_layout.py <input.json>", file=sys.stderr)
        return 1

    input_path = sys.argv[1]
    try:
        with open(input_path, encoding="utf-8") as f:
            input_data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Erro ao ler {input_path}: {exc}", file=sys.stderr)
        return 1

    try:
        layout = compute_layout(input_data)
    except (ValueError, KeyError) as exc:
        print(f"Erro ao computar layout: {exc}", file=sys.stderr)
        return 1

    json.dump(layout, sys.stdout, indent=2, ensure_ascii=False)
    print()  # newline final
    return 0


if __name__ == "__main__":
    sys.exit(main())
