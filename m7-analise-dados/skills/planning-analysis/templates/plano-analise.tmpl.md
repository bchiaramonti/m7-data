# PLANO DE ANÁLISE — {{titulo_analise}}

> **Função deste arquivo**: contrato executável entre os agentes
> `data-scientist` (extração) e `executive-communicator` (briefing). Cada
> seção aqui mapeia diretamente a uma `§N` do briefing canônico
> (`analytics-briefing.tmpl.md`) — preencher este plano é **especificar o
> blueprint** do Analytics Report.
>
> **Diretório de trabalho** (path absoluto): `{{diretorio_absoluto}}`

---

## 1 · Identificação *(→ briefing §1 Controle)*

| Campo | Valor |
|---|---|
| `CODIGO_DOCUMENTO` | `ANL-{{AREA_SIGLA}}-{{NNN}}` *(ex.: `ANL-COM-001`)* |
| `VERSAO` | `v1.0` |
| `DATA_PLANO` | `YYYY-MM-DD` |
| `AREA_RESPONSAVEL` | {{area_negocio}} *(ex.: Comercial, Captação, Riscos)* |
| `DIRETORIA` | {{diretoria_responsavel}} |
| `ELABORADOR` | Nome · Cargo |
| `REVISOR` | Nome · Cargo |
| `APROVADOR` | Nome · Cargo |
| `CLASSIFICACAO` | `Interno · Confidencial` *(ou outra)* |
| `CADENCIA_REVISAO` | `Trimestral` *(ou `Mensal` / `Ad-hoc`)* |
| `DOC_SUPERIOR` *(opcional)* | Política/manual de referência (ex.: `POL-COM-001`) |

> Estes valores preenchem **diretamente** os tokens `{{CODIGO_DOCUMENTO}}`,
> `{{AREA_RESPONSAVEL}}`, `{{NOME_ELABORADOR}}`, etc. do briefing.

---

## 2 · Pergunta única *(→ briefing §2 Capa · `{{COVER_PERGUNTA}}`)*

**A análise responde, em UMA frase:**

> {{pergunta_unica_em_uma_frase}}

**Hipótese inicial** *(opcional; é o que esperamos encontrar):*

> {{hipotese_inicial}}

> ⚠ Regra dura: se você não consegue escrever a pergunta em uma frase,
> ainda não sabe o que vai investigar. Volte para a Fase 1 da skill.

---

## 3 · Audiência + Profundidade *(→ briefing §3 e §4 quotas)*

**Audiência primária**: {{Diretoria | Gerentes | Técnico | Comercial}}

Quotas aplicáveis (lookup direto em [audiencia-profundidade.md](../../planning-analysis/references/audiencia-profundidade.md)):

| Quota | Valor para esta audiência |
|---|---|
| KPIs no TL;DR (§3 briefing) | `4` (invariante) |
| KPIs no Scorecard (§4) | {{6-8 | 8-10 | 10-12 | 6-8}} |
| Blocos de análise (§6) | {{2-3 | 3-4 | 4-6 | 2-3}} |
| Subseções por bloco | {{2 | 2-3 | 3-5 | 2-3}} |
| Findings narrados (§7) | {{3-4 | 4-6 | 6-10 | 3-5}} |
| Recomendações (§8) | {{3-5 | 5-8 | 5-10 | 3-6}} |
| Páginas-alvo (PDF final) | {{8-12 | 12-18 | 18-30 | 8-14}} |
| Dados brutos no briefing | {{Nunca | Resumo | Completo (anexo) | Nunca}} |
| Linguagem técnica permitida | {{Não | Não | Sim | Não}} |

**Tom**: `{{Otimista | Cauteloso | Neutro | Alarmante}}`
**Restrições editoriais específicas desta análise**: {{...ou "N/A"}}

---

## 4 · Período & Snapshot *(→ briefing §5)*

| Campo | Valor |
|---|---|
| `PERIODO_PRINCIPAL` | `{{YYYY-MM → YYYY-MM}}` *(ex.: `jan/26 → mar/26`)* |
| `PERIODO_COMPARATIVO` | `{{periodo}}` *(ex.: `Q4-2025`)* |
| `DATA_SNAPSHOT` | `YYYY-MM-DD HH:MM` *(quando os dados foram extraídos)* |
| **Sazonalidade**: `{{alta | media | baixa}}` | Se `alta` → **YoY é obrigatório** em todos os KPIs temporais |
| **Eventos atípicos no período** | {{lista ou "Nenhum"}} |

---

## 5 · Fontes de Dados *(→ briefing §5 — tabela de fontes)*

Ordenadas por **relevância para a análise** (a fonte que dirige a história primeiro):

| # | Fonte (tabela/view/sistema) | MCP/Stack | Timeliness | Contribuição esperada |
|---|---|---|---|---|
| 1 | {{nome_técnico}} | {{MCP-x ou script Python ou arquivo}} | `D-0` / `D+1` / `D+7` / `M+1` | {{onde no briefing — ex.: "série mensal §3.1, base do KPI de captação"}} |
| 2 | | | | |
| 3 | | | | |

**DATA-PROFILE.md referenciado**: {{caminho ou "N/A — sem fase de discovery prévia"}}

> Convenção de timeliness: `D-0` tempo real · `D+1` 1 dia útil · `D+7`
> semanal · `M+1` mensal · `M+15` 15 dias após fechamento.

---

## 6 · Indicadores *(→ briefing §3 TL;DR + §4 Scorecard)*

**Fonte da verdade**: [docs/INDICADORES.md](../docs/INDICADORES.md) — **obrigatório**.

Sumário aqui (papel de cada métrica no briefing):

| # | Métrica | Papel | Unidade | Granularidade | Comparativo principal |
|---|---|---|---|---|---|
| 1 | {{nome}} | `destaque-tldr` | R$ mi | Mensal | vs Meta |
| 2 | {{nome}} | `destaque-tldr` | % | Mensal | YoY |
| 3 | {{nome}} | `destaque-tldr` | count | Mensal | MoM |
| 4 | {{nome}} | `destaque-tldr` | pontos | Trimestral | vs Benchmark |
| 5 | {{nome}} | `detalhe-scorecard` | R$ mi | Mensal | MoM |
| 6 | {{nome}} | `detalhe-scorecard` | | | |
| 7 | {{nome}} | `detalhe-scorecard` | | | |
| 8 | {{nome}} | `detalhe-scorecard` | | | |
| 9 | {{nome}} | `detalhe-scorecard` | | | |
| 10 | {{nome}} | `detalhe-scorecard` | | | |

> **Validação automática na Fase 7 da skill**:
> - Exatamente 4 métricas marcadas `destaque-tldr`
> - Entre 6 e 12 métricas no total
> - Nenhuma métrica `destaque-tldr` se repete entre os 4 primeiros do scorecard

---

## 7 · Blocos de análise *(→ briefing §6)*

Cada bloco responde **uma** pergunta. A numeração da seção no briefing é
manual (`03`, `04`, ...), iniciando em `03` após TL;DR (`01`) e Contexto (`02`).

### Bloco 1 — {{titulo_bloco}}

- **Pergunta**: {{pergunta_específica_uma_frase}}
- **Tipo de gráfico**: {{tipo_canônico_dos_12}} *(consulte [grafico-por-bloco.md](../references/grafico-por-bloco.md))*
- **Métricas usadas**: M1, M3, M7 *(referência ao §6 Indicadores acima)*
- **Subseções**: {{N}} *(respeitar quota da audiência)*
- **Hipótese de leitura**: {{o que esperamos ver — base para o `{{A_SUBN_GRAFICO_LEITURA}}` do briefing}}
- **Instrução estruturada para data-scientist**:
  - Query/extração: {{descrição calculável}}
  - Comparativos a calcular: {{lista}}
  - Validações específicas: {{nulls, outliers, gaps}}
- **Cortes investigativos se anomalia**: {{por canal, por região, por assessor — definir antes para não improvisar depois}}

### Bloco 2 — {{titulo_bloco}}

*(repetir estrutura para cada bloco; respeitar a quota da audiência da §3)*

---

## 8 · Findings esperados *(→ briefing §3 TL;DR + §7 narrados)*

Hipóteses do que vamos encontrar. **Hipóteses, não fatos** — o data-scientist
confirma ou refuta. Cada finding tem ID que será reutilizado no briefing.

| ID | Hipótese de finding (1 frase) | Hipótese de IMPACTO (o "e daí?") | Evidência esperada |
|---|---|---|---|
| F-01 | {{frase única, conclusão hipotética}} | {{o que muda na decisão se confirmado}} | {{Bloco N · subseção N.M}} |
| F-02 | | | |
| F-03 | | | |

> Quotas: respeitar §3 "Findings narrados" da audiência. Findings sem
> hipótese de IMPACTO são bloqueio — se não conseguimos antecipar o "e daí?",
> provavelmente o finding não é decisão-relevante.

---

## 9 · Recomendações candidatas *(→ briefing §8)*

Hipóteses de ação. O briefing final pode adicionar/refinar, mas planejá-las
aqui força disciplina: não geramos análise que não desemboca em decisão.

| ID | Ação imperativa (1 frase) | Dono provável | Prazo provável | Decorre de | ICE estimado |
|---|---|---|---|---|---|
| R-01 | {{ex.: Limitar concentração de canal a 65%}} | {{cargo}} | `Q2-2026` | `F-01` | `8.5` |
| R-02 | | | | | |
| R-03 | | | | | |

> **ICE** = (Impacto 1-10 × Confiança 1-10) ÷ Esforço 1-10. Priorize ≥ 6.
> Sem dono identificado, a recomendação não entra no briefing — é desejo,
> não ação.

---

## 10 · Instruções estruturadas para os agentes

### Para o `data-scientist`

1. **Ler obrigatoriamente**: este plano + `docs/INDICADORES.md` (não existe? abortar e pedir replanejamento)
2. **Executar por bloco**: ver §7 acima — cada bloco já tem query/extração + comparativos + validações declarados
3. **Validar qualidade**: checklist padrão (nulls, gaps temporais, outliers > 3σ, schema match, volume coerente)
4. **Cross-source join** (se aplicável): seguir o padrão de join em Python documentado em `references/analysis-patterns.md` (§ Padrão 7)
5. **Salvar outputs em**: `output/data-scientist/<nome-bloco>.md` — uma tabela por bloco, com rastreabilidade explícita (fonte, query, snapshot)
6. **Reportar anomalias**: se algum finding hipotetizado (§8) é claramente refutado pelos dados, sinalizar no output — não silenciar

### Para o `executive-communicator`

1. **Ler obrigatoriamente**: este plano + outputs do data-scientist + `docs/INDICADORES.md` (para benchmarks e contexto) + briefing canônico (`analytics-briefing.tmpl.md`)
2. **Audiência**: {{audiencia}} (todas quotas da §3 deste plano são duras)
3. **Mapeamento direto** plano → briefing:
   - §1 Identificação deste plano → §1 Controle do briefing (cópia 1:1)
   - §2 Pergunta única → `{{COVER_PERGUNTA}}` do briefing
   - §6 Indicadores com `destaque-tldr` → 4 KPIs do TL;DR (§3)
   - §6 Indicadores com `detalhe-scorecard` → Scorecard (§4)
   - §7 Blocos → §6 Análises do briefing (1 bloco = 1 `<article class="page">`)
   - §8 Findings → §3 cards + §7 cards narrados (com IMPACTO)
   - §9 Recomendações → §8 do briefing (cards com ICE)
4. **Iterar com data-scientist se necessário**: até 3 ciclos (protocolo de Solicitação Complementar)
5. **Salvar briefing em**: `output/ANL-{{AREA}}-{{NNN}}-briefing.md`

---

## 11 · Critério de Conclusão

Antes de marcar o plano como `concluído` e iniciar a Fase 3:

- [ ] §1 Identificação completa (todos os campos preenchidos, código `ANL-` definido)
- [ ] §2 Pergunta única escrita em UMA frase
- [ ] §3 Audiência + Profundidade com quotas extraídas da matriz
- [ ] §4 Período principal e comparativo definidos; data de snapshot reservada
- [ ] §5 Fontes com timeliness e contribuição preenchidos para todas
- [ ] §6 Indicadores: exatamente 4 `destaque-tldr` + 6-8 `detalhe-scorecard`, sem overlap
- [ ] `docs/INDICADORES.md` existe e tem entrada completa para cada métrica do §6
- [ ] §7 Blocos: cada bloco tem pergunta + tipo de gráfico canônico + métricas + instrução estruturada
- [ ] §8 Findings: cada um com hipótese de IMPACTO ("e daí?") preenchida
- [ ] §9 Recomendações: cada uma com dono provável + prazo + ICE estimado
- [ ] §10 Instruções para ambos agentes preenchidas
- [ ] Estrutura de pastas criada com path absoluto explícito

**Critério específico desta análise**: {{...regra adicional que fecha a análise — ex.: "Confirmar se a inflexão Q1 é estrutural (3 evidências independentes apontando para cima)"}}

---

*Template versão 4.0.0 — espelha 1:1 a estrutura do briefing canônico
`analytics-briefing.tmpl.md` do M7 Design System. Cada token aqui tem
correspondência direta no HTML final gerado no Claude Design.*
