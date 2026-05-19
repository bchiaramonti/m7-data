---
schema_version: 1

processo_ref: "P5"
slug: "p5-credito"

processos:
  - { code: "P5.1", name: "Originação",    owner: "Comercial · Mesa Crédito", cadence: "D+0 contínuo", tone: "a" }
  - { code: "P5.2", name: "Análise",       owner: "Analista · Risco",         cadence: "SLA 3-5d",      tone: "b" }
  - { code: "P5.3", name: "Formalização",  owner: "Jurídico · BO",            cadence: "SLA 2-3d",      tone: "c" }
  - { code: "P5.4", name: "Desembolso",    owner: "Mesa Ops · Tesouraria",    cadence: "SLA D+1",       tone: "d" }
  - { code: "P5.5", name: "Monitoramento", owner: "Servicing · Cobrança",     cadence: "Diário",        tone: "e" }

rows:
  - id: touchpoint
    label: "Canal / Touchpoint"
    sublabel: "onde o cliente está"
    cells:
      - "Site M7 · Indicação · RD Marketing · WhatsApp · Bitrix Landing"
      - "WhatsApp · Telefone · Reunião remota · E-mail"
      - "E-mail jurídico · Portal cliente · DocuSign · e-Notariado"
      - "Conta bancária · App do banco · SMS de confirmação"
      - "WhatsApp · Boleto · App banco · Carta · Jurídico"

  - id: action
    label: "Ação do cliente"
    sublabel: "frontstage"
    cells:
      - "Procura solução de capital, preenche cadastro e envia documentos básicos"
      - "Sobe documentos financeiros, recebe parecer, avalia e negocia condições"
      - "Lê a minuta, valida garantias e assina CCB + aditivos digitalmente"
      - "Confere o crédito na conta e usa o recurso para a finalidade pactuada"
      - "Paga parcelas via boleto/débito/folha, renegocia ou encerra a operação"

  - id: mot
    label: "Momentos da Verdade"
    sublabel: "inflexão emocional"
    cells:
      - intensity: 3
        items:
          - "Primeira impressão de confiança"
          - "Velocidade do retorno inicial"
      - intensity: 3
        items:
          - "Recebe parecer aprovado ou negado"
          - "Vê taxa, CET e prazo"
      - intensity: 2
        items:
          - "Clica em Assinar — vínculo formal"
      - intensity: 3
        items:
          - "Dinheiro disponível na conta"
      - intensity: 3
        items:
          - "1ª parcela vence — compromisso real"
          - "Quitação celebrada ou cobrança recebida"

  - id: pain
    label: "Pain points · sentimento"
    sublabel: "tom: − negativo · ~ neutro · + positivo"
    cells:
      - tone: "-"
        items:
          - "\"Cadastro demorado, querem dados demais\""
          - "\"Estou no escuro, ninguém me responde\""
      - tone: "-"
        items:
          - "\"Já mandei tudo, por que demora tanto?\""
          - "\"A taxa é maior do que eu esperava\""
      - tone: "~"
        items:
          - "\"Contrato cheio de cláusulas, não entendo\""
          - "\"Estou assinando uma dívida — sem volta\""
      - tone: "+"
        items:
          - "\"Caiu o dinheiro! Funcionou\""
      - tone: "-"
        items:
          - "\"Cuidado para não furar o orçamento\""
          - "\"Atrasei um dia e já me ligaram pressionando\""
---

# Jornada CX · P5 Crédito

## Notas

- MoT mais críticos para retenção: P5.4 (entrega) e P5.5 (1ª parcela)
- Pain points P5.1 e P5.2 são recorrentes (NPS oscila em -25 a -40 nessas etapas)
- Oportunidade: ritmo de comunicação em P5.2 — clientes relatam silêncio de 2-3 dias
