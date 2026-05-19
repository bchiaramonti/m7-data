---
name: mapeamento-n2
description: >-
  Pipeline iterativo de 3 fases (entrevista crítica → 4 MDs canônicos SSOT →
  build em camadas com gates) que decompõe UM processo primário de uma cadeia
  N1 em ~5 subprocessos e produz 4 artefatos HTML interligados M7-2026:
  Processo N2 (BPMN end-to-end), SIPOC/DEIP (sidebar + canvas), Jornada CX
  (touchpoint/action/MoT/pain) e Data Lake (systems/data/marts/consumers).
  Build em cascata: cada artefato é insumo do próximo, validado antes de
  avançar. SIPOC é iterado subprocesso-a-subprocesso. Use when the user asks
  for "mapeamento N2", "decomposição em subprocessos", "SIPOC DEIP",
  "jornada CX", "data lake do processo", ou tem um processo primário N1
  pronto (ex.: P5 Crédito) e quer destrinchar.

  <example>
  user: "Quero destrinchar o P5 Crédito em subprocessos N2"
  assistant: pede path do BRIEFING.md da N1, valida que P5 existe nos
  processos[], conduz Fase A em 5 blocos gerando entrevista.md, depois Fase B
  preenche 4 MDs canônicos em ssot/, e Fase C builda processo-n2 → 5 SIPOCs
  (iterativo, 1 por vez) → jornada-cx → data-lake com gates entre etapas.
  </example>

  <example>
  user: "Já tenho entrevista.md e ssot/ preenchidos, faz só o build"
  assistant: pula para Fase C; build_processo.py primeiro, confirma, depois
  build_sipoc.py --subproc para cada um, confirma cada, então build_jornada
  e build_datalake.
  </example>
user-invocable: true
---

# Mapeamento N2 · M7 Design System 2026

Pipeline **iterativo por design** que decompõe **um processo primário** vindo de uma cadeia N1 (ex.: P5 Crédito) em ~5 subprocessos e produz **4 artefatos HTML interligados** que respondem "O que fazer e o que esperar?" sob 4 lentes complementares:

| Camada | Artefato | Pergunta que responde |
|---|---|---|
| **Processo N2** | `processo-n2.html` (BPMN end-to-end Cliente↔M7) | *Quais os subprocessos e como se encadeiam?* |
| **SIPOC/DEIP** | `sipoc-deip.html` + `dados-{slug}.js` | *Para cada subprocesso: o que entra, o que sai, como executa?* |
| **Jornada CX** | `jornada-cx.html` + `journey-{slug}.js` (P5_JOURNEY) | *Como o cliente sente cada etapa?* |
| **Data Lake** | `data-lake.html` + `journey-{slug}.js` (P5_DATALAKE) | *Que dado nasce e onde persiste?* |

A skill é **iterativa em duas dimensões**: (1) entre camadas (cada artefato é gate para o próximo); (2) **dentro da camada SIPOC** (subprocesso-a-subprocesso, não single-shot).

## Arquitetura do pipeline

```
┌────────────────────────┐   ┌────────────────────────────┐   ┌──────────────────────────────────┐
│  FASE A · Entrevista   │   │  FASE B · 4 MDs SSOT       │   │  FASE C · Build em camadas       │
│  output: entrevista.md │──▶│  output: ssot/*.md         │──▶│  Processo → SIPOC* → Jornada →  │
│  (perguntas+respostas) │   │  validação por MD          │   │  Data Lake (gate entre etapas)   │
└────────────────────────┘   └────────────────────────────┘   └──────────────────────────────────┘
       │ loop max 3                    │                              │
       ▼                               ▼                              ▼
  n2-interview-critic            check_ssot.py                  n2-build-critic
  (subagent read-only)           (1 script, --target)           (subagent read-only)

                                                      *SIPOC: loop subprocesso-a-subprocesso
                                                       (Fase C.2 itera ~5 vezes, 1 por subproc.)
```

## Diferenças vs mapeamento-n1

| Aspecto | N1 | N2 (esta skill) |
|---|---|---|
| **Escopo** | Cadeia inteira (~18 processos macro) | 1 processo primário decomposto (~5 subprocessos) |
| **SSOT** | 1 BRIEFING.md monolítico | **4 MDs canônicos** em `ssot/` (um por artefato) |
| **Fase A output** | Já é o BRIEFING (SSOT) | `entrevista.md` (log perguntas+respostas) — SSOT vem na Fase B |
| **N2 produção** | Single-shot (todos SIPOCs juntos) | **Iterativa subprocesso-a-subprocesso** |
| **Validador** | `check_briefing.py` monolítico (763 linhas) | `check_ssot.py --target {processo-n2\|sipocs\|jornada-cx\|data-lake}` |
| **Build** | 1 build orchestrator | 4 scripts entrypoint + `_build_common.py` (gates explícitos) |
| **Handoff** | Standalone | **Exige BRIEFING.md da N1**; carrega artefatos N1 oportunisticamente (especialmente política) |

## Quando usar

- Já existe **cadeia de valor N1 mapeada** (BRIEFING.md + cadeia-de-valor-{slug}.html) e o usuário quer destrinchar **um** processo primário
- "mapeamento N2", "decomposição em subprocessos", "SIPOC DEIP do processo X", "jornada CX do produto Y", "data lake do processo Z"
- Empresa precisa **operacionalizar** um processo primário (passar de "o que faz" para "como faz") preservando rastreabilidade até a Política N4
- Documento vivo para Heads/Owners (não para diretoria — para diretoria, use N1+N4)

## Pré-requisitos

Antes de iniciar a Fase A:

1. **BRIEFING.md da N1** (obrigatório) — caminho relativo ao diretório de trabalho. Skill bloqueia se não encontrar ou se o `code` do processo (ex.: P5) não constar em `processos[]`
2. **Artefatos N1 do mesmo diretório** (opcional mas recomendado) — `cadeia-de-valor-{slug}.html`, `missao-do-processo-{slug}.html`, `mapa-de-interdependencia-{slug}.html`, **especialmente `politica-{slug}.html`** (ancoras governança)
3. **Diretório de trabalho** — onde `entrevista.md`, `ssot/`, e `build/` serão escritos. Recomendado `mapeamento-n2-{slug-processo}/` na mesma pasta da N1
4. **Código do processo a decompor** — ex.: `P5` (Crédito) ou `G2` (Performance)
5. **Documentos de apoio** (opcional) — PE, brandbook, manual operacional anterior. Citados como anexos na entrevista

## Arquivos da skill

```
skills/mapeamento-n2/
├── SKILL.md                                         ← este arquivo (entrypoint)
├── ENTREVISTA.tmpl.md                               ← template do log Fase A
├── references/
│   ├── phase-a-entrevista.md                        ← blocos da entrevista + interview-critic loop
│   ├── phase-b-ssot.md                              ← visão geral dos 4 MDs canônicos
│   ├── phase-c-build.md                             ← sequência, iteração SIPOC, gates
│   ├── ssot-processo-n2.md                          ← schema + regras processo-n2.md
│   ├── ssot-sipocs.md                               ← schema + regras sipocs.md
│   ├── ssot-jornada-cx.md                           ← schema + regras jornada-cx.md
│   ├── ssot-data-lake.md                            ← schema + regras data-lake.md
│   ├── design-system-m7.md                          ← tokens M7-2026 (idêntico ao N1)
│   └── critique-rules.md                            ← catálogo regras semânticas N2
├── agents/
│   ├── n2-interview-critic.md                       ← analisa entrevista.md (gaps semânticos)
│   └── n2-build-critic.md                           ← valida HTML+JS gerado por camada
├── templates/
│   ├── ssot/                                        ← 4 templates dos MDs canônicos
│   │   ├── processo-n2.tmpl.md
│   │   ├── sipocs.tmpl.md
│   │   ├── jornada-cx.tmpl.md
│   │   └── data-lake.tmpl.md
│   ├── html/
│   │   ├── processo-n2.tmpl.html                    ← tokenizado com {{placeholders}}
│   │   ├── sipoc-deip.html                          ← shell estático (do ZIP)
│   │   ├── sipoc-deip.js                            ← renderer (do ZIP)
│   │   ├── jornada-cx.html                          ← shell estático
│   │   └── data-lake.html                           ← shell estático
│   ├── js/
│   │   ├── dados.tmpl.js                            ← window.P5_DATA equivalente
│   │   └── journey.tmpl.js                          ← window.P5_JOURNEY + P5_DATALAKE
│   ├── m7-tokens.css · m7-header-dark.css
│   ├── mapeamento.css · mapeamento-views.css
│   ├── fonts/ (4× TWK Everett .otf)
│   └── assets/ (3× logos M7)
├── scripts/
│   ├── _build_common.py                             ← bootstrap, helpers compartilhados
│   ├── check_ssot.py                                ← validador, flag --target
│   ├── build_processo.py                            ← gate: BRIEFING N1
│   ├── build_sipoc.py                               ← gate: processo-n2.html; flag --subproc
│   ├── build_jornada.py                             ← gate: sipoc-deip.html + dados-{slug}.js
│   ├── build_datalake.py                            ← gate: journey-{slug}.js
│   └── requirements.txt
└── examples/
    ├── exemplo-entrevista-p5-credito.md             ← entrevista do P5 (referência)
    ├── exemplo-ssot-p5/                             ← 4 MDs canônicos preenchidos do P5
    └── exemplo-build-p5/                            ← HTML+JS prontos (mirror do ZIP)
```

## Fase A · Entrevista crítica

5 blocos com **checkpoints** ao final de cada bloco. **Output**: `entrevista.md` (log estruturado de perguntas feitas + respostas dadas), **não** o SSOT. Material exaustivo o suficiente para a Fase B preencher os 4 MDs canônicos sem precisar voltar.

Se o usuário anexa doc de referência (PE, manual, doc anterior), a entrevista marca **"respondida por anexo X"** em vez de transcrever literalmente — preserva rastreabilidade sem duplicar.

| Bloco | Foco | Saída em entrevista.md |
|---|---|---|
| 1 — Contexto N1 | Processo primário (code, name, owner, receita_meta, descrição) puxado do BRIEFING N1; lede do N2 | `## Contexto` |
| 2 — Decomposição | Quantos subprocessos, nomes, sequência, fronteira de cada | `## Subprocessos` (esqueleto) |
| 3 — SIPOC por subprocesso | Para cada: purpose, owner, cadência, sistemas, volume, inputs[], outputs[], etapas[], regulação[], suporte[] | `## SIPOC · {código}` (1 por subproc.) |
| 4 — Jornada CX | Para cada subproc.: touchpoint (canais), action (frontstage), MoT (intensity 1-3 + items), pain (tone +/-/~ + items) | `## Jornada CX` |
| 5 — Data Lake | Para cada subproc.: sistemas[], dados persistidos[], marts {dim[], fact[]}, consumers[] | `## Data Lake` |

Ao final do Bloco 5, invoca `n2-interview-critic` (subagent read-only) → relatório de **gaps** (campos vazios, fronteiras fuzzy, MoT sem inflexão, marts sem consumers correspondentes). **Loop max 3 ciclos**.

Detalhes em [`references/phase-a-entrevista.md`](references/phase-a-entrevista.md).

## Fase B · 4 MDs canônicos como SSOT

Cada MD é **auto-suficiente para regenerar seu artefato visual**. Estrutura: frontmatter YAML estruturado + seções markdown narrativas.

```
ssot/
├── processo-n2.md      ← meta processo + 5 subprocessos curtos + interfaces cliente↔M7
├── sipocs.md           ← SIPOC/DEIP completo por subprocesso (purpose, owner, I/O, etapas, reg/sup)
├── jornada-cx.md       ← 4 rows × N subprocessos (touchpoint, action, mot, pain)
└── data-lake.md        ← systems/data por subproc + marts/consumers globais
```

**Validação por MD** com `check_ssot.py --target {nome}` — exit code 1 se há bloqueadores.

Schemas completos:
- [`references/ssot-processo-n2.md`](references/ssot-processo-n2.md)
- [`references/ssot-sipocs.md`](references/ssot-sipocs.md)
- [`references/ssot-jornada-cx.md`](references/ssot-jornada-cx.md)
- [`references/ssot-data-lake.md`](references/ssot-data-lake.md)

Visão geral integrada em [`references/phase-b-ssot.md`](references/phase-b-ssot.md).

## Fase C · Build em camadas com gates

**Sequência rígida**, cada etapa só roda se a anterior passou (HTML renderiza sem `{{...}}` sobrando, JS data file presente):

1. **Processo N2** — `build_processo.py --ssot-dir ssot/ --out build/`
   - Gate: BRIEFING N1 existe e P{X} está em `processos[]`
   - Lê `ssot/processo-n2.md`, substitui ~30 placeholders no `processo-n2.tmpl.html`
   - Output: `build/processo-n2.html` + bootstrap CSS/fonts/assets
   - **Confirma com usuário antes de avançar**

2. **SIPOC/DEIP** — `build_sipoc.py --ssot-dir ssot/ --out build/ --subproc {ID}` (**iterativo**)
   - Gate: `build/processo-n2.html` existe
   - Para cada subprocesso (P5.1, P5.2, ...): atualiza o JS data file só com aquele subproc., copia `sipoc-deip.html` e `sipoc-deip.js` (estáticos), invoca `n2-build-critic` só naquele DEIP
   - **Confirma com usuário antes do próximo subprocesso**
   - Após o último, o `dados-{slug}-{cod}.js` está consolidado

3. **Jornada CX** — `build_jornada.py --ssot-dir ssot/ --out build/`
   - Gate: `build/sipoc-deip.html` + `build/dados-{slug}-{cod}.js` existem
   - Lê `ssot/jornada-cx.md`, gera parte `window.P5_JOURNEY` do `journey-{slug}-{cod}.js`, copia `jornada-cx.html`
   - **Confirma**

4. **Data Lake** — `build_datalake.py --ssot-dir ssot/ --out build/`
   - Gate: `build/journey-{slug}-{cod}.js` existe (parcial)
   - Lê `ssot/data-lake.md`, **completa** o `journey-{slug}-{cod}.js` adicionando `window.P5_DATALAKE`, copia `data-lake.html`

Detalhes em [`references/phase-c-build.md`](references/phase-c-build.md).

Após cada gate, opção de invocar [`m7-design-system:reviewing-html-design`](#) para QA visual (paleta, tipografia, espacamento).

## Validação obrigatória

### Pré-build (Fase B → C)
```bash
python3 scripts/check_ssot.py --all ssot/
```
Bloqueia se qualquer MD tem bloqueadores. Saída JSON ou legível.

### Por camada de build
- **Processo N2** → [`references/ssot-processo-n2.md §5`](references/ssot-processo-n2.md) + `n2-build-critic` opcional
- **SIPOC/DEIP** → [`references/ssot-sipocs.md §5`](references/ssot-sipocs.md) + `n2-build-critic` por subprocesso
- **Jornada CX** → [`references/ssot-jornada-cx.md §5`](references/ssot-jornada-cx.md)
- **Data Lake** → [`references/ssot-data-lake.md §5`](references/ssot-data-lake.md)

**Sempre verifique** ao final:
- [ ] Nenhum `{{placeholder}}` sobrou (busque `{{` em `build/*.html`)
- [ ] CSS, fonts, assets, e JS data files ao lado dos HTMLs
- [ ] Tabs do header navegam entre os 4 artefatos
- [ ] Sidebar SIPOC seleciona subprocesso, DEIP renderiza com fit-to-frame
- [ ] Jornada CX mostra N colunas × 4 rows; Data Lake mostra N colunas × 5 rows + inventário

## Estilo visual — invariantes

Não mexa em nada disto (idêntico aos invariantes da N1):
- **Fonte**: TWK Everett via `m7-tokens.css` (fallback Arial)
- **Background**: `var(--off-white)` `#fffdef`
- **Cor primária**: verde-caqui `#424135` (`var(--vc-500)`)
- **Cor de destaque**: lime `#eef77c` — só foco, accent, hover. Nunca texto corrido
- **Header escuro**: `m7-header-dark.css` full-bleed com logo offwhite + tabs N2

Não invente cores, gradientes, ícones decorativos ou emojis. Detalhes em [`references/design-system-m7.md`](references/design-system-m7.md).

## Anti-padrões transversais

- ❌ **Pular Fase A e ir direto pros templates** — sem entrevista exaustiva, os SSOT MDs ficam rasos e Fase C vira retrabalho
- ❌ **Tentar preencher os 4 SSOT MDs em paralelo na Fase B** — preencha sequencialmente: processo-n2 → sipocs → jornada-cx → data-lake (mantém coerência)
- ❌ **SIPOC single-shot (todos 5 subprocessos juntos)** — quebra o princípio iterativo da skill. Use `build_sipoc.py --subproc` por vez
- ❌ **Ignorar gates entre camadas** — não rode `build_jornada.py` se `dados-{slug}-{cod}.js` ainda não está pronto
- ❌ **Inventar SSOT MD novo (ex.: kpis.md, controles.md)** — escopo é fixo nos 4. Indicadores e controles ficam para skill N3 (futura)
- ❌ **Owner como nome próprio** (SIPOC) — sempre cargo/comitê (idêntico à N1)
- ❌ **Verbo genérico no `purpose`** (SIPOC) — sem "fazer", "realizar", "gerenciar"
- ❌ **MoT com `intensity` fora de {1,2,3}** ou **Pain com `tone` fora de {+, -, ~}**
- ❌ **Marts sem consumers** ou **consumers sem nenhum mart correspondente** (data-lake)
- ❌ **N2 sem N1** — skill bloqueia. Se realmente não há N1, rode `mapeamento-n1` primeiro

## Recursos adicionais

- **Caso de referência**: [`examples/exemplo-entrevista-p5-credito.md`](examples/exemplo-entrevista-p5-credito.md) — entrevista completa do P5 Crédito (5 blocos, 5 subprocessos)
- **SSOT preenchido**: [`examples/exemplo-ssot-p5/`](examples/exemplo-ssot-p5/) — 4 MDs canônicos do P5 validando limpo
- **Build de referência**: [`examples/exemplo-build-p5/`](examples/exemplo-build-p5/) — HTML+JS prontos (mirror visual do ZIP de gabarito)
- **Tokens M7-2026**: [`references/design-system-m7.md`](references/design-system-m7.md)
- **Catálogo de regras de crítica**: [`references/critique-rules.md`](references/critique-rules.md)
