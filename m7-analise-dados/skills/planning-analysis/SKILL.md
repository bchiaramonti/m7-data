---
name: planning-analysis
description: >-
  Planeja análises de dados mapeando objetivos, audiência, fontes de dados (Bitrix24/ClickHouse),
  métricas e estrutura do relatório. Produz PLANO-ANALISE.md que orquestra o pipeline
  data-scientist → executive-communicator.
  Use when the user asks for data analysis, needs a report, mentions business intelligence,
  or wants to plan before executing. Also use when the user provides a business question
  that requires data to answer.

  <example>
  Context: User wants to analyze sales performance
  user: "Preciso analisar a performance de vendas do último trimestre"
  assistant: Planeja a análise mapeando fontes Bitrix24 e ClickHouse, define métricas e gera PLANO-ANALISE.md
  </example>

  <example>
  Context: User wants a recurring report
  user: "Quero montar um relatório mensal de captação para a diretoria"
  assistant: Planeja com audiência Diretoria, métricas de captação, comparativos MoM/YoY
  </example>
user-invocable: true
---

# Planning Analysis — Planejamento de Análises de Dados

> "Nenhuma análise começa sem um plano. O plano define o que perguntar, onde buscar e para quem entregar."

Esta skill planeja análises de dados de ponta a ponta, produzindo um `PLANO-ANALISE.md` que serve como contrato entre os agentes `data-scientist` e `executive-communicator`.

## Dependências Internas

- [references/analysis-patterns.md](references/analysis-patterns.md) — 7 padrões de análise pré-montados
- Skill `exploring-data-sources` — se DATA-PROFILE.md existir, reutilizar
- Catálogo de fontes em `exploring-data-sources/references/data-source-catalog.md`

## Pré-requisitos

- MCP `clickhouse-m7bronze` e/ou `bitrix24` acessíveis
- Conhecimento do escopo da análise (obtido na Fase 1)

## Workflow

### Fase 1 — Entender o Pedido

Coletar via conversa com o usuário:

| Dimensão | Pergunta | Obrigatório |
|----------|----------|-------------|
| **Objetivo** | O que queremos descobrir/responder? | Sim |
| **Audiência** | Quem consumirá o resultado? (Diretoria/Gerentes/Técnico/Comercial) | Sim |
| **Contexto** | Reunião mensal? Ad-hoc? Crise? Planejamento? | Sim |
| **Período** | Intervalo temporal dos dados | Sim |
| **Urgência** | Para quando? | Não |
| **Precedentes** | Já existe análise similar? DATA-PROFILE.md? | Não |

Se o usuário não especificar audiência, perguntar explicitamente — a audiência define a profundidade e linguagem do relatório.

### Fase 2 — Mapear Fontes de Dados

**Se DATA-PROFILE.md existir** no diretório de trabalho:
- Reutilizar schemas e recomendações do perfil existente
- Verificar se cobre o período e métricas necessárias

**Se DATA-PROFILE.md NÃO existir**:
1. Consultar catálogo de fontes (`data-source-catalog.md`)
2. Explorar schemas via MCP discovery:
   - ClickHouse: `clickhouse_list_tables` + `clickhouse_describe_table`
   - Bitrix24: consultar ferramentas disponíveis por domínio
3. Documentar schemas relevantes

**Decisão de fonte** — usar a Matriz de Decisão do catálogo:
- Dados históricos/agregados → ClickHouse
- Dados operacionais/pipeline → Bitrix24
- Cruzamento → ambos com join em Python (Padrão #7)

### Fase 3 — Definir Métricas e Indicadores

**Passo 1 — Verificar se o usuário já definiu o indicador:**

- Se BRIEFING.md ou mensagem do usuário contiver YAML ou definição estruturada → usar diretamente
- Se não → conduzir entrevista colaborativa com as seguintes perguntas:
  1. **Nome e definição**: Qual o nome do indicador e o que ele mede?
  2. **Fonte de dados**: Qual tabela do ClickHouse ou entidade do Bitrix24?
  3. **Fórmula / lógica de cálculo**: Como é calculado? (ex: `SUM(entradas) - SUM(saidas)`)
  4. **Comparativos**: Quais referências importam? (YoY, MoM, vs meta, vs benchmark)
  5. **Contexto de negócio**: Faixa esperada? Sazonalidade? Fatores externos relevantes?

Salvar a definição em `docs/INDICADORES.md` no diretório de trabalho usando o formato:

```markdown
## [Nome do Indicador]
- **Definição**: ...
- **Fonte**: ClickHouse tabela X / Bitrix24 entidade Y
- **Fórmula**: SUM(col_a) - SUM(col_b)
- **Comparativos**: MoM, vs meta R$Xm
- **Contexto**: faixa esperada, sazonalidade, fatores externos
```

**Passo 2 — Definir métricas ad-hoc adicionais:**

Para cada métrica necessária além do indicador principal, definir:

| Campo | Exemplo |
|-------|---------|
| **Nome** | Captação líquida |
| **Definição** | Soma de entradas menos soma de saídas no período |
| **Fórmula** | `SUM(entradas) - SUM(saidas)` |
| **Fonte** | ClickHouse: `clickhouse_query(SELECT ...)` |
| **Comparativo** | YoY, MoM, vs meta de R$ 200M |
| **Granularidade** | Mensal |

Consultar `analysis-patterns.md` para métricas pré-definidas por tipo de análise.

### Fase 4 — Estruturar o Relatório

Definir a estrutura do relatório final:

1. **Blocos temáticos** — agrupar métricas em 2-4 blocos narrativos
2. **Narrativa central** — qual história os dados devem contar
3. **Tom** — Otimista / Cauteloso / Neutro / Alarmante
4. **Formato** — Relatório Executivo / Status Update / Talking Points / Briefing
5. **Limite de páginas** — baseado na audiência (ver framework no agent `executive-communicator`)

### Fase 5 — Gerar PLANO-ANALISE.md

Usar o template em [templates/plano-analise.tmpl.md](templates/plano-analise.tmpl.md) para gerar o plano completo no diretório de trabalho.

O plano DEVE incluir:
- Instruções específicas para cada agente
- Critérios de conclusão mensuráveis
- Diretório de trabalho definido

### Fase 6 — Criar Estrutura de Pastas

Criar no diretório de trabalho definido:

```
<diretorio-de-trabalho>/
├── PLANO-ANALISE.md          # Gerado nesta fase
├── docs/
│   ├── SCHEMA.md              # Schemas das fontes MCP relevantes (se novo)
│   └── INDICADORES.md         # Definições das métricas (preenchido nesta fase)
├── data/
│   └── extractions/           # Vazio — será preenchido pelo data-scientist
├── src/                       # Vazio — scripts Python se necessário
└── output/
    └── data-scientist/        # Vazio — outputs do agente
```

Se DATA-PROFILE.md existir, linkar no plano.

## Diretório de Trabalho

O diretório onde a análise será executada é **configurável**:

- **Default**: Diretório atual do Claude Code
- **Personalizado**: Qualquer caminho especificado pelo usuário
- Exemplos: `./analise-captacao-q1/`, `~/Documents/brain/2-areas/m7/sandbox/data-science/2026-03-04_captacao/`

Definir no campo `Diretório de trabalho` do PLANO-ANALISE.md.

## Validação Pré-Geração

Antes de gerar o plano, verificar:

- [ ] Objetivo claramente definido (não vago)
- [ ] Audiência identificada e nível de detalhe calibrado
- [ ] Todas as métricas mapeadas a pelo menos uma fonte MCP
- [ ] Pelo menos um comparativo definido por métrica
- [ ] Blocos temáticos fazem sentido para a audiência
- [ ] Período de análise explícito (data início e fim)
- [ ] Diretório de trabalho definido
- [ ] Formato de output definido (Relatório/Status/Talking Points/Briefing)
- [ ] `docs/INDICADORES.md` preenchido com definição completa para cada métrica

## Anti-Patterns

- ❌ NUNCA gerar plano sem confirmar audiência com o usuário
- ❌ NUNCA mapear métricas sem verificar que a fonte MCP tem os dados
- ❌ NUNCA incluir mais de 4 blocos temáticos para Diretoria (overload)
- ❌ NUNCA pular a definição de comparativos — números sem referência não comunicam
- ❌ NUNCA gerar PLANO-ANALISE.md sem critérios de conclusão
- ❌ NUNCA assumir que o usuário conhece os dados — perguntar se DATA-PROFILE.md existe
- ❌ NUNCA pular a entrevista de definição de indicadores se o usuário não forneceu definição
