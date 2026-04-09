# Catalogo de Notacao BPMN 2.0

Referencia completa dos elementos BPMN 2.0 suportados pela skill `drawing-bpmn-flowcharts`.
Fonte: BPM CBOK 3.0, OMG BPMN 2.0 Specification, gestao-de-processos-book.md secao 6.

---

## 1. Eventos (Circulos)

Representam **acontecimentos** no processo. O contorno indica quando ocorrem.

### Eventos de Inicio

| ID | Tipo | JSON type | XML Element | Descricao |
|----|------|-----------|-------------|-----------|
| `start-none` | Inicio simples | `startEvent` | `<bpmn:startEvent>` | Dispara o processo sem gatilho especifico |
| `start-message` | Inicio por mensagem | `startEvent-message` | `<bpmn:startEvent>` + `<bpmn:messageEventDefinition/>` | Processo inicia ao receber mensagem |
| `start-timer` | Inicio por tempo | `startEvent-timer` | `<bpmn:startEvent>` + `<bpmn:timerEventDefinition/>` | Processo inicia em data/hora ou intervalo |
| `start-signal` | Inicio por sinal | `startEvent-signal` | `<bpmn:startEvent>` + `<bpmn:signalEventDefinition/>` | Processo inicia ao receber sinal broadcast |

### Eventos Intermediarios

| ID | Tipo | JSON type | XML Element | Descricao |
|----|------|-----------|-------------|-----------|
| `intermediate-none` | Intermediario simples | `intermediateEvent` | `<bpmn:intermediateCatchEvent>` | Marca ponto relevante no fluxo |
| `intermediate-message` | Mensagem (catch) | `intermediateEvent-message` | `<bpmn:intermediateCatchEvent>` + `<bpmn:messageEventDefinition/>` | Aguarda recebimento de mensagem |
| `intermediate-timer` | Timer | `intermediateEvent-timer` | `<bpmn:intermediateCatchEvent>` + `<bpmn:timerEventDefinition/>` | Aguarda prazo ou intervalo |
| `intermediate-error` | Erro (boundary) | `intermediateEvent-error` | `<bpmn:boundaryEvent>` + `<bpmn:errorEventDefinition/>` | Captura erro em atividade (attached) |
| `intermediate-signal` | Sinal | `intermediateEvent-signal` | `<bpmn:intermediateCatchEvent>` + `<bpmn:signalEventDefinition/>` | Aguarda sinal broadcast |

### Eventos de Fim

| ID | Tipo | JSON type | XML Element | Descricao |
|----|------|-----------|-------------|-----------|
| `end-none` | Fim simples | `endEvent` | `<bpmn:endEvent>` | Encerra o processo ou um caminho |
| `end-message` | Fim com mensagem | `endEvent-message` | `<bpmn:endEvent>` + `<bpmn:messageEventDefinition/>` | Envia mensagem ao encerrar |
| `end-error` | Fim com erro | `endEvent-error` | `<bpmn:endEvent>` + `<bpmn:errorEventDefinition/>` | Encerra com erro (throw) |
| `end-terminate` | Terminacao | `endEvent-terminate` | `<bpmn:endEvent>` + `<bpmn:terminateEventDefinition/>` | Encerra todos os caminhos do processo |

---

## 2. Atividades (Retangulos)

Representam **unidades de trabalho** — tarefas a serem realizadas.

| ID | Tipo | JSON type | XML Element | Descricao |
|----|------|-----------|-------------|-----------|
| `task` | Tarefa generica | `task` | `<bpmn:task>` | Unidade atomica de trabalho |
| `task-user` | Tarefa de usuario | `userTask` | `<bpmn:userTask>` | Executada por uma pessoa |
| `task-service` | Tarefa de servico | `serviceTask` | `<bpmn:serviceTask>` | Executada por sistema/automatizada |
| `task-script` | Tarefa de script | `scriptTask` | `<bpmn:scriptTask>` | Regida por documento de apoio (POP) |
| `task-send` | Tarefa de envio | `sendTask` | `<bpmn:sendTask>` | Envia mensagem |
| `task-receive` | Tarefa de recebimento | `receiveTask` | `<bpmn:receiveTask>` | Aguarda recebimento de mensagem |
| `subprocess` | Subprocesso | `subProcess` | `<bpmn:subProcess>` | Conjunto de tarefas agrupadas (colapsavel) |
| `subprocess-expanded` | Subprocesso expandido | `subProcess-expanded` | `<bpmn:subProcess>` (com filhos) | Mostra tarefas internas |

### Marcadores de atividade

| Marcador | Icone | Significado |
|----------|-------|-------------|
| Loop | Seta circular | Atividade que repete ate condicao |
| Multi-instance (paralelo) | 3 barras verticais | Multiplas instancias simultaneas |
| Multi-instance (sequencial) | 3 barras horizontais | Multiplas instancias em sequencia |
| Compensacao | Seta dupla para tras | Atividade de compensacao |

---

## 3. Gateways (Losangos)

Representam **pontos de decisao** ou divisao/juncao de fluxo.

| ID | Tipo | JSON type | XML Element | Descricao | Regra |
|----|------|-----------|-------------|-----------|-------|
| `gateway-xor` | Exclusivo (XOR) | `exclusiveGateway` | `<bpmn:exclusiveGateway>` | Apenas **um** caminho segue | Avalia condicoes, primeiro verdadeiro ganha |
| `gateway-and` | Paralelo (AND) | `parallelGateway` | `<bpmn:parallelGateway>` | **Todos** os caminhos seguem | Nao avalia condicao, todos executam |
| `gateway-or` | Inclusivo (OR) | `inclusiveGateway` | `<bpmn:inclusiveGateway>` | **Um ou mais** caminhos seguem | Avalia condicoes, todos verdadeiros executam |
| `gateway-event` | Baseado em evento | `eventBasedGateway` | `<bpmn:eventBasedGateway>` | Proximo evento determina caminho | Aguarda primeiro evento |

### Regras de uso de gateways

1. Todo gateway de **divergencia** deve ter um gateway de **convergencia** correspondente do mesmo tipo
2. Labels obrigatorios: no gateway (pergunta) ou nos fluxos de saida (respostas)
3. Gateway XOR: labels nos fluxos (ex: "Sim" / "Nao"). Sempre incluir caminho default
4. Gateway AND: nao precisa de labels nos fluxos (todos seguem)
5. Gateway OR: labels nos fluxos indicando condicoes

---

## 4. Conexoes

| ID | Tipo | JSON type | XML Element | Descricao | Regra |
|----|------|-----------|-------------|-----------|-------|
| `sequence-flow` | Fluxo de sequencia | `sequenceFlow` | `<bpmn:sequenceFlow>` (dentro de process) | Ordem das atividades dentro de um pool | Dentro do mesmo pool |
| `message-flow` | Fluxo de mensagem | `messageFlow` | `<bpmn:messageFlow>` (dentro de collaboration) | Comunicacao entre pools | Apenas entre pools diferentes |
| `association` | Associacao | `association` | `<bpmn:association>` (dentro de process) | Liga artefatos a elementos | Sem direcao por padrao |

---

## 5. Divisoes (Pools e Lanes)

| ID | Tipo | Descricao | Regra |
|----|------|-----------|-------|
| `pool` | Pool (piscina) | Representa um processo de negocio completo ou um participante | Todo fluxograma tem pelo menos 1 pool |
| `lane` | Lane (raia) | Representa um ator ou area funcional dentro do pool | Atividades devem estar na lane do executor |
| `milestone` | Milestone | Extensao vertical representando subprocessos ou fases | Divisao visual por etapas |

### Regras de pools e lanes

- Fluxo de sequencia (→) **nunca** cruza fronteiras de pool
- Fluxo de mensagem (⇢) **sempre** cruza fronteiras de pool
- Cada atividade pertence a exatamente uma lane
- Lanes podem ser aninhadas (sub-lanes)

---

## 6. Artefatos

| ID | Tipo | JSON type | XML Element | Descricao |
|----|------|-----------|-------------|-----------|
| `data-object` | Objeto de dados | `dataObject` | `<bpmn:dataObjectReference>` | Informacao lida ou produzida |
| `data-store` | Armazem de dados | `dataStore` | `<bpmn:dataStoreReference>` | Base de dados ou repositorio |
| `group` | Grupo | `group` | `<bpmn:group>` | Agrupamento visual (sem semantica de fluxo) |
| `annotation` | Anotacao | `textAnnotation` | `<bpmn:textAnnotation>` + `<bpmn:text>` | Comentarios ou explicacoes |

---

## 7. Niveis de Modelagem

### Visao Logica (N1-N2)

Usada para mapear a **essencia do processo** sem detalhamento operacional:

- **SEM** pools/lanes (ou pool unico sem lanes)
- Apenas atividades principais e subprocessos
- Gateways exclusivos (XOR) somente
- Eventos de inicio e fim simples
- Foco no fluxo de valor ponta a ponta

### Visao Fisica (N3-N5)

Usada para mapear o **detalhamento operacional** com atores e regras:

- **COM** pools e lanes (swimlanes por area/ator)
- Todos os tipos de atividade (user, service, script)
- Todos os tipos de gateway
- Eventos intermediarios (timer, message, error)
- Boundary events em atividades
- Data objects e annotations
- Condicoes temporais e links entre processos

---

## 8. Schema JSON de Input

O JSON de entrada para geracao do arquivo `.bpmn` segue este schema:

```json
{
  "metadata": {
    "title": "Nome do Processo",
    "level": "N2",
    "version": "1.0",
    "date": "2026-02-27",
    "author": "Nome do Autor"
  },
  "pools": [
    {
      "id": "pool-1",
      "name": "Nome do Processo",
      "isExecutable": false,
      "lanes": [
        {
          "id": "lane-1",
          "name": "Area Funcional"
        }
      ]
    }
  ],
  "nodes": [
    {
      "id": "node-1",
      "type": "startEvent",
      "label": "",
      "lane": "lane-1",
      "pool": "pool-1"
    },
    {
      "id": "node-2",
      "type": "userTask",
      "label": "Verificar documento",
      "lane": "lane-1",
      "pool": "pool-1",
      "description": "Detalhes da atividade (mapeado para bpmn:documentation)"
    },
    {
      "id": "node-3",
      "type": "exclusiveGateway",
      "label": "Documento valido?",
      "lane": "lane-1",
      "pool": "pool-1"
    },
    {
      "id": "node-4",
      "type": "intermediateEvent-error",
      "label": "Erro de validacao",
      "lane": "lane-1",
      "pool": "pool-1",
      "attachedTo": "node-2"
    }
  ],
  "edges": [
    {
      "id": "edge-1",
      "type": "sequenceFlow",
      "source": "node-1",
      "target": "node-2"
    },
    {
      "id": "edge-2",
      "type": "sequenceFlow",
      "source": "node-2",
      "target": "node-3"
    },
    {
      "id": "edge-3",
      "type": "sequenceFlow",
      "source": "node-3",
      "target": "node-4",
      "label": "Sim"
    },
    {
      "id": "edge-4",
      "type": "sequenceFlow",
      "source": "node-3",
      "target": "node-5",
      "label": "Nao",
      "isDefault": true
    },
    {
      "id": "edge-5",
      "type": "sequenceFlow",
      "source": "node-3",
      "target": "node-6",
      "label": "Condicional",
      "condition": "valor > 1000"
    }
  ]
}
```

### Campos por objeto

| Objeto | Campo | Tipo | Obrigatorio | Descricao |
|--------|-------|------|-------------|-----------|
| `metadata` | `title` | string | sim | Nome do processo |
| | `level` | string | sim | N1\|N2\|N3\|N4\|N5 |
| | `version` | string | sim | Versao (ex: "1.0") |
| | `date` | string | sim | Data YYYY-MM-DD |
| | `author` | string | sim | Nome do autor |
| `pools[]` | `id` | string | sim | Identificador unico |
| | `name` | string | sim | Nome do pool/participante |
| | `isExecutable` | boolean | nao | Se o processo e executavel (default: false) |
| | `lanes[]` | array | sim | Lanes dentro do pool |
| `nodes[]` | `id` | string | sim | Identificador unico |
| | `type` | string | sim | Tipo BPMN (ver tabelas acima) |
| | `label` | string | sim | Rotulo visivel |
| | `lane` | string | sim | ID da lane |
| | `pool` | string | sim | ID do pool |
| | `description` | string | nao | Texto mapeado para `<bpmn:documentation>` |
| | `attachedTo` | string | nao | ID da activity para boundary events |
| `edges[]` | `id` | string | sim | Identificador unico |
| | `type` | string | sim | sequenceFlow \| messageFlow \| association |
| | `source` | string | sim | ID do node de origem |
| | `target` | string | sim | ID do node de destino |
| | `label` | string | nao | Rotulo da conexao (condicao, etc.) |
| | `isDefault` | boolean | nao | Marca como caminho default de XOR gateway |
| | `condition` | string | nao | Expressao condicional formal |
