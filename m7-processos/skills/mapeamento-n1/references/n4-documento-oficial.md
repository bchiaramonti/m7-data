# N4 · Documento Oficial (PDF paginado) — regras detalhadas

Documento de apoio à [SKILL.md](../SKILL.md). Cobre o nível N4: documento HTML/PDF paginado A4 que apresenta a cadeia de valor como artefato oficial M7-2026, embebendo os 3 diagramas anteriores em sequência narrativa.

## Sumário

1. [Objetivo e quando usar](#1-objetivo-e-quando-usar)
2. [Estrutura de páginas](#2-estrutura-de-páginas)
3. [Paginação CSS](#3-paginação-css)
4. [Embed dos diagramas](#4-embed-dos-diagramas)
5. [Checklist de validação](#5-checklist-de-validação)
6. [Anti-padrões](#6-anti-padrões)

---

## 1. Objetivo e quando usar

O N4 é o **documento oficial** que apresenta a cadeia de valor como artefato apresentável: capa, sumário, narrativa, diagramas (N1, N2, N3), encerramento, footer numerado.

Use quando o usuário pedir:
- "PDF da cadeia de valor"
- "Documento oficial / institucional"
- "Apresentar à diretoria"
- "Imprimir a cadeia"
- "Versão executiva paginada"

**Pré-condição**: N1, N2 e N3 já gerados no diretório de trabalho (regra `PDF-DEPENDENCIA` em [`critique-rules.md`](critique-rules.md)).

---

## 2. Estrutura de páginas

Sequência fixa, ordem de leitura natural:

```
P1     CAPA (fullbleed verde-caqui, sem footer)
P2     SUMÁRIO (sem page numbers no MVP)
P3     INTRODUÇÃO (objetivo, contexto, metodologia)
P4-5   N1 CADEIA DE VALOR (retrato + diagrama embedado)
P6     ABERTURA "Missões dos processos"
P7..N  UMA POR PROCESSO (N2 SIPOC)
P N+1  ABERTURA "Mapa de interdependência"
P N+2  N3 MAPA NEURAL (LANDSCAPE)
P N+3  TABELA DE RELAÇÕES + FRICÇÕES (LANDSCAPE)
P M+1  ENCERRAMENTO (próximos passos)
```

### Capa (P1)
- **Fullbleed verde-caqui** (`background: var(--vc-700)`, margem 0)
- Logo offwhite (`assets/m7-logo-offwhite.png`) no topo, height 14mm
- Eyebrow `{AREA} · Documento Oficial` em uppercase + tracking
- Título `Cadeia de valor` em 64pt, com `de valor` em accent lime weight 500
- Subtítulo (lede) em 16pt regular
- 4 meta blocks na base (Empresa, Período, Versão, Processos)
- **Sem footer** (`@page :first { @bottom-center { content: "" } }`)

### Sumário (P2)
- Lista numerada das 5 seções (Introdução, N1, N2, N3, Encerramento)
- Sub-itens da N2 listam contagem por camada (`Gerenciais (4)`, `Primários (9)`, `Apoio (5)`)
- **Sem page numbers no MVP** — melhoria fica para v1.1 (requer JS injection no Playwright)

### Introdução (P3)
- Eyebrow `Documento Oficial · Mapeamento N1`
- Título `Cadeia de Valor {empresa}` com nome em accent lime
- Lede vem de `## Lede do documento` do BRIEFING
- 3 sub-seções numeradas:
  - **01 Objetivo do diagrama** — extraído de `## Objetivo do diagrama`
  - **02 Contexto da empresa** — extraído de `## Contexto da empresa`
  - **03 Metodologia** — texto fixo descrevendo Plan-Extract-Analyze-Interpret-Report

### N1 — Cadeia de Valor (P4-5)
- Eyebrow `N1 · Visão consolidada`
- Título `Cadeia de Valor`
- Lede com contagem de processos
- Diagrama embedado (extraído do `cadeia-de-valor-{slug}.html` via `<div class="chain-container">`)

### Abertura N2 (P6)
- Layout especial: número grande `03` em lime (64pt, weight 200)
- Título `Missão dos processos` (36pt, weight 300)
- Lede curto explicando o formato SIPOC (Inputs → Missão → Outputs)

### Páginas SIPOC (P7..N)
- Uma por processo (apenas processos com `sipoc` preenchido)
- `page-break-before: always` em cada `.process-page`
- Header runner: `03 · Missao · {Camada}` à esquerda, `{Empresa}` à direita
- Headline: `{codigo} {nome}` + tag de camada
- Owner inline (`OWNER · Cargo · Comitê`)
- 3 colunas SIPOC: Inputs (esq, branco) · Missão (centro, verde-caqui escuro) · Outputs (dir, branco)
- Verbo em lime, finalidade em opacity 85%

### Abertura N3 (P N+1)
- Layout idêntico à abertura N2: número grande `04` lime
- Título `Mapa de interdependência`
- Subtítulo informa que próxima página está em landscape

### Mapa neural (P N+2, LANDSCAPE)
- `<section class="page page--landscape">`
- Header runner `04 · Mapa de interdependência`
- Diagrama N3 embedado (extraído via `<div class="neural">`)
- Sem painel info lateral (esse é interativo; em PDF não faz sentido)

### Tabela de relações + Fricções (P N+3, LANDSCAPE)
- Eyebrow `{X} relações · {Y} fricções`
- Tabela de 5 colunas: De · Para · Tipo · Força · O que flui
- Coloração da coluna Tipo:
  - `cliente` → lime weight 500
  - `info` → cinza vc-400
  - `decisao` → cinza vc-300 italic
- Lista de fricções abaixo da tabela: code (vermelho) + descrição

### Encerramento (P M+1, retrato)
- Header `05 · Encerramento`
- Título `Para onde vamos a partir daqui`
- Lede curto sobre próximos níveis (N3 subprocessos, N4 atividades, N5 procedimentos)
- 2 colunas:
  - **Próximos passos sugeridos** (lista de 4 itens)
  - **Notas de iteração** (extraído de `## Notas de iteração` do BRIEFING)

### Footer (em todas exceto capa)
- `@page @bottom-center { content: counter(page) " · {empresa} · {data}" }`
- 9pt, color vc-300

---

## 3. Paginação CSS

Detalhes em [`m7-print.css`](../templates/m7-print.css). Pontos-chave:

### Named pages para orientação
```css
@page          { size: A4 portrait; margin: 18mm 16mm; @bottom-center { ... } }
@page cover    { size: A4 portrait; margin: 0; @bottom-center { content: "" } }
@page toc      { size: A4 portrait; margin: 18mm 16mm; @bottom-center { content: "" } }
@page landscape { size: A4 landscape; margin: 16mm 18mm; @bottom-center { ... } }

.page--cover    { page: cover; }
.page--toc      { page: toc; }
.page--landscape { page: landscape; }
```

### Quebras de página
```css
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
.process-page { page-break-before: always; }
```

### Break-inside protection
```css
.sipoc-bloc, h1, h2, h3, .relations-table tr, .friction-item { break-inside: avoid; }
```

### Modo compacto
Ativado dinamicamente por `render_pdf.py` se `scrollHeight > 1123px`. Reduz padding, gap e font-size em zonas específicas (NÃO altera fonte do conteúdo principal).

---

## 4. Embed dos diagramas

Estratégia: **inline via parsing HTML** (não iframe, não screenshot).

`scripts/build_n4.py` extrai os fragmentos relevantes dos HTMLs N1/N2/N3 já renderizados:
- **N1**: `<div class="chain-container">...</div>` → injetado em `{{N1_DIAGRAMA_EMBEDADO}}`
- **N3**: `<div class="neural">...</div>` (sem `info-panel`) → injetado em `{{N3_DIAGRAMA_EMBEDADO}}`
- **N2**: NÃO embedado direto — `build_n4.py` gera as páginas SIPOC do zero a partir do `processos[].sipoc` do BRIEFING (mais limpo que extrair fragmentos do template N2)

Vantagens vs alternativas:
- ✓ **Texto selecionável** no PDF (vs screenshot rasterizado)
- ✓ **Vetorial** — SVG do mapa preserva qualidade em qualquer zoom (vs PNG embed)
- ✓ **Footprint pequeno** — sem duplicação de assets (vs iframe que carregaria tudo de novo)
- ✓ **Texto pesquisável** — Cmd+F no PDF encontra qualquer label

Desvantagens:
- ✗ Requer namespacing CSS (`body[data-source="n4"]`) para evitar conflito com regras globais
- ✗ Animações CSS (halo de fricção do N3) não funcionam em PDF — esperado, removido por `@media print`

---

## 5. Checklist de validação

### Pré-geração (antes de invocar build_n4.py)
- [ ] BRIEFING tem `n4-pdf` em `artefatos_a_gerar`
- [ ] BRIEFING também tem `n1`, `n2`, `n3` (regra PDF-DEPENDENCIA)
- [ ] N1.html, N2.html, N3.html já existem no diretório de trabalho

### HTML do N4 gerado
- [ ] Nenhum `{{placeholder}}` (busque `{{` no arquivo)
- [ ] BeautifulSoup parseia sem erro
- [ ] `<div class="chain-container">` aparece dentro do `<section class="page">` da N1
- [ ] `<div class="neural">` aparece dentro do `<section class="page page--landscape">` da N3
- [ ] Cada processo do BRIEFING com `sipoc` aparece como `<article class="page process-page">`
- [ ] Tabela de relações tem 1 `<tr>` por relação do BRIEFING
- [ ] Lista de fricções tem 1 `.friction-item` por processo com `is_friction=true`

### PDF renderizado
- [ ] Capa fullbleed verde-caqui sem margem branca
- [ ] Logo offwhite na capa
- [ ] Sumário aparece na P2
- [ ] N1 ocupa 1-2 páginas com diagrama legível
- [ ] Cada processo SIPOC ocupa exatamente 1 página
- [ ] Mapa neural está em landscape (página rotacionada vs anteriores)
- [ ] Tabela de relações também em landscape
- [ ] Footer "página X · {empresa} · {data}" em todas as páginas exceto capa
- [ ] Texto é selecionável (não rasterizado)
- [ ] Tamanho < 8 MB

### Validação automatizada via `pdf-validator`
- [ ] Subagent executa checklist textual + visual
- [ ] Reporta como markdown com ✓/✗ por item

---

## 6. Anti-padrões

- ❌ **Tentar gerar PDF sem N1+N2+N3 prontos** — pre-condição obrigatória.
- ❌ **Embed via iframe** — quebra paginação CSS, conteúdo não pesquisável.
- ❌ **Embed via screenshot PNG** — perde texto selecionável, perde qualidade vetorial.
- ❌ **Page numbers no TOC sem JS injection** — implementação frágil; deixar para v1.1.
- ❌ **Capa com logo dark em vez de offwhite** — fundo é verde-caqui escuro, precisa logo claro.
- ❌ **Footer na capa** — quebra a estética editorial. `@page :first { @bottom-center { content: "" } }`.
- ❌ **Colocar SIPOC em 2 colunas (várias por página)** — perde respiração. 1 processo = 1 página.
- ❌ **Animação do halo de fricção visível em PDF** — está corretamente desabilitada em `@media print`. Confirmar que não voltou.
- ❌ **Mapa neural em retrato comprimido** — perde legibilidade. Use landscape (decisão aprovada).
- ❌ **Substituir TWK Everett por outra fonte no print** — quebra identidade. Manter via `@font-face`.
- ❌ **Editar o N4.html à mão depois de gerado** — alterações ficam no `build_n4.py` ou no template, nunca direto no output.
