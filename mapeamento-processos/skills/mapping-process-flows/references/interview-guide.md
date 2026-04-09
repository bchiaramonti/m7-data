# Guia de Entrevista — Mapeamento de Fluxo de Processo

Roteiro detalhado para conduzir a entrevista de mapeamento do fluxo. Segue as 8 fases definidas no SKILL.md, com perguntas de abertura, perguntas-sonda e adaptacoes por nivel.

---

## Principios de Facilitacao

1. **Escuta ativa**: Reformule o que o usuario disse antes de avancar ("Entao, se eu entendi bem, o processo começa quando...")
2. **Concretude**: Peca exemplos reais ("Me da um exemplo de quando isso acontece")
3. **Questionar o obvio**: O que parece simples muitas vezes esconde complexidade ("Quem valida isso? Sempre e a mesma pessoa?")
4. **Resistir a solucoes**: O mapeamento e sobre o estado atual (AS-IS), nao o desejado (TO-BE). Se o usuario comecar a descrever melhorias, reconheca e anote, mas continue o mapeamento AS-IS
5. **Confirmar antes de avancar**: Ao final de cada fase, apresente o que coletou e peca confirmacao

---

## Fase 1 — Identificar o Processo

### Abertura
> "Para comecar o mapeamento, preciso entender o contexto geral do processo. Vamos comecar pelo basico."

### Pergunta principal
> "Qual e o nome deste processo?"

### Perguntas-sonda
- "Existe um codigo ou identificador oficial para este processo na cadeia de valor da empresa?" (ex: G2.3, AP.1)
- "Quem e o responsavel por este processo — a area dona, nao quem executa?"
- "Em uma frase, qual e o proposito deste processo? O que ele existe para fazer?"

### Determinando o nivel
> "Em qual nivel de detalhe voce quer modelar este processo?"

Apresentar como `AskUserQuestion` com opcoes:
- **N1** — Processo estrategico na cadeia de valor (visao macro da empresa)
- **N2** — Macroprocesso (visao gerencial, base para DEIP)
- **N3** — Processo operacional com atores e lanes (padrao mais comum)
- **N4** — Subprocesso detalhado (detalhamento de uma etapa de N3)
- **N5** — Procedimento passo a passo (instrucao de trabalho)

### Dica de nivel
Se o usuario nao souber, pergunte: "Voce quer mostrar quem executa cada atividade (cargos ou areas especificos)?" Se sim → N3+. Se nao → N1 ou N2.

### Confirmacao de Fase 1
> "Entao temos: processo '[nome]', nivel [N?], responsavel pela area [responsavel], com o objetivo de [objetivo]. Esta correto?"

---

## Fase 2 — Mapear Participantes

*Aplicavel apenas para N3–N5.*

### 2a — Pools

> "Ha outros sistemas, empresas ou unidades de negocio completamente separadas que participam deste processo?"

**Quando criar um pool separado:**
- Sistema externo que envia/recebe mensagens (ex: Banco Central, sistema de terceiro)
- Empresa parceira com processo proprio (ex: seguradora, gestora de fundos)
- Unidade de negocio com autonomia completa

**Quando NAO criar pool separado:**
- Areas internas da mesma empresa → sao lanes, nao pools
- Sistemas internos que as atividades usam → sao artefatos (Data Store)

Se o usuario nao tiver pools externos: usar apenas o pool principal com o nome do processo.

### 2b — Lanes

> "Dentro do processo, quais sao os atores que executam as atividades? Liste os cargos, areas ou sistemas que participam."

**Perguntas-sonda:**
- "Quem inicia o processo? Qual e a area responsavel por cada etapa?"
- "Ha alguma area de aprovacao ou controle que participa?"
- "Ha algum sistema automatico que executa alguma etapa sem intervencao humana?"

**Padrao por tipo de processo:**

| Tipo | Lanes tipicas |
|------|--------------|
| Aprovacao | Solicitante / Analisador / Aprovador |
| Onboarding | Cliente (externo) / Area Comercial / Compliance / Operacoes |
| Processamento batch | Sistema de Entrada / Processador / Sistema de Saida |
| Atendimento | Cliente (externo) / Atendente / Backoffice |
| Financeiro | Solicitante / Financeiro / Aprovador / Contabilidade |

**Perguntas de refinamento:**
- "Esta lane e sempre a mesma pessoa ou pode ser qualquer membro da area?" (define se e cargo ou area)
- "O sistema [X] executa automaticamente ou alguem precisa acionar?" (distingue lane de sistema vs. Data Store)

### Confirmacao de Fase 2
> "Entao temos [N] pool(s): [lista]. Dentro do pool principal, as lanes sao: [lista]. Confirma?"

---

## Fase 3 — Evento de Inicio

### Pergunta principal
> "O que da inicio a este processo? Como ele começa?"

### Perguntas-sonda por tipo de trigger

**Trigger manual (startEvent none):**
- "Quem inicia o processo? O que essa pessoa precisa fazer para dar o start?"
- Ex.: "O cliente acessa o portal e preenche o formulario" → startEvent com label "Receber solicitacao do cliente"

**Trigger por mensagem (messageStartEvent):**
- "O processo começa quando recebe algo de fora — um e-mail, uma API call, uma notificacao?"
- Ex.: "O Banco Central envia o arquivo D+0 todo dia util" → messageStartEvent

**Trigger por tempo (timerStartEvent):**
- "O processo roda em horario fixo ou em intervalos regulares?"
- Ex.: "Todo dia 18h, o sistema roda o processamento" → timerStartEvent

**Trigger por sinal (signalStartEvent):**
- "O processo e disparado por um evento de outro processo interno?"
- Ex.: "Quando o processo de onboarding encerra, este processo e acionado automaticamente" → signalStartEvent

### Armadilhas comuns
- **Multiplos triggers**: "O processo pode comecar de duas formas" → dois startEvents separados com gateway logo apos, ou dois subprocessos
- **Trigger vago**: "Quando precisamos" — refinar com "o que especificamente desencadeia a necessidade?"
- **Pre-condicao vs. trigger**: "Precisa ter saldo disponivel" — isso e pre-condicao, nao trigger

### Confirmacao de Fase 3
> "O processo inicia com [descricao do trigger], do tipo [tipo]. Esta correto?"

---

## Fase 4 — Caminho Feliz

### Abertura
> "Agora vamos mapear o fluxo ideal — o cenario onde tudo da certo, sem erros, sem excecoes. Quais sao os passos em sequencia?"

### Tecnica de elicitacao: "E depois?"

Para cada atividade que o usuario menciona:
1. Anote o nome e tipo
2. Pergunte: "E depois? Qual e o proximo passo?"
3. Repita ate o usuario chegar ao fim do processo

### Perguntas-sonda para refinamento

**Para cada atividade:**
- "Quem faz isso? E automatico ou manual?" (define tipo e lane)
- "O que essa atividade produz como resultado?" (ajuda a identificar artefatos e conexoes)
- "Quanto tempo normalmente leva?" (informacao para anotacao, nao para o BPMN em si)

**Para nomear corretamente:**
- Se o usuario disser "Processo de analise" → "Como voce chamaria a acao que acontece aqui? Use verbo + complemento: 'Analisar [o que]?'"
- Se o usuario disser "Verificacao de documentos" → reformular para "Verificar documentacao do cliente"

### Tipos de atividade — como identificar

| O usuario diz... | Tipo BPMN | Descricao |
|-----------------|-----------|-----------|
| "A pessoa clica, escolhe, preenche..." | `userTask` | Tarefa humana com interface |
| "O sistema automaticamente..." | `serviceTask` | Tarefa executada por sistema via API |
| "Roda um script, regra automatica..." | `scriptTask` | Tarefa executada por codigo |
| "Envia uma mensagem/e-mail para fora..." | `sendTask` | Tarefa de envio de mensagem |
| "Espera uma resposta/confirmacao..." | `receiveTask` | Tarefa de recebimento de mensagem |
| "E uma etapa complexa com sub-passos..." | `subProcess` | Subprocesso expansivel |
| "Nao sei exatamente como funciona..." | `task` | Tarefa generica |

### Padrao por tipo de processo

**Processo de aprovacao tipico:**
1. Receber solicitacao → 2. Analisar documentacao → 3. Avaliar elegibilidade → 4. [Gateway de aprovacao] → 5a. Aprovar solicitacao → 6. Notificar aprovacao / 5b. Rejeitar solicitacao → 6b. Notificar rejeicao

**Processo de onboarding tipico:**
1. Receber cadastro → 2. Verificar documentos → 3. Validar dados no sistema → 4. Criar conta → 5. Configurar perfil → 6. Notificar cliente

**Processo de processamento batch:**
1. Receber arquivo → 2. Validar formato → 3. Processar registros → 4. Tratar erros → 5. Gerar relatorio → 6. Publicar resultado

### Armadilhas comuns do caminho feliz
- **Atividades compostas**: "Recebe, analisa e aprova" → sao tres atividades separadas
- **Lacunas de handoff**: "O comercial passa para o compliance" — como? Via sistema? E-mail? Isso e uma conexao importante
- **Atividades de espera esquecidas**: "Esperamos o cliente assinar" — isso e uma atividade ou evento de espera?

### Confirmacao de Fase 4
> "O caminho feliz tem [N] atividades: [lista numerada]. Esta sequencia esta correta?"

---

## Fase 5 — Decisoes e Ramificacoes

### Abertura
> "Agora vamos identificar os pontos onde o fluxo pode tomar caminhos diferentes. Existe algum momento no processo onde ha uma escolha ou decisao?"

### Tipos de gateway — como identificar

| O usuario diz... | Tipo de gateway | Label sugerido |
|-----------------|-----------------|----------------|
| "Se aprovado, vai para X; se nao, vai para Y" | XOR (exclusiveGateway) | "Aprovado?" |
| "Ao mesmo tempo, enviamos para A e B" | AND (parallelGateway) | (sem label) |
| "Dependendo do tipo, pode ir para um ou mais destinos" | OR (inclusiveGateway) | "Tipo de operacao?" |
| "Esperamos pelo primeiro evento que ocorrer" | Event-based (eventBasedGateway) | "Aguardando resposta" |

### Perguntas-sonda para cada gateway

**Identificar a pergunta do gateway:**
- "O que voce verifica nesse ponto para decidir o caminho?"
- "Quem toma essa decisao? A pessoa ou o sistema?"
- Formular como pergunta com resposta binaria ou multipla: "Documentacao completa?"

**Identificar os ramos:**
- "Quais sao as possiveis respostas a essa pergunta?"
- "Ha um caminho 'padrao' se nenhuma condicao for atendida?"
- Para XOR: "Os caminhos se reencontram em algum ponto? Onde?"

**Verificar convergencia:**
- Para cada gateway divergente, encontrar onde os ramos convergem
- "Apos [ramo A] e [ramo B], o fluxo volta para um ponto comum?"
- Inserir gateway convergente (mesmo tipo, sem label) onde os ramos se unem

### Gateway XOR — checklist de validacao
- [ ] Label e uma pergunta ("Aprovado?", "Valor dentro do limite?")
- [ ] Todos os ramos de saida tem label (condicao)
- [ ] Exatamente um ramo e marcado como default (`isDefault: true`)
- [ ] Ha um gateway XOR de convergencia correspondente (exceto quando ramos terminam em endEvent)

### Armadilhas comuns
- **Gateway sem convergencia**: "Se nao aprovado, termina" — neste caso o ramo vai direto para endEvent, sem necessidade de convergencia
- **XOR vs. AND confundidos**: "Enviamos para compliance e juridico ao mesmo tempo" → AND (paralelo), nao XOR (exclusivo)
- **Decisao implicita**: Atividade que na verdade e um gateway ("Verificar e aprovar ou rejeitar") → separar em atividade + gateway

### Confirmacao de Fase 5
> "Identificamos [N] ponto(s) de decisao: [lista com pergunta e ramos]. Os ramos convergem em [ponto de convergencia]. Esta correto?"

---

## Fase 6 — Excecoes e Eventos Intermediarios

*Aplicavel apenas para N3–N5.*

### Abertura
> "Agora vamos olhar para as excecoes e situacoes especiais. Existe algum momento no processo onde algo pode interromper o fluxo normal, ou onde o processo espera por algo externo?"

### Perguntas-sonda por categoria

**Timeouts e esperas:**
- "O processo espera alguma resposta ou confirmacao que pode demorar? Ha um prazo?"
- "Se o prazo vencer, o que acontece com o processo?"
- Ex.: "Esperamos a assinatura em ate 5 dias. Se nao vier, cancelamos" → boundaryEvent (timer) na atividade "Aguardar assinatura"

**Erros conhecidos:**
- "Ha alguma situacao de erro esperada — nao uma excecao rara, mas algo que acontece com frequencia?"
- "Quando o sistema retorna um erro especifico, o que o processo faz?"
- Ex.: "Se o CPF for invalido, o sistema rejeita e vai para a correcao" → boundaryEvent (error) na atividade de validacao

**Confirmacoes externas:**
- "O processo precisa receber alguma confirmacao de um sistema externo ou de outra area para continuar?"
- Ex.: "Esperamos o D0 do Banco Central para continuar o processamento" → intermediateCatchEvent (message)

**Cancelamentos:**
- "O processo pode ser cancelado a qualquer momento? Por quem e como?"
- Ex.: "O cliente pode cancelar antes da assinatura" → boundaryEvent (signal) com caminho de cancelamento

### Importante
- Evento intermediario NO fluxo: aparece na sequencia como um no normal (ex: "esperar confirmacao antes de continuar")
- Boundary event: fica "colado" em uma atividade especifica (ex: "se esta atividade demorar mais de X, fazer Y")

### Confirmacao de Fase 6
> "Identificamos [N] excecao(oes)/evento(s) intermediario(s): [lista]. Cada um com seu caminho de saida. Confirma?"

---

## Fase 7 — Eventos de Fim

### Abertura
> "Para fechar o mapeamento, quais sao as possiveis conclusoes deste processo? Como ele pode terminar?"

### Perguntas-sonda
- "Qual e a conclusao normal e esperada do processo?"
- "Ha cenarios onde o processo termina de forma diferente — com erro documentado, com cancelamento, com notificacao obrigatoria?"
- "Para cada caminho que identificamos (ramos dos gateways, caminhos de excecao), onde ele termina?"

### Verificacao de completude
Revisar todos os caminhos abertos:
- Cada ramo de gateway que nao volta para o fluxo principal → precisa de endEvent
- Cada caminho de excecao → precisa de endEvent
- O caminho feliz → precisa de endEvent
- Garantir que nenhum no fica sem conexao de saida

### Confirmacao de Fase 7
> "O processo pode terminar de [N] formas: [lista]. Todos os caminhos chegam a um evento de fim. Confirma?"

---

## Fase 8 — Artefatos e Dados (Opcional)

### Abertura
> "Por ultimo, ha documentos ou dados especificos que as atividades consultam ou produzem? Isso e opcional, mas enriquece a documentacao."

### Perguntas-sonda
- "Qual atividade consulta um banco de dados ou sistema? Como esse sistema se chama?"
- "Quais documentos o processo gera como resultado intermediario?"
- "Ha formularios, contratos ou relatorios especificos que passam pelo processo?"

### Quando nao usar artefatos
- N1–N2: raramente necessario; focar no fluxo
- Artefatos demais: se cada atividade tiver um artefato, o diagrama fica poluido; usar apenas os mais relevantes

---

## Sinais de Alerta Durante a Entrevista

| Sinal | O que fazer |
|-------|------------|
| Usuario descreve TO-BE (solucao futura) | "Anotei como melhoria. Para o mapeamento AS-IS, como funciona hoje?" |
| Atividade muito vaga ("Processar o pedido") | "O que especificamente acontece dentro dessa etapa? Quem faz o que?" |
| Gateway sem convergencia clara | "Onde os caminhos se encontram novamente?" |
| Processo com mais de 20 atividades | "Este pode ser um processo N4/N5. Voce quer modelar em N3 com subprocessos?" |
| Usuario nao sabe quem executa | "E possivel verificar com o responsavel? Enquanto isso, uso 'A definir'" |
| Atividade que e na verdade multiplas | "Voce mencionou [X]. E uma unica acao ou varios passos distintos?" |
| Loop sem saida clara | "Quantas vezes isso pode se repetir? Ha um limite? O que encerra o loop?" |

---

## Resumo do Roteiro por Nivel

| Fase | N1 | N2 | N3 | N4 | N5 |
|------|----|----|----|----|-----|
| 1 — Identificacao | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 — Participantes | ❌ | ❌ | ✅ | ✅ | ✅ |
| 3 — Evento de inicio | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4 — Caminho feliz | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5 — Gateways | ✅ simples | ✅ simples | ✅ completo | ✅ completo | ✅ completo |
| 6 — Excecoes | ❌ | ❌ | ✅ | ✅ | ✅ |
| 7 — Eventos de fim | ✅ | ✅ | ✅ | ✅ | ✅ |
| 8 — Artefatos | ❌ | ❌ | opcional | ✅ | ✅ |
