# BPMN 2.0 XML Reference — Geracao de Arquivos .bpmn

Referencia completa para Claude gerar arquivos `.bpmn` validos a partir do JSON schema de input. Inclui namespaces, mapeamento de elementos, padroes estruturais, algoritmo de auto-layout e exemplo anotado.

---

## 1. Namespaces e Elemento Raiz

Todo arquivo `.bpmn` comeca com esta declaracao exata:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  id="Definitions_1"
  targetNamespace="http://bpmn.io/schema/bpmn"
  exporter="Claude Code"
  exporterVersion="1.0">

  <!-- conteudo aqui -->

</bpmn:definitions>
```

| Namespace | Prefixo | Uso |
|-----------|---------|-----|
| BPMN 2.0 Model | `bpmn:` | Todos os elementos de processo (events, tasks, gateways, flows) |
| BPMN Diagram Interchange | `bpmndi:` | Elementos visuais (BPMNDiagram, BPMNPlane, BPMNShape, BPMNEdge) |
| Diagram Common | `dc:` | Dimensoes e posicoes (`Bounds`) |
| Diagram Interchange | `di:` | Waypoints para conexoes |
| XML Schema Instance | `xsi:` | Tipagem de expressoes condicionais |

---

## 2. Mapeamento Completo: JSON type → XML Element

### 2.1 Events

| JSON `type` | XML Element | Filhos Obrigatorios | Atributos |
|-------------|-------------|---------------------|-----------|
| `startEvent` | `<bpmn:startEvent>` | `<bpmn:outgoing>` | `id`, `name` |
| `startEvent-message` | `<bpmn:startEvent>` | `<bpmn:messageEventDefinition/>` + `<bpmn:outgoing>` | `id`, `name` |
| `startEvent-timer` | `<bpmn:startEvent>` | `<bpmn:timerEventDefinition/>` + `<bpmn:outgoing>` | `id`, `name` |
| `startEvent-signal` | `<bpmn:startEvent>` | `<bpmn:signalEventDefinition/>` + `<bpmn:outgoing>` | `id`, `name` |
| `intermediateEvent` | `<bpmn:intermediateCatchEvent>` | `<bpmn:incoming>` + `<bpmn:outgoing>` | `id`, `name` |
| `intermediateEvent-message` | `<bpmn:intermediateCatchEvent>` | `<bpmn:messageEventDefinition/>` + incoming/outgoing | `id`, `name` |
| `intermediateEvent-timer` | `<bpmn:intermediateCatchEvent>` | `<bpmn:timerEventDefinition/>` + incoming/outgoing | `id`, `name` |
| `intermediateEvent-error` (sem `attachedTo`) | `<bpmn:intermediateCatchEvent>` | `<bpmn:errorEventDefinition/>` + incoming/outgoing | `id`, `name` |
| `intermediateEvent-error` (com `attachedTo`) | `<bpmn:boundaryEvent>` | `<bpmn:errorEventDefinition/>` + `<bpmn:outgoing>` | `id`, `name`, `attachedToRef`, `cancelActivity="true"` |
| `intermediateEvent-signal` | `<bpmn:intermediateCatchEvent>` | `<bpmn:signalEventDefinition/>` + incoming/outgoing | `id`, `name` |
| `endEvent` | `<bpmn:endEvent>` | `<bpmn:incoming>` | `id`, `name` |
| `endEvent-message` | `<bpmn:endEvent>` | `<bpmn:messageEventDefinition/>` + `<bpmn:incoming>` | `id`, `name` |
| `endEvent-error` | `<bpmn:endEvent>` | `<bpmn:errorEventDefinition/>` + `<bpmn:incoming>` | `id`, `name` |
| `endEvent-terminate` | `<bpmn:endEvent>` | `<bpmn:terminateEventDefinition/>` + `<bpmn:incoming>` | `id`, `name` |

### 2.2 Activities

| JSON `type` | XML Element | Filhos Obrigatorios | Atributos |
|-------------|-------------|---------------------|-----------|
| `task` | `<bpmn:task>` | `<bpmn:incoming>` + `<bpmn:outgoing>` | `id`, `name` |
| `userTask` | `<bpmn:userTask>` | incoming + outgoing | `id`, `name` |
| `serviceTask` | `<bpmn:serviceTask>` | incoming + outgoing | `id`, `name` |
| `scriptTask` | `<bpmn:scriptTask>` | incoming + outgoing | `id`, `name` |
| `sendTask` | `<bpmn:sendTask>` | incoming + outgoing | `id`, `name` |
| `receiveTask` | `<bpmn:receiveTask>` | incoming + outgoing | `id`, `name` |
| `subProcess` | `<bpmn:subProcess>` | incoming + outgoing | `id`, `name` |

### 2.3 Gateways

| JSON `type` | XML Element | Filhos Obrigatorios | Atributos |
|-------------|-------------|---------------------|-----------|
| `exclusiveGateway` | `<bpmn:exclusiveGateway>` | incoming + outgoing | `id`, `name`, `default` (id do flow default, se houver) |
| `parallelGateway` | `<bpmn:parallelGateway>` | incoming + outgoing | `id`, `name` |
| `inclusiveGateway` | `<bpmn:inclusiveGateway>` | incoming + outgoing | `id`, `name` |
| `eventBasedGateway` | `<bpmn:eventBasedGateway>` | incoming + outgoing | `id`, `name` |

### 2.4 Connections

| JSON `type` | XML Element | Escopo | Atributos |
|-------------|-------------|--------|-----------|
| `sequenceFlow` | `<bpmn:sequenceFlow>` | Dentro de `<bpmn:process>` | `id`, `name` (opcional), `sourceRef`, `targetRef` |
| `messageFlow` | `<bpmn:messageFlow>` | Dentro de `<bpmn:collaboration>` | `id`, `name` (opcional), `sourceRef`, `targetRef` |
| `association` | `<bpmn:association>` | Dentro de `<bpmn:process>` | `id`, `sourceRef`, `targetRef` |

### 2.5 Artifacts

| JSON `type` | XML Element | Filhos | Atributos |
|-------------|-------------|--------|-----------|
| `dataObject` | `<bpmn:dataObjectReference>` | — | `id`, `name` |
| `dataStore` | `<bpmn:dataStoreReference>` | — | `id`, `name` |
| `textAnnotation` | `<bpmn:textAnnotation>` | `<bpmn:text>label</bpmn:text>` | `id` |
| `group` | `<bpmn:group>` | — | `id`, `categoryValueRef` |

---

## 3. Padroes Estruturais

### 3.1 Collaboration + Participants + Processes

Quando ha pools no JSON, a estrutura segue este padrao:

```xml
<bpmn:collaboration id="Collaboration_1">
  <!-- Um participant por pool -->
  <bpmn:participant id="{pool.id}_participant" name="{pool.name}" processRef="{pool.id}" />

  <!-- Message flows entre pools (se houver) -->
  <bpmn:messageFlow id="{edge.id}" name="{edge.label}" sourceRef="{edge.source}" targetRef="{edge.target}" />
</bpmn:collaboration>

<!-- Um process por pool -->
<bpmn:process id="{pool.id}" name="{pool.name}" isExecutable="{pool.isExecutable || false}">
  <!-- conteudo do processo -->
</bpmn:process>
```

**Regra**: Mesmo com um unico pool, usar o padrao collaboration/participant para consistencia.

### 3.2 Lane Sets

Dentro de cada `<bpmn:process>`:

```xml
<bpmn:laneSet id="LaneSet_{pool.id}">
  <bpmn:lane id="{lane.id}" name="{lane.name}">
    <!-- Lista de IDs dos nodes NESTA lane -->
    <bpmn:flowNodeRef>{node.id}</bpmn:flowNodeRef>
    <bpmn:flowNodeRef>{node.id}</bpmn:flowNodeRef>
  </bpmn:lane>
</bpmn:laneSet>
```

**Regra critica**: Lanes NAO contam os elementos do node — apenas referenciam seus IDs via `<bpmn:flowNodeRef>`. Os elements ficam soltos dentro de `<bpmn:process>`.

### 3.3 Incoming/Outgoing (referencia bidirecional)

Cada flow node DEVE listar suas conexoes:

```xml
<bpmn:userTask id="n2" name="Analisar solicitacao">
  <bpmn:incoming>e1</bpmn:incoming>   <!-- ID do sequenceFlow que chega -->
  <bpmn:outgoing>e2</bpmn:outgoing>   <!-- ID do sequenceFlow que sai -->
</bpmn:userTask>

<bpmn:sequenceFlow id="e1" sourceRef="n1" targetRef="n2" />
<bpmn:sequenceFlow id="e2" sourceRef="n2" targetRef="n3" />
```

**Regras:**
- Start events: apenas `<bpmn:outgoing>`
- End events: apenas `<bpmn:incoming>`
- Todos os demais: ambos `<bpmn:incoming>` e `<bpmn:outgoing>`
- Um node pode ter multiplos incoming e/ou outgoing (ex: gateways)

### 3.4 XOR Gateway com Default Path

Quando um edge tem `isDefault: true`:

```xml
<bpmn:exclusiveGateway id="g1" name="Aprovado?" default="e4">
  <bpmn:incoming>e3</bpmn:incoming>
  <bpmn:outgoing>e4</bpmn:outgoing>  <!-- default path -->
  <bpmn:outgoing>e5</bpmn:outgoing>  <!-- conditional path -->
</bpmn:exclusiveGateway>

<!-- Flow default: SEM conditionExpression -->
<bpmn:sequenceFlow id="e4" name="Nao" sourceRef="g1" targetRef="n4" />

<!-- Flow condicional: COM conditionExpression -->
<bpmn:sequenceFlow id="e5" name="Sim" sourceRef="g1" targetRef="n5">
  <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">aprovado == true</bpmn:conditionExpression>
</bpmn:sequenceFlow>
```

### 3.5 Conditional Flows

Quando um edge tem campo `condition`:

```xml
<bpmn:sequenceFlow id="{edge.id}" name="{edge.label}" sourceRef="{edge.source}" targetRef="{edge.target}">
  <bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">{edge.condition}</bpmn:conditionExpression>
</bpmn:sequenceFlow>
```

Se o edge NAO tem `condition` e NAO e `isDefault`, emitir `<bpmn:sequenceFlow>` sem filhos.

### 3.6 Boundary Events

Quando um node tem campo `attachedTo`:

```xml
<bpmn:boundaryEvent id="{node.id}" name="{node.label}" attachedToRef="{node.attachedTo}" cancelActivity="true">
  <bpmn:outgoing>{edge.id}</bpmn:outgoing>
  <bpmn:errorEventDefinition id="{node.id}_evtdef" />
</bpmn:boundaryEvent>
```

**Regras:**
- Boundary events NAO tem `<bpmn:incoming>` — sao triggered pela activity
- Boundary events TEM `<bpmn:outgoing>` — para o fluxo de excecao
- O `attachedToRef` aponta para o ID da activity que "hospeda" o boundary event
- Boundary events NAO aparecem no `<bpmn:flowNodeRef>` da lane — eles herdam a posicao da activity

### 3.7 Documentation

Quando um node tem campo `description`:

```xml
<bpmn:userTask id="n2" name="Analisar solicitacao">
  <bpmn:documentation>{node.description}</bpmn:documentation>
  <bpmn:incoming>e1</bpmn:incoming>
  <bpmn:outgoing>e2</bpmn:outgoing>
</bpmn:userTask>
```

`<bpmn:documentation>` e sempre o primeiro filho do element.

---

## 4. Algoritmo de Auto-Layout

O arquivo `.bpmn` inclui uma secao `<bpmndi:BPMNDiagram>` com coordenadas x/y/width/height para cada elemento. Este algoritmo gera coordenadas deterministicas "good enough" — o usuario pode ajustar manualmente no Camunda Modeler.

### 4.1 Constantes

```
POOL_HEADER_HEIGHT = 30      // altura do header horizontal do pool
LANE_HEADER_WIDTH  = 30      // largura do header vertical da lane
H_SPACING          = 150     // distancia horizontal entre centros de nodes (por rank)
V_SPACING          = 100     // distancia vertical entre centros de nodes (mesma lane/rank)
LEFT_MARGIN        = 80      // margem do header da lane ate o primeiro node
TOP_MARGIN         = 50      // margem do header do pool ate o conteudo

// Dimensoes dos elementos
EVENT_W  = 36    EVENT_H  = 36
TASK_W   = 100   TASK_H   = 80
GATEWAY_W = 50   GATEWAY_H = 50
SUBPROC_W = 120  SUBPROC_H = 80
```

### 4.2 Determinar Dimensoes por Tipo

```
function elementSize(type):
  if type starts with "startEvent" or "intermediateEvent" or "endEvent":
    return (EVENT_W, EVENT_H)
  if type starts with "exclusive" or "parallel" or "inclusive" or "eventBased":
    return (GATEWAY_W, GATEWAY_H)
  if type == "subProcess":
    return (SUBPROC_W, SUBPROC_H)
  return (TASK_W, TASK_H)   // task, userTask, serviceTask, etc.
```

### 4.3 Algoritmo Passo a Passo

**Passo 1 — Topological Sort e Rank Assignment**

```
ranks = {}
Processar nodes em ordem topologica (BFS a partir dos start events):
  - Start events: rank = 0
  - Para cada node N com predecessores P1, P2, ...:
    rank[N] = max(rank[P1], rank[P2], ...) + 1
```

**Passo 2 — Agrupar por Lane e Rank**

```
Para cada pool:
  Para cada lane L no pool:
    Para cada rank R:
      laneRankNodes[L][R] = nodes nesta lane com este rank
```

**Passo 3 — Calcular Altura de Cada Lane**

```
Para cada lane L:
  maxNodesInAnyRank = max(|laneRankNodes[L][R]|) para todos R
  laneHeight = max(maxNodesInAnyRank * V_SPACING, 120)
```

**Passo 4 — Calcular Coordenadas Y das Lanes**

```
Para cada pool P:
  currentY = pool.y + POOL_HEADER_HEIGHT
  Para cada lane L em P (na ordem do JSON):
    lane.y = currentY
    lane.height = laneHeight[L]
    currentY += laneHeight[L]
```

**Passo 5 — Calcular Coordenadas dos Nodes**

```
Para cada node N:
  (w, h) = elementSize(N.type)

  // X: baseado no rank
  N.x = pool.x + LANE_HEADER_WIDTH + LEFT_MARGIN + (rank[N] * H_SPACING) - w/2

  // Y: centrado na lane, distribuido se multiplos nodes no mesmo rank
  nodesInThisRankAndLane = laneRankNodes[N.lane][rank[N]]
  indexInGroup = posicao de N neste grupo
  totalInGroup = |nodesInThisRankAndLane|

  laneCenter = lane[N.lane].y + lane[N.lane].height / 2
  firstY = laneCenter - ((totalInGroup - 1) * V_SPACING) / 2
  N.y = firstY + (indexInGroup * V_SPACING) - h/2
```

**Passo 6 — Calcular Dimensoes do Pool**

```
maxRank = max(rank[N]) para todos N no pool
pool.width = LANE_HEADER_WIDTH + LEFT_MARGIN + (maxRank + 1) * H_SPACING + LEFT_MARGIN
pool.height = POOL_HEADER_HEIGHT + sum(laneHeight[L]) para todas lanes L no pool

Cada lane:
  lane.width = pool.width
  lane.x = pool.x
```

**Passo 7 — Gerar Waypoints dos Edges**

```
Para cada sequenceFlow/messageFlow:
  source = node do sourceRef
  target = node do targetRef
  (sw, sh) = elementSize(source.type)
  (tw, th) = elementSize(target.type)

  // Saida pelo lado direito do source
  wp1.x = source.x + sw
  wp1.y = source.y + sh/2

  // Entrada pelo lado esquerdo do target
  wp2.x = target.x
  wp2.y = target.y + th/2

  // Se cross-lane (wp1.y != wp2.y), adicionar waypoint intermediario
  if |wp1.y - wp2.y| > 10:
    midX = (wp1.x + wp2.x) / 2
    waypoints = [wp1, (midX, wp1.y), (midX, wp2.y), wp2]
  else:
    waypoints = [wp1, wp2]
```

### 4.4 Pool Base Position

```
pool.x = 160    // margem esquerda do diagrama
pool.y = 0      // primeiro pool comeca no topo

// Se multiplos pools:
pool[0].y = 0
pool[1].y = pool[0].y + pool[0].height + 60   // gap entre pools
```

---

## 5. Geracao do BPMNDiagram

### 5.1 BPMNShape para Containers

```xml
<!-- Pool -->
<bpmndi:BPMNShape id="{pool.id}_participant_di" bpmnElement="{pool.id}_participant" isHorizontal="true">
  <dc:Bounds x="{pool.x}" y="{pool.y}" width="{pool.width}" height="{pool.height}" />
</bpmndi:BPMNShape>

<!-- Lane -->
<bpmndi:BPMNShape id="{lane.id}_di" bpmnElement="{lane.id}" isHorizontal="true">
  <dc:Bounds x="{lane.x}" y="{lane.y}" width="{lane.width}" height="{lane.height}" />
</bpmndi:BPMNShape>
```

### 5.2 BPMNShape para Flow Nodes

```xml
<bpmndi:BPMNShape id="{node.id}_di" bpmnElement="{node.id}">
  <dc:Bounds x="{node.x}" y="{node.y}" width="{node.width}" height="{node.height}" />
</bpmndi:BPMNShape>
```

Para gateways XOR, adicionar `isMarkerVisible="true"`:
```xml
<bpmndi:BPMNShape id="{node.id}_di" bpmnElement="{node.id}" isMarkerVisible="true">
```

### 5.3 BPMNEdge para Connections

```xml
<bpmndi:BPMNEdge id="{edge.id}_di" bpmnElement="{edge.id}">
  <di:waypoint x="{wp1.x}" y="{wp1.y}" />
  <di:waypoint x="{wp2.x}" y="{wp2.y}" />
  <!-- waypoints adicionais se cross-lane -->
</bpmndi:BPMNEdge>
```

---

## 6. Exemplo Anotado Completo

Processo "Exemplo de Solicitacao" com 1 pool, 2 lanes, 7 nodes, 7 edges.

**JSON de input:**
```json
{
  "metadata": {
    "title": "Processo de Solicitacao",
    "level": "N3",
    "version": "1.0",
    "date": "2026-02-27",
    "author": "Claude Code"
  },
  "pools": [{
    "id": "pool1",
    "name": "Empresa",
    "lanes": [
      { "id": "lane1", "name": "Solicitante" },
      { "id": "lane2", "name": "Aprovador" }
    ]
  }],
  "nodes": [
    { "id": "n1", "type": "startEvent",        "label": "Inicio",                "lane": "lane1", "pool": "pool1" },
    { "id": "n2", "type": "userTask",           "label": "Preencher solicitacao", "lane": "lane1", "pool": "pool1", "description": "Solicitante preenche formulario com dados da solicitacao" },
    { "id": "n3", "type": "userTask",           "label": "Analisar solicitacao",  "lane": "lane2", "pool": "pool1" },
    { "id": "n4", "type": "exclusiveGateway",   "label": "Aprovado?",            "lane": "lane2", "pool": "pool1" },
    { "id": "n5", "type": "serviceTask",        "label": "Registrar aprovacao",  "lane": "lane2", "pool": "pool1" },
    { "id": "n6", "type": "userTask",           "label": "Corrigir solicitacao",  "lane": "lane1", "pool": "pool1" },
    { "id": "n7", "type": "endEvent",           "label": "Fim",                  "lane": "lane2", "pool": "pool1" }
  ],
  "edges": [
    { "id": "e1", "type": "sequenceFlow", "source": "n1", "target": "n2" },
    { "id": "e2", "type": "sequenceFlow", "source": "n2", "target": "n3" },
    { "id": "e3", "type": "sequenceFlow", "source": "n3", "target": "n4" },
    { "id": "e4", "type": "sequenceFlow", "source": "n4", "target": "n5", "label": "Sim" },
    { "id": "e5", "type": "sequenceFlow", "source": "n4", "target": "n6", "label": "Nao", "isDefault": true },
    { "id": "e6", "type": "sequenceFlow", "source": "n5", "target": "n7" },
    { "id": "e7", "type": "sequenceFlow", "source": "n6", "target": "n2" }
  ]
}
```

**Output XML gerado:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  id="Definitions_1"
  targetNamespace="http://bpmn.io/schema/bpmn"
  exporter="Claude Code"
  exporterVersion="1.0">

  <!-- ═══ COLLABORATION ═══ -->
  <bpmn:collaboration id="Collaboration_1">
    <bpmn:participant id="pool1_participant" name="Empresa" processRef="pool1" />
  </bpmn:collaboration>

  <!-- ═══ PROCESS ═══ -->
  <bpmn:process id="pool1" name="Empresa" isExecutable="false">

    <!-- Lane Set -->
    <bpmn:laneSet id="LaneSet_pool1">
      <bpmn:lane id="lane1" name="Solicitante">
        <bpmn:flowNodeRef>n1</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>n2</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>n6</bpmn:flowNodeRef>
      </bpmn:lane>
      <bpmn:lane id="lane2" name="Aprovador">
        <bpmn:flowNodeRef>n3</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>n4</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>n5</bpmn:flowNodeRef>
        <bpmn:flowNodeRef>n7</bpmn:flowNodeRef>
      </bpmn:lane>
    </bpmn:laneSet>

    <!-- Start Event -->
    <bpmn:startEvent id="n1" name="Inicio">
      <bpmn:outgoing>e1</bpmn:outgoing>
    </bpmn:startEvent>

    <!-- User Task: Preencher -->
    <bpmn:userTask id="n2" name="Preencher solicitacao">
      <bpmn:documentation>Solicitante preenche formulario com dados da solicitacao</bpmn:documentation>
      <bpmn:incoming>e1</bpmn:incoming>
      <bpmn:incoming>e7</bpmn:incoming>
      <bpmn:outgoing>e2</bpmn:outgoing>
    </bpmn:userTask>

    <!-- User Task: Analisar -->
    <bpmn:userTask id="n3" name="Analisar solicitacao">
      <bpmn:incoming>e2</bpmn:incoming>
      <bpmn:outgoing>e3</bpmn:outgoing>
    </bpmn:userTask>

    <!-- Exclusive Gateway -->
    <bpmn:exclusiveGateway id="n4" name="Aprovado?" default="e5">
      <bpmn:incoming>e3</bpmn:incoming>
      <bpmn:outgoing>e4</bpmn:outgoing>
      <bpmn:outgoing>e5</bpmn:outgoing>
    </bpmn:exclusiveGateway>

    <!-- Service Task: Registrar -->
    <bpmn:serviceTask id="n5" name="Registrar aprovacao">
      <bpmn:incoming>e4</bpmn:incoming>
      <bpmn:outgoing>e6</bpmn:outgoing>
    </bpmn:serviceTask>

    <!-- User Task: Corrigir -->
    <bpmn:userTask id="n6" name="Corrigir solicitacao">
      <bpmn:incoming>e5</bpmn:incoming>
      <bpmn:outgoing>e7</bpmn:outgoing>
    </bpmn:userTask>

    <!-- End Event -->
    <bpmn:endEvent id="n7" name="Fim">
      <bpmn:incoming>e6</bpmn:incoming>
    </bpmn:endEvent>

    <!-- Sequence Flows -->
    <bpmn:sequenceFlow id="e1" sourceRef="n1" targetRef="n2" />
    <bpmn:sequenceFlow id="e2" sourceRef="n2" targetRef="n3" />
    <bpmn:sequenceFlow id="e3" sourceRef="n3" targetRef="n4" />
    <bpmn:sequenceFlow id="e4" name="Sim" sourceRef="n4" targetRef="n5" />
    <bpmn:sequenceFlow id="e5" name="Nao" sourceRef="n4" targetRef="n6" />
    <bpmn:sequenceFlow id="e6" sourceRef="n5" targetRef="n7" />
    <bpmn:sequenceFlow id="e7" sourceRef="n6" targetRef="n2" />

  </bpmn:process>

  <!-- ═══ DIAGRAM ═══ -->
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Collaboration_1">

      <!-- Pool -->
      <bpmndi:BPMNShape id="pool1_participant_di" bpmnElement="pool1_participant" isHorizontal="true">
        <dc:Bounds x="160" y="0" width="790" height="340" />
      </bpmndi:BPMNShape>

      <!-- Lanes -->
      <bpmndi:BPMNShape id="lane1_di" bpmnElement="lane1" isHorizontal="true">
        <dc:Bounds x="160" y="30" width="790" height="155" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="lane2_di" bpmnElement="lane2" isHorizontal="true">
        <dc:Bounds x="160" y="185" width="790" height="155" />
      </bpmndi:BPMNShape>

      <!-- n1: Start Event (rank 0, lane1) -->
      <bpmndi:BPMNShape id="n1_di" bpmnElement="n1">
        <dc:Bounds x="252" y="90" width="36" height="36" />
      </bpmndi:BPMNShape>

      <!-- n2: User Task (rank 1, lane1) -->
      <bpmndi:BPMNShape id="n2_di" bpmnElement="n2">
        <dc:Bounds x="370" y="68" width="100" height="80" />
      </bpmndi:BPMNShape>

      <!-- n3: User Task (rank 2, lane2) -->
      <bpmndi:BPMNShape id="n3_di" bpmnElement="n3">
        <dc:Bounds x="520" y="223" width="100" height="80" />
      </bpmndi:BPMNShape>

      <!-- n4: Exclusive Gateway (rank 3, lane2) -->
      <bpmndi:BPMNShape id="n4_di" bpmnElement="n4" isMarkerVisible="true">
        <dc:Bounds x="695" y="238" width="50" height="50" />
      </bpmndi:BPMNShape>

      <!-- n5: Service Task (rank 4, lane2) -->
      <bpmndi:BPMNShape id="n5_di" bpmnElement="n5">
        <dc:Bounds x="820" y="223" width="100" height="80" />
      </bpmndi:BPMNShape>

      <!-- n6: User Task (rank 4, lane1) -->
      <bpmndi:BPMNShape id="n6_di" bpmnElement="n6">
        <dc:Bounds x="820" y="68" width="100" height="80" />
      </bpmndi:BPMNShape>

      <!-- n7: End Event (rank 5, lane2) -->
      <bpmndi:BPMNShape id="n7_di" bpmnElement="n7">
        <dc:Bounds x="952" y="245" width="36" height="36" />
      </bpmndi:BPMNShape>

      <!-- Edges -->
      <bpmndi:BPMNEdge id="e1_di" bpmnElement="e1">
        <di:waypoint x="288" y="108" />
        <di:waypoint x="370" y="108" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="e2_di" bpmnElement="e2">
        <di:waypoint x="470" y="108" />
        <di:waypoint x="495" y="108" />
        <di:waypoint x="495" y="263" />
        <di:waypoint x="520" y="263" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="e3_di" bpmnElement="e3">
        <di:waypoint x="620" y="263" />
        <di:waypoint x="695" y="263" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="e4_di" bpmnElement="e4">
        <di:waypoint x="745" y="263" />
        <di:waypoint x="820" y="263" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="e5_di" bpmnElement="e5">
        <di:waypoint x="720" y="238" />
        <di:waypoint x="720" y="108" />
        <di:waypoint x="820" y="108" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="e6_di" bpmnElement="e6">
        <di:waypoint x="920" y="263" />
        <di:waypoint x="952" y="263" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="e7_di" bpmnElement="e7">
        <di:waypoint x="870" y="68" />
        <di:waypoint x="870" y="48" />
        <di:waypoint x="420" y="48" />
        <di:waypoint x="420" y="68" />
      </bpmndi:BPMNEdge>

    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>

</bpmn:definitions>
```

---

## 7. Checklist de Validacao Pre-Save

Antes de salvar o arquivo `.bpmn`, verificar:

- [ ] Todos os 5 namespaces declarados no `<bpmn:definitions>` (bpmn, bpmndi, dc, di, xsi)
- [ ] Todo `<bpmn:sequenceFlow>` tem `sourceRef` e `targetRef` apontando para IDs existentes
- [ ] Todo flow node lista seus flows em `<bpmn:incoming>` e `<bpmn:outgoing>` (exceto start=somente outgoing, end=somente incoming)
- [ ] Todo node ID aparece em exatamente um `<bpmn:flowNodeRef>` dentro de uma lane
- [ ] Todo elemento do modelo tem um `<bpmndi:BPMNShape>` ou `<bpmndi:BPMNEdge>` correspondente
- [ ] `bpmnElement` em cada shape/edge aponta para o ID correto
- [ ] IDs sao unicos em todo o documento
- [ ] Todo `<bpmn:participant>` tem `processRef` apontando para um `<bpmn:process>` existente
- [ ] XOR gateways com `default` referenciam um sequence flow ID valido
- [ ] Boundary events tem `attachedToRef` valido e NAO tem `<bpmn:incoming>`
- [ ] Coordenadas no BPMNDiagram nao tem sobreposicoes
