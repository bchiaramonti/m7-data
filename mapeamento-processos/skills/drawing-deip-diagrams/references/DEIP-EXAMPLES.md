# Inventario de DEIPs Existentes

Catalogo dos Diagramas DEIP disponiveis no vault para referencia e validacao.
Organizados por projeto/contexto.

---

## 1. DEIP de Referencia Metodologica

| Arquivo | Contexto | Localizacao |
|---------|----------|-------------|
| `DEIP.pdf` | Exemplo INDG — Prefeitura SP (SIURB/PROJ Melhoramentos Viarios) | `4-archives/` |
| `Diagrama DEIP.pptx` | Template generico processos financeiros | `4-archives/` |
| `01_OSA_DEIP.pptx` | Referencia OSA | `4-archives/` |

---

## 2. Projeto EVA — Blue Trade (Onda 1 - Processos)

DEIPs completos para 8 processos do projeto de transformacao EVA:

| Processo | Arquivo | Path |
|----------|---------|------|
| Captacao | `DEIP - Processo Captação.pptx` | `4-archives/projetos/blue3/1-gestao-bt/3-projetos/01-eva/` |
| Manutencao de Carteira | `DEIP - Processo de Manutenção de Carteira.pptx` | idem |
| Retencao de Resgate | `DEIP - Processo de Retenção de Resgate.pptx` | idem |
| Ativacao (Captacao Digital) | `DEIP - Processo Ativação.pptx` | idem |
| Seguros | `DEIP - Processo Seguros.pptx` | idem |
| Credito | `DEIP - Processo Crédito.pptx` | idem |
| Geracao de Leads | `DEIP - Processo Geração Leads.pptx` | idem |
| Comissionamento | `DEIP - Processo Comissionamento.pptx` | idem |

**Caracteristicas dos DEIPs EVA**:
- Formato PowerPoint (1 slide = 1 DEIP)
- Layout tabular com 5 colunas (Fornecedores / Entradas / Macrofluxo / Saidas / Clientes)
- Faixa superior com regulacao
- Faixa inferior com suporte
- Sinalizacao por cores nas interfaces

---

## 3. Outros Modelos

| Arquivo | Contexto | Formato |
|---------|----------|---------|
| `DEIP_Primavera_v2.pptx` | Modelo Primavera | PPTX |
| `DEIP_Modelo&Flash.pptx` | Modelo & Flash | PPTX |
| `DEIP_Rota de venda_novo.xlsx` | Rota de Venda | Excel |
| `DEIP_Promoção_novo.xlsx` | Promocao | Excel |
| `DEIP_Venda_novo.xlsx` | Venda | Excel |
| `20151003_DEIP - Sub 1,2,3 e 4.pptx` | Metro Rio — Suprimentos | PPTX |

---

## 4. Materiais de Apoio (Metodologia)

| Arquivo | Contexto | Path |
|---------|----------|------|
| `DEIP.xlsx` | Exercicio 3 — ROP Teorico (Apoio) | `3-resources/metodologias/solucoes/rop-teor-material-apoio-2011-08/analises-exercicio-3/` |
| `ROP Teorico_Apoio Cap3_Analise horizontal (processo)_DEIP_PGP_OM_ESTR.xlsx` | Analise horizontal de processos | idem cap-3-pdca |

---

## 5. Padroes Observados nos DEIPs Existentes

### Layout

- **5 colunas centrais**: Fornecedores | Entradas | Macrofluxo | Saidas | Clientes
- **3 faixas horizontais**: Regulacao (topo) | Central (5 colunas) | Suporte (base)
- **Header**: Nome do processo + Responsavel + Data

### Sinalizacao

- 🟢 **Verde** = Interface conforme (atende requisitos)
- 🔴 **Vermelho** = Oportunidade de melhoria (gap identificado)
- Cores aplicadas nas regulacoes e opcionalmente nos fornecedores/clientes

### Macrofluxo

- Simplificado: 3 a 8 etapas
- Representado como boxes com setas (→)
- Nao usa notacao BPMN completa — apenas sequencia linear

### Granularidade

- DEIPs de nivel N1-N2: poucos itens, visao macro
- DEIPs de nivel N3+: mais itens, detalhamento operacional
- Processos EVA: nivel N2 com 4-6 etapas no macrofluxo
