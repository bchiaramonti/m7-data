---
description: Valida consistência dos dados e artefatos da fase atual com verificações cruzadas, rastreabilidade numérica e coerência entre fases
---

# Analysis Review

## Objetivo

Verificar a qualidade e consistência dos artefatos da fase atual antes de avançar. Diferente de um review de código — este é um **review de dados** que verifica rastreabilidade numérica, coerência aritmética, e consistência entre fases e indicadores.

## Processo

### 1. Localizar CLAUDE.md

Procurar `CLAUDE.md` no diretório atual. Se não encontrar:
"Nenhum projeto de análise encontrado. Execute `/m7-analise-dados:initializing-analysis` para criar um."

### 2. Identificar fase a revisar

Ler tabela de status. Identificar a **última fase com status ✅** (a mais recente concluída). Se nenhuma fase além de Setup foi concluída:
"Nenhuma fase para revisar. Execute `/m7-analise-dados:next` para avançar."

### 3. Ler TODOS os artefatos

Ler todos os artefatos produzidos até a fase sendo revisada:
- `docs/BRIEFING.md` — contexto e objetivo (sempre)
- `DATA-PROFILE.md` — se Fase 1 concluída
- `docs/SCHEMA.md` — schemas documentados
- `PLANO-ANALISE.md` — se Fase 2 concluída
- `docs/INDICADORES.md` — métricas definidas
- `output/data-scientist/*.md` — se Fase 3 em andamento/concluída
- `output/relatorio-*.md` — relatório final

### 4. Executar verificações por fase

---

#### Fase 1 — Discovery Review

**Completude**:
- [ ] DATA-PROFILE.md existe e não está vazio
- [ ] Pelo menos uma fonte de dados explorada com estatísticas descritivas
- [ ] docs/SCHEMA.md atualizado com schemas das fontes relevantes

**Consistência com Briefing**:
- [ ] Fontes exploradas são relevantes ao objetivo do BRIEFING.md
- [ ] Cobertura temporal dos dados inclui o período definido no BRIEFING.md
- [ ] Se BRIEFING.md menciona métricas específicas, fontes para elas foram identificadas

**Qualidade dos dados**:
- [ ] Tipos de dados estão corretos (datas como Date, valores como Float/Int)
- [ ] Taxa de nulls documentada para campos críticos
- [ ] Outliers identificados e documentados (não necessariamente resolvidos)
- [ ] Volume de dados é suficiente para análise estatisticamente significativa

---

#### Fase 2 — Planning Review

**Completude**:
- [ ] PLANO-ANALISE.md existe com todas as seções preenchidas
- [ ] Nenhum placeholder `[...]` ou `<...>` remanescente
- [ ] Critérios de conclusão definidos e mensuráveis

**Coerência com Discovery (cascata Fase 1 → 2)**:
- [ ] Fontes mapeadas no plano existem no DATA-PROFILE.md (se Fase 1 executada)
- [ ] Período do plano está dentro da cobertura temporal identificada
- [ ] Métricas ad-hoc têm fórmula calculável com os campos documentados nos schemas

**Coerência com Briefing (cascata Fase 0 → 2)**:
- [ ] Audiência no plano = audiência no BRIEFING.md
- [ ] Objetivo do plano endereça as perguntas do BRIEFING.md
- [ ] Blocos temáticos do relatório são adequados à audiência definida

**Indicadores e métricas definidos**:
- [ ] `docs/INDICADORES.md` existe e tem definição completa para cada métrica do plano (nome, fórmula, fonte, comparativos)
- [ ] Nenhuma métrica no PLANO-ANALISE.md sem correspondência em INDICADORES.md

**Métricas**:
- [ ] Cada métrica tem pelo menos um comparativo definido (YoY/MoM/vs meta)
- [ ] Fórmulas são matematicamente válidas (não divide por zero, unidades compatíveis)
- [ ] Granularidade da métrica é compatível com a fonte (ex: não pedir diário se fonte é mensal)

---

#### Fase 3 — Execution Review (O MAIS CRÍTICO)

Este é o review mais importante porque valida os **dados que serão comunicados a stakeholders**.

##### A. Rastreabilidade

Para cada número/métrica no relatório final (`output/relatorio-*.md`):
- [ ] O número existe em algum output de `output/data-scientist/`
- [ ] A fonte específica (arquivo, tabela, linha) é identificável
- [ ] Se o número é derivado (calculado a partir de outros), os componentes existem

**Formato do check**: Listar as 5 métricas principais do relatório com seu valor e a fonte rastreada.

##### B. Consistência Aritmética

- [ ] **Totais = soma das partes**: Se relatório diz "Captação total: R$ 500M", a soma dos N4 (assessores) nos outputs do data-scientist deve ser R$ 500M
- [ ] **Percentuais somam 100%**: Se mostra distribuição por equipe (B2B 60%, B2C 40%), a soma deve ser 100%
- [ ] **Variações calculadas corretamente**: Se diz "crescimento MoM de +15%", verificar que (mês_atual / mês_anterior - 1) = 0.15
- [ ] **N1 vs soma N4**: Para indicadores com cubo hierárquico, verificar que realizado_N1 = Σ(realizado_N4). Sinalizar divergência > 1% como erro.

##### C. Coerência Temporal

- [ ] Período dos dados extraídos = período definido no PLANO-ANALISE.md
- [ ] Comparativos usam o período correto (YoY = mesmo mês do ano anterior, não mês adjacente)
- [ ] Se análise é mensal, todos os meses do período estão representados (sem gaps)

##### D. Cross-Check entre Métricas

- [ ] Se mesma métrica aparece em múltiplos outputs do data-scientist, os valores coincidem
- [ ] Indicadores `related_indicators` com relação `correlated` se comportam de forma coerente (se captação sobe, faturamento tende a subir com lag)
- [ ] Indicadores com relação `inverse` mostram comportamento oposto
- [ ] Se relação esperada não se confirma, deve estar sinalizado como anomalia (não ignorado)

##### E. Outliers e Anomalias

- [ ] Valores > 2 desvios-padrão da média estão sinalizados no relatório ou nos outputs
- [ ] Para cada outlier: existe explicação ou nota de investigação
- [ ] Concentração excessiva (top assessor > 30% do total) está documentada

##### F. Benchmarks e Contexto de Negócio

Se `docs/INDICADORES.md` documenta contexto de negócio para as métricas:
- [ ] Os benchmarks registrados foram aplicados corretamente (faixas de atingimento)
- [ ] A sazonalidade documentada foi considerada na interpretação
- [ ] Fatores externos relevantes ao período foram mencionados

##### G. Adequação à Audiência

- [ ] Linguagem do relatório é adequada à audiência definida no CLAUDE.md
- [ ] Nível de detalhe respeita limites:
  - Diretoria: max 2 páginas, 3 blocos, zero jargão técnico
  - Gerentes: max 3 páginas, 4 blocos, termos de negócio ok
  - Técnico: max 5 páginas, sem limite de blocos, termos técnicos ok
  - Comercial: max 3 páginas, 3 blocos, linguagem comercial
- [ ] Próximos passos incluem responsável e prazo
- [ ] Dados brutos NÃO aparecem para audiência Diretoria/Comercial

---

### 5. Gerar relatório de review

Apresentar resultado estruturado:

```
Review da Fase [N]: [Nome]
Data: YYYY-MM-DD

[Artefato 1]
  ✅ [check que passou]
  ✅ [check que passou]
  ⚠️ [aviso — não bloqueia mas deve ser notado]
  ❌ [erro — deve ser corrigido antes de avançar]

[Artefato 2]
  ✅ [check que passou]
  ...

Resumo:
  Total de checks: [N]
  Passou: [N] ✅
  Avisos: [N] ⚠️
  Erros:  [N] ❌

Veredicto: [APROVADO / APROVADO COM RESSALVAS / REPROVADO]
```

### 6. Resolver problemas

Para cada ❌ erro:
- Apresentar o problema com dados específicos (ex: "Captação N1 = R$ 500M, Σ(N4) = R$ 497.7M, diff = R$ 2.3M")
- Perguntar: "Corrigir agora, investigar causa, ou registrar como limitação?"
  - **Corrigir**: Invocar data-scientist para recalcular ou executive-communicator para ajustar
  - **Investigar**: Aprofundar no output do data-scientist para entender a divergência
  - **Registrar**: Adicionar nota de limitação no relatório

Para cada ⚠️ aviso:
- Apresentar e perguntar: "Adicionar nota explicativa no relatório ou ignorar?"

### 7. Resumo final

```
Review concluído:
  ✅ [N] checks aprovados
  ⚠️ [N] avisos registrados
  ❌ [N] erros [corrigidos/registrados como limitação]

Próximo passo:
  - Se aprovado → /m7-analise-dados:next para avançar
  - Se erros pendentes → corrigir e /m7-analise-dados:review novamente
  - /m7-analise-dados:status para ver progresso geral
```

## Anti-Patterns

- ❌ NUNCA aprovar Fase 3 com inconsistências aritméticas não explicadas
- ❌ NUNCA ignorar divergência entre N1 e Σ(N4) sem investigação
- ❌ NUNCA pular verificação de rastreabilidade — todo número no relatório deve ter origem
- ❌ NUNCA aprovar relatório com dados inventados (não rastreáveis a output/data-scientist/)
- ❌ NUNCA considerar outliers > 2σ como "normais" sem explicação documentada
- ❌ NUNCA aprovar relatório para Diretoria com mais de 2 páginas ou jargão técnico
