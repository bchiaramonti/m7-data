# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.0.0] - 2026-05-26

**BREAKING** — fecha os 3 bugs arquiteturais remanescentes do `creating-manual` v5.0.0 (#1 `identity.pages` derivado, #2 §11 Anexos opcional com novo shortcode `:::ficha-icp`, #11 RACI tbody injection N×M dinâmico — **CRÍTICO**). Após v5.1 (9 fixes cirúrgicos) + v6.0 (3 fixes arquiteturais), os 12 bugs registrados em `2026-05-20_bug-creating-manual-pages-fixed.md` estão resolvidos — manuais não precisam mais de patches surgical pós-Fase 3.

### Added (creating-manual)

- **Novo shortcode `:::ficha-icp`** para fichas de persona/ICP no capítulo §11 Anexos. Espelha estrutura canônica de 7-8 blocos da `ICP.xlsx` (Características da Pessoa, Dores Principais/Secundárias, Implicações, Resolução M7, Objetivos, Claims, Características da Negociação). 3 attrs: `titulo`, `icp`, `arquetipo` (`persona-decisor` ou `persona-gate`). Cabeçalho com chip invertido por arquétipo. CSS dedicado em `.ficha-icp`/`.ficha-cabecalho`/`.ficha-arquetipo`/`.ficha-bloco-*`. Allowlist expandida.
- **`{{ANEXOS_BLOCK}}` placeholder** no template (após página 11 Docs Relacionados). Quando MD declara `## 11. Anexos`, script gera article completo (`<article class="page anexos-page">`) com header/footer dinâmicos — sub-anexos `### A.`, `### B.` viram `<h3 class="anexo-titulo">`. Quando ausente, placeholder vira string vazia (zero impacto).
- **`render_raci_table(header, rows)`** — gera `<thead>` e `<tbody>` da matriz RACI §6.1 dinamicamente a partir do MD. Suporta **N atividades × M papéis** (não trava em 5×5) e **células compostas** `R, A` via `_render_raci_cell()` (reuso do fix de v5.1 Bug #6). Validação semântica emite **warnings** (não aborta) quando linha tem ≠1 A ou 0 R — autor revisa antes de publicar.
- **`render_anexos_block(parsed_content, code, titulo, versao, total_paginas)`** — renderiza o article de §11 Anexos com substituição inline de `__TOTAL__` (resolve ordem de substituição de placeholders).
- **`_DEFAULT_RACI_THEAD`/`_DEFAULT_RACI_TBODY`** como constantes Python — usadas quando MD não tem RACI, preservando layout legacy via placeholders `RACI_PAPEL_N` + `RACI_ATIV_N` (backward compat).
- **`_ANEXOS_ARTICLE_TEMPLATE`** como template string Python — `<article>` completo com header/footer, page 12, classe `.anexos-page`.

### Changed (creating-manual)

- **§6.1 Matriz RACI no template** colapsada de ~60 linhas hardcoded (5×5 com células default fixas) para `{{RACI_THEAD}}{{RACI_TBODY}}` (2 placeholders). Cells R/A/C/I do MD agora são honradas — não mais ignoradas silenciosamente.
- **`identity.pages`** marcado como `deprecated: true` no schema. Script ignora valor declarado e calcula `TOTAL_PAGINAS` dinamicamente: `11 + (1 if has_anexos else 0)`. Campo permanece no YAML para retrocompat do Cockpit de Normativos, mas a documentação `manual-schema.md` orienta omiti-lo.
- **Validação RACI semântica** de "abort" → "warning" — matrizes em transição (sub-processos novos, refactor em andamento) não bloqueiam mais a publicação. Autor revisa a Fase 3 antes de promover.
- **`component-catalog-manual.md`** documenta `:::ficha-icp` (8º shortcode), regra de células compostas R,A, e mudança de validação RACI.
- **SKILL.md** menciona v6.0: `:::ficha-icp` no quadro de shortcodes, `identity.pages` derivado no gate Fase 2 → Fase 3.
- **`m7-normativos/.claude-plugin/plugin.json`** bumped 5.1.0 → 6.0.0 com descrição refletindo os 3 fixes arquiteturais.
- **`m7-data/.claude-plugin/marketplace.json`** entrada sincronizada.

### Fixed (creating-manual)

- **BUG #11 (CRÍTICO)** — RACI cells R/A/C/I não eram parseadas do MD; template hardcodava 25 células sem placeholders → HTML distorcia accountability documentada. Fix: tbody injection com geração N×M dinâmica.
- **BUG #2** — Falta de slot para conteúdo de referência denso (fichas ICP, tabelas taxonômicas, anexos). Fix: `{{ANEXOS_BLOCK}}` opcional + shortcode `:::ficha-icp`.
- **BUG #1** — `identity.pages` tratado como fixo (=11) impedia manuais com anexos. Fix: derivado pelo script, ignora declaração do YAML.

### Notes

- Caminho **Composição Modular Full** (split do template em fragments) foi diferido para v7.0 — caminho A evolutivo (1 placeholder `ANEXOS_BLOCK` + article completo gerado pelo script) entrega o user-value com risco menor (-77 linhas no template, +327 no script).
- Paginação multi-página de anexos é v7.0 (atual: 1 article = 1 página com `page-break-inside: avoid` nos cards).
- Smoke tests aprovados: MAN-PERF-003 gold sem anexos (11 páginas, RACI compound `A,R` em E4 renderizado como `.raci-ra`, 0 residuais) + MAN-PERF-003 com §11 sintético (12 páginas, `:::ficha-icp` completo, 0 residuais).

---

## [5.1.0] - 2026-05-26

Corrige 9 bugs cirúrgicos do `creating-manual` v5.0.0 descobertos durante geração de MAN-CRE-002, MAN-GOV-001 e MAN-TEC-001, eliminando ~10-15 min de patches surgical pós-Fase 3 por manual gerado.

### Added (creating-manual)

- **Placeholder `{{TOC_HTML}}` dinâmico** — sumário formal (página 2) gerado a partir de `structure.formal_toc[]` no YAML, ou de `DEFAULT_FORMAL_TOC` quando ausente. Regra estrita: `subsection: true` é o ÚNICO discriminador da classe `h2` no TOC.
- **Placeholder `{{BPMN_SVG}}` único** em §4.4 — substitui o `<svg>` hardcoded com 8 sub-placeholders. Quando MD declara `:::diagrama` em §4.4, usa o SVG do autor (preservado via `@@SC_BLOCK_N@@`); senão renderiza SVG default via `render_default_bpmn_svg()`.
- **Classes CSS `.narrative-list` e `.section-foot-note`** no template — substituem 2 inline `style="..."` de linhas 1411 (BPMN narrativa) e 1617 (§7 KPI footer).
- **Classe `.raci-cell.raci-ra`** para células compostas R+A no shortcode `:::raci` (mesmo papel é Responsible E Accountable).
- **Classe `.cover-suffix`** com CSS `:not(:empty)::before { content: ' '; }` — espaço entre `</em>` e sufixo só aparece quando há sufixo de fato (fix de espaço residual no `title_full`).
- **`structure.formal_toc[]`** no `normativo.schema.yaml` — schema explícito com campos `num`, `label`, `pg`, `subsection: bool`. Validação: numeração toplevel `^\d+$` + `subsection: true` são mutuamente excludentes (emite warning).
- **Função `_md_isolate_tables()`** — pre-processa o MD inserindo blank line entre conteúdo não-tabela e cabeçalho de tabela MD. Previne python-markdown de absorver tabelas em `</li>` adjacentes.
- **Função `_render_raci_cell()`** — centraliza renderização de células RACI (single, compound R+A, vazio).
- **Função `render_default_bpmn_svg(labels)`** — gera o SVG BPMN default a partir de um dict de labels.

### Changed (creating-manual)

- **§4.3 Interfaces** no template: `<p>{{TEXTO_INTERFACES}}</p>` → `{{TEXTO_INTERFACES}}` (sem wrapper) — permite shortcodes block-level. Script roteia conteúdo de §4.3 por `markdown_to_html()` (em vez de capturar só primeiro parágrafo via `.split("\n\n")[0]`), preservando `:::processo-grid` e outros shortcodes.
- **TOC estático no template** substituído por `{{TOC_HTML}}`. Fix do bug onde §9 era erroneamente marcada com classe `h2`.
- **`restore_shortcodes(html)` GLOBAL** no final de `main()` — defense-in-depth para qualquer `@@SC_BLOCK_N@@` que escape de qualquer caminho de extração (não só §4.3).
- **DTO prefix stripping** — script remove `^\*\*DTO-\d{2}\*\*\s*[—·\-–]\s*` do conteúdo extraído do MD antes de atribuir ao placeholder, evitando duplicação com o `<strong>DTO-NN</strong> · ` hardcoded no template.
- **Cronograma key lookup** com `_norm_cad()` — normaliza markdown bold (`**Diário**`), acentos (`á → a`) e case. Suporta variações pt/en (daily/weekly/monthly/quarterly/biannual/yearly).
- **`split_cover_title()`** ganhou strip defensivo + uso de `.get("text", "")` para robustez contra parts malformadas.
- **Allowlist CSS** adicionada com `narrative-list`, `section-foot-note`, `raci-ra`, `cover-suffix`.

### Fixed (creating-manual)

- **BUG #3** — `:::diagrama` ignorava SVG inline do autor (template tinha SVG default hardcoded). Fix: `{{BPMN_SVG}}` único.
- **BUG #4** — Cronograma off-by-one (primeira cadência Diário vazia). Fix: normalização robusta de chave via `_norm_cad()`.
- **BUG #5** — DTO duplicava prefixo `**DTO-NN**`. Fix: regex strip antes da substituição.
- **BUG #6** — Células RACI compostas `R, A` silenciosamente ignoradas no shortcode `:::raci`. Fix: detecção via `_RACI_COMPOUND_RE` + classe `.raci-ra`.
- **BUG #7** — Espaço residual entre `</em>` e `</h1>` no cover-title quando suffix vazio. Fix: `<span class="cover-suffix">` + CSS `:not(:empty)::before`.
- **BUG #8** — TOC marcava toplevel (§9) com classe `h2` erroneamente. Fix: TOC dinâmico via `render_formal_toc()` com regra estrita.
- **BUG #9** — Inline styles em narrative-list (§4.4) e section-foot-note (§7) violavam contrato "zero `style="..."` inline". Fix: 2 classes novas + substituição.
- **BUG #10** — `:::processo-grid` declarado mas não expandido em §4.3 (script capturava só primeiro parágrafo). Fix: `markdown_to_html` em §4.3 + `restore_shortcodes` global.
- **BUG #12** — Tabelas MD absorvidas em `</li>` adjacentes. Fix: `_md_isolate_tables()` pre-processor.

### Notes

- Smoke tests em `/tmp`: MAN-PERF-003 gold (com MD completo) — 0 placeholders residuais, BPMN SVG do autor preservado (viewBox 1000×320), TOC com apenas §4.1 como h2, DTO sem prefixo duplicado. MAN-PERF-003 sem MD — default BPMN SVG renderizado (viewBox 1000×360, labels "Tarefa 1"..."Decisão?"). `:::raci` compound — `R, A` e `A, R` viraram `<span class="raci-cell raci-ra">R<br>A</span>`.
- Bugs #1, #2 e #11 (arquiteturais) ficam para v6.0.

---

## [5.0.0] - 2026-05-20

**BREAKING** — refatoração completa de `creating-manual` para espelhar a arquitetura da `creating-politica` v4.0. A skill abandona o pipeline DOCX (python-docx clonando template Word) e adota o **trio canônico HTML+YAML+review.md** já usado pela política — agora todos os normativos M7 saem no mesmo formato, consumível pelo Cockpit de Normativos. Manuais ganham gate obrigatório de design review, separação rígida design × conteúdo, e validação automática contra schema e allowlist de classes.

### Added (creating-manual)

- **`scripts/generate-html-yaml.py`** (novo, ~1.860 linhas) — pipeline determinístico clonado de `creating-politica` e adaptado para manuais: validação de schema YAML, parser de 10 seções específicas de manual (Objetivo, Escopo, Definições, Visão Geral + SIPOC + Interfaces + BPMN, Regras de Negócio, Papéis + RACI 5×5, KPIs + PPIs, Cronograma, Critérios de Qualidade DTO, Documentos Relacionados), expansão de 7 shortcodes, inline de CSS+fontes+logos como base64, e validação pós-render contra allowlist.
- **149 placeholders no template** (vs. 145 da política) cobrindo identidade + estruturas procedurais manual-específicas: SIPOC 5-col (3-3-4-3-3 itens), BPMN com 4 tasks + 1 gateway + 2 fins + 3 narrativas, RACI 5×5 (5 papéis × 5 atividades), 2 KPIs + 2 PPIs (5 campos cada), 5 cadências de cronograma (Diário/Semanal/Mensal/Trimestral/Semestral), 5 critérios DTO de qualidade, 4 docs relacionados.
- **Novo shortcode `:::raci`** para matrizes RACI adicionais no corpo do MD (a RACI principal usa placeholders fixos do template). Sintaxe: tabela markdown 5×5 dentro do shortcode com células contendo R/A/C/I; o parser valida códigos válidos e renderiza com cores semânticas (`.raci-r`/`.raci-a`/`.raci-c`/`.raci-i`) preservando letra textual para acessibilidade P&B.
- **`references/manual-schema.md`** (novo) — guia do schema YAML para autor de MAN, com defaults específicos (tipo=MAN, aprovador_role=Head de área, revisaoFreq=Semestral, pages=11) e mapeamento YAML → 149 placeholders.
- **`references/manual-design-rules.md`** (novo) — 9 dimensões de revisão específicas de manual (8 herdadas de política + 1 nova: **conformidade procedural** que valida BPMN com viewBox, SIPOC ≥3 itens por bloco, RACI com exatamente 1 A por linha, KPI/PPI com fórmula executável e meta numérica, cronograma com outputs concretos, DTO mensurável).
- **`references/component-catalog-manual.md`** (novo) — catálogo de 7 shortcodes (6 herdados + `:::raci`) e allowlist expandida com classes manual-específicas: BPMN (`.bpmn-task`, `.bpmn-gateway`, `.bpmn-flow`, etc.), SIPOC (`.sipoc`, `.col.is-process`), RACI (`.raci-table`, `.raci-cell`, `.raci-r/a/c/i`), Indicadores (`.kpi-card`, `.kpi-card.ppi`), Cronograma (`.timeline`, `.ritual`), Qualidade (`.dto-list`).
- **`references/reference-output/MAN-PERF-003-gold.{html,yaml,md}`** (novo) — gold reference do manual de Rituais de Gestão. Agente compara cada HTML em revisão contra esse gold. YAML e MD são starters (engenharia reversa do HTML) — determinismo total byte-a-byte não é garantido nesta versão; ver README do diretório.
- **`agents/manual-design-reviewer.md`** (novo) — agente irmão de `politica-design-reviewer`, read-only (Read/Grep/Glob, opus), produz relatório markdown com Score A/B/C/D, issues categorizadas (CRITICO / ATENCAO / SUGESTAO) em 9 dimensões e Quick Fix CSS. Gate obrigatório no final da Fase 3 — Score < B bloqueia entrega.
- **`assets/manual-m7-template.html`** (novo) — template oficial com 149 placeholders, 11 páginas A4 (Capa, Controle+Sumário, Objetivo+Escopo, Definições, Visão Geral, Fluxograma BPMN, Regras, Papéis, Indicadores, Cronograma+Qualidade, Docs+Versões+Aprovações).
- **Assets compartilhados** copiados de `creating-politica`: `m7-tokens.css`, `fonts/` com 6 TWK Everett OTF, `m7-logo-favicon.png`. Mantém autocontainment (~1.4-1.5 MB HTML standalone).
- **Stub `{slug}.review.md`** gerado pelo script — placeholder que o agente `manual-design-reviewer` sobrescreve com o relatório completo.
- **Validações soft (warnings)** para tipo=MAN: `lifecycle.revisaoFreq ≠ "Semestral"` e `governance.aprovador_role ≠ "Head de área"` emitem warning no stderr sem bloquear.
- **Auto-cleanup `_strip_empty_slots()`** adaptado para manual: remove `<li>` vazios em SIPOC, `<tr>` totalmente vazios em docs relacionados, e cards KPI/PPI sem `.name` preenchido.

### Changed (creating-manual)

- **Output muda de DOCX para trio HTML+YAML+review.md** — `MAN-XXX-NNN.docx` substituído por `MAN-XXX-NNN.html` (autocontido ~1.5MB) + `MAN-XXX-NNN.yaml` (sidecar canônico) + `MAN-XXX-NNN.review.md` (relatório do agente). Cockpit de Normativos passa a consumir manuais com o mesmo contrato das políticas.
- **Workflow muda de 5 fases informais para 3 fases formais com gates**: Discovery (Fase 1, BRIEFING.md + gate de confirmação) → Redação MD (Fase 2, manual-{slug}.md + validação) → Produção HTML+YAML+Review (Fase 3, script determinístico + gate do agente Score ≥ B).
- **SKILL.md reescrita por completo** — espelha 100% a estrutura de `creating-politica/SKILL.md`: filosofia, princípio de geração (trio), contexto normativo, assets autocontidos, 3 fases com tabelas de mapeamento, validações automáticas + visuais, regras e anti-patterns.
- **Schema YAML compartilhado** — `references/normativo.schema.yaml` é cópia da política (esquema já cobre POL/MAN/INS/ESP); defaults específicos de MAN são aplicados pela skill.
- **`m7-normativos/.claude-plugin/plugin.json`** bumped 4.0.0 → 5.0.0 com descrição reescrita refletindo a paridade de output entre creating-politica e creating-manual.
- **`m7-data/.claude-plugin/marketplace.json`** entrada de `m7-normativos` sincronizada para 5.0.0 com a mesma descrição.

### Removed (creating-manual)

- **`assets/TPL-MAN-Template-de-Manual.docx`** — template Word não é mais necessário; substituído por `manual-m7-template.html`.
- **`scripts/generate-docx.py`** — pipeline DOCX baseada em python-docx removido; substituído por `generate-html-yaml.py`.
- **`assets/m7-logo-dark.png.b64` e `m7-logo-offwhite.png.b64`** — arquivos base64 separados não são mais necessários; o script inlina logos diretamente dos PNGs durante a geração.

### Migration Notes

- Autores que tinham processos baseados no DOCX precisam migrar: Fase 1 agora produz BRIEFING.md (YAML), Fase 2 produz manual-{slug}.md (markdown estruturado), Fase 3 emite o trio. O `.docx` antigo não tem upgrade automático — manuais legados podem ser convertidos manualmente reescrevendo o conteúdo no formato MD canônico.
- `INS` e `ESP` ainda saem em DOCX (migração futura). Apenas POL e MAN agora têm contrato HTML+YAML+review.md unificado.
- Smoke test sintético `MAN-TEC-001` confirmou pipeline end-to-end: trio gerado (1.428 KB autocontido), zero placeholders residuais, YAML válido, teste negativo (MD com `<style>`) corretamente rejeitado pela validação.

---

## [4.0.0] - 2026-05-19

**BREAKING** — refatoração completa do contrato MD ↔ template em `creating-politica` para resolver a despadronização visual observada em POL-GOV-001/002/003. O diagnóstico foi que o MD da Fase 2 acumulou responsabilidade de design (via `<style>` blocks, `style="..."` inline e classes ad-hoc), permitindo que cada autor improvisasse seu mini-design system. Esta release isola design (template + tokens + shortcodes catalogados) de conteúdo (MD canônico, semântico) e introduz **gate obrigatório de Score ≥ B** via agente revisor.

### Added (creating-politica)

- **5 shortcodes semânticos pandoc-fenced** no MD da Fase 2: `:::papel-card`, `:::papel-card-separador`, `:::callout` (variantes `-info` / `-alerta` / `-exemplo`), `:::indicador`, `:::diagrama` (aceita `<svg>` ou `<img>`), `:::processo-grid`. Cada um mapeia para classes CSS já catalogadas no template — autor não precisa escrever HTML inline com classes nunca mais.
- **`references/component-catalog.md`** (novo) — catálogo único de shortcodes + allowlist exaustiva de classes CSS permitidas no HTML final. Inclui processo formal para adicionar shortcode novo (`Como adicionar um shortcode novo`).
- **`references/policy-design-rules.md`** (novo) — 8 dimensões de revisão específicas de política (6 do design-reviewer genérico + 2 específicas: Paginação A4 + Estrutura 8 seções). Usado como gabarito pelo agente revisor.
- **`references/reference-output/`** (novo) — diretório com trio canônico `POL-GOV-001-gold.{html,yaml,md}` que serve como ponto de calibração visual. Agente compara cada HTML em revisão contra esse gold.
- **`agents/politica-design-reviewer.md`** (novo) — agente read-only (Read/Grep/Glob, opus) que produz relatório markdown com Score A/B/C/D, issues categorizadas (CRITICO / ATENCAO / SUGESTAO) e Quick Fix CSS pronto para aplicar. Gate obrigatório no final da Fase 3 — Score < B bloqueia entrega.
- **`SHORTCODE_CATALOG` e `CSS_ALLOWLIST`** em `generate-html-yaml.py` — fontes de verdade compartilhadas para validação. CSS_ALLOWLIST reflete o template oficial completo (104 classes estruturais + tipográficas + nav + shortcodes).
- **`validate_md_content()`** — valida o MD da Fase 2 ANTES de qualquer renderização. Rejeita: `<style>`, `style="..."`, `<svg>` solto, `<div class="X">` com X fora da allowlist, shortcodes inválidos ou sem fechamento. Mensagens com linha + trecho para localização rápida.
- **`expand_shortcodes()` + `restore_shortcodes()`** — pipeline de stash (similar ao SVG) que substitui `:::nome ... :::` por placeholders `@@SC_BLOCK_N@@` antes do markdown parser e restaura HTML após. Evita que python-markdown serialize HTML de shortcode como prosa.
- **`render_shortcode()`** — renderizadores específicos por shortcode, usando apenas classes da allowlist e tokens canônicos (zero hex literal).
- **`validate_html_classes()`** — pós-render: extrai todas as classes do HTML final e rejeita as que não estão na allowlist. Defesa em profundidade contra leak via shortcode mal-renderizado ou edição direta do template.
- **`validate_html_no_inline_styles()`** — pós-render: conta `<style>` blocks e `style="..."` inline; compara contra baseline do template (1 style block + 12 inline esperados). Excesso indica leak.
- **`.callout`, `.callout-title`, `.callout-tag`, `.callout-alerta`, `.callout-exemplo`** — novas classes no template para shortcode `:::callout`. Tokens canônicos (lime, âmbar para alerta, verde claro para exemplo).
- **`.indicador-card`, `.indicador-nome`, `.indicador-meta`** — novas classes no template para shortcode `:::indicador`.
- **Stub `{slug}.review.md`** gerado pelo script — placeholder que o agente `politica-design-reviewer` sobrescreve com o relatório completo. Trio final é `.html` + `.yaml` + `.review.md`.

### Changed

- **MD da Fase 2 é canônico de conteúdo, não de design**. Toda apresentação visual vem de shortcodes catalogados + template. Esta separação fica explícita no SKILL.md (Regras Importantes #6/7/8, Anti-Patterns reformulados) e no `normativo-schema.md` (seção "CSS customizado no MD — PROIBIDO").
- **Fase 3 da pipeline** ganha 2 fases adicionais: (a) validação técnica do MD ANTES de expandir shortcodes; (b) validação técnica do HTML APÓS render; (c) invocação do agente como gate de Score ≥ B.
- **`markdown_to_html`** agora usa extensão `md_in_html` da python-markdown — necessário para que tags `<div>` block-level (vindas dos shortcodes) não sejam envolvidas em `<p>`.
- **`:::diagrama` aceita tanto `<svg>` quanto `<img>`** — útil para SVGs já encodados em data URI (caso POL-GOV-002).
- **CHANGELOG** documenta a refatoração como motivação histórica do diagnóstico nos 3 primeiros POLs.

### Removed

- **Permissão de `<style>` no MD** — `normativo-schema.md` seção "CSS customizado no MD do autor" foi reescrita como "PROIBIDO (v4.0)". Status anterior ("use prefixos exclusivos") era a raiz da despadronização.
- **Permissão de `style="..."` inline** — idem.
- **Permissão de HTML inline com classes ad-hoc** — só shortcodes do catálogo ou classes da allowlist do template são aceitos.
- **Auto-isolation `_md_isolate_html_blocks`** continua existindo mas é redundante para shortcodes (que agora têm stash próprio). Mantido para compatibilidade com SVG.
- **Seção "Namespaces CSS reservados pelo template (v3.0+)"** do `normativo-schema.md` — substituída por "Apresentação visual — shortcodes do catálogo (v4.0)".

### Fixed

- **Despadronização visual entre POL-GOV-001/002/003**: a regeração com a skill v4.0 produz HTMLs visualmente consistentes — POL-GOV-001 byte-idêntico ao gold (Score A); POL-GOV-002 após migração do MD (Score B, 4 ATENCAO sugerindo refinar com `:::papel-card` futuramente); POL-GOV-003 com **zero ocorrências de `.icp-*`** (eliminadas pelo gate).
- **Leak de hex literal em POL-GOV-003**: `.icp-card-title { color: #424135 }` virava parte do HTML final via `<style>` injetado. Agora bloqueado na validação.
- **Leak de redefinição em POL-GOV-002**: `.inv-card` redefinido com hex `#1a1d22` via `<style>`. Agora bloqueado.
- **Classes ad-hoc `.cadeia-img`/`.cadeia-caption`** em POL-GOV-002: substituídas pelo shortcode `:::diagrama` (que aceita `<img>` para SVGs embedded em data URI).

### Migration guide (v3.x → v4.0)

POLs criadas em v3.x continuam vigentes — mas qualquer **regeração** com a skill v4.0 exige migrar o MD-fonte se ele contiver:

1. **`<style>` block**: remova. Se o block redefinia classes do template (`.inv-*`, `.skill-proc-*`, `.embed-svg`), o resultado fica visualmente igual sem ele (template já tem as regras). Se definia classes ad-hoc (`.icp-*`, `.cadeia-*`), substitua pelo shortcode correspondente.
2. **`<div class="X">` HTML inline**: se X está na allowlist (ex.: `.inv-card`), pode ficar como está — mas a forma idiomática v4.0 é usar `:::papel-card` (mesmo output, MD mais limpo).
3. **`<svg>` solto**: envolva em `:::diagrama caption: ...`.
4. **`<img class="X">`**: se X é classe ad-hoc, remova ou envolva em `:::diagrama` (que aceita `<img>` desde v4.0).
5. **`style="..."` inline**: remova; use shortcode correspondente.

Após migrar o MD, rode `python scripts/generate-html-yaml.py ...`. Se script aborta, leia a mensagem (sempre indica linha + trecho).

## [3.2.0] - 2026-05-19

Iteração baseada na revisão de `SKILL-v2.3.0-PATCH-PROPOSAL.md` que catalogou **6 anomalias residuais** (severidade B) descobertas no uso de v3.1.0 para gerar POL-GOV-001, POL-GOV-002 e POL-GOV-003 em produção. Motivação central: **operador da skill é o Claude COWORK** (Claude no claude.ai web, sem filesystem local) — workarounds em `postprocess-{CODE}.py` deixam de ser viáveis. v3.2 internaliza todos os 6 fixes no canonical script para que trio (`.html` + `.yaml` + `.md`) saia correto no primeiro passe.

### Added (creating-politica)

- **`_strip_empty_slots(html)`** — novo helper em `generate-html-yaml.py` que executa auto-cleanup pós-substituição de placeholders, removendo (a) blocos `<div class="principle">` com `<div class="pt"></div>` vazio (anomalia #2), (b) `<tr>` vazios em `<table data-table="papeis">` (anomalia #3), (c) `<tr>` vazios em `<table data-table="doc-related">` (anomalia #5). Idempotente — rodar 2x produz mesmo output. Chamado entre `inject_m7_classes()` e validação de placeholders residuais.
- **10 slots dinâmicos para DOC_REL** (anomalia #5): template expande de 1 para 10 `<tr>` com placeholders `DOC_REL_{1..10}_*`. Script popula até 10 entradas a partir da tabela markdown da seção 8.2; slots não usados são removidos pelo cleanup pass. Quando ZERO documentos são declarados, o cleanup injeta uma linha única `<tr><td colspan="3" class="muted-empty">Nenhum documento subordinado vinculado nesta versão.</td></tr>` como fallback informativo (substituindo a tabela vazia sem mensagem que existia em v3.1).
- **CSS `.muted-empty`** no template `<style>` block (font-style italic, color `var(--vc-400)`, centralizado, padding 14px 8px) — visual da fallback row de DOC_REL.
- **Atributos `data-table="papeis"` e `data-table="doc-related"`** nas duas tabelas alvo do cleanup pass — seam HTML semântico para o regex localizar inequivocamente sem depender de posição ou cabeçalho.

### Changed

- **Tipografia h3.sub revisada (anomalia #6)**: `font-size: 12px → 14.5px`, `font-weight: 500 → 600`, `color: var(--vc-600) → var(--vc-900)`, `margin: 12px 0 6px → 18px 0 8px`, `letter-spacing: 0.02em → -0.005em`, gap 8 → 10. Decorative line `::before` `width: 12px → 18px, height: 1px → 2px`. Resolve hierarquia tipográfica indistinguível do body em capítulo 5 (Diretrizes), que afetava POL-GOV-001/002/003.
- **Tipografia h4.subsub revisada (anomalia #6)**: `font-size: 11px → 12.5px`, `font-weight: 500 → 600`, `color: var(--vc-600) → var(--vc-700)`, `margin: 10px 0 4px → 14px 0 6px`, `letter-spacing: 0.02em → 0.005em`.
- **`section-lede` aplicado aos 2 `<p>` do Objetivo** (anomalia #1): seção 01 agora usa a mesma classe tipográfica de Escopo/Princípios/Diretrizes/Papéis (11.5px verde-claro, max-width 70ch). Eliminava o descuido do template onde o Objetivo era exceção sem motivo aparente.
- **Tratamento de `governance.parent: null`** em `build_placeholders()` (anomalia #4): quando `parent` é null ou dict sem `code`, fallback semântico `parent = {"code": "N/A", "title": "Política raiz da hierarquia normativa M7"}` evita o " · " solto que existia em POL-GOV-001 (Política raiz da hierarquia).
- **DOC_REL builder** em `parse_content_md()`: loop `for i in range(MAX_DOC_REL=10)` substitui o handler de slot único.

### Fixed

- 6 anomalias residuais catalogadas em `SKILL-v2.3.0-PATCH-PROPOSAL.md` (revisão 2026-05-19), todas severidade B:
  - **#1** `section-lede` ausente nos parágrafos do Objetivo
  - **#2** Slot de Princípio vazio (P5-P7 quando autor declara só 4) renderizando indicador lateral lime e blocos em branco
  - **#3** Linhas vazias na tabela de Papéis e Responsabilidades (PAPEL_4 a PAPEL_8 quando autor declara só 3)
  - **#4** "Documento superior" renderizando `<span class="mono"></span> · ` solto quando `governance.parent: null` (caso raiz da hierarquia)
  - **#5** Linha vazia em "Documentos relacionados" quando seção 8.2 do MD não declara nenhuma linha + limite hardcoded de 1 slot
  - **#6** Hierarquia tipográfica fraca em h3.sub/h4.subsub no capítulo 5 (Diretrizes)

### Notes

- **Operação pelo Claude COWORK**: motivação central da iteração. v3.2 elimina necessidade de orquestrar `postprocess-{CODE}.py` externo — o trio sai correto direto do `generate-html-yaml.py`. A pasta `catalogo/_tools/` com postprocess scripts pode ser arquivada (mantida apenas para os 3 docs pré-v3.2 até regeneração futura).
- **Fix forward apenas**: POL-GOV-001/002/003 publicados permanecem com CSS antigo até decisão explícita de regeneração pelo Bruno (regra "no regenerate published artifacts" preservada).
- **Idempotência validada**: 7 smoke tests sintéticos em `/tmp/v3.2.0-smoke/test_strip_empty.py` cobrem (i) Princípios 4+3 vazios, (ii) Papéis 3+5 vazios, (iii) DOC_REL 3+7 vazios, (iv) DOC_REL 0 com fallback, (v) DOC_REL 7 cheios sem fallback, (vi) backwards compat 7 princípios full, (vii) idempotência (rodar 2x = output idêntico). Todos PASS.

## [3.1.0] - 2026-05-19

Iteração baseada na versão atualizada de `SKILL-v2.3.0-PATCH-PROPOSAL.md`, que adicionou 3 anomalias residuais (#4, #5, #6) descobertas no uso de v3.0.0 com POL-GOV-002 final (com SVG inline da Cadeia de Valor M7 + tabela 5.2 adjacente a `<div class="inv-card">`).

### Added (creating-politica)

- **`links.artifact_md`** como campo first-class no schema (anomalia #4). Opcional. Convenção: `{basename}.md` co-localizado com .html e .yaml. Útil para o cockpit oferecer "abrir fonte editável" ao curador e para auditoria/regeneração determinística.
- **Stash/restore de `<svg>` inline** na função `markdown_to_html` (anomalia #5). Antes do parse via python-markdown, blocos `<svg>...</svg>` são substituídos por placeholders `@@SVG_BLOCK_N@@`; após o parse, são restaurados intactos. Sem isso, a lib serializa o conteúdo do SVG como prosa (perde `<rect>`, `<path>`, e transforma `<text>` em texto solto).
- **Auto-isolamento de bloco HTML + markdown** via `_md_isolate_html_blocks` (anomalia #6). Insere linha em branco entre `</div|p|table|figure|aside|section>` e o próximo elemento markdown (`#`, `|`, `-`, `*`), garantindo que a python-markdown reconheça o limite do bloco HTML e processe a tabela/heading/lista que vem depois.
- **Suporte a tabelas no fallback** (`_md_render_table` + `_is_md_table`). Quando a lib `markdown` não está instalada, o fallback agora renderiza tabelas markdown como `<table>` semântico — antes só suportava bullets/parágrafos/headings.

### Changed

- `markdown_to_html` refatorado: stash SVG → isola HTML blocks → parse (md_lib ou fallback) → restore SVG. Função `_md_fallback` extraída como helper público.
- Exemplo `normativo.exemplo-pol-gov-002.yaml` atualizado para usar convenção atual: `artifact_html: "POL-GOV-002.html"` + `artifact_md: "POL-GOV-002.md"` (co-localizados em catalogo/).
- `references/normativo-schema.md` ganhou 4 novas subseções:
  - "SVG inline preservado (v3.1+)" — stash/restore + uso de `.embed-svg`
  - "Tabela markdown adjacente a HTML é auto-isolada (v3.1+)" — comportamento auto + exemplo
  - "`links.artifact_md` — fonte editável (v3.1+)" — semântica, convenção, casos de uso
  - Em "Schema → Links": doc do `artifact_md`
- `SKILL.md` Fase 2 ganhou bullets v3.1 sobre SVG, auto-isolamento de tabelas e `artifact_md`.

### Notes

- **Anomalia #4 é histórica**, não código novo: `parse_briefing()` + `yaml.safe_dump()` já preservavam campos custom como `artifact_md`. A v3.1 só formaliza o campo no schema + docs.
- **Catálogo do user em produção não foi tocado** — feedback aplicado: smoke test sintético em `/tmp/` é suficiente para validar bug fixes. Autor regere quando quiser.

## [3.0.0] - 2026-05-18

Iteração baseada em [SKILL-v2.3.0-PATCH-PROPOSAL.md](../../catalogo/SKILL-v2.3.0-PATCH-PROPOSAL.md), que documentou 3 anomalias residuais descobertas no uso real da v2.3.0 em POL-GOV-002 (inventário narrativo de 21 processos com 7 page-breaks).

### Breaking changes (creating-politica)

- **Rename de classes CSS** para evitar colisão com `<style>` injetado no MD do autor:
  - `.proc-block` → `.skill-proc-block`
  - `.proc-card` → `.skill-proc-card`
  - `.proc-title` → `.skill-proc-title`
  - `.proc-owner` → `.skill-proc-owner`
  - `.camada-sep` → `.skill-camada-sep`
  - `.camada-title` → `.skill-camada-title`
- Documentos que dependiam dessas classes herdando estilo do template precisam migrar para os novos nomes (ou adotar o padrão `.inv-*` natativo abaixo). Em produção apenas POL-GOV-002 existia, e o autor já havia migrado para `.inv-*` como workaround — impacto efetivo zero.

### Added (creating-politica)

- **Padrão `.inv-*` nativo no template** (anomalia #1 do patch proposal): 8 classes (`inv-card`, `inv-title`, `inv-owner`, `inv-block`, `inv-block strong`, `inv-sep`, `inv-sep-title`, `inv-sep-desc`) que renderizam cards verticais narrativos com border-left lime. Adequado para inventário com explicação por processo ("Por que existe / O que transforma / Alimenta"). Autor do POL-GOV-002 pode agora deletar 8 das 11 linhas do `<style>` block do MD — as classes batem 1:1.
- **Padrão `.embed-svg-*`** para SVG inline (cadeia de valor, fluxogramas): 3 classes (`embed-svg`, `embed-svg svg`, `embed-svg-caption`). Padrão reutilizável.
- **Height estimator com warnings** (anomalia #2): nova função `_estimate_chunk_height(md_text)` no script. Estima altura px do chunk renderizado (cards = 180px, tabelas = 35px/linha, SVG = 540px, h3 = 30px, h4 = 22px, bullets = 22px, parágrafos = 22px). Emite warning no stderr quando chunk > 900px (margem de segurança em relação aos ~960px úteis do page-body A4). Aplicado tanto ao chunk 0 (CONTEUDO_DIRETRIZES) quanto aos extras gerados por `<!-- /page-break -->`. Não bloqueia geração — só alerta.

### Changed

- **`references/normativo-schema.md`** ganhou seção robusta "Namespaces CSS reservados pelo template" com 3 padrões HTML lado a lado:
  - Padrão A: grid compacto `.skill-proc-*`
  - Padrão B: vertical narrativo `.inv-*`
  - Padrão C: SVG embed `.embed-svg`
- Documentação do "Page-break com alerta de altura" com tabela de heurística e exemplos.
- Documentação do CSS customizado (prefixos próprios, scope com seletor descendente, regra de especificidade).
- **SKILL.md** Fase 2 menciona namespaces reservados + page-break alerta + link para a doc detalhada.

### Migration

POL-GOV-002 atual continua funcionando sem ajuste — workaround do user usa `.inv-*` que agora é nativo. Para "limpar":

1. Deletar o `<style>` block do MD da seção 5 (linhas 91-103 do POL-GOV-002.md).
2. Regenerar — visual idêntico, MD mais limpo, 1 fonte de verdade para as classes (template).

### Anomalia #3 (style global) — abordagem

Não fizemos `<style scoped>` (deprecated em HTML5). Optamos por **documentação explícita** sobre:
- Quais namespaces são reservados (não sobrescrever)
- Como usar prefixos próprios em CSS customizado
- Como escopar via seletor descendente quando necessário

Solução pragmática que cobre 100% dos casos sem adicionar complexidade no parser.

## [2.3.0] - 2026-05-18

### Fixed (creating-politica)

- **Bug `DATA_REVISAO=""` hardcoded** (anomalia #6 do POL-GOV-002.PATCHES): trocado para `date_label` igual `DATA_ELABORACAO`/`DATA_APROVACAO`. Caixa do Revisor agora recebe data correta.
- **Bullets do markdown fallback não aplicavam inline bold/italic** (anomalia #1): fallback de `markdown_to_html` agora processa `**bold**`, `*italic*`, `` `code` ``, `[link](url)` dentro de bullet items, headings e parágrafos.

### Added (creating-politica)

- **Marker `<!-- /page-break -->` na seção 5 do MD** (anomalia #7): divide Diretrizes em múltiplas páginas A4. Chunk 0 → CONTEUDO_DIRETRIZES (página existente); chunks 1..N → `<article class="page">` extras inseridos via novo `{{EXTRA_DIRETRIZES_PAGES}}`. Compatível com docs sem markers (vira 1 página).
- **Auto-numeração de páginas via JS**: cada `<article class="page">` recebe seu número em `.pf-page strong` baseado na posição no DOM. Páginas extras geradas pelo script herdam numeração correta sem precisar hardcode.
- **Função `inline_markdown(text)`**: processa bold/italic/code/link em campos de texto que vão diretamente para o template (não só em CONTEUDO_DIRETRIZES). Aplica-se a 30+ placeholders: TEXTO_OBJETIVO_*, LEDE_ESCOPO, ESCOPO_INCLUSAO_*, ESCOPO_EXCLUSAO_*, DEF_TEXTO_*, LEDE_PRINCIPIOS, PRINCIPIO_*_DESCRICAO, LEDE_DIRETRIZES, LEDE_PAPEIS, PAPEL_*_RESPONSABILIDADES, REVISAO_PERIODICA_INTRO, GATILHO_REVISAO_*, TEXTO_VIGENCIA, DOC_REL_1_RELACAO.
- **Função `inject_m7_classes(html)`**: pós-processa o HTML rendered injetando `.doc-table` em `<table>`, `.sub` em `<h3>`, `.subsub` em `<h4>` (anomalias #10/#11/#12). Lookahead negativo preserva elementos com classe já declarada (`.proc-title`, `.camada-title`, `.kv-table`).
- **Função `inline_external_images(html, base_dir)`** (anomalia #3): converte `<img src="<path-relativo>">` em `data:image/{ext};base64,...`. Suporta svg/png/jpg/webp/gif. Path relativo ao MD da Fase 2. URLs http/https e data: URIs já existentes são preservadas.
- **CSS no template** (anomalias #4, #8, #12):
  - `.approval-card` flex-column + `min-height: 110px` + `.what min-height: 14px` + `.sig-line margin-top: auto` — alinhamento horizontal robusto entre os 3 cards mesmo com `.what` vazio
  - `.doc h4.subsub` (11px + lime accent) — hierarquia visual abaixo de `.sub` (h3 = 12px)
  - `.proc-card` / `.proc-title` / `.proc-owner` / `.proc-block` / `.camada-sep` / `.camada-title` — padrão de inventário de processos reutilizável

### Changed (creating-politica)

- **Parser leniente**:
  - Bloco Escopo aceita `**Aplica-se a**` (bold) OU `### Aplica-se a` (h3). Idem "Não se aplica a" (anomalia #2).
  - Bloco Revisão/Vigência aceita prefixo numérico opcional: `### 7.1 · Revisão periódica` ou `### Revisão periódica` (anomalia #5).
- **Ordem de operações no main**: `inline_assets` agora roda DEPOIS da substituição de placeholders, garantindo que logos das páginas extras (geradas via `{{EXTRA_DIRETRIZES_PAGES}}`) também sejam base64-inlinados.
- **`references/normativo-schema.md`** ganhou 5 novas seções documentando o comportamento da v2.3: page-break, marcação leniente, injeção de classes M7, cards de inventário, imagens externas.
- **SKILL.md** Fase 2 menciona explicitamente as variações lenientes aceitas.

### Notes

- A v2.3 incorpora **9 dos 12 fixes** documentados em `POL-GOV-002.PATCHES.md`. As outras 3 anomalias são decisões do autor (não da skill): #9 (bucketing) desaparece com markers explícitos; "Decisão A" (escopo: holding) já foi entregue na v2.2.0; "Decisão B" (revisor com separador `·`) é uma escolha YAML, complementada pelo CSS flex-column que torna o alinhamento robusto mesmo se o autor esquecer o separador.
- POLs gerados pelas v2.0–2.2 continuam válidos. Para aproveitar os fixes upstream, regere com `python3 generate-html-yaml.py --briefing <yaml> --content <md> --output-dir <dir>`.

## [2.2.0] - 2026-05-18

### Added (creating-politica)

- **Campo `governance.escopo`** no schema YAML (sincronizado com schema canônico do cockpit). Enum: `holding | transversal | processo`. Controla alocação na Matriz do Cockpit:
  - `holding` → 1 célula na lane "Holding M7" (col POL/MAN/INS/ESP)
  - `transversal` → N células, uma por processo no array `processos`
  - `processo` → 1 célula no único processo do array
- **Auto-derivação no validador**: quando `escopo` é omitido, o script (`normalize_governance`) preenche:
  - 0 ou 1 processo → `processo`
  - 2+ processos → `transversal`
  - `holding` **nunca** é auto-derivado (sempre explícito) — proteção contra docs que cobrem P1-P12 mas semanticamente são transversais, não holding.
- O valor derivado é serializado no YAML de saída — leitor (cockpit) sempre vê o campo preenchido.

### Changed

- `governance` agora exige `escopo` na validação (`required: [owner, parent, processos, escopo]`).
- Exemplo POL-GOV-002 atualizado com `escopo: holding` explícito.
- `references/normativo-schema.md` ganhou seção dedicada com **4 jeitos de alinhar à Holding**, tabela de regras de alocação e vocabulário de códigos por lane (Holding/Gerencial/Primário/Apoio).
- SKILL.md Fase 1: campo `escopo` adicionado à entrevista de discovery (governance row).

### Notes

- "M7" continua removido do enum `identity.area` (consolidado para GOV na v2.1.2). O canônico do cockpit ainda lista `M7` por compatibilidade, mas o code pattern já rejeita códigos com dígitos no bloco AREA — a remoção local mantém o validador estritamente consistente.
- "M7" agora existe **apenas** no vocabulário interno do cockpit como célula-destino da lane Holding, acessível via `escopo: holding`. Nunca aparece no array `processos`.

## [2.1.2] - 2026-05-18

### Changed (creating-politica)

- **Removido `M7` do enum de `identity.area`** no `normativo.schema.yaml`. O enum agora é `[GOV, PERF, INV, CRE, SEG, UNI, TEC, PES]` (8 áreas funcionais). Políticas institucionais da holding (escopo cross-cutting) usam `area: GOV` — não há código separado.
- **Motivo da consolidação**: o code pattern `^(POL|MAN|INS|ESP)-[A-Z]{2,4}-[0-9]{3}$` exige letras puras no bloco AREA, então `POL-M7-001` (com dígito) já era inválido por regex. A entrada `M7` no enum de área era inconsistente e enganosa.
- **Sincronizado** validador no `generate-html-yaml.py` (`ALLOWED_AREA`) com o novo enum.
- Atualizado `references/normative-standards.md` removendo `M7` da tabela de AREA e o exemplo `POL-M7-001` (que era inválido).

### Migration

- POLs existentes que usavam `area: M7` (caso houvesse) precisam migrar para `area: GOV`. O code já não casava com regex, então provavelmente nenhuma POL real está afetada.

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
