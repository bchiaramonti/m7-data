# CLAUDE.md — Análise: {{titulo}}

Este arquivo orquestra o pipeline de análise de dados. Leia-o ao iniciar qualquer sessão neste diretório.

## Metadata

| Campo | Valor |
|-------|-------|
| **Objetivo** | {{objetivo}} |
| **Audiência** | {{audiencia}} |
| **Período** | {{periodo}} |
| **Contexto** | {{contexto}} |
| **Criado em** | {{data_criacao}} |
| **Diretório** | {{diretorio}} |

---

## Pipeline de Fases

> **Fase atual**: 0 — Setup ✅

| Fase | Nome | Skill | Status | Artefato |
|------|------|-------|--------|----------|
| 0 | Setup | `initializing-analysis` | ✅ Completa | CLAUDE.md, BRIEFING.md |
| 1 | Discovery | `exploring-data-sources` | ⬜ Pendente | DATA-PROFILE.md |
| 2 | Planejamento | `planning-analysis` | ⬜ Pendente | PLANO-ANALISE.md, docs/INDICADORES.md |
| 3 | Execução | `generating-executive-reports` | ⬜ Pendente | output/relatorio-*.md |

**Regra**: Avançar uma fase de cada vez. Cada fase tem entry/exit criteria. Ao concluir, atualizar a tabela acima.

### Comandos de Orquestração

Use estes comandos para navegar o pipeline:

| Comando | Função |
|---------|--------|
| `/m7-analise-dados:status` | Ver progresso, fase atual e próximo passo recomendado |
| `/m7-analise-dados:next` | Avançar para a próxima fase (verifica entry criteria, invoca skill) |
| `/m7-analise-dados:review` | Validar consistência dos dados da fase atual (rastreabilidade, aritmética, cross-checks) |

**Fluxo recomendado por fase**: `next` (executar) → `review` (validar) → `next` (avançar)

---

## Fase 1 — Discovery (Opcional)

**Invocar**: `/m7-analise-dados:exploring-data-sources`

**Quando pular**: Se já conhece as fontes de dados e schemas relevantes para esta análise.

**Entry criteria**:
- [ ] BRIEFING.md preenchido com objetivo e perguntas a responder

**O que faz**:
1. Lista databases e tabelas disponíveis (ClickHouse/Bitrix24)
2. Profila schemas relevantes ao objetivo
3. Executa EDA com estatísticas descritivas, distribuições, outliers
4. Documenta hipóteses iniciais

**Exit criteria**:
- [ ] DATA-PROFILE.md gerado neste diretório
- [ ] Schemas das fontes relevantes documentados em `docs/SCHEMA.md`
- [ ] Hipóteses iniciais alinhadas ao objetivo

**Ao concluir**: Atualizar tabela de status → ✅ e avançar para Fase 2.

---

## Fase 2 — Planejamento

**Invocar**: `/m7-analise-dados:planning-analysis`

**Entry criteria**:
- [ ] Objetivo e audiência definidos (docs/BRIEFING.md)
- [ ] DATA-PROFILE.md disponível (se Fase 1 foi executada)

**O que faz**:
1. Mapeia fontes de dados ao objetivo da análise
2. Define métricas via input do usuário ou entrevista colaborativa → salva em `docs/INDICADORES.md`
3. Estrutura o relatório (blocos temáticos, narrativa, tom)
4. Gera PLANO-ANALISE.md com instruções específicas para cada agente

**Exit criteria**:
- [ ] PLANO-ANALISE.md gerado neste diretório
- [ ] `docs/INDICADORES.md` preenchido com definição de cada métrica
- [ ] Todas as métricas mapeadas a pelo menos uma fonte MCP
- [ ] Estrutura do relatório definida com blocos temáticos
- [ ] Critérios de conclusão definidos

**Ao concluir**: Atualizar tabela de status → ✅ e avançar para Fase 3.

**Nota**: A skill `planning-analysis` pode criar subpastas adicionais. Não é necessário recriar o que já existe.

---

## Fase 3 — Execução

**Invocar**: `/m7-analise-dados:generating-executive-reports`

**Entry criteria**:
- [ ] PLANO-ANALISE.md existe e foi revisado/aprovado
- [ ] MCPs configurados e acessíveis

**O que faz**:
1. **data-scientist** extrai dados conforme PLANO-ANALISE.md → salva em `output/data-scientist/`
2. **executive-communicator** interpreta dados → gera relatório em `output/relatorio-*.md`
3. Itera até 3 ciclos se dados insuficientes
4. Valida qualidade final do relatório

**Exit criteria**:
- [ ] Todas as métricas do plano foram extraídas
- [ ] Relatório executivo gerado em `output/`
- [ ] Todos os números rastreáveis aos outputs do data-scientist
- [ ] Linguagem adequada à audiência: {{audiencia}}

**Ao concluir**: Atualizar tabela de status → ✅.

---

## Regras dos Agentes

### data-scientist
- **Faz**: Extrai dados, calcula métricas, executa quality checks, identifica anomalias numericamente
- **NÃO faz**: Interpreta, conclui, recomenda, gera bullet points narrativos
- **Salva em**: `output/data-scientist/`
- **Ferramentas**: Read, Write, Edit, Bash, Grep, Glob + MCPs (ClickHouse, Bitrix24)

### executive-communicator
- **Faz**: Interpreta dados, gera relatórios adaptados à audiência, escreve insights acionáveis
- **NÃO faz**: Acessa MCPs, extrai dados, escreve código, inventa números
- **Salva em**: `output/relatorio-*.md`
- **Ferramentas**: Read, Write, Grep, Glob (sem MCPs)

**Separação é inegociável** — misturar responsabilidades degrada a qualidade dos outputs.

---

## Estrutura do Projeto

```
{{diretorio}}/
├── CLAUDE.md                    # Este arquivo (orquestrador)
├── README.md                    # Status geral do projeto
├── docs/
│   ├── BRIEFING.md              # Contexto de negócio e perguntas
│   ├── SCHEMA.md                # Schemas das fontes de dados
│   └── INDICADORES.md           # Definições de métricas
├── DATA-PROFILE.md              # Gerado na Fase 1 (opcional)
├── PLANO-ANALISE.md             # Gerado na Fase 2
├── data/
│   └── extractions/             # Dados brutos extraídos
├── src/                         # Scripts Python auxiliares
└── output/
    ├── data-scientist/          # Outputs do agente (tabelas, métricas)
    └── relatorio-*.md           # Relatório executivo final
```

## Checklist Final de Qualidade

Antes de considerar a análise completa:

- [ ] Objetivo do BRIEFING.md foi respondido
- [ ] Todas as perguntas do BRIEFING.md foram endereçadas
- [ ] Relatório adequado à audiência ({{audiencia}})
- [ ] Todos os números do relatório são rastreáveis a `output/data-scientist/`
- [ ] Comparativos incluídos (YoY/MoM/vs meta) em todas as métricas
- [ ] Próximos passos no relatório incluem responsável e prazo
- [ ] Nenhuma solicitação pendente entre agentes
