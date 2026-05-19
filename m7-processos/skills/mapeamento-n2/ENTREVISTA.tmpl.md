# Entrevista N2 · {{NOME_PROCESSO}} ({{CODIGO}})

> **Data**: {{DATA}} · **Entrevistador**: Claude (skill mapeamento-n2) · **Entrevistados**: {{LISTA_ENTREVISTADOS}}
> **N1 BRIEFING**: `{{PATH_BRIEFING_N1}}` · **Round**: 1

## Anexos consultados

<!-- Liste documentos enviados pelo usuário que respondem perguntas em bloco.
     Marque cada resposta com "respondida por anexo X" quando aplicável. -->

- [ ] Política `politica-{{slug-empresa}}.html` (se existir, já cobre governança)
- [ ] Manual operacional / SOP anterior: `{{path}}`
- [ ] PE / Planejamento Estratégico: `{{path}}`
- [ ] Outro: `{{path}}`

---

## Bloco 1 · Contexto N1

> Objetivo: ancorar o processo N2 na cadeia N1 já mapeada. Puxar do BRIEFING N1 o que já está formalizado e validar com o usuário.

**Q1.1** Qual o `code` do processo primário a decompor? (ex.: P5, G2)
**R1.1** {{CODIGO}}

**Q1.2** Confirme `name`, `owner`, `receita_meta`, `descricao` do BRIEFING N1 (puxados de `processos[code=X]`):
**R1.2**
- name: {{NOME_PROCESSO}}
- owner: {{OWNER}}
- receita_meta: {{RECEITA_META}}
- descricao: {{DESCRICAO}}

**Q1.3** Qual a **lede do N2** (parágrafo curto que entra no header do `processo-n2.html`)?
**R1.3** {{LEDE_N2}}

**Q1.4** WBS · Janela · Status (metadata da strip do header):
**R1.4** WBS={{WBS}} · Janela={{JANELA}} · Status={{STATUS}}

---

## Bloco 2 · Decomposição em subprocessos

> Objetivo: definir esqueleto de N (3-8) subprocessos, sequência, fronteira. Saída entra direto no `ssot/processo-n2.md`.

**Q2.1** Quantos subprocessos compõem `{{CODIGO}}` end-to-end? (faixa saudável 3-8)
**R2.1** {{N}} subprocessos

**Q2.2** Liste os subprocessos em ordem (id, code, name, owner, cadence, sp_meta=timbre curto, sp_tech=sistemas-chave):
**R2.2**

| id | code | name | owner | cadence | sp_meta | sp_tech |
|---|---|---|---|---|---|---|
| {{id1}} | {{code1}} | {{name1}} | {{owner1}} | {{cadence1}} | {{sp_meta1}} | {{sp_tech1}} |
| ... | ... | ... | ... | ... | ... | ... |

**Q2.3** Mensagens que cruzam a pool Cliente ↔ M7 (uma por subprocesso, frase única descrevendo o "cliente → M7" e "M7 → cliente"):
**R2.3**

| code | message |
|---|---|
| {{code1}} | {{message1}} |
| ... | ... |

**Q2.4** Há fronteiras fuzzy entre subprocessos? (ex.: P5.2 e P5.3 com decisão de "onde termina análise e começa formalização")
**R2.4** {{NOTAS_FRONTEIRA}}

---

## Bloco 3 · SIPOC por subprocesso

> Objetivo: SIPOC/DEIP completo para CADA subprocesso. Material entra em `ssot/sipocs.md`.
> **Repita esta seção N vezes**, uma por subprocesso.

### SIPOC · {{CODE}}

**Q3.1** Purpose do subprocesso (verbo de ação + objeto + finalidade, sem "fazer/realizar/gerenciar"):
**R3.1** {{PURPOSE}}

**Q3.2** Owner (cargo/comitê, NUNCA nome próprio):
**R3.2** {{OWNER}}

**Q3.3** Cadência (D+0 contínuo · SLA Xd · Mensal · etc.):
**R3.3** {{CADENCE}}

**Q3.4** Sistemas-chave (CSV):
**R3.4** {{SISTEMAS}}

**Q3.5** Volume / mês:
**R3.5** {{VOLUME}}

**Q3.6** Inputs (3-5; cada: what / from / detail):
**R3.6**

| what | from | detail |
|---|---|---|
| ... | ... | ... |

**Q3.7** Outputs (3-5; cada: what / to / detail):
**R3.7**

| what | to | detail |
|---|---|---|
| ... | ... | ... |

**Q3.8** Etapas (4-8 passos sequenciais, verbo no infinitivo):
**R3.8**
1. ...
2. ...

**Q3.9** Regulação (2-4 entradas; cada: code R1..R4 / label / detail):
**R3.9**

| code | label | detail |
|---|---|---|
| R1 | ... | ... |

**Q3.10** Suporte (2-4 entradas; cada: code S1..S3 / label / detail):
**R3.10**

| code | label | detail |
|---|---|---|
| S1 | ... | ... |

---

## Bloco 4 · Jornada CX

> Objetivo: para CADA subprocesso, 4 rows do Service Blueprint do lado-cliente. Material entra em `ssot/jornada-cx.md`.

### CX · {{CODE}}

**Q4.1** Touchpoint / Canal (CSV de canais onde o cliente está nesse subprocesso):
**R4.1** {{TOUCHPOINT}}

**Q4.2** Action (frontstage — uma frase descrevendo o que o cliente faz):
**R4.2** {{ACTION}}

**Q4.3** Momentos da Verdade (MoT) — `intensity` ∈ {1,2,3} e 1-3 items descrevendo a inflexão emocional:
**R4.3**
- intensity: {{1|2|3}}
- items:
  - ...
  - ...

**Q4.4** Pain points · sentimento — `tone` ∈ {+, -, ~} e 1-3 frases entre aspas no formato "como o cliente fala":
**R4.4**
- tone: {{+|-|~}}
- items:
  - "..."
  - "..."

(Repita Bloco 4 para cada subprocesso)

---

## Bloco 5 · Data Lake

> Objetivo: para CADA subprocesso, sistemas/fontes + dado persistido; **globais por processo**: marts (dim/fact) e consumers. Material entra em `ssot/data-lake.md`.

### Data · {{CODE}}

**Q5.1** Systems / fontes (CSV de sistemas backstage nesse subprocesso):
**R5.1** {{SYSTEMS}}

**Q5.2** Dados persistidos (lista; cada: name / where / kind ∈ {CRM, PII, Score, Bureau, Doc, Contrato, Lastro, Tesouraria, Cobrança, KPI}):
**R5.2**

| name | where | kind |
|---|---|---|
| ... | ... | ... |

(Repita Q5.1-Q5.2 para cada subprocesso)

### Marts globais do processo

**Q5.3** Dimensões ClickHouse (≥3; cada: name + source resumida):
**R5.3**

| name | source |
|---|---|
| dim_... | ... |

**Q5.4** Facts ClickHouse (≥3; cada: name + descrição):
**R5.4**

| name | description |
|---|---|
| fact_... | ... |

### Consumers globais

**Q5.5** Tiers de consumidores (≥4; cada: tier + descrição do uso):
**R5.5**

| tier | description |
|---|---|
| BI | ... |
| Operação | ... |
| ... | ... |

---

## Notas livres da entrevista

<!-- Observações que não se encaixam em bloco específico mas são úteis para a Fase B. -->

- ...

---

## Validação final · n2-interview-critic

<!-- Cola aqui o output do agent n2-interview-critic após o Bloco 5.
     Cada round substitui esta seção. -->

> Round 1: (pendente)
