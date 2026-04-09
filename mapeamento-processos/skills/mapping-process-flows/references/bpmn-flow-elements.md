# Guia de Elementos BPMN por Nivel

Referencia rapida para selecionar o elemento BPMN correto com base no que o usuario descreve, e nas restricoes de cada nivel de modelagem.

> Para a especificacao completa de cada elemento (XML mapping, atributos), consulte `drawing-bpmn-flowcharts/references/BPMN-NOTATION.md`.

---

## Regras Criticas por Nivel

| Regra | N1–N2 | N3–N5 |
|-------|--------|--------|
| Pools | Opcional (1 pool implicito) | Sim, se ha participantes externos |
| Lanes | **NAO** | **Obrigatorio** (minimo 1) |
| Eventos de inicio complexos | Apenas none | Todos os tipos |
| Boundary events | **NAO** | Sim |
| Sub-processos | Nao recomendado | Sim |
| Artefatos (Data Object, Store) | Nao recomendado | Opcional |
| Anotacoes | Opcional | Opcional |

---

## Tabela de Conversao: "O usuario diz..." → Elemento BPMN

### Eventos de Inicio

| O usuario diz... | Tipo BPMN | `type` no JSON | Disponivel |
|-----------------|-----------|---------------|------------|
| "Quando o cliente solicita / pede / envia" | Start Event (none) | `startEvent` | N1–N5 |
| "Quando recebemos uma mensagem / e-mail / notificacao / arquivo" | Message Start Event | `messageStartEvent` | N3–N5 |
| "Todo dia X / a cada hora / no fechamento do mes" | Timer Start Event | `timerStartEvent` | N3–N5 |
| "Quando outro processo dispara / sinaliza" | Signal Start Event | `signalStartEvent` | N3–N5 |
| "Qualquer um de X ou Y pode iniciar" | Multiplos Start Events | Dois `startEvent` | N3–N5 |

---

### Atividades

| O usuario diz... | Tipo BPMN | `type` no JSON | Observacao |
|-----------------|-----------|---------------|------------|
| "A pessoa preenche / seleciona / aprova / decide / valida" | User Task | `userTask` | Tarefa humana com interface |
| "O sistema automaticamente processa / consulta / calcula / integra" | Service Task | `serviceTask` | API, microservico, integracao |
| "Roda um script / regra automatica / algoritmo" | Script Task | `scriptTask` | Codigo executado pelo motor |
| "Envia e-mail / mensagem / notificacao para fora do pool" | Send Task | `sendTask` | Envio de mensagem externa |
| "Aguarda / espera resposta / confirmacao de fora" | Receive Task | `receiveTask` | Recebimento de mensagem |
| "E uma etapa com varios sub-passos complexos" | Sub-Process | `subProcess` | Expansivel no diagrama |
| "Chama outro processo definido separadamente" | Call Activity | `callActivity` | Reutilizacao de processo |
| "Nao tenho certeza de como funciona / e manual mas nao sei detalhes" | Task | `task` | Generico, sem tipo especifico |

---

### Gateways

| O usuario diz... | Tipo BPMN | `type` no JSON | Quando usar |
|-----------------|-----------|---------------|------------|
| "Se X, vai para A; se nao, vai para B" | XOR Gateway | `exclusiveGateway` | Apenas um caminho por vez |
| "Ao mesmo tempo / em paralelo / simultaneamente" | AND Gateway | `parallelGateway` | Todos os caminhos em paralelo |
| "Dependendo do tipo / pode ir para um ou mais" | OR Gateway | `inclusiveGateway` | Um ou mais caminhos |
| "Esperamos pelo primeiro evento que acontecer (resposta OU timeout)" | Event-based Gateway | `eventBasedGateway` | Decisao baseada em evento futuro |

**Regras de gateway divergente (abertura de caminhos):**
- XOR: label obrigatoria em todos os ramos de saida + 1 marcado como `isDefault`
- AND: sem label nos ramos (todos sao executados)
- OR: label nos ramos que tem condicao; pode ter default

**Regras de gateway convergente (fechamento de caminhos):**
- XOR convergente: sem label (aguarda qualquer um dos ramos)
- AND convergente: sem label (aguarda TODOS os ramos)
- Usar o mesmo tipo do gateway divergente correspondente

---

### Eventos Intermediarios (dentro do fluxo)

| Situacao | Tipo BPMN | `type` no JSON | Disponivel |
|----------|-----------|---------------|------------|
| "Aguardamos confirmacao de fora antes de continuar" | Intermediate Catch — Message | `intermediateCatchEvent` + `messageEventDefinition` | N3–N5 |
| "Esperamos X dias/horas antes de continuar" | Intermediate Catch — Timer | `intermediateCatchEvent` + `timerEventDefinition` | N3–N5 |
| "Enviamos uma notificacao no meio do processo" | Intermediate Throw — Message | `intermediateThrowEvent` + `messageEventDefinition` | N3–N5 |
| "O processo sinaliza outro processo neste ponto" | Intermediate Throw — Signal | `intermediateThrowEvent` + `signalEventDefinition` | N3–N5 |

---

### Boundary Events (presos em atividades)

*Disponivel apenas em N3–N5. Ficam "colados" em uma atividade especifica.*

| Situacao | Tipo BPMN | `type` no JSON | Uso |
|----------|-----------|---------------|-----|
| "Se a atividade demorar mais de X, fazer Y" | Boundary Timer | `boundaryEvent` + timer | Timeout com caminho alternativo |
| "Se a atividade retornar erro, ir para recuperacao" | Boundary Error | `boundaryEvent` + error | Tratamento de erro esperado |
| "Se receber uma mensagem enquanto executa, mudar de rota" | Boundary Message | `boundaryEvent` + message | Interrupcao por mensagem |
| "Se um sinal de cancelamento chegar, encerrar a atividade" | Boundary Signal | `boundaryEvent` + signal | Cancelamento externo |

No JSON, usar `"attachedTo": "<id da atividade>"` no no do boundary event.

---

### Eventos de Fim

| O usuario diz... | Tipo BPMN | `type` no JSON | Quando usar |
|-----------------|-----------|---------------|------------|
| "O processo termina / conclui normalmente" | End Event (none) | `endEvent` | Conclusao padrao |
| "Ao terminar, envia uma mensagem / notifica outro processo" | Message End | `messageEndEvent` | Fim com envio obrigatorio |
| "Termina com um erro documentado / lancar excecao" | Error End | `errorEndEvent` | Fim por erro de negocio |
| "Cancela tudo que esta em andamento forcosamente" | Terminate End | `terminateEndEvent` | Encerramento forcado |

---

### Conexoes

| Situacao | Tipo | `type` no JSON |
|----------|------|---------------|
| Fluxo entre atividades do mesmo pool | Sequence Flow | `sequenceFlow` |
| Mensagem entre pools diferentes | Message Flow | `messageFlow` |
| Ligacao a anotacao ou artefato | Association | `association` |

---

### Artefatos (N3–N5, opcional)

| Elemento | `type` no JSON | Quando usar |
|----------|---------------|------------|
| Documento, dado ou entidade de negocio | `dataObject` | Produzido ou consumido por atividade |
| Banco de dados, sistema de registro | `dataStore` | Consultado por multiplas atividades |
| Nota explicativa sobre elemento | `textAnnotation` | Regra de negocio ou esclarecimento |
| Agrupamento visual sem significado semantico | `group` | Organizar visualmente etapas |

---

## IDs — Convencao de Nomenclatura

Para gerar IDs unicos e legíveis no JSON:

| Tipo de no | Padrao de ID | Exemplos |
|------------|-------------|---------|
| Start Event | `start_<N>` | `start_1`, `start_2` |
| End Event | `end_<N>` | `end_1`, `end_erro` |
| Task/Activity | `task_<N>` ou `task_<verbo>` | `task_1`, `task_validar` |
| User Task | `ut_<N>` | `ut_1`, `ut_aprovacao` |
| Service Task | `st_<N>` | `st_consulta_crm` |
| Gateway (XOR) | `gw_<N>` | `gw_1`, `gw_aprovacao` |
| Gateway (AND) | `and_<N>` | `and_paralelo` |
| Intermediate Event | `ev_<N>` | `ev_espera_assinatura` |
| Boundary Event | `be_<N>` | `be_timeout_analise` |
| Pool | `pool_<nome>` | `pool_principal`, `pool_banco` |
| Lane | `lane_<ator>` | `lane_assessor`, `lane_compliance` |
| Sequence Flow | `seq_<N>` ou `seq_<origem>_<destino>` | `seq_1`, `seq_gw_aprovado` |
| Message Flow | `msg_<N>` | `msg_notificacao_cliente` |

---

## Checklist de Validacao Pre-Geracao

Antes de passar o JSON para `drawing-bpmn-flowcharts`, verificar:

**Estrutural:**
- [ ] Exatamente 1 `startEvent` por processo (ou por pool executavel)
- [ ] Pelo menos 1 `endEvent`
- [ ] Todos os nos tem pelo menos uma conexao (nao ha no isolado)
- [ ] Todos os caminhos chegam a um `endEvent`

**Gateways:**
- [ ] Todo gateway divergente tem um gateway convergente correspondente (exceto quando ramos terminam em `endEvent`)
- [ ] Gateways XOR: todos os ramos rotulados, exatamente 1 `isDefault: true`
- [ ] Gateways AND: nenhum ramo rotulado
- [ ] Nenhum gateway com apenas 1 saida (seria uma atividade, nao um gateway)

**Nomenclatura:**
- [ ] Atividades: verbo + complemento ("Verificar documentacao", nao "Verificacao")
- [ ] Gateways XOR: pergunta direta ("Aprovado?", "Valor dentro do limite?")
- [ ] Eventos de inicio: descricao do trigger ("Receber solicitacao do cliente")
- [ ] Sem nomes genericos: "Processar", "Executar", "Fazer"

**Niveis:**
- [ ] N1–N2: nenhuma lane, nenhum boundary event, nenhum subprocesso
- [ ] N3–N5: toda atividade esta em uma lane (`"lane": "<id>"`)

**IDs:**
- [ ] Sem IDs duplicados em `nodes` ou `edges`
- [ ] Todo `source` e `target` em `edges` referencia um ID existente em `nodes`
- [ ] Boundary events tem `"attachedTo": "<id da atividade>"`
