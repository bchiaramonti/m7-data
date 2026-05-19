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
│   └── normativo.exemplo-pol-gov-002.yaml      ← exemplo preenchido (POL-GOV-002)
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

**REGRA CRÍTICA**: NUNCA recrie o template do zero. SEMPRE use `politica-m7-template.html`
como base — ele tem 145 placeholders `{{...}}` explícitos cobrindo identidade + conteúdo.
A estrutura (16 páginas A4 — Capa, Controle, 8 seções, versões, aprovações), classes CSS
e tags semânticas são INVARIANTES.

**Geração autocontida** (v2.1): o script inlina CSS, fonts (base64) e logos (base64) no
HTML, produzindo arquivo único de ~1.4MB que funciona em `file://`, HTTP e anexo de email
sem dependência de paths relativos.

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

O MD segue **estrutura estrita** — h2 numerados, blocos específicos por seção. A partir da v2.3 o parser aceita variações lenientes (vide [normativo-schema.md → Marcação leniente](references/normativo-schema.md#marcação-leniente-no-md-v23)):

- `**Aplica-se a:**` (bold) OU `### Aplica-se a` (h3) — ambos casam para Escopo
- `### 7.1 · Revisão periódica` (com prefixo) OU `### Revisão periódica` — idem para Vigência
- `**bold**`, `*itálico*`, `` `code` ``, `[texto](url)` funcionam em **todos** os campos de texto, não só Diretrizes
- `<!-- /page-break -->` na seção 5 quebra Diretrizes em múltiplas páginas A4

A partir da v3.0:

- **Namespaces CSS reservados**: `.skill-proc-*` (grid compacto), `.inv-*` (cards verticais narrativos), `.embed-svg` (wrappers de SVG), além de `.approval-card`/`.kv-table`/`.doc-table`/`.sub`/`.subsub`. **Não sobrescreva**. Para custom CSS use prefixos próprios. Detalhes e exemplos HTML em [normativo-schema.md → Namespaces CSS reservados](references/normativo-schema.md#namespaces-css-reservados-pelo-template-v30).
- **Page-break com alerta**: o script estima a altura de cada chunk de Diretrizes e avisa no stderr quando excede ~900px (margem de segurança), indicando onde adicionar `<!-- /page-break -->` extras.

A partir da v3.1:

- **SVG inline preservado**: cole `<svg viewBox="..." xmlns="...">...</svg>` no MD livremente — o parser faz stash/restore para evitar que a markdown lib serialize o conteúdo do SVG como prosa. Combine com `.embed-svg` para wrap visual.
- **Tabela markdown após bloco HTML é auto-isolada**: você pode escrever `<div class="inv-card">...</div>` imediatamente seguido de uma tabela markdown — o script injeta a linha em branco que a python-markdown precisa para reconhecer o limite. Sem ajuste manual.
- **`links.artifact_md`** opcional: aponta para o MD da Fase 2 (fonte editável). Convenção: `{basename}.md` no mesmo dir que `.html` + `.yaml`. Útil pro cockpit oferecer "abrir fonte".

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

### Fase 3 — Produção HTML + YAML

**Objetivo**: emitir o par .html + .yaml final.
**Input**: BRIEFING-{CODE}.md (+ opcional politica-{slug}.md)
**Output**: par `{slug}.html` + `{slug}.yaml` (basename idêntico).

**Execução**: invocação única do script:

```bash
python scripts/generate-html-yaml.py \
  --briefing  <path>/BRIEFING-POL-GOV-003.md \
  --output-dir <dir> \
  [--content <path>/politica-foo.md] \
  [--basename politica-foo]
```

Pergunte ao usuário onde salvar (sugestões abaixo) e passe via `--output-dir`.

**O que o script faz** (determinístico — mesmo input ⇒ mesmo output):

1. Parseia o BRIEFING como YAML
2. **Valida** contra `normativo.schema.yaml` (aborta com mensagem clara se faltar campo required, status inválido, código fora do padrão, etc.)
3. Serializa o YAML canônico em `{slug}.yaml`
4. Parseia `politica-{slug}.md` extraindo blocos das 8 seções para placeholders de conteúdo
5. Constrói dicionário de **145 placeholders** → valores (identidade + datas + governança + cover título + 8 seções). DOC_REL suporta até 10 entradas dinamicamente (v3.2+); `governance.parent: null` recebe fallback "N/A · Política raiz da hierarquia normativa M7" (v3.2+).
6. Carrega `assets/politica-m7-template.html` (versão isolada, com `{{...}}` explícitos)
7. **Inlinea CSS + 6 fonts + 3 logos** como base64 dentro do HTML
8. Aplica `html.replace("{{KEY}}", value)` para cada um dos 145 placeholders
9. **Auto-cleanup de slots vazios (v3.2+)**: remove `<div class="principle">`, `<tr>` de Papéis e `<tr>` de DOC_REL que ficaram com placeholders vazios após substituição. Se DOC_REL fica com zero linhas, injeta fallback row informativa. Idempotente — autor não precisa se preocupar em preencher slots não usados.
10. Valida zero placeholders residuais e zero paths relativos
11. Salva `{slug}.html` autocontido (~1.4MB)

**Locais sugeridos para output**:
- `01-fundacao-2.1/normativos/catalogo/` (alinhado com Cockpit de Normativos)
- `2-areas/m7/policies/normativos/` (repositório oficial vault)
- `1-projects/<projeto>/` (vinculado a projeto ativo)

---

# Validações da Fase 3 (automáticas)

O script aborta com erro se:

- [ ] Faltar qualquer campo `required` do schema
- [ ] `identity.code` não casa `^(POL|MAN|INS|ESP)-[A-Z]{2,4}-[0-9]{3}$`
- [ ] `identity.tipo` ≠ POL/MAN/INS/ESP
- [ ] `identity.area` fora do enum
- [ ] `identity.status` fora do enum
- [ ] `identity.classif` fora do enum
- [ ] `identity.version` não casa `v?\d+\.\d+`
- [ ] `lifecycle.revisaoFreq` fora do enum
- [ ] Status ∈ {vigente, revisao, vencido} sem `lifecycle.date` ou `nextReview`
- [ ] `governance.parent.code` (se objeto) inválido
- [ ] Item de `governance.processos` fora do padrão `G1-G4 | P1-P12 | A1-A5`
- [ ] Anchor não encontrado no template (sinaliza divergência template × script)

# Validações manuais antes de entregar

Após o script rodar:

- [ ] Abrir o HTML no browser e validar visualmente (capa, controle, 8 seções)
- [ ] Conferir que `identity.code` aparece corretamente em todos os anchors
- [ ] Conferir que aprovador é Diretoria
- [ ] Conferir que revisaoFreq = Anual
- [ ] Editar conteúdo narrativo das páginas 3-15 (limitação atual)
- [ ] Validar que o cockpit reconhece o par (se aplicável)

# Regras Importantes

1. **Nível estratégico** — POL define "por quê" e "dentro de quais limites", NUNCA "como fazer"
2. **Aprovação pela Diretoria** — `governance.aprovador_role` = Diretoria SEMPRE
3. **Revisão Anual** — `lifecycle.revisaoFreq` = Anual SEMPRE
4. **Referências por código** — em `parent.code`, em "Documentos relacionados", em texto narrativo: usar `POL-XXX-NNN`, nunca "Política de X"
5. **Estrutura invariante** — não altere ordem de páginas, classes CSS, tags. Só preencha valores.
6. **YAML é canônico** — em conflito YAML×HTML, regere o HTML rodando o script

# Anti-Patterns

- **Nunca detalhar procedimentos** — "Acesse o sistema X e clique em Y" é INS, não POL
- **Nunca omitir princípios** — Toda política precisa de fundamentos filosóficos
- **Nunca criar sem Governança** — Se não tem como medir aderência, a política é letra morta
- **Nunca usar aprovador abaixo da Diretoria** — POL exige aprovação no nível mais alto
- **Nunca pular o gate de Fase 1** — Fase 2 não inicia sem BRIEFING confirmado
- **Nunca alterar o template oficial** — Para mudar a forma, abra uma issue/iteração separada
- **Nunca editar o YAML para "combinar" com edição manual no HTML** — vence o YAML, regere o HTML
