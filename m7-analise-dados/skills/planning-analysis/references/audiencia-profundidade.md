# Audiência → Profundidade do Plano

Matriz canônica para calibrar **quantidade** de cada artefato do briefing
canônico (`analytics-briefing.tmpl.md`) por audiência. Use na Fase 2 da skill
`planning-analysis` para fixar restrições antes de modelar análises e blocos.

> A skill `generating-executive-reports` tem o **framework qualitativo**
> completo (linguagem, tom, ceticismo) em
> `references/audience-adaptation-framework.md`. Este arquivo aqui é o
> **lookup quantitativo** que o planning usa para dimensionar o plano.

---

## Matriz mestre

| Dimensão do plano | Diretoria | Gerentes | Técnico | Comercial |
|---|---|---|---|---|
| **KPIs no TL;DR (§3 briefing)** | 4 | 4 | 4 | 4 |
| **KPIs no Scorecard (§4)** | 6–8 | 8–10 | 10–12 | 6–8 |
| **Blocos de análise (§6)** | 2–3 | 3–4 | 4–6 | 2–3 |
| **Subseções por bloco** | 2 | 2–3 | 3–5 | 2–3 |
| **Findings narrados (§7)** | 3–4 | 4–6 | 6–10 | 3–5 |
| **Recomendações (§8)** | 3–5 | 5–8 | 5–10 | 3–6 |
| **Páginas-alvo (PDF final)** | 8–12 | 12–18 | 18–30 | 8–14 |
| **Tipos de gráfico permitidos** | "Estamos no alvo?" + "Quem é maior?" | + composição + ponte | Os 12 tipos | + ranking + funil |
| **Dados brutos no briefing** | Nunca | Resumo agregado | Completo (anexo) | Nunca |
| **Linguagem técnica (SQL/p-value/schema)** | Zero | Zero | Permitido | Zero |
| **Comparativos exigidos por KPI** | vs Meta + 1 outro | 2 | 2–3 | vs Meta + ranking |

---

## Quotas duras (use no checklist da Fase 2)

Estas são as **regras inegociáveis** ao gerar o `PLANO-ANALISE.md`:

| Regra | Aplicabilidade |
|---|---|
| **Sempre 4 KPIs no TL;DR** — não mais, não menos | Todas as audiências |
| **Os 4 do TL;DR NÃO podem duplicar os 4 primeiros do scorecard** | Todas |
| **Soma destaque-tldr + detalhe-scorecard ≤ 12** no `INDICADORES.md` | Todas |
| **Cada bloco de análise indica 1 dos 12 tipos canônicos** de `grafico-por-bloco.md` | Todas |
| **Diretoria nunca recebe dados brutos** — nem em anexo | Diretoria + Comercial |
| **Técnico pode ter SQL inline no briefing** — outros não | Só Técnico |
| **Recomendações sem dono são bloqueio** — todo R-N tem owner | Todas |

---

## Roteiro de uso na Fase 2 da skill

Depois de coletar a audiência na Fase 1:

1. **Bater na matriz**: lookup das 11 dimensões para essa audiência
2. **Fixar as quotas no plano**: copiar os valores diretamente para a §3
   `Audiência + Profundidade` do `PLANO-ANALISE.md`
3. **Validar restrições**: se o usuário pedir 8 blocos para Diretoria,
   sinalizar: "Diretoria suporta 2–3 blocos; quer (a) reduzir escopo,
   (b) trocar audiência ou (c) gerar dois briefings — um TL;DR para
   Diretoria e um Detalhado para Gerentes/Técnico?"
4. **Usar as quotas como gate da Fase 5** (modelar blocos) e Fase 6
   (findings + recomendações) — não exceder

---

## Convenções de leitura

- **TL;DR (§3 do briefing)** sempre 4 KPIs — invariante do template, não da audiência. O que muda é **quais** 4 (Diretoria foca em risco/ROI; Comercial em ranking/oportunidade)
- **Scorecard (§4)** é variável: Diretoria aceita só 6–8 porque "menos = mais leitura"; Técnico aceita 10–12 porque consegue absorver
- **Páginas-alvo** referencia o **PDF final** (gerado no Claude Design), não o briefing markdown. Diretoria recebe um PDF de ~10 páginas; Técnico recebe ~25
- **Comparativos exigidos** é o piso. Sempre pode ter mais — nunca menos

---

## Quando reabrir esta matriz

- **Audiência híbrida** (ex.: Diretoria + Gerentes em uma única reunião): use a quota mais restritiva (Diretoria) — sempre é mais seguro corta-curto do que sobrecarregar
- **Reuso para skills futuras** (dashboards, status reports, talking points): a matriz cobre o **briefing canônico** especificamente. Outros formatos têm seus próprios limites — não estender daqui sem reavaliação
- **Conflito com `audience-adaptation-framework.md`** da skill downstream: este arquivo prevalece para **dimensionamento** (quantos); o framework downstream prevalece para **adaptação qualitativa** (como falar). Eles são complementares, não concorrentes

## Anti-padrões

- ❌ Tratar a matriz como sugestão — quotas são duras (especialmente "4 KPIs no TL;DR" e "destaque-tldr não duplica scorecard")
- ❌ "Splittar a diferença" entre audiências (ex.: 5 blocos para "atender Diretoria e Gerentes") — gera relatório que não serve para ninguém
- ❌ Ignorar a coluna "Tipos de gráfico permitidos" — Radar e Teia em briefing pra Diretoria viram ruído
- ❌ Encher o scorecard de Comercial com 12 indicadores — a audiência Comercial quer ranking e meta, não dashboard
