# Catálogo de Componentes — Política (creating-politica)

> **Princípio**: o MD da Fase 2 é canônico de **conteúdo**, não de design. Toda
> apresentação visual vem de classes CSS pré-definidas no template oficial
> (`assets/politica-m7-template.html`). Quando o autor precisa de um bloco
> visual especial (card, callout, diagrama), usa **shortcodes semânticos**
> deste catálogo — nunca HTML inline ad-hoc ou `<style>` injetado.

## Sintaxe dos shortcodes

Shortcodes seguem o padrão **pandoc fenced divs**:

```markdown
:::nome-do-shortcode
título: Valor opcional
chave: valor

Corpo em markdown padrão (parágrafos, listas, bold, italic, code, links).
:::
```

A skill (script `scripts/generate-html-yaml.py`) parseia o shortcode e o
converte para o HTML correspondente usando **apenas classes CSS já
declaradas no template**. Variáveis em **chave: valor** no topo viram
atributos do markup gerado.

## Regras de uso

1. **Allowlist única** — só os shortcodes listados abaixo são válidos. Tentar
   usar `:::nome-inventado` aborta a Fase 3 com mensagem clara.
2. **Sem HTML inline com classes** — `<div class="...">`, `<span class="...">`,
   `<style>` no MD são rejeitados pela validação. Use shortcodes para
   tudo que não for markdown padrão.
3. **Tokens, nunca hex literal** — qualquer CSS referenciado deve usar
   `var(--vc-*)`, `var(--lime)`, `var(--off-white)`, etc. O catálogo só
   contém classes que já respeitam essa regra.
4. **Estender requer release** — adicionar shortcode novo é breaking change
   menor (entrada no catálogo + classes no template + parser no script +
   exemplo no gold reference + bump de versão).

---

## Shortcodes

### `:::papel-card` — Card vertical narrativo

**Uso semântico**: descrição rica de um papel/processo na seção 6 (Papéis &
Responsabilidades) quando uma tabela de 3 colunas é insuficiente — autor
precisa de subseções narrativas tipo "Por que existe", "O que faz", "Como mede".

**Substitui legacy**: `.inv-card` + `.inv-title` + `.inv-owner` + `.inv-block`
(já existiam no template mas autor escrevia HTML inline).

**Sintaxe MD**:

```markdown
:::papel-card
título: P1 · Geração de Demanda
owner: Head de Marketing

**Por que existe**: ativar pipeline de leads qualificados.

**O que transforma**: demanda latente em oportunidade quente.

**Alimenta**: P2 (Qualificação) com leads scored.
:::
```

**HTML gerado**:

```html
<div class="inv-card">
  <h4 class="inv-title">P1 · Geração de Demanda</h4>
  <p class="inv-owner">Owner: Head de Marketing</p>
  <p class="inv-block"><strong>Por que existe</strong>: ativar pipeline...</p>
  <p class="inv-block"><strong>O que transforma</strong>: demanda...</p>
  <p class="inv-block"><strong>Alimenta</strong>: P2 (Qualificação)...</p>
</div>
```

**Classes utilizadas (já no template)**: `.inv-card`, `.inv-title`, `.inv-owner`, `.inv-block`.

**Quando usar separador de camada**: `:::papel-card-separador` (variante):

```markdown
:::papel-card-separador
título: Camada Primária
descrição: Doze processos que geram receita direta.
:::
```

Gera `<div class="inv-sep"><h4 class="inv-sep-title">...</h4><p class="inv-sep-desc">...</p></div>`.

---

### `:::callout` — Bloco de destaque (3 variantes)

**Uso semântico**: chamar atenção para conceito-chave, alerta ou exemplo
em qualquer seção. Substitui o padrão `.icp-*` ad-hoc que aparecia em
POL-GOV-003 com hex literal.

**Substitui legacy**: `.icp-card`, `.icp-card-title`, `.icp-tag` (injetados
via `<style>` no MD — proibido daqui em diante).

**Variantes**: `info` (default), `alerta`, `exemplo`.

**Sintaxe MD**:

```markdown
:::callout
tag: ICP
título: Investidor Qualificado

Investidor com >R$ 1MM em aplicações financeiras, registrado conforme
Resolução CVM 30.
:::

:::callout-alerta
tag: ATENÇÃO
título: Limitação operacional

A política não autoriza operações em mercados internacionais sem...
:::

:::callout-exemplo
tag: EXEMPLO
título: Aplicação prática

Cliente solicita operação fora do escopo. Procedimento: ...
:::
```

**HTML gerado** (variante info):

```html
<div class="callout">
  <span class="callout-title">
    <span class="callout-tag">ICP</span>
    Investidor Qualificado
  </span>
  <p>Investidor com >R$ 1MM em aplicações financeiras, registrado conforme Resolução CVM 30.</p>
</div>
```

**Classes utilizadas (novas no template)**: `.callout`, `.callout-title`,
`.callout-tag`, `.callout-alerta`, `.callout-exemplo`.

**Tokens**: borda lime (info), âmbar (alerta), verde claro (exemplo). Zero hex literal.

---

### `:::indicador` — Card de indicador de aderência

**Uso semântico**: descrever um indicador de aderência da seção 7 (Governança)
quando a tabela 4-col padrão (Nome / Fórmula / Frequência / Meta) é
insuficiente — por exemplo, fórmulas longas ou metas com múltiplos critérios.

**Quando usar tabela vs card**: até 5 indicadores simples → tabela padrão da
seção 7 (já mapeada em `INDICADOR_N_*`). Indicadores complexos → cards.

**Sintaxe MD**:

```markdown
:::indicador
nome: Aderência à política de exceção
fórmula: (Exceções aprovadas no rito formal / Total de exceções) × 100
frequência: Mensal
meta: ≥ 95%
:::
```

**HTML gerado**:

```html
<div class="indicador-card">
  <h4 class="indicador-nome">Aderência à política de exceção</h4>
  <dl class="indicador-meta">
    <dt>Fórmula:</dt><dd>(Exceções aprovadas no rito formal / Total de exceções) × 100</dd>
    <dt>Frequência:</dt><dd>Mensal</dd>
    <dt>Meta:</dt><dd>≥ 95%</dd>
  </dl>
</div>
```

**Classes utilizadas (novas no template)**: `.indicador-card`, `.indicador-nome`,
`.indicador-meta`.

---

### `:::diagrama` — SVG embebido

**Uso semântico**: incorporar diagrama vetorial inline (cadeia de valor,
fluxograma, hierarquia) em qualquer seção. Substitui o uso ad-hoc de
`<div class="embed-svg"><svg>...</svg></div>` direto no MD.

**Sintaxe MD**:

```markdown
:::diagrama
caption: Fig 1 · Cadeia de Valor M7

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900">
  <!-- conteúdo do SVG -->
</svg>
:::
```

**HTML gerado**:

```html
<div class="embed-svg">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900">
    <!-- conteúdo preservado intacto -->
  </svg>
</div>
<p class="embed-svg-caption">Fig 1 · Cadeia de Valor M7</p>
```

**Classes utilizadas (já no template)**: `.embed-svg`, `.embed-svg-caption`.

**Regra**: SVG inline **só** dentro deste shortcode. Fora dele, o parser
rejeita `<svg>` solto.

---

### `:::processo-grid` — Grid compacto de processos

**Uso semântico**: listar 4+ processos macro em formato grid responsivo
(4 colunas) quando cada um precisa só de título + owner. Caso de uso típico:
listar todos os P1-P12 em seção de "Documentos subordinados".

**Substitui legacy**: `.skill-proc-block`, `.skill-proc-card`, `.skill-proc-title`,
`.skill-proc-owner`, `.skill-camada-sep`, `.skill-camada-title` (autor
escrevia HTML inline — agora é shortcode).

**Sintaxe MD**:

```markdown
:::processo-grid
camada: Camada Primária
descrição: Doze processos que geram receita direta.

- P1 · Geração de Demanda | Head de Marketing
- P2 · Qualificação | Head de Vendas
- P3 · Operação Crédito | Head de Crédito
:::
```

Cada item da lista usa formato `título | owner`, separado por `|`.

**HTML gerado**:

```html
<div class="skill-camada-sep">
  <h4 class="skill-camada-title">Camada Primária</h4>
  <p>Doze processos que geram receita direta.</p>
</div>
<div class="skill-proc-block">
  <div class="skill-proc-card">
    <h4 class="skill-proc-title">P1 · Geração de Demanda</h4>
    <p class="skill-proc-owner">Head de Marketing</p>
  </div>
  <div class="skill-proc-card">
    <h4 class="skill-proc-title">P2 · Qualificação</h4>
    <p class="skill-proc-owner">Head de Vendas</p>
  </div>
  <!-- ... -->
</div>
```

**Classes utilizadas (já no template)**: `.skill-proc-block`,
`.skill-proc-card`, `.skill-proc-title`, `.skill-proc-owner`,
`.skill-camada-sep`, `.skill-camada-title`.

---

## Allowlist de classes CSS no HTML final

Após renderização, **toda classe CSS no HTML deve pertencer a uma destas
categorias**. Classes fora da allowlist são bloqueadas pela validação.

### Classes estruturais do template (sempre presentes)

`.doc`, `.page`, `.page-head`, `.page-body`, `.page-foot`, `.ph-left`,
`.ph-sep`, `.ph-title`, `.ph-meta`, `.pf-classif`, `.pf-page`, `.cover`,
`.cover-title`, `.cover-subtitle`, `.section`, `.section-lede`, `.sub`,
`.subsub`, `.muted`, `.muted-empty`, `.chip`, `.mono`, `.kv-table`,
`.doc-table`, `.principles`, `.principle`, `.principle-card`, `.principle-row`,
`.pn`, `.pt`, `.pd`, `.approval-card`, `.approval-grid`, `.toc`, `.toc-item`,
`.toc-num`, `.toc-title`, `.toc-page`, `.total-pg`.

### Classes de tipografia (m7-tokens.css)

`.text-display-1`, `.text-display-2`, `.text-h1` a `.text-h4`,
`.text-body-1` a `.text-body-3`, `.text-button`, `.text-label`,
`.text-muted`, `.text-mono`, `.section-eyebrow`, `.wcag-pass`,
`.wcag-fail`, `.wcag-marg`.

### Classes navegacionais (m7-tokens.css)

`.m7-nav`, `.m7-nav-inner`, `.m7-nav-logo`, `.m7-nav-links`, `.ds-tag`,
`.m7-foot`, `.m7-foot-inner`, `.container`, `.stack`, `.row`, `.grid`.

### Classes de shortcodes (este catálogo)

- **papel-card**: `.inv-card`, `.inv-title`, `.inv-owner`, `.inv-block`,
  `.inv-sep`, `.inv-sep-title`, `.inv-sep-desc`
- **callout**: `.callout`, `.callout-title`, `.callout-tag`,
  `.callout-alerta`, `.callout-exemplo`
- **indicador**: `.indicador-card`, `.indicador-nome`, `.indicador-meta`
- **diagrama**: `.embed-svg`, `.embed-svg-caption`
- **processo-grid**: `.skill-proc-block`, `.skill-proc-card`,
  `.skill-proc-title`, `.skill-proc-owner`, `.skill-camada-sep`,
  `.skill-camada-title`

### Classes ad-hoc — PROIBIDAS

Qualquer classe que **não** apareça nas categorias acima é rejeitada pela
validação. Exemplos do que **não** é mais aceito:

- `.icp-card`, `.icp-card-title`, `.icp-tag` (POL-GOV-003 legacy) →
  use `:::callout`
- `.user-*`, `.note-*`, `.diagram-*`, `.my-namespace` (prefixos "customizados"
  que o SKILL.md antigo permitia) — **acabou**. Não há mais escape hatch.

---

## Como adicionar um shortcode novo (processo formal)

1. **Abrir issue** descrevendo o caso de uso semântico (não estético).
2. **Definir CSS** em `assets/politica-m7-template.html` usando apenas
   `var(--*)` — zero hex literal.
3. **Adicionar entrada neste catálogo** (sintaxe + HTML gerado +
   classes utilizadas).
4. **Implementar parser** em `scripts/generate-html-yaml.py` na função
   `expand_shortcodes()`.
5. **Atualizar allowlist** acima.
6. **Atualizar gold reference** se faz sentido demonstrar.
7. **Bump** de versão menor do plugin (3.x → 3.(x+1).0).
8. **Smoke test** em `/tmp` antes de commit.
