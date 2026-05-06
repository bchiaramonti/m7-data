---
# ============================================================================
# BRIEFING.tmpl.md · single source of truth para mapeamento-n1
# ----------------------------------------------------------------------------
# Como usar:
#   1. Copie este template para o diretorio de trabalho como
#      `mapeamento-{slug}.briefing.md`.
#   2. Preencha o frontmatter YAML com os dados do mapeamento.
#   3. Preencha as secoes markdown abaixo do frontmatter.
#   4. Execute `scripts/check_briefing.py <arquivo>` para validar.
#   5. Quando bloqueadores=[], dispare a Fase C (geracao dos 4 artefatos).
#
# Schema completo: references/phase-b-briefing.md
# Validacao programatica: scripts/check_briefing.py
# Validacao critica (LLM): agents/process-critic.md
# ============================================================================
schema_version: 1

empresa:
  nome: "{{NOME_EMPRESA}}"
  slug: "{{slug-empresa}}"               # kebab-case, sem acentos
  setor: "{{SETOR}}"
  escopo: "{{ESCOPO}}"                   # holding | bu:<nome> | produto:<nome>

data_referencia: "{{MES_ANO}}"           # ex: "Fev / 2026"
versao: "{{VERSAO}}"                     # ex: "02/26"
area_documento: "{{AREA}}"               # ex: "Estrategia", "Operacoes"
logo: "default"                          # "default" usa M7 / ou caminho relativo

# ----------------------------------------------------------------------------
# N1 · Cadeia de Valor
# ----------------------------------------------------------------------------
n1:
  variante: "{{A_OU_B}}"                 # A (master) | B (linear)
  rotulo_nucleo: "{{ROTULO}}"            # ex: "Verticais de Produto"
  total_processos: 0                     # soma de gerenciais + primarios + apoio
  contagens:
    gerenciais: 0
    primarios:  0
    apoio:      0

# ----------------------------------------------------------------------------
# Processos · lista canonica
#
# Para cada processo, preencher TODOS os campos. Campos N2 (sipoc) podem
# vir depois da entrevista de missao do processo. Campos N3 (posicao,
# friction) podem vir depois do mapeamento de relacoes.
# ----------------------------------------------------------------------------
processos:
  - codigo: "G1"
    camada: "gerencial"                  # gerencial | primario | apoio
    nome: "{{NOME}}"                     # max 3 palavras
    tooltip:                             # 2-4 linhas, telegraficas, sem ponto final
      - "{{LINHA_1}}"
      - "{{LINHA_2}}"
      - "Freq: {{FREQUENCIA}}"           # obrigatorio para gerenciais
    frequencia: "{{ANUAL_MENSAL_ETC}}"   # obrigatorio se camada=gerencial
    highlight: false                     # true ativa fundo lime (max 2 na cadeia)
    blue_accent: false                   # true ativa fundo azul (max 1 na cadeia)
    sipoc:
      verbo: "{{VERBO}}"                 # 1-2 palavras (Definir, Construir, Operar...)
      objeto: "{{o objeto do processo}}" # substantivo claro
      finalidade: "{{para X e Y}}"       # depois de "para"
      inputs:
        - "{{Chip 1}}"                   # 3-6 chips, 2-4 palavras cada
        - "{{Chip 2}}"
        - "{{Chip 3}}"
      outputs:
        - "{{Chip 1}}"                   # 3-6 chips, NAO repetir inputs
        - "{{Chip 2}}"
        - "{{Chip 3}}"
      owner: "{{Cargo}} · {{Forum}}"     # cargo + comite, NUNCA nome proprio
    n3:
      coluna: "gerencial"                # gerencial | front | nucleo-l | nucleo-r | back | apoio
      posicao: { left: 8, top: 18 }      # %, dentro do canvas neural
      friction:
        is_friction: false
        text: ""                         # se is_friction=true, descreve o problema

  # Repetir bloco para cada processo. Exemplo de primario:
  # - codigo: "P1"
  #   camada: "primario"
  #   subcamada: "front"                 # front | nucleo | back (so se variante A)
  #   nome: "Geracao de Demanda"
  #   tooltip: ["Marketing + ABM", "Gera leads qualificados", "Funil topo"]
  #   highlight: false
  #   blue_accent: false
  #   sipoc:
  #     verbo: "Atrair"
  #     objeto: "leads qualificados"
  #     finalidade: "alimentar o funil comercial das verticais"
  #     inputs: ["Brief de campanha", "Persona definida", "Verba aprovada"]
  #     outputs: ["MQLs entregues", "Lista de eventos", "Conteudo publicado"]
  #     owner: "Head de Marketing · Comite Comercial"
  #   n3:
  #     coluna: "front"
  #     posicao: { left: 26, top: 34 }
  #     friction:
  #       is_friction: false
  #       text: ""

# ----------------------------------------------------------------------------
# Relacoes · alimenta a tabela RELATIONS do N3
#
# Cada item: { from, to, kind, label, forca }
#   kind:  cliente | info | decisao
#   forca: strong | mid | soft  (so para kind=cliente; afeta espessura)
# ----------------------------------------------------------------------------
relacoes:
  # - { from: "P1", to: "P2", kind: "cliente", label: "Lead qualificado", forca: "strong" }
  # - { from: "A1", to: "P3", kind: "info",    label: "Dados de cliente", forca: "mid" }
  # - { from: "G3", to: "P5", kind: "decisao", label: "Aderencia regulatoria", forca: "soft" }

# ----------------------------------------------------------------------------
# Artefatos a gerar
#
# Sequencia rigida: N1 (sempre) -> N2 (opcional) -> N3 (opcional) -> N4-PDF
# Se N4-PDF estiver listado, N1+N2+N3 sao obrigatorios (validacao bloqueia).
# ----------------------------------------------------------------------------
artefatos_a_gerar:
  - n1
  # - n2
  # - n3
  # - n4-pdf

# ----------------------------------------------------------------------------
# Resultado da validacao (preenchido por check_briefing.py + process-critic)
# ----------------------------------------------------------------------------
validacao:
  bloqueadores: []                       # lista de violacoes que IMPEDEM geracao
  avisos: []                             # lista de violacoes nao-bloqueantes
  todos: []                              # campos deixados como TODO explicito
  bloqueadores_aceitos: []               # excecoes que o usuario decidiu seguir mesmo assim
---

# Briefing — Cadeia de Valor {{NOME_EMPRESA}}

> **Status**: rascunho · **Owner**: {{OWNER_DOC}} · **Atualizado**: {{DATA}}

## Objetivo do diagrama

<!-- 2-3 linhas: por que mapear agora? Que decisao este diagrama suporta?
     Ex: "Documentar a cadeia atual antes do redesenho do CRM (H1-03), para que o novo
     fluxo de dados respeite as fronteiras de processo existentes." -->

## Lede do documento

<!-- 1-2 linhas que aparecem no header do N1 (campo `lede` do template).
     Ex: "Visao consolidada dos 18 processos macro da holding M7 Investimentos.
     Navegue pelas abas para aprofundar cada camada." -->

## Contexto da empresa

<!-- Setor, modelo de negocio, BUs, segmentacao, qualquer referencia relevante.
     Ex: setor wealth management, holding com 6 verticais, 100k clientes PF,
     receita anual R$ 31,7 MM, em transformacao para R$ 130 MM ate 2030. -->

## Notas de iteracao

<!-- Historico de criticas aceitas/recusadas durante a entrevista.
     Mantido pela skill — entrada cronologica, nao apagar.
     Ex:
     - 2026-05-06 — verbo `Gerenciar` em G2 substituido por `Garantir` (sugestao do critic)
     - 2026-05-06 — `Plano estrategico` aparecia em input e output de G1, mantido so no output
     -->

## Anexos / referencias

<!-- Links para PE, brandbook, cadeia anterior, briefings de projeto.
     Ex:
     - PE 2026-2030: link://...
     - Brandbook M7: link://...
     - Cadeia anterior (versao 09/2025): link://...
     -->
