# N4 · Documento Oficial / Política — regras detalhadas

Documento de apoio à [SKILL.md](../SKILL.md). Cobre o nível N4: documento HTML A4-paginado **standalone** que apresenta a cadeia de valor como **política formal** assinável. Renderiza no navegador como 8 páginas A4 empilhadas com sombra; exporta como PDF via `window.print()` (Salvar como PDF no diálogo nativo).

> **Atualização (2026-05)**: a arquitetura mudou de **server-rendered Playwright/Jinja** (legacy) para **client-side window.print()**. Veja [§7 · Migração e legacy](#7--migração-e-legacy) ao fim do documento.

## Sumário

1. [Objetivo e quando usar](#1-objetivo-e-quando-usar)
2. [Estrutura de páginas](#2-estrutura-de-páginas)
3. [Arquitetura técnica](#3-arquitetura-técnica)
4. [Mapeamento BRIEFING → placeholders](#4-mapeamento-briefing--placeholders)
5. [Checklist de validação](#5-checklist-de-validação)
6. [Anti-padrões](#6-anti-padrões)
7. [Migração e legacy](#7-migração-e-legacy)

---

## 1. Objetivo e quando usar

O N4 é o **documento oficial e assinável** que consolida o mapeamento da cadeia de valor (N1 + N2 + N3) em uma política formal: capa institucional, controle de versões, aprovações, objetivo/escopo/definições, diagrama da cadeia, processos descritos por camada, amostra SIPOC e governança.

Use quando o usuário pedir:
- "Documento oficial / institucional"
- "Política de processos"
- "PDF da cadeia para arquivo / assinatura / diretoria"
- "Apresentar formalmente à governança"
- "Versão executiva paginada"

**Pré-condições**:
- N1, N2 e N3 prontos (regra `PDF-DEPENDENCIA` em [`critique-rules.md`](critique-rules.md))
- Seção `politica:` do BRIEFING preenchida (regra `POLITICA-AUSENTE`)
- Campo `meta:` preenchido em cada vertical primária (aviso `POLITICA-META-PRIM`)

---

## 2. Estrutura de páginas

Sequência fixa de **8 páginas A4 retrato** (sem landscape no MVP — todas portrait):

```
P1     CAPA (fullbleed verde-caqui no topo, branca no resto)
P2     CONTROLE DE VERSÕES + APROVAÇÕES + SUMÁRIO
P3     OBJETIVO · ESCOPO · DEFINIÇÕES
P4     ESTRUTURA DA CADEIA (diagrama mini + princípios)
P5     PROCESSOS GERENCIAIS (G1–Gn)
P6     PROCESSOS PRIMÁRIOS (P1–Pn, com meta nos verticais)
P7     PROCESSOS DE APOIO (A1–An, SLA inter-camadas)
P8     SIPOC sample (2 processos) + INTERDEPENDÊNCIAS + GOVERNANÇA/EXCEÇÕES
```

### P1 · Capa

- **Top band verde-caqui** (`var(--vc-700)`, ~24mm de altura) com:
  - Logo offwhite (`assets/m7-logo-offwhite.png`, 22px) à esquerda
  - Metadata uppercase: `{AREA_DOCUMENTO}` · `Política · N1` · `{DATA_REFERENCIA}` à direita
  - **Cover-tabs** abaixo (4 abas, "Política DOC" ativa em lime) — apenas visual, não navegável no PDF
- **Cover-body em branco** com:
  - Eyebrow `Documento de governança · {CODIGO_DOCUMENTO}`
  - Título 56pt weight 200 — `Política de processos & cadeia de valor` (com "de processos" em lime accent)
  - Subtítulo 16pt weight 300 — `{LEDE_DOCUMENTO}`
  - Grid 4-cell (Versão · Vigência · Próxima revisão · Responsável)
- **Cover-foot**: classificação "Uso interno · Confidencial" + identificação (`{NOME_DA_EMPRESA} · {CODIGO_DOCUMENTO} · {VERSAO_COMPLETA}`)

### P2 · Controle · Aprovações · Sumário

- **Seção 00 · Controle de versões** — tabela de 5 colunas (Versão · Data · Alterações · Responsável · Status), até 3 linhas (vigente + 2 obsoletas). Status: tag lime "vigente" ou tag cinza "obsoleto"
- **Seção 00 · Aprovações** — 3 cards lado a lado (Elaborador · Revisor · Aprovador), cada um com role label + nome + cargo + linha de assinatura + data
- **Seção 00 · Sumário** — 10 entradas com hierarquia (4 root + 6 sub), numeração mono e indicação de página

### P3 · Objetivo · Escopo · Definições

- **01 Objetivo** — parágrafo `{TEXTO_OBJETIVO}` + parágrafo padrão com 3 ênfases (`linguagem comum`, `arquitetura de processos`, `regras de governança`)
- **02 Escopo e aplicação** — 3 colunas (Aplica-se a / Não se aplica a / Documentos relacionados)
- **03 Definições e termos** — dl com 5 termos canônicos: Cadeia de valor N1, Processo macro Nível 1, Missão do processo SIPOC, Mapa de interdependência N3, Owner do processo RACI

### P4 · Estrutura da cadeia + Princípios

- **04 Estrutura da cadeia de valor** — versão miniatura do N1 (3 layers Porter: Gerenciais · Primários · Apoio). Mesmo padrão do diagrama mas em escala reduzida para caber em 1 página A4
  - Primários renderizam com layout especial: `col-fb` (P1+P2) → flow arrow → `cverticais` (P3-P8 grid) → flow arrow → `col-fb` (P9)
  - Highlight (lime-faint) e blue-accent disponíveis (P3, P5 highlight; A1 blue)
- **Princípios estruturantes** — 4 cards (P1: 1 dono por processo · P2: missão antes de atividade · P3: verticais como núcleo · P4: interdependência explícita)

### P5 · Processos Gerenciais

- **05 Processos gerenciais** — lede explicando camada de direcionamento
- **Lista** de cards (1 por gerencial), cada um com:
  - Código mono grande
  - Nome + missão (verbo + objeto + finalidade concatenados)
  - Owner + Frequência à direita
- **Regras gerais da camada** — bullet list de 3 itens (decisões em rituais formais, metas só de gerencial, exceções regulatórias)

### P6 · Processos Primários

- **06 Processos primários** — lede explicando núcleo produtivo
- **Lista** de cards (1 por primário), cada um com:
  - Código + nome + missão
  - Para verticais (subcamada=nucleo): Owner + **Meta**
  - Para front (P1, P2) e back (P9): Owner + Camada (`Front-end` / `Back-end`)
- Highlight (lime) em P3, P5 (configurável via BRIEFING.processos[].highlight)

### P7 · Processos de Apoio

- **07 Processos de apoio** — lede explicando camada de habilitação
- **Lista** de cards (1 por apoio), cada um com:
  - Código + nome + missão
  - Owner + **Tipo** (`Habilitador` / `Risco` / `Capital` / `Pessoas` / `Operação`)
- Blue-accent em A1 (Tecnologia & Dados, configurável)
- **SLA inter-camadas** — bloco com referência cruzada a `{DOC_SLA}` e cadência de report mensal a G2

### P8 · SIPOC + Interdependências + Governança

- **08 Missão dos processos · SIPOC** — amostra de 2 processos featurados (de `politica.sipoc_amostra`):
  - Cada bloco: header (código + nome + owner) + row 3 colunas (Inputs / Missão lime-faint / Outputs)
- **09 Mapa de interdependências · N3** — lista compacta de relações principais (formato `from → [targets]`)
  - Lime em targets críticos (foco estratégico)
- **10 Governança, revisão e exceções** — 2 colunas (Cadência de revisão / Exceções)
  - Inclui referência a `{COMITE_REVISOR}`, `{AREA_COMPLIANCE}`, próxima revisão `{DATA_PROXIMA_REVISAO}`

### Footer (em todas as páginas exceto capa)

- `pf-classif` à esquerda: "Uso interno · Confidencial" + ponto lime
- `pf-page` à direita: `Página X de 8` mono

---

## 3. Arquitetura técnica

### Single-file standalone HTML

O `template-politica.html` é **autocontido**: 1874 linhas com CSS embutido em `<style>` + shell-header fixo + sidebar de sumário 280px + área de doc rolável. Sem Jinja includes, sem dependências externas além de:
- `m7-tokens.css` (fontes + paleta)
- `m7-header-dark.css` (não usado neste template, mantido para consistência da skill)
- `assets/m7-logo-offwhite.png`, `assets/m7-logo-dark.png`

### Toolbar interativo (apenas em tela)

Floating no canto superior direito:

```html
<div class="toolbar">
  <button id="prev-page">◀</button>
  <div class="counter">Página <strong id="cur-page">1</strong> / <span id="total-pages">8</span></div>
  <button id="next-page">▶</button>
  <div class="sep"></div>
  <button class="export" id="export-pdf">Exportar PDF</button>
</div>
```

JavaScript (inline, vanilla, ~50 linhas):
- **IntersectionObserver** atualiza contador conforme usuário scrolla
- Botões `◀ ▶` fazem `scrollIntoView({behavior: 'smooth'})`
- Teclas `↑/↓/PgUp/PgDn` também navegam
- Botão `Exportar PDF` chama `window.print()`
- `@media print { .toolbar { display: none !important; } }` esconde no PDF

### Paginação CSS

```css
@page { size: A4; margin: 0; }

@media print {
  body { background: var(--white) !important; padding: 0 !important;
         -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .toolbar { display: none !important; }
  .doc { width: var(--page-w); margin: 0; gap: 0; }
  .page { width: var(--page-w); height: var(--page-h);
          box-shadow: none !important; margin: 0 !important;
          break-after: page; page-break-after: always; }
  .page:last-child { break-after: auto; page-break-after: auto; }
}
```

Cada `<article class="page">` tem `width: 210mm; height: 297mm; page-break-after: always`. Em tela aparecem com sombra; em print viram páginas A4 reais.

### Como o usuário exporta o PDF

1. Abre `politica-{slug}.html` no Chrome/Safari/Firefox
2. Clica em "Exportar PDF" no toolbar (ou `Cmd+P`)
3. Diálogo nativo do navegador abre
4. **CRÍTICO**: marca "Plano de fundo gráfico" (Chrome) / "Imprimir cabeçalhos e rodapés" desmarcado / "Salvar como PDF" no destino
5. Salva — gera PDF de 8 páginas com cores preservadas

**Por que esta abordagem**:
- ✓ Zero infra (sem Playwright, sem WeasyPrint, sem dependência Python)
- ✓ Usuário controla onde salva e como nomeia
- ✓ Funciona offline em qualquer navegador moderno
- ✓ Texto selecionável, vetorial, < 500KB típico
- ✓ Aberto no navegador: navegável, exportável, compartilhável como link

**Limitações aceitas**:
- ✗ Exige ação do usuário (1 clique + 1 confirmação no diálogo)
- ✗ Cross-browser: Safari pode renderizar cores ligeiramente diferentes
- ✗ Footer dinâmico via `@page @bottom-center` foi removido — número da página fica hardcoded no `.pf-page strong`

---

## 4. Mapeamento BRIEFING → placeholders

A geração do N4 substitui ~120 placeholders. Mapeamento (não exaustivo):

### Cabeçalho / metadata da política

| Placeholder | Fonte no BRIEFING |
|---|---|
| `{{NOME_DA_EMPRESA}}` | `empresa.nome` |
| `{{AREA_DOCUMENTO}}` | `area_documento` |
| `{{DATA_REFERENCIA}}` | `data_referencia` |
| `{{LEDE_DOCUMENTO}}` | seção markdown `## Lede do documento` |
| `{{CODIGO_DOCUMENTO}}` | `politica.metadata.codigo_documento` |
| `{{DATA_VIGENCIA}}` | `politica.metadata.data_vigencia` |
| `{{DATA_PROXIMA_REVISAO}}` | `politica.metadata.proxima_revisao` |
| `{{AREA_RESPONSAVEL}}` | `politica.metadata.area_responsavel` |
| `{{VERSAO_COMPLETA}}` | derivado de `politica.versoes[0]` (vigente): ex. `v1.0 · 02/2026` |

### Controle de versões (3 linhas)

| Placeholder | Fonte |
|---|---|
| `{{ALTERACOES_VERSAO_ATUAL}}` | `politica.versoes[vigente].alteracoes` |
| `{{VERSAO_ANTERIOR_1}}`, `{{DATA_VERSAO_ANTERIOR_1}}`, etc. | `politica.versoes[obsoleto-1]` |
| `{{VERSAO_ANTERIOR_2}}`, etc. | `politica.versoes[obsoleto-2]` |

Se o usuário só tem 1 versão (vigente), as linhas 2 e 3 mostram placeholders — a skill deve renderizar como `—` ou esconder via CSS condicional.

### Aprovações

| Placeholder | Fonte |
|---|---|
| `{{NOME_ELABORADOR}}`, `{{CARGO_ELABORADOR}}`, `{{DATA_ELABORACAO}}` | `politica.aprovacoes.elaborador.*` |
| `{{NOME_REVISOR}}`, `{{CARGO_REVISOR}}`, `{{DATA_REVISAO}}` | `politica.aprovacoes.revisor.*` |
| `{{NOME_APROVADOR}}`, `{{CARGO_APROVADOR}}`, `{{DATA_APROVACAO}}` | `politica.aprovacoes.aprovador.*` |

### Objetivo, escopo, definições

| Placeholder | Fonte |
|---|---|
| `{{TEXTO_OBJETIVO}}` | `politica.objetivo_texto` |
| `{{ESCOPO_INCLUSAO_1/2/3}}` | `politica.escopo.inclusoes[0..2]` |
| `{{ESCOPO_EXCLUSAO_1/2}}` | `politica.escopo.exclusoes[0..1]` |
| `{{DOC_RELACIONADO_1/2/3}}` | `politica.escopo.doc_relacionados[0..2]` |

### Processos (G1–G4, P1–P9, A1–A5)

| Placeholder | Fonte |
|---|---|
| `{{NOME_PROCESSO_X}}` | `processos[codigo=X].nome` |
| `{{MISSAO_X}}` | concatena `processos[X].sipoc.{verbo} {objeto} {finalidade}` |
| `{{OWNER_X}}` | `processos[X].sipoc.owner` |
| `{{FREQUENCIA_G1..G4}}` | `processos[gerencial].frequencia` |
| `{{META_P3..P8}}` | `processos[vertical].meta` |
| `{{N_GERENCIAIS}}`, `{{N_PRIMARIOS}}`, `{{N_APOIO}}`, `{{TOTAL_PROCESSOS}}` | `n1.contagens.*`, `n1.total_processos` |
| `{{ROTULO_NUCLEO}}` | `n1.rotulo_nucleo` |

### SIPOC amostra (2 processos)

| Placeholder | Fonte |
|---|---|
| `{{CODIGO_PROCESSO_SIPOC_A}}` | `politica.sipoc_amostra[0]` |
| `{{NOME_PROCESSO_SIPOC_A}}` | `processos[politica.sipoc_amostra[0]].nome` |
| `{{OWNER_SIPOC_A}}` | `processos[...].sipoc.owner` |
| `{{INPUT_A_1/2/3}}` | `processos[...].sipoc.inputs[0..2]` |
| `{{OUTPUT_A_1/2/3}}` | `processos[...].sipoc.outputs[0..2]` |
| `{{MISSAO_SIPOC_A}}` | concatena verbo+objeto+finalidade |
| `{{...SIPOC_B}}` | idem usando `politica.sipoc_amostra[1]` |

### Governança

| Placeholder | Fonte |
|---|---|
| `{{COMITE_REVISOR}}` | `politica.governanca.comite_revisor` |
| `{{DOC_SLA}}` | `politica.governanca.doc_sla` |
| `{{AREA_COMPLIANCE}}` | `politica.governanca.area_compliance` |

---

## 5. Checklist de validação

### Pré-geração (Fase B → C)

- [ ] BRIEFING tem `n4-pdf` em `artefatos_a_gerar`
- [ ] BRIEFING tem `n1`, `n2`, `n3` também (regra `PDF-DEPENDENCIA`)
- [ ] N1, N2, N3 HTML já gerados no diretório de trabalho (sequência rígida)
- [ ] `check_briefing.py` retorna 0 bloqueadores para o BRIEFING
- [ ] Seção `politica:` 100% preenchida (sem `{{placeholders}}` em campos da política)

### HTML do N4 gerado

- [ ] Nenhum `{{placeholder}}` remanescente (grep `{{` no arquivo)
- [ ] CSS embutido valida (sem regras quebradas — abrir no navegador, verificar console)
- [ ] Logos carregam (`m7-logo-offwhite.png` na capa, `m7-logo-dark.png` no header das páginas internas)
- [ ] Toolbar aparece e responde a teclado/clique
- [ ] Cada `<article class="page">` tem dimensões corretas (210mm × 297mm) — verificar no Inspector

### PDF exportado (após window.print())

- [ ] **8 páginas** (não 7, não 9)
- [ ] Capa fullbleed verde-caqui no topo, sem barra branca acima
- [ ] Logo offwhite na capa (não dark)
- [ ] Cores preservadas (lime accent visível, fundo verde-caqui no top band) → confirma que "Plano de fundo gráfico" estava marcado
- [ ] Sumário aparece em P2, tabela de versões renderiza com tags de status
- [ ] Diagrama da cadeia (P4) cabe em 1 página sem quebra
- [ ] Cards de processos (P5, P6, P7) não quebram entre páginas (`page-break-inside: avoid` implícito)
- [ ] SIPOC sample (P8) tem 2 blocos visíveis
- [ ] Footer com `Página X de 8` correto
- [ ] Texto selecionável (não rasterizado)
- [ ] Toolbar **NÃO** aparece no PDF
- [ ] Tamanho ≤ 1MB (sem imagens vetorializadas pesadas)

### Validação via `pdf-validator` (subagent)

O subagent abre o PDF gerado e roda checklist visual:
- [ ] Capa renderiza no padrão
- [ ] Hierarquia tipográfica preserva (h2.section > h3.sub > body)
- [ ] Tabelas e grids alinhados
- [ ] Princípios em P4 não quebram cards entre páginas
- [ ] Footer está no rodapé absoluto de cada página

---

## 6. Anti-padrões

- ❌ **Gerar N4 sem `politica:` no BRIEFING** — bloqueado em `POLITICA-AUSENTE`. Execute Bloco 6 da Fase A antes.
- ❌ **Tentar imprimir sem marcar "Plano de fundo gráfico"** — perde verde-caqui da capa, lime accents, header bands. Resultado fica branco demais.
- ❌ **Editar o HTML à mão depois de gerado** — alterações ficam no template ou no script de substituição. Output é descartável.
- ❌ **Adicionar mais de 3 versões em `politica.versoes`** — template suporta exatamente 3 linhas. Excedentes truncados.
- ❌ **Mesmo nome como Elaborador E Aprovador** — conflito de papéis. Política assinada por si mesma não tem valor de auditoria.
- ❌ **Featurar SIPOC sem `sipoc.verbo` preenchido** — bloqueado em `POLITICA-AMOSTRA-SEM-SIPOC`.
- ❌ **Tentar usar Jinja `{% include %}` ou Playwright** — abordagem antiga (ver §7). Template novo é standalone HTML.
- ❌ **Skip do toolbar para "limpar" o HTML** — toolbar é o ponto de export. Sem ele o usuário não sabe como gerar PDF.
- ❌ **Mexer no JavaScript do contador de páginas** — IntersectionObserver é o único método que funciona bem em todos navegadores. Não substituir por scroll handlers.
- ❌ **Adicionar páginas além das 8** — estrutura fechada. Conteúdo extra entra em apêndice (futuro) ou em documento separado.

---

## 7. Migração e legacy

### O que mudou (2026-05)

**Antes** (arquitetura legacy, deprecada):
- `template-politica.html` usava Jinja2 `{% include 'fragments/...' %}`
- `scripts/build_n4.py` orquestrava: lia N1.html, N2.html, N3.html, extraía fragmentos via BeautifulSoup, montava o template final
- `scripts/render_pdf.py` renderizava via Playwright (chromium headless) com fallback WeasyPrint
- Output: PDF direto (.pdf), sem HTML intermediário visível ao usuário

**Agora** (arquitetura atual):
- `template-politica.html` é standalone — 1660 linhas inline, sem includes
- Conteúdo é replicado: a estrutura miniatura do N1 vive dentro do próprio template, igual para SIPOC, mapa, etc.
- Geração: a skill substitui ~120 placeholders por strings no BRIEFING (sem parsing de outros HTMLs)
- Export PDF: client-side, via `window.print()`, pelo navegador do usuário

### Por que mudou

1. **Simplicidade** — eliminou Playwright/WeasyPrint (instalação Python + chromium, ~300MB). Skill funciona em qualquer máquina com navegador.
2. **Controle do usuário** — abrir o HTML no navegador permite revisar antes de exportar, compartilhar como link, tweakar pequenos detalhes inline se necessário.
3. **Consistência visual** — `window.print()` usa o mesmo engine de renderização que o usuário vê em tela. Zero divergência tela↔PDF.
4. **Robustez cross-platform** — Playwright headless tinha glitches em macOS Sonoma+ (fontes faltando em CI, timeouts intermitentes). Browser do usuário "é o" ambiente.

### Trade-offs aceitos

- Perda de geração 100% automatizada (usuário precisa clicar "Exportar PDF" no navegador)
- Perda de landscape — todo o documento agora é portrait. Tabelas largas usam scroll horizontal em tela; no PDF caem em mais linhas
- Perda da etapa de "embed inteligente" — antes o N4 reaproveitava o N1.html já gerado; agora a estrutura mini é replicada

### Scripts legacy

`scripts/render_pdf.py` e `scripts/build_n4.py` foram **mantidos** com banner `# DEPRECATED` no topo, para 2 casos:

1. Usuário quiser PDF de N1/N2/N3 individuais (sem ser via Política)
2. Caso surja necessidade futura de geração server-side automatizada (CI, batch)

Não invocar esses scripts no fluxo padrão da skill. Veja [`pdf-generation.md`](pdf-generation.md) para detalhes históricos.
