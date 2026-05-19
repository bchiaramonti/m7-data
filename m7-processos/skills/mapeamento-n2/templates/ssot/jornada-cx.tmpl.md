---
# ============================================================================
# ssot/jornada-cx.md · SSOT para build/jornada-cx.html + journey-{slug}.js (parte P5_JOURNEY)
# Schema completo: references/ssot-jornada-cx.md
# Validacao: scripts/check_ssot.py --target jornada-cx
# ============================================================================
schema_version: 1

processo_ref: "{{CODIGO}}"
slug:         "{{slug-processo}}"

# Lista de subprocessos para a coluna do grid. Espelha processo-n2.md mas com tone
# que vira classe CSS (a, b, c, d, e) para colorir a coluna.
processos:
  - code:    "{{CODE-1}}"
    name:    "{{NOME-1}}"
    owner:   "{{OWNER-1}}"
    cadence: "{{CADENCE-1}}"
    tone:    "a"                           # a..e, ciclico

# 4 rows. cells[] tem 1 entrada por subprocesso (mesma ordem de processos[]).
rows:
  - id:       touchpoint
    label:    "Canal / Touchpoint"
    sublabel: "onde o cliente esta"
    cells:                                 # 1 string por subprocesso
      - "{{Canais subproc 1}}"             # ex: "Site M7 · WhatsApp · Indicacao · RD"
      - "{{Canais subproc 2}}"
      - "..."

  - id:       action
    label:    "Acao do cliente"
    sublabel: "frontstage"
    cells:                                 # 1 string por subprocesso
      - "{{O que o cliente faz subproc 1}}"
      - "..."

  - id:       mot
    label:    "Momentos da Verdade"
    sublabel: "inflexao emocional"
    cells:                                 # 1 objeto {intensity, items} por subprocesso
      - intensity: 3                       # 1..3
        items:
          - "{{Primeira impressao}}"
          - "{{Velocidade do retorno}}"
      - intensity: 2
        items:
          - "..."

  - id:       pain
    label:    "Pain points · sentimento"
    sublabel: "tom: - negativo · ~ neutro · + positivo"
    cells:                                 # 1 objeto {tone, items} por subprocesso
      - tone: "-"                          # +/-/~
        items:
          - "\"Cadastro demorado\""
          - "\"Ninguem me responde\""
      - tone: "~"
        items:
          - "..."
---

# Jornada CX · {{NOME_PROCESSO}}

## Notas

<!-- Insights da entrevista sobre o CX que nao entram no JS data:
     - Quais MoTs sao mais criticos para retencao?
     - Quais pains sao recorrentes vs episodicos?
     - Onde estao oportunidades de redesenho?
-->

- ...
