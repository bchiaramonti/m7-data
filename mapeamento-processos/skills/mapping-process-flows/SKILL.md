---
name: mapping-process-flows
description: >-
  Conduz entrevista estruturada para mapear o fluxo de atividades de um processo,
  adaptada ao nivel de modelagem (N1–N5). Coleta participantes, eventos, atividades,
  gateways e excecoes via AskUserQuestion, e gera JSON compativel com a skill
  drawing-bpmn-flowcharts mais um descritivo Markdown do fluxo.
  Use when the user wants to map a process flow, create a BPMN from scratch,
  describe process steps for a flowchart, or conduct a structured process flow workshop.

  <example>
  Context: User needs to document a new process flow
  user: "Preciso mapear o fluxo do processo de aprovacao de credito"
  assistant: Inicia entrevista estruturada fase a fase, coleta participantes, atividades, decisoes e eventos via AskUserQuestion, e gera JSON bpmn-input.json + flow-descritivo.md
  </example>

  <example>
  Context: User wants to generate a BPMN file but doesn't know the JSON format
  user: "Quero criar um diagrama BPMN do processo de abertura de conta, mas nao sei o JSON"
  assistant: Conduz entrevista de mapeamento do fluxo para coletar as informacoes e produz o JSON pronto para drawing-bpmn-flowcharts gerar o arquivo .bpmn
  </example>

user-invocable: true
---

# Mapeamento de Fluxo de Processo (BPMN)

Conduz uma entrevista estruturada com o usuario para mapear o fluxo de atividades de um processo, identificar participantes, decisoes e excecoes, e gerar os artefatos que alimentam a skill `drawing-bpmn-flowcharts`.

## Filosofia

> "Antes de desenhar o fluxo, entenda quem faz o que, quando, e por que as excecoes existem."

A entrevista segue a ordem **de dentro para fora**: primeiro o caminho feliz (espinha dorsal do processo), depois as decisoes que ramificam, depois as excecoes que desviam. Isso evita o erro comum de comecar pelas excecoes e perder o foco no fluxo principal.

## Dependencias

```
<this-skill>/
├── SKILL.md                              # Este arquivo
├── references/
│   ├── interview-guide.md                # Roteiro de entrevista com perguntas-sonda por fase
│   └── bpmn-flow-elements.md             # Guia de elementos BPMN por nivel (N1–N5)
└── templates/
    └── flow-descritivo.tmpl.md           # Template Markdown do descritivo do fluxo
```

## Artefatos de Saida

| Artefato | Formato | Consumidor |
|----------|---------|------------|
| BPMN Input JSON | `.json` | Skill `drawing-bpmn-flowcharts` (gera arquivo .bpmn) |
| Descritivo do Fluxo | `.md` | Documentacao do processo (leitura humana) |

**Pipeline**: `mapping-process-flows` → JSON + MD → `drawing-bpmn-flowcharts` → `.bpmn` + `-descritivo.md`

## Nivel de Modelagem — Impacto no Mapeamento

O nivel (N1–N5) determina o grau de detalhe e os elementos permitidos:

| Nivel | Descricao | Lanes? | Eventos avancados? | Uso tipico |
|-------|-----------|--------|-------------------|------------|
| N1 | Processo na cadeia de valor | Nao | Nao | Mapa de processos corporativo |
| N2 | Macroprocesso | Nao | Nao | DEIP / visao geral |
| N3 | Processo operacional | Sim | Sim | Padrao operacional de processo |
| N4 | Subprocesso | Sim | Sim | Detalhamento de etapas N3 |
| N5 | Procedimento | Sim | Sim | Instrucao de trabalho |

**Regra critica**: N1–N2 = logico (sem lanes, sem boundary events, gateways simples). N3–N5 = fisico (lanes obrigatorias, todos os elementos disponiveis).

## Workflow

### Regras Gerais da Entrevista

1. **Uma pergunta por vez** — nunca sobrecarregar o usuario
2. **Sugerir quando possivel** — oferecer opcoes baseadas no contexto
3. **Usar `AskUserQuestion`** — para todas as interacoes estruturadas
4. **Inferir do contexto** — se o usuario ja forneceu informacao, nao perguntar de novo
5. **Validar antes de avancar** — confirmar dados coletados ao final de cada fase
6. **Manter progresso visivel** — usar `TodoWrite` para rastrear o andamento das fases

Para roteiro detalhado de perguntas, ver [interview-guide.md](references/interview-guide.md).
Para guia de elementos por nivel, ver [bpmn-flow-elements.md](references/bpmn-flow-elements.md).

---

### Fase 1 — Identificar o Processo

Coletar metadados basicos:

| Campo | Como coletar |
|-------|-------------|
| Nome do processo | Pergunta aberta |
| Codigo (se houver) | Pergunta aberta (ex: "G2.3") — opcional |
| Nivel BPM | `AskUserQuestion` com opcoes: N1 / N2 / N3 / N4 / N5 |
| Responsavel pelo processo | Pergunta aberta (area ou cargo) |
| Objetivo | "Em uma frase, qual o proposito deste processo?" |
| Versao e data | Sugerir "1.0" e data de hoje, confirmar |

**Validacao**: Nome, nivel e objetivo preenchidos antes de avancar.

**Output parcial**: Preencher secao `metadata` do JSON:
```json
{
  "metadata": {
    "title": "<nome>",
    "level": "<N1|N2|N3|N4|N5>",
    "version": "1.0",
    "date": "<YYYY-MM-DD>",
    "author": "<responsavel>"
  }
}
```

---

### Fase 2 — Mapear Participantes

**N1–N2**: Pular esta fase (sem pools nem lanes). Usar um pool implicito com o nome do processo.

**N3–N5**: Coletar:

**2a — Pools (entidades externas ou sistemas separados)**

Perguntar: "Ha sistemas externos, outras empresas ou unidades organizacionais completamente separadas que participam do processo?"
- Se sim: nome de cada pool, descricao breve
- Se nao: um unico pool com o nome do processo

**2b — Lanes (atores dentro do pool principal)**

Perguntar: "Dentro do processo, quem sao os responsaveis por executar as atividades? Liste os cargos ou areas envolvidos."
- Cada lane = um ator (ex: "Assessor", "Compliance", "Sistema CRM")
- Minimo 1 lane; maximo recomendado 5 (mais que isso indica processo muito complexo para N3)

**Output parcial**: Preencher secao `pools` do JSON:
```json
{
  "pools": [
    {
      "id": "pool_principal",
      "name": "<nome do pool>",
      "isExecutable": false,
      "lanes": [
        { "id": "lane_1", "name": "<ator 1>" },
        { "id": "lane_2", "name": "<ator 2>" }
      ]
    }
  ]
}
```

---

### Fase 3 — Evento de Inicio

Identificar o trigger que dispara o processo.

Perguntar: "O que inicia este processo? Como ele comeca?"

Mapear para o tipo de evento correto (ver [bpmn-flow-elements.md](references/bpmn-flow-elements.md)):

| O usuario diz... | Tipo BPMN |
|-----------------|-----------|
| "Quando o cliente solicita..." | `startEvent` (none) |
| "Quando recebemos um e-mail/mensagem..." | `messageStartEvent` |
| "Todo dia X / de hora em hora..." | `timerStartEvent` |
| "Quando o sistema notifica..." | `signalStartEvent` |

Coletar:
- Descricao do trigger
- Em qual lane ocorre (N3–N5)

**Output parcial**: Adicionar no `nodes`:
```json
{ "id": "start_1", "type": "startEvent", "label": "<descricao do trigger>", "pool": "pool_principal", "lane": "lane_1" }
```

---

### Fase 4 — Caminho Feliz (Atividades Principais)

Mapear o fluxo principal do processo passo a passo, **sem ramificacoes ainda**.

Perguntar: "Descrevendo o cenario ideal, sem excecoes ou erros, quais sao os passos do processo em sequencia?"

Para cada atividade:
1. **Nome**: formatar como verbo + complemento ("Analisar documentacao do cliente", "Emitir contrato")
2. **Tipo de atividade**: User Task (pessoa), Service Task (sistema automatico), Script Task (regra automatizada), ou Task simples (nao especificado)
3. **Lane responsavel** (N3–N5): quem executa esta atividade?

Regras de nomenclatura:
- Usar verbo no infinitivo ou 3a pessoa ("Verificar" ou "Verifica")
- Nunca usar nomes genericos ("Processar", "Executar", "Fazer")
- Cada atividade: uma responsabilidade clara

Sugerir agrupamentos e confirmar com o usuario antes de avancar.

**Output parcial**: Adicionar cada atividade em `nodes` e cada conexao em `edges`:
```json
{ "id": "task_1", "type": "userTask", "label": "Receber solicitacao do cliente", "pool": "pool_principal", "lane": "lane_1" },
{ "id": "seq_1", "type": "sequenceFlow", "source": "start_1", "target": "task_1" }
```

---

### Fase 5 — Decisoes e Ramificacoes (Gateways)

Identificar os pontos de decisao no fluxo mapeado.

Perguntar: "Existe algum ponto no processo onde o fluxo pode tomar caminhos diferentes? Qual a condicao?"

Para cada gateway:
1. **Pergunta do gateway**: formatar como pergunta direta ("Documentacao completa?", "Valor aprovado?")
2. **Tipo**: XOR (apenas um caminho) | AND (caminhos paralelos) | OR (um ou mais caminhos)
3. **Ramos de saida**: nome de cada ramo e condicao
4. **Caminho padrao** (XOR): qual ramo e o padrao se nenhuma condicao for satisfeita?
5. **Convergencia**: onde os ramos se reencontram?

Inserir o gateway na posicao correta entre as atividades do caminho feliz. Ajustar as conexoes anteriores conforme necessario.

**Output parcial**:
```json
{ "id": "gw_1", "type": "exclusiveGateway", "label": "Documentacao completa?", "pool": "pool_principal", "lane": "lane_compliance" },
{ "id": "seq_gw_sim", "type": "sequenceFlow", "source": "gw_1", "target": "task_aprovacao", "label": "Sim", "isDefault": false },
{ "id": "seq_gw_nao", "type": "sequenceFlow", "source": "gw_1", "target": "task_devolucao", "label": "Nao", "isDefault": true }
```

---

### Fase 6 — Excecoes e Eventos Intermediarios

**N1–N2**: Pular esta fase (apenas caminho feliz e gateways simples).

**N3–N5**: Identificar excecoes, timeouts e interacoes externas.

Perguntar: "Existe alguma situacao onde o processo e interrompido, espera uma confirmacao externa, ou falha de forma esperada?"

Tipos de situacoes a investigar:

| Situacao | Elemento BPMN |
|----------|---------------|
| "Esperamos resposta do cliente em ate X dias" | `intermediateCatchEvent` (timer) ou boundary event |
| "Se o sistema falha, o processo volta para..." | `boundaryEvent` (error) na atividade |
| "Quando recebemos confirmacao bancaria, continuamos" | `intermediateCatchEvent` (message) |
| "Cada X horas verificamos o status" | `intermediateCatchEvent` (timer) |
| "O processo pode ser cancelado a qualquer momento" | `boundaryEvent` (signal) no subprocesso |

Coletar para cada excecao:
- Descricao da situacao
- Atividade onde ocorre (N3–N5: boundary events ficam "attached" a atividade)
- O que acontece depois (caminho de excecao)

---

### Fase 7 — Eventos de Fim

Identificar todos os possiveis estados de conclusao do processo.

Perguntar: "Como o processo pode terminar? Existe mais de uma forma de conclusao?"

| Conclusao | Tipo BPMN |
|-----------|-----------|
| Conclusao normal | `endEvent` (none) |
| Mensagem enviada ao finalizar | `messageEndEvent` |
| Processo termina com erro documentado | `errorEndEvent` |
| Termina e cancela tudo que esta em andamento | `terminateEndEvent` |

Um evento de fim para cada caminho identificado nas fases 4, 5 e 6. Verificar que todos os caminhos tem um fim — nenhum no-ar.

---

### Fase 8 — Artefatos e Dados (Opcional)

Perguntar: "Ha documentos, dados ou sistemas especificos que as atividades consultam ou produzem?"

Tipos:
- **Data Object**: documento ou dado produzido/consumido por uma atividade (ex: "Formulario KYC", "Relatorio de analise")
- **Data Store**: banco de dados ou sistema consultado (ex: "CRM", "Sistema de credito")
- **Annotation**: nota explicativa sobre uma atividade

Coletar apenas o que o usuario mencionar — nao inventar artefatos.

---

### Geracao de Artefatos

Apos todas as fases (ou quando o usuario confirmar que o mapeamento esta completo):

**G1 — Montar JSON completo**

Consolidar todos os `nodes` e `edges` coletados nas fases anteriores no schema completo:

```json
{
  "metadata": {
    "title": "<nome do processo>",
    "level": "<N1|N2|N3|N4|N5>",
    "version": "1.0",
    "date": "<YYYY-MM-DD>",
    "author": "<responsavel>"
  },
  "pools": [
    {
      "id": "pool_principal",
      "name": "<nome>",
      "isExecutable": false,
      "lanes": [
        { "id": "lane_1", "name": "<ator>" }
      ]
    }
  ],
  "nodes": [
    { "id": "<id>", "type": "<tipo>", "label": "<nome>", "pool": "<pool_id>", "lane": "<lane_id>", "description": "<opcional>" }
  ],
  "edges": [
    { "id": "<id>", "type": "sequenceFlow", "source": "<id>", "target": "<id>", "label": "<condicao opcional>", "isDefault": false }
  ]
}
```

Salvar como `<nome-processo-kebab>-bpmn-input.json`.

**G2 — Gerar descritivo do fluxo**

Usar o template em [flow-descritivo.tmpl.md](templates/flow-descritivo.tmpl.md) e preencher com os dados coletados.

Salvar como `<nome-processo-kebab>-descritivo.md`.

**G3 — Sugerir proximo passo**

> "O mapeamento do fluxo foi concluido. Deseja gerar o arquivo BPMN agora? Posso usar a skill `drawing-bpmn-flowcharts` com o JSON produzido para gerar o `.bpmn` pronto para abrir no Camunda Modeler ou bpmn.io."

## Validacao Pre-Geracao

Antes de gerar os artefatos, verificar:

- [ ] Exatamente 1 evento de inicio por processo (ou por pool)
- [ ] Pelo menos 1 evento de fim
- [ ] Todos os caminhos chegam a um evento de fim
- [ ] Nenhum no desconectado (sem incoming/outgoing)
- [ ] Todo gateway divergente tem um gateway convergente par (XOR↔XOR, AND↔AND)
- [ ] Gateways XOR: todos os ramos rotulados + 1 caminho default
- [ ] Atividades: nomes no formato verbo + complemento, sem genericos
- [ ] N3–N5: toda atividade esta em uma lane
- [ ] N1–N2: sem lanes, sem boundary events

## Anti-Padroes

- **NAO pular a validacao** — processos mal formados geram XML invalido no drawing-bpmn-flowcharts
- **NAO comecar pelas excecoes** — sempre mapear o caminho feliz primeiro (Fase 4 antes da Fase 6)
- **NAO usar nomes genericos** — "Processar", "Executar", "Fazer" nao dizem nada
- **NAO criar gateways sem convergencia** — cada divergencia precisa de uma convergencia
- **NAO misturar niveis** — N1-N2 sem lanes; N3-N5 com lanes e atores explicitos
- **NAO inventar dados** — sugerir e esperar confirmacao do usuario
- **NAO fazer mais de uma pergunta por vez** — entrevista, nao formulario

## Recursos Adicionais

- Para roteiro de entrevista detalhado: [interview-guide.md](references/interview-guide.md)
- Para guia de elementos BPMN por nivel: [bpmn-flow-elements.md](references/bpmn-flow-elements.md)
- Para template do descritivo: [flow-descritivo.tmpl.md](templates/flow-descritivo.tmpl.md)
- Para gerar o BPMN a partir do JSON: skill `drawing-bpmn-flowcharts`
- Para validar o BPMN gerado: agente `bpmn-reviewer`
- Para schema JSON completo com todos os tipos de elementos: `drawing-bpmn-flowcharts/references/BPMN-NOTATION.md`
