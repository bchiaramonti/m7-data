# Fase C · Produção dos 4 artefatos

Documento de apoio à [SKILL.md](../SKILL.md). Detalha a Fase C: sequência de geração dos 4 artefatos a partir do BRIEFING, render do PDF e validação final.

## Sumário

1. [Pré-condições](#1-pré-condições)
2. [Sequência rígida](#2-sequência-rígida)
3. [Geração N1 · Cadeia de Valor](#3-geração-n1--cadeia-de-valor)
4. [Geração N2 · Missão do Processo](#4-geração-n2--missão-do-processo)
5. [Geração N3 · Mapa de Interdependência](#5-geração-n3--mapa-de-interdependência)
6. [Geração N4 · Documento Oficial PDF](#6-geração-n4--documento-oficial-pdf)
7. [Validação pós-produção](#7-validação-pós-produção)

---

## 1. Pré-condições

Antes de iniciar a Fase C:

1. **BRIEFING.md está pronto** — Fase A fechada, `validacao.bloqueadores` está vazio (ou exceções registradas em `bloqueadores_aceitos`).
2. **`scripts/check_briefing.py` retornou `ok=true`** — sem bloqueadores não aceitos.
3. **Diretório de trabalho definido** — onde os artefatos serão escritos (ex.: `/tmp/mapeamento-acme/` ou pasta do projeto).
4. **Assets copiados** — `m7-tokens.css`, `m7-header-dark.css`, `fonts/`, `assets/` precisam estar **ao lado dos HTMLs** que vão ser gerados. Ou a skill copia (recomendado para artefatos standalone) ou usa caminhos relativos para a skill.

**Estratégia recomendada**: copiar os assets necessários para o diretório de trabalho do usuário antes de gerar os HTMLs:

```bash
mkdir -p /tmp/mapeamento-acme
cp templates/m7-tokens.css      /tmp/mapeamento-acme/
cp templates/m7-header-dark.css /tmp/mapeamento-acme/
cp templates/m7-print.css       /tmp/mapeamento-acme/   # só se N4-PDF
cp -r templates/fonts           /tmp/mapeamento-acme/
cp -r templates/assets          /tmp/mapeamento-acme/
```

Isso garante que cada HTML carrega seus assets via caminho relativo (`href="m7-tokens.css"`).

---

## 2. Sequência rígida

```
BRIEFING.md
   │
   ├─[1]─▶ N1: cadeia-de-valor-{slug}.html
   │
   ├─[2]─▶ N2: missao-do-processo-{slug}.html       (se em artefatos_a_gerar)
   │
   ├─[3]─▶ N3: mapa-de-interdependencia-{slug}.html (se em artefatos_a_gerar)
   │
   └─[4]─▶ N4: documento-oficial-{slug}.html
            ▼
            scripts/render_pdf.py
            ▼
            documento-oficial-{slug}.pdf
```

**Por que sequencial e não paralelo**:
- N4 precisa dos 3 anteriores prontos (embeda via Jinja).
- Erros são localizáveis (se N3 quebra, N1/N2 já foram entregues).
- Permite invocar [`m7-design-system:reviewing-html-design`](#) entre etapas para QA visual.

**Como decidir o que gerar**: leia `briefing.artefatos_a_gerar`. Só gere o que está listado ali.

**Bloqueio do PDF**: se `n4-pdf` está em `artefatos_a_gerar`, então `n1`, `n2` e `n3` também devem estar (regra PDF-DEPENDENCIA). `check_briefing.py` valida isso automaticamente.

---

## 3. Geração N1 · Cadeia de Valor

**Input**: BRIEFING.md (frontmatter YAML).
**Output**: `cadeia-de-valor-{slug}.html` no diretório de trabalho.

**Passos**:

1. Carregar BRIEFING (parseia frontmatter via `yaml.safe_load`).
2. Selecionar template baseado em `briefing.n1.variante`:
   - `A` → `templates/template-cadeia-de-valor.html`
   - `B` → `templates/template-cadeia-de-valor--linear.html`
3. Substituir placeholders:
   - Header: `{{NOME_DA_EMPRESA}}`, `{{AREA_DOCUMENTO}}`, `{{DATA_REFERENCIA}}`, `{{LEDE_DOCUMENTO}}`, `{{TOTAL_PROCESSOS}}`, `{{N_VERTICAIS}}`, `{{VERSAO_CURTA}}`
   - Lane labels: `{{N_GERENCIAIS}}`, `{{N_PRIMARIOS}}`, `{{N_APOIO}}`
   - Variante A: `{{ROTULO_NUCLEO}}`
   - Para cada processo: `{{NOME_PROCESSO_<código>}}`, `{{LINHA_1_<código>}}`, etc.
4. Aplicar classes CSS:
   - `class="process-box highlight"` se `processo.highlight: true`
   - `class="process-box blue-accent"` se `processo.blue_accent: true`
5. Tabs do header:
   - Se `n2` em `artefatos_a_gerar`: `<a class="tab" href="missao-do-processo-{slug}.html">Missão do processo</a>`
   - Se `n2` ausente: `<div class="tab">Missão do processo</div>` (sem href)
   - Idem para N3.

**Regras de preenchimento**: ver [`n1-cadeia-de-valor.md §5-6`](n1-cadeia-de-valor.md).

**Validação**: ver checklist em [`n1-cadeia-de-valor.md §8`](n1-cadeia-de-valor.md).

---

## 4. Geração N2 · Missão do Processo

**Input**: BRIEFING.md (frontmatter YAML, especialmente `processos[].sipoc`).
**Output**: `missao-do-processo-{slug}.html`.

**Passos**:

1. Carregar BRIEFING.
2. Template: `templates/template-missao-do-processo.html`.
3. **Sidebar**: gerar lista de processos agrupados em Gerenciais / Primários / Apoio. Cada item:
   ```html
   <li data-code="G1"><span class="code">G1</span> Planejamento Estratégico</li>
   ```
4. **Painel SIPOC por processo**: para cada processo com `sipoc` preenchido, gerar bloco:
   ```html
   <article id="G1" class="mp-process-page">
     <h1><span class="code-prefix">G1</span> Planejamento Estratégico</h1>
     <div class="owner">OWNER · CEO · Comitê Estratégico</div>
     <div class="sipoc">
       <div class="sipoc-col">
         <div class="sipoc-label">INPUTS</div>
         <div class="mp-chips">
           <div class="mp-chip">Cenário macro</div>
           ...
         </div>
       </div>
       <div class="sipoc-col mp-mission">
         <div class="sipoc-label">MISSÃO</div>
         <p><span class="verb">Definir</span> o direcionamento estratégico de longo prazo
            <em>para alinhar investimentos, estrutura e cultura às oportunidades</em>.</p>
       </div>
       <div class="sipoc-col">
         <div class="sipoc-label">OUTPUTS</div>
         <div class="mp-chips">
           <div class="mp-chip">Plano estratégico aprovado</div>
           ...
         </div>
       </div>
     </div>
   </article>
   ```
5. **Hash deep-link**: o JS do template já trata `window.location.hash` (`#G1` abre G1). Não precisa adicionar.
6. **Tabs do header**: `Missão do processo` é a tab ativa (`class="tab active"`). N1 e N3 viram links se gerados.

**Regras**: ver [`n2-missao-do-processo.md §3-4`](n2-missao-do-processo.md).

**Validação**: ver checklist em [`n2-missao-do-processo.md §5`](n2-missao-do-processo.md).

---

## 5. Geração N3 · Mapa de Interdependência

**Input**: BRIEFING.md (frontmatter YAML, especialmente `processos[].n3` e `relacoes[]`).
**Output**: `mapa-de-interdependencia-{slug}.html`.

> ⚠ **Aviso crítico**: o template do N3 (`template-mapa-de-interdependencia.html`) vem **pré-preenchido com dados M7 reais** (18 processos, paths SVG, RELATIONS). **Substitua tudo** antes de entregar.

**Passos**:

1. Carregar BRIEFING.
2. Template: `templates/template-mapa-de-interdependencia.html`.
3. **Substituir cada nó**: para cada processo do BRIEFING, gerar:
   ```html
   <div class="node"
        data-layer="{layer-code}"
        data-name="{codigo} · {nome}"
        data-desc="{tooltip primeira linha ou descrição custom}"
        {{ data-friction="true" data-friction-text="..." se is_friction }}
        style="left: {n3.posicao.left}%; top: {n3.posicao.top}%;">{codigo}</div>
   ```
   Mapping de `briefing.n3.coluna` para `data-layer`:
   - `gerencial` → `G`
   - `front` → `P-front`
   - `nucleo-l` ou `nucleo-r` → `P-core`
   - `back` → `P-back`
   - `apoio` → `A`

4. **Substituir paths SVG `.edges`**: para cada relação em `briefing.relacoes`, gerar `<path>` em SVG. **Coordenadas**: viewBox é `1000x600`, então `1% horizontal = 10 unidades`, `1% vertical = 6 unidades`. Para um nó em `left: 44%, top: 22%`, o ponto SVG é `(440, 132)`.

   Curva Bezier suave entre dois nós:
   ```html
   <path class="e-cliente-strong" d="M {x1} {y1} C {x1+50} {y1}, {x2-50} {y2}, {x2} {y2}"/>
   ```

   Mapping de `kind` + `forca` para classe CSS:
   - `kind=cliente, forca=strong` → `e-cliente-strong`
   - `kind=cliente, forca=mid` → `e-cliente-mid`
   - `kind=cliente, forca=soft` → `e-cliente-soft`
   - `kind=info` → `e-info`
   - `kind=decisao` → `e-decisao`

5. **Substituir tabela `RELATIONS`** no JS (final do `<script>`): converte `briefing.relacoes` para o array JS.

6. **Strip do header**: `{{TOTAL_RELACOES}}` = `len(relacoes)`, `{{TOTAL_FRICCOES}}` = count de processos com `is_friction=true`.

7. **Tabs**: `Mapa de interdependência` é a ativa (`data-active="true"`).

**Regras**: ver [`n3-mapa-interdependencia.md §3-4`](n3-mapa-interdependencia.md).

**Validação**: ver checklist em [`n3-mapa-interdependencia.md §5`](n3-mapa-interdependencia.md).

---

## 6. Geração N4 · Documento Oficial PDF

**Pré-condição rígida**: N1, N2 e N3 já gerados no diretório de trabalho. Se faltam, abortar com mensagem clara.

**Input**:
- BRIEFING.md
- `cadeia-de-valor-{slug}.html` (já gerado)
- `missao-do-processo-{slug}.html` (já gerado)
- `mapa-de-interdependencia-{slug}.html` (já gerado)

**Output**:
- `documento-oficial-{slug}.html` (HTML paginado)
- `documento-oficial-{slug}.pdf` (renderizado via Playwright)

**Passos**:

### 6.1 — Gerar HTML paginado

1. Template: `templates/template-documento-oficial.html`.
2. Aplicar `m7-print.css` para regras `@page` + page-break.
3. Estrutura de páginas:
   - **P1**: Capa fullbleed verde-caqui (logo offwhite, título, subtítulo, data, versão).
   - **P2**: Sumário (sem page numbers no MVP).
   - **P3**: Introdução narrativa (objetivo, escopo, metodologia — extraído de `## Objetivo do diagrama`, `## Lede do documento`, `## Contexto da empresa` do BRIEFING).
   - **P4-5**: Seção N1 — texto curto explicativo + diagrama N1 embedado.
   - **P6**: Abertura "Missões dos processos".
   - **P7..N**: Uma página por processo (N2 SIPOC). Headline + Owner + Inputs/Missão/Outputs.
   - **P (N+1)**: Abertura "Mapa de interdependência" (ainda retrato).
   - **P (N+2)**: Mapa neural full-page (LANDSCAPE).
   - **P (N+3)**: Tabela de relações + lista de fricções (LANDSCAPE).
   - **P final**: Encerramento (próximos passos / link para N3+).
4. Footer em todas exceto capa: `página X · {empresa} · {data}` (via `@page @bottom-center { content: counter(page) ... }`).
5. **Embed dos 3 diagramas**: ver [§ 6.2](#62--embed-dos-diagramas).

### 6.2 — Embed dos diagramas

Estratégia: **Jinja2 `{% include %}`** com fragmentos extraídos dos templates N1/N2/N3.

Para cada artefato, extrair só a **região do diagrama** (sem o header full-bleed, sem o footer-note original):

- **N1**: extrair `<div class="chain-container">...</div>` (o bloco das 3 lanes).
- **N2**: para cada processo, extrair `<article id="{codigo}" class="mp-process-page">...</article>` — uma página por processo.
- **N3**: extrair `<div class="neural" id="neural">...</div>` mais o `<script>` que monta o painel info.

Para evitar conflito CSS, namespacing via `body[data-source="n4"]`:
```css
body[data-source="n4"] .chain-container { ... }
body[data-source="n4"] .neural { transform: scale(0.85); }  /* ajuste fit */
```

### 6.3 — Render do PDF

```bash
cd /tmp/mapeamento-acme
python3 /path/to/skills/mapeamento-n1/scripts/render_pdf.py \
    documento-oficial-acme.html \
    documento-oficial-acme.pdf
```

`render_pdf.py` usa **Playwright** (Chromium headless) com `prefer_css_page_size=True` — respeita `@page landscape` em páginas individuais.

Se Playwright/Chromium não disponível, fallback para **WeasyPrint** (com aviso de limitações: named pages CSS limitadas).

Detalhes em [`pdf-generation.md`](pdf-generation.md).

### 6.4 — Validação

Invoca `pdf-validator` (subagent):
- Extrai texto do PDF (via `pdftotext` ou `pdfplumber`)
- Roda checklist:
  - Capa correta (busca por `{empresa.nome}` na primeira página)
  - Sumário lista todas as seções esperadas
  - Sem `{{...}}` no texto extraído (placeholders escaparam?)
  - Mapa neural está em landscape (verifica orientação da página)
  - Footer numerado em todas exceto capa
  - Texto selecionável (não rasterizado)
- Reporta como markdown com ✓/✗ por item.

Detalhes em [`n4-documento-oficial.md`](n4-documento-oficial.md).

---

## 7. Validação pós-produção

Após gerar **todos** os artefatos solicitados, rodar checklist final:

### Por artefato (já listadas em cada reference)
- [ ] N1: ver [`n1-cadeia-de-valor.md §8`](n1-cadeia-de-valor.md)
- [ ] N2: ver [`n2-missao-do-processo.md §5`](n2-missao-do-processo.md)
- [ ] N3: ver [`n3-mapa-interdependencia.md §5`](n3-mapa-interdependencia.md)
- [ ] N4: ver [`n4-documento-oficial.md`](n4-documento-oficial.md) + `pdf-validator`

### Diretório de trabalho
- [ ] Todos os HTMLs e PDF estão no mesmo diretório
- [ ] CSS irmãos (`m7-tokens.css`, `m7-header-dark.css`, `m7-print.css` se N4) presentes
- [ ] `fonts/` e `assets/` presentes
- [ ] Logo carrega em todos os artefatos (testar visualmente)

### Coerência cruzada
- [ ] Tabs do header N1 → N2/N3 funcionam (links válidos)
- [ ] Sidebar do N2 lista exatamente os processos do BRIEFING (mesmos códigos e nomes)
- [ ] Nós do N3 batem com os processos do BRIEFING
- [ ] PDF embute corretamente os 3 diagramas (sem cortes em meio de página)
- [ ] Versão e data são consistentes entre os 4 artefatos

### Performance e tamanho
- [ ] PDF abre em < 3 segundos
- [ ] Tamanho do PDF < 8 MB (ideal < 4 MB)
- [ ] HTMLs carregam em < 1 segundo no browser

---

## Resumo do output esperado

```
{diretorio-de-trabalho}/
├── mapeamento-{slug}.briefing.md          ← SSOT (gerado/refinado em Fase A-B)
├── cadeia-de-valor-{slug}.html            ← N1
├── missao-do-processo-{slug}.html         ← N2 (se solicitado)
├── mapa-de-interdependencia-{slug}.html   ← N3 (se solicitado)
├── documento-oficial-{slug}.html          ← N4 fonte (HTML pré-PDF)
├── documento-oficial-{slug}.pdf           ← N4 final
├── m7-tokens.css                          ← copiado da skill
├── m7-header-dark.css                     ← copiado
├── m7-print.css                           ← copiado se N4
├── fonts/                                 ← copiado
└── assets/                                ← copiado
```
