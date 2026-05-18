# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.1] - 2026-05-18

### Fixed (creating-politica)

- Template `politica-m7-template.html`: `<title>` ficava com "Política de Processos" hardcoded para qualquer POL (placeholder estava só em `{{NOME_DA_EMPRESA}}`). Trocado por `<title>{{TITULO_DOCUMENTO}} — {{NOME_DA_EMPRESA}}</title>` — agora o title da janela reflete o título real da política gerada (ex.: "Política Geral de Governança Corporativa — M7 Investimentos").

## [2.1.0] - 2026-05-18

### Changed (creating-politica)

- **Template substituído** por `politica-isolada.html` (1142 linhas, versão enxuta sem shell-header global / sidebar TOC / tabs) com **145 placeholders `{{...}}`** explícitos cobrindo identidade + conteúdo das 8 seções.
- **Pipeline reescrito** (`generate-html-yaml.py` v2.1): substitui regex em HTML renderizado por simples `str.replace("{{KEY}}", value)` — muito mais robusto e legível.
- **Conteúdo das 8 seções agora é injetado** a partir de `politica-{slug}.md`. A limitação anterior (conteúdo das pages 3-15 preservava o exemplo POL-GOV-002) foi resolvida. O parser MD extrai blocos estruturados de cada h2 numerado:
  - 1. Objetivo: 2 parágrafos
  - 2. Escopo: lede + listas `**Aplica-se a:**` e `**Não se aplica a:**`
  - 3. Definições: tabela 2 col (até 12 linhas)
  - 4. Princípios: lede + h3+parágrafo (até 7)
  - 5. Diretrizes: lede + lista `**Sumário:**` + conteúdo livre (markdown→HTML)
  - 6. Papéis: lede + tabela 3 col (até 8)
  - 7. Governança: bloco "Revisão periódica" + tabelas Indicadores (até 5) + Exceções (até 6)
  - 8. Disposições: vigência + tabela doc relacionado (1)

### Added (creating-politica)

- **HTML autocontido (~1.4MB)** — script inlina CSS + 6 fonts TWK Everett OTF (base64) + 3 logos (base64). Output funciona em `file://`, HTTP server, anexo de email — sem depender de paths relativos. Resolve o problema reportado: ao salvar em `catalogo/` (sibling de `normativos-cockpit/`), o HTML antigo perdia identidade visual porque o CSS não estava lá.
- Flag `--no-inline` no script para debug (gera HTML que depende de paths relativos).
- `assets/m7-logo-favicon.png` adicionado.

### Removed (creating-politica)

- `assets/m7-header-dark.css` (template novo não usa)
- `assets/m7-print.css` (idem)
- Toda a lógica de renderização de shell-header, side-toc, formal-toc, tabs, kv-table, cover-grid — substituída pelo template com placeholders.

### Cockpit completude

- Copiados `m7-header-dark.css` e `m7-print.css` para `01-fundacao-2.1/normativos/normativos-cockpit/`, completando a fonte de design do projeto (decisão à parte do template isolado — visa robustez de longo prazo).

## [2.0.0] - 2026-05-18

### Breaking changes

- **`creating-politica` agora emite par `{slug}.html` + `{slug}.yaml` em vez de `.docx`.** O sidecar YAML é a fonte canônica de identidade consumida pelo Cockpit de Normativos M7; o HTML replica EXATAMENTE o template oficial `politica-m7-investimentos.html` (estrutura invariante). MAN, INS e ESP ainda emitem DOCX — migração pendente.
- **Plugin movido do marketplace `m7-creative` para `m7-data`** (alinhamento de domínio: governança documental fica junto com data/processos, não com presentations/design).

### Added (creating-politica)

- Workflow em 3 fases nomeadas com gates explícitos:
  - **Fase 1 (Discovery)** — entrevista guiada pelo schema YAML; output `BRIEFING-{CODE}.md`
  - **Fase 2 (Redação MD)** — produz `politica-{slug}.md` com as 8 seções narrativas
  - **Fase 3 (Produção HTML+YAML)** — script determinístico valida + renderiza
- `scripts/generate-html-yaml.py` — pipeline da Fase 3:
  - Validação custom contra `normativo.schema.yaml` (patterns, enums, required, required_when)
  - Renderização do `title_full.parts` em 2 variantes (shell `<span class="accent">` + cover `<em>` com auto-`<br>`)
  - Geração dinâmica de tabs, sumário lateral, sumário formal, KV-table, cover-grid
  - Substituição global de ph-meta, ph-title, pf-classif, total-pg em todas as páginas
- Assets oficiais incorporados: `politica-m7-template.html` (template invariante), `m7-tokens.css`, `m7-header-dark.css`, `m7-print.css`, `fonts/`
- References novas:
  - `normativo.schema.yaml` (schema canônico do sidecar)
  - `normativo.exemplo-pol-gov-002.yaml` (exemplo preenchido para golden test)
  - `normativo-schema.md` (guia anchor → campo, defaults POL)
- Golden test reproduzível: regenerar POL-GOV-002 a partir do exemplo YAML resulta em HTML quase byte-idêntico ao template (~131 linhas de diff, todas explicáveis por diferenças no próprio YAML exemplo — `pages: 15` vs template 16, ausência de entrada "Escopo" no toc — ou pela policy de `<em>` na cover-title definida no handoff §4).

### Changed (creating-politica)

- `references/normative-standards.md` reescrito: removidas seções de formatação DOCX (capa Word, headings, estilos python-docx, cores antigas Navy/Cream). Mantidas hierarquia normativa, codificação, ciclo de vida, frequências, status, conteúdo POL, indicadores e exceções.
- `SKILL.md` reescrito com 3 fases agrupadas em "Parte A · Discovery" e "Parte B · Produção", gates explícitos e tabela campo→anchor.

### Removed (creating-politica)

- `assets/TPL-POL-Template-de-Politica.docx` (template Word)
- `assets/m7-logo-*.png.b64` (base64 não usado pelo HTML)
- `scripts/generate-docx.py` (geração via clonagem do template Word)

### Migration notes

- Limitação atual: o script da Fase 3 espelha identidade/metadata em todos os anchors, mas **não injeta conteúdo das 8 seções narrativas** (pages 3-15). Após gerar o HTML, edite manualmente o corpo das seções usando o MD da Fase 2 como referência. Próxima iteração: injeção automática a partir do MD.
- Skills `creating-manual`, `creating-instrucao`, `creating-especificacao-tecnica` permanecem na geração DOCX antiga. Migração para HTML+YAML é o próximo passo.

## [1.0.2] - 2026-04-06

### Added
- Base64 (.b64) companions for all PNG assets across 4 skills (creating-especificacao-tecnica, creating-instrucao, creating-manual, creating-politica) — enables self-contained HTML generation

## [1.0.1] - 2026-03-13

### Fixed
- Cover code placeholder mismatch: template uses `[ÁREA]` (with accent), script searched for `[AREA]` (without accent)
- Document Control table placeholders: template uses descriptive text (`[Área responsável]`, `[Nome, Cargo]`, `[Código do documento de nível acima, se aplicável]`), script searched for short tokens (`[area]`, `[elaborado_por]`, `[documento_superior]`) that didn't exist in the template
- `[Nome, Cargo]` ambiguity: both "Elaborado por" and "Aprovado por" rows had identical placeholder text, causing both to receive the same value — now replaced by row index
- Footer not replaced: `TPL-MAN`/`TPL-POL`/`TPL-INS`/`TPL-ESP` remained in generated documents instead of the actual document code
- "Como usar este template" instructional section was not removed from generated documents
- Version Control table: `[DD/MM/AAAA]` and `[Autor]` placeholders were not replaced

## [1.0.0] - 2026-02-26

### Added
- Initial release with 4 document creation skills (POL, MAN, INS, ESP)
- QA compliance review skill (reviewing-normativo)
- Governance writer agent (Opus)
- Official DOCX templates with M7 branding
- Template-cloning approach preserving all formatting
