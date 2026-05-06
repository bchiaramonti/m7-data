---
name: mapeamento-n1
description: >-
  Pipeline de 3 fases (entrevista crítica → BRIEFING.md → produção) que gera
  4 artefatos M7-2026: Cadeia de Valor N1, Missão SIPOC N2, Mapa de
  Interdependência N3 e Documento Oficial PDF N4. Analisa criticamente
  respostas (verbo genérico, IO-DUP, owner como nome próprio) com max 3
  ciclos. Use when the user asks for "cadeia de valor", "value chain",
  "SIPOC", "mapa de interdependência", "PDF oficial da cadeia", or anexa
  briefing estratégico e quer estruturar processos.

  <example>
  user: "Preciso montar a cadeia de valor da holding"
  assistant: conduz Fase A (5 blocos), gera BRIEFING.md, valida com
  check_briefing + process-critic, itera e produz N1.html
  </example>

  <example>
  user: "Quero o PDF oficial da cadeia para a diretoria"
  assistant: confirma N1+N2+N3 prontos (bloqueia se falta), gera N4.html
  com diagramas embedados, renderiza com render_pdf.py (Playwright) e
  valida com pdf-validator
  </example>
user-invocable: true
---

# Mapeamento N1 · M7 Design System 2026

Pipeline de 3 fases para mapeamento macro de processos (nível N1), produzindo **4 artefatos** que se complementam:

| Nível | Artefato | Pergunta que responde |
|---|---|---|
| **N1** | Cadeia de Valor (Porter, 3 camadas) | *O que a empresa faz?* |
| **N2** | Missão do Processo (SIPOC) | *O que cada processo entrega?* |
| **N3** | Mapa de Interdependência (grafo) | *Como os processos se conectam?* |
| **N4** | Documento Oficial (PDF paginado) | *Como apresentar tudo isso oficialmente?* |

A skill **não é apenas produtora** — é facilitadora: analisa criticamente respostas, detecta inconsistências e itera com o usuário antes de gerar artefatos.

## Arquitetura do pipeline

```
┌──────────────────┐   ┌─────────────────────┐   ┌──────────────────┐
│  FASE A          │   │  FASE B             │   │  FASE C          │
│  Entrevista &    │──▶│  BRIEFING.md        │──▶│  Produção        │
│  Crítica iter.   │   │  (SSOT canônico)    │   │  4 artefatos     │
└──────────────────┘   └─────────────────────┘   └──────────────────┘
        │  loop (max 3 ciclos)                           │
        ▼                                                ▼
   process-critic                                  pdf-validator
   (subagent read-only)                            (subagent read-only)
```

- **SSOT (BRIEFING.md)** separa entendimento do negócio (Fase A) da produção de pixels (Fase C).
- **Subagents read-only** (`process-critic`, `pdf-validator`) sinalizam problemas sem editar arquivos.
- **Geração sequencial 1→2→3→4**: erros localizáveis, possível invocar [`m7-design-system:reviewing-html-design`](#) entre etapas.

## Quando usar

- Briefing estratégico / Planejamento Estratégico mencionando processos
- "cadeia de valor", "value chain", "SIPOC", "missão dos processos", "mapa de interdependência", "blueprint da arquitetura de negócio", "N1 / N2 / N3 / N4", "documento oficial da cadeia"
- Empresa precisa documentar **o que faz** antes de detalhar **como faz** (subprocessos, atividades — fora do escopo desta skill)
- Documento PDF para apresentação executiva da cadeia

## Pré-requisitos

Antes de iniciar a Fase A:

1. **Diretório de trabalho** — onde o BRIEFING e os artefatos serão escritos (recomendo `mapeamento-{slug}/`)
2. **Escopo** — toda a holding? uma BU? um produto?
3. **Empresa-alvo** — nome, setor, data de referência (mês/ano)
4. **Logo** — usar M7 padrão (incluído nos assets) ou logo próprio?
5. **Quais artefatos gerar** — N1 sempre primeiro; N2/N3 sob demanda; N4 (PDF) exige N1+N2+N3 prontos
6. **Briefing existente?** — se houver PE, brandbook ou cadeia anterior, anexe antes da entrevista

## Arquivos da skill

```
skills/mapeamento-n1/
├── SKILL.md                                  ← este arquivo (entrypoint)
├── BRIEFING.tmpl.md                          ← template do SSOT (frontmatter YAML + seções MD)
├── references/
│   ├── n1-cadeia-de-valor.md                 ← regras N1
│   ├── n2-missao-do-processo.md              ← regras N2 (SIPOC)
│   ├── n3-mapa-interdependencia.md           ← regras N3 (grafo neural)
│   ├── n4-documento-oficial.md               ← regras N4 (PDF paginado)
│   ├── design-system-m7.md                   ← tokens M7-2026
│   ├── phase-a-entrevista-critica.md         ← Fase A: blocos + checkpoints
│   ├── phase-b-briefing.md                   ← Fase B: schema canônico do SSOT
│   ├── phase-c-producao.md                   ← Fase C: sequência de geração + render PDF
│   ├── critique-rules.md                     ← catálogo das regras de crítica
│   └── pdf-generation.md                     ← Playwright + WeasyPrint fallback
├── agents/
│   ├── process-critic.md                     ← read-only, analisa BRIEFING
│   └── pdf-validator.md                      ← read-only, valida PDF gerado
├── templates/
│   ├── template-cadeia-de-valor.html         ← N1 variante A (master)
│   ├── template-cadeia-de-valor--linear.html ← N1 variante B (linear)
│   ├── template-missao-do-processo.html      ← N2 (sidebar + SIPOC)
│   ├── template-mapa-de-interdependencia.html← N3 (neural graph)
│   ├── template-documento-oficial.html       ← N4 (A4 paginado)
│   ├── m7-tokens.css                         ← tokens
│   ├── m7-header-dark.css                    ← header escuro
│   ├── m7-print.css                          ← @page, page-break, landscape
│   ├── fonts/                                ← TWK Everett (6 .otf)
│   └── assets/                               ← logos M7
├── scripts/
│   ├── check_briefing.py                     ← validador determinístico
│   ├── render_pdf.py                         ← Playwright + WeasyPrint
│   └── requirements.txt
└── examples/
    ├── exemplo-m7-preenchido.html            ← N1 caso M7
    ├── exemplo-briefing-m7.md                ← BRIEFING M7 (gabarito mental)
    └── exemplo-documento-m7.pdf              ← PDF M7 gerado
```

## Fase A — Entrevista & Crítica iterativa

5 blocos curtos com **checkpoints** (heurísticas leves no prompt) ao final de cada bloco. Ao final do bloco 5, invoca `process-critic` para análise consolidada. Loop de **max 3 ciclos** de iteração antes de escalar.

Detalhes em [`references/phase-a-entrevista-critica.md`](references/phase-a-entrevista-critica.md).

| Bloco | Foco | Checkpoint |
|---|---|---|
| 1 — Identidade | Nome, slug, setor, escopo, data, logo | Slug é kebab-case? Data formatada? |
| 2 — Estrutura | Contagens por camada, variante A/B, nomes dos processos | Camadas válidas? Nomes ≤ 3 palavras? |
| 3 — Primários | Detalhamento dos primários (SIPOC se N2) | Verbo não genérico? Inputs ≠ Outputs? |
| 4 — Demais camadas | Gerenciais (com `Freq:`) e Apoio | Gerenciais têm frequência? |
| 5 — Confirmação | Revisão final + invocação do `process-critic` | Bloqueadores resolvidos ou aceitos? |

## Fase B — BRIEFING.md (SSOT)

Frontmatter YAML estruturado + seções markdown narrativas. Nome convencional: `mapeamento-{slug}.briefing.md` no diretório de trabalho do usuário.

```yaml
---
schema_version: 1
empresa: { nome, slug, setor, escopo }
data_referencia, versao, area_documento, logo
n1: { variante, rotulo_nucleo, total_processos, contagens }
processos:                          # lista canônica com sipoc + n3 por processo
  - codigo, camada, nome, tooltip, frequencia, highlight, blue_accent
    sipoc: { verbo, objeto, finalidade, inputs, outputs, owner }
    n3: { coluna, posicao, friction }
relacoes: [ { from, to, kind, label, forca } ]
artefatos_a_gerar: [n1, n2, n3, n4-pdf]
validacao: { bloqueadores, avisos, todos, bloqueadores_aceitos }
---
# Briefing — Cadeia de Valor {empresa}
## Objetivo do diagrama
## Lede do documento
## Contexto da empresa
## Notas de iteração
## Anexos / referências
```

Schema completo em [`references/phase-b-briefing.md`](references/phase-b-briefing.md). Validação via `python3 scripts/check_briefing.py {arquivo}` — saída JSON com `bloqueadores` e `avisos`. Roda **antes** de cada round do critic e **antes** de Fase C iniciar.

## Fase C — Produção dos 4 artefatos

Sequência **rígida** (cada artefato lê o BRIEFING):

1. **N1** → `cadeia-de-valor-{slug}.html` (variante A ou B segundo `n1.variante`)
2. **N2** → `missao-do-processo-{slug}.html` (sidebar + painel SIPOC por processo)
3. **N3** → `mapa-de-interdependencia-{slug}.html` (posições % + RELATIONS)
4. **N4 PDF** → `documento-oficial-{slug}.html` → `documento-oficial-{slug}.pdf`
   - **Bloqueia** se N1, N2 ou N3 não estão prontos no diretório
   - Embute os 3 anteriores via Jinja `{% include %}` (vetorial, texto selecionável)
   - Render: `python3 scripts/render_pdf.py input.html output.pdf` (Playwright; WeasyPrint fallback)
   - Mapa N3 fica em **landscape** no meio do PDF; capa e SIPOC em retrato

Detalhes em [`references/phase-c-producao.md`](references/phase-c-producao.md).

Após gerar tudo, invoca `pdf-validator` (subagent) que abre o PDF e roda checklist de validação.

## Estilo visual — invariantes

Não mexa em nada disto:
- **Fonte**: TWK Everett via `m7-tokens.css` (fallback Arial)
- **Background**: `var(--off-white)` `#fffdef`
- **Cor primária**: verde-caqui `#424135` (`var(--vc-500)`)
- **Cor de destaque**: lime `#eef77c` — só foco estratégico, accent ou hover. Nunca texto corrido.
- **Header escuro**: `m7-header-dark.css` full-bleed com logo offwhite, metadata, título com `.accent` lime, strip de stats, tabs (Visão geral N1 · Missão do processo · Mapa de interdependência)

Não invente cores, gradientes (exceto os já no template do mapa), ícones decorativos ou emojis. Detalhes em [`references/design-system-m7.md`](references/design-system-m7.md).

## Validação obrigatória

### Pré-geração (Fase B → C)
Use [`scripts/check_briefing.py`](scripts/check_briefing.py) — bloqueia se há bloqueadores não aceitos.

### Por artefato
- N1 → [`references/n1-cadeia-de-valor.md §8`](references/n1-cadeia-de-valor.md)
- N2 → [`references/n2-missao-do-processo.md §5`](references/n2-missao-do-processo.md)
- N3 → [`references/n3-mapa-interdependencia.md §5`](references/n3-mapa-interdependencia.md)
- N4 → [`references/n4-documento-oficial.md`](references/n4-documento-oficial.md) + `pdf-validator` subagent

**Sempre verifique**:
- [ ] Nenhum `{{placeholder}}` sobrou (busque `{{` no arquivo final)
- [ ] CSS, fonts e logos estão ao lado dos HTMLs gerados
- [ ] Tabs do header navegam para os outros artefatos do mesmo set
- [ ] Hover funciona (tooltip, halo, painel)
- [ ] Para N4: capa renderiza, mapa em landscape, footer numerado

## Anti-padrões transversais

- ❌ **Pular Fase A e ir direto para templates** — sem BRIEFING não há SSOT, e correções viram retrabalho.
- ❌ **Ignorar bloqueadores do critic sem registrar** — sempre documentar exceções em `validacao.bloqueadores_aceitos` com rationale.
- ❌ **Iterar mais de 3 rounds** — sintoma de mapeamento estrutural raso. Pause e reagende com mais informação prévia.
- ❌ **Inventar 4ª camada Porter** — sempre 3: Gerenciais · Primários · Apoio.
- ❌ **Trocar a fonte ou o palette** — TWK Everett + verde-caqui + lime + off-white.
- ❌ **Adicionar gráficos, KPIs grandes ou dashboards** — N1/N2/N3/N4 é mapa de processo, não BI.
- ❌ **Owner como nome próprio** (N2) — sempre cargo/comitê.
- ❌ **Atividades/passos no lugar da missão** (N2) — SIPOC é "o quê", não "como".
- ❌ **Múltiplos kinds entre os mesmos dois nós** (N3) — escolha o tipo dominante.
- ❌ **Gerar N4 com N1/N2/N3 incompletos** — bloqueia em Fase C.

## Recursos adicionais

- **Caso de referência completo**: [`examples/exemplo-briefing-m7.md`](examples/exemplo-briefing-m7.md) — BRIEFING M7 com 18 processos, valida limpo (0 bloqueadores).
- **Visualização HTML do N1 M7**: [`examples/exemplo-m7-preenchido.html`](examples/exemplo-m7-preenchido.html).
- **PDF M7 gerado**: [`examples/exemplo-documento-m7.pdf`](examples/exemplo-documento-m7.pdf) — gabarito do output final.
- **Tokens M7-2026**: [`references/design-system-m7.md`](references/design-system-m7.md).
- **Catálogo de regras de crítica**: [`references/critique-rules.md`](references/critique-rules.md).
