# AI Agents em BPMN — Padrao Camunda 8.8+ via Ad-hoc Sub-process

Como modelar agentes de IA dentro de processos BPMN 2.0 quando ha decisoes nao-deterministicas (LLM-driven). Cobre o padrao **ad-hoc sub-process** (`~`), as extensoes Camunda 8.8+ (AI Agent Task, AI Agent Sub-process) e os 4 padroes agenticos canonicos.

> **Status do padrao:** OMG nao atualizou o BPMN 2.0 oficialmente para AI agents (ainda em 2.0 de 2011, ISO/IEC 19510:2013). Camunda e Flowable consolidaram um padrao de fato em 2024-2025. A tendencia e convergencia para BPMN 3.0 nos proximos 2-3 anos.

## Sumario

1. [O insight central — Ad-hoc Sub-process](#1-o-insight-central--ad-hoc-sub-process)
2. [Quando usar AI agent no diagrama](#2-quando-usar-ai-agent-no-diagrama)
3. [Tipos de no para AI agents](#3-tipos-de-no-para-ai-agents)
4. [Sintaxe XML — Camunda AI Agent](#4-sintaxe-xml--camunda-ai-agent)
5. [Os 4 padroes agenticos canonicos](#5-os-4-padroes-agenticos-canonicos)
6. [Naming conventions para AI agents](#6-naming-conventions-para-ai-agents)
7. [Anti-patterns](#7-anti-patterns)
8. [Aplicacao M7](#8-aplicacao-m7)

---

## 1. O insight central — Ad-hoc Sub-process

BPMN 2.0 ja tinha o elemento certo para modelar comportamento agentico, so nao era usado para isso: **ad-hoc sub-process** (simbolo `~`).

Em um ad-hoc sub-process:

- O processo entra em um segmento **nao estruturado** (sem ordem rigida de execucao)
- O agente (LLM) ve o contexto, identifica uma **lista de acoes (tools) disponiveis** dentro do sub-processo, e decide quais executar e em qual ordem
- O loop de execucao e gerenciado pelo engine (Camunda), com auditabilidade total
- Resolve a tensao **deterministico (BPMN classico)** vs **nao-deterministico (LLM)** convivendo no mesmo modelo

### Visualmente

```
┌──────────────────────────────────────────────────┐
│ ~ Ad-hoc Sub-process: AI Agent decide          │
│                                                  │
│   ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│   │ Tool A     │  │ Tool B     │  │ Tool C   │ │
│   │ Search     │  │ Enrich     │  │ Validate │ │
│   └────────────┘  └────────────┘  └──────────┘ │
│   (sem flow rigido — agente escolhe)           │
└──────────────────────────────────────────────────┘
```

O simbolo `~` no canto inferior do retangulo indica ad-hoc.

---

## 2. Quando usar AI agent no diagrama

### Use ad-hoc sub-process + AI agent quando:

- ✅ A decisao depende de contexto que so um LLM consegue interpretar (ex: classificar tom de uma conversa, extrair dados de doc nao-estruturado)
- ✅ A ordem de execucao das sub-tarefas nao e fixa — depende do que o agente decidir
- ✅ O comportamento envolve um **loop agentico** (chamar tool, ver resultado, decidir proxima tool, repetir)
- ✅ Voce quer auditabilidade da decisao (Camunda registra cada tool call + resultado)

### Use Service Task convencional quando:

- ❌ E uma **chamada simples** a um LLM (ex: "summarize esse texto", "classifique este email") — **single-call, nao agentico**
- ❌ A ordem de execucao e fixa
- ❌ Nao ha decisao do LLM sobre o que fazer a seguir

> **Atencao:** "service task que chama OpenAI" NAO e AI agent. Sem ad-hoc + tools + feedback loop, e apenas uma chamada de API com nome bonito.

---

## 3. Tipos de no para AI agents

A skill suporta 3 padroes principais (Camunda 8.8+):

### 3.1 AI Agent Task (single-call)

Para uso simples e nao-agentico (1 chamada ao LLM, sem tools, sem loop):

| JSON `type` | XML | Descricao |
|---|---|---|
| `aiAgentTask` | `<bpmn:serviceTask>` + Camunda zeebe taskDefinition | Single-call a um LLM (summarize, classify, extract) |

```json
{
  "id": "n5",
  "type": "aiAgentTask",
  "label": "Resumir conversa",
  "lane": "lane1",
  "pool": "pool1",
  "aiAgent": {
    "model": "claude-3-5-sonnet",
    "promptTemplate": "Resuma em 3 bullets: {{conversa}}",
    "outputVariable": "resumo"
  }
}
```

### 3.2 AI Agent Sub-process (ad-hoc com tools)

Para uso agentico com tools e feedback loop (loop ate satisfacao):

| JSON `type` | XML | Descricao |
|---|---|---|
| `adHocSubProcess` (com `aiAgent`) | `<bpmn:adHocSubProcess>` + Camunda zeebe:adHoc | Agente decide quais tools chamar e em que ordem |

```json
{
  "id": "n5",
  "type": "adHocSubProcess",
  "label": "Enriquecer hotlist Salesforce",
  "lane": "lane1",
  "pool": "pool1",
  "aiAgent": {
    "model": "claude-3-5-sonnet",
    "systemPrompt": "Voce enriquece dados de hotlist consultando tools.",
    "tools": ["consultar_gold_layer", "enrich_crm", "gerar_html", "validar_regras"],
    "exitCondition": "agent.confidence > 0.85 OR iteration > 5"
  },
  "children": [
    { "id": "tool1", "type": "serviceTask", "label": "Consultar gold layer", "parent": "n5" },
    { "id": "tool2", "type": "serviceTask", "label": "Enrich CRM", "parent": "n5" },
    { "id": "tool3", "type": "serviceTask", "label": "Gerar HTML", "parent": "n5" },
    { "id": "tool4", "type": "serviceTask", "label": "Validar regras", "parent": "n5" }
  ]
}
```

### 3.3 Multi-agent Orchestration

Para cenarios com multiplos agentes especializados (ainda em adocao crescente):

```json
{
  "id": "n5",
  "type": "adHocSubProcess",
  "label": "Coordenar agentes",
  "aiAgent": {
    "type": "orchestrator",
    "subAgents": ["utility-agent", "document-agent", "knowledge-agent"]
  }
}
```

Cada `subAgent` pode ser modelado como um proprio `adHocSubProcess` filho.

---

## 4. Sintaxe XML — Camunda AI Agent

### 4.1 Namespaces necessarios

Adicionar ao `<bpmn:definitions>`:

```xml
xmlns:zeebe="http://camunda.org/schema/zeebe/1.0"
xmlns:camunda="http://camunda.org/schema/1.0/bpmn"
```

### 4.2 AI Agent Task (single-call)

```xml
<bpmn:serviceTask id="n5" name="Resumir conversa">
  <bpmn:extensionElements>
    <zeebe:taskDefinition type="io.camunda:aiagent:1" />
    <zeebe:ioMapping>
      <zeebe:input source="= conversa" target="prompt" />
      <zeebe:output source="= response" target="resumo" />
    </zeebe:ioMapping>
    <zeebe:taskHeaders>
      <zeebe:header key="model" value="claude-3-5-sonnet" />
      <zeebe:header key="systemPrompt" value="Resuma em 3 bullets" />
    </zeebe:taskHeaders>
  </bpmn:extensionElements>
  <bpmn:incoming>e1</bpmn:incoming>
  <bpmn:outgoing>e2</bpmn:outgoing>
</bpmn:serviceTask>
```

### 4.3 AI Agent Sub-process (ad-hoc + tools)

```xml
<bpmn:adHocSubProcess id="n5" name="Enriquecer hotlist" cancelRemainingInstances="false">
  <bpmn:extensionElements>
    <zeebe:adHoc activeElementsCollection="= ['tool1', 'tool2', 'tool3', 'tool4']" />
    <zeebe:taskHeaders>
      <zeebe:header key="aiAgent.model" value="claude-3-5-sonnet" />
      <zeebe:header key="aiAgent.systemPrompt" value="Voce enriquece dados consultando tools." />
      <zeebe:header key="aiAgent.exitCondition" value="agent.confidence > 0.85 OR iteration > 5" />
    </zeebe:taskHeaders>
  </bpmn:extensionElements>

  <!-- Tools como child service tasks -->
  <bpmn:serviceTask id="tool1" name="Consultar gold layer" />
  <bpmn:serviceTask id="tool2" name="Enrich CRM" />
  <bpmn:serviceTask id="tool3" name="Gerar HTML" />
  <bpmn:serviceTask id="tool4" name="Validar regras" />

  <bpmn:incoming>e4</bpmn:incoming>
  <bpmn:outgoing>e5</bpmn:outgoing>
</bpmn:adHocSubProcess>
```

**Observacoes:**

- `cancelRemainingInstances="false"` — agente pode chamar tools em paralelo
- Tools sao `serviceTask` filhos. **Sem sequence flows entre tools** — agente decide ordem
- O loop e implicito (engine continua iterando ate `exitCondition` ser satisfeita)

### 4.4 Visualizacao (BPMNDiagram)

```xml
<bpmndi:BPMNShape id="n5_di" bpmnElement="n5"
                  isExpanded="true"
                  bioc:fill="#eef77c"
                  bioc:stroke="#424135">
  <dc:Bounds x="500" y="100" width="350" height="200" />
</bpmndi:BPMNShape>

<!-- Tools renderizadas dentro -->
<bpmndi:BPMNShape id="tool1_di" bpmnElement="tool1" bioc:fill="#fffdef" bioc:stroke="#424135">
  <dc:Bounds x="520" y="140" width="80" height="60" />
</bpmndi:BPMNShape>
<!-- ... -->
```

A skill reconhece `adHocSubProcess` com `aiAgent` e aplica:
- **Fill `#eef77c` com 15% opacity** (lime sutil) para sinalizar "zona nao-deterministica"
- **Stroke 2px** (mais grosso) para diferenciar de subprocess regular
- **isExpanded="true"** — sempre expandido, mostrando tools dentro

---

## 5. Os 4 padroes agenticos canonicos

Camunda formalizou 4 padroes para integrar AI agents com BPMN classico. A skill suporta os 4:

### 5.1 Human triggers AI

Humano dispara, IA executa.

```
[Start Event] → [User Task: Solicitar enrichment] → [~AI Agent: Enriquecer dados] → [End Event]
```

### 5.2 AI suggests, human decides (ideal para regulado)

Agente recomenda, humano aprova.

```
[Start Event] → [~AI Agent: Sugerir acao] → [User Task: Aprovar sugestao]
                                              ↓
                                         [XOR: Aprovado?]
                                          ↙        ↘
                                    [Executar]  [Rejeitar]
```

### 5.3 Multi-agent collaboration

Multiplos agentes especializados, cada um com seu sub-process.

```
[Start] → [~AI Orchestrator] → [End]
              ↓
         (escolhe entre)
              ↓
   ┌────────┬────────┬────────┐
   ↓        ↓        ↓        ↓
[~Utility][~Doc][~Knowledge][~Other]
```

### 5.4 Fallback e escalation

Se confianca do agente < threshold, BPMN reroteia para humano ou agente backup.

```
[~AI Agent] → [XOR: confidence > 0.85?]
                  ↙ Sim         ↘ Nao
              [Continue]    [User Task: Revisao manual]
```

---

## 6. Naming conventions para AI agents

### Para AI Agent Task (single-call)

- Sempre usar verbo + complemento, igual atividades normais
- Exemplos:
  - ✅ "Resumir conversa"
  - ✅ "Classificar lead"
  - ✅ "Extrair dados do contrato"

### Para AI Agent Sub-process (ad-hoc com tools)

- Verbo + complemento + (opcional) qualificador "(IA)" no fim
- Exemplos:
  - ✅ "Enriquecer hotlist (IA)"
  - ✅ "Coordenar agentes especialistas"
  - ✅ "Gerar relatorio executivo (IA)"

### Para tools dentro do sub-process

- Verbo + complemento, igual service tasks normais
- Exemplos:
  - ✅ "Consultar gold layer"
  - ✅ "Enrich CRM via API"

---

## 7. Anti-patterns

### Generais

- ❌ **"AI Service Task" sem ad-hoc + tools + loop**: e so chamada de API. Nao chame de AI agent
- ❌ **AI agent dentro de pool sem owner humano**: governance fica perdida. Sempre ter um humano aprovador ou fallback
- ❌ **AI agent com >5-7 tools**: dificulta auditoria. Particionar em multiplos agentes
- ❌ **Sem `exitCondition` clara**: agente pode loopar infinitamente. Sempre definir threshold de confianca + max iteracoes
- ❌ **Tools com nomes vagos** ("processar", "executar"): documentar o que cada tool faz no `<bpmn:documentation>`

### Especificos M7

- ❌ **Usar AI agent para decisoes que ja tem regra deterministica**: se voce tem um SOP claro, nao gaste LLM. Use exclusiveGateway + serviceTask
- ❌ **Esconder o agente em service task generica**: o `~` do ad-hoc e o sinal visual de "aqui ha LLM". Sem ele, leitor nao sabe distinguir deterministico de nao-deterministico
- ❌ **Inventar simbologia propria** (icones de robo, etc.): o padrao Camunda + ad-hoc e suficiente. Nao adicionar ruido visual

---

## 8. Aplicacao M7

### Casos de uso reais que beneficiam de AI agents

| Caso de uso | Padrao recomendado | Tools |
|---|---|---|
| **Hotlist Salesforce com enrichment** | Ad-hoc sub-process + AI agent | consulta gold layer, enrich CRM, gera HTML, valida regras |
| **Voice agents para rituais gerenciais** | Ad-hoc sub-process + AI agent dentro de ritual classico | transcrever, classificar tom, sugerir resposta, escalar para humano |
| **Triagem inicial de tickets de service desk** | AI agent task (single-call) → exclusive gateway | classify (severity, category) |
| **Resumo executivo de WBR** | AI agent task (single-call) | summarize com prompt template |
| **Document agent para contratos** | Ad-hoc sub-process | extract clauses, validate compliance, flag risks |

### Argumento de governance para apresentacao executiva

> "Empresas usando fluxos BPMN com AI agents reduziram vazamentos de PII em interacoes com IA em 98,5% comparado a sistemas improvisados."

Esse argumento funciona bem para liderancas regulatorias (XP, M7, parceiros).

### O que documentar no `-descritivo.md`

Quando ha AI agents no diagrama, o `-descritivo.md` gerado pela skill deve conter uma secao adicional:

```markdown
## Agentes de IA no diagrama

### {{aiAgent.label}}
- **Padrao**: {{Human triggers / AI suggests / Multi-agent / Fallback}}
- **Tipo**: {{aiAgentTask single-call / adHocSubProcess agentic}}
- **Modelo**: {{model id}}
- **Tools** (se ad-hoc): {{lista}}
- **Exit condition**: {{condition}}
- **Governance**: {{quem aprova, quem audita}}
```

### Convencao M7 para a notacao

- **Simbolo `~`** sempre visivel no canto inferior do ad-hoc
- **Cor de fill `#eef77c` com 15% opacity** (lime sutil) — sinaliza zona nao-deterministica
- **Stroke 2px** mais grosso que sub-process regular
- **Label sempre com sufixo "(IA)"** quando o agente e o ator principal — ex: "Enriquecer hotlist (IA)"
- **Tools dentro com fill off-white** (`#fffdef`) — para diferenciar do container

---

## Notas finais

- O padrao ad-hoc + AI agent **ja e suportado pela skill** quando o input JSON tem nodes do tipo `adHocSubProcess` ou `aiAgentTask`
- A skill aplica auto-layout especial para ad-hoc: tools sao posicionadas em grid 2-3 colunas dentro do container
- Para mais detalhes do padrao Camunda: docs Camunda 8.8+ AI Agent Connectors
- Para evitar lock-in: a skill gera BPMN com extensoes Camunda (`zeebe:`) mas mantem toda a notacao em BPMN 2.0 standard. Ferramentas que nao suportam `zeebe:` ainda renderizam o ad-hoc corretamente, apenas ignoram metadata do agente
