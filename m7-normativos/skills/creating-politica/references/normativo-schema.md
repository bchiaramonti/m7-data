# Schema YAML do Normativo — Guia para autor de POL (v2.1)

Esta referência destila o que o autor precisa saber para preencher o sidecar YAML
de uma Política. Para o schema canônico completo, vide
[normativo.schema.yaml](normativo.schema.yaml). Para o exemplo preenchido,
[normativo.exemplo-pol-gov-002.yaml](normativo.exemplo-pol-gov-002.yaml).

## Princípio

Cada POL produzida pela skill é **um par de arquivos com mesmo basename**:

```
catalogo/
├── politica-foo.html   ← renderização autocontida (~1.4MB, CSS/fonts/logos inlinados)
└── politica-foo.yaml   ← identidade canônica para o Cockpit de Normativos
```

- **YAML é fonte canônica**. Em conflito YAML × HTML, regere o HTML.
- **HTML é autocontido (v2.1)**. Funciona em `file://`, HTTP, anexo de email — sem precisar de paths relativos a CSS ou fonts.
- O Cockpit lê só os YAMLs para montar matriz/lista/hierarquia.

## Pipeline da Fase 3

O script [generate-html-yaml.py](../scripts/generate-html-yaml.py) faz:

1. Parseia BRIEFING (YAML)
2. Valida contra schema (patterns, enums, required, required_when)
3. Opcionalmente parseia `politica-{slug}.md` extraindo blocos das 8 seções
4. Constrói dicionário de **145 placeholders** → valores
5. **Inlinea CSS + 6 fonts (base64) + 3 logos (base64)** no template
6. Aplica `html.replace("{{KEY}}", value)` para todos os placeholders
7. Valida: zero `{{}}` residuais, zero paths relativos
8. Escreve `{slug}.html` + `{slug}.yaml`

## Estrutura YAML — 6 blocos

```yaml
schema_version: "1.0"
identity:     {...}    # código, tipo, área, versão, status, classif
lifecycle:    {...}    # datas de vigência e revisão
governance:   {...}    # owner, aprovador, hierarquia, processos
presentation: {...}    # títulos, leds, eyebrow, área-label
structure:    {toc: [...]}  # opcional — usado pelo cockpit
links:        {siblings, artifact_html}  # opcional
```

## Defaults para POL (aplicados pela skill)

| Campo | Default |
|-------|---------|
| `identity.tipo` | `POL` |
| `identity.tipo_label` | `Política` |
| `identity.version` | `v1.0` |
| `identity.status` | `rascunho` |
| `identity.classif` | `Interno` |
| `identity.classif_label` | `Uso interno · Confidencial` |
| `lifecycle.revisaoFreq` | `Anual` (fixo para POL) |
| `lifecycle.nextReview` | `lifecycle.date + 1 ano` |
| `governance.aprovador_role` | `Diretoria` (fixo para POL) |

## `governance.escopo` — alocação na Matriz do Cockpit

Campo **obrigatório** (com auto-derivação): controla **onde** o documento é alocado na lane da Matriz do Cockpit. Valores permitidos: `holding | transversal | processo`.

| escopo | O que faz | Quantas células |
|--------|-----------|------------------|
| `holding` | aloca na lane "Holding M7" (célula única M7::tipo) | 1 |
| `transversal` | aloca em cada processo do array `processos` | N (= tamanho do array) |
| `processo` | aloca no único processo do array | 1 |

### Auto-derivação quando ausente

A skill (script `generate-html-yaml.py`) preenche o campo se ausente:
- `processos` com 0 ou 1 item → `escopo: processo`
- `processos` com 2 ou mais itens → `escopo: transversal`
- **`holding` NUNCA é auto-derivado**, sempre explícito (proteção contra docs que cobrem P1-P12 mas semanticamente são transversais, não holding).

### 4 jeitos de alinhar à Holding

**1. Doc da Holding (rege todos os primários ou a M7 como entidade)**

```yaml
governance:
  escopo: holding
  processos: [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12]
  # ↑ informativo: aparece no drawer "Processos cobertos".
  # A Matriz IGNORA esta lista quando escopo=holding e aloca só em M7::POL.
```
Resultado: 1 célula na lane Holding M7, coluna POL.

**2. Manual/Instrução de 1 processo (típico de MAN/INS/ESP)**

```yaml
governance:
  # escopo omitido → auto-derivado para "processo"
  processos: [P3]   # P3 = Operação Crédito
```
Resultado: 1 célula em P3 × MAN (lane Primários).

**3. Instrução transversal (cruza 2+ processos sem ser holding)**

```yaml
governance:
  # escopo omitido → auto-derivado para "transversal"
  processos: [P1, P12]   # vale para Geração de Demanda e Retenção
```
Resultado: 2 células — P1 × INS e P12 × INS.

**4. Doc de camada Gerencial ou Apoio**

```yaml
governance:
  processos: [G2]   # G2 = Gestão de Performance (Gerencial)
# ou
  processos: [A1]   # A1 = Tecnologia & Dados (Apoio)
```
Aparece na lane respectiva (Gerenciais / Apoio).

### Vocabulário de códigos válidos

| Lane | Códigos no array `processos` | Exemplo |
|------|------------------------------|---------|
| **Holding M7** | (use `escopo: holding` — não use "M7" no array) | POL-GOV-002 |
| Gerenciais | `G1` / `G2` / `G3` / `G4` | INS-PERF-001 (G2) |
| Primários | `P1` ... `P12` | MAN-CRE-001 (P3) |
| Apoio | `A1` / `A2` / `A3` / `A4` / `A5` | MAN-TEC-001 (A1) |

**Regra de ouro**: "Holding" é o **escopo**, não um item do array. "M7" existe no vocabulário interno do cockpit como célula-destino da lane Holding, mas você nunca escreve `processos: [M7]` — escreve `escopo: holding` e lista os processos regidos em `processos` (informativo).

## Mapeamento YAML → 145 placeholders do template

### Identidade (12 placeholders)

| Placeholder | Fonte YAML |
|-------------|------------|
| `{{CODIGO_DOCUMENTO}}` | `identity.code` |
| `{{TIPO_DOCUMENTO}}` | `identity.tipo_label` |
| `{{TIPO_DOCUMENTO_SIGLA}}` | `identity.tipo` |
| `{{NIVEL_DOCUMENTO}}` | `identity.tipo` (POL/MAN/INS/ESP) |
| `{{AREA_DOCUMENTO}}` | `identity.area_label` |
| `{{TITULO_DOCUMENTO}}` | `presentation.title_short` |
| `{{NOME_DA_EMPRESA}}` | fixo: "M7 Investimentos" |
| `{{VERSAO_CURTA}}` | `identity.version` |
| `{{VERSAO_COMPLETA}}` | `identity.version_label` |
| `{{CLASSIFICACAO_DOCUMENTO}}` | `identity.classif_label` |
| `{{TOTAL_PAGINAS}}` | `identity.pages` |

### Datas (7 placeholders)

| Placeholder | Fonte YAML |
|-------------|------------|
| `{{DATA_REFERENCIA}}` | `lifecycle.date_label` |
| `{{DATA_VIGENCIA}}` | `lifecycle.date_label` |
| `{{DATA_PROXIMA_REVISAO}}` | `lifecycle.nextReview_label` |
| `{{DATA_ELABORACAO}}` | `lifecycle.date_label` (default) |
| `{{DATA_REVISAO}}` | "" (vazio até primeira revisão) |
| `{{DATA_APROVACAO}}` | `lifecycle.date_label` (default) |
| `{{CADENCIA_REVISAO}}` | `lifecycle.revisaoFreq` |

### Capa título — decomposição (5 placeholders)

| Placeholder | Fonte YAML |
|-------------|------------|
| `{{COVER_TITULO_LINHA1}}` | primeira palavra de `presentation.title_full.parts[0].text` (heurística: ≤12 chars) |
| `{{COVER_TITULO_PREFIXO}}` | texto restante antes do segmento accent |
| `{{COVER_TITULO_ACENTO}}` | texto da parte com `accent: true` |
| `{{COVER_TITULO_SUFIXO}}` | texto após o segmento accent |
| `{{COVER_SUBTITULO}}` | `presentation.subtitle` |

Exemplo: `parts: [{text: "Política "}, {text: "geral de governança", accent: true}, {text: " corporativa"}]`

Resulta em:
- LINHA1: `"Política"`
- PREFIXO: `""`
- ACENTO: `"geral de governança"`
- SUFIXO: `"corporativa"`

Renderiza na cover: `Política<br><em>geral de governança</em> corporativa`

### Governança (9 placeholders)

| Placeholder | Fonte YAML |
|-------------|------------|
| `{{AREA_RESPONSAVEL}}` | `governance.owner` |
| `{{NOME_ELABORADOR}}` | parte 1 de `governance.elaboradoPor` (split por " · ") |
| `{{CARGO_ELABORADOR}}` | parte 2+ de `governance.elaboradoPor` |
| `{{NOME_APROVADOR}}` + `{{CARGO_APROVADOR}}` | split de `governance.aprovadoPor` |
| `{{NOME_REVISOR}}` + `{{CARGO_REVISOR}}` | split de `governance.revisor` |
| `{{CODIGO_DOC_SUPERIOR}}` | `governance.parent.code` |
| `{{TITULO_DOC_SUPERIOR}}` | `governance.parent.title` |

Exemplo: `elaboradoPor: "Bruno Chiaramonti · Head de Desempenho · M7 Investimentos"` →
- NOME_ELABORADOR: `"Bruno Chiaramonti"`
- CARGO_ELABORADOR: `"Head de Desempenho · M7 Investimentos"`

### Conteúdo das 8 seções — vem do MD da Fase 2 (~110 placeholders)

Mapeamento entre seção MD e placeholders:

| Seção MD (h2) | Placeholders gerados |
|---------------|----------------------|
| `## 1. Objetivo` | `TEXTO_OBJETIVO_P1`, `TEXTO_OBJETIVO_P2` (2 parágrafos) |
| `## 2. Escopo` | `LEDE_ESCOPO`, `ESCOPO_INCLUSAO_1..3`, `ESCOPO_EXCLUSAO_1..3` |
| `## 3. Definições` | `DEF_TERMO_1..12`, `DEF_TEXTO_1..12` (tabela 2 col) |
| `## 4. Princípios` | `LEDE_PRINCIPIOS`, `PRINCIPIO_1..7_TITULO`, `PRINCIPIO_1..7_DESCRICAO` (h3 + parágrafo) |
| `## 5. Diretrizes` | `LEDE_DIRETRIZES`, `SUMARIO_DIRETRIZES` (gerado da lista após `**Sumário**`), `CONTEUDO_DIRETRIZES` (HTML rico) |
| `## 6. Papéis & Responsabilidades` | `LEDE_PAPEIS`, `PAPEL_1..8_NIVEL`, `PAPEL_1..8_NOME`, `PAPEL_1..8_RESPONSABILIDADES` (tabela 3 col) |
| `## 7. Governança` | `REVISAO_PERIODICA_INTRO`, `GATILHO_REVISAO_1..4`, `INDICADOR_1..5_{NOME,FORMULA,FREQ,META}`, `ESCALA_TIPO_1..6`, `ESCALA_APROVADOR_1..6` |
| `## 8. Disposições Finais` | `TEXTO_VIGENCIA`, `DOC_REL_1_{CODIGO,TITULO,RELACAO}` |

Placeholders sem dado correspondente (ex.: `PRINCIPIO_6` quando o MD só tem 5) ficam com **string vazia**. O CSS trata graciosamente.

## Inline de assets (autocontido)

O script substitui antes da expansão de placeholders:

| Asset | Como é inlinado |
|-------|-----------------|
| `m7-tokens.css` (7KB) | `<link rel="stylesheet" href="m7-tokens.css">` → `<style>...</style>` |
| 6 fonts TWK Everett OTF (~1MB total) | dentro do CSS inlinado, `url("fonts/X.otf")` → `url(data:font/otf;base64,...)` |
| 3 logos (m7-logo-dark.png, offwhite, favicon) | `assets/m7-logo-*.png` → `data:image/png;base64,...` |

Resultado: HTML ~1.4MB sem nenhum `<link>` externo ou `<img src="assets/">` — abre standalone em qualquer browser.

## Validações automáticas

Antes de gerar o HTML, o script valida:

- [ ] Todos os `required` do schema preenchidos
- [ ] `identity.code` casa `^(POL|MAN|INS|ESP)-[A-Z]{2,4}-[0-9]{3}$`
- [ ] `identity.tipo` ∈ `{POL, MAN, INS, ESP}`
- [ ] `identity.area` ∈ `{GOV, PERF, INV, CRE, SEG, UNI, TEC, PES, M7}`
- [ ] `identity.status` ∈ `{vigente, revisao, rascunho, pendente, vencido}`
- [ ] `identity.classif` ∈ `{Público, Interno, Confidencial, Restrito}`
- [ ] `identity.version` casa `v?\d+\.\d+`
- [ ] `lifecycle.revisaoFreq` ∈ enum
- [ ] Status ∈ `{vigente, revisao, vencido}` ⇒ `lifecycle.date` e `nextReview` obrigatórios
- [ ] `governance.parent.code` (se objeto) casa pattern
- [ ] `governance.processos[]` casam `G1-G4 | P1-P12 | A1-A5`

Após a substituição:
- [ ] Zero placeholders `{{}}` residuais
- [ ] Zero `href="assets/`, `href="fonts/`, `href="m7-tokens.css"` (paths relativos)

Falha em qualquer item aborta a geração com mensagem clara.

## Conflito YAML × HTML

Se você editar o HTML manualmente e divergir do YAML, **vence o YAML**: regere o
HTML rodando o script de novo. Nunca tente "sincronizar manualmente".

## Page-break em Diretrizes (v2.3+)

Para documentos com seção 5 (Diretrizes) extensa, use o marker
`<!-- /page-break -->` no MD da Fase 2 para quebrar em múltiplas páginas A4:

```markdown
## 5. Diretrizes

(lede)

**Sumário:**
- 5.1 Bloco A
- 5.2 Bloco B

### 5.1 · Bloco A

(conteúdo da página 6)

<!-- /page-break -->

### 5.2 · Bloco B

(conteúdo da página 7 — nova <article>)
```

- Sem markers → 1 página de Diretrizes (comportamento padrão).
- Com N markers → N+1 páginas (chunk 0 fica em CONTEUDO_DIRETRIZES; chunks 1..N viram `<article>` extras inseridos via `{{EXTRA_DIRETRIZES_PAGES}}`).
- A numeração das páginas é atualizada pelo JS do template em runtime — todos os "Página X" são derivados da posição da `.page` no DOM.

## Marcação leniente no MD (v2.3+)

A partir da v2.3, o parser aceita variações:

- **Escopo "Aplica-se a"**: tanto `**Aplica-se a:**` (bold) quanto `### Aplica-se a` (heading h3). Idem "Não se aplica a".
- **Revisão/Vigência (seção 7/8)**: aceita prefixo numérico opcional, ex.: `### 7.1 · Revisão periódica` ou `### Revisão periódica`.
- **Bold/itálico/code/link em campos de texto**: `**bold**`, `*itálico*`, `` `code` ``, `[texto](url)` funcionam em TODOS os campos (não só CONTEUDO_DIRETRIZES). Anteriormente apenas o conteúdo de Diretrizes processava markdown — agora Objetivo, Escopo, Princípios, Papéis, Governança, Disposições também.

## Classes M7 em conteúdo livre (v2.3+)

Quando o autor inclui tabelas, h3 ou h4 dentro de `## 5. Diretrizes` (que vira HTML rico via markdown lib), o script aplica automaticamente as classes M7:

- `<table>` → `<table class="doc-table">` (header dark + spacing M7)
- `<h3>` → `<h3 class="sub">` (12px, lime accent)
- `<h4>` → `<h4 class="subsub">` (11px, lime accent menor)

Elementos que já tenham classe (ex.: `<h4 class="proc-title">` em cards de processo) **não** são tocados — preserva customizações do autor.

## Cards de inventário de processos (v2.3+)

Para listar processos macro (P1-P12, G1-G4, A1-A5), o template oficial agora embute CSS para:

```html
<div class="camada-sep">
  <h4 class="camada-title">Camada Primária</h4>
  <p>Doze processos que geram receita direta.</p>
</div>
<div class="proc-block">
  <div class="proc-card">
    <h4 class="proc-title">P1 · Geração de Demanda</h4>
    <p class="proc-owner">Head de Marketing</p>
  </div>
  <!-- ... -->
</div>
```

Renderiza como cartões `lime-bordered` 4 colunas com separadores discretos por camada. Padrão reutilizável em qualquer POL/MAN que liste processos.

## Imagens externas (v2.3+)

`<img src="path/relativo/img.svg">` (ou .png/.jpg/.webp) no MD é automaticamente inlinado como `data:image/...;base64`. Path é relativo ao diretório do MD. Imagens com `src="data:..."`, `http://`, `https://` são preservadas. Se o arquivo não existir, o script emite warning no stderr mas continua.
