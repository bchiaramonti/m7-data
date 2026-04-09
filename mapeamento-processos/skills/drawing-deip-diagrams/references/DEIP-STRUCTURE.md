# Anatomia do DEIP — Diagrama de Escopo, Interface e Processos

Referencia estrutural para a skill `drawing-deip-diagrams`.
Fonte: BPM CBOK 3.0, gestao-de-processos-book.md secao 5.4, DEIP.pdf (SIURB/PROJ SP).

---

## 1. O que e o DEIP

O DEIP representa a **visao geral de um processo** e define seu escopo, interfaces e relacionamentos. E o primeiro artefato a ser construido antes da modelagem BPMN detalhada.

> Um DEIP responde: "Quem fornece o que, para qual processo, que entrega o que, para quem, sob quais regras e com quais recursos?"

---

## 2. Estrutura Visual Canonica (v2)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  HEADER: Nome do processo + Codigo + Responsavel + Nivel + Versao + Data │
├──────────────────────────────────────────────────────────────────────────┤
│  REGULACAO   [R1●] Doc1   [R2●] Doc2   [R3●] Doc3                       │
├──┬───────────────────┬──────────────────────────┬──────────────────┬─────┤
│  │ Fornecedor  # Insumo │                        │ Produto # Cliente │    │
│E │                       │  ┌─────────────────┐  │                   │ S  │
│N │ Marketing  [I1] Lead  │  │ Processo: G2.3  │  │ Cadastro [O1] GC │ A  │
│T │ Cliente    [I2] Docs  │  │                 │  │ Ficha    [O2] CO │ I  │
│R │ Parceiro   [I3] Indic │  │ ▶S1 ▶S2 ▶S3 ▶  │  │ Contrato [O3] JU │ D  │
│A │                       │  │                 │  │                   │ A  │
│D │                       │  └─────────────────┘  │                   │ S  │
│A │                       │                        │                   │    │
│S │                       │                        │                   │    │
├──┴───────────────────┴──────────────────────────┴──────────────────┴─────┤
│  SUPORTE   [S1●] Equipe   [S2●] CRM   [S3●] Plataforma                  │
├──────────────────────────────────────────────────────────────────────────┤
│  LEGENDA:  ● Conforme  ● Melhoria  ● Neutro                             │
└──────────────────────────────────────────────────────────────────────────┘
```

**Diferenciais do v2**:
- **Interfaces codificadas**: Cada interface tem um ID com prefixo de zona (I1, O1, R1, S1)
- **Pares visuais**: Fornecedor→[In]→Insumo e Produto→[On]→Cliente mostrados na mesma linha
- **Macrofluxo chevron**: Etapas como setas horizontais (chevron) no centro
- **Pagina unica**: Layout compacto que cabe em A4 landscape sem scroll

---

## 3. As 7+1+1 Dimensoes do DEIP

### 3.0 Metadata (Header)

| Campo | Descricao | Exemplo |
|-------|-----------|---------|
| Nome do processo | Identificacao unica | "Captacao de Clientes PF" |
| Codigo | Referencia na cadeia de valor | "G2.3" |
| Responsavel | Dono do processo | "Gerencia Comercial" |
| Data | Data da versao | "2026-02-27" |
| Nivel BPM | N1, N2, N3, N4 ou N5 | "N2 — Subprocesso" |
| Versao | Numero da versao | "1.0" |

### 3.1 Regulacao (faixa superior)

**O que e**: Documentos que regulam a transformacao — politicas, leis, normas, decretos, procedimentos internos que o processo deve obedecer.

| Campo | Descricao |
|-------|-----------|
| Nome | Identificacao da regulacao (ex: "Lei 8.658/77") |
| Tipo | Politica, Norma, Lei, Decreto, POP, Instrucao |
| Status | `conforme` (🟢) ou `melhoria` (🔴) |
| Observacao | Nota sobre a interface (ex: "Prazo de resposta nao atendido") |

**Sinalizacao por cores** (diferencial do modelo):
- **🟢 Verde** (`conforme`): Interface atendida, sem gaps
- **🔴 Vermelho** (`melhoria`): Interface com oportunidade de melhoria identificada
- **⚪ Cinza** (`neutral`): Status nao avaliado explicitamente

### 3.2 Fornecedores (coluna esquerda)

**O que e**: Quem entrega insumos para o processo — areas internas, clientes, parceiros, sistemas.

| Campo | Descricao |
|-------|-----------|
| Nome | Identificacao do fornecedor |
| Tipo | Interno, Externo, Sistema |
| Status | `conforme` ou `melhoria` (opcional) |

### 3.3 Entradas / Insumos (segunda coluna)

**O que e**: O que entra no processo — informacoes, documentos, materiais, dados, gatilhos.

| Campo | Descricao |
|-------|-----------|
| Nome | Identificacao da entrada |
| Descricao | Detalhamento (opcional) |
| Origem | Qual fornecedor entrega |
| Status | `conforme` ou `melhoria` (opcional) |

### 3.4 Macrofluxo (coluna central)

**O que e**: Os passos principais do processo em sequencia simplificada (nao e BPMN completo).

| Campo | Descricao |
|-------|-----------|
| Etapas | Lista ordenada de passos principais |
| Sequencia | Ordem de execucao (chevrons horizontais ▶) |

**Regra**: O macrofluxo no DEIP deve ser **simplificado** — apenas 3 a 8 etapas principais. O detalhamento completo vai no fluxograma BPMN.

### 3.5 Saidas / Produtos (quarta coluna)

**O que e**: O que o processo entrega — documentos, servicos, informacoes, decisoes.

| Campo | Descricao |
|-------|-----------|
| Nome | Identificacao da saida |
| Descricao | Detalhamento (opcional) |
| Destino | Qual cliente recebe |
| Status | `conforme` ou `melhoria` (opcional) |

### 3.6 Clientes (coluna direita)

**O que e**: Quem recebe as saidas do processo — areas internas, clientes finais, reguladores.

| Campo | Descricao |
|-------|-----------|
| Nome | Identificacao do cliente |
| Tipo | Interno, Externo, Regulador |
| Status | `conforme` ou `melhoria` (opcional) |

### 3.7 Suporte (faixa inferior)

**O que e**: Recursos necessarios para executar o processo — pessoas, sistemas, equipamentos, infraestrutura.

| Campo | Descricao |
|-------|-----------|
| Nome | Identificacao do recurso |
| Tipo | Pessoas, Sistemas, Equipamentos, Infraestrutura |
| Detalhamento | Quantidade, especificacao (opcional) |

### 3.8 Interfaces (codificacao — v2)

**O que e**: Cada ponto de conexao entre o processo e uma entidade externa (fornecedor, cliente, regulacao, suporte) e uma **interface**. Interfaces sao codificadas com prefixo de zona para facilitar o mapeamento de desconexoes.

| Prefixo | Zona | Significado |
|---------|------|-------------|
| **I** | input | Conexao fornecedor → entrada |
| **O** | output | Conexao saida → cliente |
| **R** | regulation | Regulacao que governa o processo |
| **S** | support | Recurso de suporte ao processo |

**Cada interface tem**:

| Campo | Descricao |
|-------|-----------|
| id | Codigo unico (ex: I1, O3, R2, S1) |
| zone | input, output, regulation, support |
| provider | Quem fornece (para inputs/regulation/support) |
| artifact | O que e fornecido/entregue |
| receiver | Quem recebe (para outputs) |
| status | conforme, melhoria, neutral |
| note | Observacao sobre a desconexao (obrigatorio se melhoria) |

**Regra de numeracao**: Sequencial dentro de cada zona (I1, I2, I3... / O1, O2, O3... / R1, R2... / S1, S2...).

---

## 4. Regras de Preenchimento

1. **Completude**: Todas as 7 dimensoes devem ser preenchidas. Se nao ha regulacao, explicitar "Sem regulacao identificada"
2. **Coerencia**: Toda entrada deve ter um fornecedor. Toda saida deve ter um cliente
3. **Simplificacao**: Macrofluxo com 3-8 etapas. Detalhamento vai no BPMN
4. **Status**: Sinalizar interfaces criticas com 🔴 e incluir observacao
5. **Granularidade**: O DEIP segue o nivel BPM do processo. N1-N2 = visao macro; N3+ = mais detalhado
6. **Unicidade**: Cada item aparece uma unica vez na dimensao correspondente
7. **Codificacao**: Toda interface deve receber um codigo (I/O/R/S + numero sequencial)

---

## 5. JSON Schema de Input

O template aceita dois formatos. O formato **v2 (recomendado)** inclui o array `interfaces`. O formato **v1 (legado)** usa arrays separados e o motor gera interfaces automaticamente.

### Formato v2 (recomendado)

```json
{
  "metadata": {
    "processName": "Captacao de Clientes PF",
    "code": "G2.3",
    "responsible": "Gerencia Comercial",
    "date": "2026-02-27",
    "level": "N2",
    "version": "1.0"
  },
  "regulation": [
    { "name": "Politica Comercial POL-COM-001", "type": "Politica", "status": "conforme", "note": "" },
    { "name": "Resolucao CVM 175", "type": "Norma", "status": "melhoria", "note": "Formulario de suitability nao cobre todos os perfis" }
  ],
  "suppliers": [
    { "name": "Marketing Digital", "type": "Interno", "status": "conforme" },
    { "name": "Cliente prospect", "type": "Externo" }
  ],
  "inputs": [
    { "name": "Lead qualificado", "description": "Lead com scoring >= 70", "origin": "Marketing Digital", "status": "conforme" },
    { "name": "Documentos pessoais", "origin": "Cliente prospect" }
  ],
  "macroflow": [
    "Receber lead",
    "Qualificar prospect",
    "Realizar reuniao",
    "Enviar proposta",
    "Formalizar cadastro"
  ],
  "outputs": [
    { "name": "Cliente cadastrado", "destination": "Gestao de Carteira", "status": "conforme" },
    { "name": "Ficha cadastral", "destination": "Compliance" }
  ],
  "customers": [
    { "name": "Gestao de Carteira", "type": "Interno", "status": "conforme" },
    { "name": "Compliance", "type": "Interno" },
    { "name": "Cliente PF", "type": "Externo" }
  ],
  "support": [
    { "name": "Equipe Comercial (8 assessores)", "type": "Pessoas" },
    { "name": "CRM Salesforce", "type": "Sistemas" }
  ],
  "interfaces": [
    { "id": "I1", "zone": "input", "provider": "Marketing Digital", "providerType": "Interno", "artifact": "Lead qualificado", "artifactDetail": "Lead com scoring >= 70", "status": "conforme", "note": "" },
    { "id": "I2", "zone": "input", "provider": "Cliente prospect", "providerType": "Externo", "artifact": "Documentos pessoais", "artifactDetail": "", "status": "neutral", "note": "" },
    { "id": "O1", "zone": "output", "artifact": "Cliente cadastrado", "artifactDetail": "", "receiver": "Gestao de Carteira", "receiverType": "Interno", "status": "conforme", "note": "" },
    { "id": "O2", "zone": "output", "artifact": "Ficha cadastral", "artifactDetail": "", "receiver": "Compliance", "receiverType": "Interno", "status": "neutral", "note": "" },
    { "id": "R1", "zone": "regulation", "artifact": "Politica Comercial POL-COM-001", "artifactType": "Politica", "status": "conforme", "note": "" },
    { "id": "R2", "zone": "regulation", "artifact": "Resolucao CVM 175", "artifactType": "Norma", "status": "melhoria", "note": "Formulario de suitability nao cobre todos os perfis" },
    { "id": "S1", "zone": "support", "artifact": "Equipe Comercial (8 assessores)", "artifactType": "Pessoas", "status": "neutral", "note": "" },
    { "id": "S2", "zone": "support", "artifact": "CRM Salesforce", "artifactType": "Sistemas", "status": "neutral", "note": "" }
  ]
}
```

### Formato v1 (legado — compativel)

O mesmo JSON **sem** o campo `interfaces`. O motor de renderizacao gera interfaces automaticamente:
- Inputs: pareia `input.origin` com `supplier.name` → I1, I2, ...
- Outputs: pareia `output.destination` com `customer.name` → O1, O2, ...
- Regulations: R1, R2, ... (sequencial)
- Support: S1, S2, ... (sequencial)

---

## 6. Referencia Visual: DEIP SIURB/PROJ (Prefeitura de SP)

O modelo de referencia do DEIP.pdf da Prefeitura de SP apresenta:

```
┌─────────────────────────────────────────────────────────────────┐
│  SIURB/PROJ — Melhoramentos Viarios                              │
│  Responsavel: PROJ G | Data: [data]                              │
├─────────────────────────────────────────────────────────────────┤
│  REGULACAO                                                       │
│  [Lei 8.658/77 🟢] [Lei 14.141/06 🟢] [Decreto 32.329/92 🔴]  │
├────────┬────────┬──────────────────────────┬────────┬───────────┤
│FORNEC. │INSUMO  │  Receber → Analisar →    │Parecer │SEHAB      │
│SEHAB   │Alvaras │  Verificar → Emitir      │Comuni- │Interessado│
│PARSOLO │Pedido  │                          │quesce  │           │
│Interes.│Diretr. │                          │Diretr. │           │
├────────┴────────┴──────────────────────────┴────────┴───────────┤
│  SUPORTE                                                         │
│  PROJ G (17 pessoas) | Levant. topograficos | SIMPROC           │
│  PROJ 1-4, 004 | SNJ/DESAP | Subprefeitura                     │
└─────────────────────────────────────────────────────────────────┘
```

**Diferenciais desse modelo**:
- Sinalizacao por cores nas interfaces regulatorias
- Layout tabular claro (5 colunas x 3 faixas)
- Macrofluxo simplificado (4 passos)
- Suporte com detalhamento de headcount

## 7. Referencia Visual: DEIP Votorantim Cimentos (Aquila)

O modelo de referencia da Votorantim Cimentos/Grupo Aquila apresenta:

**Diferenciais desse modelo**:
- Interfaces numeradas com circulos coloridos (verde=conforme, vermelho=nao conforme)
- Pares visuais explícitos: fornecedor → [circulo numerado] → entrada
- Macrofluxo como chevrons (setas horizontais) no centro
- Layout em pagina unica (A4 landscape)
- Codificacao para mapeamento de desconexoes futuro
