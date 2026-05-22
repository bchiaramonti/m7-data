---
name: planning-analysis
description: >-
  Planeja análises de dados produzindo PLANO-ANALISE.md e docs/INDICADORES.md
  que servem como contrato executável entre os agentes data-scientist e
  executive-communicator. O plano é desenhado como blueprint do briefing
  canônico do M7 Design System: cada seção mapeia 1:1 ao analytics-briefing.tmpl.md
  consumido na fase de geração do relatório.
  Use when the user asks for data analysis, needs a report, mentions business
  intelligence, or wants to plan before executing. Also use when the user provides
  a business question that requires data to answer.

  <example>
  Context: User wants to analyze sales performance
  user: "Preciso analisar a performance de vendas do último trimestre"
  assistant: Planeja a análise definindo código documental, pergunta única, audiência, fontes, indicadores (com papel destaque-tldr/detalhe-scorecard), blocos com tipo de gráfico canônico, findings e recomendações candidatas
  </example>

  <example>
  Context: User wants a recurring report
  user: "Quero montar um relatório mensal de captação para a diretoria"
  assistant: Planeja com audiência Diretoria (quotas: 4 KPIs TL;DR, 6-8 scorecard, 2-3 blocos), métricas com YoY+MoM, gráficos canônicos restritos à audiência
  </example>
user-invocable: true
---

# Planning Analysis — Blueprint do Analytics Report

> "O plano não é roteiro genérico — é blueprint. Cada seção do plano vira
> uma `§N` do briefing canônico, sem improviso entre as duas pontas."

Esta skill desenha o blueprint completo de uma análise de dados, produzindo:

1. **`PLANO-ANALISE.md`** — contrato estruturado seção-por-seção espelhando o briefing canônico (`analytics-briefing.tmpl.md`) consumido pela skill `generating-executive-reports`
2. **`docs/INDICADORES.md`** — fonte da verdade das métricas, **obrigatório** desde v4.0.0

A skill **não** executa a análise. Ela garante que, quando o `data-scientist`
e o `executive-communicator` rodarem, eles encontram um plano sem ambiguidade
e geram um briefing já dimensionado para o briefing canônico.

## Dependências Internas

- [templates/plano-analise.tmpl.md](templates/plano-analise.tmpl.md) — Estrutura do contrato (11 seções espelhando o briefing)
- [templates/indicadores.tmpl.md](templates/indicadores.tmpl.md) — Template canônico do `docs/INDICADORES.md`
- [references/audiencia-profundidade.md](references/audiencia-profundidade.md) — Matriz "audiência → quotas" (Fase 2)
- [references/grafico-por-bloco.md](references/grafico-por-bloco.md) — Decisão dos 12 tipos canônicos (Fase 5)
- [references/analysis-patterns.md](references/analysis-patterns.md) — 7 padrões pré-montados (consulta opcional na Fase 5)
- Skill `exploring-data-sources` — se `DATA-PROFILE.md` existir, reutilizar na Fase 3
- Skill `generating-executive-reports` — consome o output desta skill

## Pré-requisitos

- **Fontes de dados configuradas** (MCPs, scripts Python, arquivos CSV — o que o usuário tiver disponível). A skill é MCP-agnostic; o `data-scientist` agent é que precisa de acesso real às fontes na fase de extração
- **Diretório de trabalho** definido (path absoluto, não relativo)
- **Audiência primária** conhecida (Diretoria, Gerentes, Técnico ou Comercial)

## Workflow (8 fases)

### Fase 1 — Identificação & Pergunta Única

Coletar via conversa:

| Dimensão | Pergunta ao usuário | Obrigatório |
|---|---|---|
| **Código documental** | Qual área (sigla 3 letras) e número sequencial? Ex.: `ANL-COM-001` | Sim — é o `{{CODIGO_DOCUMENTO}}` do briefing |
| **Pergunta única** | A análise responde, em UMA frase, qual pergunta? | Sim — vira `{{COVER_PERGUNTA}}` |
| **Hipótese inicial** | O que você espera encontrar? | Não, mas recomendado |
| **Área + Diretoria** | Quem é dono do conteúdo? | Sim |
| **Elaborador / Revisor / Aprovador** | Quem assina? | Sim |
| **Contexto** | Reunião mensal? Ad-hoc? Crise? Planejamento? | Sim |
| **Urgência** | Para quando? | Não |
| **Precedentes** | Já existe análise similar? `DATA-PROFILE.md`? | Não |

> ⚠ Se a pergunta não couber em uma frase, **pare** — o usuário ainda não
> sabe o que está investigando. Refinar antes de seguir.

### Fase 2 — Audiência & Profundidade

1. **Definir audiência primária** (Diretoria / Gerentes / Técnico / Comercial). Audiência híbrida → usar a quota mais restritiva
2. **Consultar [audiencia-profundidade.md](references/audiencia-profundidade.md)** e extrair as 9 quotas para essa audiência (KPIs TL;DR, scorecard, blocos, subseções, findings, recomendações, páginas, dados brutos, linguagem)
3. **Definir tom** (Otimista / Cauteloso / Neutro / Alarmante)
4. **Anotar restrições editoriais** específicas desta análise

> Validação: se o pedido excede as quotas (ex.: "8 blocos para Diretoria"),
> escalar ao usuário com 3 opções — reduzir escopo, mudar audiência, ou
> dividir em dois briefings.

### Fase 3 — Período, Snapshot & Fontes

1. **Período principal** + **período comparativo** (YYYY-MM → YYYY-MM)
2. **Data de snapshot** (quando os dados foram extraídos — para reprodutibilidade)
3. **Sazonalidade** (alta / média / baixa). Regra dura: **se alta → YoY é obrigatório** em todos os KPIs temporais
4. **Eventos atípicos no período** (campanha, crise, mudança regulatória) — declarar antes da extração
5. **Fontes mapeadas** ordenadas por relevância:
   - Se `DATA-PROFILE.md` existir, reutilizar schemas
   - Caso contrário, listar as fontes que o usuário tem acesso (MCP, scripts, arquivos) com:
     - Nome técnico (tabela, view, endpoint)
     - Stack (MCP-x · script Python · arquivo CSV — string livre)
     - **Timeliness**: `D-0` (real-time) · `D+1` · `D+7` · `M+1` · `M+15`
     - **Contribuição esperada** específica (ex.: "série mensal para §3.1, base do KPI de captação")
6. **Validar acesso real** (gate): se a fonte foi citada mas o agente downstream não consegue alcançá-la, sinalizar agora — não na fase de extração

### Fase 4 — Indicadores (preenchimento obrigatório do `docs/INDICADORES.md`)

**Obrigatório desde v4.0.0**. Os agentes `data-scientist` e `executive-communicator` **abortam** se este arquivo não existir.

Para cada métrica da análise:

1. **Decidir o papel** no briefing: `destaque-tldr` (vai pros 4 KPIs principais da §3) **ou** `detalhe-scorecard` (vai pros 8-10 da §4). Não pode ser ambos
2. **Verificar se o usuário já definiu o indicador** em BRIEFING.md ou em mensagem. Se sim, transcrever
3. **Caso contrário, conduzir entrevista** com 6 perguntas:
   - Nome e definição (o que mede em uma frase)
   - Unidade e granularidade
   - Fonte (`<MCP/stack>` · tabela/entidade)
   - Fórmula calculável (SQL, Python, ou regra agregada — texto narrativo **não** vale)
   - Comparativos (MoM, YoY, vs Meta, vs Benchmark, vs Baseline)
   - Benchmark + faixas de leitura (verde/amarelo/vermelho) + contexto de negócio + fatores externos + limitações
4. **Salvar em `docs/INDICADORES.md`** usando [templates/indicadores.tmpl.md](templates/indicadores.tmpl.md) como base
5. **Validar quotas duras**:
   - Exatamente 4 métricas marcadas `destaque-tldr`
   - Entre 6 e 12 métricas no total
   - Métricas `destaque-tldr` NÃO podem coincidir com as 4 primeiras do scorecard

### Fase 5 — Modelagem dos Blocos de Análise

Cada bloco responde **uma** pergunta. Quantos blocos? Quota da audiência (Fase 2).

Para cada bloco:

1. **Definir a pergunta** específica (uma frase)
2. **Escolher o tipo de gráfico canônico** — 1 dos 12. Consulta direta a [grafico-por-bloco.md](references/grafico-por-bloco.md). A escolha é função da pergunta, não do dataset
3. **Mapear métricas usadas** (referência ao §6 Indicadores do plano)
4. **Declarar a hipótese de leitura** (o que esperamos ver no gráfico)
5. **Estruturar a instrução para o data-scientist**:
   - Query/extração: descrição calculável
   - Comparativos a calcular
   - Validações específicas (nulls esperados, gaps, outliers)
6. **Antecipar cortes investigativos** se anomalia (por canal, região, assessor) — fixados antes para não improvisar depois

**Consulta opcional a `analysis-patterns.md`**: se a pergunta única se encaixa em 1 dos 7 padrões pré-montados (Captação Líquida, Pipeline Funnel, Performance Comercial, Customer Concentration, Trend Analysis, KPI Dashboard, Cross-Source Join), abrir o arquivo e reusar a estrutura. Caso contrário, ignorar — não force.

### Fase 6 — Findings + Recomendações candidatas (hipóteses)

Hipóteses do que vamos encontrar. **Hipóteses, não fatos** — o data-scientist confirma ou refuta na extração.

**Findings esperados** (quota: ver Fase 2):

Para cada F-N:
- ID (`F-01`, `F-02`, ...)
- Hipótese (uma frase com a conclusão hipotética)
- **Hipótese de IMPACTO** (o "e daí?" — o que muda na decisão se confirmado). **Bloqueio se vazio.**
- Evidência esperada (referência ao bloco e subseção)

**Recomendações candidatas** (quota: ver Fase 2):

Para cada R-N:
- ID (`R-01`, `R-02`, ...)
- Ação imperativa em uma frase
- **Dono provável** (cargo ou nome). **Bloqueio se vazio** — sem dono é desejo, não recomendação
- Prazo provável
- Finding de origem (`Decorre de F-01`)
- ICE estimado = (Impacto 1-10 × Confiança 1-10) ÷ Esforço 1-10. Priorizar ≥ 6

### Fase 7 — Gerar `PLANO-ANALISE.md` + Validar

1. **Preencher o template** [templates/plano-analise.tmpl.md](templates/plano-analise.tmpl.md) com tudo coletado nas Fases 1-6
2. **Executar o checklist de conclusão** (último bloco do template). Itens duros:
   - §1 Identificação completa
   - §2 Pergunta única em uma frase
   - §3 Quotas da matriz aplicadas
   - §5 Timeliness preenchido para cada fonte
   - §6 Exatamente 4 `destaque-tldr`, 6-12 total, sem overlap
   - `docs/INDICADORES.md` existe e cobre todas as métricas
   - §7 Cada bloco tem tipo de gráfico canônico
   - §8 Cada finding tem hipótese de IMPACTO
   - §9 Cada recomendação tem dono + prazo + ICE
3. **Se algum item falhar**: voltar à fase correspondente, corrigir, revalidar

### Fase 8 — Estrutura de Pastas (path absoluto)

Confirmar o **diretório de trabalho absoluto** (não relativo — `./analise/` é ambíguo).

Criar:

```
{{diretorio_absoluto}}/
├── PLANO-ANALISE.md           # Gerado na Fase 7
├── docs/
│   ├── BRIEFING.md            # Já existe se veio do initializing-analysis
│   ├── SCHEMA.md              # Schemas das fontes (se discovery foi feito)
│   └── INDICADORES.md         # Gerado na Fase 4 — OBRIGATÓRIO
├── data/
│   └── extractions/           # Vazio — será preenchido pelo data-scientist
├── src/                        # Vazio — scripts Python auxiliares
└── output/
    ├── data-scientist/         # Outputs da extração
    └── ANL-{{AREA}}-{{NNN}}-briefing.md  # Output final (gerado por generating-executive-reports)
```

Se `DATA-PROFILE.md` existir, linkar no §5 Fontes do plano.

## Validação Pré-Geração (gate da Fase 7)

```
CHECKLIST DURO — PLANO-ANALISE.md
─────────────────────────────────
[ ] §1: CODIGO_DOCUMENTO no formato ANL-{ÁREA}-{NNN}
[ ] §1: Elaborador, Revisor e Aprovador definidos
[ ] §2: Pergunta única em UMA frase (não 2, não 3)
[ ] §3: Audiência definida; 9 quotas extraídas da matriz
[ ] §4: Período principal + comparativo; sazonalidade declarada
[ ] §5: Todas as fontes com timeliness e contribuição esperada
[ ] §6: Exatamente 4 destaque-tldr · 6-12 total · sem overlap
[ ] docs/INDICADORES.md existe e tem entrada para todas as métricas
[ ] §7: Cada bloco com pergunta + tipo de gráfico canônico + instrução
[ ] §8: Cada finding com hipótese de IMPACTO ("e daí?")
[ ] §9: Cada recomendação com dono + prazo + ICE estimado
[ ] §10: Instruções para ambos agentes preenchidas
[ ] Diretório de trabalho como path ABSOLUTO
```

## Diretório de Trabalho

**Sempre path absoluto.** Exemplos válidos:

- `/Users/bchiaramonti/Documents/brain/2-areas/m7/sandbox/data-science/2026-03-04_captacao/`
- `~/projetos/anl-com-001-captacao-q1/` *(o `~` é resolvido pelo shell — não confiar dentro do plano)*

Exemplos **inválidos** (rejeitar):

- `./analise/` — ambíguo (relativo a quê?)
- `analise-q1` — sem path completo

## Anti-Patterns

- ❌ NUNCA gerar plano sem código documental `ANL-{ÁREA}-{NNN}` definido
- ❌ NUNCA aceitar pergunta com mais de uma frase — refinar antes
- ❌ NUNCA exceder as quotas da matriz `audiencia-profundidade.md`
- ❌ NUNCA tratar `docs/INDICADORES.md` como opcional — os agentes downstream abortam sem ele
- ❌ NUNCA permitir que uma métrica seja `destaque-tldr` e simultaneamente entre os 4 primeiros do scorecard
- ❌ NUNCA aceitar bloco de análise sem tipo de gráfico canônico declarado
- ❌ NUNCA aceitar finding sem hipótese de IMPACTO ("e daí?")
- ❌ NUNCA aceitar recomendação sem dono e prazo
- ❌ NUNCA usar path relativo para o diretório de trabalho
- ❌ NUNCA pular a entrevista de indicadores quando o usuário não forneceu definição estruturada
- ❌ NUNCA inventar fontes ou MCPs que o usuário não confirmou ter acesso
