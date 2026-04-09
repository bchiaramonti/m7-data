# Catálogo de Fontes de Dados

Referência completa das fontes disponíveis via MCP para análise de dados M7.

---

## ClickHouse — Data Warehouse M7Bronze

**Tipo**: Data warehouse analítico, read-only
**Acesso**: MCP `clickhouse-m7bronze` (6 ferramentas)

### Ferramentas de Discovery

| Ferramenta | Input | Output |
|------------|-------|--------|
| `clickhouse_list_databases` | — | Lista de databases |
| `clickhouse_list_tables` | `database` | Lista de tabelas |
| `clickhouse_describe_table` | `database`, `table` | Schema (colunas, tipos) |
| `clickhouse_get_table_sample` | `database`, `table`, `limit` | Primeiros N registros |
| `clickhouse_get_table_stats` | `database`, `table` | Contagem, min/max datas |

### Ferramenta de Query

| Ferramenta | Input | Restrições |
|------------|-------|------------|
| `clickhouse_query` | `query` (SQL) | Apenas SELECT/WITH. LIMIT auto 1000. |

### Padrões SQL Úteis

**Série temporal mensal:**
```sql
SELECT
  toStartOfMonth(data) AS mes,
  sum(valor) AS total,
  count() AS operacoes
FROM M7Bronze.tabela
WHERE data BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY mes
ORDER BY mes
```

**YoY (Year-over-Year):**
```sql
SELECT
  toYear(data) AS ano,
  toMonth(data) AS mes,
  sum(valor) AS total
FROM M7Bronze.tabela
WHERE toYear(data) IN (2024, 2025)
GROUP BY ano, mes
ORDER BY mes, ano
```

**Top N com percentual:**
```sql
SELECT
  campo,
  sum(valor) AS total,
  round(total / (SELECT sum(valor) FROM M7Bronze.tabela) * 100, 1) AS pct
FROM M7Bronze.tabela
GROUP BY campo
ORDER BY total DESC
LIMIT 10
```

---

## Bitrix24 — CRM Operacional

**Tipo**: CRM com 48 ferramentas MCP
**Acesso**: MCP `bitrix24` (webhook auth)

### Domínio: Deals (Negócios)

| Ferramenta | Descrição | Filtros |
|------------|-----------|---------|
| `bitrix24_list_deals` | Lista paginada de deals | — |
| `bitrix24_get_deal` | Deal individual por ID | ID |
| `bitrix24_get_latest_deals` | Deals mais recentes | — |
| `bitrix24_get_deals_from_date_range` | Deals por período | data início/fim |
| `bitrix24_get_deals_with_user_names` | Deals com nomes dos responsáveis | — |
| `bitrix24_filter_deals_by_pipeline` | Deals por pipeline | pipeline ID |
| `bitrix24_filter_deals_by_budget` | Deals por faixa de valor | min/max |
| `bitrix24_filter_deals_by_status` | Deals por status | status ID |

### Domínio: Leads

| Ferramenta | Descrição |
|------------|-----------|
| `bitrix24_list_leads` | Lista paginada |
| `bitrix24_get_lead` | Lead por ID |
| `bitrix24_get_latest_leads` | Leads recentes |
| `bitrix24_get_leads_from_date_range` | Leads por período |
| `bitrix24_get_leads_with_user_names` | Leads com nomes |

### Domínio: Contacts & Companies

| Ferramenta | Descrição |
|------------|-----------|
| `bitrix24_list_contacts` / `list_companies` | Lista paginada |
| `bitrix24_get_contact` / `get_company` | Individual por ID |
| `bitrix24_get_latest_contacts` / `get_latest_companies` | Mais recentes |
| `bitrix24_get_contacts_with_user_names` / `get_companies_with_user_names` | Com nomes |
| `bitrix24_get_companies_from_date_range` | Empresas por período |

### Domínio: Analytics & Performance

| Ferramenta | Descrição | Uso Típico |
|------------|-----------|------------|
| `bitrix24_generate_sales_report` | Relatório de vendas consolidado | Resumo periódico |
| `bitrix24_get_team_dashboard` | Dashboard da equipe | Visão geral operacional |
| `bitrix24_analyze_account_performance` | Performance por conta | Análise de clientes |
| `bitrix24_analyze_customer_engagement` | Engajamento de clientes | Retenção e atividade |
| `bitrix24_forecast_performance` | Forecast de performance | Projeções |
| `bitrix24_track_deal_progression` | Progressão no pipeline | Funil de vendas |
| `bitrix24_compare_user_performance` | Comparação entre usuários | Rankings |
| `bitrix24_get_user_performance_summary` | Resumo individual | Avaliação de assessor |
| `bitrix24_monitor_sales_activities` | Atividades de vendas | Volume operacional |
| `bitrix24_monitor_user_activities` | Atividades por usuário | Produtividade |

### Domínio: Pipeline & Infraestrutura

| Ferramenta | Descrição |
|------------|-----------|
| `bitrix24_get_deal_pipelines` | Listar pipelines configurados |
| `bitrix24_get_deal_stages` | Listar estágios de cada pipeline |
| `bitrix24_get_all_users` | Todos os usuários do CRM |
| `bitrix24_get_user` | Usuário por ID |
| `bitrix24_resolve_user_names` | Resolver IDs para nomes |
| `bitrix24_search_crm` | Busca full-text no CRM |

### Domínio: Diagnóstico

| Ferramenta | Descrição |
|------------|-----------|
| `bitrix24_validate_webhook` | Testar conectividade |
| `bitrix24_check_crm_settings` | Configurações do CRM |
| `bitrix24_diagnose_permissions` | Verificar permissões |
| `bitrix24_test_leads_api` | Testar API de leads |

---

## Matriz de Decisão: Quando Usar Qual Fonte

| Cenário de Análise | Fonte Primária | Fonte Secundária | Razão |
|---------------------|----------------|------------------|-------|
| **Captação líquida mensal** | ClickHouse | Bitrix24 (deals) | Warehouse tem séries históricas otimizadas |
| **Pipeline atual** | Bitrix24 | — | CRM tem dados operacionais em tempo real |
| **Performance por assessor** | Bitrix24 | ClickHouse (histórico) | CRM tem tools dedicadas de performance |
| **Tendência YoY/MoM** | ClickHouse | — | SQL analítico com grandes volumes |
| **Concentração de clientes** | ClickHouse | Bitrix24 (accounts) | Cálculo de concentração em warehouse |
| **Forecast** | Bitrix24 | ClickHouse (baseline) | CRM tem ferramenta de forecast |
| **Funil de conversão** | Bitrix24 | — | Pipeline e stages são CRM |
| **Comparação de equipes** | Bitrix24 | — | Tools de comparação de usuários |
| **Análise ad-hoc com SQL** | ClickHouse | — | Flexibilidade do SQL SELECT |

---

## Campos-Chave para Cross-Source Join

Quando dados precisam ser cruzados entre ClickHouse e Bitrix24:

| Campo | ClickHouse | Bitrix24 | Tipo |
|-------|------------|----------|------|
| Código do assessor | `cod_assessor` (varia por tabela) | User ID / `ASSIGNED_BY_ID` | int |
| Data | `data` / `date` (varia) | `DATE_CREATE` / `DATE_MODIFY` | date |
| Código do cliente | `cod_cliente` (varia) | Contact ID / Company ID | int |
| Pipeline | — | `CATEGORY_ID` | int |
| Valor do deal | — | `OPPORTUNITY` | float |

**Processo de join:**
1. Extrair dados de cada fonte separadamente
2. Identificar campo-chave comum
3. Em Python: `pd.merge(df_clickhouse, df_bitrix, on='campo_chave', how='left')`
4. Tratar mismatches (chaves faltantes, tipos diferentes)

---

## Troubleshooting MCP

### ClickHouse não responde

1. Verificar se o servidor está acessível: `nc -zv 172.17.0.14 8123`
2. Verificar credenciais em `.claude/credentials/.env` (`CLICKHOUSE_HOST`, `CLICKHOUSE_PORT`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`)
3. Verificar se o MCP está buildado: `ls 3-resources/mcp/clickhouse-m7bronze-mcp/dist/index.js`
4. Reiniciar o MCP: fechar e reabrir a sessão Claude Code

### Bitrix24 não responde

1. Verificar `BITRIX24_WEBHOOK_URL` em `.claude/credentials/.env`
2. Testar webhook: `bitrix24_validate_webhook`
3. Verificar permissões: `bitrix24_diagnose_permissions`
4. Verificar se o MCP está buildado: `ls 3-resources/mcp/bitrix24-mcp-server/build/index.js`

### Query ClickHouse rejeitada

- Apenas `SELECT` e `WITH` são permitidos — DDL/DML bloqueados
- Queries sem `LIMIT` recebem `LIMIT 1000` automaticamente
- Verificar se não há DDL/DML acidental na query (INSERT, UPDATE, DELETE, DROP, ALTER)
