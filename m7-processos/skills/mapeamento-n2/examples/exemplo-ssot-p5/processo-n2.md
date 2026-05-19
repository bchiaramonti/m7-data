---
schema_version: 1

n1_artifacts:
  briefing: "./_fake-n1-briefing.md"

processo:
  code: "P5"
  name: "Crédito"
  slug: "p5-credito"
  camada: "primario"
  owner: "Diretor Comercial · Mesa Crédito"
  receita_meta: "R$ 22,6 MM"
  descricao: "FIDC Crédito, FIDC Serviços e Consignado privado/público."

wbs: "WBS 3.2"
janela: "12/05 → 30/05"
status: "Em produção"

subprocessos:
  - id: p5-1
    code: "P5.1"
    name: "Originação"
    owner: "Comercial Crédito · Originadores"
    cadence: "D+0 contínuo"
    sp_meta: "Multi-canal · pré-análise"
    sp_tech: "Bitrix24 · Boa Vista · Quod"

  - id: p5-2
    code: "P5.2"
    name: "Análise & Score"
    owner: "Analista Crédito · Mesa Risco"
    cadence: "SLA 3-5d"
    sp_meta: "Underwriting · alçadas"
    sp_tech: "Serasa · SCR Bacen · Modelo M7"

  - id: p5-3
    code: "P5.3"
    name: "Estruturação & Formalização"
    owner: "Backoffice Jurídico"
    cadence: "SLA 2-3d"
    sp_meta: "Contratos · garantias"
    sp_tech: "DocuSign · CETIP · Núclea"

  - id: p5-4
    code: "P5.4"
    name: "Desembolso & Operação"
    owner: "Mesa Operações · Tesouraria"
    cadence: "SLA D+1"
    sp_meta: "Liberação · cota FIDC"
    sp_tech: "FIDC Admin · PIX · Folha"

  - id: p5-5
    code: "P5.5"
    name: "Monitoramento & Cobrança"
    owner: "Servicing · Cobrança"
    cadence: "Diário"
    sp_meta: "NPL · régua · recovery"
    sp_tech: "ClickHouse · Régua · Núclea"

interfaces:
  - code: "P5.1"
    message: "Cliente → M7: solicitação + dados básicos / M7 → Cliente: pré-aprovação ou recusa motivada"
  - code: "P5.2"
    message: "Cliente → M7: documentos financeiros / M7 → Cliente: oferta com limite/taxa/prazo"
  - code: "P5.3"
    message: "M7 → Cliente: minutas para assinar / Cliente → M7: CCB assinada + garantias"
  - code: "P5.4"
    message: "M7 → Cliente: confirmação de desembolso / Cliente: recebe TED/PIX ou averbação"
  - code: "P5.5"
    message: "M7 → Cliente: lembretes e cobrança / Cliente → M7: pagamento de parcelas"
---

# Processo N2 · Crédito

## Lede

O P5 Crédito é a vertical primária do grupo (FIDC Crédito, FIDC Serviços e Consignado), com originação multi-canal, gestão de risco end-to-end e maior contribuição de receita do portfólio. Este documento decompõe o P5 em 5 subprocessos, com BPMN end-to-end e SIPOC/DEIP por card.

## Notas de iteracao

- Owner inicialmente capturado como "Filipe Costa" (nome próprio) - corrigido para "Diretor Comercial · Mesa Crédito" no checkpoint do Bloco 1
- Cadências confirmadas com o Owner; P5.2 estava sem SLA, foi formalizada em 3-5d
