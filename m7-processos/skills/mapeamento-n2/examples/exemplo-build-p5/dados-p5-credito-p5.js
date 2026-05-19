/* ===================================================================
   P5 Crédito — Dados N2 (DEIPs)
   Gerado por build_sipoc.py. NAO editar manualmente.
   =================================================================== */

window.P5_DATA = {
  "meta": {
    "code": "P5",
    "name": "Crédito",
    "camada": "primario",
    "owner": "Diretor Comercial · Mesa Crédito",
    "receita_meta": "R$ 22,6 MM",
    "descricao": "FIDC Crédito, FIDC Serviços e Consignado privado/público."
  },
  "subprocessos": [
    {
      "id": "p5-1",
      "code": "P5.1",
      "name": "Originação & Pré-análise",
      "purpose": "Capturar demanda de crédito vinda de originadores, indicações e parceiros, aplicar triagem inicial e classificar o lead para análise.",
      "cadence": "D+0 online · contínuo",
      "owner": "Comercial Crédito · Originadores",
      "sistemas": "Bitrix24 · Boa Vista · Quod · LandingPage",
      "volume": "~ 1.200 leads / mês",
      "inputs": [
        {
          "what": "Lead / Indicação de crédito",
          "from": "P1 Captação · P9 Pós-venda",
          "detail": "Form, telefone, originador externo"
        },
        {
          "what": "Política de Crédito M7",
          "from": "Mesa Risco · POL-CR-001",
          "detail": "Régua de elegibilidade vigente"
        },
        {
          "what": "Bureau Score básico",
          "from": "Boa Vista · Quod",
          "detail": "Score público + flag restritivo"
        },
        {
          "what": "Dados cadastrais do solicitante",
          "from": "Cliente",
          "detail": "CPF/CNPJ, contato, finalidade"
        }
      ],
      "outputs": [
        {
          "what": "Lead qualificado para análise",
          "to": "P5.2 Análise",
          "detail": "Em fila para underwriting"
        },
        {
          "what": "Pré-aprovação ou recusa",
          "to": "Cliente · Comercial",
          "detail": "Mensagem automática + ticket"
        },
        {
          "what": "dim_lead_credito",
          "to": "BI · ClickHouse",
          "detail": "Snapshot CDC ~5min"
        }
      ],
      "etapas": [
        "Receber lead pelo canal de origem",
        "Validar dados cadastrais + restritivos",
        "Consultar bureau de score básico",
        "Pré-classificar verde/amarelo/vermelho",
        "Encaminhar para análise ou negar"
      ],
      "regulacao": [
        {
          "code": "R1",
          "label": "LGPD",
          "detail": "Consentimento + minimização"
        },
        {
          "code": "R2",
          "label": "BCB 4.949",
          "detail": "Direitos do consumidor"
        },
        {
          "code": "R3",
          "label": "POL-CR-001",
          "detail": "Política interna"
        }
      ],
      "suporte": [
        {
          "code": "S1",
          "label": "TI / CRM",
          "detail": "Bitrix24 + integração bureau"
        },
        {
          "code": "S2",
          "label": "Mesa de Risco",
          "detail": "Régua de elegibilidade"
        }
      ]
    },
    {
      "id": "p5-2",
      "code": "P5.2",
      "name": "Análise de Crédito & Score",
      "purpose": "Avaliar capacidade de pagamento, garantias propostas e score interno; decidir por alçada ou escalar para Comitê de Crédito.",
      "cadence": "SLA 3-5 dias úteis · 1ª resposta em D+1",
      "owner": "Analista de Crédito · Mesa de Risco · Comitê",
      "sistemas": "Serasa Experian · SCR Bacen · Modelo M7 · DocuSign",
      "volume": "~ 480 análises / mês",
      "inputs": [
        {
          "what": "Lead qualificado verde/amarelo",
          "from": "P5.1 Originação",
          "detail": "Com pré-classificação"
        },
        {
          "what": "Documentos financeiros",
          "from": "Cliente",
          "detail": "IR, contracheque, faturamento 12m"
        },
        {
          "what": "Bureau Completo",
          "from": "Serasa · SPC · SCR Bacen",
          "detail": "Histórico + endividamento sistema"
        },
        {
          "what": "Política de Crédito + Manual",
          "from": "Mesa Risco · POL-CR-001/002",
          "detail": "Alçadas, taxas, prazos máx"
        }
      ],
      "outputs": [
        {
          "what": "Score M7 calculado",
          "to": "BI · P5.3 Estruturação",
          "detail": "Persistido em fact_score"
        },
        {
          "what": "Decisão aprovado/comitê/negado",
          "to": "P5.3 · Cliente",
          "detail": "Com justificativa formal"
        },
        {
          "what": "Limite e taxa propostos",
          "to": "P5.3 Estruturação",
          "detail": "CET, prazo, garantia, IOF"
        },
        {
          "what": "Parecer técnico assinado",
          "to": "Auditoria · DocuSign",
          "detail": "Trilha CVM/Anbima"
        }
      ],
      "etapas": [
        "Validar completude documental",
        "Consultar bureau completo + SCR",
        "Calcular score interno M7",
        "Avaliar comprometimento e garantias",
        "Submeter ao comitê se acima de alçada",
        "Emitir parecer + oferta"
      ],
      "regulacao": [
        {
          "code": "R1",
          "label": "Res. CMN 4.557",
          "detail": "Gestão de risco"
        },
        {
          "code": "R2",
          "label": "LGPD",
          "detail": "Tratamento dados financeiros"
        },
        {
          "code": "R3",
          "label": "Lei 4.595",
          "detail": "Sistema financeiro"
        },
        {
          "code": "R4",
          "label": "ANBIMA",
          "detail": "Autorregulação"
        }
      ],
      "suporte": [
        {
          "code": "S1",
          "label": "TI / Dados",
          "detail": "Pipeline bureau + modelo"
        },
        {
          "code": "S2",
          "label": "Comitê de Crédito",
          "detail": "Quinzenal (5ª)"
        },
        {
          "code": "S3",
          "label": "Compliance",
          "detail": "PEP / Sanctions / PLD"
        }
      ]
    },
    {
      "id": "p5-3",
      "code": "P5.3",
      "name": "Estruturação & Formalização",
      "purpose": "Modelar a operação (CCB, cota FIDC, consignação em folha), gerar contratos, coletar assinaturas e constituir garantias registradas.",
      "cadence": "SLA 2-3 dias úteis após decisão",
      "owner": "Backoffice Jurídico · Estruturação",
      "sistemas": "DocuSign · CETIP · Núclea · e-Notariado · FIDC Admin",
      "volume": "~ 320 operações / mês",
      "inputs": [
        {
          "what": "Decisão aprovada + oferta",
          "from": "P5.2 Análise",
          "detail": "Limite, taxa, prazo, garantias"
        },
        {
          "what": "Modelos contratuais",
          "from": "Jurídico · MOD-CR-XXX",
          "detail": "CCB, aditivos, fiança"
        },
        {
          "what": "Garantias / Avais ofertados",
          "from": "Cliente",
          "detail": "Imóvel, recebível, aval"
        },
        {
          "what": "Convênio consignante",
          "from": "Empregador / Órgão",
          "detail": "Quando consignado"
        }
      ],
      "outputs": [
        {
          "what": "CCB e contratos assinados",
          "to": "P5.4 Desembolso · Cliente",
          "detail": "DocuSign · trilha auditoria"
        },
        {
          "what": "Registro Núclea / CETIP",
          "to": "Órgãos · FIDC",
          "detail": "Lastro oficial"
        },
        {
          "what": "Operação contratada pronta",
          "to": "P5.4 Desembolso",
          "detail": "Para liberação"
        },
        {
          "what": "dim_operacao",
          "to": "BI · ClickHouse",
          "detail": "CDC ~5min"
        }
      ],
      "etapas": [
        "Modelar operação CCB / FIDC / Consig",
        "Gerar minuta a partir do modelo",
        "Constituir garantias avaliação + registro",
        "Coletar assinaturas digitais",
        "Registrar em Núclea, CETIP ou cartório",
        "Liberar para desembolso"
      ],
      "regulacao": [
        {
          "code": "R1",
          "label": "CVM 175",
          "detail": "FIDC"
        },
        {
          "code": "R2",
          "label": "Lei 10.820",
          "detail": "Consignado"
        },
        {
          "code": "R3",
          "label": "Lei 9.514",
          "detail": "Alienação fiduciária"
        },
        {
          "code": "R4",
          "label": "MP 2.200-2",
          "detail": "Assinatura ICP-Brasil"
        }
      ],
      "suporte": [
        {
          "code": "S1",
          "label": "Jurídico",
          "detail": "Curadoria contratual"
        },
        {
          "code": "S2",
          "label": "Cartório / e-Not.",
          "detail": "Registro garantias"
        },
        {
          "code": "S3",
          "label": "FIDC Admin",
          "detail": "Singulare · BRL"
        }
      ]
    },
    {
      "id": "p5-4",
      "code": "P5.4",
      "name": "Desembolso & Operação",
      "purpose": "Conferir a operação contratada, debitar o FIDC ou integrar com folha, liberar recurso ao cliente e contabilizar no fact do BI.",
      "cadence": "SLA D+1 do contrato assinado",
      "owner": "Mesa de Operações · Tesouraria",
      "sistemas": "FIDC Admin Singulare · API banco · PIX · Folha · ClickHouse",
      "volume": "~ R$ 4,8 MM desembolsado / mês",
      "inputs": [
        {
          "what": "Operação contratada com lastro",
          "from": "P5.3 Formalização",
          "detail": "Com lastro registrado"
        },
        {
          "what": "Saldo do FIDC disponível",
          "from": "FIDC Admin · Tesouraria",
          "detail": "Caixa + cotas"
        },
        {
          "what": "Convênio consignador ativo",
          "from": "Empregador",
          "detail": "Margem consignável"
        },
        {
          "what": "Dados bancários validados",
          "from": "Cliente",
          "detail": "Validados via DICT"
        }
      ],
      "outputs": [
        {
          "what": "TED / PIX ao cliente",
          "to": "Cliente",
          "detail": "Liquidação D+1"
        },
        {
          "what": "Cota FIDC emitida",
          "to": "Investidor FIDC",
          "detail": "Lastro contábil"
        },
        {
          "what": "fact_operacao_credito",
          "to": "BI · DRE Crédito",
          "detail": "Receita + custo de funding"
        },
        {
          "what": "Confirmação ao cliente",
          "to": "Cliente",
          "detail": "SMS + e-mail + Bitrix"
        }
      ],
      "etapas": [
        "Conferir documentação + lastro",
        "Reservar caixa do FIDC",
        "Disparar PIX/TED ou averbar em folha",
        "Conciliar bancário + FIDC",
        "Lançar no fact + DRE",
        "Notificar cliente e originador"
      ],
      "regulacao": [
        {
          "code": "R1",
          "label": "CVM 175",
          "detail": "FIDC · servicing"
        },
        {
          "code": "R2",
          "label": "CMN 4.595",
          "detail": "Compliance bancário"
        },
        {
          "code": "R3",
          "label": "Lei 9.613",
          "detail": "PLD/FT"
        }
      ],
      "suporte": [
        {
          "code": "S1",
          "label": "Tesouraria",
          "detail": "Reserva de caixa"
        },
        {
          "code": "S2",
          "label": "FIDC Admin",
          "detail": "Cotas + servicing"
        },
        {
          "code": "S3",
          "label": "TI / Dados",
          "detail": "Conciliação automática"
        }
      ]
    },
    {
      "id": "p5-5",
      "code": "P5.5",
      "name": "Monitoramento & Cobrança",
      "purpose": "Acompanhar carteira em produção, identificar atrasos, executar régua de cobrança e antecipar recuperação acionando garantias quando necessário.",
      "cadence": "Diário (D+0) · Relatório mensal",
      "owner": "Servicing · Cobrança · Recuperação",
      "sistemas": "ClickHouse · Régua automatizada · Núclea · Bitrix24 · Jurídico externo",
      "volume": "Carteira ativa ~ R$ 78 MM · 2.300 contratos",
      "inputs": [
        {
          "what": "Carteira em produção viva",
          "from": "P5.4 Desembolso",
          "detail": "Todos os contratos vivos"
        },
        {
          "what": "Movimento bancário / folha",
          "from": "Banco · Consignante",
          "detail": "Conciliação D+1"
        },
        {
          "what": "Régua de cobrança vigente",
          "from": "Mesa Risco · PLT-CB-002",
          "detail": "Cadência por faixa atraso"
        },
        {
          "what": "Garantias registradas",
          "from": "P5.3 Núclea · CETIP",
          "detail": "Para acionamento"
        }
      ],
      "outputs": [
        {
          "what": "NPL / Inadimplência reportada",
          "to": "Diretoria · Comitê Risco",
          "detail": "Diário + mensal"
        },
        {
          "what": "Acordos de renegociação",
          "to": "Cliente · P5.3",
          "detail": "Quando necessário aditivo"
        },
        {
          "what": "fact_inadimplencia",
          "to": "BI · provisão DRE",
          "detail": "Faixas 15/30/60/90+"
        },
        {
          "what": "Alerta de recovery",
          "to": "P5.3 · Jurídico",
          "detail": "Acionamento garantia"
        }
      ],
      "etapas": [
        "Conciliar pagamento D+1",
        "Identificar atrasos por faixa",
        "Disparar régua automatizada",
        "Escalar para cobrança amigável",
        "Acionar garantia / jurídico",
        "Lançar provisão + reportar NPL"
      ],
      "regulacao": [
        {
          "code": "R1",
          "label": "CVM 175",
          "detail": "Servicing FIDC"
        },
        {
          "code": "R2",
          "label": "CMN 4.966",
          "detail": "IFRS 9 perda esperada"
        },
        {
          "code": "R3",
          "label": "BCB 4.949",
          "detail": "Cobrança ética"
        },
        {
          "code": "R4",
          "label": "LGPD",
          "detail": "Contato + retenção"
        }
      ],
      "suporte": [
        {
          "code": "S1",
          "label": "TI / BI",
          "detail": "Régua + dashboards"
        },
        {
          "code": "S2",
          "label": "Jurídico Externo",
          "detail": "Cobrança judicial"
        },
        {
          "code": "S3",
          "label": "Tesouraria",
          "detail": "Provisão + reservas"
        }
      ]
    }
  ],
  "interfaces": [
    {
      "code": "P5.1",
      "message": "Cliente → M7: solicitação + dados básicos / M7 → Cliente: pré-aprovação ou recusa motivada"
    },
    {
      "code": "P5.2",
      "message": "Cliente → M7: documentos financeiros / M7 → Cliente: oferta com limite/taxa/prazo"
    },
    {
      "code": "P5.3",
      "message": "M7 → Cliente: minutas para assinar / Cliente → M7: CCB assinada + garantias"
    },
    {
      "code": "P5.4",
      "message": "M7 → Cliente: confirmação de desembolso / Cliente: recebe TED/PIX ou averbação"
    },
    {
      "code": "P5.5",
      "message": "M7 → Cliente: lembretes e cobrança / Cliente → M7: pagamento de parcelas"
    }
  ]
};
