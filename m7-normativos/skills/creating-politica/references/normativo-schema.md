# Schema YAML do Normativo — Guia para autor de POL

Esta referência destila o que o autor precisa saber para preencher o sidecar YAML
de uma Política. Para o schema canônico completo, vide
[normativo.schema.yaml](normativo.schema.yaml). Para o exemplo preenchido,
[normativo.exemplo-pol-gov-002.yaml](normativo.exemplo-pol-gov-002.yaml).

## Princípio

Cada POL produzida pela skill é **um par de arquivos com mesmo basename**:

```
artefatos/
├── politica-foo.html   ← renderização humana (estrutura invariante)
└── politica-foo.yaml   ← identidade canônica (fonte de verdade para o Cockpit)
```

- O **YAML é a fonte canônica**. Em caso de conflito YAML × HTML, regere o HTML.
- O **HTML é estrutura invariante** (template oficial). A skill só preenche valores.
- Cada campo do YAML é espelhado em ~10 pontos do HTML automaticamente.

## Estrutura — 6 blocos

```yaml
schema_version: "1.0"
identity:     {...}    # código, tipo, área, versão, status, classif
lifecycle:    {...}    # datas de vigência e revisão
governance:   {...}    # owner, aprovador, hierarquia, processos
presentation: {...}    # títulos, leds, eyebrow, área-label
structure:    {toc: [...]}  # sumário lateral (páginas)
links:        {siblings: [...], artifact_html: ...}
```

## Defaults para POL

A skill aplica estes defaults sem perguntar:

| Campo | Default POL |
|-------|-------------|
| `identity.tipo` | `POL` |
| `identity.tipo_label` | `Política` |
| `identity.version` | `v1.0` (se for documento novo) |
| `identity.status` | `rascunho` (até aprovação formal) |
| `identity.classif` | `Interno` |
| `identity.classif_label` | `Uso interno · Confidencial` |
| `lifecycle.revisaoFreq` | `Anual` (fixo — vide POL-M7-001) |
| `lifecycle.nextReview` | `lifecycle.date + 1 ano` |
| `governance.aprovador_role` | `Diretoria` (fixo — POL exige aprovação no nível mais alto) |
| `presentation.eyebrow_categoria` | `Documento de governança` |
| `presentation.page_label_section` | derivado de `area_label` |

## Tabela campo → ponto no HTML (essencial)

| YAML | Aparece em |
|------|------------|
| `identity.code` | `<title>`, shell-meta, side-meta, cover-eyebrow, cover-foot, ph-meta (×N), kv-table |
| `identity.version` | `.strip`, `.cover-foot`, `.ph-meta` (×N) |
| `identity.version_label` | `.strip`, side-meta, cover-grid, kv-table |
| `identity.pages` | `.strip`, `.total-pg` (×N), `#total-pages` |
| `identity.classif_label` | `.cover-foot .conf`, `.pf-classif` (×N) |
| `lifecycle.date_label` | shell-meta, cover-meta, `.strip` (curta), `.cover-grid`, kv-table |
| `lifecycle.nextReview_label` | side-meta, `.strip` (curta), `.cover-grid` |
| `lifecycle.revisaoFreq` | kv-table |
| `governance.owner` | side-meta, `.cover-grid` |
| `governance.elaboradoPor` | kv-table (primeiro segmento em `<strong>`) |
| `governance.aprovadoPor` | kv-table, página de aprovações |
| `governance.parent.code` + `title` | kv-table (formato: `<mono>{code}</mono> · {title}`) |
| `presentation.title_short` | `<title>`, `.ph-title` (×N pages internas) |
| `presentation.title_full.parts` | `<h1>` no shell (com `<span class="accent">`) + `.cover-title` (com `<em>` e auto-`<br>`) |
| `presentation.subtitle` | `.cover-subtitle` |
| `presentation.lede` | `.lede` no shell |
| `presentation.eyebrow_categoria` | `.cover-eyebrow` (primeiro span) |
| `presentation.page_label_section` | shell-meta, cover-meta (primeiro span) |
| `structure.toc[]` | sumário lateral (`<button class="item">` ×N) + sumário formal da p.2 |
| `links.siblings[]` | tabs do shell |

## Renderização do título com destaque (`title_full.parts`)

O título do documento aparece em DOIS lugares com markup diferente:

### No shell header (single-line)

```html
<h1>Política <span class="accent">geral de governança</span> corporativa</h1>
```

A partir de:

```yaml
title_full:
  parts:
    - text: "Política "
    - text: "geral de governança"
      accent: true
    - text: " corporativa"
```

### Na cover (multi-line)

```html
<h1 class="cover-title">Política<br><em>geral de governança</em> corporativa</h1>
```

Mesmo YAML, renderização diferente:
- `accent: true` vira `<span class="accent">` no shell e `<em>` na cover.
- A skill aplica **auto-quebra `<br>`** antes da segunda parte quando a primeira é
  uma palavra curta (≤12 chars). Para forçar quebra em outro ponto, use
  `break_before: true`.
- A política de design (handoff §4): envolve o **segmento accent inteiro** em
  `<em>` — não só uma palavra. Se quiser destacar só uma palavra, decomponha a
  parte em três (texto antes, palavra com `accent: true`, texto depois).

## Tabs do shell (`links.siblings`)

```yaml
links:
  siblings:
    - { label: "Visão geral", badge: "N1", href: "cadeia-de-valor.html" }
    - { label: "Missão do processo", href: "missao.html" }
    - { label: "Política", badge: "DOC", href: "politica.html", active: true }
```

- A entrada `active: true` é a do próprio documento — vira `<div class="tab" data-active="true">`.
- As outras viram `<a class="tab" href="...">`.
- Ordem do YAML = ordem visual no HTML.

## Sumário lateral e formal (`structure.toc`)

Cada entrada é uma página A4 do documento:

```yaml
structure:
  toc:
    - { page: 1, label: "Capa" }
    - { page: 2, label: "Controle & sumário" }
    - { page: 3, label: "1. Objetivo & 2. Escopo", section: "1. Objetivo" }
    - { page: 4, label: "3. Definições", section: "3. Definições" }
    # ...
    - { page: 7, label: "5.1.2 · Gerencial", subsection: true }
```

- **Sumário lateral**: TODAS as entradas viram um `<button class="item">`.
- **Sumário formal (página 2)**: apenas entradas com `section` (h1 do TOC) ou
  `subsection: true` (h2 do TOC, com classe `.toc-item.h2`).
- `page` é 1-based; aparece formatado com `zfill(2)` no botão lateral.

## Validações automáticas do script

Antes de gerar o HTML, `generate-html-yaml.py` valida:

- [ ] Todos os `required` do schema preenchidos
- [ ] `identity.code` casa `^(POL|MAN|INS|ESP)-[A-Z]{2,4}-[0-9]{3}$`
- [ ] `identity.tipo` ∈ `{POL, MAN, INS, ESP}`
- [ ] `identity.area` ∈ `{GOV, PERF, INV, CRE, SEG, UNI, TEC, PES, M7}`
- [ ] `identity.status` ∈ `{vigente, revisao, rascunho, pendente, vencido}`
- [ ] `identity.classif` ∈ `{Público, Interno, Confidencial, Restrito}`
- [ ] `identity.version` casa `^v?[0-9]+\.[0-9]+$`
- [ ] `lifecycle.revisaoFreq` ∈ `{Anual, Semestral, Trimestral, Mensal, Sob demanda}`
- [ ] `governance.parent` é `null` ou objeto com `code` válido
- [ ] `governance.processos[]` casam `^(G[1-4]|P[1-9]|P1[0-2]|A[1-5])$`
- [ ] Quando `status ∈ {vigente, revisao, vencido}`: `lifecycle.date` e `nextReview` são obrigatórios

Falha de validação aborta a geração com mensagem clara — sem produção de HTML/YAML.

## Conflito YAML × HTML

Se você editar o HTML manualmente e divergir do YAML, **vence o YAML**: regere o
HTML rodando o script de novo. Nunca tente "sincronizar manualmente" — o
cockpit lê só o YAML, então é ele que conta.

## Limitação atual da Fase 3 (importante)

O script de Fase 3 espelha **identidade/metadata** (anchors da tabela acima)
mas **não injeta conteúdo das 8 seções narrativas** (Objetivo, Escopo, Definições,
Princípios, Diretrizes, Papéis, Governança, Disposições finais).

Em vez disso, ele preserva o conteúdo das seções vindo do template (que está
no exemplo POL-GOV-002). Para uma POL nova, o autor edita manualmente as
páginas 3-15 do HTML gerado depois — ou aguarda a próxima iteração da skill
que adicionará injeção do MD da Fase 2.
