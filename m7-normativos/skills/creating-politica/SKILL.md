---
name: creating-politica
description: >
  Cria documentos do tipo Política (POL) para a M7 Investimentos como par
  {slug}.html (renderização A4 paginada com identidade M7-2026) + {slug}.yaml
  (sidecar canônico consumido pelo Cockpit de Normativos). Segue 100% o template
  oficial e as diretrizes da POL-M7-001, com 3 fases nomeadas: Discovery,
  Redação MD e Produção HTML+YAML.
  Use when the user asks to create a policy, write a política, draft a POL document,
  create normative policy, or mentions política corporativa, política de gestão,
  política M7, política para o cockpit, sidecar YAML, or needs a strategic-level
  governance document that defines principles, limits and guidelines.
user-invocable: true
---

# Criação de Política (POL) — M7 Investimentos

Crie documentos de **Política** (nível estratégico da hierarquia normativa M7)
como **par `{slug}.html` + `{slug}.yaml`**, seguindo 100% o template oficial e
as diretrizes da POL-M7-001.

## Filosofia

**"Uma política responde: POR QUÊ fazemos e DENTRO DE QUAIS LIMITES."**

A Política é o nível mais alto da hierarquia normativa. Ela:
1. **Define princípios** — os valores fundamentais que orientam decisões
2. **Estabelece limites** — o que é e o que NÃO é aceitável
3. **Atribui responsabilidades** — quem governa, quem executa, quem fiscaliza
4. **NÃO detalha procedimentos** — isso é papel do Manual (MAN) e da Instrução (INS)

## Princípio de Geração

Cada POL é entregue como **dois arquivos com mesmo basename**:

```
artefatos/
├── politica-foo.html   ← renderização humana (template invariante M7-2026)
└── politica-foo.yaml   ← identidade canônica (10+ anchors do HTML são preenchidos a partir daqui)
```

- O **YAML é a fonte canônica**. Em conflito YAML × HTML, regere o HTML.
- O **HTML é estrutura invariante** — a skill nunca altera ordem de páginas,
  classes CSS ou tags. Só preenche valores nos anchors definidos pelo schema.
- O **Cockpit de Normativos** consome só os YAMLs; cada par .html+.yaml é
  apresentado pelo cockpit como linha da matriz / item da hierarquia.

## Contexto Normativo

- **Código**: `POL-[AREA]-[NNN]`
- **Aprovador formal**: Diretoria (fixo para POL)
- **Frequência de revisão**: Anual (fixo para POL)
- **Público-alvo**: Toda a organização
- **Documento superior**: Outra POL (ex.: POL-GOV-001 é a mãe da hierarquia) ou `null` para a política raiz
- **Documentos subordinados**: MANs, INSs e ESPs que implementam esta política

Consulte [normative-standards.md](references/normative-standards.md) e
[normativo-schema.md](references/normativo-schema.md) para detalhes.

## Assets e References (autocontidos)

```
creating-politica/
├── SKILL.md                                    ← este arquivo
├── references/
│   ├── normative-standards.md                  ← hierarquia normativa, codificação, ciclo de vida
│   ├── normativo-schema.md                     ← guia do schema YAML + tabela placeholder→campo
│   ├── normativo.schema.yaml                   ← schema canônico do sidecar
│   ├── normativo.exemplo-pol-gov-002.yaml      ← exemplo preenchido (POL-GOV-002 — legacy)
│   ├── component-catalog.md                    ← shortcodes do MD + allowlist de classes CSS
│   ├── policy-design-rules.md                  ← 8 dimensões de revisão (usado pelo agente)
│   └── reference-output/                       ← gold reference (POL-GOV-001-gold.{html,yaml,md})
├── assets/
│   ├── politica-m7-template.html               ← template oficial (145 placeholders {{...}})
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
└── politica-design-reviewer.md                 ← gate obrigatório de design review (v4.0)
```

**REGRA CRÍTICA**: NUNCA recrie o template do zero. SEMPRE use `politica-m7-template.html`
como base — ele tem 145 placeholders `{{...}}` explícitos cobrindo identidade + conteúdo.
A estrutura (16 páginas A4 — Capa, Controle, 8 seções, versões, aprovações), classes CSS
e tags semânticas são INVARIANTES.

**Geração autocontida** (v2.1+): o script inlina CSS, fonts (base64) e logos (base64) no
HTML, produzindo arquivo único de ~1.4MB que funciona em `file://`, HTTP e anexo de email
sem dependência de paths relativos.

**Separação rígida design × conteúdo** (v4.0+): o MD da Fase 2 é canônico de
**conteúdo**, nunca de design. Toda apresentação visual vem do template e dos
shortcodes pré-aprovados em [component-catalog.md](references/component-catalog.md).
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

| Bloco YAML | Campos coletados | Defaults POL |
|------------|------------------|--------------|
| `identity` | code, area, version, status, classif, pages (inicial) | tipo=POL; tipo_label=Política; version=v1.0; status=rascunho; classif=Interno; classif_label="Uso interno · Confidencial" |
| `lifecycle` | date, nextReview, revisaoFreq | nextReview = date + 1 ano; revisaoFreq=Anual (fixo) |
| `governance` | **escopo**, owner, elaboradoPor, aprovadoPor, revisor, parent{code,title}, processos | aprovador_role=Diretoria (fixo); escopo auto-deriva quando ausente |
| `presentation` | title_short, title_full.parts (com `accent`), subtitle, lede, eyebrow_categoria, page_label_section | eyebrow_categoria="Documento de governança"; page_label_section ← area_label |
| `structure.toc` | lista inicial de páginas (mín 10: Capa, Controle, 8 seções) | — |
| `links.siblings` | irmãos do mesmo projeto/processo (tabs do shell) | opcional |

**`governance.escopo`** controla onde o documento é alocado na Matriz do Cockpit (`holding | transversal | processo`):

- Para POL institucional da holding → pergunte `escopo: holding` **explicitamente** (nunca auto-derivado por proteção).
- 1 processo único → o script auto-deriva `escopo: processo`.
- 2+ processos sem ser holding → auto-deriva `escopo: transversal`.

Detalhes e os 4 jeitos de alinhar à Holding em [normativo-schema.md](references/normativo-schema.md#governanceescopo-—-alocação-na-matriz-do-cockpit).

**Formato do BRIEFING.md**: bloco único de YAML em fence ```yaml ... ```
ou frontmatter `--- ... ---` no topo. Aceita-se também arquivo `.yaml` puro.

**Gate de saída (Fase 1 → Fase 2)**:
- Todos os campos `required` do schema preenchidos
- Resumo apresentado e **explicitamente confirmado** pelo usuário
- Sem confirmação, a skill NÃO avança

---

## Parte B · Produção

### Fase 2 — Redação MD (conteúdo das 8 seções)

**Objetivo**: produzir o conteúdo narrativo das 8 seções no formato estruturado que
mapeia 1:1 para os ~110 placeholders de conteúdo do template.
**Input**: `BRIEFING-{CODE}.md`
**Output persistido**: `politica-{slug}.md` (editável, parser-friendly).

O MD segue **estrutura estrita** — h2 numerados, blocos específicos por seção. O parser aceita variações lenientes (vide [normativo-schema.md → Marcação leniente](references/normativo-schema.md#marcação-leniente-no-md)):

- `**Aplica-se a:**` (bold) OU `### Aplica-se a` (h3) — ambos casam para Escopo
- `### 7.1 · Revisão periódica` (com prefixo) OU `### Revisão periódica` — idem para Vigência
- `**bold**`, `*itálico*`, `` `code` ``, `[texto](url)` funcionam em **todos** os campos de texto
- `<!-- /page-break -->` na seção 5 quebra Diretrizes em múltiplas páginas A4

#### MD é canônico de conteúdo, não de design (v4.0)

A partir da v4.0 a skill aplica **separação rígida** entre conteúdo (MD) e
apresentação (template + shortcodes). O script valida o MD ANTES de gerar e
rejeita:

| Bloqueado no MD | Por quê | Use no lugar |
|-----------------|---------|--------------|
| `<style>...</style>` | Design vem do template/tokens, não do MD | Shortcode do catálogo |
| `style="..."` inline | Idem — apresentação é classe CSS | Shortcode ou markdown padrão |
| `<svg>...</svg>` solto | SVG precisa de wrapper canônico | `:::diagrama ... :::` |
| `<div class="X">` com `X` fora da allowlist | Cada classe deve ter semântica catalogada | Shortcode correspondente |
| `:::nome` fora do catálogo | Só shortcodes pré-aprovados | Ver `component-catalog.md` |

#### Shortcodes semânticos do MD (5 disponíveis)

Para blocos visuais especiais, use os shortcodes pandoc-fenced abaixo. Cada um
mapeia para um conjunto de classes CSS já presentes no template. Para
sintaxe completa de cada um, ver [component-catalog.md](references/component-catalog.md).

| Shortcode | Quando usar | Output (classes) |
|-----------|-------------|------------------|
| `:::papel-card` | Seção 6 · cards narrativos de papéis com sub-tópicos | `.inv-card`, `.inv-title`, `.inv-owner`, `.inv-block` |
| `:::papel-card-separador` | Separador de camada antes de grupo de cards | `.inv-sep`, `.inv-sep-title`, `.inv-sep-desc` |
| `:::callout` (`-info` / `-alerta` / `-exemplo`) | Destaque visual de conceito-chave | `.callout`, `.callout-title`, `.callout-tag` |
| `:::indicador` | Seção 7 · card alternativo à tabela 4-col | `.indicador-card`, `.indicador-nome`, `.indicador-meta` |
| `:::diagrama` | Embedding de SVG inline (cadeia, fluxograma) | `.embed-svg`, `.embed-svg-caption` |
| `:::processo-grid` | Grid compacto 4-col de processos com camada | `.skill-proc-*`, `.skill-camada-*` |

Sintaxe geral (pandoc fenced divs):

```markdown
:::nome-do-shortcode
chave: valor opcional
outra-chave: outro valor

Corpo em markdown padrão (parágrafos, listas, bold, italic, code, links).
:::
```

Exemplo prático — card de papel na seção 6:

```markdown
:::papel-card
título: P1 · Geração de Demanda
owner: Head de Marketing

**Por que existe**: ativar pipeline de leads qualificados.

**O que transforma**: demanda latente em oportunidade quente.

**Alimenta**: P2 (Qualificação) com leads scored.
:::
```

**Para adicionar shortcode novo**: processo formal em
[component-catalog.md](references/component-catalog.md#como-adicionar-um-shortcode-novo-processo-formal) —
nunca em ad-hoc no MD.

#### Outras facilidades preservadas

- **Imagens externas referenciadas em MD**: `<img src="caminho/relativo.png">`
  é inlinada como `data:image/...;base64` automaticamente pelo script.
- **`links.artifact_md`** opcional: aponta para o MD da Fase 2 (fonte editável).
  Convenção: `{basename}.md` no mesmo dir que `.html` + `.yaml`. Útil pro
  cockpit oferecer "abrir fonte".
- **Page-break com alerta**: o script estima a altura de cada chunk de
  Diretrizes e avisa no stderr quando excede ~900px (margem de segurança),
  indicando onde adicionar `<!-- /page-break -->` extras.

Estrutura canônica:

```markdown
# {{Título da Política}}

## 1. Objetivo

Esta política estabelece... (1º parágrafo → TEXTO_OBJETIVO_P1)

Continua... (2º parágrafo → TEXTO_OBJETIVO_P2)

## 2. Escopo

Esta política aplica-se a... (lede → LEDE_ESCOPO)

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
| Compliance | ... → DEF_TERMO_1 / DEF_TEXTO_1
| Governança | ... → DEF_TERMO_2 / DEF_TEXTO_2
(até 12 linhas → DEF_TERMO_12 / DEF_TEXTO_12)

## 4. Princípios

(lede opcional → LEDE_PRINCIPIOS)

### Transparência
Descrição... → PRINCIPIO_1_TITULO + PRINCIPIO_1_DESCRICAO

### Accountability
... → PRINCIPIO_2_*
(até 7 → PRINCIPIO_7_*)

## 5. Diretrizes

(lede opcional → LEDE_DIRETRIZES)

**Sumário:**
- 5.1 ...
- 5.2 ...
(→ SUMARIO_DIRETRIZES, renderizado como <ul>)

### 5.1 ...
(conteúdo livre — markdown rico → CONTEUDO_DIRETRIZES)

## 6. Papéis & Responsabilidades

(lede opcional → LEDE_PAPEIS)

| Nível | Papel | Responsabilidades |
|-------|-------|-------------------|
| Estratégico | Diretoria | ... → PAPEL_1_*
| Tático | Heads | ... → PAPEL_2_*
(até 8 → PAPEL_8_*)

## 7. Governança

### Revisão periódica

(intro → REVISAO_PERIODICA_INTRO)

- Gatilho 1 → GATILHO_REVISAO_1
- ...
(até 4 → GATILHO_REVISAO_4)

### Indicadores de aderência

| Indicador | Fórmula | Frequência | Meta |
|-----------|---------|------------|------|
| ... | ... | ... | ... → INDICADOR_1_NOME/FORMULA/FREQ/META
(até 5)

### Escalonamento de exceções

| Tipo | Aprovador |
|------|-----------|
| ... | ... → ESCALA_TIPO_1 / ESCALA_APROVADOR_1
(até 6)

## 8. Disposições Finais

### Vigência

(parágrafo → TEXTO_VIGENCIA)

### Documentos relacionados

| Código | Título | Relação |
|--------|--------|---------|
| POL-GOV-001 | ... | ... → DOC_REL_1_*
(somente 1 linha — o template tem slot para apenas 1 doc relacionado)
```

**Limites de slot do template**:
- 12 definições · 7 princípios · 8 papéis · 5 indicadores · 6 exceções · 1 doc relacionado
- Se o autor exceder qualquer limite, conteúdo extra é silenciosamente ignorado pelo script. Avise-o ao revisar o BRIEFING/MD.

**Gate de saída (Fase 2 → Fase 3)**:
- MD revisado pelo usuário
- Estrutura conforme — h2 numerados, blocos identificáveis
- `identity.pages` no BRIEFING atualizado (16 default)

### Fase 3 — Produção HTML + YAML + Review

**Objetivo**: emitir o **trio** `.html` + `.yaml` + `.review.md` final.
**Input**: BRIEFING-{CODE}.md (+ opcional politica-{slug}.md)
**Output**: trio com basename idêntico — HTML autocontido, YAML sidecar,
e relatório de design review (preenchido pelo agente).

**Execução em 2 passos**:

**Passo 1 — Rodar o script** (geração mecânica determinística):

```bash
python scripts/generate-html-yaml.py \
  --briefing  <path>/BRIEFING-POL-GOV-003.md \
  --output-dir <dir> \
  [--content <path>/politica-foo.md] \
  [--basename politica-foo]
```

O script faz (determinístico — mesmo input ⇒ mesmo output):

1. Parseia o BRIEFING como YAML
2. **Valida YAML** contra `normativo.schema.yaml` (aborta com mensagem clara
   se faltar campo required, status inválido, código fora do padrão, etc.)
3. Serializa o YAML canônico em `{slug}.yaml`
4. **Valida MD** (v4.0): rejeita `<style>`, `style="..."`, `<svg>` solto,
   classes ad-hoc fora do component-catalog, shortcodes inválidos
5. **Expande shortcodes** (v4.0): `:::papel-card`, `:::callout`, `:::indicador`,
   `:::diagrama`, `:::processo-grid` viram HTML usando classes da allowlist
6. Parseia `politica-{slug}.md` extraindo blocos das 8 seções para placeholders
7. Constrói dicionário de **145 placeholders** → valores
8. Carrega `assets/politica-m7-template.html`
9. **Inlinea CSS + 6 fonts + 3 logos** como base64 dentro do HTML
10. Aplica `html.replace("{{KEY}}", value)` para cada um dos 145 placeholders
11. **Auto-cleanup de slots vazios**: remove `<div class="principle">`,
    `<tr>` de Papéis e DOC_REL com placeholders vazios. Fallback row em
    DOC_REL se zero linhas.
12. **Valida HTML final** (v4.0): zero `{{}}` residuais, zero paths relativos,
    **zero classes fora da allowlist**, **no máximo 1 `<style>` block**, **zero
    `style="..."` inline**
13. Salva `{slug}.html` autocontido (~1.4MB) + `{slug}.yaml` + `{slug}.review.md` (stub)

**Passo 2 — Invocar o agente `politica-design-reviewer`** (gate obrigatório):

Imediatamente após o script rodar com sucesso, invoque o agente via Task tool:

```
Task(
  subagent_type="politica-design-reviewer",
  prompt="""Revise o HTML da política {CODE}.

  HTML:        {output-dir}/{basename}.html
  YAML:        {output-dir}/{basename}.yaml
  MD-fonte:    {path do MD da Fase 2, se houver}
  Code:        {CODE}

  Compare contra references/reference-output/POL-GOV-001-gold.html e
  policy-design-rules.md (8 dimensões). Produza relatório markdown e
  persista em {output-dir}/{basename}.review.md (sobrescreve o stub).

  Score >= B aprova entrega. Score < B bloqueia."""
)
```

O agente leva ~1-2 minutos, lê os arquivos relevantes, gera o relatório
sobrescrevendo o `.review.md` e retorna o veredito (Score + lista de issues).

**Locais sugeridos para output**:
- `01-fundacao-2.1/normativos/catalogo/` (alinhado com Cockpit de Normativos)
- `2-areas/m7/policies/normativos/` (repositório oficial vault)
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
      classes ad-hoc fora do component-catalog, ou shortcode `:::nome` inválido
- [ ] **HTML final** tem placeholders residuais, paths relativos, classes
      CSS fora da allowlist, mais de um `<style>` block, ou `style="..."` inline

## Validação visual (gate de design — agente obrigatório)

Após o script gerar com sucesso, o gate de Score >= B é **obrigatório**:

- [ ] **Invocar `politica-design-reviewer`** com caminho do HTML, YAML, MD e code
- [ ] Agente produz `.review.md` com:
  - Conformidade base (M7-2026 conforme / parcial / fora)
  - Score A / B / C / D
  - Veredito (APROVADO / APROVADO COM RESSALVAS / REPROVADO)
  - Issues categorizadas (CRITICO / ATENCAO / SUGESTAO)
  - Quick Fix CSS (se aplicável)
- [ ] **Score < B bloqueia entrega** — corrija o MD/BRIEFING conforme issues
      CRITICO e re-execute o script
- [ ] Score ≥ B entrega o trio completo

## Conferência final pelo autor

Após Score ≥ B:

- [ ] Abrir o HTML no browser e revisar visualmente (capa, controle, 8 seções)
- [ ] Conferir que `identity.code` aparece corretamente em todos os anchors
- [ ] Conferir que aprovador é Diretoria
- [ ] Conferir que revisaoFreq = Anual
- [ ] Validar que o cockpit reconhece o par (se aplicável)

# Regras Importantes

1. **Nível estratégico** — POL define "por quê" e "dentro de quais limites", NUNCA "como fazer"
2. **Aprovação pela Diretoria** — `governance.aprovador_role` = Diretoria SEMPRE
3. **Revisão Anual** — `lifecycle.revisaoFreq` = Anual SEMPRE
4. **Referências por código** — em `parent.code`, em "Documentos relacionados", em texto narrativo: usar `POL-XXX-NNN`, nunca "Política de X"
5. **Estrutura invariante** — não altere ordem de páginas, classes CSS, tags. Só preencha valores.
6. **YAML é canônico de identidade, MD é canônico de conteúdo, template é canônico de design** — três fontes separadas; em conflito YAML×HTML, regere o HTML
7. **Design não vive no MD** (v4.0) — toda apresentação visual vem do template
   + shortcodes do `component-catalog.md`. Nunca injete `<style>`, `style="..."`
   ou classes ad-hoc no MD da Fase 2.
8. **Gate de design review obrigatório** (v4.0) — sem Score ≥ B do agente
   `politica-design-reviewer`, a política não está entregue.

# Anti-Patterns

- **Nunca detalhar procedimentos** — "Acesse o sistema X e clique em Y" é INS, não POL
- **Nunca omitir princípios** — Toda política precisa de fundamentos filosóficos
- **Nunca criar sem Governança** — Se não tem como medir aderência, a política é letra morta
- **Nunca usar aprovador abaixo da Diretoria** — POL exige aprovação no nível mais alto
- **Nunca pular o gate de Fase 1** — Fase 2 não inicia sem BRIEFING confirmado
- **Nunca alterar o template oficial** — Para mudar a forma, abra uma issue/iteração separada
- **Nunca editar o YAML para "combinar" com edição manual no HTML** — vence o YAML, regere o HTML
- **Nunca injetar CSS no MD** (v4.0) — `<style>`, `style="..."`, `<div class="...">` ad-hoc são rejeitados. Use shortcodes do catálogo.
- **Nunca pular o agente de design review** (v4.0) — Score < B = bloqueio. Corrija e regere.
- **Nunca adicionar shortcode ad-hoc** — para novo bloco visual, siga o processo formal em `component-catalog.md` (catálogo + template + script + bump de versão).
