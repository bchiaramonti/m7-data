---
name: creating-manual
description: >
  Cria documentos do tipo Manual (MAN) para a M7 Investimentos como trio
  {slug}.html (renderização A4 paginada com identidade M7-2026) +
  {slug}.yaml (sidecar canônico consumido pelo Cockpit de Normativos) +
  {slug}.review.md (relatório do design review). Segue 100% o template
  oficial e as diretrizes da POL-PERF-001, com 3 fases nomeadas: Discovery,
  Redação MD e Produção HTML+YAML.
  Use when the user asks to create a manual, write a MAN document, draft a
  manual operacional, create normative manual, ou menciona manual M7,
  manual de processo, manual de operação, rituais de gestão, MAN-XXX-NNN,
  documento tático, manual para o cockpit, sidecar YAML de manual, ou
  precisa de um documento tático que define O QUE FAZER e O QUE ESPERAR
  com BPMN, SIPOC, RACI, KPIs e cronograma.
user-invocable: true
---

# Criação de Manual (MAN) — M7 Investimentos

Crie documentos de **Manual** (nível tático da hierarquia normativa M7)
como **trio `{slug}.html` + `{slug}.yaml` + `{slug}.review.md`**, seguindo
100% o template oficial e as diretrizes da POL superior (tipicamente
POL-PERF-001 ou equivalente da área).

## Filosofia

**"Um manual responde: O QUE FAZER e O QUE ESPERAR."**

O Manual é o nível tático da hierarquia normativa. Ele:
1. **Descreve o processo** — visão macro, entradas, saídas, interfaces (SIPOC + BPMN)
2. **Define regras de negócio** — critérios de decisão, limites, exceções permitidas
3. **Atribui papéis via RACI** — quem é Responsible, Accountable, Consulted, Informed
4. **Estabelece indicadores duplos** — KPIs (resultado) e PPIs (processo)
5. **Define cronograma de rituais** — cadências diária/semanal/mensal/trimestral/semestral
6. **Mede qualidade via DTO** — critérios mensuráveis de aceite
7. **NÃO detalha passos operacionais** — isso é papel da Instrução (INS)
8. **NÃO detalha cálculos técnicos** — isso é papel da Especificação (ESP)

## Princípio de Geração

Cada MAN é entregue como **três arquivos com mesmo basename**:

```
artefatos/
├── MAN-PERF-003.html       ← renderização humana (template invariante M7-2026)
├── MAN-PERF-003.yaml       ← identidade canônica (Cockpit consome só YAMLs)
└── MAN-PERF-003.review.md  ← relatório do design reviewer (gate obrigatório)
```

- O **YAML é a fonte canônica**. Em conflito YAML × HTML, regere o HTML.
- O **HTML é estrutura invariante** — a skill nunca altera ordem de páginas,
  classes CSS ou tags. Só preenche valores nos placeholders.
- O **Cockpit de Normativos** consome só os YAMLs.

## Contexto Normativo

- **Código**: `MAN-[AREA]-[NNN]`
- **Aprovador formal**: Head de área (fixo para MAN)
- **Frequência de revisão**: Semestral (fixo para MAN)
- **Público-alvo**: Gestores e líderes da área
- **Documento superior**: POL da área (ex.: POL-PERF-001 para manuais de Performance)
- **Documentos subordinados**: INSs (instruções operacionais) e ESPs (especificações técnicas)

Consulte [normative-standards.md](references/normative-standards.md) e
[manual-schema.md](references/manual-schema.md) para detalhes.

## Assets e References (autocontidos)

```
creating-manual/
├── SKILL.md                                    ← este arquivo
├── references/
│   ├── normative-standards.md                  ← hierarquia normativa, codificação, ciclo de vida
│   ├── manual-schema.md                        ← guia do schema YAML + 149 placeholders
│   ├── normativo.schema.yaml                   ← schema canônico do sidecar (compartilhado POL/MAN/INS/ESP)
│   ├── normativo.exemplo-man-perf-003.yaml     ← exemplo preenchido (MAN-PERF-003)
│   ├── component-catalog-manual.md             ← 7 shortcodes do MD + allowlist de classes CSS
│   ├── manual-design-rules.md                  ← 9 dimensões de revisão (usado pelo agente)
│   └── reference-output/                       ← gold reference (MAN-PERF-003-gold.{html,yaml,md})
├── assets/
│   ├── manual-m7-template.html                 ← template oficial (149 placeholders {{...}}, 11 páginas A4)
│   ├── m7-tokens.css                           ← design tokens M7-2026 (inlinado pelo script)
│   ├── fonts/                                  ← 6 TWK Everett OTF (inlinados base64)
│   ├── m7-logo-dark.png                        ← logo fundo claro (inlinado base64)
│   ├── m7-logo-offwhite.png                    ← logo fundo escuro (inlinado base64)
│   └── m7-logo-favicon.png                     ← favicon (inlinado base64)
└── scripts/
    └── generate-html-yaml.py                   ← pipeline da Fase 3 (validação + inline + render)
```

Agente associado (no plugin):

```
m7-normativos/agents/
├── governance-writer.md                        ← assistente de redação (compartilhado)
└── manual-design-reviewer.md                   ← gate obrigatório de design review (v1.0)
```

**REGRA CRÍTICA**: NUNCA recrie o template do zero. SEMPRE use `manual-m7-template.html`
como base — ele tem 149 placeholders `{{...}}` explícitos cobrindo identidade +
conteúdo procedural (BPMN, SIPOC, RACI, KPI/PPI, Cronograma, DTO). A estrutura
(11 páginas A4 — Capa, Controle+Sumário, Objetivo+Escopo, Definições, Visão Geral,
BPMN, Regras, Papéis, Indicadores, Cronograma+Qualidade, Docs+Versões+Aprovações),
classes CSS e tags semânticas são INVARIANTES.

**Geração autocontida** (v1.0+): o script inlina CSS, fonts (base64) e logos (base64)
no HTML, produzindo arquivo único de ~1.5MB que funciona em `file://`, HTTP e anexo
de email sem dependência de paths relativos.

**Separação rígida design × conteúdo** (v1.0+): o MD da Fase 2 é canônico de
**conteúdo**, nunca de design. Toda apresentação visual vem do template e dos
shortcodes pré-aprovados em [component-catalog-manual.md](references/component-catalog-manual.md).
O MD **não pode** conter `<style>`, `style="..."` inline, nem classes CSS ad-hoc —
o script rejeita esses casos antes de renderizar.

---

# Workflow — 3 fases

## Parte A · Discovery

### Fase 1 — Entrevista guiada pelo schema

**Objetivo**: capturar todos os campos do sidecar YAML antes de qualquer redação.
**Output**: `BRIEFING-{CODE}.md` (estruturado, persistido em disco).
**Gate**: o usuário deve revisar e confirmar o BRIEFING antes da Fase 2.

Estrutura da entrevista — uma pergunta por vez, infira defaults inteligentes:

| Bloco YAML | Campos coletados | Defaults MAN |
|------------|------------------|--------------|
| `identity` | code, area, version, status, classif, pages | tipo=MAN; tipo_label=Manual; version=v1.0; status=rascunho; classif=Interno; pages=11 |
| `lifecycle` | date, nextReview, revisaoFreq | nextReview = date + 6 meses; revisaoFreq=Semestral (fixo) |
| `governance` | escopo, owner, elaboradoPor, aprovadoPor, parent{code,title}, processos, process_owner, nome_processo, codigo_processo | aprovador_role=Head de área (fixo); escopo auto-deriva quando ausente |
| `presentation` | title_short, title_full.parts (com `accent`), subtitle, lede, eyebrow_categoria | eyebrow_categoria="Manual operacional"; page_label_section ← area_label |
| `structure.toc` | lista das 11 páginas A4 | template padrão |
| `links.siblings` | irmãos do mesmo projeto/processo (tabs do shell) | opcional |

**`governance.escopo`** para MAN: o caso padrão é `processo` (manual de UM
processo macro). `transversal` (cruza múltiplos processos) ou `holding`
(institucional) são casos atípicos. Detalhes em
[manual-schema.md](references/manual-schema.md#governanceescopo-—-alocação-na-matriz-do-cockpit).

**Campos manual-específicos novos**:
- `governance.nome_processo`: nome do processo descrito (ex.: "Rituais de Gestão")
- `governance.codigo_processo`: código interno (ex.: "G2.3")
- `governance.process_owner`: dono do processo (formato "Nome · Cargo")

**Formato do BRIEFING.md**: bloco único de YAML em fence ```yaml ... ```
ou frontmatter `--- ... ---` no topo. Aceita-se também arquivo `.yaml` puro.

**Gate de saída (Fase 1 → Fase 2)**:
- Todos os campos `required` do schema preenchidos
- Resumo apresentado e **explicitamente confirmado** pelo usuário
- Sem confirmação, a skill NÃO avança

---

## Parte B · Produção

### Fase 2 — Redação MD (conteúdo das 10 seções)

**Objetivo**: produzir o conteúdo narrativo das 10 seções no formato estruturado
que mapeia 1:1 para os ~110 placeholders de conteúdo do template.
**Input**: `BRIEFING-{CODE}.md`
**Output persistido**: `manual-{slug}.md` (editável, parser-friendly).

O MD segue **estrutura estrita** — h2 numerados 1-10, blocos específicos por seção.

#### MD é canônico de conteúdo, não de design

A v1.0 aplica **separação rígida** entre conteúdo (MD) e apresentação
(template + shortcodes). O script valida o MD ANTES de gerar e rejeita:

| Bloqueado no MD | Por quê | Use no lugar |
|-----------------|---------|--------------|
| `<style>...</style>` | Design vem do template/tokens, não do MD | Shortcode do catálogo |
| `style="..."` inline | Idem | Shortcode ou markdown padrão |
| `<svg>...</svg>` solto | SVG precisa de wrapper canônico | `:::diagrama ... :::` |
| `<div class="X">` com `X` fora da allowlist | Cada classe deve ter semântica catalogada | Shortcode correspondente |
| `:::nome` fora do catálogo | Só shortcodes pré-aprovados | Ver `component-catalog-manual.md` |

#### Shortcodes semânticos do MD (7 disponíveis)

| Shortcode | Quando usar | Output (classes) |
|-----------|-------------|------------------|
| `:::papel-card` | Seção 6 · cards narrativos de papéis com sub-tópicos | `.inv-card`, `.inv-title`, `.inv-owner`, `.inv-block` |
| `:::papel-card-separador` | Separador de camada antes de grupo de cards | `.inv-sep`, `.inv-sep-title`, `.inv-sep-desc` |
| `:::callout` (`-info` / `-alerta` / `-exemplo`) | Destaque visual de conceito-chave | `.callout`, `.callout-title`, `.callout-tag` |
| `:::indicador` | Seção 7 · card alternativo à tabela para KPI/PPI complexo | `.indicador-card`, `.indicador-nome`, `.indicador-meta` |
| `:::diagrama` | Embedding de SVG inline (BPMN auxiliar, fluxograma) | `.embed-svg`, `.embed-svg-caption` |
| `:::processo-grid` | Grid compacto 4-col de processos com camada | `.skill-proc-*`, `.skill-camada-*` |
| `:::raci` | Matriz RACI 5×5 adicional (a RACI principal usa placeholders do template) | `.raci-table`, `.raci-cell`, `.raci-r/a/c/i` |

Detalhes completos em [component-catalog-manual.md](references/component-catalog-manual.md).

**Para adicionar shortcode novo**: processo formal em
[component-catalog-manual.md](references/component-catalog-manual.md#como-adicionar-um-shortcode-novo-processo-formal).

Estrutura canônica:

```markdown
# {{Título do Manual}}

## 1. Objetivo

Este manual orienta... (1º parágrafo → TEXTO_OBJETIVO_P1)

Continua... (2º parágrafo → TEXTO_OBJETIVO_P2)

## 2. Escopo

Lede... (LEDE_ESCOPO)

**Aplica-se a:**
- Item 1 → ESCOPO_INCLUSAO_1
- Item 2 → ESCOPO_INCLUSAO_2
- Item 3 → ESCOPO_INCLUSAO_3

**Não se aplica a:**
- Item 1 → ESCOPO_EXCLUSAO_1
- ...

## 3. Definições

| Termo | Definição |
|-------|-----------|
| ... | ... → DEF_TERMO_1 / DEF_TEXTO_1
(até 10 linhas → DEF_TERMO_10 / DEF_TEXTO_10)

## 4. Visão Geral do Processo

(lede opcional → LEDE_VISAO_GERAL)

### 4.1 · Missão do processo

(parágrafo → MISSAO_PROCESSO)

### 4.2 · SIPOC

| Suppliers | Inputs | Process | Outputs | Customers |
|-----------|--------|---------|---------|-----------|
| S1 | I1 | P1 | O1 | C1
| S2 | I2 | P2 | O2 | C2
| S3 | I3 | P3 | O3 | C3
| (linha 4 só para Process P4) |  | P4 |  | 

### 4.3 · Interfaces e dependências

(parágrafo → TEXTO_INTERFACES)

### 4.4 · Fluxograma BPMN

:::diagrama
caption: Fig 1 · Fluxograma BPMN
<svg viewBox="...">...</svg>
:::

**Narrativa do fluxo:**

1. (parágrafo → BPMN_NARRATIVA_1)
2. (parágrafo → BPMN_NARRATIVA_2)
3. (parágrafo → BPMN_NARRATIVA_3)

## 5. Regras de Negócio

(lede → LEDE_REGRAS)

### 5.1 · {Tema 1} (REGRAS_TEMA_1)

1. **RN-01** · ... → REGRA_01
2. **RN-02** · ... → REGRA_02
3. **RN-03** · ... → REGRA_03

### 5.2 · {Tema 2} (REGRAS_TEMA_2)

4. **RN-04** · ... → REGRA_04
5. **RN-05** · ... → REGRA_05
6. **RN-06** · ... → REGRA_06

### 5.3 · Exceções permitidas

| Exceção | Aprovador |
|---------|-----------|
| ... | ... → EXCECAO_1 / APROVADOR_EXCECAO_1
| ... | ... → EXCECAO_2 / APROVADOR_EXCECAO_2

## 6. Papéis e Responsabilidades

(lede → LEDE_PAPEIS)

### 6.1 · Matriz RACI

| Atividade | {Papel 1} | {Papel 2} | {Papel 3} | {Papel 4} | {Papel 5} |
|-----------|-----------|-----------|-----------|-----------|-----------|
| ...     | R/A/C/I  | ...     | ...     | ...     | ...
(5 linhas → RACI_ATIV_1..5; header → RACI_PAPEL_1..5)

## 7. Indicadores

(lede → LEDE_INDICADORES)

### 7.1 · KPIs

| Nome | Fórmula | Meta | Frequência | Fonte |
|------|---------|------|------------|-------|
| ... | ... | ... | ... | ... → KPI_1_*
| ... | ... | ... | ... | ... → KPI_2_*

### 7.2 · PPIs

| Nome | Fórmula | Meta | Frequência | Fonte |
|------|---------|------|------------|-------|
| ... | ... | ... | ... | ... → PPI_1_*
| ... | ... | ... | ... | ... → PPI_2_*

## 8. Cronograma e Frequência

(lede → LEDE_CRONOGRAMA)

| Cadência | Ritual / Atividade | Output |
|----------|--------------------|--------|
| Diária | ... | ... → CRONO_DIARIO_*
| Semanal | ... | ... → CRONO_SEMANAL_*
| Mensal | ... | ... → CRONO_MENSAL_*
| Trimestral | ... | ... → CRONO_TRIMESTRAL_*
| Semestral | ... | ... → CRONO_SEMESTRAL_*

## 9. Critérios de Qualidade

(lede → LEDE_QUALIDADE)

1. **DTO-01** — ... → DTO_01
2. **DTO-02** — ... → DTO_02
3. **DTO-03** — ... → DTO_03
4. **DTO-04** — ... → DTO_04
5. **DTO-05** — ... → DTO_05

## 10. Documentos Relacionados

| Código | Título | Tipo |
|--------|--------|------|
| POL-PERF-001 | Política de Performance | Documento superior → REL_*_1
| INS-PERF-001 | ... | Subordinado → REL_*_2
| ESP-PERF-001 | ... | Subordinado → REL_*_3 (CODIGO_ESP)
| ... | ... | ... → REL_*_4

---

**Controle de Versões**

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| v1.0 | DD/MM/AAAA | [Autor] | Versão inicial. → ALTERACOES_VERSAO
```

**Limites de slot do template**:
- 10 definições · 6 regras · 5 papéis RACI · 2 KPIs · 2 PPIs · 5 cadências · 5 DTOs · 4 docs relacionados
- Se o autor exceder qualquer limite, conteúdo extra é silenciosamente ignorado pelo script. Avise-o ao revisar o BRIEFING/MD.

**Gate de saída (Fase 2 → Fase 3)**:
- MD revisado pelo usuário
- Estrutura conforme — h2 numerados, blocos identificáveis
- `identity.pages` no BRIEFING confirmado (11 default)

### Fase 3 — Produção HTML + YAML + Review

**Objetivo**: emitir o **trio** `.html` + `.yaml` + `.review.md` final.
**Input**: BRIEFING-{CODE}.md (+ opcional manual-{slug}.md)
**Output**: trio com basename idêntico — HTML autocontido, YAML sidecar,
e relatório de design review (preenchido pelo agente).

**Execução em 2 passos**:

**Passo 1 — Rodar o script** (geração mecânica determinística):

```bash
python scripts/generate-html-yaml.py \
  --briefing  <path>/BRIEFING-MAN-PERF-003.md \
  --output-dir <dir> \
  [--content <path>/manual-rituais-de-gestao.md] \
  [--basename MAN-PERF-003]
```

O script faz (determinístico — mesmo input ⇒ mesmo output):

1. Parseia o BRIEFING como YAML
2. **Valida YAML** contra `normativo.schema.yaml` (aborta com mensagem clara
   se faltar campo required, status inválido, código fora do padrão, etc.)
3. Serializa o YAML canônico em `{slug}.yaml`
4. **Valida MD** (v1.0): rejeita `<style>`, `style="..."`, `<svg>` solto,
   classes ad-hoc fora do component-catalog-manual, shortcodes inválidos
5. **Expande shortcodes** (`:::papel-card`, `:::callout`, `:::indicador`,
   `:::diagrama`, `:::processo-grid`, `:::raci`)
6. Parseia `manual-{slug}.md` extraindo blocos das 10 seções para placeholders
7. Constrói dicionário de **149 placeholders** → valores
8. Carrega `assets/manual-m7-template.html`
9. **Inlinea CSS + 6 fonts + 3 logos** como base64 dentro do HTML
10. Aplica `html.replace("{{KEY}}", value)` para cada um dos 149 placeholders
11. **Auto-cleanup de slots vazios**: remove `<li>` vazios em SIPOC, `<tr>` com
    todas as cells vazias em docs relacionados, cards KPI/PPI sem nome
12. **Valida HTML final** (v1.0): zero `{{}}` residuais, zero paths relativos,
    **zero classes fora da allowlist**, **no máximo 2 `<style>` blocks**, **zero
    `style="..."` inline extras**
13. Salva `{slug}.html` autocontido (~1.5MB) + `{slug}.yaml` + `{slug}.review.md` (stub)

**Passo 2 — Invocar o agente `manual-design-reviewer`** (gate obrigatório):

Imediatamente após o script rodar com sucesso, invoque o agente via Task tool:

```
Task(
  subagent_type="manual-design-reviewer",
  prompt="""Revise o HTML do manual {CODE}.

  HTML:        {output-dir}/{basename}.html
  YAML:        {output-dir}/{basename}.yaml
  MD-fonte:    {path do MD da Fase 2, se houver}
  Code:        {CODE}

  Compare contra references/reference-output/MAN-PERF-003-gold.html e
  manual-design-rules.md (9 dimensões). Produza relatório markdown e
  persista em {output-dir}/{basename}.review.md (sobrescreve o stub).

  Score >= B aprova entrega. Score < B bloqueia."""
)
```

O agente leva ~1-2 minutos, lê os arquivos relevantes, gera o relatório
sobrescrevendo o `.review.md` e retorna o veredito (Score + lista de issues).

**Locais sugeridos para output**:
- `01-fundacao-2.1/normativos/catalogo/` (alinhado com Cockpit de Normativos)
- `2-areas/m7/manuals/normativos/` (repositório oficial vault)
- `1-projects/<projeto>/` (vinculado a projeto ativo)

---

# Validações da Fase 3

## Validações automáticas (mecânicas — script)

O script aborta com erro se:

- [ ] Faltar qualquer campo `required` do schema YAML
- [ ] `identity.code` não casa `^(POL|MAN|INS|ESP)-[A-Z]{2,4}-[0-9]{3}$`
- [ ] `identity.tipo` ≠ POL/MAN/INS/ESP, `area`/`status`/`classif`/`version` fora do enum
- [ ] Status ∈ {vigente, revisao, vencido} sem `lifecycle.date` ou `nextReview`
- [ ] `governance.parent.code` (se objeto) ou `processos[]` inválidos
- [ ] **MD da Fase 2** contém `<style>`, `style="..."` inline, `<svg>` solto,
      classes ad-hoc fora do component-catalog-manual, ou shortcode `:::nome` inválido
- [ ] **HTML final** tem placeholders residuais, paths relativos, classes
      CSS fora da allowlist

**Warnings (não-bloqueantes)**:
- `lifecycle.revisaoFreq` ≠ "Semestral" para tipo=MAN (warning, não erro)
- `governance.aprovador_role` ≠ "Head de área" para tipo=MAN (warning)

## Validação visual (gate de design — agente obrigatório)

Após o script gerar com sucesso, o gate de Score >= B é **obrigatório**:

- [ ] **Invocar `manual-design-reviewer`** com caminho do HTML, YAML, MD e code
- [ ] Agente produz `.review.md` com:
  - Conformidade base (M7-2026 conforme / parcial / fora)
  - Score A / B / C / D
  - Veredito (APROVADO / APROVADO COM RESSALVAS / REPROVADO)
  - Issues categorizadas (CRITICO / ATENCAO / SUGESTAO) em 9 dimensões
  - Quick Fix CSS (se aplicável)
- [ ] **Score < B bloqueia entrega** — corrija o MD/BRIEFING conforme issues
      CRITICO e re-execute o script
- [ ] Score ≥ B entrega o trio completo

## Conferência final pelo autor

Após Score ≥ B:

- [ ] Abrir o HTML no browser e revisar visualmente (capa, 11 seções)
- [ ] Conferir que `identity.code` aparece corretamente em todos os anchors
- [ ] Conferir que aprovador é Head de área
- [ ] Conferir que revisaoFreq = Semestral
- [ ] BPMN renderiza com viewBox (escala em qualquer tela)
- [ ] RACI matrix tem letras textuais visíveis (acessibilidade P&B)
- [ ] KPIs e PPIs têm fórmula + meta + frequência + fonte preenchidos
- [ ] Cronograma tem pelo menos uma cadência preenchida
- [ ] Validar que o cockpit reconhece o par (se aplicável)

# Regras Importantes

1. **Nível tático** — MAN define "o que fazer" e "o que esperar", NUNCA "como fazer passo a passo"
2. **Sempre referencia POL** — Todo MAN tem um documento superior (POL)
3. **Aprovação pelo Head** — `governance.aprovador_role` = Head de área SEMPRE
4. **Revisão Semestral** — `lifecycle.revisaoFreq` = Semestral SEMPRE
5. **RACI obrigatório** — Seção 6.1 deve ter matriz 5×5 com 1 A por linha
6. **Indicadores duplos** — Seção 7 separa KPI (resultado) de PPI (processo)
7. **Referências por código** — em `parent.code`, em "Documentos relacionados", em texto narrativo: usar `MAN-XXX-NNN`, nunca "Manual de X"
8. **Estrutura invariante** — não altere ordem de páginas (11 fixas), classes CSS, tags. Só preencha valores.
9. **YAML é canônico de identidade, MD é canônico de conteúdo, template é canônico de design** — três fontes separadas; em conflito YAML×HTML, regere o HTML
10. **Design não vive no MD** (v1.0) — toda apresentação visual vem do template
    + shortcodes do `component-catalog-manual.md`. Nunca injete `<style>`, `style="..."`
    ou classes ad-hoc no MD da Fase 2.
11. **Gate de design review obrigatório** (v1.0) — sem Score ≥ B do agente
    `manual-design-reviewer`, o manual não está entregue.

# Anti-Patterns

- **Nunca detalhar passos operacionais** — "Abra o sistema X e clique em Y" é INS, não MAN
- **Nunca detalhar cálculos técnicos** — "A fórmula SQL é SELECT..." é ESP, não MAN
- **Nunca omitir POL superior** — Todo MAN nasce de uma POL
- **Nunca criar indicador sem fórmula** — "Medir produtividade" não é indicador
- **Nunca pular Critérios de Qualidade** — Sem DTO, não há como avaliar o processo
- **Nunca usar aprovador abaixo de Head** — MAN exige Head de área
- **Nunca pular o gate de Fase 1** — Fase 2 não inicia sem BRIEFING confirmado
- **Nunca alterar o template oficial** — Para mudar a forma, abra uma issue/iteração separada
- **Nunca editar o YAML para "combinar" com edição manual no HTML** — vence o YAML, regere o HTML
- **Nunca injetar CSS no MD** (v1.0) — `<style>`, `style="..."`, `<div class="...">` ad-hoc são rejeitados. Use shortcodes do catálogo.
- **Nunca pular o agente de design review** (v1.0) — Score < B = bloqueio. Corrija e regere.
- **Nunca adicionar shortcode ad-hoc** — para novo bloco visual, siga o processo formal em `component-catalog-manual.md`.
- **Nunca confundir KPI com PPI** — KPI mede resultado (saída); PPI mede processo (execução).
- **Nunca aprovar RACI inválido** — 0 A por linha = sem accountability; 2+ A = ambiguidade. Ambos são CRITICO.
- **Nunca gerar BPMN sem viewBox** — SVG sem viewBox não escala em A4. Sempre CRITICO.
