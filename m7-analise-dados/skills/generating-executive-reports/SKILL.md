---
name: generating-executive-reports
description: >-
  Orquestra o pipeline completo Plan-Extract-Analyze-Interpret-Report usando os agentes
  data-scientist e executive-communicator. Coordena iterações entre agentes, adapta
  relatórios por audiência e gera outputs finais em Markdown.
  Use when executing an analysis plan (PLANO-ANALISE.md exists), generating executive reports,
  or when the user asks to run the analysis and produce the report.

  <example>
  Context: PLANO-ANALISE.md exists and user wants to execute
  user: "Execute o plano de análise e gere o relatório"
  assistant: Orquestra data-scientist para extrair e analisar, depois executive-communicator para interpretar e gerar relatório
  </example>

  <example>
  Context: User wants a report on existing data outputs
  user: "Gera o relatório executivo a partir desses dados"
  assistant: Invoca executive-communicator para interpretar outputs existentes e gerar relatório adaptado
  </example>
user-invocable: true
---

# Generating Executive Reports — Orquestração do Pipeline

> "O dado sem narrativa é ruído. A narrativa sem dado é achismo. Esta skill conecta ambos."

Esta skill orquestra o pipeline completo de análise, coordenando a interação entre os agentes `data-scientist` (extração e análise) e `executive-communicator` (interpretação e relatório).

## Dependências Internas

- [references/audience-adaptation-framework.md](references/audience-adaptation-framework.md) — 4 perfis × 6 dimensões
- [references/executive-writing-guide.md](references/executive-writing-guide.md) — Fórmulas de escrita
- [templates/relatorio-executivo.tmpl.md](templates/relatorio-executivo.tmpl.md) — Template do relatório
- `docs/INDICADORES.md` — Definições de métricas do projeto (queries, comparativos, contexto de negócio)
- Agent `data-scientist` — Extração e análise de dados
- Agent `executive-communicator` — Interpretação e geração do relatório

## Pré-requisitos

- `PLANO-ANALISE.md` existente no diretório de trabalho (gerado pela skill `planning-analysis`)
- MCPs configurados e acessíveis (conforme mapeado no plano)
- Estrutura de pastas criada (`docs/`, `data/extractions/`, `src/`, `output/`)

## Pipeline Completo

```
PLANO-ANALISE.md
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 1: EXTRACT + ANALYZE (data-scientist)                 │
│                                                             │
│  1. Ler PLANO-ANALISE.md — métricas, fontes, período        │
│  2. Explorar schemas MCP (se necessário)                    │
│  3. Extrair dados de cada fonte conforme mapeamento         │
│  4. Validar qualidade (checklist obrigatório)               │
│  5. Transformar e calcular métricas definidas               │
│  6. Executar cross-source join se planejado                 │
│  7. Salvar todos os outputs em output/data-scientist/       │
│                                                             │
│  Outputs: tabelas .md, CSVs, métricas rotuladas             │
└──────────────┬──────────────────────────────────────────────┘
               │ outputs brutos (dados, não interpretação)
               ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 2: INTERPRET + REPORT (executive-communicator)        │
│                                                             │
│  1. Ler PLANO-ANALISE.md — audiência, narrativa, blocos     │
│  2. Ler todos os outputs de output/data-scientist/          │
│  3. Aplicar framework de audiência (4 perfis × 6 dimensões) │
│  4. Consultar guia de escrita executiva                     │
│  5. Gerar relatório usando template                         │
│  6. Se dados insuficientes → gerar Solicitação Complementar │
│  7. Salvar relatório em output/relatorio-<nome>.md          │
│                                                             │
│  Output: relatório executivo adaptado à audiência           │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼ (se dados insuficientes)
┌─────────────────────────────────────────────────────────────┐
│  FASE 3: ITERATE (max 3 ciclos)                             │
│                                                             │
│  Ciclo:                                                     │
│  1. executive-communicator gera Solicitação Complementar    │
│  2. data-scientist executa queries adicionais               │
│  3. executive-communicator atualiza relatório               │
│  4. Repetir até dados suficientes ou max 3 ciclos           │
│                                                             │
│  Se após 3 ciclos: informar usuário + gerar com dados       │
│  disponíveis sinalizando lacunas                            │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────────────┐
│  FASE 4: VALIDATE + DELIVER                                 │
│                                                             │
│  1. Executar checklist de qualidade do relatório            │
│  2. Verificar rastreabilidade (todo dado → output source)   │
│  3. Confirmar adequação à audiência                         │
│  4. Salvar versão final em output/relatorio-<nome>.md       │
│  5. Apresentar resumo ao usuário                            │
└─────────────────────────────────────────────────────────────┘
```

## Execução Detalhada

### Fase 1: Invocar data-scientist

Prompt para o agente:

```
Leia o PLANO-ANALISE.md em [diretório].
Execute as análises listadas na seção "Instruções para data-scientist".

Se docs/INDICADORES.md existir no diretório de trabalho:
1. Leia a definição de cada métrica (fórmula, fonte, comparativos, contexto)
2. Use a fórmula definida para construir a query
3. Execute o checklist de validação de qualidade padrão
4. Se anomalia detectada, use o contexto de negócio do INDICADORES.md para cortes investigativos

Para todas as métricas:
1. Extraia os dados da fonte MCP indicada
2. Execute o checklist de validação de qualidade padrão
3. Calcule os comparativos definidos (YoY/MoM/vs meta)

Salve todos os outputs em output/data-scientist/ com nomes descritivos.
Se precisar de cross-source join, siga o Padrão #7 dos analysis-patterns.
```

**Critérios de saída da Fase 1:**
- [ ] Todas as métricas do plano foram extraídas
- [ ] Checklist de qualidade executado para cada extração
- [ ] Comparativos calculados
- [ ] Outputs salvos em `output/data-scientist/`

### Fase 2: Invocar executive-communicator

Prompt para o agente:

```
Leia o PLANO-ANALISE.md em [diretório] (audiência, narrativa, blocos).
Leia todos os outputs em output/data-scientist/.
Consulte references/audience-adaptation-framework.md para calibração.
Consulte references/executive-writing-guide.md para padrões de escrita.
Use templates/relatorio-executivo.tmpl.md como base.

Se docs/INDICADORES.md existir no diretório de trabalho:
1. Leia o contexto de cada métrica — use benchmarks e faixas para calibrar interpretação
2. Contextualize com fatores externos documentados quando aplicável

Gere o relatório executivo adaptado para a audiência [nome].
Salve em output/relatorio-[nome].md.

Se dados forem insuficientes, gere uma Solicitação de Dados Complementares.
```

**Critérios de saída da Fase 2:**
- [ ] Relatório gerado com todos os blocos do plano
- [ ] Linguagem adequada à audiência
- [ ] Todos os números rastreáveis aos outputs do data-scientist
- [ ] OU Solicitação Complementar gerada (→ Fase 3)

### Fase 3: Protocolo de Iteração

**Formato da Solicitação Complementar:**

```markdown
## Solicitação de Dados Complementares — Ciclo N/3

### Necessidade 1
- **Métrica**: [nome da métrica faltante]
- **Período**: [intervalo temporal necessário]
- **Granularidade**: [diário / semanal / mensal]
- **Fonte provável**: [Bitrix24: tool_name / ClickHouse: SQL hint]
- **Formato esperado**: [tabela / valor único / série temporal]
- **Justificativa**: [por que é necessário para completar o relatório]

### Necessidade 2
- ...
```

**Regras de iteração:**
1. Máximo **3 ciclos** de solicitação-resposta
2. Cada solicitação deve ser **específica e acionável** pelo data-scientist
3. Solicitação inclui **fonte provável** para acelerar a extração
4. Após 3 ciclos sem resolução: gerar relatório com dados disponíveis + seção "Limitações"
5. **Nunca** solicitar dados que já existem nos outputs

### Fase 4: Validação Final

**Checklist de qualidade do relatório:**

```
VALIDAÇÃO FINAL
────────────────
[ ] Todos os blocos temáticos do PLANO-ANALISE.md cobertos
[ ] Todos os números rastreáveis a outputs de output/data-scientist/
[ ] Linguagem adequada à audiência definida
[ ] Limite de páginas respeitado para a audiência
[ ] Comparativos incluídos em todos os números
[ ] Próximos passos com responsável e prazo
[ ] Nenhuma solicitação pendente do executive-communicator
[ ] Relatório salvo em output/relatorio-<nome>.md
```

**Se algum item falhar:** corrigir antes de entregar.

## Adaptação por Audiência (Quick Reference)

| Aspecto | Diretoria | Gerentes | Técnico | Comercial |
|---------|-----------|----------|---------|-----------|
| **Métricas** | 3-5 chave | 5-8 com contexto | Todas | Rankings + metas |
| **Blocos** | Max 3 | Max 4 | Sem limite | Max 3 |
| **Bullets/bloco** | 3-5 | 4-6 | Sem limite | 3-5 |
| **Páginas** | 1-2 | 2-3 | 3-5 | 2-3 |
| **Linguagem** | Zero jargão | Negócio + domínio | Técnica ok | Comercial |
| **Dados brutos** | Nunca | Resumo | Completo | Nunca |
| **CTA** | Decisão + deadline | Ação + owner + prazo | Tasks + timeline | Meta + oportunidade |

Para detalhes completos, ver [references/audience-adaptation-framework.md](references/audience-adaptation-framework.md).

## Fluxo Alternativo: Relatório sem PLANO-ANALISE.md

Se outputs do data-scientist já existem mas não há PLANO-ANALISE.md:

1. Perguntar ao usuário: **audiência** e **objetivo**
2. Ler outputs disponíveis em `output/data-scientist/`
3. Invocar executive-communicator diretamente com contexto mínimo
4. Recomendar ao usuário usar `planning-analysis` nas próximas vezes

## Anti-Patterns

- ❌ NUNCA pular a Fase 1 (extração) e ir direto para o relatório sem dados
- ❌ NUNCA permitir que o executive-communicator invente dados
- ❌ NUNCA exceder 3 ciclos de iteração sem escalar ao usuário
- ❌ NUNCA gerar relatório sem verificar a audiência definida no plano
- ❌ NUNCA misturar outputs dos agentes — data-scientist salva em `output/data-scientist/`, relatório final em `output/`
- ❌ NUNCA entregar relatório sem executar o checklist de validação final
