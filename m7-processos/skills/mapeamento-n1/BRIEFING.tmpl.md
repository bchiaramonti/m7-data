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
  #   meta: "10k MQLs/mes"                # opcional, usado APENAS em N4 (Politica).
  #                                       # KR/indicador principal do processo.
  #                                       # Obrigatorio para primarios se n4-pdf em artefatos_a_gerar.
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
# Politica · metadata adicional para N4 (Documento Oficial)
#
# Preenchimento OBRIGATORIO se `n4-pdf` esta em `artefatos_a_gerar`.
# Pode permanecer com placeholders se voce so vai gerar N1/N2/N3.
#
# Captura o que diferencia uma "politica formal" de um "mapa operacional":
# codigo do documento, controle de versoes, aprovacoes assinadas,
# objetivo/escopo narrativos e governanca.
# ----------------------------------------------------------------------------
politica:
  metadata:
    codigo_documento: "{{POL-PROC-001}}"   # codigo formal — ex: POL-PROC-001, NORM-GOV-005
    data_vigencia: "{{DD/MM/AAAA}}"        # quando entra em vigor
    proxima_revisao: "{{DD/MM/AAAA}}"      # data limite para proxima revisao
    area_responsavel: "{{Area}}"           # quem responde pela politica

  # Versao atual + ate 2 anteriores (templates suporta exatamente 3 linhas)
  versoes:
    - versao: "{{v1.0}}"                   # ex: "v1.0", "v2.1"
      data: "{{MES / AAAA}}"               # ex: "Fev / 2026"
      alteracoes: "{{Descricao das mudancas desta versao}}"
      responsavel: "{{Nome ou cargo}}"
      status: "vigente"                    # vigente | obsoleto
    # Anteriores (opcional, ate 2):
    # - versao: "v0.9"
    #   data: "Dez / 2025"
    #   alteracoes: "Revisao geral apos workshop com BUs"
    #   responsavel: "Comite de Processos"
    #   status: "obsoleto"
    # - versao: "v0.8"
    #   data: "Out / 2025"
    #   alteracoes: "Versao inicial"
    #   responsavel: "Bruno Chiaramonti"
    #   status: "obsoleto"

  # 3 papeis formais — todos obrigatorios para N4
  aprovacoes:
    elaborador:
      nome: "{{Nome}}"
      cargo: "{{Cargo}}"
      data: "{{DD/MM/AAAA}}"
    revisor:
      nome: "{{Nome}}"
      cargo: "{{Cargo}}"
      data: "{{DD/MM/AAAA}}"
    aprovador:
      nome: "{{Nome}}"
      cargo: "{{Cargo}}"
      data: "{{DD/MM/AAAA}}"

  # Conteudo narrativo das paginas 3 (Objetivo · Escopo · Definicoes)
  objetivo_texto: |
    {{2-4 linhas explicando o objetivo formal desta politica.
    Para que ela existe? Que valor estabelece? Como suporta a estrategia?}}

  escopo:
    inclusoes:                             # 2-4 itens — a quem se aplica
      - "{{Inclusao 1 — ex: Todos os colaboradores das BUs}}"
      - "{{Inclusao 2 — ex: Parceiros que operam processos da cadeia}}"
    exclusoes:                             # 1-3 itens — a quem NAO se aplica
      - "{{Exclusao 1 — ex: Operacoes de M&A em curso}}"
    doc_relacionados:                      # 1-4 itens — referencias cruzadas
      - "{{Documento relacionado 1 — ex: Plano Estrategico 2026-2030}}"
      - "{{Documento relacionado 2 — ex: Manual de Compliance}}"

  governanca:
    comite_revisor: "{{Comite ou Forum}}"  # ex: "Comite de Processos"
    doc_sla: "{{Codigo}}"                  # ex: "SLA-OPE-001" — referenciado em SLA inter-camadas
    area_compliance: "{{Area}}"            # ex: "Compliance & Risco"

  # SIPOC sample — quais 2 processos featurar na pagina 8 (amostra didatica)
  # Use codigos de processos[] que tenham sipoc preenchido.
  sipoc_amostra:
    - "{{CODIGO_A}}"                       # ex: "G1" — primeiro processo featurado
    - "{{CODIGO_B}}"                       # ex: "P3" — segundo processo featurado

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
