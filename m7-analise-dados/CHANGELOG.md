# Changelog — m7-analise-dados

Todas as mudanças notáveis deste plugin serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [2.0.1] - 2026-05-06

### Removed
- `.mcp.json` agora vazio — registros inline de `clickhouse-m7bronze` e `bitrix24` removidos. MCPs do ClickHouse e Bitrix24 passam a ser configurados em **user scope** via `claude mcp add` (preferência operacional do owner), não distribuídos no plugin

### Migration
Após upgrade, configure os MCPs em user scope:
```bash
claude mcp add clickhouse-m7bronze --scope user --transport http \
  --url https://clickhouse.mcp-tunnels-01-4f6d8a.com/mcp \
  --header "Authorization: Bearer <token>"

claude mcp add bitrix24 --scope user --transport http \
  --url https://bitrix24.mcp-tunnels-01-4f6d8a.com/mcp \
  --header "Authorization: Bearer <token>"
```

O plugin continua referenciando ambos os MCPs em skills/agents — apenas a entrega do registro deixa de ser inline.

## [2.0.0] - 2026-03-27

### Breaking Changes
- **Plugin renamed** from `analise-dados-m7` to `m7-analise-dados` — all skill invocations must be updated (e.g., `/analise-dados-m7:planning-analysis` → `/m7-analise-dados:planning-analysis`)
- **`indicators/` library removed** — self-contained indicator YAMLs (comercial/, receita/, clientes/) deleted from the plugin. Indicator definitions now live per-project in `docs/INDICADORES.md`

### Changed
- `planning-analysis`: Fase 3 now accepts user-provided indicator definitions or conducts a 5-question collaborative interview instead of consulting the plugin library. Saves definitions to `docs/INDICADORES.md` in the working directory
- `exploring-data-sources`: Removed Phase 0 (library check); phases renumbered (Discovery=0, Profiling=1, EDA=2, Documentation=3)
- `data-scientist`: "Consumo de Indicadores YAML" section replaced — agent now reads definitions from `docs/INDICADORES.md` in the working directory
- `initializing-analysis`: Pipeline reduced from 5 phases (0–4) to 4 phases (0–3); `managing-indicators` Phase 4 removed; `docs/INDICADORES.md` header updated
- `CLAUDE.tmpl.md`: All `/analise-dados-m7:` → `/m7-analise-dados:`; Phase 4 section removed; Fase 2 description updated
- `commands/next`, `status`, `review`: Command references updated; Phase 4 logic removed; review checks updated to validate `docs/INDICADORES.md`
- `README.md`: Updated title and removed Indicator Library architecture section

### Removed
- `indicators/` directory with all domain YAMLs (`comercial/`, `receita/`, `clientes/`, `_index.yaml`, `_schema.yaml`)
- `managing-indicators` Phase 4 pipeline step

## [1.8.0] - 2026-03-16

### Removido
- Skill `managing-indicators` (SKILL.md, references, templates) — migrada para plugin standalone `m7-metas`
- Keyword `indicators` removida do marketplace.json (responsabilidade movida para `m7-metas`)

## [1.7.0] - 2026-03-05

### Adicionado
- 8 novos indicadores validados na Biblioteca de Indicadores:
  - `iea_mensal` (comercial): Índice de Efetividade do Assessor — meta fixa 0.7, não-aditivo
  - `modelo_servir_mensal` (comercial): Qualidade de atendimento — fonte escala 0-100 convertida para 0-1
  - `nps_mensal` (comercial): Net Promoter Score — fonte airbyte raw, meta 0.9, não-aditivo
  - `rentabilidade_mensal` (comercial): Performance vs CDI rolling 6M — média geométrica, PL >= 100k
  - `volume_consorcio_mensal` (comercial): Cartas ativas — meta N4 do airbyte raw JSON
  - `receita_consorcio_mensal` (receita): Comissões de consórcio — mapeamento comercial→codigo_xp
  - `receita_investimentos_produto_mensal` (receita): Receita por 7 produtos — view flat sem hierarquia
  - `receita_seguros_mensal` (receita): Comissões de seguros — fonte Prata, fuzzy matching
- Índice `_index.yaml` regenerado com 11 indicadores (7 comercial, 4 receita)
- Explanatory context completo em todos os indicadores: related_indicators, segmentation_dimensions, external_factors e investigation_playbook

## [1.5.0] - 2026-03-05

### Alterado
- Transporte MCP de stdio para HTTP (StreamableHTTP)
- MCPs agora conectam via http://localhost:3001/mcp (ClickHouse) e http://localhost:3002/mcp (Bitrix24)
- Compatível com Claude Code e Cowork (ambientes com VM isolada)

## [1.4.1] - 2026-03-04

### Corrigido
- Resolução de caminhos da biblioteca de indicadores: skills e agentes agora instruem Claude a localizar `indicators/` no diretório do plugin via Glob, não no diretório de trabalho do usuário
- Arquivos corrigidos: `exploring-data-sources/SKILL.md`, `planning-analysis/SKILL.md`, `managing-indicators/SKILL.md`, `data-scientist.md`, `CLAUDE.tmpl.md`

## [1.4.0] - 2026-03-04

### Adicionado
- Comando `status`: visão geral do progresso da análise, fase atual e próximo passo recomendado
- Comando `next`: avança para a próxima fase do pipeline com verificação de entry criteria
- Comando `review`: validação de consistência de dados por fase — rastreabilidade numérica, coerência aritmética (N1 = Σ N4), cross-check entre indicadores e adequação à audiência

### Alterado
- Template CLAUDE.tmpl.md: adicionada seção "Comandos de Orquestração" com tabela dos 3 comandos e fluxo recomendado (next → review → next)
- `.mcp.json`: simplificação dos MCPs ClickHouse e Bitrix24 — invocação direta via node sem shell wrapper

## [1.3.0] - 2026-03-04

### Adicionado
- Skill `initializing-analysis`: ponto de entrada do pipeline que scaffolda projetos de análise com diretório estruturado e CLAUDE.md orquestrador
- Template CLAUDE.tmpl.md: orquestrador de fases com phase gates, entry/exit criteria e tracking por tabela markdown
- Template README.tmpl.md: status checklist do projeto
- Template BRIEFING.tmpl.md: contexto de negócio pré-preenchido
- Pipeline cadenciado em 5 fases: Setup → Discovery → Planejamento → Execução → Indicadores

## [1.2.0] - 2026-03-04

### Adicionado
- Indicador `abertura_contas_300k` (comercial): contas ativadas 300k+ com cubo hierárquico 4 níveis
- Indicador `captacao_liquida_mensal` (comercial): captação líquida com GROUPING SETS e metas aditivas
- Indicador `faturamento_mensal` (receita): receita bruta com meta escritório independente
- Queries validadas contra ClickHouse `m7Bronze` com prefixo explícito de database
- Quality checks executados e aprovados para os 3 indicadores (todos PASS)
- Explanatory context completo: related_indicators, segmentation_dimensions, external_factors e investigation_playbook
- Status `validated` para os 3 indicadores (queries testadas, quality_checks passam, analysis_guide preenchido)

## [1.1.0] - 2026-03-04

### Adicionado
- Biblioteca de Indicadores M7 em YAML (`indicators/`) com schema, índice e estrutura por domínio
- Skill `managing-indicators`: criar, editar, validar, promover indicadores e regenerar índice
- Guia de boas práticas para indicadores (`indicator-guidelines.md`)
- Template YAML para novos indicadores (`indicator.tmpl.yaml`)
- Integração da biblioteca no pipeline: planning consulta indicadores antes de definir ad-hoc
- Agent `data-scientist` consome queries e quality_checks dos YAMLs
- Agent `executive-communicator` usa analysis_guide e explanatory_context para interpretação
- Troubleshooting MCP migrado para `data-source-catalog.md`

### Removido
- `references/mcp-data-sources.md` — substituído pela biblioteca de indicadores + troubleshooting no catálogo

### Alterado
- `exploring-data-sources`: Fase 0 verifica biblioteca de indicadores antes do discovery
- `planning-analysis`: Fase 3 consulta `_index.yaml` antes de definir métricas ad-hoc
- `generating-executive-reports`: Fases 1 e 2 usam indicadores YAML no pipeline
- Template `plano-analise.tmpl.md`: seções separadas para indicadores da biblioteca vs ad-hoc

## [1.0.0] - 2026-03-04

### Adicionado
- Plugin `analise-dados-m7` com pipeline completo de análise de dados
- Integração MCP: Bitrix24 (CRM, 48 tools) + ClickHouse (data warehouse, 6 tools)
- Agent `data-scientist`: extração, análise, EDA, validação de qualidade
- Agent `executive-communicator`: interpretação, relatórios adaptados a 4 audiências
- Skill `exploring-data-sources`: discovery + EDA com DATA-PROFILE.md
- Skill `planning-analysis`: planejamento com 7 padrões pré-montados
- Skill `generating-executive-reports`: orquestração do pipeline com max 3 iterações
- Framework de audiência: Diretoria, Gerentes, Técnico, Comercial (4 × 6 dimensões)
- Guia de escrita executiva com fórmulas de bullet points e anti-patterns
- Catálogo de fontes de dados com matriz de decisão ClickHouse vs Bitrix24
- Template PLANO-ANALISE.md e RELATORIO-EXECUTIVO.md
- Padrão #7: Cross-Source Join (ClickHouse × Bitrix24 via Python)
