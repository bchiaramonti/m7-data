/* journey/data file gerado por mapeamento-n2. NAO editar manualmente. */

/* === BLOCK:P5_JOURNEY === */
window.P5_JOURNEY = {
  "processos": [
    {
      "code": "P5.1",
      "name": "Originação",
      "owner": "Comercial · Mesa Crédito",
      "cadence": "D+0 contínuo",
      "tone": "a"
    },
    {
      "code": "P5.2",
      "name": "Análise",
      "owner": "Analista · Risco",
      "cadence": "SLA 3-5d",
      "tone": "b"
    },
    {
      "code": "P5.3",
      "name": "Formalização",
      "owner": "Jurídico · BO",
      "cadence": "SLA 2-3d",
      "tone": "c"
    },
    {
      "code": "P5.4",
      "name": "Desembolso",
      "owner": "Mesa Ops · Tesouraria",
      "cadence": "SLA D+1",
      "tone": "d"
    },
    {
      "code": "P5.5",
      "name": "Monitoramento",
      "owner": "Servicing · Cobrança",
      "cadence": "Diário",
      "tone": "e"
    }
  ],
  "rows": [
    {
      "id": "touchpoint",
      "label": "Canal / Touchpoint",
      "sublabel": "onde o cliente está",
      "cells": [
        "Site M7 · Indicação · RD Marketing · WhatsApp · Bitrix Landing",
        "WhatsApp · Telefone · Reunião remota · E-mail",
        "E-mail jurídico · Portal cliente · DocuSign · e-Notariado",
        "Conta bancária · App do banco · SMS de confirmação",
        "WhatsApp · Boleto · App banco · Carta · Jurídico"
      ]
    },
    {
      "id": "action",
      "label": "Ação do cliente",
      "sublabel": "frontstage",
      "cells": [
        "Procura solução de capital, preenche cadastro e envia documentos básicos",
        "Sobe documentos financeiros, recebe parecer, avalia e negocia condições",
        "Lê a minuta, valida garantias e assina CCB + aditivos digitalmente",
        "Confere o crédito na conta e usa o recurso para a finalidade pactuada",
        "Paga parcelas via boleto/débito/folha, renegocia ou encerra a operação"
      ]
    },
    {
      "id": "mot",
      "label": "Momentos da Verdade",
      "sublabel": "inflexão emocional",
      "cells": [
        {
          "intensity": 3,
          "items": [
            "Primeira impressão de confiança",
            "Velocidade do retorno inicial"
          ]
        },
        {
          "intensity": 3,
          "items": [
            "Recebe parecer aprovado ou negado",
            "Vê taxa, CET e prazo"
          ]
        },
        {
          "intensity": 2,
          "items": [
            "Clica em Assinar — vínculo formal"
          ]
        },
        {
          "intensity": 3,
          "items": [
            "Dinheiro disponível na conta"
          ]
        },
        {
          "intensity": 3,
          "items": [
            "1ª parcela vence — compromisso real",
            "Quitação celebrada ou cobrança recebida"
          ]
        }
      ]
    },
    {
      "id": "pain",
      "label": "Pain points · sentimento",
      "sublabel": "tom: − negativo · ~ neutro · + positivo",
      "cells": [
        {
          "tone": "-",
          "items": [
            "\"Cadastro demorado, querem dados demais\"",
            "\"Estou no escuro, ninguém me responde\""
          ]
        },
        {
          "tone": "-",
          "items": [
            "\"Já mandei tudo, por que demora tanto?\"",
            "\"A taxa é maior do que eu esperava\""
          ]
        },
        {
          "tone": "~",
          "items": [
            "\"Contrato cheio de cláusulas, não entendo\"",
            "\"Estou assinando uma dívida — sem volta\""
          ]
        },
        {
          "tone": "+",
          "items": [
            "\"Caiu o dinheiro! Funcionou\""
          ]
        },
        {
          "tone": "-",
          "items": [
            "\"Cuidado para não furar o orçamento\"",
            "\"Atrasei um dia e já me ligaram pressionando\""
          ]
        }
      ]
    }
  ]
};
/* === ENDBLOCK:P5_JOURNEY === */

/* === BLOCK:P5_DATALAKE === */
window.P5_DATALAKE = {
  "processos": [
    {
      "code": "P5.1",
      "name": "Originação",
      "owner": "Comercial · Mesa Crédito",
      "cadence": "D+0 contínuo",
      "tone": "a"
    },
    {
      "code": "P5.2",
      "name": "Análise",
      "owner": "Analista · Risco",
      "cadence": "SLA 3-5d",
      "tone": "b"
    },
    {
      "code": "P5.3",
      "name": "Formalização",
      "owner": "Jurídico · BO",
      "cadence": "SLA 2-3d",
      "tone": "c"
    },
    {
      "code": "P5.4",
      "name": "Desembolso",
      "owner": "Mesa Ops · Tesouraria",
      "cadence": "SLA D+1",
      "tone": "d"
    },
    {
      "code": "P5.5",
      "name": "Monitoramento",
      "owner": "Servicing · Cobrança",
      "cadence": "Diário",
      "tone": "e"
    }
  ],
  "rows": [
    {
      "id": "systems",
      "label": "Sistemas / fontes",
      "sublabel": "backstage · ferramentas",
      "cells": [
        [
          "Site M7",
          "Bitrix24 CRM",
          "RD Station",
          "Receita WS",
          "Boa Vista",
          "Quod"
        ],
        [
          "Serasa Experian",
          "SCR Bacen",
          "Modelo Score M7",
          "DocuSign"
        ],
        [
          "Modelos jurídicos",
          "GED interno",
          "DocuSign",
          "CETIP",
          "Núclea",
          "e-Notariado"
        ],
        [
          "FIDC Admin (Singulare)",
          "PIX/TED API",
          "Folha consignado",
          "ClickHouse"
        ],
        [
          "Régua automatizada",
          "Banco · Consignante",
          "ClickHouse",
          "Núclea (baixa)",
          "Jurídico externo"
        ]
      ]
    },
    {
      "id": "data",
      "label": "Dado armazenado",
      "sublabel": "persistência · marts",
      "cells": [
        [
          {
            "name": "lead_origem",
            "where": "Bitrix · dim_lead",
            "kind": "CRM"
          },
          {
            "name": "cliente_pf/pj",
            "where": "Bitrix · dim_cliente",
            "kind": "PII"
          },
          {
            "name": "score_bureau",
            "where": "ClickHouse · dim_lead_credito",
            "kind": "Score"
          },
          {
            "name": "restritivos",
            "where": "ClickHouse · dim_lead_credito",
            "kind": "Bureau"
          }
        ],
        [
          {
            "name": "docs_financ",
            "where": "GED · S3 buckets",
            "kind": "Doc"
          },
          {
            "name": "score_M7",
            "where": "ClickHouse · fact_score",
            "kind": "Score"
          },
          {
            "name": "parecer_tecnico",
            "where": "DocuSign · trilha",
            "kind": "Doc"
          }
        ],
        [
          {
            "name": "CCB assinada",
            "where": "DocuSign · S3 contratos",
            "kind": "Contrato"
          },
          {
            "name": "registro_lastro",
            "where": "CETIP · Núclea",
            "kind": "Lastro"
          }
        ],
        [
          {
            "name": "movimento_caixa",
            "where": "FIDC Admin · ledger",
            "kind": "Tesouraria"
          },
          {
            "name": "fact_operacao",
            "where": "ClickHouse · fact_operacao_credito",
            "kind": "KPI"
          }
        ],
        [
          {
            "name": "acordos",
            "where": "Bitrix · cobranca",
            "kind": "Cobranca"
          },
          {
            "name": "fact_npl",
            "where": "ClickHouse · fact_inadimplencia",
            "kind": "KPI"
          }
        ]
      ]
    }
  ],
  "marts": {
    "dim": [
      {
        "name": "dim_lead_credito",
        "source": "Bitrix CRM + bureau"
      },
      {
        "name": "dim_cliente",
        "source": "Onboarding + KYC"
      },
      {
        "name": "dim_oferta",
        "source": "Score + política"
      },
      {
        "name": "dim_operacao",
        "source": "P5.3 Formalização"
      },
      {
        "name": "dim_garantia",
        "source": "P5.3 + Núclea/CETIP"
      }
    ],
    "fact": [
      {
        "name": "fact_score",
        "description": "Score M7 calculado por lead/oferta"
      },
      {
        "name": "fact_desembolso",
        "description": "Liberações PIX/TED/folha"
      },
      {
        "name": "fact_operacao_credito",
        "description": "Desembolso, taxa, prazo, garantia"
      },
      {
        "name": "fact_pagamento",
        "description": "Parcelas recebidas D+1"
      },
      {
        "name": "fact_inadimplencia",
        "description": "NPL por faixa 15/30/60/90+"
      },
      {
        "name": "fact_provisao",
        "description": "IFRS 9 perda esperada"
      }
    ]
  },
  "consumers": [
    {
      "tier": "BI",
      "description": "Dashboards de captação, NPL, DRE Crédito, score por safra"
    },
    {
      "tier": "Operação",
      "description": "Mesa de Crédito + Servicing (decisões D+0)"
    },
    {
      "tier": "Risco",
      "description": "Comitê + estresse + provisão IFRS 9"
    },
    {
      "tier": "Regulatório",
      "description": "Reportes CVM, Bacen, ANBIMA, FIDC monthly"
    },
    {
      "tier": "Tesouraria",
      "description": "Reserva de caixa, cotas FIDC, projeção fluxo"
    },
    {
      "tier": "Auditoria",
      "description": "Trilha contratual, parecer técnico, conciliação"
    }
  ]
};
/* === ENDBLOCK:P5_DATALAKE === */
