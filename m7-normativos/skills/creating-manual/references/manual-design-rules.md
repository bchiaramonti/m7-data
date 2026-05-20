# Regras de Design — Manual M7 (9 dimensões)

> Documento canônico que o agente `manual-design-reviewer` usa como gabarito
> para comparar cada HTML gerado. Específico para o artefato **Manual (MAN)**
> — herda o design system M7-2026 mas adiciona 3 dimensões próprias
> (paginação A4 de 11 páginas + estrutura de 10 seções + conformidade
> BPMN/SIPOC/RACI/KPI).

## Conformidade base — M7-2026

Todo manual gerado deve respeitar **integralmente** os tokens declarados em
`assets/m7-tokens.css`:

| Token | Valor canônico |
|-------|----------------|
| Fonte | TWK Everett (200/300/400/500/700) |
| Primária | `var(--verde-caqui)` = `#424135` |
| Accent | `var(--lime)` = `#eef77c` (decorativo, nunca texto) |
| Surface | `var(--off-white)` = `#fffdef` (quente, nunca `#FAF9F6`) |
| Escala VC | `--vc-50` a `--vc-900` |
| Escala OW | `--ow-50` a `--ow-900` |

**Regra dura**: o HTML gerado pelo script **não pode conter hex literal**
para essas cores. Toda referência a `#424135`, `#fffdef`, `#eef77c` ou tons
da escala deve aparecer como `var(--vc-500)`, `var(--off-white)`, etc.
Hex literal só é tolerado em status (Success/Warning/Error/Info quando
necessário) e nas 4 cores semânticas RACI (R/A/C/I) que vivem no template.

---

## 9 dimensões de revisão

### Dimensão 1 — Paleta de cores

**Verifica:**
- Todas as cores principais via `var(--*)`. Zero hex literal para verde caqui,
  lime, off-white ou tons da escala.
- Off-white **quente** (`#fffdef`). Nunca `#FAF9F6`, `#FFFFFF`, `#FAFAFA`.
- Accent (lime) **nunca em texto** — só borda, fundo translúcido, badge decorativo.
- Status neon (`#00ff00`, `#ffff00`) **nunca em texto** — usa variantes `-text`.

**Contraste mínimo (WCAG AA):**

| Elemento | Razão mínima |
|----------|--------------|
| Texto normal (< 18px) | 4.5:1 |
| Texto grande (≥ 18px) | 3:1 |
| Componentes UI | 3:1 |
| Células RACI coloridas | 3:1 (texto sobre fundo da cor R/A/C/I) |

**Falhas conhecidas a flaggar como CRITICO:**
- `#eef77c` em `#fffdef` = 1.1:1 — sempre falha.
- Texto branco sobre célula `.raci-a` lime escuro sem contraste suficiente.
- Hex literal de `#424135` em CSS injetado pelo MD.

### Dimensão 2 — Tipografia

**Verifica:**
- Font-family em headings e body: `var(--font-sans)` (= `"twkEverett", ...`).
- Headings (h1–h4): `font-weight: 400` (Regular). **Nunca** Bold/700.
- Bold reservado para BANs, métricas, valores em destaque.
- Eyebrow/label: `weight: 500`, `letter-spacing: 0.08em`, `text-transform: uppercase`.
- Line-height ≥ 1.5 em body text.
- `@font-face` TWK Everett presente (HTML autocontido → base64).
- Hierarquia visual: h1 > h2 > h3 > h4 > body. Nunca um heading menor que body.

**Falhas a flaggar como CRITICO:**
- Heading com `font-weight: 700` ou `bold`.
- Eyebrow sem letter-spacing 0.08em.
- Mistura de famílias (Arial mixed com TWK Everett sem fallback declarado).

### Dimensão 3 — Espaçamento

**Grid 8px** (ou subdivisões reconhecidas):

```
4px → 6px → 8px → 10px → 12px → 14px → 16px → 24px → 32px → 48px → 64px → 96px
```

(Manual aceita 6/10/14 como subdivisões intermediárias para imprimir em
formato A4. Cells de tabelas RACI e SIPOC usam padding `6px 8px` por
restrição de espaço horizontal.)

**Verifica:**
- Padding interno ≤ gap externo (cards não "explodem" o container).
- Espaçamento entre seções coerente (não 8px aqui, 20px ali, 13px lá).
- Margin em cards seguindo escala (não valores aleatórios como `7px`, `11px`).
- Gap entre lanes BPMN consistente (típico: 24px vertical, 48px horizontal).

**Falhas a flaggar:**
- Valores fora da escala (`margin: 7px`, `padding: 11px 13px`).
- `padding: 0` em containers visíveis.

### Dimensão 4 — Proporções

**Verifica:**
- SVG **obrigatoriamente** com `viewBox`. Width/height absolutos sem viewBox = falha.
- Página A4: aspect ratio `1:1.4142` (210mm × 297mm).
- Cards seguindo proporções harmônicas.
- Containers com `max-width` declarado.

**Específico de manual:**
- 11 páginas A4 fixas (Capa, Controle+Sumário, Objetivo+Escopo, Definições,
  Visão Geral, BPMN, Regras, Papéis, Indicadores, Cronograma+Qualidade,
  Docs+Versões+Aprovações).
- Cada `.page` tem altura útil `~960px` para conteúdo.
- BPMN canvas usa viewBox aspect `1.85:1` (típico 1400×760).

### Dimensão 5 — Layout & componentes

**Verifica:**
- Toda classe CSS no HTML pertence à allowlist do `component-catalog-manual.md`.
- Sem `<style>` injetado fora do bloco principal do template.
- Sem `style="..."` inline.
- Componentes oficiais do template intactos: `.page`, `.page-head`, `.page-foot`,
  `.cover`, `.section`, `.bpmn-*`, `.raci-*`, `.kpi-card`, `.dto-list`, etc.
- Shortcodes do catálogo gerando o HTML correto.

**Falhas a flaggar como CRITICO:**
- `<style>` adicional injetado pelo autor.
- Classes ad-hoc tipo `.man-*`, `.proc-*`, `.user-*`.
- `style="color: ..."` em qualquer elemento.

### Dimensão 6 — Acessibilidade

**Verifica:**
- Contraste WCAG AA em todo texto (ver Dimensão 1).
- Lime/neon nunca em texto.
- `<img>` tem `alt`.
- Status nunca só por cor — sempre ícone ou label textual.
- Font size em body ≥ 9px (mínimo absoluto para impressão A4).
- **Células RACI** contém **letra textual** (R/A/C/I) além da cor — quem
  imprimir em P&B ainda consegue ler.
- BPMN tasks têm rótulo textual visível (não só ícone).

### Dimensão 7 — Paginação A4 (específico de manual)

**Verifica:**
- HTML contém exatamente as **11 páginas** oficiais do template (ordem
  invariante):
  1. Capa
  2. Controle & sumário
  3. Objetivo & Escopo
  4. Definições
  5. Visão geral do processo (Missão + SIPOC + Interfaces)
  6. Fluxograma BPMN
  7. Regras de negócio
  8. Papéis & responsabilidades (RACI)
  9. Indicadores (KPI + PPI)
  10. Cronograma & qualidade
  11. Docs relacionados, versões & aprovações
- Cada `.page` tem `data-page-label` correto.
- Cada `.page` tem `<header class="page-head">` + `<div class="page-body">`
  + `<footer class="page-foot">`.
- `page-break-inside: avoid` em cards e tabelas curtas.
- Auto-numeração via JS (`{{TOTAL_PAGINAS}}` substituído + `.total-pg`
  atualizado).

**Falhas a flaggar como CRITICO:**
- Página faltando ou em ordem trocada.
- `.page-body` com altura excedendo ~960px (texto cortado por
  `overflow: hidden`).

### Dimensão 8 — Estrutura das 10 seções (específico de manual)

**Verifica:**
- h2 numerados de 01 a 10 (formato com prefixo `<span class="num">01</span>`)
  na ordem canônica.
- Cada seção com conteúdo mínimo:

| Seção | Conteúdo mínimo |
|-------|-----------------|
| 01. Objetivo | Pelo menos 1 parágrafo (ideal 2) |
| 02. Escopo e aplicabilidade | LEDE + ao menos 1 inclusão |
| 03. Definições e glossário | Ao menos 3 linhas na tabela |
| 04. Visão geral do processo | Missão + SIPOC completo (≥3 S, ≥3 I, ≥3 P, ≥3 O, ≥3 C) + Interfaces |
| 04.4. Fluxograma BPMN | ≥1 evt início, ≥3 tasks, ≥1 evt fim, narrativa textual |
| 05. Regras de negócio | ≥1 tema + ≥3 regras numeradas |
| 06. Papéis & responsabilidades | RACI 5×5 preenchido (5 papéis × 5 atividades) |
| 07. Indicadores | ≥1 KPI completo (Nome+Fórmula+Meta+Freq+Fonte) + ≥1 PPI |
| 08. Cronograma | ≥1 cadência preenchida (Diário/Semanal/Mensal/Trimestral/Semestral) |
| 09. Critérios de qualidade | ≥3 critérios DTO |
| 10. Docs relacionados | ≥1 doc subordinado (INS, ESP ou MAN sibling) |

- Slot limits respeitados (10 defs, 6 regras, 5 papéis RACI, 2 KPIs, 2 PPIs,
  4 docs relacionados, 5 DTOs).
- Slots vazios removidos pelo cleanup (zero `<tr>` com células vazias).

**Falhas a flaggar como CRITICO:**
- Seção faltando (h2 ausente).
- BPMN sem narrativa textual (só diagrama é insuficiente).
- RACI com 0 papéis ou 0 atividades.
- Sem indicador algum (KPI nem PPI).

### Dimensão 9 — Conformidade procedural (BPMN / SIPOC / RACI / KPI/PPI) — manual-específica

**Verifica BPMN:**
- SVG do canvas tem `viewBox` definido.
- Evento de início único (círculo verde claro, 1 ocorrência).
- Eventos de fim com `.bpmn-event-end` (1-2 ocorrências). Múltiplos fins
  sinalizam saídas alternativas (ex.: aprovado vs rejeitado).
- Tasks (`.bpmn-task`) com `bpmn-task-label` preenchido (nunca placeholder
  `{{BPMN_TASK_N}}` residual).
- Gateways (`.bpmn-gateway` losango) com `.bpmn-gateway-mark` (`+` ou `X`).
- Setas (`<line>` ou `<path>` com `marker-end="url(#bpmn-arrow)"`) conectam
  todos os elementos (zero órfão).
- Narrativa textual em até 3 parágrafos (`BPMN_NARRATIVA_1..3`) descreve o
  fluxo em prosa.
- Caption (`bpmn-caption`) explicita "Fig X · Nome do fluxo".

**Verifica SIPOC:**
- 5 colunas (S/I/P/O/C) preenchidas.
- Pelo menos 3 itens em cada bloco de fronteira (S, I, O, C) e 4 no Process.
- Não há item duplicado intra-bloco.
- Process steps em ordem cronológica (1→2→3→4).

**Verifica RACI:**
- Matriz 5×5 — 5 papéis nos headers de coluna, 5 atividades nas linhas.
- Cada linha tem exatamente 1 `A` (Accountable é único).
- Cada linha tem pelo menos 1 `R` (Responsible).
- Células contém **letra textual** + cor (não só cor) — acessibilidade P&B.
- Legenda (`.raci-legend`) presente explicando R/A/C/I.
- Cores semânticas:
  - R: `.raci-r` (verde caqui suave)
  - A: `.raci-a` (lime escuro translúcido)
  - C: `.raci-c` (amarelo claro)
  - I: `.raci-i` (cinza neutro)

**Verifica KPI/PPI:**
- 2 KPIs (resultado) + 2 PPIs (processo) — simetria intencional.
- Cada indicador com 5 campos preenchidos: Nome, Fórmula, Meta, Frequência,
  Fonte de dados.
- KPI mede **resultado** (saída do processo); PPI mede **processo**
  (atividades intermediárias). Confusão entre os dois é ATENCAO.
- Meta deve ser **numérica** (ex.: `≥ 95%`, `≤ 5 dias`), não qualitativa
  (`alta`, `boa`).
- Fórmula deve ser **executável** (ex.: `(Aprovados / Total) × 100`), não
  qualitativa.

**Verifica Cronograma:**
- 5 cadências (Diário, Semanal, Mensal, Trimestral, Semestral) — cada uma
  com ritual + output. Vazias são aceitáveis (autor pode declarar "—") mas
  pelo menos uma deve estar preenchida.
- Outputs concretos (ex.: "Ata", "Dashboard", "Relatório"), não verbos
  vagos ("acompanhar", "monitorar").

**Verifica Critérios de Qualidade (DTO):**
- 3-5 critérios `DTO_01..05`.
- Cada critério é **mensurável** ("Indicador X dentro da meta") não
  qualitativo ("Processo está bem").

**Falhas a flaggar como CRITICO:**
- BPMN sem evt início ou fim.
- RACI com 0 A em uma linha (sem accountability) ou 2+ A na mesma linha.
- KPI/PPI sem fórmula ou com meta qualitativa.
- Placeholder `{{BPMN_TASK_N}}` ou `{{RACI_PAPEL_N}}` residual no HTML
  final.

---

## Score e veredito

| Score | Critério | Veredito |
|-------|----------|----------|
| **A** | Zero CRITICO, ≤ 2 ATENCAO | APROVADO |
| **B** | Zero CRITICO, 3-5 ATENCAO | APROVADO COM RESSALVAS |
| **C** | 1+ CRITICO ou 6+ ATENCAO | REPROVADO |
| **D** | Violação grave (off-brand, página faltando, BPMN/RACI quebrado) | REPROVADO |

**Gate da Fase 3**: a skill só entrega o trio (.html + .yaml + .review.md)
se Score ∈ {A, B}. Score C/D bloqueia e exige correção no MD/BRIEFING +
re-execução do script.

---

## Comparação com gold reference

O agente sempre compara o HTML em revisão contra o gold reference em
`references/reference-output/MAN-PERF-003-gold.html`. Verifica especialmente:

1. **Header/footer**: estrutura idêntica (logo, separador, código, classificação).
2. **Capa**: composição do título (linha 1 + acento + sufixo) seguindo o
   padrão visual.
3. **Tipografia**: hierarquia h1/h2/h3/h4 com mesmos tamanhos relativos.
4. **Espaçamento entre seções**: ritmo consistente.
5. **BPMN canvas**: lanes, swimlanes, proporções de tasks/gateways/eventos.
6. **SIPOC table**: 5 colunas com headers coloridos consistentes.
7. **RACI matrix**: 5×5 com cores semânticas corretas.
8. **KPI/PPI cards**: layout 2-col simétrico.
9. **Cronograma**: 5 linhas (cadências) × 2 colunas (ritual, output).

Divergências significativas (não causadas por conteúdo diferente) viram
ATENCAO ou CRITICO conforme severidade.
