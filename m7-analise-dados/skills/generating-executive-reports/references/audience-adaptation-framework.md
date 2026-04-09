# Framework de Adaptação por Audiência

Guia completo para calibrar relatórios executivos para 4 perfis de audiência × 6 dimensões de adaptação.

---

## Os 4 Perfis

### 1. Diretoria / C-Level

**Quem são**: CEO, CIO, diretores, sócios, board.
**O que precisam**: Decisões informadas em 2-3 minutos.

| Dimensão | Calibração |
|----------|------------|
| **Conhecimento** | Sabem do negócio, não dos detalhes. Contexto mínimo. |
| **Poder de decisão** | Aprovam orçamento, prioridades estratégicas, go/no-go. |
| **Tempo** | 2-3 minutos. 1 página de síntese + 1 de suporte. |
| **Preocupações** | "Estamos no caminho? Qual o risco? Quanto custa?" |
| **Linguagem** | Zero jargão. R$, %, impacto, ROI, risco. |
| **Ceticismo** | Varia. Sempre incluir limitações proativamente. |

**Estrutura recomendada:**
```
Síntese (tabela 3-5 métricas) → Resultado principal (1 frase)
→ Max 3 blocos (3-5 bullets cada) → Próximos passos (decisões com prazo)
```

**O que incluir:**
- Números com comparativos (vs meta, vs ano anterior)
- Impacto financeiro em R$
- Decisões necessárias com deadline
- Riscos enquadrados como decisões

**O que NÃO incluir:**
- Metodologia técnica
- Queries SQL ou schemas
- Mais de 3 blocos temáticos
- Dados brutos

---

### 2. Gerentes / Sponsors

**Quem são**: Gerentes, coordenadores, sponsors de projeto, heads de área.
**O que precisam**: Visão operacional para ação e alocação.

| Dimensão | Calibração |
|----------|------------|
| **Conhecimento** | Conhecem a operação e métricas de domínio. |
| **Poder de decisão** | Alocação de recursos, priorização, escalação. |
| **Tempo** | 5-10 minutos. 2-3 páginas. |
| **Preocupações** | "O que fazer? Quem é responsável? Qual o prazo?" |
| **Linguagem** | Negócio + domínio (SLA, conversion, pipeline, AuC). |
| **Ceticismo** | Geralmente neutros. Querem fatos para tomar ação. |

**Estrutura recomendada:**
```
Síntese (5-8 métricas) → Max 4 blocos (4-6 bullets cada)
→ Destaques e alertas → Ações com responsável e prazo
```

**O que incluir:**
- Métricas operacionais com tendência
- Comparativos contextualizados
- Alertas de desvio com impacto estimado
- Ações com owner e deadline

**O que NÃO incluir:**
- Dados brutos completos (apenas resumos)
- Detalhes técnicos de extração
- Mais de 4 blocos temáticos

---

### 3. Técnico / Equipe

**Quem são**: Analistas, desenvolvedores, equipe de dados, operações.
**O que precisam**: Entender os dados, a metodologia e as limitações.

| Dimensão | Calibração |
|----------|------------|
| **Conhecimento** | Conhecem os dados e ferramentas. Podem ver queries. |
| **Poder de decisão** | Implementação, escolhas técnicas, escalação. |
| **Tempo** | 15-30 minutos. 3-5 páginas. |
| **Preocupações** | "Os dados são confiáveis? Qual a metodologia? Limitações?" |
| **Linguagem** | Técnica permitida. SQL, correlação, p-value, schema. |
| **Ceticismo** | Alto em relação aos dados. Querem ver a metodologia. |

**Estrutura recomendada:**
```
Síntese executiva (1 parágrafo) → Metodologia → Resultados detalhados
→ Limitações e caveats → Dados brutos / links → Tasks e next steps
```

**O que incluir:**
- Metodologia de extração e transformação
- Queries utilizadas (ou referência)
- Estatísticas de qualidade dos dados
- Todas as métricas com precisão
- Limitações e caveats explícitos
- Links para dados brutos

**O que NÃO incluir:**
- Narrativa estratégica excessiva (eles formam as próprias conclusões)
- Simplificação excessiva de números

---

### 4. Comercial / Assessores

**Quem são**: Assessores de investimento, equipe comercial, gestores de carteira.
**O que precisam**: Saber onde estão as oportunidades e como se comparam.

| Dimensão | Calibração |
|----------|------------|
| **Conhecimento** | Conhecem os clientes e produtos. Falar em oportunidades. |
| **Poder de decisão** | Abordagem de clientes, priorização de carteira. |
| **Tempo** | 5 minutos. 2-3 páginas, direto ao ponto. |
| **Preocupações** | "Onde estão as oportunidades? Como me comparo?" |
| **Linguagem** | Comercial + competitivo. Rankings, metas, ticket médio. |
| **Ceticismo** | Baixo se veem oportunidade. Alto se veem cobrança. |

**Estrutura recomendada:**
```
Metas e progresso (tabela visual) → Rankings (top performers)
→ Oportunidades por segmento → Ações com meta clara
```

**O que incluir:**
- Rankings de performance (com contexto, não punição)
- Progresso vs meta (com % e gap)
- Top oportunidades por segmento/produto
- Ações com meta numérica clara
- Benchmarks da equipe

**O que NÃO incluir:**
- Metodologia técnica
- Dados brutos (só rankings processados)
- Tom punitivo ou de cobrança

---

## Regras Universais (Todas as Audiências)

1. **Todo número com comparativo** — "R$ 150M" sozinho não comunica. "R$ 150M (+15% vs meta)" comunica.
2. **Liderar com o mais importante** — primeira frase de cada bloco é o resumo.
3. **Dados são evidência, não decoração** — cada número deve suportar um argumento.
4. **Ser honesto sobre limitações** — dados incompletos são mencionados, não escondidos.
5. **Ação > Descrição** — preferir "Reduzir concentração" a "A concentração é alta".

---

## Tabela de Calibração Rápida

| Aspecto | Diretoria | Gerentes | Técnico | Comercial |
|---------|-----------|----------|---------|-----------|
| **Métricas** | 3-5 chave | 5-8 com contexto | Todas + metodologia | Rankings + metas |
| **Blocos** | Max 3 | Max 4 | Sem limite | Max 3 |
| **Bullets/bloco** | 3-5 | 4-6 | Sem limite | 3-5 |
| **Páginas** | 1-2 | 2-3 | 3-5 | 2-3 |
| **Linguagem** | Zero jargão | Negócio + domínio | Técnica ok | Comercial |
| **Dados brutos** | Nunca | Resumo | Completo | Nunca |
| **Metodologia** | Nunca | Resumo se relevante | Obrigatório | Nunca |
| **CTA** | Decisão + deadline | Ação + owner + prazo | Tasks + timeline | Meta + oportunidade |
