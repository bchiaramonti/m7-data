# Regras de Design — Política M7 (8 dimensões)

> Documento canônico que o agente `politica-design-reviewer` usa como gabarito
> para comparar cada HTML gerado. Específico para o artefato **Política (POL)**
> — herda o design system M7-2026 mas adiciona 2 dimensões próprias
> (paginação A4 + estrutura 8 seções) e remove o que não se aplica a este
> formato (hero overlays, dashboards).

## Conformidade base — M7-2026

Toda política gerada deve respeitar **integralmente** os tokens declarados em
`assets/m7-tokens.css`:

| Token | Valor canônico |
|-------|----------------|
| Fonte | TWK Everett (200/300/400/500/700) |
| Primária | `var(--verde-caqui)` = `#424135` |
| Accent | `var(--lime)` = `#eef77c` (decorativo, nunca texto) |
| Surface | `var(--off-white)` = `#fffdef` (quente, nunca `#FAF9F6`) |
| Escala VC | `--vc-50` a `--vc-900` |
| Escala OW | `--ow-50` a `--ow-900` |

**Regra dura**: o HTML gerado pelo script **não pode conter hex literal**
para essas cores. Toda referência a `#424135`, `#fffdef`, `#eef77c` ou tons
da escala deve aparecer como `var(--vc-500)`, `var(--off-white)`, etc.
Hex literal só é tolerado em status (Success/Warning/Error/Info quando
necessário) e em escalas semânticas não-cobertas pelos tokens (ex.: âmbar
do `.callout-alerta` que vive no template).

---

## 8 dimensões de revisão

### Dimensão 1 — Paleta de cores

**Verifica:**
- Todas as cores principais via `var(--*)`. Zero hex literal para verde caqui,
  lime, off-white ou tons da escala.
- Off-white **quente** (`#fffdef`). Nunca `#FAF9F6`, `#FFFFFF`, `#FAFAFA`.
- Accent (lime) **nunca em texto** — só borda, fundo translúcido, badge decorativo.
- Status neon (`#00ff00`, `#ffff00`) **nunca em texto** — usa variantes `-text`
  (`#006600`, `#8a6d00`, `#b8000f`, `#004db3`).

**Contraste mínimo (WCAG AA):**

| Elemento | Razão mínima |
|----------|--------------|
| Texto normal (< 18px) | 4.5:1 |
| Texto grande (≥ 18px) | 3:1 |
| Componentes UI | 3:1 |

**Falhas conhecidas a flaggar como CRITICO:**
- `#eef77c` em `#fffdef` = 1.1:1 — sempre falha.
- `#79755c` em `#fffdef` = 4.2:1 — marginal (só texto ≥18px).
- Hex literal de `#424135` em CSS injetado pelo MD (caso POL-GOV-003).

### Dimensão 2 — Tipografia

**Verifica:**
- Font-family em headings e body: `var(--font-sans)` (= `"twkEverett", ...`).
- Headings (h1–h4): `font-weight: 400` (Regular). **Nunca** Bold/700.
- Bold reservado para BANs, métricas, valores em destaque.
- Eyebrow/label: `weight: 500`, `letter-spacing: 0.08em`, `text-transform: uppercase`.
- Line-height ≥ 1.5 em body text.
- `@font-face` TWK Everett presente (HTML autocontido → base64).
- Hierarquia visual: h1 > h2 > h3 > h4 > body. Nunca um heading menor que body.

**Escalas canônicas** (devem aparecer no CSS injetado):

```css
.text-h1 { font-size: 3rem;     font-weight: 400; line-height: 1.1; }
.text-h2 { font-size: 2.5rem;   font-weight: 400; line-height: 1.15; }
.text-h3 { font-size: 2rem;     font-weight: 400; line-height: 1.2; }
.text-h4 { font-size: 1.5rem;   font-weight: 400; line-height: 1.25; }
```

No template específico de política (impressão A4) o tamanho efetivo é
reduzido (10-13px em headings, 9-11px em body) mas o **peso e a fonte**
seguem a regra.

**Falhas a flaggar como CRITICO:**
- Heading com `font-weight: 700` ou `bold`.
- Eyebrow sem letter-spacing 0.08em.
- Mistura de famílias (Arial mixed com TWK Everett sem fallback declarado).

### Dimensão 3 — Espaçamento

**Grid 8px** (ou subdivisões reconhecidas):

```
4px → 6px → 8px → 10px → 12px → 14px → 16px → 24px → 32px → 48px → 64px → 96px
```

(Política aceita 6/10/14 como subdivisões intermediárias para imprimir em
formato A4, onde 8px puro vira muito largo.)

**Verifica:**
- Padding interno ≤ gap externo (cards não "explodem" o container).
- Padding responsivo: `12px → 16px (≥640px) → 24px (≥1024px)` em containers.
- Espaçamento entre seções coerente (não 8px aqui, 20px ali, 13px lá).
- Margin em cards seguindo escala (não valores aleatórios como `7px`, `11px`).

**Falhas a flaggar:**
- Valores fora da escala (`margin: 7px`, `padding: 11px 13px`).
- `padding: 0` em containers visíveis (texto colado na borda).

### Dimensão 4 — Proporções

**Verifica:**
- SVG **obrigatoriamente** com `viewBox`. Width/height absolutos sem viewBox = falha.
- Página A4: aspect ratio `1:1.4142` (210mm × 297mm). O `.page` no template
  já está definido — não alterar.
- Cards seguindo proporções harmônicas (golden 1.618:1 ou 3:2 quando possível).
- Containers com `max-width` declarado (não estiquem em telas largas).

**Específico de política:**
- 16 páginas A4 fixas (Capa, Controle, 8 seções, Versões, Aprovações, etc.).
- Cada `.page` tem altura útil `~960px` para conteúdo (descontando header/footer).

### Dimensão 5 — Layout & componentes

**Verifica:**
- Toda classe CSS no HTML pertence à allowlist do `component-catalog.md`.
- Sem `<style>` injetado fora do bloco principal do template (= zero `<style>`
  extras além do que o `inline_assets()` produz a partir de `m7-tokens.css`).
- Sem `style="..."` inline (atributo `style` em qualquer elemento é falha).
- Componentes oficiais do template intactos: `.page`, `.page-head`, `.page-foot`,
  `.cover`, `.cover-title`, `.section`, `.principle`, etc.
- Shortcodes do catálogo gerando o HTML correto (papel-card → `.inv-card`,
  callout → `.callout`, etc.).

**Falhas a flaggar como CRITICO:**
- `<style>` adicional injetado pelo autor (sinal de leak — caso POL-GOV-003).
- Classes ad-hoc tipo `.icp-*`, `.user-*`, `.my-card`.
- `style="color: ..."` em qualquer elemento.

### Dimensão 6 — Acessibilidade

**Verifica:**
- Contraste WCAG AA em todo texto (ver Dimensão 1).
- Lime/neon nunca em texto.
- `<img>` tem `alt` (`assets/m7-logo-*.png` inlinados base64 mantêm o alt).
- Touch targets em links/botões ≥ 44×44px (raros em política, mas se houver).
- Status nunca só por cor — sempre ícone ou label textual.
- Font size em body ≥ 9px (mínimo absoluto para impressão A4).

### Dimensão 7 — Paginação A4 (específico de política)

**Verifica:**
- HTML contém exatamente as 16 páginas oficiais do template (ordem
  invariante): Capa → Controle → Sumário → Objetivo → Escopo → Definições
  → Princípios → Diretrizes → Papéis → Governança → Disposições → Versões
  → Aprovações → Anexos → Vigência → Próximas revisões.
- Cada `.page` tem `data-page-label` correto.
- Cada `.page` tem `<header class="page-head">` + `<div class="page-body">`
  + `<footer class="page-foot">`.
- `page-break-inside: avoid` em cards e tabelas curtas.
- Quebra de Diretrizes (`<!-- /page-break -->` no MD) preserva continuidade
  de header/footer entre páginas.
- Auto-numeração via JS (`{{TOTAL_PAGINAS}}` substituído + `.total-pg`
  atualizado).

**Falhas a flaggar como CRITICO:**
- Página faltando ou em ordem trocada.
- `.page-body` com altura excedendo ~960px (texto cortado por
  `overflow: hidden`).
- Chunk de Diretrizes estimado em >900px sem page-break (warning do
  script vira issue se ignorado).

### Dimensão 8 — Estrutura das 8 seções (específico de política)

**Verifica:**
- h2 numerados de 1 a 8 na ordem canônica.
- Cada seção com conteúdo mínimo:

| Seção | Conteúdo mínimo |
|-------|-----------------|
| 1. Objetivo | Pelo menos 1 parágrafo |
| 2. Escopo | LEDE + ao menos 1 inclusão (excluções opcionais) |
| 3. Definições | Ao menos 3 linhas na tabela |
| 4. Princípios | Ao menos 3 princípios |
| 5. Diretrizes | LEDE + sumário + conteúdo |
| 6. Papéis | Ao menos 3 linhas (Estratégico, Tático, Operacional) |
| 7. Governança | Revisão periódica + indicadores + escalação |
| 8. Disposições | Vigência + ao menos 1 doc relacionado |

- Slot limits respeitados (12 defs, 7 princípios, 8 papéis, 5 indicadores,
  6 exceções, 10 docs relacionados).
- Slots vazios removidos pelo cleanup (zero `<div class="principle">` com
  body em branco, zero `<tr>` com `<strong></strong>` vazio).
- Quando `governance.parent: null` → renderiza "N/A · Política raiz".

**Falhas a flaggar como CRITICO:**
- Seção faltando (h2 ausente).
- Slot vazio que escapou do cleanup (princípio sem título, papel sem nome).
- Tabela DOC_REL com zero linhas e sem fallback row.

---

## Score e veredito

| Score | Critério | Veredito |
|-------|----------|----------|
| **A** | Zero CRITICO, ≤ 2 ATENCAO | APROVADO |
| **B** | Zero CRITICO, 3-5 ATENCAO | APROVADO COM RESSALVAS |
| **C** | 1+ CRITICO ou 6+ ATENCAO | REPROVADO |
| **D** | Violação grave (off-brand, página faltando) | REPROVADO |

**Gate da Fase 3**: a skill só entrega o trio (.html + .yaml + .review.md)
se Score ∈ {A, B}. Score C/D bloqueia e exige correção no MD/BRIEFING +
re-execução do script.

---

## Comparação com gold reference

O agente sempre compara o HTML em revisão contra o gold reference em
`references/reference-output/POL-GOV-001-gold.html`. Verifica especialmente:

1. **Header/footer**: estrutura idêntica (logo, separador, código, classificação).
2. **Capa**: composição do título (linha 1 + acento + sufixo) seguindo o
   padrão visual.
3. **Tipografia**: hierarquia h1/h2/h3/h4 com mesmos tamanhos relativos.
4. **Espaçamento entre seções**: ritmo consistente.
5. **Cards e tabelas**: bordas, sombras e cores conforme o gold.

Divergências significativas (não causadas por conteúdo diferente) viram
ATENCAO ou CRITICO conforme severidade.
