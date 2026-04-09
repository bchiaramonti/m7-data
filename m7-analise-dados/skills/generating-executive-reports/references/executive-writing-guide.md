# Guia de Escrita Executiva

Fórmulas, padrões e anti-patterns para comunicação executiva baseada em dados.

---

## Fórmula do Bullet Point Executivo

```
**[Título impactante — max 5 palavras]:** [Interpretação 1-2 frases]
= [dado numérico] + [contexto do negócio] + [implicação ou ação]
```

### Exemplos

**Bom:**
- **Captação acima da meta:** R$ 230M de captação líquida no trimestre (+15% vs meta de R$ 200M), impulsionada pela campanha de renda fixa que trouxe 42% do volume.
- **Concentração preocupante:** Os 5 maiores clientes representam 67% do AuC total (R$ 1,2B de R$ 1,8B). Perda de qualquer um impactaria significativamente a receita.
- **Pipeline aquecido:** 142 deals em negociação com valor total de R$ 89M, 35% acima do mesmo período do ano anterior.

**Ruim:**
- ❌ "A captação foi boa no trimestre." (vago, sem número)
- ❌ "R$ 230M de captação." (número sem contexto)
- ❌ "Notamos uma tendência interessante nos dados." (vago, sem dado)

---

## Padrões de Linguagem Executiva

### Verbos de Ação (usar)

| Situação | Verbos |
|----------|--------|
| Crescimento | Cresceu, avançou, acelerou, superou |
| Queda | Recuou, retraiu, caiu, desacelerou |
| Estabilidade | Manteve, estabilizou, consolidou |
| Risco | Requer atenção, demanda ação, exige decisão |
| Oportunidade | Apresenta potencial, abre espaço, viabiliza |
| Recomendação | Priorizar, intensificar, reduzir, ajustar |

### Quantificação Precisa (usar)

| Em vez de... | Escrever... |
|-------------|-------------|
| "melhorou significativamente" | "+23% vs trimestre anterior" |
| "número expressivo" | "R$ 150,3M" |
| "a maioria" | "67% (134 de 200)" |
| "crescimento recente" | "+R$ 12M em fevereiro (+8% MoM)" |
| "poucos clientes" | "5 clientes (3% da base)" |
| "resultado positivo" | "R$ 45M acima da meta" |

### Comparativos Claros (usar)

Todo número DEVE ter uma referência:

| Tipo | Formato | Exemplo |
|------|---------|---------|
| vs Meta | `(+X% vs meta de Y)` | R$ 230M (+15% vs meta de R$ 200M) |
| MoM | `(+X% vs mês anterior)` | R$ 80M (+12% vs janeiro) |
| YoY | `(+X% vs mesmo período ano anterior)` | R$ 230M (+28% YoY) |
| vs Média | `(X% acima/abaixo da média de Y)` | 4,2 deals/dia (18% acima da média de 3,6) |
| Ranking | `(#N de M)` | Assessor João (#3 de 45 em captação) |

---

## Enquadrando Riscos como Decisões

### Ruim: Descrever risco passivamente
❌ "Há um risco de concentração nos maiores clientes."
❌ "A equipe pode não atingir a meta no trimestre."

### Bom: Enquadrar como decisão necessária
✅ "Precisamos decidir até [data] se expandimos a base ativa (67% concentrado em 5 clientes, R$ 1,2B em risco)."
✅ "O gap de R$ 30M vs meta exige decisão: intensificar campanha de renda fixa (maior volume) ou ativar programa de indicação (maior ticket)."

### Fórmula
```
"Precisamos [verbo de ação] [o quê] até [quando],
porque [dado numérico que evidencia urgência]."
```

---

## Estrutura de Blocos Temáticos

Cada bloco segue o padrão **Título → Contexto → Evidência → Implicação**:

```markdown
## Bloco N — [Tema em 2-3 palavras]

- **[Destaque 1 — max 5 palavras]:** [1-2 frases com dado + contexto + implicação]

- **[Destaque 2 — max 5 palavras]:** [1-2 frases com dado + contexto + implicação]

- **[Destaque 3 — max 5 palavras]:** [1-2 frases com dado + contexto + implicação]
```

### Regras dos Blocos:
- Máximo 3-5 bullets por bloco (Diretoria: 3, Técnico: 5+)
- Cada bullet é autocontido — faz sentido isoladamente
- Ordenar por impacto (mais importante primeiro)
- Separar fatos de recomendações

---

## Tabela de Síntese

A tabela de síntese abre o relatório e resume os KPIs principais:

```markdown
| Métrica | Valor | Referência | Status |
|---------|-------|------------|--------|
| **Captação líquida** | R$ 230M | Meta: R$ 200M (+15%) | ✅ |
| **AuC total** | R$ 1,8B | YoY: +22% | ✅ |
| **Concentração Top 5** | 67% | Target: <50% | ⚠️ |
| **Deals em pipeline** | 142 | MoM: +35% | ✅ |
```

**Regras:**
- 3-5 linhas para Diretoria, 5-8 para Gerentes
- Coluna Status: ✅ (no track), ⚠️ (atenção), ❌ (off track)
- Referência sempre presente (meta, YoY, MoM, benchmark)

---

## Anti-Patterns de Escrita Executiva

| Anti-Pattern | Problema | Solução |
|-------------|----------|---------|
| **Número sem contexto** | "R$ 150M" — é bom ou ruim? | Sempre incluir referência |
| **Adjetivo vago** | "resultado significativo" | Substituir por número |
| **Passiva excessiva** | "foi observado que" | Usar voz ativa: "a captação cresceu" |
| **Jargão técnico** | "correlação de 0.85" (para Diretoria) | Traduzir: "forte relação entre X e Y" |
| **Lista sem hierarquia** | 10 bullets igualmente importantes | Ordenar por impacto, limitar a 5 |
| **Conclusão sem dado** | "acreditamos que vai melhorar" | Basear em evidência ou declarar como hipótese |
| **Risco sem ação** | "a concentração é preocupante" | Enquadrar como decisão necessária |
| **Dado inventado** | Arredondar ou estimar sem indicar | Usar valores exatos do data-scientist |

---

## Fórmula de Próximos Passos

```markdown
- **[Ação específica]:** [Descrição concisa] — **Responsável**: [quem] — **Prazo**: [quando]
```

### Regras:
- Ação é verbo no infinitivo (Aprovar, Reduzir, Implementar, Avaliar)
- Responsável é cargo ou nome (não "a equipe" ou "alguém")
- Prazo é data ou semana (não "em breve" ou "no futuro")
- Se não sabe o responsável, usar "[a definir pelo sponsor]"

### Exemplos:
- **Expandir base ativa:** Lançar programa de indicação para reduzir concentração dos Top 5 de 67% para <50% — **Responsável**: Head Comercial — **Prazo**: até 30/04
- **Investigar gap de dados:** 15% de nulls na coluna X impactam a precisão da análise — **Responsável**: Equipe de dados — **Prazo**: próxima sprint
