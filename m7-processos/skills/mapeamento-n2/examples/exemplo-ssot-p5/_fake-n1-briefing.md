---
# Mini BRIEFING N1 FAKE — para o smoke test do exemplo P5 validar limpo.
# NAO use este arquivo em producao. Em uso real, aponte para o BRIEFING
# completo gerado pela skill mapeamento-n1.
schema_version: 1

empresa:
  nome: "M7 Investimentos"
  slug: "m7"
  setor: "wealth-management"
  escopo: "holding"

data_referencia: "Mai / 2026"
versao: "01/26"
area_documento: "Estrategia"
logo: "default"

n1:
  variante: "A"
  rotulo_nucleo: "Verticais de Produto"
  total_processos: 5
  contagens:
    gerenciais: 1
    primarios:  3
    apoio:      1

processos:
  - codigo: "G1"
    camada: "gerencial"
    nome:   "Governanca"
    tooltip: ["Comite executivo", "Freq: Mensal"]
    frequencia: "Mensal"
  - codigo: "P1"
    camada: "primario"
    subcamada: "front"
    nome:   "Captacao"
    tooltip: ["Multi-canal"]
  - codigo: "P5"
    camada: "primario"
    subcamada: "nucleo"
    nome:   "Credito"
    tooltip: ["FIDC Credito · FIDC Servicos · Consignado"]
    highlight: true
  - codigo: "P7"
    camada: "primario"
    subcamada: "back"
    nome:   "Servicing"
    tooltip: ["Pos-venda + cobranca"]
  - codigo: "A1"
    camada: "apoio"
    nome:   "TI & Dados"
    tooltip: ["Plataforma"]

artefatos_a_gerar: ["n1"]
validacao:
  bloqueadores: []
  avisos: []
  todos: []
  bloqueadores_aceitos: []
---

# BRIEFING N1 FAKE — M7
