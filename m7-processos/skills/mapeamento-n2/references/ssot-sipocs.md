# Schema · `ssot/sipocs.md`

SSOT para `build/sipoc-deip.html` + `build/dados-{slug}-{cod}.js` (SIPOC/DEIP por subprocesso).

## Sumário

1. [Frontmatter YAML](#1-frontmatter-yaml)
2. [Estrutura SIPOC/DEIP](#2-estrutura-sipocdeip)
3. [Exemplo mínimo](#3-exemplo-mínimo)
4. [Regras de validação](#4-regras-de-validação)
5. [Anti-padrões SIPOC](#5-anti-padrões-sipoc)

---

## 1. Frontmatter YAML

```yaml
---
schema_version: 1

processo_ref: <string>               # ex: "P5". Deve casar com processo.code de ssot/processo-n2.md
slug:         <string>               # ex: "p5-credito". Deve casar com processo.slug

subprocessos:                        # 1 entrada por subprocesso (mesma quantidade de processo-n2.md)
  - id:        <string>              # kebab. Ex: p5-1
    code:      <string>              # ex: P5.1
    name:      <string>              # ex: "Originação & Pré-análise"
    purpose:   <string>              # verbo + objeto + finalidade. SEM "fazer/realizar/gerenciar"
    cadence:   <string>              # ex: "D+0 online · contínuo"
    owner:     <string>              # cargo/comitê
    sistemas:  <string>              # CSV
    volume:    <string>              # ex: "~ 1.200 leads / mês"
    inputs:                          # 3-5 entradas
      - what:   <string>             # nome curto do insumo
        from:   <string>             # fornecedor (subproc, ator externo, política)
        detail: <string>             # 1 frase explicando
    outputs:                         # 3-5 entradas. what NÃO pode duplicar inputs[].what
      - what:   <string>
        to:     <string>             # consumidor (subproc, ator externo, BI)
        detail: <string>
    etapas:                          # 4-8 entradas. Cada: string com verbo no infinitivo
      - <string>
    regulacao:                       # 2-4 entradas
      - code:   <string>             # R1, R2, R3, R4
        label:  <string>             # ex: "LGPD"
        detail: <string>             # ex: "Consentimento + minimização"
    suporte:                         # 2-4 entradas
      - code:   <string>             # S1, S2, S3
        label:  <string>             # ex: "TI / CRM"
        detail: <string>
---
```

---

## 2. Estrutura SIPOC/DEIP

A estrutura espelha **1:1** o `P5_DATA.subprocessos[N]` do gabarito JS (`dados-P5-credito.js`).

Visualmente, cada subprocesso renderiza em um DEIP com:
- **Cabeçalho**: code + name + purpose + owner + cadence
- **Banda superior** (Regulação): R1..R4 com label + detail
- **Central**:
  - Esquerda (Entradas): inputs[] como iorows com fornecedor → I-N → insumo
  - Centro: macrofluxo (code/name) + etapas numeradas 1..N
  - Direita (Saídas): outputs[] como iorows com produto → O-N → cliente
- **Banda inferior** (Suporte): S1..S3 com label + detail
- **Foot**: cadence, owner, sistemas, volume

A sidebar lista todos os subprocessos com code, name, purpose, cadence pill.

---

## 3. Exemplo mínimo

```yaml
---
schema_version: 1

processo_ref: "P5"
slug: "p5-credito"

subprocessos:
  - id: p5-1
    code: "P5.1"
    name: "Originação & Pré-análise"
    purpose: "Capturar demanda de crédito, aplicar triagem inicial e classificar o lead para análise."
    cadence: "D+0 online · contínuo"
    owner: "Comercial Crédito · Originadores"
    sistemas: "Bitrix24 · Boa Vista · Quod · LandingPage"
    volume: "~ 1.200 leads / mês"
    inputs:
      - what: "Lead / Indicação de crédito"
        from: "P1 Demanda · P2 Prospecção · P9 Pós-venda"
        detail: "Form, telefone, originador externo"
      - what: "Política de Crédito M7"
        from: "Risco · POL-CR-001"
        detail: "Régua de elegibilidade vigente"
      - what: "Bureau Score básico"
        from: "Boa Vista · Quod"
        detail: "Score público + flag restritivo"
    outputs:
      - what: "Lead qualificado"
        to: "P5.2 Análise"
        detail: "Em fila para underwriting"
      - what: "Pré-aprovação ou recusa"
        to: "Cliente · Comercial"
        detail: "Mensagem automática + ticket"
      - what: "dim_lead_credito"
        to: "BI · ClickHouse"
        detail: "Snapshot CDC ~5min"
    etapas:
      - "Receber lead pelo canal de origem"
      - "Validar dados cadastrais + restritivos"
      - "Consultar bureau de score básico"
      - "Pré-classificar (verde/amarelo/vermelho)"
      - "Encaminhar para análise ou negar"
    regulacao:
      - code: R1
        label: "LGPD"
        detail: "Consentimento + minimização"
      - code: R2
        label: "BCB 4.949"
        detail: "Direitos do consumidor"
    suporte:
      - code: S1
        label: "TI / CRM"
        detail: "Bitrix24 + integração bureau"
      - code: S2
        label: "Mesa de Risco"
        detail: "Régua de elegibilidade"
---
```

---

## 4. Regras de validação

### Determinísticas (bloqueadores)
- **SCHEMA-MISSING** — campo raiz ausente (`processo_ref`, `slug`, `subprocessos`)
- **SUBPROC-INCOMPLETO** — falta campo obrigatório no subproc.
- **VERB-GENERIC** — purpose começa com verbo proibido: {fazer, realizar, gerenciar, executar, cuidar, tratar}
- **PURPOSE-VAZIO** — purpose vazio ou < 30 chars
- **OWNER-PESSOA** — owner não contém marcador de cargo (mesma regex da N1)
- **IO-DUP** — `inputs[].what` aparece também em `outputs[].what` (pass-through detectado; subproc. não transforma)
- **IO-COUNT** — inputs ou outputs fora de [3..5]
- **ETAPAS-FAIXA** — etapas.length fora de [4..8]
- **REG-FAIXA** — regulacao.length fora de [2..4]
- **SUP-FAIXA** — suporte.length fora de [2..4]
- **REG-CODE-INVALIDO** — code fora de {R1, R2, R3, R4}
- **SUP-CODE-INVALIDO** — code fora de {S1, S2, S3, S4}

### Determinísticas (avisos)
- **VERB-WEAK** — purpose começa com verbo abstrato: {administrar, atuar, lidar, manter, ...} (mesma lista da N1)
- **PURPOSE-LONGO** — purpose > 200 chars (pode quebrar o layout do DEIP)
- **ETAPA-LONGA** — alguma etapa > 80 chars
- **DETAIL-AUSENTE** — input/output/regulacao/suporte sem `detail` (perde info no DEIP)

### Cross-checks (com processo-n2.md, em `--all`)
- **SUBPROC-MISMATCH** — set de `subprocessos[].code` aqui ≠ set em `processo-n2.md` (faltam ou sobram)
- **SUBPROC-ORDEM-MISMATCH** — ordem dos subprocessos[] difere (importante porque a sidebar e o BPMN herdam ordem)

### Semânticas (delegadas ao `n2-interview-critic` / `n2-build-critic`)
- Inputs[].from realmente existem (subproc citado existe? ator externo é plausível?)
- Outputs[].to realmente consomem (subproc citado existe? BI faz sentido?)
- Etapas são sequenciais coerentes (não pula passo crítico)
- Regulação aderente ao setor (FIDC sem CVM 175 é suspeito)

---

## 5. Anti-padrões SIPOC

- ❌ **purpose como atividade** ("Receber leads, validar e encaminhar") — purpose é **finalidade**, não passo-a-passo. Use: "Capturar demanda e classificar para análise."
- ❌ **owner = pessoa** ("João Silva") — sempre cargo/comitê
- ❌ **inputs == outputs** — significa pass-through. Se realmente é pass-through, junte com o subproc. anterior ou posterior
- ❌ **etapas tipo "Fazer X / Fazer Y"** — etapas são granularidade N2 macro, verbo no infinitivo, sem "fazer"
- ❌ **regulação genérica** ("Compliance geral") — cite norma específica (LGPD, CVM 175, CMN 4.557, Lei 9.514, ...)
- ❌ **suporte sem detail** — não basta dizer "TI"; explique "TI/CRM — Bitrix24 + integração bureau"
- ❌ **DEIP de N3** — se você está descrevendo atividades passo-a-passo internas do subproc., parou de fazer N2 e foi para N3
