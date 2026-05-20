# Schema YAML do Normativo — Guia para autor de MAN (v1.0)

Esta referência destila o que o autor precisa saber para preencher o sidecar YAML
de um Manual. Para o schema canônico completo (compartilhado entre POL/MAN/INS/ESP),
vide [normativo.schema.yaml](normativo.schema.yaml). Para o exemplo preenchido,
[normativo.exemplo-man-perf-003.yaml](normativo.exemplo-man-perf-003.yaml).

## Princípio

Cada MAN produzido pela skill é **um trio de arquivos com mesmo basename**:

```
catalogo/
├── MAN-PERF-003.html        ← renderização autocontida (~1.5MB, CSS/fonts/logos inlinados)
├── MAN-PERF-003.yaml        ← identidade canônica para o Cockpit de Normativos
└── MAN-PERF-003.review.md   ← relatório do agente manual-design-reviewer
```

- **YAML é fonte canônica**. Em conflito YAML × HTML, regere o HTML.
- **HTML é autocontido**. Funciona em `file://`, HTTP, anexo de email — sem precisar de paths relativos a CSS ou fonts.
- O Cockpit lê só os YAMLs para montar matriz/lista/hierarquia.

## Pipeline da Fase 3

O script [generate-html-yaml.py](../scripts/generate-html-yaml.py) faz:

1. Parseia BRIEFING (YAML)
2. Valida contra schema (patterns, enums, required, required_when)
3. Opcionalmente parseia `manual-{slug}.md` extraindo blocos das 10 seções
4. Constrói dicionário de **149 placeholders** → valores
5. **Inlinea CSS + 6 fonts (base64) + 3 logos (base64)** no template
6. Aplica `html.replace("{{KEY}}", value)` para todos os placeholders
7. Valida: zero `{{}}` residuais, zero paths relativos, classes na allowlist
8. Escreve `{slug}.html` + `{slug}.yaml` + `{slug}.review.md` (stub)

## Estrutura YAML — 6 blocos (idêntica à POL)

```yaml
schema_version: "1.0"
identity:     {...}    # código, tipo, área, versão, status, classif
lifecycle:    {...}    # datas de vigência e revisão
governance:   {...}    # owner, aprovador, hierarquia, processos
presentation: {...}    # títulos, leds, eyebrow, área-label
structure:    {toc: [...]}  # 11 entradas (manual tem 11 páginas A4)
links:        {siblings, artifact_html, artifact_md}  # opcional
```

## Defaults para MAN (aplicados pela skill)

| Campo | Default |
|-------|---------|
| `identity.tipo` | `MAN` |
| `identity.tipo_label` | `Manual` |
| `identity.version` | `v1.0` |
| `identity.status` | `rascunho` |
| `identity.classif` | `Interno` |
| `identity.classif_label` | `Uso interno · Confidencial` |
| `identity.pages` | `11` (manual tem 11 páginas A4 fixas) |
| `lifecycle.revisaoFreq` | `Semestral` (fixo para MAN) |
| `lifecycle.nextReview` | `lifecycle.date + 6 meses` |
| `governance.aprovador_role` | `Head de área` (fixo para MAN) |
| `presentation.eyebrow_categoria` | `Manual operacional` |

## `governance.escopo` — alocação na Matriz do Cockpit

Campo **obrigatório** (com auto-derivação): controla **onde** o documento é alocado na lane da Matriz do Cockpit. Para MAN os valores comuns são `processo` ou `transversal` (raramente `holding` — manuais da Holding M7 cobrem governança institucional, caso atípico).

| escopo | Quando usar (em MAN) | Quantas células |
|--------|----------------------|------------------|
| `processo` | Manual de UM processo específico (mais comum: 90% dos MANs) | 1 |
| `transversal` | Manual que cobre 2+ processos sem ser holding | N |
| `holding` | Manual da Holding M7 (institucional, ex.: MAN-GOV-001 Manual de Governança Corporativa) | 1 |

### Auto-derivação quando ausente

A skill (script `generate-html-yaml.py`) preenche o campo se ausente:
- `processos` com 0 ou 1 item → `escopo: processo`
- `processos` com 2 ou mais itens → `escopo: transversal`
- **`holding` NUNCA é auto-derivado**, sempre explícito.

### Casos típicos de MAN

**1. Manual de UM processo primário (caso padrão — 90% dos MANs)**

```yaml
governance:
  # escopo omitido → auto-derivado para "processo"
  processos: [G2]   # G2 = Gestão de Desempenho (Gerencial)
```
Resultado: 1 célula em G2 × MAN.

**2. Manual transversal (cruza 2+ processos)**

```yaml
governance:
  # escopo omitido → auto-derivado para "transversal"
  processos: [P1, P2, P3]   # vale para Captação, Onboarding, Operação
```
Resultado: 3 células — P1×MAN, P2×MAN, P3×MAN.

**3. Manual da Holding (atípico)**

```yaml
governance:
  escopo: holding
  processos: [G1, G2, G3, G4]  # informativo
```
Resultado: 1 célula na lane Holding M7.

### Vocabulário de códigos válidos

| Lane | Códigos no array `processos` | Exemplo |
|------|------------------------------|---------|
| Gerenciais | `G1` / `G2` / `G3` / `G4` | MAN-PERF-003 (G2 — Gestão de Desempenho) |
| Primários | `P1` ... `P12` | MAN-CRE-001 (P3 — Operação Crédito) |
| Apoio | `A1` / `A2` / `A3` / `A4` / `A5` | MAN-TEC-001 (A1 — Tecnologia & Dados) |
| Holding | (use `escopo: holding`) | MAN-GOV-001 |

## Mapeamento YAML → 149 placeholders do template

### Identidade (12 placeholders)

| Placeholder | Fonte YAML |
|-------------|------------|
| `{{CODIGO_DOCUMENTO}}` | `identity.code` |
| `{{TIPO_DOCUMENTO}}` | `identity.tipo_label` (= "Manual") |
| `{{AREA_DOCUMENTO}}` | `identity.area_label` |
| `{{TITULO_DOCUMENTO}}` | `presentation.title_short` |
| `{{NOME_DA_EMPRESA}}` | fixo: "M7 Investimentos" |
| `{{VERSAO_CURTA}}` | `identity.version` |
| `{{VERSAO_COMPLETA}}` | `identity.version_label` |
| `{{CLASSIFICACAO_DOCUMENTO}}` | `identity.classif_label` |
| `{{TOTAL_PAGINAS}}` | `identity.pages` (= 11 por default) |

### Datas (3 placeholders)

| Placeholder | Fonte YAML |
|-------------|------------|
| `{{DATA_REFERENCIA}}` | `lifecycle.date_label` |
| `{{DATA_VIGENCIA}}` | `lifecycle.date_label` |
| `{{DATA_PROXIMA_REVISAO}}` | `lifecycle.nextReview_label` |

### Capa título — decomposição (5 placeholders)

| Placeholder | Fonte YAML |
|-------------|------------|
| `{{COVER_TITULO_LINHA1}}` | primeira parte de `presentation.title_full.parts` (heurística) |
| `{{COVER_TITULO_PREFIXO}}` | texto restante antes do segmento accent |
| `{{COVER_TITULO_ACENTO}}` | texto da parte com `accent: true` |
| `{{COVER_TITULO_SUFIXO}}` | texto após o segmento accent |
| `{{COVER_SUBTITULO}}` | `presentation.subtitle` |

### Governança (7 placeholders)

| Placeholder | Fonte YAML |
|-------------|------------|
| `{{NOME_ELABORADOR}}` + `{{CARGO_ELABORADOR}}` | split de `governance.elaboradoPor` |
| `{{NOME_APROVADOR}}` + `{{CARGO_APROVADOR}}` | split de `governance.aprovadoPor` |
| `{{CODIGO_DOC_SUPERIOR}}` | `governance.parent.code` |
| `{{TITULO_DOC_SUPERIOR}}` | `governance.parent.title` |

### Processo macro (6 placeholders — manual-específico)

| Placeholder | Fonte YAML / MD |
|-------------|-----------------|
| `{{NOME_PROCESSO}}` | `presentation.nome_processo` (manual-específico) |
| `{{CODIGO_PROCESSO}}` | primeiro item de `governance.processos` (ex.: G2) |
| `{{PROCESS_OWNER}}` | `governance.process_owner` (split de `Nome · Cargo`) |
| `{{PROCESS_OWNER_CARGO}}` | (idem, parte 2) |
| `{{MISSAO_PROCESSO}}` | MD seção 4.1 (linha após "### 4.1 · Missão") |
| `{{TEXTO_INTERFACES}}` | MD seção 4.3 (parágrafos após "### 4.3 · Interfaces") |

### Conteúdo das 10 seções — vem do MD da Fase 2 (~104 placeholders)

Mapeamento entre seção MD e placeholders:

| Seção MD (h2) | Placeholders gerados |
|---------------|----------------------|
| `## 1. Objetivo` | `TEXTO_OBJETIVO_P1`, `TEXTO_OBJETIVO_P2` (2 parágrafos) |
| `## 2. Escopo` | `LEDE_ESCOPO`, `ESCOPO_INCLUSAO_1..3`, `ESCOPO_EXCLUSAO_1..3` |
| `## 3. Definições` | `DEF_TERMO_1..10`, `DEF_TEXTO_1..10` (tabela 2 col, máx 10) |
| `## 4. Visão Geral` | `LEDE_VISAO_GERAL`, `MISSAO_PROCESSO`, SIPOC (`SIPOC_S_1..3`, `SIPOC_I_1..3`, `SIPOC_P_1..4`, `SIPOC_O_1..3`, `SIPOC_C_1..3`), `TEXTO_INTERFACES` |
| `### 4.4 · Fluxograma BPMN` | `BPMN_DIAGRAMA_TITULO`, `BPMN_CAPTION`, `BPMN_EVT_INICIO`, `BPMN_TASK_1..4`, `BPMN_GATEWAY_1`, `BPMN_EVT_FIM_1`, `BPMN_EVT_FIM_2`, `BPMN_NARRATIVA_1..3` |
| `## 5. Regras de Negócio` | `LEDE_REGRAS`, `REGRAS_TEMA_1`, `REGRAS_TEMA_2`, `REGRA_01..06`, `EXCECAO_1`, `APROVADOR_EXCECAO_1`, `EXCECAO_2`, `APROVADOR_EXCECAO_2` |
| `## 6. Papéis e Responsabilidades` | `LEDE_PAPEIS`, `RACI_PAPEL_1..5`, `RACI_ATIV_1..5` |
| `## 7. Indicadores` | `LEDE_INDICADORES`, KPIs (`KPI_1..2_NOME/FORMULA/META/FREQ/FONTE`), PPIs (`PPI_1..2_NOME/FORMULA/META/FREQ/FONTE`) |
| `## 8. Cronograma` | `LEDE_CRONOGRAMA`, `CRONO_DIARIO_RITUAL/OUT`, `CRONO_SEMANAL_RITUAL/OUT`, `CRONO_MENSAL_RITUAL/OUT`, `CRONO_TRIMESTRAL_RITUAL/OUT`, `CRONO_SEMESTRAL_RITUAL/OUT` |
| `## 9. Critérios de Qualidade` | `LEDE_QUALIDADE`, `DTO_01..05` |
| `## 10. Documentos Relacionados` | `REL_CODIGO_1..4`, `REL_NOME_1..4`, `REL_TIPO_1..4`, `CODIGO_ESP` |
| (footer) | `ALTERACOES_VERSAO` (controle de versões) |

Placeholders sem dado correspondente ficam com **string vazia**. O CSS trata graciosamente e o `_strip_empty_slots()` remove rows vazias.

## Inline de assets (autocontido)

O script substitui antes da expansão de placeholders:

| Asset | Como é inlinado |
|-------|-----------------|
| `m7-tokens.css` | `<link rel="stylesheet" href="m7-tokens.css">` → `<style>...</style>` |
| 6 fonts TWK Everett OTF (~1MB total) | dentro do CSS inlinado, `url("fonts/X.otf")` → `url(data:font/otf;base64,...)` |
| 3 logos (m7-logo-dark.png, offwhite, favicon) | `assets/m7-logo-*.png` → `data:image/png;base64,...` |

Resultado: HTML ~1.5MB sem nenhum `<link>` externo ou `<img src="assets/">` — abre standalone em qualquer browser.

## Validações automáticas

Antes de gerar o HTML, o script valida:

- [ ] Todos os `required` do schema preenchidos
- [ ] `identity.code` casa `^MAN-[A-Z]{2,4}-[0-9]{3}$` (skill-específico)
- [ ] `identity.tipo` == `MAN`
- [ ] `identity.area` ∈ `{GOV, PERF, INV, CRE, SEG, UNI, TEC, PES}`
- [ ] `identity.status` ∈ `{vigente, revisao, rascunho, pendente, vencido}`
- [ ] `identity.version` casa `v?\d+\.\d+`
- [ ] `lifecycle.revisaoFreq` == `Semestral` (warning se diferente)
- [ ] Status ∈ `{vigente, revisao, vencido}` ⇒ `lifecycle.date` e `nextReview` obrigatórios
- [ ] `governance.parent.code` (se objeto) casa pattern
- [ ] `governance.processos[]` casam `G1-G4 | P1-P12 | A1-A5`
- [ ] `governance.aprovador_role` == `Head de área` (warning se diferente)

Após a substituição:
- [ ] Zero placeholders `{{}}` residuais
- [ ] Zero `href="assets/`, `href="fonts/`, `href="m7-tokens.css"` (paths relativos)
- [ ] Zero `<style>` extra além do bloco principal
- [ ] Zero `style="..."` inline
- [ ] Toda classe CSS no HTML pertence à allowlist

Falha em qualquer item aborta a geração com mensagem clara.

## Conflito YAML × HTML

Se você editar o HTML manualmente e divergir do YAML, **vence o YAML**: regere o
HTML rodando o script de novo. Nunca tente "sincronizar manualmente".

## Marcação leniente no MD

O parser aceita variações:

- **Escopo "Aplica-se a"**: tanto `**Aplica-se a:**` (bold) quanto `### Aplica-se a` (heading h3). Idem "Não se aplica a".
- **Subseções numeradas**: aceita prefixo numérico opcional, ex.: `### 4.1 · Missão do processo` ou `### Missão do processo`.
- **Bold/itálico/code/link em campos de texto**: `**bold**`, `*itálico*`, `` `code` ``, `[texto](url)` funcionam em TODOS os campos.

## Shortcodes válidos no MD

A skill aceita os 6 shortcodes herdados de creating-politica + 1 novo manual-específico:

| Shortcode | Quando usar | Output (classes) |
|-----------|-------------|------------------|
| `:::papel-card` | Cards narrativos de papéis com sub-tópicos | `.inv-card`, `.inv-title`, `.inv-owner`, `.inv-block` |
| `:::callout` (`-info` / `-alerta` / `-exemplo`) | Destaque visual de conceito-chave | `.callout`, `.callout-title`, `.callout-tag` |
| `:::indicador` | Card alternativo à tabela 4-col para KPI/PPI | `.indicador-card`, `.indicador-nome`, `.indicador-meta` |
| `:::diagrama` | Embedding de SVG inline (BPMN, fluxos) | `.embed-svg`, `.embed-svg-caption` |
| `:::processo-grid` | Grid 4-col de processos com camada | `.skill-proc-*`, `.skill-camada-*` |
| `:::raci` | **Novo** — matriz RACI 5×5 colorida | `.raci-matrix`, `.raci-r`, `.raci-a`, `.raci-c`, `.raci-i` |

Para detalhes completos: [component-catalog-manual.md](component-catalog-manual.md).

## CSS customizado no MD — PROIBIDO

Em v1.0 o script rejeita o MD se encontrar:

- `<style>...</style>` em qualquer lugar do MD
- `style="..."` inline em qualquer tag
- `<div class="X">`, `<span class="X">` etc com `X` fora da allowlist
- `<svg>` solto (precisa estar dentro de `:::diagrama`)

Por quê é assim: a despadronização visual entre normativos vem exatamente da
falta dessa regra. Manual M7 deve parecer Manual M7 — não cada autor inventando
seu mini-design system.
