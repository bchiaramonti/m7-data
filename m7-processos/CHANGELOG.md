# Changelog

Todas as mudanças notáveis deste plugin serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o versionamento segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-05-06

Primeira versão estável da skill `mapeamento-n1`. Pipeline completo de 3 fases (entrevista crítica → BRIEFING.md SSOT → produção) que gera 4 artefatos M7-2026.

### Added
- **Skill `mapeamento-n1`** com pipeline completo de 3 fases:
  - **Fase A** — Entrevista & Crítica iterativa em 5 blocos com checkpoints; loop de até 3 ciclos com `process-critic` antes de fechar BRIEFING.
  - **Fase B** — `BRIEFING.md` como single source of truth (frontmatter YAML + seções markdown).
  - **Fase C** — Produção sequencial de 4 artefatos.
- **4 artefatos visuais**:
  - **N1** Cadeia de Valor (Porter, 3 camadas — variantes A master / B linear)
  - **N2** Missão do Processo (SIPOC simplificado: Verbo+Objeto+Finalidade+Inputs+Outputs+Owner)
  - **N3** Mapa de Interdependência (grafo neural com posições %, edges SVG, fricções com halo pulsante)
  - **N4** Documento Oficial PDF paginado A4 (capa fullbleed, sumário, intro, N1, 1 página por SIPOC, mapa neural em landscape, tabela de relações, encerramento, footer numerado)
- **2 subagents read-only**:
  - `process-critic` (Read, Grep, Glob; opus) — analisa BRIEFING e devolve relatório com Bloqueadores/Avisos/Sugestões.
  - `pdf-validator` (Read, Bash; opus) — extrai texto do PDF gerado e valida estrutura visual.
- **3 scripts Python**:
  - `check_briefing.py` — validador determinístico aplicando 30+ regras de [`critique-rules.md`](skills/mapeamento-n1/references/critique-rules.md) (regex, set diff, length, cross-checks). Saída JSON com bloqueadores/avisos.
  - `build_artifacts.py` — orquestrador da Fase C: lê BRIEFING e gera N1/N2/N3/N4 em sequência. Inclui geradores inline para os 3 templates HTML (substitui placeholders, gera SVG paths, RELATIONS no JS).
  - `render_pdf.py` — Playwright + Chromium primário, WeasyPrint fallback. `prefer_css_page_size=True` respeita @page named pages para landscape no meio do documento. Modo compacto auto-ativado se `scrollHeight > 1123px`.
- **Templates HTML** (5):
  - `template-cadeia-de-valor.html` (variante A master)
  - `template-cadeia-de-valor--linear.html` (variante B linear)
  - `template-missao-do-processo.html` (sidebar + painel SIPOC)
  - `template-mapa-de-interdependencia.html` (neural graph)
  - `template-documento-oficial.html` (A4 paginado, novo neste release)
- **CSS de paginação**:
  - `m7-print.css` (novo) — `@page` named pages (cover/toc/landscape), page-break, modo compacto.
  - `m7-tokens.css`, `m7-header-dark.css` — mantidos.
- **9 references**:
  - `n1-cadeia-de-valor.md`, `n2-missao-do-processo.md`, `n3-mapa-interdependencia.md` — regras detalhadas por nível
  - `n4-documento-oficial.md` (novo) — paginação, capa, footer, fit, landscape no N3
  - `phase-a-entrevista-critica.md` (novo), `phase-b-briefing.md` (novo), `phase-c-producao.md` (novo) — fluxos do pipeline
  - `critique-rules.md` (novo) — catálogo de 30+ regras nomeadas (VERB-GENERIC, IO-DUP, OWNER-PESSOA, REL-ORFA, etc.)
  - `pdf-generation.md` (novo) — Playwright + WeasyPrint fallback, troubleshooting
  - `design-system-m7.md` — tokens M7-2026, anti-padrões visuais
- **3 exemplos**:
  - `exemplo-m7-preenchido.html` — caso M7 visualizado em N1
  - `exemplo-briefing-m7.md` (novo) — BRIEFING M7 com 18 processos, valida com 0 bloqueadores
  - `exemplo-documento-m7.pdf` (novo) — PDF gerado a partir do BRIEFING acima (31 páginas, 280 KB)

### Changed
- **`plugin.json`** — descrição expandida (de "estrutura inicial" para descrição completa do pipeline) e keywords ampliadas.
- **`marketplace.json`** (no marketplace `m7-data`) — entrada do plugin atualizada com nova descrição e versão 1.0.0.

### Migration

Não há migração necessária — primeira versão pública/stable. Versão 0.1.0 (scaffold) não tinha skills funcionais.

## [0.1.0] - 2026-05-06

### Added
- Estrutura inicial do plugin (scaffold).
- Diretórios `skills/`, `agents/`, `commands/` criados (vazios).
- Manifesto `plugin.json` com metadados básicos.
- Registro no marketplace `m7-data`.
