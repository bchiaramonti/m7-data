# Changelog

Todas as mudanças notáveis deste plugin serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o versionamento segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [2.0.1] - 2026-05-14

Patch crítico de geração: o `build_artifacts.py` (skill `mapeamento-n1`) produzia o N2 (Missão do Processo) com markup divergente do template interativo, resultando em layout achatado (todos os SIPOCs empilhados em scroll) em vez do shell sidebar + panel-com-toggle. Corrigido para casar exatamente com a estrutura esperada pelo CSS + JS do template.

### Fixed

- **`render_n2_sidebar()`** — gerava `<li><a href="#X">` dentro de `<ul>` com `<h4>` headers. CSS do template espera `<div class="mp-group">` com `<div class="mp-group-label">` (não `<h4>`) e botões `<button class="mp-item" data-process-id="X">` (não anchors). Sem `data-process-id`, o JS de toggle nunca casa.
- **`render_n2_panels()`** — gerava `<article id="X" class="mp-process-page">`. Template tem CSS `.mp-detail { display: none }` + JS que toggles `.active` no `<article id="detail-X">`. Como nada batia, o CSS hiding nunca aplicava e todos os panels apareciam empilhados.
- **Primeira ativação faltava** — nenhum elemento recebia `.active` por default. Agora apenas o primeiro processo (overall) recebe `.mp-item.active` na sidebar e `.mp-detail.active` no painel, replicando o estado inicial do template.
- **Headline + Owner reestruturados** — `<h2><span class="code-prefix">` → `<h2 class="mp-process-name"><span class="code">`; `<div class="mp-owner">OWNER · <span class="v">` → `.mp-owner > .label/.name` (estrutura esperada pelo CSS).
- **Setas SIPOC ausentes** — adicionados 2 `<div class="sipoc-arrow"><svg>` entre as 3 colunas. Sem elas, as colunas ficavam coladas.
- **Coluna do meio com classe errada** — `<div class="sipoc-col mp-mission">` → `<div class="sipoc-col mission">` (CSS hook é `.sipoc-col.mission`, não `.mp-mission` na coluna; `.mp-mission` é classe do `<p>` interno).
- **Labels SIPOC em capslock literal** — "INPUTS"/"MISSAO"/"OUTPUTS" → "Inputs"/"Missão"/"Outputs". Template usa `text-transform: uppercase` no CSS — não escrever maiúsculas no HTML para manter acessibilidade do screen reader.
- **Camada tag minúscula** — `{escape_html(camada.title())}` (gerava "Gerencial") → mapeamento dedicado: gerencial → "Camada gerencial", primário+núcleo → "Camada primária · Vertical", apoio → "Camada de apoio". Pixel-match com o template original.
- **Aba "Política" não tratada no loop de tabs** — adicionado branch que reescreve href para `documento-oficial-{slug}.html` quando `n4-pdf` está em artefatos, ou converte para `<div>` não-navegável caso contrário.
- **Fallback para processos sem SIPOC** — antes processos sem `sipoc.verbo` eram silenciosamente pulados (não apareciam no painel mas apareciam na sidebar — clique em órfão). Agora geram `<article class="mp-detail" id="detail-{codigo}">` com placeholder `<div class="mp-empty">`, mantendo a navegação coerente.

### Migration

Não-breaking. Quem gerou N2 com v2.0.0 deve regenerar via `python3 scripts/build_artifacts.py briefing.md output_dir/ --skip-pdf` (ou re-rodar a skill `/mapeamento-n1`) para receber o layout corrigido.

Validado contra `examples/exemplo-briefing-m7.md` (18 processos): 18 botões `.mp-item`, 18 articles `.mp-detail`, 2 elementos `.active` (G1 sidebar + G1 panel), 36 setas SIPOC. JS de toggle e deep-linking via hash funcionais.

## [2.0.0] - 2026-05-13

**MAJOR · skill mapeamento-n1** — N4 (Documento Oficial) re-arquitetado de server-rendered (Playwright/Jinja) para HTML standalone client-side com export PDF via `window.print()`. Promovido para "Política formal" — documento assinável com governança completa (código, vigência, aprovações, escopo, controle de versões). Nova 4ª aba "Política DOC" navega entre todos os 4 templates.

Cruzamento com o design canvas exportado de Claude Design (`process-mapping-value-chain`): identificadas 4 templates byte-quase-idênticas + 1 artefato novo (Política). Sincronizado.

### Added
- **N4 promovido a "Política"** — template `template-documento-oficial.html` agora é HTML standalone de 1660 linhas com 8 páginas A4 portrait, toolbar interativo (contador, navegação ◀/▶, botão "Exportar PDF") e estrutura formal: Capa · Controle de versões + Aprovações + Sumário · Objetivo/Escopo/Definições · Estrutura da cadeia + Princípios · Gerenciais · Primários · Apoio · SIPOC sample + Interdependências + Governança.
- **4ª aba "Política DOC"** nos 4 templates principais (N1 master, N1 linear, N2 SIPOC, N3 mapa) — navegação consistente entre todos os artefatos do set.
- **Seção `politica:`** no `BRIEFING.tmpl.md` — ~30 campos formais agrupados em `metadata` (código, vigência, próxima revisão, área responsável), `versoes` (histórico até 3 entradas com status vigente/obsoleto), `aprovacoes` (3 papéis: elaborador/revisor/aprovador), `objetivo_texto`, `escopo` (inclusões/exclusões/doc relacionados), `governanca` (comitê revisor, doc SLA, área compliance), `sipoc_amostra` (2 processos featurados).
- **Campo `meta`** opcional em `processos[]` — KR/indicador principal exibido para verticais primárias na página de Primários do N4.
- **Bloco 6 da Fase A · Governança & Política** em `references/phase-a-entrevista-critica.md` — 7 sub-blocos cobrindo todos os campos de `politica:` com perguntas, inferências, push-back proativo e checkpoints. Executado apenas se `n4-pdf` em `artefatos_a_gerar`.
- **18 novas regras de validação** em `scripts/check_briefing.py`:
  - `check_politica()`: POLITICA-AUSENTE, POLITICA-META-VAZIO, POLITICA-SEM-VERSAO, POLITICA-VIGENTE, POLITICA-VERSAO-INCOMPLETA, POLITICA-VERSAO-STATUS, POLITICA-VERSOES-EXCESSO, POLITICA-APROV-AUSENTE, POLITICA-APROV-INCOMPLETO, POLITICA-OBJ-VAZIO, POLITICA-OBJ-CURTO, POLITICA-INCLUSOES, POLITICA-INCLUSOES-EXCESSO, POLITICA-EXCLUSOES, POLITICA-DOC-REL, POLITICA-GOV-VAZIO, POLITICA-AMOSTRA-QTD, POLITICA-AMOSTRA-ORFA, POLITICA-AMOSTRA-SEM-SIPOC.
  - `check_processos_meta()`: POLITICA-META-PRIM (aviso para verticais sem meta).
- **`exemplo-briefing-m7.md`** atualizado com bloco `politica:` completo usando dados M7 reais (POL-PROC-001, aprovações Bruno/Juliane/Marcelo, comitê de processos, etc.) + campo `meta` em P3–P8.

### Changed
- **Arquitetura do N4** — server-rendered (Playwright primário + WeasyPrint fallback) → client-side (HTML standalone + `window.print()`). Trade-offs documentados em `references/n4-documento-oficial.md §7 · Migração e legacy`.
- **`references/n4-documento-oficial.md`** reescrito de zero (231 linhas → 271 linhas) cobrindo nova arquitetura: estrutura de 8 páginas portrait, toolbar interativo, mapeamento BRIEFING→placeholders (122 placeholders catalogados), checklist de validação, anti-padrões atualizados e seção §7 com motivos da migração e quando ainda usar a abordagem legacy.
- **SKILL.md** — tabela de Pré-requisitos menciona Bloco 6, tabela de Fase A inclui Bloco 6 condicional, schema BRIEFING expõe `politica:`, descrição do N4 troca "PDF paginado" por "HTML A4 com window.print()", file tree marca scripts deprecated.
- **Descrição do plugin** (`plugin.json` + `marketplace.json`) — "documento oficial PDF" → "política formal A4-paginada com export PDF via window.print()" para refletir o framing de governança.

### Deprecated
- **`scripts/render_pdf.py`** — Playwright + WeasyPrint não é mais necessário para N4. Mantido com banner `[DEPRECATED 2026-05]` para casos de uso residuais (CI server-side, PDF de N1/N2/N3 individuais).
- **`scripts/build_n4.py`** — Jinja includes + BeautifulSoup parsing de fragmentos não é mais necessário (template novo é standalone). Mantido com banner deprecation.

### Fixed
- **Bug pré-existente em `template-cadeia-de-valor--linear.html`** — aba "Mapa de interdependência" era `<div class="tab">` não-navegável; corrigida para `<a class="tab" href="template-mapa-de-interdependencia.html">`. Mesmo bug existia no design exportado de Claude Design.

### Migration

**BREAKING para usuários que geram N4 (Documento Oficial / Política):**

1. **BRIEFINGs existentes com `n4-pdf` em `artefatos_a_gerar` agora falham validação** com `POLITICA-AUSENTE` até a seção `politica:` ser preenchida. Para migrar:
   - Adicione o bloco `politica:` no frontmatter YAML (use [BRIEFING.tmpl.md](BRIEFING.tmpl.md) ou [exemplo-briefing-m7.md](examples/exemplo-briefing-m7.md) como referência).
   - Adicione `meta: "KR/indicador"` em cada vertical primária (subcamada=nucleo) — aviso, não bloqueador.
   - Execute o Bloco 6 da Fase A (`references/phase-a-entrevista-critica.md §7`) para coletar os campos guiado.

2. **Pipeline de geração do N4 mudou**:
   - **Antes**: `python3 scripts/build_n4.py briefing.md output_dir/` → `documento-oficial-{slug}.html` (com Jinja includes) → `python3 scripts/render_pdf.py *.html *.pdf` (Playwright)
   - **Agora**: a skill substitui placeholders no `template-documento-oficial.html` standalone → usuário abre o HTML no navegador → clica em "Exportar PDF" no toolbar (Cmd+P, "Salvar como PDF", marcar "Plano de fundo gráfico")
   - Scripts antigos foram deprecados (não removidos). Continuam funcionais para casos residuais — ver banners no topo dos arquivos.

3. **Aba "Política" nos templates N1/N2/N3** — visualmente novos cliques. Quem tinha HTMLs gerados pela skill v1.x verá a aba ausente; re-gerar pela skill v2.0 para incorporar.

4. **Sem perda de dados** — BRIEFINGs antigos que NÃO pediam N4 continuam validando sem mudança (seção `politica:` é opt-in por `n4-pdf`).

## [1.2.2] - 2026-05-08

Patch de layout: inset de 30px nas lanes em relação à borda esquerda do pool — corrige sobreposição de labels.

### Fixed
- **Lane inset (`lane.x = pool.x + LANE_HEADER_WIDTH`)** — bug v1.1-v1.2.1: lanes herdavam `x = pool.x`, fazendo o label vertical do pool ("Maquina de Vendas - Onda 1") competir com labels verticais das lanes ("Comercial", "Plataforma de Dados") pela mesma faixa de 30px à esquerda. Resultado: texto sobreposto e truncado no bpmn-js. **Fix:** `lane.x = pool.x + 30` e `lane.width = pool.width - 30`. Cria uma faixa exclusiva para o label do pool.
  - `compute_auto_layout.py` Passo 4 atualizado
  - `auto-layout-algorithm.md` § Passo 4 documenta o inset com diagrama ASCII
  - `exemplo-onboarding.bpmn` lanes atualizadas (`x=160→190`, `width=1240→1210`)

### Migration
Não-breaking. Apenas correção de coordenadas das lanes nos artefatos gerados pela skill. BPMNs existentes continuam funcionando — para corrigir manualmente um BPMN antigo, ajustar `<dc:Bounds>` de cada `<bpmndi:BPMNShape>` referenciando lane: somar 30 ao `x` e subtrair 30 do `width`.

## [1.2.1] - 2026-05-08

Patch visual: lanes brancas (`#ffffff`) em vez de warm off-white (`#fffdef`) para contraste máximo com tasks `#fdfbe5`.

### Changed
- **Lane fill: `#fffdef` → `#ffffff`** — feedback de uso real (BPMN Onda1 v0.4) mostrou que o contraste entre lane warm e task esverdeado era visualmente fraco. Lanes brancas + tasks esverdeadas dão contraste muito mais nítido. **Pool mantém `#fffdef`** (preserva aroma M7).
- **`exemplo-onboarding.bpmn`** — 3 lanes (Comercial, Compliance, Operações) atualizadas para `bioc:fill="#ffffff"`.
- **`m7-bpmn-styling.md`** — tabela, filosofia, anti-padrões e checklist atualizados; nova nota "exceção BPMN para `#ffffff` em lanes" com justificativa explícita (não propagar para outros artefatos M7).

### Migration
Não-breaking. Mudança visual incremental sobre a v1.2.0. BPMNs gerados com paleta v1.2.0 continuam válidos; ao reabrir e re-renderizar via skill v1.2.1, recebem lanes brancas automaticamente.

## [1.2.0] - 2026-05-08

Correções visuais e bug fixes do validador na skill `drawing-bpmn-flowcharts` baseadas em feedback de uso real (BPMN do projeto Onda1 Quick Win MVP).

### Changed
- **Paleta visual diferenciada por elemento BPMN** — substitui paleta uniforme `#fffdef` da v1.1:
  - Lane / Pool: `#fffdef` (warm off-white) — mantido
  - Task / Subprocess: `#fdfbe5` (off-white esverdeado, contraste sutil sobre lane)
  - Gateway: `#fef3a8` (amarelo pálido — accent de decisão; cor exclusiva do contexto BPMN, não propagar para outros artefatos M7)
  - Start event (fluxo principal): `#eef77c` (lime) — mantido
  - End event (todos: sucesso, error, terminate): `#b8000f` (vermelho M7 WCAG-safe; antes só erro era vermelho)
- **`exemplo-onboarding.bpmn`** atualizado com nova paleta (referência canônica para LLMs gerando novos BPMNs)
- **`exemplo-onboarding-descritivo.md`** — seção "Aderência ao M7-2026" reescrita com nova tabela

### Fixed
- **Validador reconhece data associations** — bug v1.1: `<bpmn:dataInputAssociation>` e `<bpmn:dataOutputAssociation>` não tinham endpoints parseados → todas eram flagadas como cruzando próprio source/target. Em diagramas com dataStores, isso gerava 14+ falsos positivos. **Fix:** parse de sourceRef/targetRef dentro das tasks (userTask, serviceTask, sendTask, receiveTask, scriptTask, manualTask, businessRuleTask, subProcess, adHocSubProcess, transaction, callActivity).
- **Validador reconhece labels multiline** — bug v1.1: labels com `\n` ou `\r\n` interno (ex: `"A3\nOrquestrador"`) eram contados como 1 linha de N chars → flagados como overflow. **Fix:** split por `\n` e considerar largura máxima das linhas + altura total.
- **Auto-layout de loop-back com offset lateral (5 waypoints)** — bug v1.1: edges com `target.x < source.x` saíam pela borda superior do source com kink visual colado ("linha começa do meio do node"). **Fix:** sair pela direita + 30px offset lateral antes da virada vertical → linha tem "respiro" antes de subir.
- **Auto-layout de dataStoreReferences distintos** — bug v1.1: múltiplos `<bpmn:dataStoreReference>` apontando para o mesmo `<bpmn:dataStore>` global recebiam bounds idênticos → 2 cilindros sobrepostos no diagrama (caso clássico cross-pool data sharing). **Fix:** posicionamento individual baseado na lane de cada referência, com espaçamento de 80px se houver múltiplas refs na mesma lane.

### Added
- **Detector 6 (`duplicate-shape-bounds`)** em `validate_bpmn_readability.py` — flagra 2+ shapes com bounds idênticas (severity: fail). Pega bug arquitetural de cilindros sobrepostos antes do diagrama virar produto.
- **Detector 7 (`long-container-label`)** em `validate_bpmn_readability.py` — flagra pool labels > 30 chars e lane labels > 25 chars (severity: warning) — bpmn-js trunca esses labels em containers altos com rotação vertical.
- **Tipos `dataStoreReference`, `dataObjectReference`, `manualTask`, `businessRuleTask`, `transaction`, `callActivity`** ao enum de `nodes[].type` em `templates/input-schema.tmpl.json` (estavam ausentes na v1.1).
- **Anti-patterns** em `bpmn-notation-essentials.md`:
  - Pool label > 30 chars / Lane label > 25 chars (warning)
  - 2+ dataStoreReferences com bounds idênticos (fail)
  - Tasks com mesma cor da lane (invisibilidade visual)
  - Gateway com mesma cor de task (decisão sem destaque)
  - End event verde caqui (confunde com stroke)
  - Mais de 1 amarelo no diagrama (ruído visual)
- **Seções 4 e 5 em `auto-layout-algorithm.md`**: "Loop-back com offset lateral" + "DataStoreReference cross-pool" com pseudocódigo e exemplos.
- **Constantes `DATA_STORE_W`, `DATA_STORE_H`, `DATA_OBJECT_W`, `DATA_OBJECT_H`, `DATA_REF_GAP`, `LOOP_LATERAL_OFFSET`** em `compute_auto_layout.py`.

### Migration
Não-breaking. Mudanças apenas de cor (`bioc:fill`) e correções de validador. BPMNs v1.1 continuam abrindo normalmente em qualquer ferramenta. Ao reabrir e re-renderizar via skill v1.2, recebem a nova paleta automaticamente.

**Nota sobre falsos positivos do validador no diagrama do projeto Onda1**: BPMN antigo (v1.1-gerado) tinha 14 fails de `edge-crosses-node` e 3 de `label-overflow` que eram falsos positivos. v1.2 elimina esses falsos positivos — o validador agora só reporta issues geométricos genuínos.

## [1.1.0] - 2026-05-08

Adição da skill `drawing-bpmn-flowcharts` — construtor de diagramas BPMN 2.0 com auto-layout determinístico, validação iterativa de legibilidade e cores M7-2026.

### Added
- **Skill `drawing-bpmn-flowcharts`** — workflow de 7 fases (parse → validação de notação → auto-layout → M7 styling → validação de legibilidade iterativa → re-validação de notação → escrita de artefatos):
  - Aceita 3 formatos de input: JSON estruturado, descrição conversacional em PT, markdown narrativo
  - Gera `.bpmn` portátil (BPMN 2.0 standard) compatível com Camunda Modeler 7+, Camunda 8, bpmn.io, Bizagi, Signavio
  - Aplica cores M7-2026 via extensões `bioc:fill` / `bioc:stroke` (Camunda / bpmn-js native)
  - Validação iterativa (max 3 ciclos) garante: sem sobreposição de linhas, sem cruzar nós, sem texto trincado, sem distorção de aspect-ratio, fluxo predominante LTR
  - **Suporte nativo a AI agents (Camunda 8.8+)**: `aiAgentTask` (single-call) e `adHocSubProcess` agentic com tools, suportando os 4 padrões canônicos (Human triggers AI / AI suggests + human decides / Multi-agent / Fallback)
- **5 references** (`skills/drawing-bpmn-flowcharts/references/`):
  - `bpmn-notation-essentials.md` — catálogo BPMN 2.0 (events, activities, gateways, conexões, pools/lanes, artefatos) + checklist de validação em 7 categorias
  - `auto-layout-algorithm.md` — algoritmo determinístico (topological sort + ranks + lanes × rank grouping + waypoints) com constantes geométricas (H_SPACING=150, V_SPACING=100, dimensões padrão por tipo)
  - `readability-rules.md` — 5 detectores geométricos (edge-crosses-node via Cohen-Sutherland, edge-overlap por colinearidade, label-overflow por largura de char, aspect-ratio guard, RTL flow ratio > 30%) + estratégias de relayout
  - `m7-bpmn-styling.md` — tabela de cores M7 por tipo de elemento BPMN + sintaxe XML (extensão `bioc:`) + compatibilidade entre ferramentas
  - `ai-agents-bpmn.md` — ad-hoc sub-process pattern (Camunda 8.8+) + 4 padrões canônicos + naming conventions + anti-patterns + casos de uso M7
- **3 templates** (`skills/drawing-bpmn-flowcharts/templates/`):
  - `bpmn-skeleton.tmpl.xml` — esqueleto XML com 9 namespaces (bpmn, bpmndi, dc, di, xsi, bioc, color, zeebe, camunda) e placeholders
  - `input-schema.tmpl.json` — JSON Schema completo com enum de 30+ tipos BPMN, suporte a `aiAgent` config (model, tools, exitCondition)
  - `descritivo.tmpl.md` — relatório companion com 10 seções (sumário, atividades, gateways, validação de notação, validação de legibilidade, aderência M7, AI agents, issues residuais, observações, como visualizar)
- **2 scripts Python** (stdlib only — sem dependências externas):
  - `compute_auto_layout.py` — recebe input JSON, retorna layout JSON com bounds e waypoints. Implementa o algoritmo determinístico de 7 passos
  - `validate_bpmn_readability.py` — recebe `.bpmn`, retorna `{passed, issues}` JSON com os 5 detectores geométricos. Cohen-Sutherland para edge-crosses-node, colinearidade para overlap, heurística de char-width para label-overflow
- **1 exemplo end-to-end** (`skills/drawing-bpmn-flowcharts/examples/`):
  - `exemplo-onboarding-input.json` — onboarding M7 com 3 lanes (Comercial, Compliance, Operações), 9 nodes, 8 edges, 3 caminhos terminais
  - `exemplo-onboarding.bpmn` — output gerado, validado: passa validação de legibilidade com 0 fails, 1 warning. Cores M7-2026 aplicadas
  - `exemplo-onboarding-descritivo.md` — relatório companion com checklist completo, validação 23 pass / 1 warning / 0 fails

### Changed
- **`plugin.json`** — versão 1.0.0 → 1.1.0, descrição expandida para mencionar BPMN, novas keywords (bpmn, bpmn-2.0, flowchart, auto-layout, camunda, ai-agents, ad-hoc-sub-process)
- **`marketplace.json`** (no marketplace `m7-data`) — entrada do plugin sincronizada com nova versão e descrição
- **`README.md`** — adicionada seção da nova skill `drawing-bpmn-flowcharts`, atualizada estrutura do plugin

### Migration

Não há migração necessária — adição não-breaking. Plugin antigo `mapeamento-processos` (v1.3.2) descontinuado; conhecimento técnico extraído e adaptado para a nova skill com auto-contenção total (zero dependência runtime do plugin antigo).

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
