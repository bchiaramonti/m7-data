# Schema · `ssot/jornada-cx.md`

SSOT para `build/jornada-cx.html` + parte `window.P5_JOURNEY` de `build/journey-{slug}-{cod}.js` (Customer Journey lado-cliente).

## Sumário

1. [Frontmatter YAML](#1-frontmatter-yaml)
2. [Estrutura do grid 4×N](#2-estrutura-do-grid-4n)
3. [Exemplo mínimo](#3-exemplo-mínimo)
4. [Regras de validação](#4-regras-de-validação)
5. [Convenções de tom emocional](#5-convenções-de-tom-emocional)

---

## 1. Frontmatter YAML

```yaml
---
schema_version: 1

processo_ref: <string>               # ex: "P5"
slug:         <string>               # ex: "p5-credito"

processos:                           # N entradas (mesma quantidade e ordem de processo-n2.md)
  - code:    <string>                # ex: P5.1
    name:    <string>                # ex: "Originação"
    owner:   <string>                # cargo/comitê
    cadence: <string>                # ex: "D+0 contínuo"
    tone:    <a|b|c|d|e>             # cor da coluna (ciclico, 5 tons)

rows:                                # exatamente 4 entradas, nesta ordem
  - id: touchpoint                   # row 1
    label:    "Canal / Touchpoint"
    sublabel: "onde o cliente está"
    cells:                           # array de N strings (1 por subprocesso)
      - <string>
      - <string>
      # ...

  - id: action                       # row 2
    label:    "Ação do cliente"
    sublabel: "frontstage"
    cells:                           # array de N strings
      - <string>
      # ...

  - id: mot                          # row 3
    label:    "Momentos da Verdade"
    sublabel: "inflexão emocional"
    cells:                           # array de N objetos
      - intensity: <1|2|3>           # 1=baixa, 3=alta
        items:                       # 1-3 strings
          - <string>
      # ...

  - id: pain                         # row 4
    label:    "Pain points · sentimento"
    sublabel: "tom: − negativo · ~ neutro · + positivo"
    cells:                           # array de N objetos
      - tone: <+|-|~>
        items:                       # 1-3 strings, formato "cliente fala"
          - "\"...\""                # entre aspas escapadas
      # ...
---
```

---

## 2. Estrutura do grid 4×N

```
                P5.1          P5.2          P5.3          P5.4          P5.5
              Originação    Análise       Formalização  Desembolso    Monitor.
            ──────────────────────────────────────────────────────────────────
Touchpoint  | Site, WApp |  WApp, Tel  |  E-mail jur |  Conta banco|  WApp, ...
Action      | Procura sol|  Sobe docs  |  Lê minuta  |  Confere $$  |  Paga ...
MoT         | int=3 [...]|  int=3 [...]|  int=2 [...]|  int=3 [...]|  int=3 ...
Pain        | tone=- ['x']| tone=- [..] |  tone=~ [..]| tone=+ [..] |  tone=- ..
```

Os 4 IDs são **fixos** (touchpoint, action, mot, pain). Não inventar `id: emotion` ou `id: goal`.

---

## 3. Exemplo mínimo

```yaml
---
schema_version: 1

processo_ref: "P5"
slug: "p5-credito"

processos:
  - code: "P5.1"
    name: "Originação"
    owner: "Comercial · Mesa Crédito"
    cadence: "D+0 contínuo"
    tone: "a"
  - code: "P5.2"
    name: "Análise"
    owner: "Analista · Risco"
    cadence: "SLA 3-5d"
    tone: "b"

rows:
  - id: touchpoint
    label: "Canal / Touchpoint"
    sublabel: "onde o cliente está"
    cells:
      - "Site M7 · Indicação · WhatsApp"
      - "WhatsApp · Telefone · Reunião"

  - id: action
    label: "Ação do cliente"
    sublabel: "frontstage"
    cells:
      - "Procura solução de capital e envia documentos básicos"
      - "Sobe documentos financeiros, recebe parecer"

  - id: mot
    label: "Momentos da Verdade"
    sublabel: "inflexão emocional"
    cells:
      - intensity: 3
        items:
          - "Primeira impressão de confiança"
          - "Velocidade do retorno inicial"
      - intensity: 3
        items:
          - "Recebe parecer (aprovado / negado)"

  - id: pain
    label: "Pain points · sentimento"
    sublabel: "tom: − negativo · ~ neutro · + positivo"
    cells:
      - tone: "-"
        items:
          - "\"Cadastro demorado, querem dados demais\""
      - tone: "-"
        items:
          - "\"Já mandei tudo, por que demora tanto?\""
---
```

---

## 4. Regras de validação

### Determinísticas (bloqueadores)
- **SCHEMA-MISSING** — campo raiz ausente
- **ROWS-COUNT** — `rows.length != 4`
- **ROWS-ID-INVALIDO** — row id fora de {touchpoint, action, mot, pain}
- **ROWS-ID-DUP** — rows[].id repetidos
- **PROCESSOS-VAZIO** — `processos.length < 1`
- **CELLS-COUNT** — `rows[].cells.length != processos.length` (em algum row)
- **MOT-INTENSITY-INVALIDA** — fora de {1, 2, 3}
- **MOT-ITEMS-VAZIO** — items vazio em algum mot.cells[]
- **PAIN-TONE-INVALIDO** — fora de {+, -, ~}
- **PAIN-ITEMS-VAZIO** — items vazio em algum pain.cells[]
- **TONE-INVALIDO** — `processos[].tone` fora de {a, b, c, d, e}

### Determinísticas (avisos)
- **TOUCHPOINT-LONGO** — touchpoint.cells[i] > 100 chars (não cabe)
- **ACTION-LONGO** — action.cells[i] > 120 chars
- **MOT-ITEM-LONGO** — algum item > 80 chars
- **PAIN-ITEM-SEM-ASPAS** — pain.cells[i].items[j] não começa com `"` (recomenda formato fala-do-cliente)

### Cross-checks (com processo-n2.md, em `--all`)
- **JORNADA-PROCESSOS-MISMATCH** — set de `processos[].code` aqui ≠ set em `processo-n2.md.subprocessos[].code`
- **JORNADA-ORDEM-MISMATCH** — ordem difere

### Semânticas (delegadas ao critic)
- MoT realmente é momento de verdade (inflexão emocional) ou só ação repetida?
- Pain points refletem fala real ou interpretação corporativa?
- Há gradiente narrativo na intensidade (não pode ser tudo 3)?

---

## 5. Convenções de tom emocional

### `mot.intensity`
- **1** — momento operacional, baixa carga emocional ("preenche formulário")
- **2** — momento de transição, atenção do cliente requerida ("clica em assinar")
- **3** — momento de verdade clássico, ponto de decisão/satisfação ("dinheiro caiu na conta")

Não use 3 em todos os subprocessos — perde sinal. Distribuição típica: 1-2 momentos `intensity=3`, resto 1-2.

### `pain.tone`
- **`-`** (negativo) — cliente frustrado, ansioso, irritado ("isso é demorado / ninguém me responde")
- **`~`** (neutro) — cliente confuso ou cauteloso ("não entendo direito o que estou assinando")
- **`+`** (positivo) — cliente satisfeito, aliviado ("caiu o dinheiro! funcionou")

Pain `+` é raro mas importante — geralmente em desembolso/entrega. Não force pain `+` em subprocesso operacional árido.

### `pain.items` formato fala-do-cliente
Sempre entre aspas escapadas: `"\"Já mandei tudo, por que demora tanto?\""`. O renderer mostra com tipografia diferenciada (italic). Frases corporativas tipo "Cliente expressa insatisfação com latência" perdem o valor de pesquisa.
