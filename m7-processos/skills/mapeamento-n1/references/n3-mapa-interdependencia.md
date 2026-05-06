# N3 · Mapa de Interdependência — regras detalhadas

Documento de apoio à [SKILL.md](../SKILL.md). Cobre o nível N3: blueprint da arquitetura de negócio em **grafo neural feedforward**, mostrando como os processos se conectam, onde passa o cliente, e onde existem fricções.

## Sumário

1. [Objetivo e quando usar](#1-objetivo-e-quando-usar)
2. [Estrutura do template — leitura LTR](#2-estrutura-do-template--leitura-ltr)
3. [Como editar o template](#3-como-editar-o-template)
4. [Taxonomia de arestas e nós](#4-taxonomia-de-arestas-e-nós)
5. [Checklist de validação](#5-checklist-de-validação)
6. [Anti-padrões](#6-anti-padrões)

---

## 1. Objetivo e quando usar

O N3 é o **mapa relacional** da cadeia de valor. Responde:

- *Onde passa o cliente?* (caminho dorsal)
- *Como os processos se alimentam de informação?*
- *Onde compliance e governança atuam?*
- *Onde estão as fricções estruturais?*

Use `template-mapa-de-interdependencia.html` quando o usuário pedir:
- "blueprint da arquitetura de negócio"
- "ver as conexões / interdependências"
- "onde passa o cliente"
- "mapa de processos com fricções"
- "N3 / terceiro nível"

**Pré-requisitos**: a N1 já existe (códigos definidos). Idealmente o N2 também — ajuda a identificar fricções e relações.

---

## 2. Estrutura do template — leitura LTR

```
┌─────────┬─────────┬─────────────────┬─────────┐
│ Gerencial│ Front   │ Núcleo          │ Back-end│
│  G1..Gn │ P1, P2  │ P3..P8          │ P9      │
│ (col 8%)│ (col 26%)│ (col 44%/56%)   │(col 74%)│
├─────────┴─────────┴─────────────────┴─────────┤
│                  Apoio (linha de baixo)        │
│    A1 ── A2 ── A3 ── A4 ── A5  (top: 86-90%)   │
└────────────────────────────────────────────────┘
```

**5 colunas verticais** + uma linha de Apoio na base. Posições em `%` permitem responsividade dentro do canvas SVG-like.

### Componentes principais
- **`.neural`** — canvas (fundo branco com textura de pontos sutis)
- **`.col-label`** — rótulos discretos das colunas no topo (Gerencial / Front-end / Núcleo · verticais / Back-end)
- **`.node`** — círculo absoluto com código (G1, P3...). Label completo só no hover via `data-name`
- **`.edges`** (SVG fullscreen) — todas as conexões em `<path>`, viewBox `1000x600` mapeando 0-100% do canvas
- **`.info-panel`** — painel lateral direito (256px) que preenche descrição + relações + fricção em hover
- **`.legend`** — legenda fixa abaixo do canvas

---

## 3. Como editar o template

> **Aviso crítico**: o template `template-mapa-de-interdependencia.html` vem **pré-preenchido com dados M7** (18 processos, posições, paths SVG, RELATIONS). **Não use o template como vem** — substitua tudo para a empresa-alvo. Se for o caso M7, considere usar o exemplo direto.

### 3.1 — Substituir cada nó

Para cada processo da N1, ajuste o `<div class="node">` correspondente:

```html
<div class="node"
     data-layer="P-core"
     data-name="P3 · Investimentos"
     data-desc="Gestão patrimonial e alocação de carteiras. Ponto de entrada mais comum do cliente PF."
     data-friction="true"
     data-friction-text="Descrição da fricção que aparece no painel."
     style="left: 44%; top: 22%;">P3</div>
```

Atributos:
- **`data-layer`** — define cor do nó. Valores válidos: `G`, `P-front`, `P-core`, `P-back`, `A`
- **`data-name`** — nome completo `Código · Nome` (aparece no hover e no painel)
- **`data-desc`** — descrição 1-2 frases (aparece no painel lateral em hover)
- **`data-friction="true"`** — opcional. Adiciona halo pulsante vermelho.
- **`data-friction-text`** — descrição da fricção (aparece no painel lateral)
- **Conteúdo do `<div>`** — só o código (ex.: `P3`)
- **`style="left: X%; top: Y%;"`** — posição absoluta dentro do canvas

### 3.2 — Posições das colunas (referência)

| Coluna | `left` |
|---|---|
| Gerencial | `8%` |
| Front-end | `26%` |
| Núcleo (esquerda) | `44%` |
| Núcleo (direita) | `56%` |
| Back-end | `74%` |
| Apoio (linha de baixo) | distribuir entre `18%` e `90%`, todos em `top: 86%` ou `90%` |

### 3.3 — Editar arestas (SVG paths)

O SVG `.edges` tem `viewBox="0 0 1000 600"` — então `1% horizontal = 10 unidades`, `1% vertical = 6 unidades`.

Para um nó em `left: 44%; top: 22%`, o ponto correspondente no SVG é `(440, 132)`.

Cada `<path>` tem uma das classes:

| Classe | Tipo | Estilo visual |
|---|---|---|
| `e-cliente-strong` | Fluxo de cliente forte | Lime sólido, espessura 3px, opacidade 0.9 |
| `e-cliente-mid` | Fluxo de cliente médio | Lime sólido, espessura 1.8px, opacidade 0.7 |
| `e-cliente-soft` | Fluxo de cliente fraco / cross-sell | Lime sólido, espessura 1.1px, opacidade 0.5 |
| `e-info` | Informação / dados | Cinza fino, espessura 0.8px, opacidade 0.55 |
| `e-decisao` | Governança / compliance | Cinza tracejado, espessura 0.9px |

**Use Bezier `C` para curvas suaves**:
```html
<path class="e-cliente-strong" d="M 260 204 C 260 280, 260 280, 260 336"/>
                                     ^                                     ^
                                     ponto inicial                ponto final
```

**Ordem dos paths importa**: paths no final do SVG ficam por cima. Coloque a espinha dorsal (cliente forte) por último para destacar.

### 3.4 — Editar a tabela `RELATIONS` no JS

No final do `<script>`, há uma constante:

```javascript
const RELATIONS = [
  { from: 'P1', to: 'P2', kind: 'cliente', label: 'Lead qualificado' },
  { from: 'A1', to: 'P3', kind: 'info', label: 'Dados de cliente e BI' },
  { from: 'G3', to: 'P5', kind: 'decisao', label: 'Aderência regulatória' },
  // ...
];
```

Cada item:
- **`from`** / **`to`** — códigos dos processos (devem existir como `<div class="node">`)
- **`kind`** — `'cliente' | 'info' | 'decisao'` (mesma taxonomia das classes de aresta)
- **`label`** — descrição curta (3-6 palavras) do que flui

Essa tabela é o que aparece no painel lateral ("Recebe de" / "Entrega para") em hover. **Cada path SVG deve ter um item correspondente em RELATIONS** — caso contrário o painel ignora visualmente a aresta.

### 3.5 — Identificar fricções

Critérios para marcar um nó como `data-friction="true"`:
- **Handoff problemático** — perde leads/dados/contexto entre processos
- **Loop quebrado** — não retorna sinal para o processo upstream
- **Dados fragmentados** — múltiplas fontes de verdade
- **Dependência não declarada** — processo precisa de input que ninguém formaliza

Limite saudável: **2 a 4 fricções** num mapa de 15-20 processos. Mais que isso vira ruído visual; o halo pulsante perde força.

### 3.6 — Header e strip

Placeholders no header:
- `{{NOME_DA_EMPRESA}}`, `{{AREA_DOCUMENTO}}`, `{{DATA_REFERENCIA}}` — iguais ao N1
- `{{TOTAL_RELACOES}}` — total de items em `RELATIONS`
- `{{TOTAL_FRICCOES}}` — quantos nós com `data-friction="true"`
- `{{VERSAO_CURTA}}`

Footer:
- `{{DATA_REVISAO}}`, `{{OWNER_DIAGRAMA}}`

---

## 4. Taxonomia de arestas e nós

### 4.1 — Tipos de aresta (kind em RELATIONS)

| Kind | Quando usar | Exemplos |
|---|---|---|
| `cliente` | O cliente (ou pedido do cliente, ou lead) **passa fisicamente** entre processos | Lead `P1 → P2`, cliente onboarded `P2 → P3` |
| `info` | Dados, KPIs, metas, sinais — sem cliente atravessando | KRs `G2 → P4`, dados de CRM `A1 → P3` |
| `decisao` | Governança, autorização, compliance — gate ou veto | Compliance `G3 → P5`, auditoria `G2 → P9` |

**Regra**: cada par `(from, to)` tem **um kind dominante**. Se há fluxo de cliente E informação entre os mesmos processos, use `cliente` (mais forte) e não duplique.

### 4.2 — Cores e tamanhos por camada

| `data-layer` | Cor de fundo | Borda | Tamanho |
|---|---|---|---|
| `G` | verde-caqui escuro | mesma cor | 30×30px, fonte 9.5px |
| `P-front` | off-white | lime sólida 2px | 32×32px |
| `P-core` | lime sólido | verde-caqui escuro | 38×38px (maior — é o coração) |
| `P-back` | off-white | lime sólida 2px | 32×32px |
| `A` | branco | verde-claro tracejado | 32×32px |

O **núcleo (`P-core`) é maior** intencionalmente — é o coração da operação. Não troque o tamanho.

### 4.3 — Espessura encoda volume de cliente

Reserve `e-cliente-strong` para **a espinha dorsal** (caminho principal de cliente). Tipicamente:
- Geração → Aquisição → Vertical principal → Customer Success

`e-cliente-mid` para fluxos importantes mas não principais (cross-sell entre verticais núcleo).

`e-cliente-soft` para fluxos de baixo volume ou loops (retenção, expansão).

---

## 5. Checklist de validação

Antes de entregar, confirmar:

- [ ] **Todos os processos da N1 estão presentes** como `<div class="node">`. Não esconda nenhum.
- [ ] **Cada nó tem `data-name`, `data-desc`** preenchidos (não placeholders).
- [ ] **Posições % não se sobrepõem** — nós em ` left: X%; top: Y%` afastados ≥ 4-6% para não colidir visualmente.
- [ ] **Cada path SVG tem um item correspondente em RELATIONS** (mesmos `from` e `to`).
- [ ] **`from` e `to` em RELATIONS existem como nós** — sem typo. Use o código exato.
- [ ] **2-4 fricções no máximo** — mais que isso satura o visual.
- [ ] **Cada fricção tem `data-friction-text`** preenchido.
- [ ] **Placeholders zerados** — `{{NOME_DA_EMPRESA}}`, `{{TOTAL_RELACOES}}`, etc.
- [ ] **Tab `Mapa de interdependência`** está com `data-active="true"`. Outras tabs apontam para os arquivos N1 e N2 (se existirem).
- [ ] **Animação do halo de fricção** funciona (verifique abrindo no browser; o halo pulsa).
- [ ] **Hover preenche o painel lateral** com descrição + recebe-de/entrega-para + (se houver) fricção.
- [ ] **Espinha dorsal de cliente** existe e usa `e-cliente-strong`.
- [ ] **Núcleo (`P-core`) está maior** — não trocou para outro tamanho.

---

## 6. Anti-padrões

- ❌ **Usar o template como vem** — ele tem dados M7 reais. Substitua todos os nós, posições e paths antes de entregar.

- ❌ **Múltiplos kinds entre os mesmos dois nós** — visualmente bagunça. Escolha o kind dominante (`cliente` > `decisao` > `info`).

- ❌ **Mais de 30 paths SVG** — densidade excessiva torna o mapa ilegível. Limite a **relações fortes/significativas** (~20-25 paths para 15-20 processos é saudável).

- ❌ **Mais de 4 fricções** — perde força semântica. Se há mais, repriorize ou agrupe na descrição.

- ❌ **Nós colidindo** — `left/top` muito próximos. Reposicione com ≥4-6% de gap.

- ❌ **Espessura uniforme em todas as arestas** — quebra a métrica visual de "volume de cliente". Use as 5 classes (cliente-strong/mid/soft, info, decisao) diferenciadamente.

- ❌ **Mudar o tamanho do núcleo** — `P-core` é maior por design (coração). Não normalize.

- ❌ **Adicionar legendas inline ao lado dos nós** — informação vai no hover (data-name) ou no painel lateral. Mapa neural fica limpo.

- ❌ **Adicionar setas (markers) nas arestas** — o template não usa setas; direção é implícita pelo grafo (entrada à esquerda, saída à direita). Não adicione `<defs><marker>`.

- ❌ **Trocar a textura de pontos do fundo (`.neural::before`)** — é o que dá a sensação de "espaço neural". Manter.

- ❌ **Remover a animação do halo** — `friction-pulse` chama atenção para a fricção. Manter (exceto em print, já tratado por `@media print`).
