# N1 · Cadeia de Valor — regras detalhadas

Documento de apoio à [SKILL.md](../SKILL.md). Cobre tudo que é específico do nível N1 (Cadeia de Valor): variantes, layout, regras de preenchimento, placeholders e checklist de validação.

## Sumário

1. [Modelo conceitual (Porter)](#1-modelo-conceitual-porter)
2. [Variantes A · Master e B · Linear](#2-variantes-a--master-e-b--linear)
3. [Variante A — layout dos primários](#3-variante-a--layout-dos-primários)
4. [Variante B — layout linear](#4-variante-b--layout-linear)
5. [Regras de preenchimento](#5-regras-de-preenchimento)
6. [Lista completa de placeholders](#6-lista-completa-de-placeholders)
7. [Anti-padrões](#7-anti-padrões)
8. [Checklist de validação](#8-checklist-de-validação)

---

## 1. Modelo conceitual (Porter)

A cadeia tem **exatamente 3 camadas** (não negociável):

| Camada | Prefixo | Conteúdo típico |
|---|---|---|
| **Gerenciais** | `G1..Gn` | Estratégia, performance, compliance, orçamento — frequência fixa |
| **Primários** | `P1..Pn` | Ponta da operação, geram receita direta |
| **Apoio** | `A1..An` | Tecnologia, jurídico, financeiro, pessoas, backoffice |

**Não** crie uma 4ª camada. Se o usuário propor (ex.: "Comercial" como camada própria), redirecione: comercial é Primário, não camada nova.

**Não** traduza os rótulos. `Gerenciais / Primários / Apoio` são canônicos. Não use "Estratégicos / Operacionais / Suporte" ou variantes.

---

## 2. Variantes A · Master e B · Linear

| Variante | Use quando… | Arquivo |
|---|---|---|
| **A · Master** | Operação clara em 3 blocos: front-end (geração/qualificação) → núcleo produtivo (verticais ou linhas de produto) → back-end (relacionamento/pós). Padrão M7. | `template-cadeia-de-valor.html` |
| **B · Linear** | Sem padrão front/núcleo/back. Primários fluem em uma linha só, da esquerda (entrada) para a direita (cliente). Recomendado 4–7 processos. | `template-cadeia-de-valor--linear.html` |

**Default → A.** Mude para B se:
- < 4 processos primários, ou
- Nenhum agrupamento de verticais faz sentido, ou
- O fluxo é claramente sequencial (processo de manufatura, pipeline de produção)

---

## 3. Variante A — layout dos primários

```
┌─────────────┐     ┌──────────────────────┐     ┌─────────────┐
│ FRONT-END   │     │   NÚCLEO PRODUTIVO   │     │ BACK-END    │
│  (1 ou 2    │ ──▶ │   (3 a 6 verticais   │ ──▶ │  (1 ou 2    │
│  processos) │     │    em grade 3-col)   │     │  processos) │
└─────────────┘     └──────────────────────┘     └─────────────┘
```

- **Front-end**: 1 ou 2 processos empilhados verticalmente (ex.: `P1 Geração de Demanda`, `P2 Prospecção & Qualificação`).
- **Núcleo**: 3 a 6 processos em grade 3-col com rótulo `{{ROTULO_NUCLEO}}` (ex.: "Verticais de Produto", "Linhas de Negócio", "Produtos").
- **Back-end**: 1 ou 2 processos empilhados (ex.: `P9 Relacionamento & Retenção`).

**Limite duro**: 6 verticais no núcleo. Mais que isso, agrupe (ex.: junte `Seguros + Consórcios → Seg/Cons`) ou mude para variante B.

**SVG dos arrows** já está no template (`<div class="flow-arrow">`) — não substituir.

---

## 4. Variante B — layout linear

Todos os primários ficam num único `.lane-content` em linha. Lê-se da esquerda (entrada) para a direita (saída/cliente).

Recomendado para 4–7 processos. Se mais de 7, considere:
- Agrupar processos em macroprocessos
- Quebrar em duas cadeias (ex.: por BU)

Ainda assim respeita as 3 camadas (Gerenciais em cima, Apoio embaixo). Só os Primários mudam de layout.

---

## 5. Regras de preenchimento

### Códigos
- Sempre `G1, G2…`, `P1, P2…`, `A1, A2…`. Numere na ordem em que o usuário listou; não reordene.
- Sem buracos. Se um processo é removido, renumere os seguintes.

### Nome do processo (`.name`)
- **Máximo 3 palavras**. Use `&` em vez de "e" para manter compacto: `Compliance & Risco`, `Tecnologia & Dados`.
- Sempre em português, capitalize cada palavra principal.
- Sem pontuação final.

### Tooltip
- 2 a 4 linhas separadas por `<br>`.
- Estilo telegráfico (sem pontuação final, sem "etc.").
- Para **processos gerenciais**, a última linha **deve** ser `Freq: …` (Anual / Mensal / Semanal / Contínua).
- Para **primários**, a última linha geralmente é uma métrica/meta ou observação relevante.
- Para **apoio**, 2 linhas geralmente bastam.

### Foco estratégico (`.highlight`)
- Aplica `class="process-box highlight"` — fundo lime suave + borda lime.
- **Máximo 2 processos** marcados na cadeia inteira. Se o usuário marcar mais, peça para priorizar.
- Reserve para processos que recebem investimento desproporcional ou OKRs prioritários.

### Cross-sell / Tech (`.blue-accent`)
- Aplica `class="process-box blue-accent"` — fundo azul suave + borda azul.
- **Máximo 1 processo** na cadeia inteira. Normalmente na camada de Apoio (Tecnologia & Dados é o caso clássico).
- Reserve para o processo que **integra** outros (CRM, plataforma única, dados).

### Tag `FOCO`
- `<div class="focus-tag">FOCO</div>` é uma tag flutuante extra. Use **só** se a cor `.highlight` não bastar — em geral **não use**, é redundante.

---

## 6. Lista completa de placeholders

### Header (variante A e B)
| Placeholder | Conteúdo | Exemplo |
|---|---|---|
| `{{NOME_DA_EMPRESA}}` | Nome legal/comercial | "M7 Investimentos" |
| `{{AREA_DOCUMENTO}}` | Área owner do diagrama | "Estratégia" |
| `{{DATA_REFERENCIA}}` | Mês/ano | "Fev / 2026" |
| `{{LEDE_DOCUMENTO}}` | Lede de 1-2 linhas (subtítulo) | "Visão consolidada dos 18 processos macro da holding…" |
| `{{TOTAL_PROCESSOS}}` | Soma de G + P + A | `18` |
| `{{N_VERTICAIS}}` | Quantos verticais no núcleo (variante A) ou primários (B) | `6` |
| `{{VERSAO_CURTA}}` | Versão compacta | `02/26` |

### Lane labels
| Placeholder | Conteúdo |
|---|---|
| `{{N_GERENCIAIS}}` | Número de gerenciais (ex.: `4`) |
| `{{N_PRIMARIOS}}` | Número de primários (ex.: `9`) |
| `{{N_APOIO}}` | Número de apoio (ex.: `5`) |

### Variante A · primários (núcleo)
| Placeholder | Conteúdo |
|---|---|
| `{{ROTULO_NUCLEO}}` | Rótulo do bloco do núcleo | "Verticais de Produto", "Linhas de Negócio", "Produtos" |

### Processos (variante A)
Para cada processo Gx/Px/Ax:
- `{{NOME_PROCESSO_<código>}}` → ex.: `{{NOME_PROCESSO_G1}}`
- `{{LINHA_1_<código>}}`, `{{LINHA_2_<código>}}`, `{{LINHA_3_<código>}}` → conteúdo do tooltip
- Para gerenciais: `{{FREQUENCIA_<código>}}` → "Anual + revisões semestrais", "Mensal", etc.

### Processos (variante B — formato simplificado)
- `{{NOME_<código>}}` → ex.: `{{NOME_G1}}`
- `{{TOOLTIP_<código>}}` → tooltip completo (já com `<br>` se multi-linha)

### Footer
Não tem placeholders dinâmicos no footer (texto fixo) — só atualize `{{NOME_DA_EMPRESA}}` e `{{DATA_REFERENCIA}}` que aparecem ali.

---

## 7. Anti-padrões

- ❌ **Criar uma 4ª camada** — sempre 3 (Gerenciais, Primários, Apoio).
- ❌ **Inverter ordem das camadas** — Gerenciais sempre em cima, Apoio embaixo.
- ❌ **Texto longo no `.name`** — vai quebrar o layout. Resuma em ≤3 palavras.
- ❌ **Trocar fonte ou palette** — TWK Everett + verde-caqui + lime + off-white. Sempre.
- ❌ **Adicionar gráficos, charts, KPIs grandes** — isto é cadeia de valor, não dashboard. Detalhes vão para tooltips.
- ❌ **Traduzir os rótulos canônicos** — Gerenciais / Primários / Apoio. Não use "Estratégicos / Operacionais / Suporte".
- ❌ **Mais de 6 verticais no núcleo (variante A)** — agrupe ou mude para B.
- ❌ **Mais de 2 `.highlight` ou mais de 1 `.blue-accent`** — perde força semântica.
- ❌ **Usar `.focus-tag` junto de `.highlight`** — escolha um dos dois (geralmente `.highlight` basta).
- ❌ **Reordenar processos depois de numerados** — mantenha a ordem da entrevista.

---

## 8. Checklist de validação

Antes de entregar, confirmar:

- [ ] **Placeholders zerados** — busque `{{` no arquivo, deve voltar 0 matches.
- [ ] **Códigos seguem ordem** — `G1..Gn → P1..Pn → A1..An`, sem buracos.
- [ ] **Limites de variantes** — máx. 2 `.highlight`, máx. 1 `.blue-accent`.
- [ ] **Tooltips de gerenciais** — última linha começa com `Freq:`.
- [ ] **Header strip** — mostra contagem real (não `{{TOTAL_PROCESSOS}}` ou `{{N_VERTICAIS}}`).
- [ ] **Header metadata** — `{{AREA_DOCUMENTO}}`, `{{LEDE_DOCUMENTO}}`, `{{VERSAO_CURTA}}` preenchidos.
- [ ] **CSS irmãos do HTML** — `m7-tokens.css`, `m7-header-dark.css` no mesmo diretório.
- [ ] **Logo carrega** — `assets/m7-logo-offwhite.png` no diretório (ou logo da empresa-alvo).
- [ ] **Hover funciona** — passar o mouse num `.process-box` mostra tooltip.
- [ ] **Tabs do header** — se N2 ou N3 também foram gerados, links funcionam (`href="missao-do-processo-{slug}.html"` e `href="mapa-de-interdependencia-{slug}.html"`); se não foram gerados, deixe os `<a>` tabs como `<div class="tab">` (sem href) para não quebrar.
- [ ] **Sem `style="..."` inline novos** — todo styling via classes do template.
- [ ] **Variante escolhida está coerente** — se < 4 primários ou sem agrupamento, deveria ser B.
