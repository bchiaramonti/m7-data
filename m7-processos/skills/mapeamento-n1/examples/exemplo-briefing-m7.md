---
schema_version: 1

empresa:
  nome: "M7 Investimentos"
  slug: "m7-investimentos"
  setor: "Wealth management / Multi-family office"
  escopo: "holding"

data_referencia: "Fev / 2026"
versao: "02/26"
area_documento: "Estrategia"
logo: "default"

n1:
  variante: "A"
  rotulo_nucleo: "Verticais de Produto"
  total_processos: 18
  contagens:
    gerenciais: 4
    primarios:  9
    apoio:      5

processos:
  # ======================== GERENCIAIS (4) ========================
  - codigo: "G1"
    camada: "gerencial"
    nome: "Planejamento Estrategico"
    tooltip:
      - "Missao, visao, metas de longo prazo"
      - "Portfolio e revisao estrategica"
      - "Freq: Anual + revisoes semestrais"
    frequencia: "Anual + revisoes semestrais"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Definir"
      objeto: "o direcionamento estrategico de longo prazo"
      finalidade: "para alinhar investimentos, estrutura e cultura as oportunidades"
      inputs:
        - "Cenario macroeconomico"
        - "Performance do ano anterior"
        - "Pleitos das BUs"
        - "Brief dos sponsors"
      outputs:
        - "Plano estrategico aprovado"
        - "OKRs por area"
        - "Capital alocado por BU"
      owner: "CEO · Comite Estrategico"
    n3:
      coluna: "gerencial"
      posicao: { left: 8, top: 18 }
      friction:
        is_friction: false
        text: ""

  - codigo: "G2"
    camada: "gerencial"
    nome: "Gestao de Performance"
    tooltip:
      - "Desdobramento de metas por vertical"
      - "Rituais N1/N2/N3 com cadencia fixa"
      - "Freq: Semanal / Mensal"
    frequencia: "Semanal / Mensal"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Acompanhar"
      objeto: "a execucao das metas e KRs"
      finalidade: "para corrigir desvios e proteger compromissos anuais"
      inputs:
        - "OKRs definidos no PE"
        - "Dashboards de BI"
        - "Comites de cada BU"
      outputs:
        - "Status reports semanais"
        - "Decisoes de correcao"
        - "Auditoria de aderencia"
      owner: "Head de Performance · Comite de Gestao"
    n3:
      coluna: "gerencial"
      posicao: { left: 8, top: 32 }
      friction:
        is_friction: false
        text: ""

  - codigo: "G3"
    camada: "gerencial"
    nome: "Compliance & Risco"
    tooltip:
      - "Monitoramento CVM, SUSEP, BACEN"
      - "Gestao de riscos operacionais"
      - "Freq: Continua + auditorias"
    frequencia: "Continua + auditorias"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Garantir"
      objeto: "aderencia regulatoria e mitigacao de riscos"
      finalidade: "para preservar reputacao, licencas e capital da holding"
      inputs:
        - "Mapas regulatorios"
        - "Logs de operacoes"
        - "Reclamacoes e ouvidoria"
      outputs:
        - "Pareceres de compliance"
        - "Planos de remediacao"
        - "Reportes regulatorios"
      owner: "Diretor de Compliance · Comite de Riscos"
    n3:
      coluna: "gerencial"
      posicao: { left: 8, top: 46 }
      friction:
        is_friction: false
        text: ""

  - codigo: "G4"
    camada: "gerencial"
    nome: "Gestao Orcamentaria"
    tooltip:
      - "Planejamento e controle orcamentario"
      - "DRE por vertical e centro de custo"
      - "Freq: Mensal"
    frequencia: "Mensal"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Alocar"
      objeto: "capital e custos as BUs e areas"
      finalidade: "para garantir solidez financeira e ROI por vertical"
      inputs:
        - "Plano estrategico aprovado"
        - "DRE realizado"
        - "Pleitos de investimento"
      outputs:
        - "Orcamento aprovado"
        - "DRE projetado"
        - "Aprovacoes de capex"
      owner: "CFO · Comite Orcamentario"
    n3:
      coluna: "gerencial"
      posicao: { left: 8, top: 60 }
      friction:
        is_friction: false
        text: ""

  # ======================== PRIMARIOS (9) =========================
  - codigo: "P1"
    camada: "primario"
    subcamada: "front"
    nome: "Geracao de Demanda"
    tooltip:
      - "Inside Sales, Marketing Digital"
      - "Campanhas, eventos, indicacoes"
      - "Funil: topo + meio"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Atrair"
      objeto: "leads qualificados para as verticais"
      finalidade: "para alimentar o funil comercial e expandir base"
      inputs:
        - "Brief de campanha"
        - "Persona definida"
        - "Verba aprovada"
      outputs:
        - "MQLs entregues"
        - "Pipeline de eventos"
        - "Conteudo publicado"
      owner: "Head de Marketing · Comite Comercial"
    n3:
      coluna: "front"
      posicao: { left: 26, top: 34 }
      friction:
        is_friction: false
        text: ""

  - codigo: "P2"
    camada: "primario"
    subcamada: "front"
    nome: "Aquisicao & Onboarding"
    tooltip:
      - "Conversao de lead em cliente"
      - "KYC, suitability, abertura"
      - "Transferencia para verticais"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Converter"
      objeto: "leads em clientes onboarded"
      finalidade: "para entregar cliente pronto a vertical apropriada"
      inputs:
        - "MQLs do P1"
        - "Documentacao do cliente"
        - "Politicas de KYC"
      outputs:
        - "Cliente onboarded"
        - "Suitability validado"
        - "Conta aberta"
      owner: "Head Comercial · Comite Comercial"
    n3:
      coluna: "front"
      posicao: { left: 26, top: 56 }
      friction:
        is_friction: true
        text: "Handoff manual P1->P2 perde cerca de 20% dos leads. Sem CRM unificado, lead esfria entre marketing e comercial."

  - codigo: "P3"
    camada: "primario"
    subcamada: "nucleo"
    nome: "Investimentos"
    meta: "Captacao R$ 130MM ate 2030"
    tooltip:
      - "XP, Fundos, Renda Fixa/Variavel"
      - "Meta: R$ 9,7 MM"
      - "Funil CRM principal"
    highlight: true
    blue_accent: false
    sipoc:
      verbo: "Construir"
      objeto: "carteiras de investimento personalizadas"
      finalidade: "para fazer o patrimonio do cliente crescer com risco controlado"
      inputs:
        - "Cliente onboarded"
        - "Suitability"
        - "Politicas de alocacao"
      outputs:
        - "Carteiras montadas"
        - "Aportes recorrentes"
        - "Rebalanceamentos"
      owner: "Head de Investimentos · Comite de Alocacao"
    n3:
      coluna: "nucleo-l"
      posicao: { left: 44, top: 22 }
      friction:
        is_friction: false
        text: ""

  - codigo: "P4"
    camada: "primario"
    subcamada: "nucleo"
    nome: "Wealth"
    meta: "AuM R$ 80MM ate 2030"
    tooltip:
      - "Gestao patrimonial, Advisory"
      - "Meta: R$ 2,4 MM"
      - "Clientes alta renda"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Operar"
      objeto: "consultoria patrimonial integrada para alta renda"
      finalidade: "para preservar e expandir patrimonio em horizonte longo"
      inputs:
        - "Cliente alta renda"
        - "Diagnostico patrimonial"
        - "Politicas tributarias"
      outputs:
        - "Plano patrimonial"
        - "Estruturas de holding"
        - "Sucessao estruturada"
      owner: "Head de Wealth · Comite Patrimonial"
    n3:
      coluna: "nucleo-l"
      posicao: { left: 44, top: 42 }
      friction:
        is_friction: false
        text: ""

  - codigo: "P5"
    camada: "primario"
    subcamada: "nucleo"
    nome: "Credito"
    meta: "Operacoes R$ 25MM/ano"
    tooltip:
      - "FIDC Credito + Servicos, Consignado"
      - "Meta: R$ 22,6 MM"
      - "Maior vertical em receita"
    highlight: true
    blue_accent: false
    sipoc:
      verbo: "Originar"
      objeto: "credito colateralizado e consignado"
      finalidade: "para liberar capital de giro e consumo com garantia adequada"
      inputs:
        - "Lead com necessidade"
        - "Politicas de credito"
        - "Funding disponivel"
      outputs:
        - "Operacao desembolsada"
        - "Carteira ativa"
        - "Taxa de inadimplencia controlada"
      owner: "Head de Credito · Comite de Credito"
    n3:
      coluna: "nucleo-l"
      posicao: { left: 44, top: 62 }
      friction:
        is_friction: false
        text: ""

  - codigo: "P6"
    camada: "primario"
    subcamada: "nucleo"
    nome: "Universo"
    meta: "Volume R$ 10MM/ano"
    tooltip:
      - "Produtos PF, Consorcios PF"
      - "Meta: R$ 2,2 MM"
      - "Base 100k CPFs"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Distribuir"
      objeto: "produtos PF para a base ampla"
      finalidade: "para monetizar relacionamento e ampliar share-of-wallet"
      inputs:
        - "Base de clientes"
        - "Catalogo de produtos"
        - "Campanhas de cross-sell"
      outputs:
        - "Produtos contratados"
        - "Receita recorrente"
        - "Engajamento da base"
      owner: "Head de Universo · Comite Comercial"
    n3:
      coluna: "nucleo-r"
      posicao: { left: 56, top: 30 }
      friction:
        is_friction: false
        text: ""

  - codigo: "P7"
    camada: "primario"
    subcamada: "nucleo"
    nome: "Seg/Cons"
    meta: "Premios R$ 8MM/ano"
    tooltip:
      - "Seguros PF e PJ, Consorcios"
      - "Meta: R$ 7,35 MM"
      - "Cross-sell natural"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Estruturar"
      objeto: "solucoes de protecao e construcao patrimonial"
      finalidade: "para mitigar riscos do cliente e antecipar projetos de longo prazo"
      inputs:
        - "Diagnostico de risco"
        - "Catalogo de seguradoras"
        - "Cotacoes ativas"
      outputs:
        - "Apolice contratada"
        - "Consorcio ativo"
        - "Renovacao gerenciada"
      owner: "Head de Seguros · Comite Comercial"
    n3:
      coluna: "nucleo-r"
      posicao: { left: 56, top: 50 }
      friction:
        is_friction: false
        text: ""

  - codigo: "P8"
    camada: "primario"
    subcamada: "nucleo"
    nome: "IB"
    meta: "Receitas R$ 6MM/ano"
    tooltip:
      - "M&A, Estruturacoes"
      - "Meta: R$ 5,5 MM"
      - "Operacoes de maior ticket"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Conduzir"
      objeto: "operacoes de M&A e estruturacao de capital"
      finalidade: "para criar liquidez e crescimento inorganico aos clientes PJ"
      inputs:
        - "Mandato do cliente"
        - "Universo de investidores"
        - "Documentacao corporativa"
      outputs:
        - "Deal fechado"
        - "Estruturacao de capital"
        - "Captacao concluida"
      owner: "Head de IB · Comite de Investimentos"
    n3:
      coluna: "nucleo-r"
      posicao: { left: 56, top: 70 }
      friction:
        is_friction: false
        text: ""

  - codigo: "P9"
    camada: "primario"
    subcamada: "back"
    nome: "Relacionamento & Retencao"
    tooltip:
      - "Pos-venda, NPS, reativacao"
      - "Cross-sell entre verticais"
      - "Retroalimenta P1 com leads"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Reter"
      objeto: "clientes ativos e ampliar relacionamento"
      finalidade: "para maximizar LTV e gerar advocacy entre os clientes"
      inputs:
        - "Cliente ativo"
        - "Sinal de risco de churn"
        - "Oportunidade de cross-sell"
      outputs:
        - "Cliente retido"
        - "Cross-sell ativado"
        - "NPS reportado"
      owner: "Head de Customer Success · Comite Comercial"
    n3:
      coluna: "back"
      posicao: { left: 74, top: 50 }
      friction:
        is_friction: true
        text: "CS nao devolve sinal estruturado para as verticais. Loop de aprendizado quebrado: insights do cliente nao chegam ao produto/oferta."

  # ========================== APOIO (5) ===========================
  - codigo: "A1"
    camada: "apoio"
    nome: "Tecnologia & Dados"
    tooltip:
      - "CRM, BI, integracoes"
      - "Pilar integrador entre verticais"
      - "Viabiliza visao 360 para cross-sell"
    highlight: false
    blue_accent: true
    sipoc:
      verbo: "Operar"
      objeto: "plataforma de dados e integracoes da holding"
      finalidade: "para que toda a operacao opere com a mesma fonte de verdade"
      inputs:
        - "Demandas das verticais"
        - "Roadmap de produto"
        - "Capacidade do time"
      outputs:
        - "Plataforma estavel"
        - "Integracoes vivas"
        - "BI confiavel"
      owner: "CTO · Comite de Tecnologia"
    n3:
      coluna: "apoio"
      posicao: { left: 18, top: 86 }
      friction:
        is_friction: true
        text: "Dados fragmentados entre verticais. Cada vertical tem sua propria fonte de verdade, visao 360 do cliente fica incompleta."

  - codigo: "A2"
    camada: "apoio"
    nome: "Juridico"
    tooltip:
      - "Contratos, regulatorio"
      - "Suporte as operacoes de IB e Credito"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Resguardar"
      objeto: "interesses legais e contratuais da holding"
      finalidade: "para minimizar exposicao juridica e viabilizar operacoes"
      inputs:
        - "Demandas das BUs"
        - "Mapa regulatorio"
        - "Contratos modelo"
      outputs:
        - "Contratos validados"
        - "Pareceres juridicos"
        - "Defesa em contencioso"
      owner: "Diretor Juridico · Comite de Riscos"
    n3:
      coluna: "apoio"
      posicao: { left: 36, top: 90 }
      friction:
        is_friction: false
        text: ""

  - codigo: "A3"
    camada: "apoio"
    nome: "Financeiro"
    tooltip:
      - "Contas a pagar/receber, tesouraria"
      - "Conciliacao, relatorios gerenciais"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Administrar"
      objeto: "fluxos financeiros e tesouraria da holding"
      finalidade: "para garantir liquidez operacional e fechamento contabil correto"
      inputs:
        - "Fluxo de caixa projetado"
        - "Contas a pagar"
        - "Contas a receber"
      outputs:
        - "Conciliacao bancaria"
        - "DRE consolidado"
        - "Relatorios fiscais"
      owner: "Gerente Financeiro · Comite Orcamentario"
    n3:
      coluna: "apoio"
      posicao: { left: 54, top: 90 }
      friction:
        is_friction: false
        text: ""

  - codigo: "A4"
    camada: "apoio"
    nome: "Gestao de Pessoas"
    tooltip:
      - "Recrutamento, T&D, clima"
      - "Avaliacao de desempenho, PDI"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Desenvolver"
      objeto: "talentos e cultura organizacional"
      finalidade: "para sustentar performance e atrair pessoas certas para o crescimento"
      inputs:
        - "Estrategia de pessoas"
        - "Mapa de talentos"
        - "Politicas de carreira"
      outputs:
        - "Time estruturado"
        - "Cultura forte"
        - "PDIs ativos"
      owner: "Head de Pessoas · Comite Estrategico"
    n3:
      coluna: "apoio"
      posicao: { left: 72, top: 90 }
      friction:
        is_friction: false
        text: ""

  - codigo: "A5"
    camada: "apoio"
    nome: "Backoffice"
    tooltip:
      - "Operacoes administrativas"
      - "Cadastro, processamento, compliance ops"
    highlight: false
    blue_accent: false
    sipoc:
      verbo: "Processar"
      objeto: "operacoes administrativas e cadastrais"
      finalidade: "para liberar a ponta comercial das tarefas operacionais"
      inputs:
        - "Demandas das verticais"
        - "Documentos pendentes"
        - "SLAs definidos"
      outputs:
        - "Cadastros completos"
        - "Operacoes processadas"
        - "SLAs cumpridos"
      owner: "Coordenador de Backoffice · Comite Operacional"
    n3:
      coluna: "apoio"
      posicao: { left: 90, top: 86 }
      friction:
        is_friction: false
        text: ""

# ========================= RELACOES =========================
relacoes:
  # Espinha dorsal de cliente (forte)
  - { from: "P1", to: "P2", kind: "cliente", label: "Lead qualificado",         forca: "strong" }
  - { from: "P2", to: "P3", kind: "cliente", label: "Cliente onboarded",        forca: "strong" }
  - { from: "P3", to: "P9", kind: "cliente", label: "Cliente ativo",            forca: "strong" }

  # Cliente medio
  - { from: "P2", to: "P5", kind: "cliente", label: "Lead com necessidade de credito", forca: "mid" }
  - { from: "P3", to: "P7", kind: "cliente", label: "Cross-sell de seguro",     forca: "mid" }
  - { from: "P5", to: "P9", kind: "cliente", label: "Cliente com credito ativo", forca: "mid" }
  - { from: "P6", to: "P9", kind: "cliente", label: "Cliente com produtos PF",  forca: "mid" }
  - { from: "P7", to: "P9", kind: "cliente", label: "Cliente com seguro",       forca: "mid" }
  - { from: "P8", to: "P9", kind: "cliente", label: "Cliente IB recorrente",    forca: "mid" }

  # Cross-sell entre verticais (fraco)
  - { from: "P3", to: "P6", kind: "cliente", label: "Cross-sell base ampla",    forca: "soft" }
  - { from: "P4", to: "P5", kind: "cliente", label: "Wealth alavancado",        forca: "soft" }
  - { from: "P5", to: "P7", kind: "cliente", label: "Seguro de garantia",       forca: "soft" }

  # Loop de retencao
  - { from: "P9", to: "P3", kind: "cliente", label: "Expansao / nova alocacao", forca: "soft" }

  # Gerencial -> primarios (info)
  - { from: "G1", to: "P3", kind: "info", label: "Metas e prioridades estrategicas" }
  - { from: "G1", to: "P1", kind: "info", label: "Posicionamento estrategico" }
  - { from: "G2", to: "P4", kind: "info", label: "KRs e ritmo de performance" }
  - { from: "G2", to: "P1", kind: "info", label: "Funil e KPIs comerciais" }
  - { from: "G4", to: "P9", kind: "info", label: "Orcamento e capital alocado" }

  # Apoio -> nucleo (info)
  - { from: "A1", to: "P3", kind: "info", label: "Dados de cliente e BI" }
  - { from: "A1", to: "P5", kind: "info", label: "Dados de cliente e BI" }
  - { from: "A1", to: "P9", kind: "info", label: "Dados de cliente e BI" }
  - { from: "A1", to: "P2", kind: "info", label: "CRM e integracoes" }
  - { from: "A2", to: "P5", kind: "info", label: "Contratos e regulatorio" }
  - { from: "A2", to: "P8", kind: "info", label: "Contratos M&A" }
  - { from: "A4", to: "P3", kind: "info", label: "Time treinado" }
  - { from: "A5", to: "P2", kind: "info", label: "Cadastro processado" }

  # Compliance -> verticais (decisao)
  - { from: "G3", to: "P3", kind: "decisao", label: "Compliance suitability" }
  - { from: "G3", to: "P5", kind: "decisao", label: "Compliance credito" }
  - { from: "G3", to: "P8", kind: "decisao", label: "Compliance M&A" }
  - { from: "G2", to: "P9", kind: "decisao", label: "Auditoria de NPS / KRs" }

politica:
  metadata:
    codigo_documento: "POL-PROC-001"
    data_vigencia: "01/03/2026"
    proxima_revisao: "01/03/2027"
    area_responsavel: "Estrategia & Governanca"

  versoes:
    - versao: "v1.0"
      data: "Fev / 2026"
      alteracoes: "Primeira versao formal da cadeia de valor apos workshop com BUs (jan/26). Substitui o mapa instrucional de 06/abr/2025."
      responsavel: "Bruno Chiaramonti · Head of Performance"
      status: "vigente"

  aprovacoes:
    elaborador:
      nome: "Bruno Chiaramonti"
      cargo: "Head of Performance"
      data: "15/02/2026"
    revisor:
      nome: "Juliane Lima"
      cargo: "COO"
      data: "22/02/2026"
    aprovador:
      nome: "Marcelo Mello"
      cargo: "CEO"
      data: "28/02/2026"

  objetivo_texto: |
    Estabelecer a arquitetura formal de processos da M7 Investimentos como linguagem
    comum entre as 6 BUs, base de execucao para os projetos H1 do Planejamento
    Estrategico 2026-2030 (CRM, Maquina de Vendas, Customer Success). Reduz
    dependencia de conhecimento individual e garante consistencia na experiencia
    do cliente em todos os pontos de contato.

  escopo:
    inclusoes:
      - "Todos os colaboradores das 6 BUs (Comercial, Investimentos, Credito, Seguros, Consorcio, CS)"
      - "Parceiros e prestadores que operam processos com clientes M7"
      - "Lideres de area com responsabilidade RACI sobre processos macro"
    exclusoes:
      - "Operacoes de M&A em curso (H2-01 Consolidacao)"
      - "BUs em descontinuacao ou pivot estrutural"
    doc_relacionados:
      - "Plano Estrategico 2026-2030 (PE-2026)"
      - "Brandbook M7-2026"
      - "Manual de Compliance & Suitability"

  governanca:
    comite_revisor: "Comite de Processos · Reuniao Mensal"
    doc_sla: "SLA-OPE-001"
    area_compliance: "Compliance & Risco"

  sipoc_amostra:
    - "G1"           # Planejamento Estrategico (gerencial, topo da arquitetura)
    - "P3"           # Investimentos (vertical principal, ponto de entrada PF)

artefatos_a_gerar:
  - n1
  - n2
  - n3
  - n4-pdf

validacao:
  bloqueadores: []
  avisos: []
  todos: []
  bloqueadores_aceitos: []
---

# Briefing — Cadeia de Valor M7 Investimentos

> **Status**: aprovado · **Owner**: Bruno Chiaramonti · **Atualizado**: 2026-05-06

## Objetivo do diagrama

Documentar a cadeia macro da holding antes do redesenho do CRM (projeto H1-03) e da estruturacao da Maquina de Vendas (H1-04), para que o novo fluxo de dados respeite as fronteiras de processo existentes e a transformacao de R$ 31,7 MM para R$ 130 MM ate 2030 nao amplifique a desorganizacao operacional atual.

## Lede do documento

Visao consolidada dos 18 processos macro da holding M7 Investimentos. Navegue pelas abas para aprofundar cada camada (missao do processo e mapa de interdependencia).

## Contexto da empresa

- **Setor**: wealth management / multi-family office, com operacoes em Investimentos, Wealth, Credito, Universo (PF), Seguros & Consorcios e IB.
- **Escopo**: holding inteira (todas as 6 verticais + areas de apoio).
- **Numero de processos**: 18 macro (4 gerenciais + 9 primarios + 5 apoio).
- **Receita anual atual**: R$ 31,7 MM (2025); meta R$ 130 MM ate 2030.
- **Base ampla**: 100k CPFs (Universo + Seguros + Consorcio); core de wealth ~ 5k clientes.
- **Pontos criticos identificados**:
  - Handoff manual entre Geracao de Demanda (P1) e Aquisicao (P2) sem CRM unificado — cerca de 20% dos leads esfriam no caminho.
  - Customer Success (P9) nao devolve sinal estruturado para as verticais — loop de aprendizado quebrado.
  - Tecnologia & Dados (A1) tem fontes de verdade fragmentadas por vertical — visao 360 do cliente incompleta.

## Notas de iteracao

- 2026-05-06 — verbo `Gerenciar` em A3 substituido por `Administrar` (sugestao do critic; ainda fraco mas aceitavel para processo de fluxo, sera revisitado em N4).
- 2026-05-06 — `Plano estrategico` aparecia em input e output de G1; mantido apenas no output (input agora e `Brief dos sponsors`).
- 2026-05-06 — Owner de G2 originalmente "Bruno Chiaramonti"; trocado para `Head de Performance · Comite de Gestao` (regra OWNER-PESSOA).
- 2026-05-06 — A1 marcado com `blue_accent: true` para destacar funcao integradora (CRM, BI, dados).
- 2026-05-06 — P3 e P5 marcados como `highlight: true` (foco estrategico: Investimentos e Credito sao 60% da receita-meta).

## Anexos / referencias

- Plano Estrategico 2026-2030 (H1): `_docs/bibliography/PE_2026-2030.md`
- Brief original de processos (06/abr/2026): `_docs/bibliography/cadeia-de-valor-v1.md`
- Brandbook M7-2026: design system documentado em `references/design-system-m7.md`
- Cadeia anterior (versao 09/2025): substituida por esta — escopo reajustado de 9 para 18 processos
