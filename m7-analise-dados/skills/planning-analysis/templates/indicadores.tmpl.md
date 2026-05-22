# Indicadores — {{titulo_analise}}

> **Fonte da verdade** das métricas usadas nesta análise. Os agentes
> `data-scientist` (queries) e `executive-communicator` (interpretação)
> consultam este arquivo. **Obrigatório** desde v4.0.0 — não opcional.
>
> Uma entrada por métrica. Mantenha o formato exato — agentes parseiam
> por seção, então o `## [Nome]` e os campos rotulados são contrato.

---

## Captação Líquida

- **Definição**: Soma de entradas menos soma de saídas no período, considerando todas as movimentações financeiras dos clientes ativos
- **Papel no briefing**: `destaque-tldr` *(aparece como KPI principal na §3 do Analytics Report)*
- **Unidade**: R$ mi (milhões de reais)
- **Granularidade**: Mensal
- **Fonte**: `<MCP-de-dados-historicos>` · tabela/view `fact_movimentacao` *(substituir pelo seu MCP real)*
- **Fórmula**: `SUM(entradas) - SUM(saidas)` agregado por `toStartOfMonth(data)`
- **Comparativos**: MoM (mês anterior), YoY (mesmo mês ano anterior), vs Meta trimestral
- **Benchmark**: R$ 100 mi/mês (meta institucional 2026)
- **Faixas de leitura**:
  - `verde` (≥ meta · `ok`): ≥ R$ 100 mi
  - `amarelo` (atenção · `warn`): R$ 80–100 mi
  - `vermelho` (crítico · `bad`): < R$ 80 mi
- **Contexto de negócio**: Captação tem sazonalidade alta — Janeiro e Julho costumam ser fracos (férias), Março e Setembro fortes (rebalanceamento). YoY é sempre mais informativo que MoM
- **Fatores externos relevantes**: Selic em ciclo de queda favorece migração de RF para multimercado; eventos como reforma tributária ou crise bancária causam pico de movimentação atípica
- **Limitações conhecidas**: Não captura migração interna entre produtos (só fluxo entrada/saída líquido)

---

## [Nome do próximo indicador]

- **Definição**: [o que mede em uma frase clara]
- **Papel no briefing**: `destaque-tldr` ou `detalhe-scorecard` *(define se vai na §3 TL;DR — máx 4 — ou na §4 Scorecard — 8 a 10)*
- **Unidade**: [R$ mi / % / pontos / count / ...]
- **Granularidade**: [Diária / Semanal / Mensal / Trimestral]
- **Fonte**: [`<MCP>` · tabela/entidade ou script/arquivo de origem]
- **Fórmula**: [expressão calculável — SQL, Python ou regra de negócio]
- **Comparativos**: [escolha entre: MoM, YoY, vs Meta, vs Benchmark de mercado, vs Baseline pré-evento]
- **Benchmark**: [valor ou faixa de referência — meta interna, média histórica, player de mercado]
- **Faixas de leitura**:
  - `verde` (`ok`): [condição]
  - `amarelo` (`warn`): [condição]
  - `vermelho` (`bad`): [condição]
- **Contexto de negócio**: [sazonalidade, dependências, padrão histórico]
- **Fatores externos relevantes**: [variáveis macro, regulatórias ou competitivas que afetam]
- **Limitações conhecidas**: [o que esta métrica NÃO mede / cuidados de interpretação]

---

## Regras de preenchimento

1. **Papel no briefing é obrigatório**. Cada métrica é `destaque-tldr` (vai pros 4 KPIs principais do TL;DR) OU `detalhe-scorecard` (vai pros 8-10 do scorecard). Não pode ser ambos — overlap polui o briefing
2. **Fórmula precisa ser calculável**. Texto narrativo ("medir a captação") não é fórmula. Use SQL, expressão Python ou regra agregada (`SUM`, `COUNT`, `AVG / total`)
3. **Pelo menos 1 comparativo**. Número solto não comunica. Sem referência, a métrica não merece estar aqui
4. **Faixas só se houver meta/benchmark**. Se a métrica é descritiva (não tem norte), pule faixas — não invente
5. **Contexto antes de fatores externos**. Sazonalidade é interna ao indicador; fatores externos são causas-raiz fora dele
6. **Limitações são honestidade, não fraqueza**. Documentar o que a métrica não cobre é o que diferencia análise séria de dashboard ingênuo

## Anti-padrões

- ❌ Indicador sem `Papel no briefing` definido — vai gerar overlap entre TL;DR e scorecard
- ❌ Mais de 4 métricas marcadas como `destaque-tldr` — briefing só aceita 4
- ❌ Mais de 12 métricas no total — scorecard cabe 8-10 no máximo
- ❌ Fórmula em prosa ("calcular a média histórica considerando os meses ativos") — agente data-scientist não consegue executar
- ❌ Benchmark inventado sem fonte ("meta R$ 100mi" sem dizer de onde veio)
- ❌ Misturar duas métricas em uma entrada ("Captação + Resgates" — separe em duas)
