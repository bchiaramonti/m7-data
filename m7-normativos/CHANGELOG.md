# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
