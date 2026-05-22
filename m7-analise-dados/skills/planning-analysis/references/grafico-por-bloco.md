# Gráfico por Bloco — Decisão dos 12 Tipos Canônicos

Mapa de decisão para escolher **qual dos 12 tipos canônicos** do M7 Design
System cada bloco de análise vai usar. O briefing canônico
(`analytics-briefing.tmpl.md`, §6) exige um tipo por subseção — esta tabela
torna a escolha determinística.

> **Source-of-truth visual**: `graficos.html` no M7 Design System.
> Cada tipo aqui aponta o `<svg viewBox>` que o Claude Design vai consumir.
> Esta skill **não renderiza** gráficos — apenas declara qual tipo cada
> bloco precisa.

---

## Decisão por pergunta

Comece pela **pergunta da subseção**. O tipo de gráfico é função da pergunta,
não do dataset.

| Pergunta da subseção | Tipo canônico | # do DS |
|---|---|---|
| "Estamos no alvo / batemos a meta?" | **Resultado vs meta** | 01 |
| "Onde estão os poucos que respondem por muito?" / "Concentração?" | **Pareto · 80/20** | 02 |
| "Quem é maior / menor?" / "Ordem dessas categorias?" | **Ranking · barras horizontais** | 03 |
| "Como esta entidade se compara em várias dimensões?" | **Radar · perfil multidimensional** | 04 |
| "Como essas entidades se conectam / dependem entre si?" | **Teia · rede de relações** | 05 |
| "Existe correlação entre A e B?" / "Risco × retorno?" | **Dispersão · risco × retorno** | 06 |
| "Como esses valores se distribuem?" / "Onde está a maioria?" | **Histograma · distribuição** | 07 |
| "Como o todo se reparte em muitas categorias hierárquicas?" | **Treemap · composição hierárquica** | 08 |
| "Como evoluiu ao longo do tempo?" / "Há tendência?" | **Linha temporal** | 09 |
| "Por que esse número virou esse?" / "O que contribuiu?" | **Waterfall · ponte** | 10 |
| "Qual a perda em cada etapa do funil?" | **Funil comercial** | 11 |
| "Decomponha esse total nas suas causas-raiz" | **Árvore de decomposição** | 12 |

---

## Decisão por intenção editorial

Outra entrada: o que você quer que o leitor **conclua** ao olhar o gráfico.

| Quero que o leitor conclua... | Tipo |
|---|---|
| "Estamos OK / no alvo" — confirmação binária com magnitude | 01 Resultado vs meta |
| "Concentração é um risco" — 80/20 desbalanceado | 02 Pareto |
| "X domina; Y é marginal" — hierarquia clara | 03 Ranking |
| "Esta entidade é forte em A mas fraca em B" — perfil | 04 Radar |
| "A rede tem nós críticos" — topologia importa | 05 Teia |
| "Quando A sobe, B sobe junto" — relação contínua | 06 Dispersão |
| "A maioria está nessa faixa" — forma da distribuição | 07 Histograma |
| "O peso de cada componente do todo" — composição | 08 Treemap |
| "Há tendência / inflexão / sazonalidade" — temporal | 09 Linha |
| "Esse delta veio de aqui, aqui e aqui" — atribuição | 10 Waterfall |
| "Perdemos X% entre etapas" — funil | 11 Funil |
| "A causa-raiz é Y, não Z" — decomposição | 12 Árvore |

---

## Restrição por audiência

Cruzando com `audiencia-profundidade.md`:

| Audiência | Tipos recomendados | Tipos a evitar |
|---|---|---|
| **Diretoria** | 01 Resultado vs meta, 03 Ranking, 09 Linha, 10 Waterfall | 04 Radar, 05 Teia, 06 Dispersão, 07 Histograma (técnicos demais) |
| **Gerentes** | + 02 Pareto, 08 Treemap, 11 Funil | 05 Teia, 06 Dispersão (a menos que seja métrica nuclear da reunião) |
| **Técnico** | Os 12 tipos disponíveis | — |
| **Comercial** | 01 Resultado vs meta, 03 Ranking, 11 Funil | 04 Radar, 05 Teia, 06 Dispersão, 07 Histograma, 12 Árvore |

> Diretoria/Comercial **podem** receber outros tipos se a história exigir —
> mas exige justificativa explícita no plano ("este Radar é central
> porque..."). Default é manter na lista recomendada.

---

## Anti-padrões cromáticos / editoriais

- ❌ **Pizza com >6 fatias** — use Treemap (08) ou Pareto (02)
- ❌ **Gráfico de barras simples para evolução temporal** — use Linha (09)
- ❌ **Linha para comparar categorias estáticas** — use Ranking (03)
- ❌ **Dois eixos Y com escalas diferentes** — use 2 gráficos lado a lado, sempre
- ❌ **Histograma sem média e mediana marcadas** — perde o ponto
- ❌ **Waterfall sem total inicial e total final visíveis** — quebra a leitura "X virou Y"
- ❌ **Funil com etapas reordenadas para parecer melhor** — fraude visual
- ❌ **Radar com escalas heterogêneas** (uma dimensão 0-100, outra 0-10) — desinforma
- ❌ **Combinar dois tipos canônicos sem justificar no rodapé do briefing** (ex.: Pareto + Linha sobrepostos)
- ❌ **Inventar um 13º tipo fora do DS** — quebra consistência editorial e a renderização no Claude Design

---

## Liberdade do analista (com limites)

A lista é um mapa de decisão, não uma camisa de força. Se a análise pede:

- **Combinação de dois canônicos** (ex.: Pareto + Ranking lateral): permitido, mas o `PLANO-ANALISE.md` deve declarar explicitamente "Bloco N: combina tipos 02+03 — justificativa: [...]"
- **Vista diferente do mesmo tipo** (ex.: Ranking invertido começando pelo menor): permitido, sem ressalva
- **Tipo inteiramente novo**: **bloqueio editorial** — para de planejar, conversa com o owner do DS. Critérios: (1) será reutilizado em outros briefings? (2) cabe em A4? (3) é editorialmente claro? Se algum "não", abandone

---

## Como o plano declara o gráfico

No `PLANO-ANALISE.md` § Blocos de análise:

```markdown
### Bloco 1 — Há inflexão estrutural em Q1?

- **Pergunta**: A inflexão de captação de Q1 é evento isolado ou tendência?
- **Tipo de gráfico**: 09 Linha temporal (intenção: "há tendência")
- **Métricas**: Captação líquida mensal · YoY · Média móvel 3m
- **Hipótese de leitura**: Se últimos 3 pontos > média móvel, é tendência
```

O `executive-communicator` lê esse bloco e popula `{{A_SUBN_GRAFICO_TITULO}}`
do briefing como "Linha temporal — Captação Q1 2026". O Claude Design depois
busca o `<svg>` correspondente no `graficos.html` do DS.
