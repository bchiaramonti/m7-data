# Design System M7-2026 — guia para artefatos N1/N2/N3

Documento de apoio à [SKILL.md](../SKILL.md). Cobre tokens, tipografia, cores, e anti-padrões visuais comuns aos três artefatos.

## Sumário

1. [Filosofia visual](#1-filosofia-visual)
2. [Tipografia](#2-tipografia)
3. [Paleta de cores](#3-paleta-de-cores)
4. [Tokens disponíveis](#4-tokens-disponíveis)
5. [Componentes do header escuro](#5-componentes-do-header-escuro)
6. [Espaçamento e raios](#6-espaçamento-e-raios)
7. [Sombra e transição](#7-sombra-e-transição)
8. [Anti-padrões visuais](#8-anti-padrões-visuais)

---

## 1. Filosofia visual

M7-2026 é **editorial, não corporativo**. Privilegia:

- Tipografia clara e hierárquica
- Bastante off-white respirando entre elementos
- Verde-caqui como cor "âncora" (séria, estável)
- Lime como **único** accent — usado com parcimônia (foco, hover, accent de título)
- **Zero gradientes inventados, zero ícones decorativos, zero emojis**
- Sombras são sutis (`shadow-sm` quase sempre)
- Tudo carregado pelo `m7-tokens.css` (não duplique tokens em CSS local)

A vibe: documento técnico bem composto, não slide de PowerPoint.

---

## 2. Tipografia

### Família
- **TWK Everett** (carregada via `@font-face` no `m7-tokens.css`)
- 6 pesos disponíveis: `200` (Ultralight), `300` (Light + LightItalic), `400` (Regular), `500` (Medium), `700` (Bold)
- **Fallback**: Arial (com ajustes `ascent-override`, `descent-override` para casar métricas)

### Regra de peso
- Headings (h1, h2, h3): **400 (Regular)** — TWK Everett tem desenho próprio que dispensa bold
- Texto corrido: **400 (Regular)**
- Labels uppercase: **500 (Medium)**
- Códigos em mono (G1, P3, etc.): peso bold no `.process-box .code`, peso 600 nos nós do mapa
- **Nunca use 700 (Bold) em headings** — quebra a estética do M7

### Escala (do `m7-tokens.css`)
```
display-1   → 4.5rem  / 1.05 / -0.02em
display-2   → 3.5rem  / 1.08 / -0.015em
h1          → 3rem    / 1.1  / -0.01em
h2          → 2.5rem  / 1.15 / -0.005em
h3          → 2rem    / 1.2
h4          → 1.5rem  / 1.25
body-3      → 1.125rem / 1.55
body-1      → 1rem    / 1.5
body-2      → 0.875rem / 1.45
button      → 1rem (uppercase, 1.25px tracking)
label       → 0.75rem (uppercase, 0.08em tracking, 500)
muted       → 0.875rem opacity 0.7
mono        → 0.8125rem (ui-monospace)
```

Use as classes `.text-h1`, `.text-body-2`, etc. quando puder. Nos templates dos artefatos, alguns headers usam tamanhos custom (ex.: 32px no `m7-header-dark .h-e h1`) — mantém os valores do template, **não inventa novos**.

---

## 3. Paleta de cores

### Cores principais
| Token | Hex | Uso |
|---|---|---|
| `--off-white` | `#fffdef` | Background da página (warm white, **não** branco frio) |
| `--verde-caqui` / `--vc-500` | `#424135` | Cor primária — texto principal, fundo de lane labels |
| `--lime` | `#eef77c` | Accent — usado com parcimônia (foco, hover, accent de título no header) |
| `--white` | `#ffffff` | Fundo de cards (process boxes), painéis |
| `--black` | `#000000` | Quase nunca usado; preferir `--vc-500` |

### Escala verde-caqui (10 tons)
| Token | Hex | Uso típico |
|---|---|---|
| `--vc-50` | `#f6f6f5` | Hover muito sutil, chips claros |
| `--vc-100` | `#d0d0cc` | Bordas (process boxes, painéis, footer) |
| `--vc-200` | `#aeada8` | Texto auxiliar muito sutil |
| `--vc-300` | `#8a8981` | Texto desabilitado, labels secundárias |
| `--vc-400` | `#66655b` | Texto secundário (`.subtitle`, footer notes) |
| `--vc-500` | `#424135` | **Cor primária** — texto principal, lane label background |
| `--vc-600` | `#35342a` | Variante mais escura |
| `--vc-700` | `#28271f` | Header dark background |
| `--vc-800` | `#1a1a15` | Quase nunca usado |
| `--vc-900` | `#0d0d0a` | Quase nunca usado |

### Escala off-white (10 tons)
| Token | Hex | Uso |
|---|---|---|
| `--ow-500` | `#fffdef` | Default body bg (= `--off-white`) |
| `--ow-700` | `#99978e` | Texto sobre fundo escuro (header dark) |

### Cores aliases (alias do verde caqui)
- `--verde-medio` = `#4f4e3c`
- `--verde-claro` = `#79755c` (texto secundário)
- `--verde-escuro` = `#2d2d24`

### Status (use só nos artefatos onde já está pré-codado)
| Token | Hex | Uso |
|---|---|---|
| `--success-text` | `#006600` | Texto verde WCAG-safe |
| `--warning-text` | `#8a6d00` | Texto amarelo WCAG-safe |
| `--error-text` | `#b8000f` | Texto vermelho WCAG-safe |
| `--info-text` | `#004db3` | Texto azul WCAG-safe |
| `--info` | `#0066ff` | Borda do `.process-box.blue-accent` (cross-sell/tech) |

### Cores derivadas dos templates (definidas localmente)
| Variável | Valor | Uso |
|---|---|---|
| `--lime-soft` | `rgba(238, 247, 124, 0.15)` | Fundo de `.highlight`, halo do hover |
| `--lime-glow` | `rgba(238, 247, 124, 0.25)` | Glow mais forte (uso eventual) |
| Vermelho de fricção | `rgba(200, 75, 60, 0.x)` | Halo pulsante no mapa N3 (não tem token oficial — definido inline no template) |

---

## 4. Tokens disponíveis

Todos os tokens vêm de `m7-tokens.css`. **Nunca redefina**:

```css
/* ❌ Não faça isto */
:root {
  --off-white: #faf9f6; /* errado, redefiniu */
}

/* ✅ Faça isto */
.minha-classe {
  background: var(--off-white); /* usa o token */
}
```

Se precisa de uma variante local (ex.: `--lime-soft` que não existe nos tokens oficiais), defina no `:root` do **próprio template** (como o N1 já faz). Não toque em `m7-tokens.css`.

---

## 5. Componentes do header escuro

`m7-header-dark.css` define o header escuro full-bleed usado em N1/N2/N3:

```html
<div class="m7-header-dark">
  <div class="doc-meta">
    <img src="assets/m7-logo-offwhite.png" alt="...">
    <div class="meta">
      <span>{{AREA_DOCUMENTO}}</span><span class="dot"></span>
      <span>Documento N1</span><span class="dot"></span>
      <span>{{DATA_REFERENCIA}}</span>
    </div>
  </div>
  <div class="h-e">
    <div class="body">
      <div>
        <h1>Cadeia <span class="accent">de valor</span></h1>
        <p class="lede">{{LEDE_DOCUMENTO}}</p>
      </div>
      <div class="strip">
        <div class="cell"><div class="v">18</div><div class="l">Processos</div></div>
        ...
      </div>
    </div>
    <div class="tabs">
      <div class="tab active">Visão geral <span class="num">N1</span></div>
      <a class="tab" href="...">Missão do processo</a>
      <a class="tab" href="...">Mapa de interdependência</a>
    </div>
  </div>
</div>
```

Características:
- **Full-bleed**: o `margin: -32px -32px 24px` neutraliza o padding do body
- **Logo offwhite**: usa `assets/m7-logo-offwhite.png` (logo claro sobre fundo escuro)
- **`<span class="accent">`** — destaque lime no título principal
- **`<span class="num">`** ao lado da tab ativa — pill com número do nível (N1)
- **`<span class="dot"></span>`** — separador visual entre items do meta strip

**Não personalize** o `m7-header-dark.css` para a empresa-alvo. Apenas troque o logo (`assets/`) se necessário.

---

## 6. Espaçamento e raios

### Raios de borda (do `m7-tokens.css`)
| Token | Valor |
|---|---|
| `--radius-md` | `0.375rem` (6px) |
| `--radius-lg` | `0.5rem` (8px) |
| `--radius-xl` | `0.75rem` (12px) |
| `--radius-2xl` | `1rem` (16px) |
| `--radius-3xl` | `1.5rem` (24px) |

Templates usam `--radius: 12px` e `--radius-sm: 8px` localmente. Mantém.

### Padding canônico
- Body: `padding: 32px` (em N1/N2/N3 desktop)
- Process box: `padding: 16px`
- Lane content: `padding: 16px 24px`
- Cells do strip: `padding: 12px 20px`

### Container max-width
- N1/N2/N3 usam `max-width: 1280px; margin: 0 auto`. Mantém.

---

## 7. Sombra e transição

### Sombras
| Token | Valor |
|---|---|
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1)` |
| `--shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)` |
| `--shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)` |
| `--shadow-xl` | `0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1)` |
| `--shadow-2xl` | `0 25px 50px -12px rgba(0,0,0,0.25)` |

Use `--shadow-sm` para cards (process boxes), `--shadow-lg` para tooltips. Nada mais é usado nos artefatos atuais.

### Transição padrão
- `--t: 0.2s cubic-bezier(0.4, 0, 0.2, 1)`
- Templates usam `--transition: 0.15s cubic-bezier(0.4, 0, 0.2, 1)` localmente. Mantém os 0.15s para sentir mais ágil.

---

## 8. Anti-padrões visuais

- ❌ **Usar branco frio (`#ffffff`) como background da página** — o M7-2026 é warm. Sempre `--off-white` (`#fffdef`).

- ❌ **Adicionar gradientes inventados** — só os já presentes no canvas do mapa N3 (radial-gradients sutis no `.neural`). Em qualquer outro lugar, gradiente quebra a estética.

- ❌ **Usar lime para texto corrido** — lime é accent. Usado em: `.accent` no título do header, `.highlight` em process box (foco estratégico), borda do hover, accent na missão SIPOC (`<span class="verb">`). Nada além disso.

- ❌ **Adicionar ícones decorativos (Material, FontAwesome, emojis)** — N1/N2/N3 são tipográficos. O único ícone aceito é o SVG inline do `flow-arrow` no N1 (já no template).

- ❌ **Adicionar logos de terceiros (verticais, parceiros)** — só logo da empresa-alvo no header. Mais que isso vira "slide de partnership".

- ❌ **Trocar a fonte por outra mesmo que pareça similar** (Inter, Helvetica, Manrope) — TWK Everett é a fonte M7. Se faltar a OTF, o fallback é Arial via `@font-face` Fallback.

- ❌ **Usar Bold (700) em headings** — peso 400 (Regular) em headings é assinatura do M7-2026.

- ❌ **Reduzir o `padding: 32px` do body** — comprime visualmente. Mantém os 32px desktop.

- ❌ **Adicionar sombras pesadas (`shadow-2xl`) em process boxes** — perde a sobriedade. `shadow-sm` ou nenhuma.

- ❌ **Aumentar o tamanho do logo no header** — `height: 28px` no doc-meta é proposital. O logo é assinatura discreta, não brand statement.

- ❌ **Centralizar tudo** — labels uppercase ficam alinhados à esquerda. Centralização é pontual (lane labels, verticais-label do núcleo).

- ❌ **Adicionar background ao body fora do off-white** — quebra a hierarquia. Se precisar de seção destacada, use `.lane-content` (branco) ou um card com fundo `--vc-500` (raro).
