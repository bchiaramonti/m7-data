# m7-analise-dados

Plugin Claude Code para análise de dados e geração de relatórios executivos da M7 Investimentos.

## O que faz

Conecta dados do **Bitrix24** (CRM) e **ClickHouse** (data warehouse) para produzir análises e relatórios executivos adaptados ao público-alvo.

## Pipeline

```
Explorar dados → Planejar análise → Extrair → Analisar → Interpretar → Relatório
     │                  │                        │                          │
exploring-       planning-              data-scientist            executive-
data-sources     analysis               (agent)                  communicator
(skill)          (skill)                                         (agent)
                                                                      │
                                                          generating-executive-
                                                          reports (skill)
```

## Indicadores por Projeto

Cada análise define suas próprias métricas em `docs/INDICADORES.md`, criado durante a Fase 2 (Planejamento). A `planning-analysis` conduz uma entrevista colaborativa para definir nome, fórmula, fonte de dados, comparativos e contexto de negócio de cada métrica — ou aceita uma definição estruturada fornecida diretamente pelo usuário.

Formato de cada métrica em `docs/INDICADORES.md`:

```markdown
## [Nome do Indicador]
- **Definição**: ...
- **Fonte**: ClickHouse tabela X / Bitrix24 entidade Y
- **Fórmula**: SUM(col_a) - SUM(col_b)
- **Comparativos**: MoM, vs meta R$Xm
- **Contexto**: faixa esperada, sazonalidade, fatores externos
```

## Componentes

### Skills (3)

| Skill | Trigger | Output |
|-------|---------|--------|
| `exploring-data-sources` | Explorar dados disponíveis, EDA | `DATA-PROFILE.md` |
| `planning-analysis` | Planejar análise de dados + definir métricas | `PLANO-ANALISE.md`, `docs/INDICADORES.md` |
| `generating-executive-reports` | Executar pipeline e gerar relatório | `relatorio-<nome>.md` |

### Agents (2)

| Agent | Papel | Tools |
|-------|-------|-------|
| `data-scientist` | Extrair, analisar, validar dados | Read, Write, Edit, Bash, Grep, Glob |
| `executive-communicator` | Interpretar dados, gerar relatórios | Read, Write, Grep, Glob |

### MCP Servers (2)

| MCP | Fonte | Tools |
|-----|-------|-------|
| `clickhouse-m7bronze` | Data warehouse (read-only) | 6 ferramentas |
| `bitrix24` | CRM operacional | 48 ferramentas |

## Princípio Fundamental

> "Quem gera dados NÃO conclui. Quem conclui NÃO gera dados."

O `data-scientist` extrai e analisa — nunca interpreta. O `executive-communicator` interpreta e escreve — nunca gera dados. Essa separação é enforced pelas ferramentas disponíveis para cada agente.

## 4 Audiências

Os relatórios se adaptam a 4 perfis:

| Audiência | Páginas | Foco |
|-----------|---------|------|
| Diretoria / C-Level | 1-2 | Impacto, ROI, decisões |
| Gerentes / Sponsors | 2-3 | Progresso, riscos, ações |
| Técnico / Equipe | 3-5 | Metodologia, dados, tasks |
| Comercial / Assessores | 2-3 | Rankings, metas, oportunidades |

## Quick Start

```bash
# Explorar dados disponíveis
/m7-analise-dados:exploring-data-sources

# Planejar uma análise (inclui definição colaborativa de indicadores)
/m7-analise-dados:planning-analysis

# Executar e gerar relatório
/m7-analise-dados:generating-executive-reports
```

## Pré-requisitos

- MCPs Bitrix24 e ClickHouse configurados e acessíveis
- Credenciais em `.claude/credentials/.env`:
  - `BITRIX24_WEBHOOK_URL`
  - `CLICKHOUSE_HOST`, `CLICKHOUSE_PORT`, `CLICKHOUSE_USER`, `CLICKHOUSE_PASSWORD`
- Python 3.9+ com `pandas` (para cross-source joins e transformações)
