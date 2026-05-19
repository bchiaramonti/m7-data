---
# ============================================================================
# ssot/processo-n2.md · SSOT para build/processo-n2.html (BPMN end-to-end)
# Schema completo: references/ssot-processo-n2.md
# Validacao: scripts/check_ssot.py --target processo-n2
# ============================================================================
schema_version: 1

# Referencia obrigatoria a mapeamento N1
n1_artifacts:
  briefing:                "{{PATH_BRIEFING_N1}}"           # OBRIGATORIO. Ex: ../mapeamento-m7/BRIEFING.md
  cadeia_de_valor:         "{{PATH_CV}}"                    # opcional. Ex: ../mapeamento-m7/cadeia-de-valor-m7.html
  missao_do_processo:      "{{PATH_MISSAO}}"                # opcional
  mapa_interdependencia:   "{{PATH_MAPA}}"                  # opcional
  politica:                "{{PATH_POLITICA}}"              # opcional mas RECOMENDADO. Ancora governanca

processo:
  code:          "{{CODIGO}}"             # ex: P5. Deve constar em processos[] do BRIEFING N1
  name:          "{{NOME}}"               # ex: Credito
  slug:          "{{slug-processo}}"      # kebab-case. Ex: p5-credito
  camada:        "{{CAMADA}}"             # vinda do BRIEFING N1: gerencial | primario | apoio
  owner:         "{{OWNER}}"              # cargo/comite, NUNCA nome proprio. Ex: Diretor Comercial
  receita_meta:  "{{RECEITA_META}}"       # opcional. Ex: "R$ 22,6 MM"
  descricao:     "{{DESCRICAO}}"          # 1-2 frases. Vai virar lede do header

# Metadata da strip do header (canto direito superior)
wbs:    "{{WBS}}"                          # ex: "WBS 3.2"
janela: "{{JANELA}}"                       # ex: "12/05 -> 30/05"
status: "{{STATUS}}"                       # ex: "Em producao"

# N (3-8) subprocessos curtos. Detalhamento SIPOC vai em ssot/sipocs.md
subprocessos:
  - id:       "{{id-1}}"                   # ex: p5-1 (kebab)
    code:     "{{CODE-1}}"                 # ex: P5.1
    name:     "{{NOME-1}}"                 # ex: Originacao
    owner:    "{{OWNER-1}}"
    cadence:  "{{CADENCE-1}}"              # ex: "D+0 contínuo"
    sp_meta:  "{{TIMBRE-1}}"               # curto. Ex: "Multi-canal · pre-analise"
    sp_tech:  "{{SISTEMAS-1}}"             # CSV. Ex: "Bitrix24 · Boa Vista · Quod"

# Mensagens cliente <-> M7 (uma por subprocesso)
interfaces:
  - code:    "{{CODE-1}}"
    message: "{{MENSAGEM-1}}"              # ex: "Cliente -> M7: solicitacao + dados / M7 -> Cliente: pre-aprovacao ou recusa"
---

# Processo N2 · {{NOME}}

## Lede

<!-- Paragrafo que entra como `<p class="lede">` no header do processo-n2.html.
     1-3 frases. Posicione o processo no setor + escopo + valor entregue. -->

{{LEDE_N2}}

## Notas de iteracao

<!-- Decisoes tomadas durante a entrevista, ambiguidades resolvidas,
     justificativa para bloqueadores aceitos do n2-interview-critic. -->

- ...
