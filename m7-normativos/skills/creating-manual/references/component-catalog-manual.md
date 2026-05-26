# Catálogo de Componentes — Manual (creating-manual)

> **Princípio**: o MD da Fase 2 é canônico de **conteúdo**, não de design. Toda
> apresentação visual vem de classes CSS pré-definidas no template oficial
> (`assets/manual-m7-template.html`). Quando o autor precisa de um bloco
> visual especial (card, callout, diagrama, RACI), usa **shortcodes semânticos**
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
declaradas no template**.

## Regras de uso

1. **Allowlist única** — só os shortcodes listados abaixo são válidos. Tentar
   usar `:::nome-inventado` aborta a Fase 3 com mensagem clara.
2. **Sem HTML inline com classes** — `<div class="...">`, `<span class="...">`,
   `<style>` no MD são rejeitados pela validação. Use shortcodes para
   tudo que não for markdown padrão.
3. **Tokens, nunca hex literal** — qualquer CSS referenciado deve usar
   `var(--vc-*)`, `var(--lime)`, `var(--off-white)`, etc.
4. **Manual herda o catálogo da Política** — os 6 shortcodes da política
   estão disponíveis. Manual adiciona apenas `:::raci`.

---

## Shortcodes (7 ao todo)

### `:::papel-card` — Card vertical narrativo

Idêntico ao da política. Descreve um papel/processo com subseções narrativas.
Tipicamente usado na seção 6 (Papéis e Responsabilidades) quando a tabela
RACI é insuficiente para descrever a riqueza de um papel-chave.

**Sintaxe MD**:

```markdown
:::papel-card
título: Process Owner
owner: Head da área dona do processo

**Por que existe**: garantir end-to-end accountability do processo.

**O que faz**: aprova exceções, valida indicadores, escala bloqueios.

**Cadência**: revisão semanal do dashboard de aderência.
:::
```

**HTML gerado**:

```html
<div class="inv-card">
  <h4 class="inv-title">Process Owner</h4>
  <p class="inv-owner">Owner: Head da área dona do processo</p>
  <p class="inv-block"><strong>Por que existe</strong>: garantir end-to-end...</p>
  ...
</div>
```

**Classes**: `.inv-card`, `.inv-title`, `.inv-owner`, `.inv-block`.

Variante: `:::papel-card-separador` para separadores de camada (idêntico à política).

---

### `:::callout` — Bloco de destaque (3 variantes)

Idêntico ao da política. 3 variantes: `info` (default), `alerta`, `exemplo`.

```markdown
:::callout-alerta
tag: ATENÇÃO
título: Exceção requer aprovação de Diretoria

Operações fora do escopo deste manual exigem aprovação formal antes da
execução. Vide seção 5.3.
:::
```

**Classes**: `.callout`, `.callout-title`, `.callout-tag`, `.callout-alerta`,
`.callout-exemplo`.

---

### `:::indicador` — Card de indicador

Idêntico ao da política. Usado para KPIs/PPIs complexos cuja fórmula ou meta
não cabe na tabela 5-col padrão da seção 7.

**Quando usar tabela vs card**: até 2 KPIs e 2 PPIs simples → tabela padrão
(placeholders `KPI_N_*` e `PPI_N_*` da seção 7). Indicadores complexos
(fórmulas multi-linha) → cards.

**Classes**: `.indicador-card`, `.indicador-nome`, `.indicador-meta`.

---

### `:::diagrama` — SVG embebido

Idêntico ao da política. Usado para BPMN customizado, fluxogramas
auxiliares, ou diagramas de interface entre processos. Note que o BPMN
principal da seção 4.4 é renderizado pelo template a partir dos
placeholders `BPMN_TASK_N`, `BPMN_GATEWAY_1`, etc — esse shortcode é para
diagramas **extras**.

```markdown
:::diagrama
caption: Fig 2 · Fluxo de aprovação de exceções

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600">
  ...
</svg>
:::
```

**Classes**: `.embed-svg`, `.embed-svg-caption`.

**Regra**: SVG inline **só** dentro deste shortcode. Fora dele, o parser
rejeita `<svg>` solto.

---

### `:::processo-grid` — Grid compacto de processos

Idêntico ao da política. Útil em manuais transversais que listam múltiplos
processos cobertos.

**Classes**: `.skill-proc-block`, `.skill-proc-card`, `.skill-proc-title`,
`.skill-proc-owner`, `.skill-camada-sep`, `.skill-camada-title`.

---

### `:::raci` — Matriz RACI 5×5 colorida (manual-específico)

**Uso semântico**: representar uma matriz RACI **adicional** dentro do corpo
do manual (a RACI principal da seção 6.1 usa placeholders `RACI_PAPEL_N` +
`RACI_ATIV_N` no template e não precisa do shortcode). Use este shortcode
quando o manual descreve sub-processos com sua própria responsabilidade
matricial.

**Sintaxe MD**:

```markdown
:::raci
título: RACI · Sub-processo de exceções (5.3)

| Atividade | CEO | CFO | Risco | Head Op | Analista |
|-----------|-----|-----|-------|---------|----------|
| Solicitar exceção | I | I | C | A | R |
| Avaliar risco | I | C | R | A | I |
| Aprovar exceção | A | C | R | I | I |
| Registrar exceção | I | I | I | A | R |
| Auditar exceção | I | A | R | C | I |
:::
```

**HTML gerado**:

```html
<div class="raci-extra">
  <h4 class="sub">RACI · Sub-processo de exceções (5.3)</h4>
  <table class="raci-table">
    <thead><tr><th>Atividade</th><th>CEO</th><th>CFO</th><th>Risco</th><th>Head Op</th><th>Analista</th></tr></thead>
    <tbody>
      <tr>
        <th>Solicitar exceção</th>
        <td class="raci-cell raci-i">I</td>
        <td class="raci-cell raci-i">I</td>
        <td class="raci-cell raci-c">C</td>
        <td class="raci-cell raci-a">A</td>
        <td class="raci-cell raci-r">R</td>
      </tr>
      ...
    </tbody>
  </table>
</div>
```

**Classes utilizadas**: `.raci-table`, `.raci-cell`, `.raci-r`, `.raci-a`,
`.raci-c`, `.raci-i`, `.raci-extra` (wrapper), `.sub` (título).

**Cores semânticas (do template)**:
- `.raci-r` — Responsible: verde caqui suave (`var(--vc-200)`)
- `.raci-a` — Accountable: lime escuro (`var(--lime)` translúcido)
- `.raci-c` — Consulted: amarelo claro (`var(--ow-300)`)
- `.raci-i` — Informed: cinza neutro (`var(--vc-100)`)

**Regras de validação**:
1. Valores `R`, `A`, `C`, `I` (case-insensitive) nas células.
2. **Células compostas** `R, A` (ou `A, R`) — quando o mesmo papel é
   Responsible **E** Accountable pela atividade. Renderizadas com classe
   `.raci-cell.raci-ra` (R em cima, A embaixo).
3. Exatamente 1 `A` por linha (Accountability é única por atividade).
   Compound `R, A` conta como ambos para validação semântica.
4. Pelo menos 1 `R` por linha (todo trabalho tem responsável).
5. Tabela deve ter pelo menos 2 papéis (colunas) e 2 atividades (linhas).

Violações geram **warnings** (não abortam) — autor revisa antes de
publicar. A v5.0.0 abortava; a v5.1+ é mais permissiva para suportar
matrizes em transição.

### `:::ficha-icp` — Ficha de persona/ICP (v6.0, capítulo Anexos)

Card estruturado para documentar personas ICP no capítulo §11 Anexos.
Espelha a estrutura canônica de 7 blocos da `ICP.xlsx`.

**Sintaxe**:
```markdown
:::ficha-icp
titulo: Empresário Middle Market — Persona-decisor
icp: ICP1
arquetipo: persona-decisor

**Características da Pessoa**
- 40-55 anos, fundador ou herdeiro
- ...

**Dores Principais**
1. Sucessão patrimonial
2. ...

**Resolução M7**
- Plano patrimonial integrado PF/PJ
- ...

**Características da Negociação**
- Ticket médio: R$ 5-15M
- Ciclo: 3-6 meses
:::
```

**Attrs**:
- `titulo` — texto do cabeçalho (obrigatório)
- `icp` — código do ICP (opcional, ex.: `ICP1`, `ICP2`)
- `arquetipo` — `persona-decisor` ou `persona-gate` (default: genérico)

**Body**: blocos nomeados via `**Título**\\n...`. Suporta listas
markdown (`-`, `1.`), parágrafos e ênfase inline. Cada bloco vira
`.ficha-bloco` com `.ficha-bloco-titulo` (uppercase) + `.ficha-bloco-corpo`.

**Estilo**: cabeçalho com borda inferior em `var(--lime)`; arquétipo
"decisor" tem chip escuro, "gate" tem chip claro (cores invertidas).
`page-break-inside: avoid` para não quebrar entre páginas.

**Uso típico**: apenas dentro de §11 Anexos. Para personas avulsas em
seções operacionais, prefira `:::papel-card`.

---

## Allowlist de classes CSS no HTML final

Após renderização, **toda classe CSS no HTML deve pertencer a uma destas
categorias**. Classes fora da allowlist são bloqueadas pela validação.

### Classes estruturais do template (sempre presentes)

`.doc`, `.page`, `.page-head`, `.page-body`, `.page-foot`, `.ph-left`,
`.ph-sep`, `.ph-title`, `.ph-meta`, `.pf-classif`, `.pf-page`, `.cover`,
`.cover-title`, `.cover-subtitle`, `.cover-body`, `.cover-grid`, `.cover-head`,
`.cover-foot`, `.cover-meta`, `.cover-eyebrow`, `.section`, `.section-lede`,
`.sub`, `.subsub`, `.muted`, `.muted-empty`, `.chip`, `.mono`, `.kv-table`,
`.doc-table`, `.approval-card`, `.approval-grid`, `.toc`, `.toc-item`,
`.toc-num`, `.toc-title`, `.toc-page`, `.total-pg`, `.shell-main`,
`.toolbar`, `.navbtn`, `.export`, `.divider`, `.num`, `.sep`, `.dot`,
`.label`, `.name`, `.role`, `.who`, `.what`, `.h`, `.l`, `.v`, `.cell`,
`.col`, `.item`, `.meta`, `.pg`, `.formula`, `.freq`, `.out`, `.counter`,
`.timeline`, `.ritual`, `.step`, `.sig-line`, `.conf`, `.hl`.

### Classes de tipografia (m7-tokens.css)

`.text-display-1`, `.text-display-2`, `.text-h1` a `.text-h4`,
`.text-body-1` a `.text-body-3`, `.text-button`, `.text-label`,
`.text-muted`, `.text-mono`, `.section-eyebrow`.

### Classes navegacionais (m7-tokens.css)

`.m7-nav`, `.m7-nav-inner`, `.m7-nav-logo`, `.m7-nav-links`, `.ds-tag`,
`.m7-foot`, `.m7-foot-inner`, `.container`, `.stack`, `.row`, `.grid`.

### Classes manual-específicas do template (BPMN / SIPOC / RACI / Indicadores / Cronograma)

**BPMN (seção 4.4)**:
`.bpmn-frame`, `.bpmn-head`, `.bpmn-head-code`, `.bpmn-head-title`,
`.bpmn-canvas`, `.bpmn-pool`, `.bpmn-lane-strip`, `.bpmn-lane-bg`,
`.bpmn-lane-bg.alt`, `.bpmn-lane-label`, `.bpmn-lane-divider`,
`.bpmn-task`, `.bpmn-task-header`, `.bpmn-task-label`, `.bpmn-event-start`,
`.bpmn-event-end`, `.bpmn-event-label`, `.bpmn-gateway`, `.bpmn-gateway-mark`,
`.bpmn-flow`, `.bpmn-flow-label`, `.bpmn-flow-label-bg`, `.bpmn-arrow-fill`,
`.bpmn-legend`, `.bpmn-caption`.

**SIPOC (seção 4.2)**: `.sipoc`, `.col.is-process`.

**RACI (seção 6.1 + shortcode `:::raci`)**:
`.raci-table`, `.raci-cell`, `.raci-r`, `.raci-a`, `.raci-c`, `.raci-i`,
`.raci-legend`, `.raci-extra`, `.activity`, `.activity-h`, `.twocol`.

**Indicadores (seção 7)**:
`.kpi-grid`, `.kpi-card`, `.kpi-card.ppi`.

**Qualidade (seção 9)**: `.dto-list`.

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
- **raci**: já listadas em "RACI" acima (`.raci-extra` é o wrapper específico do shortcode)

### Classes ad-hoc — PROIBIDAS

Qualquer classe que **não** apareça nas categorias acima é rejeitada pela
validação. Exemplos do que **não** é aceito:

- `.man-*`, `.proc-*`, `.fluxo-*` (prefixos "customizados" do autor) —
  use shortcodes ou expanda o catálogo formalmente
- `.user-*`, `.note-*`, `.my-namespace` — **acabou**. Não há mais escape hatch.

---

## Como adicionar um shortcode novo (processo formal)

1. **Abrir issue** descrevendo o caso de uso semântico (não estético).
2. **Definir CSS** em `assets/manual-m7-template.html` usando apenas
   `var(--*)` — zero hex literal.
3. **Adicionar entrada neste catálogo** (sintaxe + HTML gerado +
   classes utilizadas).
4. **Implementar parser** em `scripts/generate-html-yaml.py` na função
   `expand_shortcodes()`.
5. **Atualizar allowlist** acima.
6. **Atualizar gold reference** se faz sentido demonstrar.
7. **Bump** de versão menor do plugin.
8. **Smoke test** em `/tmp` antes de commit.
