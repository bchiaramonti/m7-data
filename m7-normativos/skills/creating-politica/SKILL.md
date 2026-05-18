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
│   ├── normativo-schema.md                     ← guia do schema YAML + tabela anchor→campo
│   ├── normativo.schema.yaml                   ← schema canônico do sidecar
│   └── normativo.exemplo-pol-gov-002.yaml      ← exemplo preenchido (POL-GOV-002)
├── assets/
│   ├── politica-m7-template.html               ← template oficial (estrutura invariante)
│   ├── m7-tokens.css                           ← design tokens M7-2026
│   ├── m7-header-dark.css                      ← shell header
│   ├── m7-print.css                            ← regras @media print
│   ├── fonts/                                  ← TWK Everett + fallbacks
│   ├── m7-logo-dark.png                        ← logo para fundo claro
│   └── m7-logo-offwhite.png                    ← logo para fundo escuro
└── scripts/
    └── generate-html-yaml.py                   ← pipeline da Fase 3 (validação + render)
```

**REGRA CRÍTICA**: NUNCA recrie o template do zero. SEMPRE use `politica-m7-template.html`
como base. As 16 páginas A4 (Capa, Controle, 8 seções, controle de versões, aprovações),
classes CSS e tags semânticas são INVARIANTES.

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
| `governance` | owner, elaboradoPor, aprovadoPor, revisor, parent{code,title}, processos | aprovador_role=Diretoria (fixo) |
| `presentation` | title_short, title_full.parts (com `accent`), subtitle, lede, eyebrow_categoria, page_label_section | eyebrow_categoria="Documento de governança"; page_label_section ← area_label |
| `structure.toc` | lista inicial de páginas (mín 10: Capa, Controle, 8 seções) | — |
| `links.siblings` | irmãos do mesmo projeto/processo (tabs do shell) | opcional |

**Formato do BRIEFING.md**: bloco único de YAML em fence ```yaml ... ```
ou frontmatter `--- ... ---` no topo. Aceita-se também arquivo `.yaml` puro.

**Gate de saída (Fase 1 → Fase 2)**:
- Todos os campos `required` do schema preenchidos
- Resumo apresentado e **explicitamente confirmado** pelo usuário
- Sem confirmação, a skill NÃO avança

---

## Parte B · Produção

### Fase 2 — Redação MD (conteúdo das 8 seções)

**Objetivo**: produzir o conteúdo narrativo das 8 seções do documento.
**Input**: `BRIEFING-{CODE}.md`
**Output persistido**: `politica-{slug}.md` (editável, fonte de verdade do conteúdo).

O MD segue a estrutura semântica do template (ordem invariante):

1. **Objetivo** — máx 2 parágrafos. "Esta política estabelece..."
2. **Escopo** — "aplica-se a..." + "não se aplica a..."
3. **Definições** — tabela alfabética, mín 5 termos
4. **Princípios** — 3-8 itens; cada um com título h3 + parágrafo explicativo
5. **Diretrizes** — subseções 5.1, 5.2... ; cada subseção pode virar uma página do TOC
6. **Papéis & Responsabilidades** — tabela 3+ papéis cobrindo Estratégico/Tático/Operacional
7. **Governança** — 7.1 Revisão (frequência+gatilhos); 7.2 Indicadores (tabela Indicador/Fórmula/Frequência/Meta); 7.3 Escalonamento de exceções (Tipo/Aprovador)
8. **Disposições Finais** — 8.1 Vigência; 8.2 Documentos relacionados (tabela Código/Título/Relação)

**Retroalimentação do BRIEFING**: quando emergem subseções em Diretrizes,
atualize `structure.toc` no BRIEFING (`subsection: true`) e atualize
`identity.pages` para refletir o total final.

**Gate de saída (Fase 2 → Fase 3)**:
- MD revisado pelo usuário
- TOC final consolidado no BRIEFING
- `identity.pages` atualizado

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
4. Carrega `assets/politica-m7-template.html`
5. **Espelha** o YAML em todos os anchors (vide [normativo-schema.md](references/normativo-schema.md)):
   - identity → `<title>`, shell-meta, side-meta, cover-eyebrow, cover-foot, ph-meta (×N), kv-table
   - lifecycle → shell-meta date, .strip vigência/próx., cover-grid, kv-table
   - governance → side-meta owner, cover-grid responsável, kv-table elaboradoPor/aprovadoPor/parent
   - presentation → shell h1 (`<span class="accent">`), cover-title (`<em>` com auto-`<br>`), .lede, .cover-subtitle, cover-eyebrow
   - structure.toc → sumário lateral (×N páginas) + sumário formal da p.2
   - links.siblings → tabs do shell
   - identity.pages → .strip, .total-pg (×N), #total-pages
   - identity.classif_label → .cover-foot .conf, .pf-classif (×N)
6. Salva `{slug}.html`

**Limitação atual (importante)**: o script **não injeta conteúdo das 8 seções
narrativas**. As páginas 3-15 preservam o conteúdo do template (que vem do
exemplo POL-GOV-002). Edite manualmente o HTML após a geração, usando o MD
da Fase 2 como referência. Próxima iteração: injeção automática.

**Locais sugeridos para output**:
- `01-fundacao-2.1/artefatos/` (alinhado com cockpit — Bruno padrão)
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
