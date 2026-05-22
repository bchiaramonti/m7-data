# Changelog — m7-analise-dados

Todas as mudanças notáveis deste plugin serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [3.0.0] - 2026-05-22

### Breaking Changes
- **Output path mudou** de `output/relatorio-*.md` para `output/ANL-{ÁREA}-{NNN}-briefing.md`. Qualquer script, automação ou CLAUDE.md de projeto que dependa do pattern antigo deixa de encontrar o artefato — atualize os globs e os checklists antes do upgrade
- **A skill `generating-executive-reports` não gera mais o artefato final do relatório**. O passo 5 da Fase 2 agora produz um **briefing markdown** (`analytics-briefing.tmpl.md`) que serve de input para o **Claude Design**, onde o HTML do M7 Design System é preenchido e exportado em PDF. Workflows que esperavam um relatório executivo "pronto para entrega" diretamente da skill precisam adicionar o passo de Claude Design ao seu fluxo
- **Template antigo `relatorio-executivo.tmpl.md` removido** — projetos que customizavam esse template precisam migrar para `analytics-briefing.tmpl.md` (estrutura completamente diferente, com §1–§9, tokens `{{PLACEHOLDERS}}` 1:1 com o HTML do DS)

### Added
- `templates/analytics-briefing.tmpl.md` — briefing canônico do Analytics Report do M7 Design System (513 linhas, fonte da verdade do conteúdo, transcrito 1:1 ao HTML via find & replace no Claude Design)
- **Fase 5 (Handoff para Claude Design)** no pipeline da skill — instruções explícitas de transposição briefing → HTML → PDF, executadas fora da skill
- Checklist de **conformidade do briefing M7** (espelha o "Checklist final" do template): código ANL-{ÁREA}-{NNN}, KPIs com referência obrigatória, findings com IMPACTO non-negotiable, 12 tipos canônicos de gráfico do DS, recomendações com dono/prazo/ICE
- 4 anti-patterns: tokens literais não-resolvidos, blocos `>` (instrução do template) esquecidos, geração de HTML dentro da skill, gráfico fora dos 12 tipos canônicos sem justificativa

### Changed
- `skills/generating-executive-reports/SKILL.md`: Fase 2 renomeada `INTERPRET + BRIEF`; prompt do `executive-communicator` reescrito com regras duras do briefing (§1 Controle, §2 Capa, §3 TL;DR, §4 Scorecard, §5 Contexto, §6 Análises com 12 tipos de gráfico, §7 Insights narrados com IMPACTO, §8 Recomendações com ICE, §9 Anexos); critérios de saída exigem "nenhum `{{TOKEN}}` restante"; Fase 4 dividida em integridade da análise + conformidade do briefing M7
- `commands/status.md`: path do artefato de Fase 3 atualizado para `./output/ANL-*-briefing.md`
- `commands/review.md`: rastreabilidade da Fase 3 agora valida números contra `output/ANL-*-briefing.md`
- `skills/initializing-analysis/templates/CLAUDE.tmpl.md`: tabela de fases, descrição da Fase 3 (Exit criteria inclui handoff ao Claude Design), regras do agente `executive-communicator` ("não gera HTML/PDF — isso é Claude Design") e árvore de arquivos do projeto atualizados para a nova nomenclatura
- `skills/initializing-analysis/templates/README.tmpl.md`: checklist passa a incluir "Briefing gerado" e "Handoff para Claude Design"

### Removed
- `skills/generating-executive-reports/templates/relatorio-executivo.tmpl.md` — substituído pelo briefing canônico do M7 Design System

### Migration

Para projetos de análise **já scaffoldados** com versões anteriores:

1. **Output do `executive-communicator` é manual**: a skill nova vai salvar em `output/ANL-{ÁREA}-{NNN}-briefing.md`, mas o `CLAUDE.md` do seu projeto ainda referencia `output/relatorio-*.md` em vários pontos. Decida: (a) regenerar o `CLAUDE.md` via `/m7-analise-dados:initializing-analysis` ou (b) atualizar manualmente as 4 ocorrências (tabela de fases, Fase 3 "O que faz" + "Exit criteria", regras do executive-communicator, árvore de arquivos)
2. **Pipeline não fecha mais no markdown**: depois da Fase 4, abra o briefing no Claude Design, duplique `templates/template-analytics.html` do M7 Design System, faça find & replace dos `{{TOKENS}}`, copie os SVGs do `graficos.html` (12 tipos canônicos) e exporte PDF via Chrome/Edge (Safari quebra fontes)
3. **Briefing exige código documental** (`ANL-{ÁREA}-{NNN}`) na §1 Controle — defina a numeração da sua área antes de rodar a skill (`ANL-COM-001`, `ANL-FIN-001`, etc.) para evitar colisões

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
