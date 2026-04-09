---
name: exploring-data-sources
description: >-
  Explora fontes de dados disponíveis (Bitrix24 CRM + ClickHouse warehouse) e executa
  Análise Exploratória de Dados (EDA). Produz DATA-PROFILE.md com inventário de schemas,
  estatísticas descritivas, distribuições, outliers, correlações e hipóteses iniciais.
  Use when the user wants to discover available data, profile tables, understand the CRM
  structure, or perform exploratory data analysis before planning a formal analysis.

  <example>
  Context: User is starting a new analysis project
  user: "Que dados temos disponíveis sobre captação no ClickHouse?"
  assistant: Explora tabelas do ClickHouse, perfila as relevantes e gera DATA-PROFILE.md
  </example>

  <example>
  Context: User wants to understand CRM data
  user: "Me mostra como estão os dados de deals no Bitrix24"
  assistant: Lista deals, perfila campos e faz EDA com estatísticas e distribuições
  </example>
user-invocable: true
---

# Exploring Data Sources — Discovery + EDA

> "Antes de perguntar, entenda o que existe. Antes de planejar, explore os dados."

Esta skill combina **discovery de schemas** com **Análise Exploratória de Dados (EDA)** para gerar um perfil completo das fontes disponíveis. O output é um `DATA-PROFILE.md` reutilizável pela skill `planning-analysis`.

## Dependências Internas

- [references/data-source-catalog.md](references/data-source-catalog.md) — Catálogo completo das ferramentas MCP
- Agent `data-scientist` — Invocado na Fase 2 para EDA computacional

## Pré-requisitos

- MCP `clickhouse-m7bronze` e/ou `bitrix24` devem estar configurados e acessíveis
- Verificar conectividade:
  - ClickHouse: `clickhouse_list_databases`
  - Bitrix24: `bitrix24_validate_webhook`

## Workflow

### Fase 0 — Descobrir (Discovery)

Mapear o que está disponível em cada fonte:

**ClickHouse:**
1. `clickhouse_list_databases` → listar databases
2. `clickhouse_list_tables(database: "M7Bronze")` → listar tabelas
3. Para cada tabela relevante:
   - `clickhouse_describe_table` → schema (colunas, tipos)
   - `clickhouse_get_table_stats` → volume (linhas, período)

**Bitrix24:**
1. Identificar entidades relevantes (Deals, Leads, Contacts, Companies)
2. Para cada entidade:
   - Listar campos disponíveis (via `get_latest_*` com 1 registro)
   - Contar registros totais
   - Verificar pipelines e estágios: `get_deal_pipelines`, `get_deal_stages`

**Output Fase 0:** Lista de tabelas/entidades com schema e volume.

### Fase 1 — Perfilar (Profiling)

Para cada fonte relevante:

1. **Amostras**: `clickhouse_get_table_sample(limit: 5)` ou `get_latest_*`
2. **Cardinalidade**: Quantos valores únicos por campo categórico
3. **Tipos de dados**: Confirmar tipos reais vs esperados
4. **Período coberto**: Primeiro e último registro com data

**Output Fase 1:** Amostras e metadados por fonte.

### Fase 2 — EDA (Análise Exploratória)

Invocar o agente `data-scientist` para executar análise computacional:

#### Estatísticas Descritivas
Para variáveis numéricas relevantes:
- Média, mediana, desvio padrão
- Min, max, percentis (P25, P50, P75)
- Coeficiente de variação (CV = σ/μ)

#### Distribuições
- Frequências de campos categóricos (ex: deals por pipeline, leads por status)
- Histogramas textuais para variáveis numéricas (faixas de valor)
- Top N valores mais frequentes

#### Valores Ausentes
- Percentual de nulls por coluna
- Padrão de ausência (aleatório ou sistemático?)
- Colunas com >50% nulls (candidatas a exclusão)

#### Outliers
- Valores > 3σ da média (z-score)
- Para valores monetários: extremos que distorcem médias
- Listar os outliers identificados com contexto

#### Correlações
- Matriz de correlação entre variáveis numéricas
- Destacar correlações |r| > 0.7 (forte)
- Correlações negativas relevantes

#### Cobertura Temporal
- Primeiro e último registro por fonte
- Gaps temporais (meses/semanas sem dados)
- Sazonalidade aparente (variação mensal)

#### Cardinalidade de Categóricos
- Número de assessores únicos
- Número de pipelines/estágios
- Número de clientes/empresas
- Distribuição por categoria principal

### Fase 3 — Documentar (DATA-PROFILE.md)

Gerar `DATA-PROFILE.md` no diretório de trabalho consolidando todas as fases:

```markdown
# Data Profile: [Escopo da Exploração]

> **Gerado em**: YYYY-MM-DD
> **Fontes exploradas**: [ClickHouse M7Bronze / Bitrix24 / Ambos]

---

## Inventário de Fontes

### ClickHouse — M7Bronze

| Tabela | Colunas | Linhas | Período | Relevância |
|--------|---------|--------|---------|------------|
| [nome] | N | N | YYYY-MM a YYYY-MM | [alta/média/baixa] |

### Bitrix24 — CRM

| Entidade | Campos | Registros | Última Atualização | Relevância |
|----------|--------|-----------|-------------------|------------|
| [nome] | N | N | YYYY-MM-DD | [alta/média/baixa] |

---

## Amostras de Dados

### [Fonte/Tabela 1]
[5 primeiros registros em tabela markdown]

---

## Análise Exploratória (EDA)

### Estatísticas Descritivas

| Variável | Média | Mediana | Desvio | Min | Max | P25 | P75 |
|----------|-------|---------|--------|-----|-----|-----|-----|
| [nome]   | X     | X       | X      | X   | X   | X   | X   |

### Distribuições

#### [Campo categórico]
| Valor | Contagem | % |
|-------|----------|---|
| [val] | N | X% |

### Valores Ausentes

| Coluna | % Nulls | Padrão |
|--------|---------|--------|
| [nome] | X% | [aleatório/sistemático] |

### Outliers Detectados

| Fonte | Campo | Valor | Z-Score | Contexto |
|-------|-------|-------|---------|----------|
| [tabela] | [col] | [val] | X.X | [obs] |

### Correlações Significativas (|r| > 0.7)

| Var A | Var B | r | Direção |
|-------|-------|---|---------|
| [nome] | [nome] | 0.XX | [positiva/negativa] |

### Cobertura Temporal

| Fonte | Primeiro Registro | Último Registro | Gaps |
|-------|-------------------|-----------------|------|
| [nome] | YYYY-MM-DD | YYYY-MM-DD | [sim/não — detalhar] |

---

## Campos-Chave para Cross-Source Join

| Campo | ClickHouse | Bitrix24 | Tipo |
|-------|------------|----------|------|
| [nome] | [coluna] | [campo] | [tipo] |

---

## Hipóteses Iniciais

Observações numéricas que merecem investigação aprofundada:

1. [Observação factual + dado numérico que a suporta]
2. [Observação factual + dado numérico que a suporta]

---

## Recomendações de Uso

- Para análise de [domínio], usar [tabela X] + [entidade Y]
- Campo [Z] é o melhor candidato para join entre fontes
- Tabela [W] tem gaps temporais — considerar filtrar período [A] a [B]
```

## Validação

- [ ] Todas as fontes solicitadas foram exploradas
- [ ] Schemas documentados com tipos corretos
- [ ] EDA executada com estatísticas descritivas, distribuições, outliers e correlações
- [ ] Amostras incluídas para cada fonte relevante
- [ ] Campos de join identificados entre fontes
- [ ] Hipóteses são factuais (baseadas em dados), não interpretativas
- [ ] DATA-PROFILE.md gerado e salvo no diretório de trabalho

## Anti-Patterns

- ❌ NUNCA explorar todas as tabelas do database — focar nas relevantes ao escopo
- ❌ NUNCA gerar conclusões de negócio na exploração — isso é do executive-communicator
- ❌ NUNCA modificar dados durante a exploração — apenas leitura
- ❌ NUNCA pular a fase de EDA — discovery sem profiling é catálogo, não exploração
