# Briefing de análise — guia de preenchimento

> **O que é isso?**
> Este markdown é a **fonte da verdade** do conteúdo de um Analytics Report.
> Preencha aqui ANTES de tocar no template HTML — depois é só transcrever
> os valores para os `{{PLACEHOLDERS}}` correspondentes.
>
> **Por que não escrever direto no HTML?**
> 1. Markdown é mais rápido de pensar e revisar
> 2. Você consegue compartilhar o briefing antes de ter o documento final
> 3. Find & replace fica trivial quando todo o conteúdo está estruturado
> 4. Serve de registro: o briefing fica versionado junto com o relatório

---

## Como usar

1. Copie este arquivo: `analytics-briefing.md` → `ANL-{AREA}-{NNN}-briefing.md`
2. Preencha cada seção numerada. Apague os blocos `>` (instruções) ao terminar.
3. Cada token `{{NOME}}` aqui é o mesmo do template HTML — a transferência é 1:1.
4. Quando estiver completo:
   - Duplique `templates/template-analytics.html`
   - Renomeie para o código do documento
   - Use o "Find & Replace" do editor: para cada `{{NOME}}`, cole o valor daqui
   - Para gráficos: vá em `graficos.html` do DS, escolha o tipo, copie o `<svg>`
   - Abra no navegador, ⌘P, salve PDF

---

## Princípios

Antes de começar, fixe três coisas:

1. **Pergunta única.** Toda análise responde uma pergunta. Se você não consegue escrevê-la em uma frase, você ainda não sabe o que está investigando.
2. **Conclusão antes do dado.** O leitor lê a resposta primeiro (TL;DR), depois o caminho. Nunca o contrário.
3. **Toda métrica precisa de referência.** Número solto não tem juízo. Compare contra meta, período anterior ou benchmark — sempre.

---

## 1 · Controle do documento

> A página de controle é a "carteira de identidade" do relatório.
> Toda referência cruzada interna usa `{{CODIGO_DOCUMENTO}}`.

| Token | O que preencher | Exemplo |
|---|---|---|
| `{{CODIGO_DOCUMENTO}}` | Código canônico `ANL-{ÁREA}-{NNN}` | `ANL-COM-001` |
| `{{VERSAO_COMPLETA}}` | Versão + data ISO | `v1.0 · 2026-04-15` |
| `{{VERSAO_CURTA}}` | Só a versão | `v1.0` |
| `{{TIPO_DOCUMENTO}}` | Categoria + cadência | `Analytics Report · Trimestral` |
| `{{TIPO_DOCUMENTO_SIGLA}}` | 3 letras | `ANL` |
| `{{CADENCIA_REVISAO}}` | Quando revisa de novo | `Trimestral` |
| `{{AREA_RESPONSAVEL}}` | Área de negócio | `Comercial` |
| `{{DIRETORIA}}` | Diretoria responsável | `Diretoria Comercial` |
| `{{PERIODO_ANALISADO_DETALHE}}` | Janela analisada | `jan/26 → mar/26` |
| `{{FONTE_PRIMARIA}}` | Tabela/sistema-fonte | `fact_captacao_v2` |
| `{{NOME_ELABORADOR}}` / `{{CARGO_ELABORADOR}}` | Quem escreveu | `Maria Silva · Head de Inteligência` |
| `{{NOME_REVISOR}}` / `{{CARGO_REVISOR}}` | Quem revisou | `João Costa · Analista Sr.` |
| `{{NOME_APROVADOR}}` / `{{CARGO_APROVADOR}}` | Quem assinou | `Pedro Lima · Diretor Comercial` |
| `{{CLASSIFICACAO_DOCUMENTO}}` | Nível de confidencialidade | `Interno · Confidencial` |
| `{{DOC_SUPERIOR_CODIGO}}` / `{{DOC_SUPERIOR_TITULO}}` | Política ou manual de referência (opcional) | `POL-COM-001 · Política Comercial` |

---

## 2 · Capa

> A capa entrega 3 coisas: **o quê** (título), **por quê** (pergunta), **quando** (período).

| Token | Diretriz | Exemplo |
|---|---|---|
| `{{COVER_TITULO_LINHA1}}` | Linha grande, ~3 palavras | `Comercial em` |
| `{{COVER_TITULO_LINHA2}}` | Linha grande, complemento | `aceleração estrutural` |
| `{{COVER_TITULO_DESTAQUE}}` | Palavra da L2 com fundo lime | `aceleração` |
| `{{COVER_SUBTITULO}}` | 1-2 linhas explicando o relatório | `Análise de captação Q1-2026 vs. plano e vs. trimestre anterior.` |
| `{{COVER_PERGUNTA}}` | Pergunta de pesquisa em UMA frase | `A inflexão de Q1 é evento ou tendência estrutural?` |
| `{{TITULO_RELATORIO}}` | Versão curta usada nos cabeçalhos das demais páginas | `Análise Comercial Q1-2026` |
| `{{PERIODO_REFERENCIA}}` | Como referenciar o período | `Q1 2026` · `jul/2026` · `FY-2025` |

---

## 3 · Sumário executivo (TL;DR)

> **Página mais importante.** Se o leitor só lê esta página, tem que sair
> sabendo a resposta + as evidências principais.

### LEDE_SUMARIO_EXECUTIVO

Parágrafo de 2-3 frases. Responde direto: **o quê descobrimos**.

> ✏ Token: `{{LEDE_SUMARIO_EXECUTIVO}}`

### 4 KPIs principais — sempre com referência explícita

> ⚠ **Regra dura**: nenhum KPI sem referência de comparação.
> "Captação R$ 142mi" não diz nada. "R$ 142mi (vs. meta R$ 100mi: +42%)" diz tudo.
>
> O primeiro cartão é destaque (lime), o quarto é em fundo escuro (resultado consolidado).

Para cada KPI N (1-4):

| Token | Descrição | Exemplo |
|---|---|---|
| `{{KPI_EXEC_N_LABEL}}` | Nome curto | `Captação líquida` |
| `{{KPI_EXEC_N_VALOR}}` | Número principal | `142,3` |
| `{{KPI_EXEC_N_UNIDADE}}` | Unidade (com espaço inicial) | ` R$ mi` |
| `{{KPI_EXEC_N_DELTA}}` | Variação percentual/absoluta | `+38%` · `+12 p.p.` · `-R$ 8 mi` |
| `{{KPI_EXEC_N_TIPO}}` | Classe CSS de cor do delta | `up` · `down` · `flat` |
| `{{KPI_EXEC_N_REFERENCIA}}` | **Contra o quê está comparando** | `Meta R$ 100 mi` · `Q4-25 (R$ 105 mi)` · `Benchmark XP (R$ 125 mi)` |

#### Tipos de referência aceitos

| Tipo | Quando usar | Exemplo de `{{KPI_EXEC_N_REFERENCIA}}` |
|---|---|---|
| **Meta** | Quando existe meta planejada | `Meta trimestral R$ 100 mi` |
| **Período anterior** | Continuidade temporal (MoM, QoQ, YoY) | `Q4-2025 (R$ 105 mi)` · `mar/2025 (R$ 87 mi)` |
| **Benchmark** | Comparação com player/mercado | `Benchmark setorial (R$ 125 mi)` |
| **Baseline pré-evento** | Antes/depois de algo concreto | `Pré-CRM (R$ 92 mi)` |

> 💡 Se um KPI não tem nenhuma das 4 referências possíveis acima,
> ele provavelmente não merece estar no TL;DR. Move para o scorecard.

### Findings que mudam decisão

> Quantos forem necessários (tipicamente 2-4). Cada finding responde "**e daí?**":
> conclusão + texto + **impacto na decisão** + evidência cruzada.

Para cada F_N (1, 2, 3, ...):

| Token | Descrição | Exemplo |
|---|---|---|
| `{{F_N_ID}}` | Identificador curto | `F-01` |
| `{{F_N_TITULO}}` | Frase de UMA linha (a conclusão) | `Concentração de canal subiu 6,2 p.p. no trimestre` |
| `{{F_N_CONFIANCA}}` | Nível de confiança (classe) | `alta` · `media` · `baixa` |
| `{{F_N_TEXTO}}` | Parágrafo de 2-3 frases | `Mesa Própria + Assessoria...` |
| `{{F_N_IMPACTO}}` | O **e daí?** — o que muda na decisão | `Limita capacidade de crescer com mesmo time. Se a tendência continuar, precisaremos investir em canais alternativos no Q3.` |
| `{{F_N_EVIDENCIA}}` | Onde achar a evidência | `ver §3.2, p.7` |

> No template atual, os 3 primeiros cards já estão no HTML. Para adicionar
> mais, **duplique o `<div class="insight">...</div>`** dentro da página
> de TL;DR. Mas atenção: o TL;DR cabe em 1 página — se passar de 3-4
> findings, considere mover os secundários pro capítulo 7 (Insights narrados).

---

## 4 · Scorecard de KPIs

> Tabela detalhada de KPIs com aderência a meta. **Não duplique** os 4 do TL;DR.
> 8-10 é o tamanho confortável. 12 é o teto.

### LEDE_SCORECARD

1-2 frases sobre o que o scorecard mostra como um todo.

> ✏ Token: `{{LEDE_SCORECARD}}`

### Linhas da tabela

Para cada KPI N (1-12):

| Token | Descrição |
|---|---|
| `{{KPI_N_NOME}}` | Nome do indicador |
| `{{KPI_N_VALOR}}` | Realizado no período |
| `{{KPI_N_META}}` | Meta planejada |
| `{{KPI_N_PCT}}` | % de aderência (ex.: `+18%`) |
| `{{KPI_N_DELTA}}` | Variação vs. base (ex.: `+12 p.p.`) |
| `{{KPI_N_STATUS}}` | Classe CSS: `ok` · `warn` · `bad` |
| `{{KPI_N_STATUS_LABEL}}` | Texto: `Acima` · `Dentro` · `Atenção` · `Crítico` |

> 🗑 Apague linhas de KPI que não usar — não preencha com vazios.

### 3 callouts resumo

| Token | Descrição |
|---|---|
| `{{SCORE_OK_RESUMO}}` / `{{SCORE_OK_TEXTO}}` | O que está acima da meta |
| `{{SCORE_WARN_RESUMO}}` / `{{SCORE_WARN_TEXTO}}` | O que está em atenção |
| `{{SCORE_BAD_RESUMO}}` / `{{SCORE_BAD_TEXTO}}` | O que está crítico |

---

## 5 · Contexto & metodologia

> Onde o leitor decide se confia na análise. **Não pule.**

| Token | Descrição |
|---|---|
| `{{LEDE_CONTEXTO}}` | Por que essa análise existe agora |
| `{{PERGUNTA_PESQUISA}}` | A mesma da capa, escrita por extenso |
| `{{PERIODO_PRINCIPAL}}` | Janela analisada (`jan/26 → mar/26`) |
| `{{PERIODO_COMPARATIVO}}` | Período de comparação (`Q4-2025`) |
| `{{DATA_SNAPSHOT}}` | Quando os dados foram extraídos |
| `{{PERIODO_OBS_OPCIONAL}}` | Observação livre sobre datas (ou apagar) |
| `{{COBERTURA_1..3}}` | O que está incluído |
| `{{COBERTURA_EXCLUSOES}}` | O que ficou de fora |
| `{{TRATAMENTO_1..4}}` | Transformações aplicadas aos dados |
| `{{LIMITACAO_1..4}}` | O que NÃO foi possível investigar |

### Tabela de fontes — quantas forem, ordenadas por relevância

> ⚠ **Sem limite de quantidade.** Ordene da fonte mais relevante para a análise
> para a menos relevante. Duplique linhas conforme necessário no HTML.

Para cada fonte N (1, 2, 3, ...):

| Token | Descrição | Exemplo |
|---|---|---|
| `{{FONTE_N_NOME}}` | Identificador técnico da tabela/view | `fact_captacao_v2` |
| `{{FONTE_N_DOMINIO}}` | Domínio de negócio | `Captação` |
| `{{FONTE_N_TIMELINESS}}` | Atraso vs. tempo real | `D-0` · `D+1` · `D+7` · `M+1` |
| `{{FONTE_N_CONTRIBUICAO}}` | **O que esta fonte agregou** à análise (seja específico) | `Série mensal §3.1, Pareto por canal §3.2, base do KPI captação líquida` |

#### Convenção de timeliness

| Código | Significado |
|---|---|
| `D-0` | Tempo real (sistema transacional) |
| `D+1` | Atualizado até 1 dia útil depois |
| `D+7` | Atualizado semanalmente |
| `M+1` | Atualizado mensalmente |
| `M+15` | Atualizado mensalmente, 15 dias após fechamento |

> 💡 A primeira linha deve ser a fonte que **dirige** a análise (sem ela
> o relatório não existe). As demais agregam contexto, controle, segmentação.

---

## 6 · Análises — onde a história é contada

> **Este é o capítulo mais extenso e dinâmico do relatório.** Não é
> burocracia, é narrativa. Trate como tal.

### Estrutura mental antes de qualquer placeholder

Cada análise responde **uma** pergunta. Antes de abrir o template, escreva:

```
Análise 3: A inflexão de Q1 é estrutural?
  → Sub 3.1: Como evoluiu a captação ao longo do tempo? → série temporal
  → Sub 3.2: Quem está liderando o crescimento? → pareto por canal
  → Sub 3.3: O ganho vem de tickets maiores ou mais clientes? → bridge
  → Conclusão: estrutural — 3 evidências independentes apontam pra cima

Análise 4: Onde estão os pontos de fragilidade?
  → Sub 4.1: ...
```

Só depois disso, mexa no HTML.

### Como o capítulo 6 funciona no template

- Cada **análise** = um `<article class="page">` no HTML
- Cada análise pode ter **N subseções** (`h3` + gráfico + observações)
- **Duplique** o `<article>` para cada nova análise
- A numeração da seção é manual (`03`, `04`, `05`...), começa em `03` (após `01` Sumário Executivo e `02` Contexto)
- A numeração da subseção é `N.M` (`3.1`, `3.2`, `4.1`, ...)

### Tokens por análise

> O template usa `{{A_*}}` no primeiro exemplo. Se você tiver 3 análises,
> renomeie para `{{A1_*}}`, `{{A2_*}}`, `{{A3_*}}` antes do find & replace.

| Token | Descrição |
|---|---|
| `{{A_TITULO_CURTO}}` | Label da página (vai no `data-page-label`) — 2-3 palavras |
| `{{A_NUM_SECAO}}` | Número da seção (`03`, `04`, ...) |
| `{{A_TITULO_SECAO}}` | Título completo (vira o `h2`) |
| `{{A_LEDE}}` | Parágrafo de abertura — pergunta + resposta em 2-3 frases |

### Tokens por subseção

| Token | Descrição |
|---|---|
| `{{A_SUBN_NUM}}` | Numeração `N.M` (ex.: `3.1`) |
| `{{A_SUBN_TITULO}}` | Título curto da subseção |
| `{{A_SUBN_LEDE}}` | Frase ligando a subseção à pergunta da análise |
| `{{A_SUBN_GRAFICO_TITULO}}` | Título do gráfico |
| `{{A_SUBN_GRAFICO_META}}` | Metadados (n, base, fonte) |
| `{{A_SUBN_GRAFICO_LEITURA}}` | Rodapé do gráfico com leitura-chave (uma frase) |
| `{{A_SUBN_OBSN}}` | Bullet de observação (3-5 por subseção) |

### Como inserir o gráfico (CRÍTICO)

O template tem um **placeholder visual** dentro de cada `<div class="chart-card">`:

```html
<svg ... style="background: var(--vc-50); border: 1px dashed var(--vc-200);">
  <text>Inserir gráfico do Design System aqui</text>
</svg>
```

**Para substituir:**

1. Abra `graficos.html` no DS
2. Identifique o tipo de gráfico que conta sua história
3. Copie o `<svg viewBox="0 0 ... ...">...</svg>` inteiro do exemplo do DS
4. Substitua o placeholder pelo SVG copiado
5. Ajuste valores, rótulos e cores conforme seus dados

#### Catálogo de gráficos do DS

> Os 12 tipos canônicos disponíveis em `graficos.html`. Cada um tem
> instruções detalhadas de uso, paleta correta e exemplos preenchidos.

| # | Tipo | Quando usar |
|---|---|---|
| 01 | **Resultado vs meta** | "Estamos no alvo?" — snapshot (várias métricas, 1 período) ou temporal (1 métrica, vários períodos) |
| 02 | **Pareto · 80/20** | Composição com ênfase em concentração — onde estão os "poucos vitais" |
| 03 | **Ranking · barras horizontais** | "Quem é maior?" — categorias ordenadas, top-down |
| 04 | **Radar · perfil multidimensional** | Perfilar 1 entidade em 4-8 dimensões, ou comparar 2-3 entidades |
| 05 | **Teia · rede de relações** | Dependências, co-investimento, exposição cruzada — quando a topologia é o ponto |
| 06 | **Dispersão · risco × retorno** | Correlação entre duas variáveis contínuas (≥20 pontos) |
| 07 | **Histograma · distribuição** | "Como esses valores se distribuem?" — sempre marcar média e mediana |
| 08 | **Treemap · composição hierárquica** | Parte-do-todo com muitas categorias hierárquicas (substitui pizza com >6 fatias) |
| 09 | **Linha temporal** | Evolução de 1-4 séries no tempo |
| 10 | **Waterfall · ponte** | Variação entre dois números via contribuições positivas/negativas |
| 11 | **Funil comercial** | Etapas sequenciais com perda — a forma da queda é o insight |
| 12 | **Árvore de decomposição** | "Por que esse número virou esse?" — drill-down hierárquico do total às causas |

#### Liberdade do analista — escolha o gráfico que conta a história

> A lista acima é um **mapa de referência**, não uma camisa de força.
> Você conhece os dados melhor que o template. Se uma análise pede um
> formato híbrido, uma vista diferente ou uma combinação dos canônicos
> — escolha o que **melhor responde a pergunta**. Princípios pra guiar:

- O gráfico existe para **responder a pergunta** da análise, não para "ilustrar"
- Se um tipo do DS resolve, use ele (consistência)
- Se nenhum resolve bem, **combine dois** (ex.: Pareto + ranking lateral) — mas justifique no rodapé
- Se você acha que precisa criar um gráfico inteiramente novo, vale **conversar antes**: o DS está sempre aberto a novos tipos canônicos, mas tem critérios (será reutilizado? cabe em A4? é editorialmente claro?)
- **Nunca** baixe Highcharts/Recharts/Chart.js — fica fora do estilo, gera dependência, quebra na exportação PDF

### Regras duras de cor

> **Cor não é decoração; é parte da mensagem.** Se você não consegue
> justificar por que usou aquela cor, troque por cinza neutro.

| Variável CSS | Quando usar |
|---|---|
| `--c1`, `--c2`, ..., `--c5` | Categorias qualitativas (canais, segmentos) |
| `--s1`, `--s2`, ..., `--s5` | Escala ordinal/sequencial (faixas etárias, tiers) |
| `--lime` | Destaque positivo · "olha aqui" |
| `--ng-red` | Destaque negativo · perda · vermelho |
| `--ok-green` | Confirmação positiva · meta atingida |
| `--warn-yellow` | Atenção · zona intermediária |
| `--vc-700` | Texto principal, valores destacados |
| `--vc-400` | Texto secundário, eixos, rótulos |
| `--vc-100` | Grids, bordas sutis |

#### Anti-padrões cromáticos

- ❌ Usar verde só porque "fica bonito" quando o número não confirma nada
- ❌ Cor diferente em cada barra de um bar chart simples (vira arco-íris)
- ❌ Gradient em barras categóricas (sugere ordem onde não tem)
- ❌ Usar `--lime` para a maioria dos elementos (perde o destaque)
- ❌ Vermelho para "atenção" e laranja para "crítico" — invertido vs. norma do DS

---

## 7 · Insights narrados — sem limite, sempre com impacto

> Versão expandida dos findings do TL;DR + outros que mereceram análise
> mas não couberam na capa. **Não há número máximo** — a análise é que decide.

### LEDE_INSIGHTS

Frase de abertura da seção. Se for usar mais de uma página de insights,
acrescente uma frase de transição no início da segunda.

> ✏ Token: `{{LEDE_INSIGHTS}}`

### NUM_SECAO_INSIGHTS

Número da seção (geralmente `07` ou `08`, depende de quantas análises você teve).

> ✏ Token: `{{NUM_SECAO_INSIGHTS}}`

### Findings F_1, F_2, F_3, ... (quantos forem)

Para cada N:

| Token | Descrição | Exemplo |
|---|---|---|
| `{{F_N_ID_FULL}}` | Mesmo ID do TL;DR | `F-01` |
| `{{F_N_TITULO_FULL}}` | Frase de uma linha (a conclusão) | `Concentração subiu 6,2 p.p.` |
| `{{F_N_CONFIANCA_FULL}}` | Classe CSS | `alta` · `media` · `baixa` |
| `{{F_N_CONFIANCA_LABEL}}` | Texto da tag | `Confiança alta` |
| `{{F_N_TEXTO_FULL}}` | Parágrafo completo (5-8 frases) | `Em Q1, Mesa Própria e Assessoria...` |
| `{{F_N_IMPACTO_FULL}}` | **O "e daí?"** — o que muda na decisão de negócio | `Se a tendência se mantiver no Q2, perdemos diversificação geográfica e ficamos expostos a saída do top-3 assessor. Recomendar teto de concentração na revisão do plano comercial.` |
| `{{F_N_EVIDENCIA_FULL}}` | Referência cruzada | `ver §3.2, p.7` |

> 💡 **O campo IMPACTO é não-negociável.** Insight sem impacto é
> observação curiosa, não finding. Se você não consegue escrever o
> impacto, o insight provavelmente não vale a página.

#### Como duplicar no HTML

- 3 cards já estão no template (`F_1`, `F_2`, `F_3`)
- Para adicionar mais: duplique `<div class="insight">...</div>` quantas vezes precisar
- Quando a página ficar cheia (~6 cards), duplique o `<article class="page">` inteiro
- Mantenha numeração contínua entre páginas (F-01, F-02, ..., F-09, F-10)

### Hipóteses abertas — pendentes de dados

> O que você levantou mas não pôde testar (dado ausente, amostra pequena).
> Serve de input pro próximo relatório.

Para cada H_N:

| Token | Descrição |
|---|---|
| `{{H_N_ID}}` | `H-01`, `H-02`, ... |
| `{{H_N_TEXTO}}` | A hipótese em si |
| `{{H_N_DADO}}` | Que dado falta pra confirmar |
| `{{H_N_TAG}}` | Classe: `warn` (indício) · `muted` (sem evidência) · `ok` (quase confirmada) |
| `{{H_N_LABEL}}` | Texto da tag |

> Sem limite de quantidade. Duplique linhas da tabela conforme necessário.

---

## 8 · Recomendações priorizadas

> O documento termina com **decisão**, não com dados. Cada recomendação
> tem dono, prazo e ICE score.

### LEDE_RECOS

Frase de abertura. Token: `{{LEDE_RECOS}}`

`{{NUM_SECAO_RECOS}}` — número da seção.

### Recomendações R_1, R_2, ... (quantas forem)

Para cada N:

| Token | Descrição | Exemplo |
|---|---|---|
| `{{R_N_NUM}}` | Número visível (`01`, `02`...) | `01` |
| `{{R_N_TITULO}}` | Frase imperativa de ação | `Limitar concentração de canal a 65%` |
| `{{R_N_DESCRICAO}}` | Por que + como | `Definir teto operacional de captação por canal...` |
| `{{R_N_REF}}` | Finding ou hipótese de origem | `Decorre de F-01.` |
| `{{R_N_DONO}}` | Nome ou cargo | `Diretor Comercial` |
| `{{R_N_PRAZO}}` | Data ou janela | `Q2-2026` |
| `{{R_N_IMPACTO}}` | Impacto esperado quantificado | `Reduz risco de concentração em 6 p.p.` |
| `{{R_N_CUSTO}}` | Esforço estimado | `Baixo · ajuste de política` |
| `{{R_N_PRIORIDADE}}` | Classe: `alta` · `media` · `baixa` | `alta` |
| `{{R_N_PRIORIDADE_LABEL}}` | Texto | `Prioridade alta` |
| `{{R_N_ICE}}` | (Impacto × Confiança) / Esforço, escala 1-10 | `8.5` |

> **Como calcular ICE:**
> - Impacto: 1 (marginal) → 10 (transformador)
> - Confiança: 1 (palpite) → 10 (evidência sólida)
> - Esforço: 1 (trivial) → 10 (gigante)
> - **ICE = (Impacto × Confiança) ÷ Esforço**
> - Priorize recomendações com ICE ≥ 6

---

## 9 · Anexos

> Fontes de dados detalhadas + dicionário de métricas + glossário.

| Token | Descrição |
|---|---|
| `{{ANEXO_FONTES_TEXTO}}` | Descrição das fontes técnicas |
| `{{DIC_N_METRICA}}` / `{{DIC_N_FORMULA}}` / `{{DIC_N_NOTA}}` | Cada entrada do dicionário (N = 1, 2, ...) |
| `{{GLOSSARIO_N_TERMO}}` / `{{GLOSSARIO_N_DEF}}` | Cada termo do glossário |

---

## Checklist final

Antes de aprovar para distribuição:

- [ ] Código segue o padrão `ANL-{ÁREA}-{NNN}`
- [ ] Capa responde claramente à pergunta de pesquisa
- [ ] Sumário executivo cabe em 1 página (sem rolar)
- [ ] **Todo KPI do TL;DR tem `{{KPI_EXEC_N_REFERENCIA}}` preenchido** — sem exceções
- [ ] Os 4 KPIs do TL;DR **não duplicam** os 4 primeiros do scorecard
- [ ] Cada análise responde **uma pergunta** clara
- [ ] Cada gráfico veio do **DS** (`graficos.html`) — nada inventado
- [ ] Cores usam **apenas** variáveis do DS (`--c*/--s*/--lime/--ng-red/--vc-*`)
- [ ] Tabela de fontes tem **timeliness** e **contribuição** preenchidos
- [ ] Cada finding tem `{{F_N_IMPACTO}}` — não-negociável
- [ ] Toda recomendação tem **dono** e **prazo** preenchidos
- [ ] Cada finding cita evidência (`ver §X.Y, p.NN`)
- [ ] Dicionário cobre **todas** as métricas mencionadas
- [ ] Limitações estão explícitas (e não escondidas)
- [ ] Aprovador assinou — `{{NOME_APROVADOR}}` não está vazio
- [ ] Versão e data estão coerentes em capa, controle e cabeçalhos
- [ ] PDF foi exportado com Chrome/Edge (Safari quebra fontes ocasionalmente)

---

## Anti-padrões — o que **não** fazer

- ❌ **KPI sem referência.** Número solto é desinformação. Sempre vs. meta/anterior/benchmark.
- ❌ **Inventar precisão.** Se a fonte tem D+1 de atraso, não publique "captação de hoje". Diga a data do snapshot.
- ❌ **Esconder limitações.** Se a amostra é pequena, diga. Confiança baixa não é vergonha; é honestidade.
- ❌ **Encher de KPIs.** Scorecard de 15 indicadores ninguém lê. 8-10 boa, 12 já é muito.
- ❌ **Gráfico sem pergunta.** Cada chart deve responder uma pergunta específica do leitor. Se não responde, corta.
- ❌ **Gráfico fora do DS.** Não use Excel default, não baixe biblioteca, não invente visualização.
- ❌ **Cor decorativa.** Cor é mensagem. Se não justifica, neutro.
- ❌ **Recomendação sem dono.** "A área deveria..." não é recomendação, é desejo.
- ❌ **Concluir o que os dados não suportam.** Se confiança é média, escreva "indício de" — não "comprovamos".
- ❌ **Finding sem impacto.** Sem o "e daí?", é trivia, não insight.

---

*Última revisão deste briefing: 2026. Mudanças no template HTML devem
ser refletidas aqui — e vice-versa. Em caso de divergência, o template manda.*
