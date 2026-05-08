# m7-processos

Plugin M7 para mapeamento e gestão de processos no nível macro (N1) com pipeline de 3 fases (entrevista crítica → BRIEFING.md SSOT → produção) e 4 artefatos visuais seguindo o design system M7-2026.

> **Status**: estável (`v1.1.0`).

## Marketplace

Este plugin pertence ao marketplace [`m7-data`](../).

## Instalação

```bash
/plugin marketplace add bchiaramonti/claude-plugins/m7-data
/plugin install m7-processos@m7-data
```

## Skills

### `drawing-bpmn-flowcharts`

Constrói diagramas BPMN 2.0 a partir de JSON estruturado, descrição conversacional ou markdown narrativo. Gera `.bpmn` portátil (abre em Camunda Modeler / bpmn.io / Bizagi) com auto-layout determinístico, validação iterativa de legibilidade e cores M7-2026 via extensões `bioc:`.

| Input | Output |
|---|---|
| JSON estruturado / descrição conversacional / markdown narrativo | `.bpmn` (XML BPMN 2.0 portátil) + `-descritivo.md` (narrativa + checklist + relatório de legibilidade) |

**Diferenciais**:
- Auto-layout determinístico (topological sort + ranks + waypoints) — script Python stdlib
- Validação iterativa de legibilidade (max 3 ciclos): sem sobreposição, sem cruzar nós, sem texto trincado
- Validação de notação BPMN 2.0 embutida (7 categorias, 23+ regras)
- Cores M7-2026 via `bioc:fill` / `bioc:stroke` (Camunda Modeler / bpmn-js compatible)
- **Suporte nativo a AI agents** (Camunda 8.8+): ad-hoc sub-process com tools, AI Agent Task single-call, 4 padrões canônicos
- Sem dependências externas (Python stdlib only)

**Quando usar**: usuário pede para gerar/construir/desenhar/modelar um fluxograma BPMN, ou fornece atividades/lanes/gateways e quer um arquivo `.bpmn`.

**A skill gera apenas `.bpmn`**: a renderização downstream (HTML embed via bpmn-js, PDF, etc.) é responsabilidade do consumidor.

### `mapeamento-n1`

Pipeline completo para mapear a cadeia de valor de uma empresa nível N1 (macroprocessos), com análise crítica iterativa (até 3 ciclos) e geração de 4 artefatos:

| Nível | Artefato | Pergunta que responde |
|---|---|---|
| **N1** | Cadeia de Valor (Porter, 3 camadas) | *O que a empresa faz?* |
| **N2** | Missão do Processo (SIPOC) | *O que cada processo entrega?* |
| **N3** | Mapa de Interdependência (grafo neural) | *Como os processos se conectam?* |
| **N4** | Documento Oficial (PDF paginado A4) | *Como apresentar tudo isso oficialmente?* |

**Arquitetura do pipeline**:
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

**Quando usar**: o usuário pede "cadeia de valor", "value chain", "SIPOC", "mapa de interdependência", "PDF oficial da cadeia", ou anexa briefing estratégico e quer estruturar processos.

## Quick start

```bash
# 1. Setup (uma vez)
cd skills/mapeamento-n1
pip install -r scripts/requirements.txt
playwright install chromium

# 2. Pipeline end-to-end com BRIEFING M7 de exemplo
mkdir /tmp/teste-m7
python3 scripts/build_artifacts.py examples/exemplo-briefing-m7.md /tmp/teste-m7/

# Resultado:
#   /tmp/teste-m7/cadeia-de-valor-m7-investimentos.html         (N1)
#   /tmp/teste-m7/missao-do-processo-m7-investimentos.html      (N2)
#   /tmp/teste-m7/mapa-de-interdependencia-m7-investimentos.html (N3)
#   /tmp/teste-m7/documento-oficial-m7-investimentos.html        (N4 fonte)
#   /tmp/teste-m7/documento-oficial-m7-investimentos.pdf         (N4 final)
```

## Estrutura

```
m7-processos/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── drawing-bpmn-flowcharts/
│   │   ├── SKILL.md                      # entrypoint da skill BPMN
│   │   ├── references/                   # 5 refs (notation, layout, readability, m7-styling, ai-agents)
│   │   ├── templates/                    # bpmn-skeleton.tmpl.xml + input-schema + descritivo
│   │   ├── scripts/                      # compute_auto_layout.py + validate_bpmn_readability.py
│   │   └── examples/                     # exemplo-onboarding (input + .bpmn + descritivo)
│   └── mapeamento-n1/
│       ├── SKILL.md                      # entrypoint do pipeline N1
│       ├── BRIEFING.tmpl.md              # template do SSOT
│       ├── references/                   # 9 references (N1-N4, fases A-C, regras)
│       ├── agents/                       # process-critic + pdf-validator (read-only)
│       ├── templates/                    # 5 HTML + 3 CSS + fonts + assets
│       ├── scripts/                      # check_briefing, build_artifacts, render_pdf
│       └── examples/                     # M7 BRIEFING + N1 HTML + PDF gerado
├── README.md
└── CHANGELOG.md
```

## Design System M7-2026

Todos os artefatos seguem rigorosamente:

| Token | Valor |
|---|---|
| Fonte | TWK Everett (200/300/400/500/700) — fallback Arial |
| Primária | `#424135` Verde Caqui |
| Accent | `#EEF77C` Lime (apenas foco / hover / accent — nunca texto corrido) |
| BG | `#fffdef` Off-White (warm, não branco frio) |
| Header escuro | `#28271f` (vc-700) com lime accent |

Detalhes em `skills/mapeamento-n1/references/design-system-m7.md`.

## Dependências

| Pacote | Função |
|---|---|
| `pyyaml >= 6.0` | Parse do BRIEFING.md (frontmatter) |
| `beautifulsoup4 >= 4.12` | Extração de fragmentos HTML |
| `jinja2 >= 3.1` | (opcional, futuro) |
| `playwright >= 1.40` + Chromium | Render HTML → PDF (driver primário) |
| `weasyprint >= 60.0` | Fallback HTML → PDF se Chromium não disponível |

## Autor

Bruno Chiaramonti — Head of Performance, M7 Investimentos.
