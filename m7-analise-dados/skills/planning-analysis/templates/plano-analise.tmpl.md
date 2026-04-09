# PLANO DE ANÁLISE: [Título]

> **Data**: YYYY-MM-DD
> **Solicitante**: [nome]
> **Audiência**: [Diretoria / Gerentes / Técnico / Comercial]
> **Contexto**: [Reunião mensal / Ad-hoc / Planejamento / Crise]
> **Diretório de trabalho**: [caminho absoluto ou relativo]

---

## Objetivo

[1-2 frases: O que queremos descobrir/responder com esta análise]

## Período de Análise

**De**: YYYY-MM-DD **Até**: YYYY-MM-DD
**Comparativos**: [YoY / MoM / vs Meta / vs Benchmark]

---

## Fontes de Dados

| # | Fonte | MCP | Ferramenta / Query | Dados Esperados |
|---|-------|-----|-------------------|-----------------|
| 1 | [fonte] | Bitrix24 / ClickHouse | [tool name ou SQL hint] | [descrição] |
| 2 | | | | |
| 3 | | | | |

**DATA-PROFILE.md referenciado**: [caminho se existir, ou "N/A — discovery será feito nesta fase"]

---

## Indicadores e Métricas

<!-- Definições completas em docs/INDICADORES.md — gerado na Fase de Planejamento -->

| # | Métrica | Definição | Fórmula | Fonte | Comparativo |
|---|---------|-----------|---------|-------|-------------|
| 1 | [nome] | [o que mede] | [cálculo] | [MCP + tool] | [YoY/MoM/etc] |
| 2 | | | | | |

---

## Estrutura do Relatório

### Narrativa Central
[Qual história os dados devem contar]

### Tom
[Otimista / Cauteloso / Neutro / Alarmante]

### Blocos Temáticos

| # | Bloco | Métricas | Mensagem-chave esperada |
|---|-------|----------|------------------------|
| 1 | [tema] | M1, M2, M3 | [hipótese] |
| 2 | [tema] | M4, M5 | [hipótese] |
| 3 | [tema] | M6, M7 | [hipótese] |

---

## Instruções para os Agentes

### Para data-scientist:
<!-- Análises específicas a executar — apenas dados -->
1. [Extração/query/cálculo específico]
2. [Extração/query/cálculo específico]
3. [Validação de qualidade obrigatória]

### Para executive-communicator:
<!-- Blocos a interpretar — apenas narrativa, calibrada para audiência -->
1. [Bloco + métricas a interpretar]
2. [Tom e profundidade para a audiência [nome]]
3. [Formato de output: Relatório Executivo / Status Update / Talking Points / Briefing]

---

## Critério de Conclusão

- [ ] Todas as métricas listadas foram extraídas
- [ ] Comparativos calculados (YoY/MoM/vs meta)
- [ ] Validação de qualidade executada sem alertas críticos
- [ ] Nenhuma solicitação pendente entre agentes
- [ ] Relatório adequado à audiência [nome]
- [ ] [Critério específico desta análise]
