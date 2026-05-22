---
name: generating-executive-reports
description: >-
  Orquestra o pipeline completo Plan-Extract-Analyze-Interpret-Report usando os agentes
  data-scientist e executive-communicator. Coordena iterações entre agentes, adapta
  relatórios por audiência e gera outputs finais em Markdown.
  Use when executing an analysis plan (PLANO-ANALISE.md exists), generating executive reports,
  or when the user asks to run the analysis and produce the report.

  <example>
  Context: PLANO-ANALISE.md exists and user wants to execute
  user: "Execute o plano de análise e gere o relatório"
  assistant: Orquestra data-scientist para extrair e analisar, depois executive-communicator para interpretar e gerar relatório
  </example>

  <example>
  Context: User wants a report on existing data outputs
  user: "Gera o relatório executivo a partir desses dados"
  assistant: Invoca executive-communicator para interpretar outputs existentes e gerar relatório adaptado
  </example>
user-invocable: true
---

# Generating Executive Reports — Orquestração do Pipeline

> "O dado sem narrativa é ruído. A narrativa sem dado é achismo. Esta skill conecta ambos."

Esta skill orquestra o pipeline completo de análise, coordenando a interação entre os agentes `data-scientist` (extração e análise) e `executive-communicator` (interpretação e relatório).

## Dependências Internas

- [references/audience-adaptation-framework.md](references/audience-adaptation-framework.md) — 4 perfis × 6 dimensões
- [references/executive-writing-guide.md](references/executive-writing-guide.md) — Fórmulas de escrita
- [templates/analytics-briefing.tmpl.md](templates/analytics-briefing.tmpl.md) — **Briefing canônico do Analytics Report M7** (fonte da verdade do conteúdo; é transcrito ao HTML do Design System no Claude Design)
- `docs/INDICADORES.md` — Definições de métricas do projeto (queries, comparativos, contexto de negócio)
- Agent `data-scientist` — Extração e análise de dados
- Agent `executive-communicator` — Interpretação e preenchimento do briefing

> **Onde o relatório vira HTML.** Esta skill **não** gera o HTML final. Ela produz um briefing markdown 100% preenchido — todos os `{{PLACEHOLDERS}}` resolvidos com valores reais — que serve de **input para o Claude Design**, onde o `templates/template-analytics.html` do M7 Design System é preenchido via find & replace e exportado em PDF.

## Pré-requisitos

- `PLANO-ANALISE.md` existente no diretório de trabalho (gerado pela skill `planning-analysis`)
- MCPs configurados e acessíveis (conforme mapeado no plano)
- Estrutura de pastas criada (`docs/`, `data/extractions/`, `src/`, `output/`)

## Pipeline Completo

```
PLANO-ANALISE.md
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 1: EXTRACT + ANALYZE (data-scientist)                 │
│                                                             │
│  1. Ler PLANO-ANALISE.md — métricas, fontes, período        │
│  2. Explorar schemas MCP (se necessário)                    │
│  3. Extrair dados de cada fonte conforme mapeamento         │
│  4. Validar qualidade (checklist obrigatório)               │
│  5. Transformar e calcular métricas definidas               │
│  6. Executar cross-source join se planejado                 │
│  7. Salvar todos os outputs em output/data-scientist/       │
│                                                             │
│  Outputs: tabelas .md, CSVs, métricas rotuladas             │
└──────────────┬──────────────────────────────────────────────┘
               │ outputs brutos (dados, não interpretação)
               ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 2: INTERPRET + BRIEF (executive-communicator)         │
│                                                             │
│  1. Ler PLANO-ANALISE.md — audiência, narrativa, blocos     │
│  2. Ler todos os outputs de output/data-scientist/          │
│  3. Aplicar framework de audiência (4 perfis × 6 dimensões) │
│  4. Consultar guia de escrita executiva                     │
│  5. Preencher analytics-briefing.tmpl.md (cada {{TOKEN}}    │
│     com valor real; apagar blocos `>` de instrução)         │
│  6. Se dados insuficientes → gerar Solicitação Complementar │
│  7. Salvar como output/ANL-{AREA}-{NNN}-briefing.md         │
│                                                             │
│  Output: briefing markdown pronto p/ Claude Design          │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼ (se dados insuficientes)
┌─────────────────────────────────────────────────────────────┐
│  FASE 3: ITERATE (max 3 ciclos)                             │
│                                                             │
│  Ciclo:                                                     │
│  1. executive-communicator gera Solicitação Complementar    │
│  2. data-scientist executa queries adicionais               │
│  3. executive-communicator atualiza briefing                │
│  4. Repetir até dados suficientes ou max 3 ciclos           │
│                                                             │
│  Se após 3 ciclos: informar usuário + gerar com dados       │
│  disponíveis sinalizando lacunas                            │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 4: VALIDATE                                           │
│                                                             │
│  1. Checklist de integridade da análise                     │
│  2. Checklist de conformidade do briefing M7                │
│  3. Verificar rastreabilidade (todo dado → output source)   │
│  4. Salvar versão final em output/ANL-{ÁREA}-{NNN}-briefing │
│     .md                                                     │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 5: HANDOFF (Claude Design)                            │
│                                                             │
│  Apresentar ao usuário as instruções de transposição:       │
│  briefing → template-analytics.html → PDF                   │
│  (executado fora da skill, no Claude Design)                │
└─────────────────────────────────────────────────────────────┘
```

## Execução Detalhada

### Fase 1: Invocar data-scientist

Prompt para o agente:

```
Leia o PLANO-ANALISE.md em [diretório].
Execute as análises listadas na seção "Instruções para data-scientist".

Se docs/INDICADORES.md existir no diretório de trabalho:
1. Leia a definição de cada métrica (fórmula, fonte, comparativos, contexto)
2. Use a fórmula definida para construir a query
3. Execute o checklist de validação de qualidade padrão
4. Se anomalia detectada, use o contexto de negócio do INDICADORES.md para cortes investigativos

Para todas as métricas:
1. Extraia os dados da fonte MCP indicada
2. Execute o checklist de validação de qualidade padrão
3. Calcule os comparativos definidos (YoY/MoM/vs meta)

Salve todos os outputs em output/data-scientist/ com nomes descritivos.
Se precisar de cross-source join, siga o Padrão #7 dos analysis-patterns.
```

**Critérios de saída da Fase 1:**
- [ ] Todas as métricas do plano foram extraídas
- [ ] Checklist de qualidade executado para cada extração
- [ ] Comparativos calculados
- [ ] Outputs salvos em `output/data-scientist/`

### Fase 2: Invocar executive-communicator

Prompt para o agente:

```
Leia o PLANO-ANALISE.md em [diretório] (audiência, narrativa, blocos).
Leia todos os outputs em output/data-scientist/.
Consulte references/audience-adaptation-framework.md para calibração.
Consulte references/executive-writing-guide.md para padrões de escrita.

USE templates/analytics-briefing.tmpl.md como base obrigatória.
Esse template é o briefing canônico do Analytics Report do M7 Design
System: ele será depois transcrito ao HTML no Claude Design.

Tarefa: preencher cada {{TOKEN}} do briefing com valor real,
respeitando estas regras DURAS do template:

  · Pergunta única por análise; conclusão antes do dado; toda
    métrica com referência (meta / período anterior / benchmark /
    baseline) — sem exceção.
  · §1 Controle: código ANL-{AREA}-{NNN}, versão, elaborador,
    revisor, aprovador, classificação.
  · §2 Capa: COVER_TITULO_LINHA1/2 + DESTAQUE + SUBTITULO +
    PERGUNTA (uma frase) + PERIODO_REFERENCIA.
  · §3 TL;DR: LEDE + 4 KPIs (cada um com KPI_EXEC_N_REFERENCIA
    obrigatório) + findings F-N com IMPACTO ("e daí?")
    não-negociável e EVIDENCIA cruzada (`ver §X.Y, p.NN`).
  · §4 Scorecard: 8-10 KPIs (teto 12), sem duplicar os 4 do TL;DR;
    status `ok|warn|bad` com label.
  · §5 Contexto: PERIODO_PRINCIPAL/COMPARATIVO, DATA_SNAPSHOT,
    COBERTURA/EXCLUSOES, TRATAMENTO, LIMITACAO, e tabela de FONTES
    ordenada por relevância com timeliness (D-0/D+1/D+7/M+1) e
    contribuição específica.
  · §6 Análises: uma pergunta por análise; cada subseção referencia
    UM dos 12 tipos canônicos do DS (`graficos.html`) — Resultado vs
    meta, Pareto, Ranking, Radar, Teia, Dispersão, Histograma,
    Treemap, Linha temporal, Waterfall, Funil, Árvore. Indique o
    tipo em {{A_SUBN_GRAFICO_TITULO}}.
  · §7 Insights narrados: findings completos com IMPACTO + Hipóteses
    abertas (H-N) com dado faltante.
  · §8 Recomendações: cada R_N com dono, prazo, ICE = (I × C) / E.
  · §9 Anexos: dicionário de métricas + glossário.

Se docs/INDICADORES.md existir no diretório de trabalho:
  · Use as definições para popular §9 Anexos (dicionário)
  · Use benchmarks/faixas para calibrar findings em §7
  · Use contexto de negócio para o IMPACTO das recomendações em §8

Apague todo bloco `>` (instrução do template) do output final —
o briefing entregue é só conteúdo, sem comentários do guia.

Salve em output/ANL-{AREA}-{NNN}-briefing.md
(use o mesmo código do {{CODIGO_DOCUMENTO}} preenchido na §1).

Se dados forem insuficientes, gere uma Solicitação de Dados
Complementares ao invés do briefing.
```

**Critérios de saída da Fase 2:**
- [ ] Briefing gerado com TODAS as seções §1–§9 preenchidas
- [ ] Nenhum `{{TOKEN}}` literal restante no output (apenas valores)
- [ ] Nenhum bloco `>` (instrução) restante no output
- [ ] Linguagem adequada à audiência definida no PLANO-ANALISE.md
- [ ] Cada KPI do TL;DR tem `{{KPI_EXEC_N_REFERENCIA}}` preenchido
- [ ] Cada finding tem `{{F_N_IMPACTO}}` ("e daí?") preenchido
- [ ] Cada recomendação tem dono, prazo e ICE calculado
- [ ] Todos os números rastreáveis aos outputs do data-scientist
- [ ] OU Solicitação Complementar gerada (→ Fase 3)

### Fase 3: Protocolo de Iteração

**Formato da Solicitação Complementar:**

```markdown
## Solicitação de Dados Complementares — Ciclo N/3

### Necessidade 1
- **Métrica**: [nome da métrica faltante]
- **Período**: [intervalo temporal necessário]
- **Granularidade**: [diário / semanal / mensal]
- **Fonte provável**: [Bitrix24: tool_name / ClickHouse: SQL hint]
- **Formato esperado**: [tabela / valor único / série temporal]
- **Justificativa**: [por que é necessário para completar o relatório]

### Necessidade 2
- ...
```

**Regras de iteração:**
1. Máximo **3 ciclos** de solicitação-resposta
2. Cada solicitação deve ser **específica e acionável** pelo data-scientist
3. Solicitação inclui **fonte provável** para acelerar a extração
4. Após 3 ciclos sem resolução: gerar relatório com dados disponíveis + seção "Limitações"
5. **Nunca** solicitar dados que já existem nos outputs

### Fase 4: Validação Final

**Checklist de qualidade do briefing** (espelha o checklist final do template — ver §"Checklist final" do `analytics-briefing.tmpl.md`):

```
VALIDAÇÃO FINAL — INTEGRIDADE DE ANÁLISE
────────────────────────────────────────
[ ] Todos os blocos temáticos do PLANO-ANALISE.md cobertos
[ ] Todos os números rastreáveis a outputs de output/data-scientist/
[ ] Linguagem adequada à audiência definida no plano
[ ] Comparativos incluídos em todos os KPIs (sem número solto)
[ ] Nenhuma solicitação pendente do executive-communicator

VALIDAÇÃO FINAL — CONFORMIDADE COM BRIEFING M7
──────────────────────────────────────────────
[ ] Código segue padrão ANL-{ÁREA}-{NNN}
[ ] Capa responde à pergunta de pesquisa em uma frase
[ ] Sumário executivo cabe em 1 página
[ ] Todo KPI do TL;DR tem {{KPI_EXEC_N_REFERENCIA}} preenchido
[ ] Os 4 KPIs do TL;DR NÃO duplicam os 4 primeiros do scorecard
[ ] Cada análise responde UMA pergunta clara
[ ] Cada subseção indica um dos 12 tipos canônicos do DS
[ ] Tabela de fontes tem timeliness e contribuição preenchidos
[ ] Cada finding (F-N) tem IMPACTO ("e daí?") preenchido
[ ] Toda recomendação tem dono, prazo e ICE
[ ] Dicionário cobre todas as métricas mencionadas
[ ] Limitações estão explícitas (não escondidas)
[ ] Aprovador assinado — {{NOME_APROVADOR}} não está vazio
[ ] Versão e data coerentes em §1 Controle e §2 Capa
[ ] Briefing salvo em output/ANL-{ÁREA}-{NNN}-briefing.md
```

**Se algum item falhar:** corrigir antes de entregar.

### Fase 5: Handoff para Claude Design

> Esta skill **encerra no briefing markdown**. A geração do PDF final
> acontece fora, no Claude Design — passe o output da Fase 4 para lá.

**Instruções a apresentar ao usuário ao concluir:**

```
Briefing pronto: output/ANL-{ÁREA}-{NNN}-briefing.md

Próximos passos no Claude Design:
1. Duplicar templates/template-analytics.html do M7 Design System
2. Renomear para ANL-{ÁREA}-{NNN}.html
3. Para cada {{TOKEN}} do template HTML, colar o valor do briefing
   (find & replace 1:1 — os tokens são idênticos)
4. Para cada subseção em §6, copiar o <svg> do tipo canônico
   indicado em {{A_SUBN_GRAFICO_TITULO}} a partir de graficos.html
   do DS, e ajustar valores/rótulos/cores aos dados do briefing
5. Abrir no Chrome/Edge → ⌘P → Salvar como PDF
   (não use Safari — quebra fontes ocasionalmente)
```

A skill **não** executa esses passos — eles vivem no Design System M7. O briefing existe justamente para que essa transposição seja mecânica (find & replace), não interpretativa.

## Adaptação por Audiência (Quick Reference)

| Aspecto | Diretoria | Gerentes | Técnico | Comercial |
|---------|-----------|----------|---------|-----------|
| **Métricas** | 3-5 chave | 5-8 com contexto | Todas | Rankings + metas |
| **Blocos** | Max 3 | Max 4 | Sem limite | Max 3 |
| **Bullets/bloco** | 3-5 | 4-6 | Sem limite | 3-5 |
| **Páginas** | 1-2 | 2-3 | 3-5 | 2-3 |
| **Linguagem** | Zero jargão | Negócio + domínio | Técnica ok | Comercial |
| **Dados brutos** | Nunca | Resumo | Completo | Nunca |
| **CTA** | Decisão + deadline | Ação + owner + prazo | Tasks + timeline | Meta + oportunidade |

Para detalhes completos, ver [references/audience-adaptation-framework.md](references/audience-adaptation-framework.md).

## Fluxo Alternativo: Relatório sem PLANO-ANALISE.md

Se outputs do data-scientist já existem mas não há PLANO-ANALISE.md:

1. Perguntar ao usuário: **audiência** e **objetivo**
2. Ler outputs disponíveis em `output/data-scientist/`
3. Invocar executive-communicator diretamente com contexto mínimo
4. Recomendar ao usuário usar `planning-analysis` nas próximas vezes

## Anti-Patterns

- ❌ NUNCA pular a Fase 1 (extração) e ir direto para o briefing sem dados
- ❌ NUNCA permitir que o executive-communicator invente dados
- ❌ NUNCA exceder 3 ciclos de iteração sem escalar ao usuário
- ❌ NUNCA gerar briefing sem verificar a audiência definida no plano
- ❌ NUNCA misturar outputs dos agentes — data-scientist salva em `output/data-scientist/`, briefing final em `output/`
- ❌ NUNCA entregar briefing sem executar o checklist de validação final
- ❌ NUNCA entregar briefing com `{{TOKENS}}` literais não substituídos
- ❌ NUNCA entregar briefing com blocos `>` (instruções do template) restantes
- ❌ NUNCA gerar o HTML/PDF aqui — esse passo é responsabilidade do **Claude Design** (Fase 5)
- ❌ NUNCA escolher um gráfico fora dos 12 tipos canônicos do DS sem justificar no rodapé
