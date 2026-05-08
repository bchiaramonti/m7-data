#!/usr/bin/env python3
"""
validate_bpmn_readability.py — Validador geometrico deterministico de arquivos .bpmn.

Aplica 5 detectores definidos em references/readability-rules.md:
    1. edge-crosses-node
    2. edge-overlap
    3. label-overflow
    4. aspect-ratio-violation
    5. rtl-flow

Stdlib only — usa xml.etree.ElementTree para parse do .bpmn.

Uso:
    python3 validate_bpmn_readability.py <arquivo.bpmn>

Output (stdout): JSON com {passed: bool, issues: [...]}.
Exit codes:
    0  passed (sem fails)
    1  not passed (>= 1 fail)
    2  erro de parse / IO
"""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from itertools import combinations

# ─────────────────────────────────────────────────────────────────────
# Constantes (espelhadas de readability-rules.md)
# ─────────────────────────────────────────────────────────────────────

EDGE_CROSS_MARGIN = 8       # px de tolerancia ao redor do bounding-box
EDGE_OVERLAP_MIN = 20       # px minimo de segmento sobreposto para flag
LABEL_CHAR_WIDTH = 6.5      # px medio por char a font-size 11
LABEL_LINE_HEIGHT = 14
LABEL_PADDING = 8           # padding interno
ASPECT_TOLERANCE = 0.01     # 1% de tolerancia em dimensoes
RTL_THRESHOLD = 0.3         # 30% de flows RTL = fail

# Dimensoes esperadas por categoria
EXPECTED_SIZES = {
    "event": (36, 36),
    "task": (100, 80),
    "subProcess": (120, 80),
    "gateway": (50, 50),
}

# Namespaces BPMN
NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}


# ─────────────────────────────────────────────────────────────────────
# Parsing
# ─────────────────────────────────────────────────────────────────────

def parse_bpmn(path: str) -> dict:
    """
    Parse do .bpmn. Retorna estrutura com nodes, edges, labels, dimensoes.
    """
    tree = ET.parse(path)
    root = tree.getroot()

    # Coletar labels e tipos de elements em qualquer lugar (process, collaboration, laneSet)
    labels = {}
    types = {}
    for elem in root.iter():
        if "}" not in elem.tag:
            continue
        tag = elem.tag.split("}")[-1]
        elem_id = elem.attrib.get("id")
        if not elem_id:
            continue
        if elem.attrib.get("name"):
            labels[elem_id] = elem.attrib["name"]
        # Nao sobrescrever se ja registrado por iter mais especifico
        if elem_id not in types:
            types[elem_id] = tag

    # Coletar shapes (bounds)
    shapes = []
    for shape in root.iter(f"{{{NS['bpmndi']}}}BPMNShape"):
        bpmn_element = shape.attrib.get("bpmnElement")
        if not bpmn_element:
            continue
        bounds = shape.find(f"{{{NS['dc']}}}Bounds")
        if bounds is None:
            continue
        shapes.append({
            "id": bpmn_element,
            "x": float(bounds.attrib.get("x", 0)),
            "y": float(bounds.attrib.get("y", 0)),
            "width": float(bounds.attrib.get("width", 0)),
            "height": float(bounds.attrib.get("height", 0)),
            "label": labels.get(bpmn_element, ""),
            "type": types.get(bpmn_element, "unknown"),
        })

    # Coletar edges (waypoints)
    edges = []
    edge_endpoints = {}
    for sf in root.iter(f"{{{NS['bpmn']}}}sequenceFlow"):
        eid = sf.attrib.get("id")
        if not eid:
            continue
        edge_endpoints[eid] = (
            sf.attrib.get("sourceRef"),
            sf.attrib.get("targetRef"),
        )
    for mf in root.iter(f"{{{NS['bpmn']}}}messageFlow"):
        eid = mf.attrib.get("id")
        if not eid:
            continue
        edge_endpoints[eid] = (
            mf.attrib.get("sourceRef"),
            mf.attrib.get("targetRef"),
        )

    for edge in root.iter(f"{{{NS['bpmndi']}}}BPMNEdge"):
        bpmn_element = edge.attrib.get("bpmnElement")
        if not bpmn_element:
            continue
        waypoints = [
            {"x": float(wp.attrib["x"]), "y": float(wp.attrib["y"])}
            for wp in edge.findall(f"{{{NS['di']}}}waypoint")
        ]
        if len(waypoints) < 2:
            continue
        source, target = edge_endpoints.get(bpmn_element, (None, None))
        edges.append({
            "id": bpmn_element,
            "source": source,
            "target": target,
            "waypoints": waypoints,
        })

    return {"shapes": shapes, "edges": edges}


# ─────────────────────────────────────────────────────────────────────
# Detector 1 — Edge crosses node
# ─────────────────────────────────────────────────────────────────────

def segment_intersects_bbox(p1: dict, p2: dict, bbox: tuple) -> bool:
    """
    Cohen-Sutherland: testa se segmento (p1 -> p2) cruza o retangulo bbox.
    bbox = (xmin, ymin, xmax, ymax).
    """
    xmin, ymin, xmax, ymax = bbox

    INSIDE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8

    def code(x, y):
        c = INSIDE
        if x < xmin: c |= LEFT
        elif x > xmax: c |= RIGHT
        if y < ymin: c |= BOTTOM
        elif y > ymax: c |= TOP
        return c

    x1, y1 = p1["x"], p1["y"]
    x2, y2 = p2["x"], p2["y"]
    c1, c2 = code(x1, y1), code(x2, y2)

    while True:
        if c1 == 0 and c2 == 0:
            return True  # totalmente dentro
        if (c1 & c2) != 0:
            return False  # totalmente fora do mesmo lado
        # caso parcial: clip
        c_out = c1 or c2
        if c_out & TOP:
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1) if y2 != y1 else x1
            y = ymax
        elif c_out & BOTTOM:
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1) if y2 != y1 else x1
            y = ymin
        elif c_out & RIGHT:
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1) if x2 != x1 else y1
            x = xmax
        elif c_out & LEFT:
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1) if x2 != x1 else y1
            x = xmin
        else:
            return False
        if c_out == c1:
            x1, y1 = x, y
            c1 = code(x1, y1)
        else:
            x2, y2 = x, y
            c2 = code(x2, y2)


def detect_edge_crosses_node(shapes: list[dict], edges: list[dict]) -> list[dict]:
    issues = []
    # Filtrar apenas flow nodes (excluir pools, lanes — eles englobam tudo por design)
    flow_nodes = [
        s for s in shapes
        if s["type"] not in ("participant", "lane", "textAnnotation")
    ]
    for edge in edges:
        endpoints = (edge["source"], edge["target"])
        wps = edge["waypoints"]
        for i in range(len(wps) - 1):
            seg_start = wps[i]
            seg_end = wps[i + 1]
            for node in flow_nodes:
                if node["id"] in endpoints:
                    continue
                bbox = (
                    node["x"] - EDGE_CROSS_MARGIN,
                    node["y"] - EDGE_CROSS_MARGIN,
                    node["x"] + node["width"] + EDGE_CROSS_MARGIN,
                    node["y"] + node["height"] + EDGE_CROSS_MARGIN,
                )
                if segment_intersects_bbox(seg_start, seg_end, bbox):
                    issues.append({
                        "type": "edge-crosses-node",
                        "edgeId": edge["id"],
                        "nodeId": node["id"],
                        "severity": "fail",
                        "suggestion": f"Reroute edge {edge['id']} to avoid node {node['id']}",
                    })
                    break  # 1 issue por edge
    return issues


# ─────────────────────────────────────────────────────────────────────
# Detector 2 — Edge overlap
# ─────────────────────────────────────────────────────────────────────

def collinear_overlap_length(s1_start, s1_end, s2_start, s2_end) -> float:
    """
    Retorna comprimento de segmento compartilhado se s1 e s2 sao colineares
    no mesmo eixo (horizontal ou vertical). Caso contrario retorna 0.
    """
    # Horizontal: y constante
    if s1_start["y"] == s1_end["y"] and s2_start["y"] == s2_end["y"] and s1_start["y"] == s2_start["y"]:
        x1_min = min(s1_start["x"], s1_end["x"])
        x1_max = max(s1_start["x"], s1_end["x"])
        x2_min = min(s2_start["x"], s2_end["x"])
        x2_max = max(s2_start["x"], s2_end["x"])
        overlap = max(0, min(x1_max, x2_max) - max(x1_min, x2_min))
        return overlap
    # Vertical: x constante
    if s1_start["x"] == s1_end["x"] and s2_start["x"] == s2_end["x"] and s1_start["x"] == s2_start["x"]:
        y1_min = min(s1_start["y"], s1_end["y"])
        y1_max = max(s1_start["y"], s1_end["y"])
        y2_min = min(s2_start["y"], s2_end["y"])
        y2_max = max(s2_start["y"], s2_end["y"])
        overlap = max(0, min(y1_max, y2_max) - max(y1_min, y2_min))
        return overlap
    return 0


def detect_edge_overlap(edges: list[dict]) -> list[dict]:
    """
    Detecta sobreposicao colinear > 20px entre 2 edges.
    Excecao: edges saindo do mesmo gateway compartilham origem; ignorar overlap
    nos primeiros 50px se ambos comecam no mesmo ponto.
    """
    issues = []
    for e1, e2 in combinations(edges, 2):
        same_source = (
            e1["source"]
            and e2["source"]
            and e1["source"] == e2["source"]
        )
        for i in range(len(e1["waypoints"]) - 1):
            for j in range(len(e2["waypoints"]) - 1):
                # Skip se ambos segmentos sao o primeiro de cada edge E sources iguais
                if i == 0 and j == 0 and same_source:
                    continue
                overlap = collinear_overlap_length(
                    e1["waypoints"][i], e1["waypoints"][i + 1],
                    e2["waypoints"][j], e2["waypoints"][j + 1],
                )
                if overlap > EDGE_OVERLAP_MIN:
                    issues.append({
                        "type": "edge-overlap",
                        "edgeIds": [e1["id"], e2["id"]],
                        "overlapLength": round(overlap, 1),
                        "severity": "fail",
                        "suggestion": f"Add intermediate waypoint to {e2['id']} with offset",
                    })
                    break
            else:
                continue
            break
    return issues


# ─────────────────────────────────────────────────────────────────────
# Detector 3 — Label overflow
# ─────────────────────────────────────────────────────────────────────

def best_2line_split_max_width(words: list[str]) -> float:
    """
    Tenta splitar em 2 linhas. Retorna a maior largura entre as 2 linhas
    no melhor split possivel.
    """
    if len(words) < 2:
        return len(" ".join(words)) * LABEL_CHAR_WIDTH

    best_max = float("inf")
    for split_idx in range(1, len(words)):
        line1 = " ".join(words[:split_idx])
        line2 = " ".join(words[split_idx:])
        max_w = max(len(line1), len(line2)) * LABEL_CHAR_WIDTH
        if max_w < best_max:
            best_max = max_w
    return best_max


def detect_label_overflow(shapes: list[dict]) -> list[dict]:
    """
    Detecta label overflow apenas em containers que renderizam o label DENTRO:
    tasks, subprocesses, gateways. Events tem label externo (abaixo do circulo)
    e nao sofrem overflow. Pools/lanes tem label vertical em barra propria.
    """
    issues = []
    # Apenas tasks e subprocesses renderizam label dentro do shape.
    # Events (circulos) e gateways (losangos) tem labels externos por convencao
    # Camunda / bpmn.io. Pools/lanes tem barra de label propria.
    INTERNAL_LABEL_TYPES = {
        "task", "userTask", "serviceTask", "scriptTask", "sendTask", "receiveTask",
        "manualTask", "businessRuleTask",
        "subProcess", "adHocSubProcess", "transaction", "callActivity",
    }
    for shape in shapes:
        if shape["type"] not in INTERNAL_LABEL_TYPES:
            continue
        if not shape["label"]:
            continue
        usable_w = shape["width"] - 2 * LABEL_PADDING
        usable_h = shape["height"] - 2 * LABEL_PADDING
        text_w_1line = len(shape["label"]) * LABEL_CHAR_WIDTH

        if text_w_1line <= usable_w:
            continue

        words = shape["label"].split()
        if len(words) < 2:
            issues.append({
                "type": "label-overflow",
                "nodeId": shape["id"],
                "severity": "fail",
                "suggestion": f"Increase node {shape['id']} width to {int(text_w_1line + 2 * LABEL_PADDING)}",
            })
            continue

        max_line_w = best_2line_split_max_width(words)
        total_h_2lines = 2 * LABEL_LINE_HEIGHT

        if max_line_w <= usable_w and total_h_2lines <= usable_h:
            issues.append({
                "type": "label-overflow",
                "nodeId": shape["id"],
                "severity": "warning",
                "suggestion": f"Label of {shape['id']} should be split in 2 lines",
            })
        else:
            issues.append({
                "type": "label-overflow",
                "nodeId": shape["id"],
                "severity": "fail",
                "suggestion": f"Label of {shape['id']} too long — abbreviate or split into subprocess",
            })
    return issues


# ─────────────────────────────────────────────────────────────────────
# Detector 4 — Aspect ratio violation
# ─────────────────────────────────────────────────────────────────────

def categorize_node(node_type: str) -> str | None:
    if node_type in ("startEvent", "intermediateCatchEvent", "intermediateThrowEvent",
                     "endEvent", "boundaryEvent"):
        return "event"
    if node_type in ("task", "userTask", "serviceTask", "scriptTask",
                     "sendTask", "receiveTask", "manualTask", "businessRuleTask"):
        return "task"
    if node_type in ("subProcess", "adHocSubProcess", "transaction", "callActivity"):
        return "subProcess"
    if node_type in ("exclusiveGateway", "parallelGateway", "inclusiveGateway",
                     "eventBasedGateway", "complexGateway"):
        return "gateway"
    return None


def detect_aspect_ratio(shapes: list[dict]) -> list[dict]:
    issues = []
    for shape in shapes:
        category = categorize_node(shape["type"])
        if not category:
            continue
        expected_w, expected_h = EXPECTED_SIZES[category]
        # Tolerar overflow de label que aumentou node em <= 25%
        max_w_allowed = expected_w * 1.25
        max_h_allowed = expected_h * 1.25

        if (
            shape["width"] < expected_w * (1 - ASPECT_TOLERANCE)
            or shape["width"] > max_w_allowed
            or shape["height"] < expected_h * (1 - ASPECT_TOLERANCE)
            or shape["height"] > max_h_allowed
        ):
            issues.append({
                "type": "aspect-ratio-violation",
                "nodeId": shape["id"],
                "severity": "fail",
                "actualSize": [shape["width"], shape["height"]],
                "expectedSize": [expected_w, expected_h],
                "suggestion": f"Restore standard dimensions for {category}",
            })
    return issues


# ─────────────────────────────────────────────────────────────────────
# Detector 5 — RTL flow
# ─────────────────────────────────────────────────────────────────────

def detect_rtl_flow(shapes: list[dict], edges: list[dict]) -> list[dict]:
    shape_by_id = {s["id"]: s for s in shapes}
    seq_flows = [e for e in edges if e["source"] and e["target"]]
    if not seq_flows:
        return []

    rtl_count = 0
    rtl_edges = []
    for edge in seq_flows:
        source = shape_by_id.get(edge["source"])
        target = shape_by_id.get(edge["target"])
        if not source or not target:
            continue
        # Considerar RTL apenas se diferenca de X significativa (> 50px)
        if target["x"] < source["x"] - 50:
            rtl_count += 1
            rtl_edges.append(edge["id"])

    if not seq_flows:
        return []

    rtl_ratio = rtl_count / len(seq_flows)
    if rtl_ratio > RTL_THRESHOLD:
        return [{
            "type": "rtl-flow",
            "ratio": round(rtl_ratio, 3),
            "rtlEdges": rtl_edges,
            "severity": "fail",
            "suggestion": "Re-execute topological sort or restructure process to flow left-to-right",
        }]
    return []


# ─────────────────────────────────────────────────────────────────────
# Orquestracao
# ─────────────────────────────────────────────────────────────────────

def validate(path: str) -> dict:
    parsed = parse_bpmn(path)
    issues: list[dict] = []
    issues.extend(detect_edge_crosses_node(parsed["shapes"], parsed["edges"]))
    issues.extend(detect_edge_overlap(parsed["edges"]))
    issues.extend(detect_label_overflow(parsed["shapes"]))
    issues.extend(detect_aspect_ratio(parsed["shapes"]))
    issues.extend(detect_rtl_flow(parsed["shapes"], parsed["edges"]))

    fail_count = sum(1 for i in issues if i["severity"] == "fail")
    warning_count = sum(1 for i in issues if i["severity"] == "warning")

    return {
        "passed": fail_count == 0,
        "issuesCount": {
            "fail": fail_count,
            "warning": warning_count,
        },
        "issues": issues,
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Uso: python3 validate_bpmn_readability.py <arquivo.bpmn>", file=sys.stderr)
        return 2

    path = sys.argv[1]
    try:
        result = validate(path)
    except (ET.ParseError, OSError) as exc:
        print(f"Erro ao validar {path}: {exc}", file=sys.stderr)
        return 2

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
