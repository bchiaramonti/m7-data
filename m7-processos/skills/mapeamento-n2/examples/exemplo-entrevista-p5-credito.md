# Entrevista N2 · Crédito (P5)

> **Data**: 2026-05-15 · **Entrevistador**: Claude (skill mapeamento-n2) · **Entrevistados**: Filipe Costa (Diretor Comercial Crédito), Maria Souza (Analista de Crédito Sênior)
> **N1 BRIEFING**: `../../mapeamento-m7/BRIEFING.md` · **Round**: 2 (final)

## Anexos consultados

- [x] Política `politica-m7.html` (cobre governança, aprovações, vigência)
- [x] Manual operacional `manual-credito-v3.pdf` (cobre fluxos detalhados P5.2 e P5.3)
- [ ] PE 2026 (não relevante para N2)

---

## Bloco 1 · Contexto N1

**Q1.1** Qual o `code` do processo primário?
**R1.1** P5

**Q1.2** Confirme name/owner/receita_meta/descricao do BRIEFING N1:
**R1.2**
- name: Crédito
- owner: **Diretor Comercial · Mesa Crédito** *(corrigido em checkpoint — entrevistado falou "Filipe Costa" mas regra exige cargo)*
- receita_meta: R$ 22,6 MM (confirmado pelo Filipe)
- descricao: FIDC Crédito, FIDC Serviços e Consignado privado/público (confirmado)

**Q1.3** Lede do N2:
**R1.3** O P5 Crédito é a vertical primária do grupo (FIDC Crédito, FIDC Serviços e Consignado), com originação multi-canal, gestão de risco end-to-end e maior contribuição de receita do portfólio. Este documento decompõe o P5 em 5 subprocessos, com BPMN end-to-end e SIPOC/DEIP por card.

**Q1.4** WBS · Janela · Status:
**R1.4** WBS=WBS 3.2 · Janela=12/05 → 30/05 · Status=Em produção

---

## Bloco 2 · Decomposição em subprocessos

**Q2.1** Quantos subprocessos compõem P5 end-to-end?
**R2.1** 5 subprocessos

**Q2.2** Liste:

| id | code | name | owner | cadence | sp_meta | sp_tech |
|---|---|---|---|---|---|---|
| p5-1 | P5.1 | Originação | Comercial Crédito · Originadores | D+0 contínuo | Multi-canal · pré-análise | Bitrix24 · Boa Vista · Quod |
| p5-2 | P5.2 | Análise & Score | Analista Crédito · Mesa Risco | SLA 3-5d | Underwriting · alçadas | Serasa · SCR Bacen · Modelo M7 |
| p5-3 | P5.3 | Estruturação & Formalização | Backoffice Jurídico | SLA 2-3d | Contratos · garantias | DocuSign · CETIP · Núclea |
| p5-4 | P5.4 | Desembolso & Operação | Mesa Operações · Tesouraria | SLA D+1 | Liberação · cota FIDC | FIDC Admin · PIX · Folha |
| p5-5 | P5.5 | Monitoramento & Cobrança | Servicing · Cobrança | Diário | NPL · régua · recovery | ClickHouse · Régua · Núclea |

**Q2.3** Mensagens cliente↔M7:

| code | message |
|---|---|
| P5.1 | Cliente → M7: solicitação + dados básicos / M7 → Cliente: pré-aprovação ou recusa motivada |
| P5.2 | Cliente → M7: documentos financeiros / M7 → Cliente: oferta com limite/taxa/prazo |
| P5.3 | M7 → Cliente: minutas para assinar / Cliente → M7: CCB assinada + garantias |
| P5.4 | M7 → Cliente: confirmação de desembolso / Cliente: recebe TED/PIX ou averbação |
| P5.5 | M7 → Cliente: lembretes e cobrança / Cliente → M7: pagamento de parcelas |

**Q2.4** Fronteiras fuzzy?
**R2.4** Inicialmente P5.2 e P5.3 tiveram debate sobre quem constitui as garantias (avaliar vs registrar). Decidido: P5.2 só **avalia** garantias propostas (entrada do parecer); P5.3 **constitui** (avalia + registra). Linha de corte: parecer aprovado vira insumo de P5.3.

---

## Bloco 3 · SIPOC por subprocesso

> Respondido principalmente por anexo `manual-credito-v3.pdf` §3-7 (5 fluxos detalhados). Anotamos abaixo só ajustes vs anexo.

### SIPOC · P5.1 — Originação
- Purpose: conforme anexo §3, validado.
- Owner: cargo "Comercial Crédito · Originadores" (anexo dizia só "Originadores" — ampliamos)
- inputs/outputs/etapas: extraídos do anexo §3 fluxograma
- regulacao: LGPD, BCB 4.949, POL-CR-001 (3 entradas, conforme anexo)
- suporte: TI/CRM, Mesa Risco

### SIPOC · P5.2 — Análise & Score
- Purpose: conforme anexo §4
- **Correção em checkpoint Round 1**: anexo dizia "fazer análise de crédito" — reformulado para "Avaliar capacidade de pagamento, garantias propostas e score interno" (verbo "fazer" não permitido)
- 4 entradas em regulacao porque setor FIDC exige citação CVM/ANBIMA

### SIPOC · P5.3 — Estruturação & Formalização
- Purpose: conforme anexo §5
- 4 regulações (CVM 175 obrigatório FIDC; Lei 10.820 consignado; Lei 9.514 alienação; MP 2.200-2 assinatura)
- e-Notariado entra só para imóveis (anexo)

### SIPOC · P5.4 — Desembolso & Operação
- Purpose: conforme anexo §6
- Volume R$ 4,8 MM/mês (Filipe atualizou número — anexo dizia R$ 3,5 MM, defasado)
- Tesouraria reserva caixa D-1 (Filipe explicou — não está no anexo)

### SIPOC · P5.5 — Monitoramento & Cobrança
- Purpose: conforme anexo §7
- Régua automatizada até 60d; após isso cobrança amigável humana (Maria)
- 4 regulações (CMN 4.966 IFRS 9 entrou em vigor)

---

## Bloco 4 · Jornada CX

> Respondido com base em NPS Q1-2026 + entrevistas com 12 clientes (Filipe trouxe).

### CX · P5.1
- Touchpoint: Site, indicação, RD, WhatsApp, Bitrix Landing
- Action: Procura solução, preenche cadastro, envia docs básicos
- MoT: intensity=3, items: "Primeira impressão de confiança", "Velocidade do retorno inicial"
- Pain: tone=-, items: "Cadastro demorado, querem dados demais", "Estou no escuro, ninguém me responde"

### CX · P5.2
- Touchpoint: WhatsApp, telefone, reunião, e-mail
- Action: Sobe docs, recebe parecer, negocia
- MoT: intensity=3, items: "Recebe parecer aprovado ou negado", "Vê taxa, CET e prazo"
- Pain: tone=-, items: "Já mandei tudo, por que demora tanto?", "A taxa é maior do que eu esperava"

### CX · P5.3
- Touchpoint: e-mail jurídico, portal, DocuSign, e-Notariado
- Action: Lê minuta, valida garantias, assina
- MoT: intensity=2, items: "Clica em Assinar — vínculo formal"
- Pain: tone=~, items: "Contrato cheio de cláusulas, não entendo", "Estou assinando uma dívida — sem volta"

### CX · P5.4
- Touchpoint: Conta bancária, app banco, SMS
- Action: Confere crédito, usa recurso
- MoT: intensity=3, items: "Dinheiro disponível na conta"
- Pain: tone=+, items: "Caiu o dinheiro! Funcionou"

### CX · P5.5
- Touchpoint: WhatsApp, boleto, app banco, carta, jurídico
- Action: Paga parcelas, renegocia, encerra
- MoT: intensity=3, items: "1ª parcela vence — compromisso real", "Quitação celebrada ou cobrança recebida"
- Pain: tone=-, items: "Cuidado para não furar o orçamento", "Atrasei um dia e já me ligaram pressionando"

---

## Bloco 5 · Data Lake

> Maria liderou. Estrutura de marts vem da arquitetura ClickHouse aprovada.

### Data · P5.1
- Systems: Site M7, Bitrix24 CRM, RD Station, Receita WS, Boa Vista, Quod
- Dados: lead_origem (Bitrix dim_lead, CRM), cliente_pf/pj (dim_cliente, PII), score_bureau (dim_lead_credito, Score), restritivos (dim_lead_credito, Bureau)

### Data · P5.2
- Systems: Serasa Experian, SCR Bacen, Modelo Score M7, DocuSign
- Dados: docs_financ (GED S3, Doc), score_M7 (fact_score, Score), parecer_tecnico (DocuSign trilha, Doc)

### Data · P5.3
- Systems: Modelos jurídicos, GED interno, DocuSign, CETIP, Núclea, e-Notariado
- Dados: CCB assinada (S3 contratos, Contrato), registro_lastro (CETIP/Núclea, Lastro)

### Data · P5.4
- Systems: FIDC Admin (Singulare), PIX/TED API, Folha consignado, ClickHouse
- Dados: movimento_caixa (FIDC ledger, Tesouraria), fact_operacao (fact_operacao_credito, KPI)

### Data · P5.5
- Systems: Régua automatizada, Banco/Consignante, ClickHouse, Núclea (baixa), Jurídico externo
- Dados: acordos (Bitrix cobranca, Cobranca), fact_npl (fact_inadimplencia, KPI)

### Marts globais
- dim: dim_lead_credito, dim_cliente, dim_oferta, dim_operacao, dim_garantia (5)
- fact: fact_score, fact_desembolso, fact_operacao_credito, fact_pagamento, fact_inadimplencia, fact_provisao (6)

### Consumers globais
- BI, Operação, Risco, Regulatório, Tesouraria, Auditoria (6 tiers)

---

## Notas livres da entrevista

- Filipe enfatizou que **comunicação em P5.2** é o maior gap: cliente fica 2-3 dias sem retorno enquanto análise acontece. Sugere régua de touchpoint mesmo no "silêncio".
- Maria comentou que **fact_provisao** ainda não está em produção; depende do projeto IFRS 9 que termina em Jul/26. Mantemos no SSOT pois o Data Lake é o estado-alvo.

---

## Validação final · n2-interview-critic

> Round 1 (2026-05-13): 3 bloqueadores e 4 avisos
> - OWNER-PESSOA em Bloco 1 R1.2 ("Filipe Costa")
> - VERB-GENERIC em SIPOC P5.2 ("fazer análise")
> - PAIN-CORPORATIVO em CX P5.1 ("Cliente expressa frustração com latência")
> + 4 avisos sobre details ausentes

> Round 2 (2026-05-15): 0 bloqueadores, 1 aviso restante
> - DATALAKE-MARTS-CONSUMERS-ORFAOS: fact_provisao não tem consumer correspondente claramente.
>   → Aceito com rationale: fact_provisao serve "Risco" (IFRS 9). Adicionado em Risco tier.
> Veredicto: pronto para Fase B.
