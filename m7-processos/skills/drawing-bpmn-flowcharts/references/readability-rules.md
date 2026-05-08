# Regras de Legibilidade — Validadores Geometricos

7 detectores deterministicos de problemas de legibilidade visual em arquivos `.bpmn`. Implementados em `scripts/validate_bpmn_readability.py` e usados pela skill em **Fase 5** (validacao iterativa).

> **Atualizado em v1.2.0:** validador reconhece data associations (`<bpmn:dataInputAssociation>` / `<bpmn:dataOutputAssociation>`) e labels multiline (com `\n`). 2 detectores novos: `duplicate-shape-bounds` e `long-container-label`.

## Sumario

1. [Filosofia](#1-filosofia)
2. [Detector 1 — Edge crosses node](#2-detector-1--edge-crosses-node)
3. [Detector 2 — Edge overlap](#3-detector-2--edge-overlap)
4. [Detector 3 — Label overflow](#4-detector-3--label-overflow)
5. [Detector 4 — Aspect ratio violation](#5-detector-4--aspect-ratio-violation)
6. [Detector 5 — RTL flow](#6-detector-5--rtl-flow)
7. [Detector 6 — Duplicate shape bounds (v1.2)](#7-detector-6--duplicate-shape-bounds-v12)
8. [Detector 7 — Long container label (v1.2)](#8-detector-7--long-container-label-v12)
9. [Severidade e relayout](#9-severidade-e-relayout)
10. [Output JSON do validador](#10-output-json-do-validador)

---

## 1. Filosofia

Notacao BPMN correta nao basta — diagrama tem que ser **legivel**. Os 5 detectores garantem o minimo:

- Linhas nao passam por cima de nos nao-extremos
- Linhas nao se sobrepoem em segmentos extensos
- Labels cabem dentro dos containers (sem texto trincado/cortado)
- Nos mantem dimensoes padrao (sem distorcao visual)
- Fluxo principal vai da esquerda para a direita

Cada detector e **deterministico** (mesmo input → mesmo output) e roda em Python stdlib. Sem dependencia em ML, sem heuristicas fuzzy.

---

## 2. Detector 1 — Edge crosses node

### Problema

Um waypoint de edge (ou segmento entre 2 waypoints) cruza o bounding-box de um node que **nao** e nem o source nem o target do edge. Isso polui a leitura visual ("o que esse fluxo esta fazendo passando por essa atividade?").

> **Fix v1.2:** o validador agora reconhece `<bpmn:dataInputAssociation>` e `<bpmn:dataOutputAssociation>` — extrai source/target corretamente do parent task + sourceRef/targetRef interno. Antes (v1.1), data associations nao tinham endpoints e eram flagadas como "cruzando seu proprio source/target" → 14 falsos positivos no diagrama tipico com dataStores. Apos o fix, falsos positivos desaparecem; apenas issues geometricos genuinos sao reportados.

### Algoritmo

```python
MARGIN = 8  # tolerancia em pixels

def detect_edge_crosses_node(edges, nodes):
    issues = []
    for edge in edges:
        endpoints = (edge.source, edge.target)
        for i in range(len(edge.waypoints) - 1):
            seg_start = edge.waypoints[i]
            seg_end = edge.waypoints[i + 1]
            for node in nodes:
                if node.id in endpoints:
                    continue
                # Bounding-box do node com margin de seguranca
                bbox = (
                    node.x - MARGIN,
                    node.y - MARGIN,
                    node.x + node.width + MARGIN,
                    node.y + node.height + MARGIN
                )
                if segment_intersects_bbox(seg_start, seg_end, bbox):
                    issues.append({
                        "type": "edge-crosses-node",
                        "edgeId": edge.id,
                        "nodeId": node.id,
                        "severity": "fail",
                        "suggestion": f"Reroute edge {edge.id} to avoid node {node.id}"
                    })
    return issues
```

`segment_intersects_bbox(p1, p2, bbox)` usa o algoritmo Cohen-Sutherland para testar se o segmento `(p1, p2)` cruza o retangulo `bbox`.

### Estrategia de relayout

1. **Primeira iteracao:** aumentar `V_SPACING` em 30%. Isso espaca lanes verticalmente, o que muitas vezes elimina cruzamentos.
2. **Segunda iteracao:** reordenar lanes com algoritmo barycentric (lane com maior numero de conexoes para a lane vizinha vai pra cima).
3. **Terceira iteracao:** adicionar waypoint intermediario manualmente para desviar do node ofensor.

---

## 3. Detector 2 — Edge overlap

### Problema

Dois edges compartilham um segmento colinear longo (mais de 20px). Isso cria ambiguidade visual ("e uma linha so ou duas?").

### Algoritmo

```python
MIN_OVERLAP = 20  # pixels

def detect_edge_overlap(edges):
    issues = []
    for i, e1 in enumerate(edges):
        for e2 in edges[i+1:]:
            for s1_start, s1_end in pairwise(e1.waypoints):
                for s2_start, s2_end in pairwise(e2.waypoints):
                    overlap = collinear_overlap_length(s1_start, s1_end, s2_start, s2_end)
                    if overlap > MIN_OVERLAP:
                        issues.append({
                            "type": "edge-overlap",
                            "edgeIds": [e1.id, e2.id],
                            "overlapLength": overlap,
                            "severity": "fail",
                            "suggestion": f"Add intermediate waypoint to {e2.id} with ±15px offset"
                        })
    return issues
```

`collinear_overlap_length` retorna 0 se os segmentos nao sao colineares; caso contrario, retorna o comprimento do trecho compartilhado.

### Estrategia de relayout

Adicionar waypoint intermediario em um dos edges com offset de ±15px no eixo perpendicular ao segmento sobreposto. Isso "afasta" visualmente as duas linhas.

---

## 4. Detector 3 — Label overflow

### Problema

O texto do label do node nao cabe dentro do container do node (overflow). Resultado: texto trincado, cortado ou invadindo espaco visual de outro elemento.

> **Fix v1.2:** o validador agora reconhece labels multiline — quando o XML tem `\n` ou `\r\n` no `name` do node (ex: `"A3\nOrquestrador"`), o detector splita por `\n` e usa a maior linha como largura, somando todas as linhas como altura. Antes (v1.1), labels pre-quebrados eram contados como 1 linha de N chars → flagados como overflow. Apos o fix, labels que ja vem quebrados e cabem nas dimensoes do node passam direto.

### Algoritmo

```python
# Heuristica: largura media de char a 11px font (label padrao BPMN) ≈ 6.5px por char
CHAR_WIDTH = 6.5
LINE_HEIGHT = 14
INTERNAL_PADDING = 8  # padding interno do container

def detect_label_overflow(nodes):
    issues = []
    for node in nodes:
        if not node.label:
            continue
        # Largura util (subtraindo padding)
        usable_w = node.width - 2 * INTERNAL_PADDING
        usable_h = node.height - 2 * INTERNAL_PADDING

        # Estimar largura ocupada (assumindo 1 linha)
        text_width_1line = len(node.label) * CHAR_WIDTH

        if text_width_1line <= usable_w:
            continue  # cabe em 1 linha, ok

        # Tentar quebrar em 2 linhas (no espaco mais central)
        words = node.label.split()
        if len(words) < 2:
            # 1 palavra so + nao cabe = problema
            issues.append({
                "type": "label-overflow",
                "nodeId": node.id,
                "severity": "fail",
                "suggestion": f"Increase node {node.id} width to {int(text_width_1line + 2 * INTERNAL_PADDING)}"
            })
            continue

        # Calcular largura maxima das 2 linhas mais equilibradas
        max_line_width = best_2line_split_width(words, CHAR_WIDTH)
        total_height_2lines = 2 * LINE_HEIGHT

        if max_line_width <= usable_w and total_height_2lines <= usable_h:
            # Cabe em 2 linhas — emitir warning sugerindo quebra
            issues.append({
                "type": "label-overflow",
                "nodeId": node.id,
                "severity": "warning",
                "suggestion": f"Label of {node.id} should be split in 2 lines"
            })
        else:
            issues.append({
                "type": "label-overflow",
                "nodeId": node.id,
                "severity": "fail",
                "suggestion": f"Label of {node.id} too long — abbreviate or split into subprocess"
            })
    return issues
```

### Estrategia de relayout

1. **Warning (cabe em 2 linhas):** marcar o XML do label com quebra `&#10;` ou ajustar renderizacao.
2. **Fail (nao cabe):** aumentar `width` do node em 20% (de 100→120px para tasks). Recalcular waypoints dos edges conectados.

---

## 5. Detector 4 — Aspect ratio violation

### Problema

Node com dimensao fora do padrao BPMN. Isso quebra a familiaridade visual do leitor.

### Algoritmo

```python
EXPECTED_SIZES = {
    "event":   (36, 36),
    "task":    (100, 80),
    "subProcess": (120, 80),
    "gateway": (50, 50),
}
TOLERANCE = 0.01  # 1%

def detect_aspect_ratio(nodes):
    issues = []
    for node in nodes:
        category = categorize_node(node.type)  # event | task | subProcess | gateway
        expected_w, expected_h = EXPECTED_SIZES[category]
        if abs(node.width - expected_w) / expected_w > TOLERANCE \
           or abs(node.height - expected_h) / expected_h > TOLERANCE:
            issues.append({
                "type": "aspect-ratio-violation",
                "nodeId": node.id,
                "severity": "fail",
                "actualSize": [node.width, node.height],
                "expectedSize": [expected_w, expected_h],
                "suggestion": f"Restore standard dimensions for {category}"
            })
    return issues
```

**Excecao tolerada:** se o detector 3 (label-overflow) sugeriu aumentar o node, o aspect-ratio nao gera failure para esse node especifico — desde que a proporcao mantenha (W/H = expected_W/expected_H ± 10%).

### Estrategia de relayout

Restaurar dimensao padrao (`element_size(node.type)`). Recalcular waypoints dos edges conectados.

---

## 6. Detector 5 — RTL flow

### Problema

Mais de 30% dos sequence flows tem `source.x > target.x` (excluindo loops explicitos). Isso indica fluxo "para tras" que confunde o leitor.

### Algoritmo

```python
RTL_THRESHOLD = 0.3  # 30%

def detect_rtl_flow(edges, nodes):
    sequence_flows = [e for e in edges if e.type == "sequenceFlow"]
    if not sequence_flows:
        return []

    rtl_count = 0
    rtl_edges = []
    for edge in sequence_flows:
        source = nodes[edge.source]
        target = nodes[edge.target]
        # Loops detectaveis: target tem rank < source (ja no campo rank do layout)
        if target.x < source.x and not is_loop_back(edge):
            rtl_count += 1
            rtl_edges.append(edge.id)

    rtl_ratio = rtl_count / len(sequence_flows)
    if rtl_ratio > RTL_THRESHOLD:
        return [{
            "type": "rtl-flow",
            "ratio": rtl_ratio,
            "rtlEdges": rtl_edges,
            "severity": "fail",
            "suggestion": "Re-execute topological sort or restructure process to flow left-to-right"
        }]
    return []
```

`is_loop_back(edge)` verifica se o edge faz parte de um ciclo conhecido (source pertence a um SCC que contem o target).

### Estrategia de relayout

Re-executar topological sort com tie-breaking diferente (ordem do JSON original). Se nao resolver em 1 iteracao, registrar como issue residual — provavelmente problema estrutural do mapeamento.

---

## 7. Detector 6 — Duplicate shape bounds (v1.2)

### Problema

2+ shapes com bounds completamente identicas. Caso classico: 2 `<bpmn:dataStoreReference>` apontando para o mesmo `<bpmn:dataStore>` global (cross-pool data sharing) recebendo as mesmas coordenadas → 2 cilindros sobrepostos no diagrama, leitura impossivel.

### Algoritmo

```python
def detect_duplicate_shape_bounds(shapes):
    issues = []
    flow_shapes = [s for s in shapes if s["type"] not in ("participant", "lane")]
    seen = {}
    for shape in flow_shapes:
        key = (shape["x"], shape["y"], shape["width"], shape["height"])
        if key in seen:
            issues.append({
                "type": "duplicate-shape-bounds",
                "shapeIds": [seen[key], shape["id"]],
                "bounds": list(key),
                "severity": "fail",
                "suggestion": "Assign distinct positions (typical: 1 dataStoreReference per pool/lane)"
            })
        else:
            seen[key] = shape["id"]
    return issues
```

### Estrategia de relayout

Indica problema arquitetural — nao tem fix automatico no auto-layout. Recomendacao no descritivo: "Posicionar cada referencia em sua propria lane, ou usar 1 unica referencia se o caso de uso permite".

---

## 8. Detector 7 — Long container label (v1.2)

### Problema

Pool labels > 30 chars e lane labels > 25 chars sao truncados pelo bpmn-js viewer quando o container e alto (rotacao vertical da label trunca o texto na barra esquerda). Resultado visual: "Maquina/Inglesia - Plataforma de Dados" com overlap entre label do pool e label da lane.

### Algoritmo

```python
POOL_LABEL_MAX = 30
LANE_LABEL_MAX = 25

def detect_long_container_label(shapes):
    issues = []
    for shape in shapes:
        if shape["type"] == "participant" and len(shape["label"]) > POOL_LABEL_MAX:
            issues.append({
                "type": "long-container-label",
                "shapeId": shape["id"],
                "labelLength": len(shape["label"]),
                "severity": "warning",
                "suggestion": "Abbreviate to avoid truncation in bpmn-js"
            })
        elif shape["type"] == "lane" and len(shape["label"]) > LANE_LABEL_MAX:
            issues.append({...})
    return issues
```

### Estrategia de relayout

Severity: warning (nao bloqueia construcao). Sugestao: abreviar manualmente. Esse e um problema de **conteudo**, nao layout — auto-layout nao tem como adivinhar a abreviacao desejada.

### Limites recomendados

| Container | Max chars |
|---|---|
| Pool | 30 |
| Lane | 25 |

Para textos mais longos, usar siglas + tooltip externo ou virar subprocess.

---

## 9. Severidade e relayout

| Severidade | Significado | Comportamento da skill |
|---|---|---|
| `pass` | Regra atendida | Continua |
| `warning` | Problema parcial, recomendacao | Registra no descritivo, nao bloqueia |
| `fail` | Violacao critica | Aplica estrategia de relayout, retry (max 3 iter) |

### Criterio de parada (max 3 iteracoes)

```python
for iteracao in range(3):
    layout = compute_auto_layout(input)
    bpmn = render_xml(input, layout, m7_styling)
    result = validate_bpmn_readability(bpmn)
    if result.passed:
        return bpmn
    apply_relayout_strategy(layout, result.issues)
# Se chegou aqui, escrever issues residuais no descritivo
return bpmn_with_residual_issues
```

Apos 3 iteracoes sem convergir, **NAO joga erro** — escreve o `.bpmn` mesmo assim e registra issues residuais no `-descritivo.md` com sugestao de acao manual ao usuario.

---

## 10. Output JSON do validador

`scripts/validate_bpmn_readability.py` produz JSON deterministico:

```json
{
  "passed": false,
  "iteration": 1,
  "issuesCount": {
    "fail": 2,
    "warning": 1,
    "pass": 23
  },
  "issues": [
    {
      "type": "edge-crosses-node",
      "edgeId": "e7",
      "nodeId": "n4",
      "severity": "fail",
      "suggestion": "Reroute edge e7 to avoid node n4"
    },
    {
      "type": "label-overflow",
      "nodeId": "n2",
      "severity": "warning",
      "suggestion": "Label of n2 should be split in 2 lines"
    },
    {
      "type": "edge-overlap",
      "edgeIds": ["e2", "e8"],
      "overlapLength": 45,
      "severity": "fail",
      "suggestion": "Add intermediate waypoint to e8 with ±15px offset"
    }
  ]
}
```

A skill consome este JSON em **Fase 5** para decidir entre:
- `passed: true` → ir para Fase 6 (validacao final de notacao)
- `passed: false` E `iteration < 3` → aplicar estrategia, re-rodar
- `passed: false` E `iteration == 3` → registrar issues residuais no descritivo, ir para Fase 7

---

## Notas finais

- Detectores sao **conservadores**: preferem flagear um false-positive a deixar passar um real-positive
- A tolerancia em `aspect-ratio-violation` (1%) e estrita porque o auto-layout sempre gera dimensoes exatas
- Para diagramas com mais de 30 nodes, o detector `edge-overlap` pode ficar lento (O(N² × M²)). Otimizar com spatial index se necessario
- Usuario pode editar o `.bpmn` manualmente em Camunda Modeler — a skill nao re-valida apos edicao manual
