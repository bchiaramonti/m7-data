# Padrões de Análise Pré-Montados

7 padrões recorrentes de análise com estratégia de extração, fontes MCP e métricas típicas.

---

## Padrão 1: Captação Líquida

**Objetivo**: Medir o fluxo líquido de recursos (entradas - saídas) em períodos definidos.

**Fontes**:
- **Primária**: ClickHouse — séries temporais de movimentação
- **Secundária**: Bitrix24 — deals associados à captação

**Métricas típicas**:
| Métrica | Fórmula | Comparativo |
|---------|---------|-------------|
| Captação bruta | Σ entradas no período | MoM, YoY |
| Resgates | Σ saídas no período | MoM, YoY |
| Captação líquida | Bruta - Resgates | vs meta, MoM, YoY |
| Taxa de retenção | 1 - (Resgates / AuC inicial) | YoY |

**Estratégia de extração**:
1. ClickHouse: query temporal com `toStartOfMonth(data)` agrupando entradas e saídas
2. Bitrix24: `get_deals_from_date_range` para deals de captação
3. Cross-source: join por `cod_assessor` + `mês` se necessário

**Granularidade sugerida**: Mensal (padrão), diária (se análise de campanha)

---

## Padrão 2: Pipeline Funnel

**Objetivo**: Analisar a conversão de leads/deals através dos estágios do pipeline.

**Fontes**:
- **Primária**: Bitrix24 — pipelines, stages, deals
- **Secundária**: — (geralmente não precisa de ClickHouse)

**Métricas típicas**:
| Métrica | Fórmula | Comparativo |
|---------|---------|-------------|
| Deals por estágio | COUNT por stage_id | MoM |
| Taxa de conversão | Deals saídos do estágio / Deals entrados | MoM, YoY |
| Tempo médio por estágio | AVG(data_saída - data_entrada) | MoM |
| Valor médio por estágio | AVG(OPPORTUNITY) por stage | vs pipeline |
| Drop-off rate | 1 - taxa de conversão | MoM |

**Estratégia de extração**:
1. `bitrix24_get_deal_pipelines` → listar pipelines
2. `bitrix24_get_deal_stages` → listar estágios de cada pipeline
3. `bitrix24_filter_deals_by_pipeline` → deals por pipeline
4. `bitrix24_track_deal_progression` → progressão detalhada

---

## Padrão 3: Performance Comercial

**Objetivo**: Avaliar e comparar performance de assessores/equipes.

**Fontes**:
- **Primária**: Bitrix24 — tools de performance e atividades
- **Secundária**: ClickHouse — histórico de resultados

**Métricas típicas**:
| Métrica | Fórmula | Comparativo |
|---------|---------|-------------|
| Deals fechados | COUNT por assessor | vs meta, ranking |
| Valor total | SUM(OPPORTUNITY) por assessor | vs meta, ranking |
| Ticket médio | AVG(OPPORTUNITY) por assessor | vs média da equipe |
| Atividades | COUNT atividades por assessor | vs média |
| Conversion rate | Deals Won / Total Deals | vs equipe |

**Estratégia de extração**:
1. `bitrix24_compare_user_performance` → comparação direta
2. `bitrix24_get_user_performance_summary` → resumo individual
3. `bitrix24_get_team_dashboard` → visão da equipe
4. `bitrix24_monitor_user_activities` → volume de atividades
5. ClickHouse (se disponível): histórico mensal por assessor para tendência

---

## Padrão 4: Customer Concentration

**Objetivo**: Medir concentração de AuC/receita nos maiores clientes (risco de concentração).

**Fontes**:
- **Primária**: ClickHouse — dados históricos de AuC por cliente
- **Secundária**: Bitrix24 — accounts e deals por empresa

**Métricas típicas**:
| Métrica | Fórmula | Comparativo |
|---------|---------|-------------|
| % Top 5 | AuC Top 5 / AuC Total | YoY |
| % Top 10 | AuC Top 10 / AuC Total | YoY |
| % Top 20 | AuC Top 20 / AuC Total | YoY |
| HHI (Herfindahl) | Σ(share_i²) | YoY |
| Gini coefficient | Índice de desigualdade | YoY |

**Estratégia de extração**:
1. ClickHouse: query com ranking de clientes por AuC
2. Bitrix24: `bitrix24_analyze_account_performance` para clientes específicos
3. Cross-source: join por `cod_cliente` para enriquecer com dados CRM

---

## Padrão 5: Trend Analysis

**Objetivo**: Identificar tendências temporais em métricas-chave.

**Fontes**:
- **Primária**: ClickHouse — séries temporais com SQL analítico

**Métricas típicas**: Depende do domínio. Aplicável a qualquer métrica quantitativa.

**Padrões SQL úteis**:

**MoM (Month-over-Month):**
```sql
SELECT
  toStartOfMonth(data) AS mes,
  sum(valor) AS total,
  lagInFrame(total) OVER (ORDER BY mes) AS mes_anterior,
  round((total - mes_anterior) / mes_anterior * 100, 1) AS var_pct
FROM M7Bronze.tabela
GROUP BY mes
ORDER BY mes
```

**YoY (Year-over-Year):**
```sql
SELECT
  toMonth(data) AS mes,
  sumIf(valor, toYear(data) = 2025) AS ano_atual,
  sumIf(valor, toYear(data) = 2024) AS ano_anterior,
  round((ano_atual - ano_anterior) / ano_anterior * 100, 1) AS var_yoy
FROM M7Bronze.tabela
WHERE toYear(data) IN (2024, 2025)
GROUP BY mes
ORDER BY mes
```

**Média móvel (3 meses):**
```sql
SELECT
  toStartOfMonth(data) AS mes,
  sum(valor) AS total,
  avg(total) OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS media_movel_3m
FROM M7Bronze.tabela
GROUP BY mes
ORDER BY mes
```

---

## Padrão 6: KPI Dashboard

**Objetivo**: Consolidar KPIs de múltiplas fontes em um painel único.

**Fontes**:
- **Ambas**: ClickHouse (métricas históricas) + Bitrix24 (métricas operacionais)

**Métricas típicas**: Seleção das mais relevantes dos padrões 1-5, mais:
| Métrica | Fonte | Frequência |
|---------|-------|------------|
| AuC total | ClickHouse | Mensal |
| Captação líquida | ClickHouse | Mensal |
| Deals no pipeline | Bitrix24 | Semanal |
| NPS / Satisfação | Bitrix24 | Mensal |
| Headcount | Bitrix24 | Mensal |

**Estratégia**: Extrair cada KPI da fonte mais adequada, consolidar em tabela única.

---

## Padrão 7: Cross-Source Join

**Objetivo**: Combinar dados de ClickHouse e Bitrix24 que não podem ser joinados via MCP.

**Processo**:

```python
import pandas as pd

# 1. Extrair de cada fonte
# (via MCP tools, salvar em arquivos ou variáveis)
df_ch = pd.read_csv('data/extractions/clickhouse_data.csv')
df_bx = pd.read_json('data/extractions/bitrix_data.json')

# 2. Normalizar campo-chave
df_ch['key'] = df_ch['cod_assessor'].astype(int)
df_bx['key'] = df_bx['ASSIGNED_BY_ID'].astype(int)

# 3. Merge
df_merged = pd.merge(
    df_ch, df_bx,
    on='key',
    how='left',  # preservar todos os registros do warehouse
    suffixes=('_ch', '_bx')
)

# 4. Validar
print(f"ClickHouse: {len(df_ch)} linhas")
print(f"Bitrix24: {len(df_bx)} linhas")
print(f"Merged: {len(df_merged)} linhas")
print(f"Sem match: {df_merged['campo_bx'].isna().sum()} linhas")
```

**Campos-chave comuns**:
- `cod_assessor` (CH) ↔ `ASSIGNED_BY_ID` (Bitrix) — ID do assessor
- `data` (CH) ↔ `DATE_CREATE` (Bitrix) — data
- `cod_cliente` (CH) ↔ Contact/Company ID (Bitrix) — cliente

**Cuidados**:
- Tipos devem ser iguais antes do merge (int com int, não int com string)
- Verificar % de match após o join — se muito baixo, o campo-chave pode estar errado
- Dados Bitrix24 podem ter mais registros que ClickHouse (CRM inclui pipeline não convertido)
