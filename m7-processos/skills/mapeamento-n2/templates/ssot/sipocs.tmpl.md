---
# ============================================================================
# ssot/sipocs.md · SSOT para build/sipoc-deip.html + dados-{slug}.js
# Schema completo: references/ssot-sipocs.md
# Validacao: scripts/check_ssot.py --target sipocs
# ============================================================================
schema_version: 1

processo_ref: "{{CODIGO}}"                 # ex: P5. Deve casar com processo.code em ssot/processo-n2.md
slug:         "{{slug-processo}}"          # ex: p5-credito

# 1 entrada por subprocesso. Estrutura espelha P5_DATA.subprocessos[N] do gabarito.
subprocessos:
  - id:        "{{id-1}}"                  # ex: p5-1
    code:      "{{CODE-1}}"                # ex: P5.1
    name:      "{{NOME-1}}"                # ex: Originacao & Pre-analise
    purpose:   "{{PURPOSE-1}}"             # verbo de acao + objeto + finalidade. SEM "fazer/realizar/gerenciar"
    cadence:   "{{CADENCE-1}}"             # ex: "D+0 online · contínuo"
    owner:     "{{OWNER-1}}"               # cargo/comite
    sistemas:  "{{SISTEMAS-1}}"            # CSV
    volume:    "{{VOLUME-1}}"              # ex: "~ 1.200 leads / mes"
    inputs:                                # 3-5 entradas
      - what:   "{{...}}"
        from:   "{{...}}"
        detail: "{{...}}"
    outputs:                               # 3-5 entradas. inputs[].what != outputs[].what (sem IO-DUP)
      - what:   "{{...}}"
        to:     "{{...}}"
        detail: "{{...}}"
    etapas:                                # 4-8 passos. Verbo no infinitivo.
      - "{{Receber lead pelo canal}}"
      - "{{Validar dados cadastrais}}"
      - "{{Consultar bureau}}"
      - "{{Pre-classificar}}"
      - "{{Encaminhar ou negar}}"
    regulacao:                             # 2-4. code R1..R4
      - code:   "R1"
        label:  "{{LGPD}}"
        detail: "{{Consentimento + minimizacao}}"
    suporte:                               # 2-4. code S1..S3
      - code:   "S1"
        label:  "{{TI / CRM}}"
        detail: "{{Bitrix24 + integracao bureau}}"
---

# SIPOC / DEIP · {{NOME_PROCESSO}}

## Notas por subprocesso

<!-- Para cada subprocesso, anote decisoes nao-obvias da entrevista:
     - Por que esse owner e nao outro?
     - Inputs/outputs que tiveram debate de fronteira
     - Etapas que foram simplificadas (originais tinham 10, viraram 6)
-->

### {{CODE-1}}

- ...

### {{CODE-2}}

- ...
