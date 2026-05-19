# Schema · `ssot/data-lake.md`

SSOT para `build/data-lake.html` + parte `window.P5_DATALAKE` de `build/journey-{slug}-{cod}.js` (Data Lake: systems/data por subproc + marts/consumers globais).

## Sumário

1. [Frontmatter YAML](#1-frontmatter-yaml)
2. [Estrutura: 2 rows por subproc + marts + consumers globais](#2-estrutura)
3. [Exemplo mínimo](#3-exemplo-mínimo)
4. [Regras de validação](#4-regras-de-validação)
5. [Enum de `kind`](#5-enum-de-kind)

---

## 1. Frontmatter YAML

```yaml
---
schema_version: 1

processo_ref: <string>               # ex: "P5"
slug:         <string>               # ex: "p5-credito"

processos:                           # N entradas (mesma de jornada-cx.md/processo-n2.md)
  - code:    <string>
    name:    <string>
    owner:   <string>
    cadence: <string>
    tone:    <a|b|c|d|e>

rows:                                # exatamente 2 entradas (systems + data)
  - id: systems                      # row 1
    label:    "Sistemas / fontes"
    sublabel: "backstage · ferramentas"
    cells:                           # array de N arrays-de-string (1 array por subproc)
      - [<string>, <string>, ...]    # nomes de sistemas
      # ...

  - id: data                         # row 2
    label:    "Dado armazenado"
    sublabel: "persistência · marts"
    cells:                           # array de N arrays-de-objetos
      - - name:  <string>
          where: <string>
          kind:  <enum>              # ver seção 5
      # ...

# GLOBAIS por processo (NÃO por subproc.)
marts:
  dim:                               # >= 3 entradas
    - name:   <string>               # ex: "dim_lead_credito"
      source: <string>               # 1 frase

  fact:                              # >= 3 entradas
    - name:        <string>          # ex: "fact_score"
      description: <string>          # 1 frase

consumers:                           # >= 4 tiers
  - tier:        <string>            # ex: "BI", "Operação", "Risco"
    description: <string>
---
```

---

## 2. Estrutura

```
                  P5.1            P5.2            P5.3            ...
                Originação      Análise         Formalização
              ────────────────────────────────────────────────────────
Systems     | [Site, Bitrix, |[Serasa, SCR,  |[Modelos,       | ...
            |  RD, RecWS, ..]| Modelo Score..]|GED, DocuSign..]|
Data        | [lead_origem,  |[docs_financ,  |[contratos,     | ...
            |  cliente_pf,   | score_M7,     | garantias,     |
            |  score_bureau] | restritivos]  | registros]     |

═══ Marts globais ═══
dim[]: dim_lead_credito, dim_cliente, dim_oferta, dim_operacao, dim_garantia
fact[]: fact_score, fact_desembolso, fact_inadimplencia, fact_provisao

═══ Consumers globais ═══
BI · Operação · Risco · Regulatório · Tesouraria · Auditoria
```

Marts e consumers são **únicos por processo** (não por subproc.) porque representam a camada agregada do data lake — vivem em ClickHouse e atendem todos os subprocs.

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
  - id: systems
    label: "Sistemas / fontes"
    sublabel: "backstage · ferramentas"
    cells:
      - ["Site M7", "Bitrix24 CRM", "RD Station", "Boa Vista", "Quod"]
      - ["Serasa Experian", "SCR Bacen", "Modelo Score M7", "DocuSign"]

  - id: data
    label: "Dado armazenado"
    sublabel: "persistência · marts"
    cells:
      - - { name: "lead_origem", where: "Bitrix · dim_lead", kind: "CRM" }
        - { name: "cliente_pf/pj", where: "Bitrix · dim_cliente", kind: "PII" }
        - { name: "score_bureau", where: "dim_lead_credito", kind: "Score" }
      - - { name: "docs_financ", where: "GED · S3", kind: "Doc" }
        - { name: "score_M7", where: "fact_score", kind: "Score" }

marts:
  dim:
    - name: "dim_lead_credito"
      source: "Bitrix CRM + bureau"
    - name: "dim_cliente"
      source: "Onboarding + KYC"
    - name: "dim_oferta"
      source: "Score + política"

  fact:
    - name: "fact_score"
      description: "Score M7 calculado por lead/oferta"
    - name: "fact_operacao_credito"
      description: "Desembolso, taxa, prazo, garantia"
    - name: "fact_inadimplencia"
      description: "NPL por faixa 15/30/60/90+"

consumers:
  - tier: "BI"
    description: "Dashboards de captação, NPL, DRE Crédito"
  - tier: "Operação"
    description: "Mesa de Crédito + Servicing"
  - tier: "Risco"
    description: "Comitê + estresse + provisão"
  - tier: "Regulatório"
    description: "Reportes CVM, Bacen, ANBIMA"
---
```

---

## 4. Regras de validação

### Determinísticas (bloqueadores)
- **SCHEMA-MISSING** — campo raiz ausente
- **ROWS-COUNT** — `rows.length != 2`
- **ROWS-ID-INVALIDO** — row id fora de {systems, data}
- **CELLS-COUNT** — `rows[].cells.length != processos.length`
- **SYSTEMS-VAZIO** — algum `systems.cells[i]` é array vazio
- **DATA-VAZIO** — algum `data.cells[i]` é array vazio
- **DATA-INCOMPLETO** — alguma entrada de data sem name/where/kind
- **KIND-INVALIDO** — `kind` fora do enum (ver seção 5)
- **MARTS-DIM-FAIXA** — `marts.dim.length < 3`
- **MARTS-FACT-FAIXA** — `marts.fact.length < 3`
- **CONSUMERS-FAIXA** — `consumers.length < 4`
- **MART-DIM-NOME-INVALIDO** — não começa com `dim_` (convenção ClickHouse)
- **MART-FACT-NOME-INVALIDO** — não começa com `fact_`
- **CONSUMER-TIER-DUP** — tier repetido em consumers[]

### Determinísticas (avisos)
- **SYSTEM-NOME-LONGO** — nome de sistema > 30 chars (não cabe no pill)
- **DATA-WHERE-AUSENTE** — entrada de data com `where` curto demais (< 8 chars)

### Cross-checks (com processo-n2.md, em `--all`)
- **DATALAKE-PROCESSOS-MISMATCH** — `processos[].code` ≠ subprocessos[].code de `processo-n2.md`
- **DATALAKE-ORDEM-MISMATCH** — ordem difere

### Semânticas (delegadas ao critic)
- Marts cobrem todos os outputs[] de `sipocs.md` (output "dim_lead_credito" do P5.1 deveria existir em `marts.dim`)
- Consumers fazem sentido (BI sem nenhum dashboard concreto descrito é suspeito)

---

## 5. Enum de `kind`

Valores aceitos para `data.cells[i][j].kind`:

| kind | Quando usar |
|---|---|
| **CRM** | Dado vindo do Bitrix24/CRM — leads, contas, atividades |
| **PII** | Dado pessoal/sensível — CPF, contato, dados bancários |
| **Score** | Score interno ou externo — bureau, modelo M7 |
| **Bureau** | Restritivos, histórico de crédito, SCR |
| **Doc** | Documento — PDF de IR, comprovante, GED |
| **Contrato** | CCB, aditivo, fiança, minuta assinada |
| **Lastro** | Registro Núclea/CETIP/cartório de garantia |
| **Tesouraria** | Caixa, fluxo, cotas FIDC |
| **Cobrança** | Régua, ações, acordos, renegociações |
| **KPI** | Indicador agregado para BI/diretoria |

Se o dado não cabe em nenhum, abra discussão antes de inventar novo kind — preferível agrupar em um existente do que diluir o enum.
