# Algoritmo de Auto-Layout — BPMN 2.0 Diagram Interchange

Algoritmo deterministico para calcular coordenadas de shapes (`<bpmndi:BPMNShape>`) e waypoints de edges (`<bpmndi:BPMNEdge>`) em arquivos `.bpmn`. Implementado em `scripts/compute_auto_layout.py`.

## Sumario

1. [Constantes geometricas](#1-constantes-geometricas)
2. [Dimensoes por tipo de elemento](#2-dimensoes-por-tipo-de-elemento)
3. [Pseudocodigo (6 passos)](#3-pseudocodigo-6-passos)
4. [Estrategias de relayout](#4-estrategias-de-relayout)
5. [Saida do algoritmo](#5-saida-do-algoritmo)
6. [Implementacao de referencia](#6-implementacao-de-referencia)

---

## 1. Constantes geometricas

Todas as constantes em pixels. Hardcoded em `scripts/compute_auto_layout.py` — nao alterar sem motivo justificado.

```python
# Spacing (entre nodes)
H_SPACING = 150       # distancia horizontal entre centros de nodes (por rank)
V_SPACING = 100       # distancia vertical entre centros de nodes (mesma lane/rank)

# Margens
LEFT_MARGIN = 80      # do header da lane ate o primeiro node
TOP_MARGIN = 50       # do header do pool ate o conteudo

# Headers
POOL_HEADER_HEIGHT = 30   # altura do header horizontal do pool
LANE_HEADER_WIDTH = 30    # largura do header vertical da lane

# Pool base
POOL_X = 160          # margem esquerda do pool no canvas
POOL_Y = 0            # primeiro pool comeca no topo
INTER_POOL_GAP = 60   # gap vertical entre pools (se multiplos)
```

## 2. Dimensoes por tipo de elemento

```python
# Eventos: circulos
EVENT_W, EVENT_H = 36, 36

# Atividades: retangulos com cantos arredondados
TASK_W, TASK_H = 100, 80
SUBPROC_W, SUBPROC_H = 120, 80

# Gateways: losangos
GATEWAY_W, GATEWAY_H = 50, 50
```

Funcao de selecao:

```python
def element_size(node_type: str) -> tuple[int, int]:
    """Retorna (width, height) baseado no tipo BPMN do node."""
    if node_type.startswith(("startEvent", "intermediateEvent", "endEvent")):
        return (EVENT_W, EVENT_H)
    if node_type.endswith("Gateway"):  # exclusiveGateway, parallelGateway, etc.
        return (GATEWAY_W, GATEWAY_H)
    if node_type == "subProcess":
        return (SUBPROC_W, SUBPROC_H)
    return (TASK_W, TASK_H)  # task, userTask, serviceTask, etc.
```

---

## 3. Pseudocodigo (6 passos)

### Passo 1 — Topological Sort e Rank Assignment

Atribui um `rank` (inteiro) a cada node, baseado na distancia maxima a partir dos start events.

```
ranks = {}
queue = [start_events]   # nodes do tipo startEvent*
para cada start_event s:
    ranks[s] = 0

# BFS iterativo
enquanto queue nao vazio:
    n = queue.pop()
    para cada successor s de n (via outgoing edges):
        candidate_rank = ranks[n] + 1
        if s nao em ranks OR candidate_rank > ranks[s]:
            ranks[s] = candidate_rank
            queue.push(s)
```

**Observacoes:**
- Usar `max()` em caso de multiplos predecessores (rank do node = maior rank dos predecessores + 1)
- Boundary events nao recebem rank (herdam posicao da activity hospedeira)
- Loops (cycles) sao detectados e tratados: o rank do node de retorno e fixado na primeira visita; flows de loop-back nao incrementam rank

### Passo 2 — Agrupar por Lane × Rank

```
lane_rank_nodes = {}   # {lane_id: {rank: [node_ids]}}
para cada node N:
    if N e boundary event: skip   # boundary events nao entram em layout normal
    lane_rank_nodes[N.lane][ranks[N]].append(N.id)
```

### Passo 3 — Calcular alturas das lanes

```
lane_heights = {}
para cada lane L:
    max_nodes_in_any_rank = max(|lane_rank_nodes[L][r]|) para todos r
    lane_heights[L] = max(max_nodes_in_any_rank * V_SPACING, 120)
```

A altura minima de 120px garante leitura confortavel mesmo em lanes com 1 unico node.

### Passo 4 — Calcular Y das lanes (dentro do pool)

```
para cada pool P:
    current_y = pool.y + POOL_HEADER_HEIGHT
    para cada lane L em P (ordem do JSON):
        lane.y = current_y
        lane.height = lane_heights[L]
        lane.x = pool.x
        current_y += lane.height
```

### Passo 5 — Calcular X e Y dos nodes

```
para cada node N (exceto boundary events):
    (w, h) = element_size(N.type)

    # X: baseado no rank
    N.x = pool.x + LANE_HEADER_WIDTH + LEFT_MARGIN + (ranks[N] * H_SPACING) - w/2

    # Y: centralizado na lane, distribuido se multiplos nodes no mesmo rank
    nodes_aqui = lane_rank_nodes[N.lane][ranks[N]]
    idx = nodes_aqui.index(N.id)
    total = len(nodes_aqui)

    lane_center = lane[N.lane].y + lane[N.lane].height / 2
    first_y = lane_center - ((total - 1) * V_SPACING) / 2
    N.y = first_y + (idx * V_SPACING) - h/2
```

**Boundary events:** posicao calculada apos os hospedeiros:
```
para cada boundary event B com attachedTo = A:
    (aw, ah) = element_size(A.type)
    (bw, bh) = element_size(B.type)
    # Posiciona no canto inferior direito da activity
    B.x = A.x + aw - bw/2
    B.y = A.y + ah - bh/2
```

### Passo 6 — Calcular dimensoes do pool

```
max_rank = max(ranks[N]) para todos N no pool
pool.width = LANE_HEADER_WIDTH + LEFT_MARGIN + (max_rank + 1) * H_SPACING + LEFT_MARGIN
pool.height = POOL_HEADER_HEIGHT + sum(lane_heights[L]) para todas L no pool

para cada lane L em pool:
    lane.width = pool.width
```

### Passo 7 — Gerar waypoints dos edges

```
para cada edge E (sequenceFlow, messageFlow, association):
    source = nodes[E.source]
    target = nodes[E.target]
    (sw, sh) = element_size(source.type)
    (tw, th) = element_size(target.type)

    # Saida pelo lado direito do source
    wp1 = (source.x + sw, source.y + sh/2)

    # Entrada pelo lado esquerdo do target
    wp2 = (target.x, target.y + th/2)

    # Se cross-lane (Y diferente), adicionar waypoint intermediario
    if abs(wp1.y - wp2.y) > 10:
        mid_x = (wp1.x + wp2.x) / 2
        waypoints = [wp1, (mid_x, wp1.y), (mid_x, wp2.y), wp2]
    else:
        waypoints = [wp1, wp2]

    E.waypoints = waypoints
```

**Casos especiais:**
- **Loop-back** (target.x < source.x): waypoint intermediario *acima* dos nodes para evitar cruzar atividades:
  ```
  waypoints = [wp1, (wp1.x, lane.y - 20), (wp2.x, lane.y - 20), wp2]
  ```
- **Self-loop** (source = target): nao implementado nesta versao do algoritmo

---

## 4. Estrategias de relayout

Quando `validate_bpmn_readability.py` retorna `passed: false`, aplicar uma das estrategias abaixo conforme o tipo de issue. Maximo **3 iteracoes** total.

### 4.1 Issue: edge-crosses-node

**Diagnostico:** algum waypoint cruza bounding-box de node nao-extremo.

**Estrategia 1 — Aumentar V_SPACING:**
```python
V_SPACING = int(V_SPACING * 1.3)   # +30%
recalcular Passos 3, 4, 5, 7
```

**Estrategia 2 — Reordenar lanes (barycentric):**
```python
# Para cada lane, calcular baricentro dos predecessores em ranks adjacentes
# Reordenar lanes verticalmente por baricentro
# Recalcular Passos 4, 5, 7
```

### 4.2 Issue: edge-overlap

**Diagnostico:** dois edges compartilham segmento colinear > 20px.

**Estrategia — Adicionar waypoint intermediario com offset:**
```python
para cada par (e1, e2) sobreposto:
    # Identificar segmento comum
    # Adicionar waypoint em e2 deslocado em ±15px no eixo perpendicular
    # Re-rodar validacao
```

### 4.3 Issue: label-overflow

**Diagnostico:** label do node excede largura interior em > 5%.

**Estrategia 1 — Quebrar label em 2 linhas:**
```python
# Dividir label em palavras, encontrar ponto de quebra mais equilibrado
# Manter dimensao do node, apenas re-renderizar o XML com label multilinha
```

**Estrategia 2 — Aumentar dimensao do node:**
```python
# Para tasks: TASK_W = 120, TASK_H = 90 (apenas para o node afetado)
# Recalcular waypoints dos edges conectados
```

### 4.4 Issue: aspect-ratio-violation

**Diagnostico:** node com dimensao fora do padrao (apos manipulacao previa).

**Estrategia — Restaurar dimensao padrao:**
```python
node.width, node.height = element_size(node.type)
recalcular waypoints dos edges conectados
```

### 4.5 Issue: rtl-flow

**Diagnostico:** > 30% dos sequence flows tem `source.x > target.x` (excluindo loops).

**Estrategia — Re-executar topological sort com tie-breaking diferente:**
```python
# Em caso de empate de rank, ordenar por posicao no JSON original
# Isso pode resolver flows "para tras" causados por ordem ambigua
```

Se a estrategia nao resolver em 1 iteracao, registrar issue residual.

---

## 5. Saida do algoritmo

`compute_auto_layout.py` produz JSON com a seguinte estrutura:

```json
{
  "pools": [
    {
      "id": "pool1",
      "x": 160, "y": 0, "width": 1090, "height": 470
    }
  ],
  "lanes": [
    {
      "id": "lane1",
      "x": 160, "y": 30, "width": 1090, "height": 220
    },
    {
      "id": "lane2",
      "x": 160, "y": 250, "width": 1090, "height": 220
    }
  ],
  "nodes": [
    {
      "id": "n1",
      "x": 252, "y": 122, "width": 36, "height": 36
    },
    {
      "id": "n2",
      "x": 370, "y": 100, "width": 100, "height": 80
    }
  ],
  "edges": [
    {
      "id": "e1",
      "waypoints": [
        {"x": 288, "y": 140},
        {"x": 370, "y": 140}
      ]
    },
    {
      "id": "e2",
      "waypoints": [
        {"x": 470, "y": 140},
        {"x": 495, "y": 140},
        {"x": 495, "y": 290},
        {"x": 520, "y": 290}
      ]
    }
  ]
}
```

A skill consome este JSON em **Fase 5** (renderizacao) para popular o `<bpmndi:BPMNDiagram>` no `.bpmn`.

---

## 6. Implementacao de referencia

A implementacao canonica esta em [`scripts/compute_auto_layout.py`](../scripts/compute_auto_layout.py):

- Stdlib only (`json`, `sys`, `math`, `collections.defaultdict`, `collections.deque`)
- Recebe path do JSON de input via `sys.argv[1]`
- Imprime layout JSON em stdout
- Exit code 0 em sucesso, 1 em erro

**Uso:**

```bash
python3 scripts/compute_auto_layout.py exemplo-input.json > exemplo-layout.json
```

**Validacao do script:**

```bash
# Testar contra o exemplo
cd skills/drawing-bpmn-flowcharts/
python3 scripts/compute_auto_layout.py examples/exemplo-onboarding-input.json | python3 -m json.tool
```

---

## Notas finais

- O algoritmo gera coordenadas "good enough" — usuario pode ajustar manualmente em Camunda Modeler ou bpmn.io
- Para casos complexos (>30 nodes), considerar particionar em subprocesses antes de aplicar layout
- O algoritmo nao trata milestones (divisao vertical) — extensao futura
- Auto-layout e deterministico: mesmo input → mesmo output. Util para git diffs.
