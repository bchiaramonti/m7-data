# BPMN 2.0 — Notacao Essencial + Checklist de Validacao

Catalogo dos elementos BPMN 2.0 suportados pela skill, regras de uso e checklist completo de validacao em 7 categorias. Fonte: BPM CBOK 3.0, OMG BPMN 2.0 Specification.

## Sumario

1. [Eventos](#1-eventos)
2. [Atividades](#2-atividades)
3. [Gateways](#3-gateways)
4. [Conexoes](#4-conexoes)
5. [Pools e Lanes](#5-pools-e-lanes)
6. [Artefatos](#6-artefatos)
7. [Schema JSON de Input](#7-schema-json-de-input)
8. [Checklist de Validacao (7 categorias)](#8-checklist-de-validacao-7-categorias)
9. [Anti-patterns](#9-anti-patterns)

---

## 1. Eventos

Representam acontecimentos no processo. Circulos com contornos diferentes por momento (inicio / intermediario / fim).

### Eventos de Inicio

| JSON `type` | XML | Filhos | Quando usar |
|---|---|---|---|
| `startEvent` | `<bpmn:startEvent>` | `<bpmn:outgoing>` | Inicio simples |
| `startEvent-message` | `<bpmn:startEvent>` | `<bpmn:messageEventDefinition/>` + outgoing | Inicia ao receber mensagem |
| `startEvent-timer` | `<bpmn:startEvent>` | `<bpmn:timerEventDefinition/>` + outgoing | Inicia em data/hora ou intervalo |
| `startEvent-signal` | `<bpmn:startEvent>` | `<bpmn:signalEventDefinition/>` + outgoing | Inicia ao receber sinal broadcast |

### Eventos Intermediarios

| JSON `type` | XML | Filhos | Quando usar |
|---|---|---|---|
| `intermediateEvent` | `<bpmn:intermediateCatchEvent>` | incoming + outgoing | Marca ponto relevante no fluxo |
| `intermediateEvent-message` | `<bpmn:intermediateCatchEvent>` | `<bpmn:messageEventDefinition/>` + i/o | Aguarda mensagem |
| `intermediateEvent-timer` | `<bpmn:intermediateCatchEvent>` | `<bpmn:timerEventDefinition/>` + i/o | Aguarda prazo |
| `intermediateEvent-error` (com `attachedTo`) | `<bpmn:boundaryEvent>` | `<bpmn:errorEventDefinition/>` + outgoing | Captura erro em atividade |
| `intermediateEvent-signal` | `<bpmn:intermediateCatchEvent>` | `<bpmn:signalEventDefinition/>` + i/o | Aguarda sinal |

### Eventos de Fim

| JSON `type` | XML | Filhos | Quando usar |
|---|---|---|---|
| `endEvent` | `<bpmn:endEvent>` | `<bpmn:incoming>` | Fim simples |
| `endEvent-message` | `<bpmn:endEvent>` | `<bpmn:messageEventDefinition/>` + incoming | Envia mensagem ao encerrar |
| `endEvent-error` | `<bpmn:endEvent>` | `<bpmn:errorEventDefinition/>` + incoming | Encerra com erro (throw) |
| `endEvent-terminate` | `<bpmn:endEvent>` | `<bpmn:terminateEventDefinition/>` + incoming | Encerra todos os caminhos |

---

## 2. Atividades

Unidades de trabalho. Retangulos com cantos arredondados.

| JSON `type` | XML | Quando usar |
|---|---|---|
| `task` | `<bpmn:task>` | Tarefa generica (atomica) |
| `userTask` | `<bpmn:userTask>` | Executada por pessoa |
| `serviceTask` | `<bpmn:serviceTask>` | Executada por sistema/automatizada |
| `scriptTask` | `<bpmn:scriptTask>` | Regida por documento de apoio (POP) |
| `sendTask` | `<bpmn:sendTask>` | Envia mensagem |
| `receiveTask` | `<bpmn:receiveTask>` | Aguarda mensagem |
| `subProcess` | `<bpmn:subProcess>` | Conjunto de tarefas agrupadas |
| `adHocSubProcess` | `<bpmn:adHocSubProcess>` | Sub-process nao-estruturado (sem ordem fixa). Container canonico para AI agents (Camunda 8.8+). Ver [`ai-agents-bpmn.md`](ai-agents-bpmn.md) |
| `aiAgentTask` | `<bpmn:serviceTask>` + `zeebe:taskDefinition type="io.camunda:aiagent:1"` | AI agent single-call (summarize, classify) |

### Marcadores de atividade

| Marcador | Quando usar |
|---|---|
| Loop (seta circular) | Atividade que repete ate condicao |
| Multi-instance paralelo (3 barras verticais) | Multiplas instancias simultaneas |
| Multi-instance sequencial (3 barras horizontais) | Multiplas instancias em sequencia |
| Compensacao (seta dupla para tras) | Atividade de compensacao |

---

## 3. Gateways

Pontos de decisao ou divisao/juncao de fluxo. Losangos.

| JSON `type` | XML | Comportamento | Regra |
|---|---|---|---|
| `exclusiveGateway` (XOR) | `<bpmn:exclusiveGateway>` | Apenas **um** caminho segue | Avalia condicoes, primeiro verdadeiro ganha |
| `parallelGateway` (AND) | `<bpmn:parallelGateway>` | **Todos** os caminhos seguem | Nao avalia condicao, todos executam |
| `inclusiveGateway` (OR) | `<bpmn:inclusiveGateway>` | **Um ou mais** caminhos seguem | Avalia condicoes, todos verdadeiros executam |
| `eventBasedGateway` | `<bpmn:eventBasedGateway>` | Proximo evento determina caminho | Aguarda primeiro evento |

### Regras obrigatorias

1. **Pareamento**: todo gateway de divergencia deve ter par de convergencia do mesmo tipo
2. **Labels obrigatorios**: pergunta no gateway OU respostas nos fluxos de saida
3. **Caminho default**: todo XOR gateway deve ter caminho default (sem condicao)

### Formato de labels

| Gateway | Label no gateway | Labels nos fluxos |
|---|---|---|
| **XOR** | Pergunta? (ex: "Aprovado?") | Respostas (ex: "Sim" / "Nao") |
| **AND** | — (nao precisa) | — (todos seguem) |
| **OR** | Pergunta geral | Condicoes (ex: "Se valor > 100k") |
| **Event-based** | — | Tipo do evento |

---

## 4. Conexoes

| JSON `type` | XML | Escopo | Regra |
|---|---|---|---|
| `sequenceFlow` | `<bpmn:sequenceFlow>` | Dentro de `<bpmn:process>` | Solido. Dentro do mesmo pool |
| `messageFlow` | `<bpmn:messageFlow>` | Dentro de `<bpmn:collaboration>` | Tracejado. Apenas entre pools diferentes |
| `association` | `<bpmn:association>` | Dentro de `<bpmn:process>` | Pontilhado. Liga artefatos |

### Bidirectional refs (incoming/outgoing)

Cada flow node DEVE listar suas conexoes:

```xml
<bpmn:userTask id="n2" name="Analisar solicitacao">
  <bpmn:incoming>e1</bpmn:incoming>
  <bpmn:outgoing>e2</bpmn:outgoing>
</bpmn:userTask>
<bpmn:sequenceFlow id="e1" sourceRef="n1" targetRef="n2" />
<bpmn:sequenceFlow id="e2" sourceRef="n2" targetRef="n3" />
```

- Start events: apenas `<bpmn:outgoing>`
- End events: apenas `<bpmn:incoming>`
- Boundary events: apenas `<bpmn:outgoing>` (triggered pela activity, nao por flow)
- Demais: ambos

---

## 5. Pools e Lanes

| Tipo | Descricao | Regra |
|---|---|---|
| Pool | Processo de negocio completo OU participante externo | Sequence flow nunca cruza fronteira |
| Lane | Ator, area funcional ou papel dentro do pool | Atividade na lane do executor |
| Milestone | Divisao vertical para fases | Visual apenas |

### Regras

- Sequence flow (→) **nunca** cruza fronteiras de pool
- Message flow (⇢) **sempre** cruza fronteiras de pool
- Cada atividade pertence a exatamente uma lane
- Maximo 5-6 lanes por pool (agrupar atores similares se mais)
- Visao logica (N1-N2): pool unico sem lanes
- Visao fisica (N3-N5): pool com lanes representando areas funcionais

### Lane Set

Dentro de cada `<bpmn:process>`:

```xml
<bpmn:laneSet id="LaneSet_pool1">
  <bpmn:lane id="lane1" name="Comercial">
    <bpmn:flowNodeRef>n1</bpmn:flowNodeRef>
    <bpmn:flowNodeRef>n2</bpmn:flowNodeRef>
  </bpmn:lane>
</bpmn:laneSet>
```

Lanes NAO contem os elements — apenas referenciam IDs via `<bpmn:flowNodeRef>`. Os elements ficam soltos dentro do `<bpmn:process>`.

---

## 6. Artefatos

| JSON `type` | XML | Quando usar |
|---|---|---|
| `dataObject` | `<bpmn:dataObjectReference>` | Informacao lida ou produzida |
| `dataStore` | `<bpmn:dataStoreReference>` | Base de dados ou repositorio |
| `group` | `<bpmn:group>` | Agrupamento visual (sem semantica) |
| `textAnnotation` | `<bpmn:textAnnotation>` + `<bpmn:text>` | Comentarios |

---

## 7. Schema JSON de Input

```json
{
  "metadata": {
    "title": "Nome do Processo",
    "level": "N3",
    "version": "1.0",
    "date": "2026-05-08",
    "author": "Nome"
  },
  "pools": [
    {
      "id": "pool1",
      "name": "Empresa",
      "isExecutable": false,
      "lanes": [
        { "id": "lane1", "name": "Comercial" },
        { "id": "lane2", "name": "Compliance" }
      ]
    }
  ],
  "nodes": [
    { "id": "n1", "type": "startEvent", "label": "Lead recebido", "lane": "lane1", "pool": "pool1" },
    { "id": "n2", "type": "userTask", "label": "Qualificar lead", "lane": "lane1", "pool": "pool1",
      "description": "Analisa fit do lead com criterios M7" },
    { "id": "n3", "type": "exclusiveGateway", "label": "Aprovado?", "lane": "lane1", "pool": "pool1" }
  ],
  "edges": [
    { "id": "e1", "type": "sequenceFlow", "source": "n1", "target": "n2" },
    { "id": "e2", "type": "sequenceFlow", "source": "n2", "target": "n3" },
    { "id": "e3", "type": "sequenceFlow", "source": "n3", "target": "n4", "label": "Sim" },
    { "id": "e4", "type": "sequenceFlow", "source": "n3", "target": "n5", "label": "Nao", "isDefault": true }
  ]
}
```

Campos opcionais:
- `nodes[].description` → mapeia para `<bpmn:documentation>`
- `nodes[].attachedTo` → ID da activity para boundary events
- `edges[].label` → nome visivel da conexao
- `edges[].isDefault` → caminho default de XOR gateway
- `edges[].condition` → expressao formal (mapeia para `<bpmn:conditionExpression>`)

---

## 8. Checklist de Validacao (7 categorias)

A skill aplica este checklist em **Fase 2** (pre-construcao) e **Fase 6** (pos-layout). Status por regra: ✅ pass / ⚠ warning / ❌ fail.

### 8.1 Eventos

- [ ] Exatamente 1 start event por processo (exceto event subprocess)
- [ ] Pelo menos 1 end event por processo
- [ ] Todos os caminhos terminam em end event (sem dead-ends)
- [ ] Tipo de evento apropriado (timer para esperas, message para integracao, error para excecoes)
- [ ] Start event na lane que inicia o processo

### 8.2 Gateways

- [ ] Todo gateway de divergencia tem par de convergencia do mesmo tipo
- [ ] Labels presentes em todos os XOR gateways E/OU nos fluxos de saida
- [ ] XOR gateway tem caminho default (`isDefault: true` em um dos edges)
- [ ] AND gateway nao tem labels nos fluxos (todos seguem)
- [ ] Nenhum gateway com 1 entrada E 1 saida (desnecessario — remover)
- [ ] XOR/OR sem nesting com tipo diferente sem clara separacao

### 8.3 Naming

- [ ] Atividades: verbo + complemento ("Verificar documento", nao "Documento")
- [ ] Verbo no infinitivo OU 3a pessoa (nao passivo: "Analisado")
- [ ] Sem nomes genericos: "Processar", "Executar", "Fazer" sem complemento
- [ ] Labels com 5 palavras ou menos (caso contrario, virar subprocess)
- [ ] Gateway labels como pergunta ("Aprovado?", nao "Aprovacao")
- [ ] Edge labels como resposta ("Sim"/"Nao", nao "Aprovado"/"Rejeitado")

### 8.4 Flow Direction

- [ ] Fluxo predominante esquerda → direita
- [ ] Sem fluxo principal direita → esquerda (loops podem)
- [ ] Cruzamentos minimizados (validado pela Fase 5 da skill)
- [ ] Atividades alinhadas em suas lanes

### 8.5 Pools & Lanes

- [ ] Sequence flow nunca cruza fronteira de pool
- [ ] Message flow apenas entre pools diferentes
- [ ] Cada atividade na lane do seu executor
- [ ] Maximo 5-6 lanes por pool

### 8.6 Subprocesses

- [ ] Atividades 3+ relacionadas agrupadas como subprocess
- [ ] Subprocess expandido tem proprio start/end event
- [ ] Maximo 2 niveis de aninhamento

### 8.7 Completude / XML Estrutural

- [ ] 5 namespaces declarados em `<bpmn:definitions>` (bpmn, bpmndi, dc, di, xsi)
- [ ] Todo `<bpmn:sequenceFlow>` tem `sourceRef` e `targetRef` com IDs validos
- [ ] Todo flow node lista seus flows em `<bpmn:incoming>` e `<bpmn:outgoing>`
  - Excecao: start = somente outgoing, end = somente incoming, boundary = somente outgoing
- [ ] Todo node ID aparece em exatamente 1 `<bpmn:flowNodeRef>` (em sua lane)
- [ ] Todo elemento tem `<bpmndi:BPMNShape>` correspondente no diagrama
- [ ] Todo edge tem `<bpmndi:BPMNEdge>` correspondente
- [ ] `bpmnElement` em cada shape/edge aponta para o ID correto
- [ ] Todos os `id` sao unicos no documento
- [ ] Todo `<bpmn:participant>` tem `processRef` valido
- [ ] XOR gateways com `default` referenciam um sequence flow ID valido
- [ ] Boundary events tem `attachedToRef` valido e NAO tem `<bpmn:incoming>`

---

## 9. Anti-patterns

- ❌ **Spaghetti flow**: mais de 3 linhas se cruzando — reordenar lanes ou virar subprocess
- ❌ **Gateway soup**: 3+ gateways consecutivos — virar tabela de decisao
- ❌ **Invisible handoffs**: atividade muda de lane sem flow explicito cruzando — explicitar
- ❌ **Orphan annotations**: text annotations sem associacao — remover ou conectar
- ❌ **Missing happy path**: sem fluxo principal claro start→end — reestruturar
- ❌ **Verbo passivo em label**: "Documento aprovado" — virar "Aprovar documento"
- ❌ **Gateway sem label E sem labels nos fluxos**: leitor nao sabe a pergunta
- ❌ **End event ausente em algum caminho**: dead-end implicito = bug do mapeamento
- ❌ **Pool unico com 1 lane**: redundante — usar pool sem lanes
- ❌ **Subprocess de 1 atividade**: nao agrupa nada — virar task simples
- ❌ **Pool label > 30 chars / Lane label > 25 chars**: bpmn-js trunca em containers altos (height > 400px). Abreviar ou usar siglas. Detector `long-container-label` reporta como warning
- ❌ **2+ dataStoreReferences com mesmas bounds**: padrao cross-pool exige 1 referencia por pool, em sua propria lane. Bounds identicas = 2 cilindros sobrepostos. Detector `duplicate-shape-bounds` reporta como fail

---

## Output do checklist no descritivo

Cada validacao gera 1 linha com status no `-descritivo.md`:

```markdown
### Categoria 8.1 — Eventos
- ✅ Exatamente 1 start event por processo
- ✅ Todos os caminhos terminam em end event
- ⚠ Start event nao esta na lane do iniciador (sugerir mover para lane Comercial)

### Categoria 8.2 — Gateways
- ❌ XOR gateway "Aprovado?" sem caminho default — adicionar `isDefault: true` em um dos edges
```

Status:
- ✅ **pass**: regra atendida
- ⚠ **warning**: parcialmente atendida ou recomendacao opcional
- ❌ **fail**: regra violada — bloqueia construcao (Fase 2) ou registra issue residual (Fase 6)
