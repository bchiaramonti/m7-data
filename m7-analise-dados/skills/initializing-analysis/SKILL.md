---
name: initializing-analysis
description: >-
  Inicializa um novo projeto de análise com diretório estruturado, CLAUDE.md orquestrador
  e templates de documentação. Cria o ponto de entrada do pipeline de análise com fases
  cadenciadas que guiam a execução passo a passo.
  Use when the user wants to start a new analysis, create an analysis project, or needs
  to structure a data analysis before executing it.

  <example>
  Context: User wants to start a new analysis
  user: "Quero criar uma análise de captação líquida do Q1"
  assistant: Coleta contexto (objetivo, audiência, período), cria diretório YYYY-MM-DD_captacao-liquida-q1/ com CLAUDE.md, BRIEFING.md e estrutura de pastas
  </example>

  <example>
  Context: User has a business question that needs structuring
  user: "Preciso entender a evolução de abertura de contas 300k"
  assistant: Coleta audiência e período, scaffolda projeto com BRIEFING.md pré-preenchido e CLAUDE.md com pipeline de fases
  </example>
user-invocable: true
---

# Initializing Analysis — Ponto de Entrada do Pipeline

> "Todo projeto de análise começa com estrutura. O CLAUDE.md é o orquestrador que garante execução passo a passo."

Esta skill cria um novo projeto de análise com diretório organizado e um CLAUDE.md que funciona como orquestrador de fases — referenciando as skills existentes do plugin como "comandos" a invocar em sequência.

## Pipeline Completo (Visão Geral)

```
Fase 0: initializing-analysis      → CLAUDE.md + BRIEFING.md + estrutura
Fase 1: exploring-data-sources     → DATA-PROFILE.md (opcional)
Fase 2: planning-analysis          → PLANO-ANALISE.md + docs/INDICADORES.md
Fase 3: generating-executive-reports → relatorio-*.md
```

Cada fase tem entry/exit criteria definidos no CLAUDE.md gerado. O usuário avança invocando a skill correspondente.

## Dependências Internas

- [templates/CLAUDE.tmpl.md](templates/CLAUDE.tmpl.md) — Template do orquestrador de fases
- [templates/README.tmpl.md](templates/README.tmpl.md) — Template do status do projeto
- [templates/BRIEFING.tmpl.md](templates/BRIEFING.tmpl.md) — Template do contexto de negócio
- Skills referenciadas no CLAUDE.md: `exploring-data-sources`, `planning-analysis`, `generating-executive-reports`

## Workflow

### Passo 1 — Coletar Contexto

Perguntar ao usuário via conversa:

| Dimensão | Pergunta | Obrigatório | Default |
|----------|----------|-------------|---------|
| **Tópico** | Qual o assunto da análise? (será o nome do diretório) | Sim | — |
| **Objetivo** | O que queremos descobrir/responder? (1-2 frases) | Sim | — |
| **Audiência** | Quem consumirá o resultado? | Sim | — |
| **Contexto** | Reunião mensal? Ad-hoc? Crise? Planejamento? | Sim | Ad-hoc |
| **Período** | Intervalo temporal dos dados | Sim | — |
| **Diretório base** | Onde criar o projeto? | Não | Diretório atual |

**Audiências válidas**: Diretoria, Gerentes, Técnico, Comercial (podem ser combinadas se necessário).

**Formato do tópico**: kebab-case, sem acentos (e.g., `captacao-liquida-q1`, `evolucao-contas-300k`).

### Passo 2 — Criar Diretório e Estrutura

Criar o diretório `YYYY-MM-DD_<topico>/` no diretório base com a seguinte estrutura:

```
YYYY-MM-DD_<topico>/
├── CLAUDE.md              # Orquestrador de fases (gerado do template)
├── README.md              # Status checklist (gerado do template)
├── docs/
│   ├── BRIEFING.md        # Contexto de negócio (pré-preenchido)
│   ├── SCHEMA.md          # Vazio — preenchido na Fase 1 (Discovery)
│   └── INDICADORES.md     # Vazio — preenchido na Fase 2 (Planejamento)
├── data/
│   └── extractions/       # Vazio — preenchido na Fase 3 (Execução)
├── src/                   # Vazio — scripts Python se necessário
└── output/
    └── data-scientist/    # Vazio — outputs do agente data-scientist
```

### Passo 3 — Gerar CLAUDE.md

Usar [templates/CLAUDE.tmpl.md](templates/CLAUDE.tmpl.md) substituindo as variáveis:

| Variável | Fonte |
|----------|-------|
| `{{titulo}}` | Tópico formatado como título (capitalizado, com espaços) |
| `{{objetivo}}` | Texto coletado no Passo 1 |
| `{{audiencia}}` | Audiência selecionada |
| `{{periodo}}` | Período informado |
| `{{contexto}}` | Contexto de negócio |
| `{{data_criacao}}` | Data atual (YYYY-MM-DD) |
| `{{diretorio}}` | Caminho completo do diretório criado |

O CLAUDE.md gerado é o **artefato principal** — ele guia toda a execução subsequente.

### Passo 4 — Gerar Documentação Inicial

1. **README.md** — Usar [templates/README.tmpl.md](templates/README.tmpl.md) com variáveis substituídas
2. **BRIEFING.md** — Usar [templates/BRIEFING.tmpl.md](templates/BRIEFING.tmpl.md) com variáveis substituídas
3. **SCHEMA.md** — Criar vazio com header: `# Schemas — [titulo]\n\n> Preenchido na Fase 1 (Discovery) ou Fase 2 (Planejamento).\n`
4. **INDICADORES.md** — Criar vazio com header: `# Indicadores — [titulo]\n\n> Definições de métricas da análise. Preenchido na Fase 2 (Planejamento) via input do usuário ou entrevista colaborativa.\n`

### Passo 5 — Apresentar Próximo Passo

Após criar a estrutura, informar ao usuário:

```
Projeto inicializado em: <caminho>

Próximo passo:
- Se precisa descobrir fontes de dados → /m7-analise-dados:exploring-data-sources
- Se já conhece as fontes → /m7-analise-dados:planning-analysis

Consulte o CLAUDE.md do projeto para o pipeline completo de fases.
```

## Validação Pós-Criação

Verificar que todos os arquivos foram criados:

- [ ] `CLAUDE.md` existe e tem variáveis substituídas (sem `{{...}}` residual)
- [ ] `README.md` existe com status checklist
- [ ] `docs/BRIEFING.md` existe com objetivo e audiência preenchidos
- [ ] `docs/SCHEMA.md` existe (pode estar vazio com header)
- [ ] `docs/INDICADORES.md` existe (pode estar vazio com header)
- [ ] Diretórios `data/extractions/`, `src/`, `output/data-scientist/` existem

## Convenção de Nomes

- **Diretório**: `YYYY-MM-DD_<topico>` (e.g., `2026-03-04_captacao-liquida-q1`)
- **Tópico**: kebab-case, sem acentos, descritivo (e.g., `evolucao-contas-300k`, `performance-comercial-fev`)
- **Data**: Sempre a data de criação, não a data do período de análise

## Anti-Patterns

- ❌ NUNCA criar o projeto sem coletar objetivo e audiência
- ❌ NUNCA deixar variáveis `{{...}}` sem substituir nos templates
- ❌ NUNCA pular a criação do CLAUDE.md — ele é o orquestrador
- ❌ NUNCA criar estrutura diferente da definida (as skills downstream dependem dela)
- ❌ NUNCA sobrescrever um projeto existente sem confirmar com o usuário
