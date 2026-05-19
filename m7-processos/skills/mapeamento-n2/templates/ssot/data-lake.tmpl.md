---
# ============================================================================
# ssot/data-lake.md · SSOT para build/data-lake.html + journey-{slug}.js (parte P5_DATALAKE)
# Schema completo: references/ssot-data-lake.md
# Validacao: scripts/check_ssot.py --target data-lake
# ============================================================================
schema_version: 1

processo_ref: "{{CODIGO}}"
slug:         "{{slug-processo}}"

# Espelho de processos[] de jornada-cx.md
processos:
  - code:    "{{CODE-1}}"
    name:    "{{NOME-1}}"
    owner:   "{{OWNER-1}}"
    cadence: "{{CADENCE-1}}"
    tone:    "a"

# 2 rows ate aqui (systems + data) por subprocesso. Depois marts + consumers globais.
rows:
  - id:       systems
    label:    "Sistemas / fontes"
    sublabel: "backstage · ferramentas"
    cells:                                 # 1 array de strings por subprocesso
      - ["{{Site M7}}", "{{Bitrix24 CRM}}", "{{Receita WS}}"]
      - ["{{Serasa}}", "{{SCR Bacen}}", "{{Modelo Score}}"]

  - id:       data
    label:    "Dado armazenado"
    sublabel: "persistencia · marts"
    cells:                                 # 1 array de {name, where, kind} por subprocesso
      - - { name: "{{lead_origem}}", where: "{{Bitrix · dim_lead}}", kind: "CRM" }
        - { name: "{{cliente_pf/pj}}", where: "{{Bitrix · dim_cliente}}", kind: "PII" }
        - { name: "{{score_bureau}}", where: "{{dim_lead_credito}}", kind: "Score" }
      - - { name: "{{docs_financ}}", where: "{{GED · S3}}", kind: "Doc" }
        - { name: "{{score_M7}}", where: "{{fact_score}}", kind: "Score" }

# Marts globais do processo (NAO por subprocesso)
marts:
  dim:                                     # >= 3
    - name: "dim_lead_credito"
      source: "{{Bitrix CRM + bureau}}"
    - name: "dim_cliente"
      source: "{{Onboarding + KYC}}"
    - name: "dim_oferta"
      source: "{{Score + politica}}"

  fact:                                    # >= 3
    - name: "fact_score"
      description: "{{Score M7 calculado por lead/oferta}}"
    - name: "fact_operacao_credito"
      description: "{{Desembolso, taxa, prazo, garantia}}"
    - name: "fact_inadimplencia"
      description: "{{NPL por faixa 15/30/60/90+}}"

# Consumers globais (NAO por subprocesso)
consumers:                                 # >= 4 tiers
  - tier: "BI"
    description: "{{Dashboards de captacao, NPL, DRE Credito}}"
  - tier: "Operacao"
    description: "{{Mesa de Credito + Servicing}}"
  - tier: "Risco"
    description: "{{Comite + estresse + provisao}}"
  - tier: "Regulatorio"
    description: "{{Reportes CVM, Bacen, ANBIMA}}"
---

# Data Lake · {{NOME_PROCESSO}}

## Notas

<!-- Decisoes de arquitetura de dados que vieram da entrevista:
     - Por que CDC ~5min e nao batch diario?
     - Que dados sao PII e precisam de mascaramento?
     - Que marts ainda nao existem e precisam ser construidos?
-->

- ...
