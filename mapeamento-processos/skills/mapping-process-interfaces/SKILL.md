---
name: mapping-process-interfaces
description: >-
  Conduz entrevista estruturada para mapear interfaces de processo (DEIP/SIPOC).
  Itera com o usuario via AskUserQuestion para identificar outputs, inputs, suporte
  e regulacao, avaliar desconexoes e gerar DEIP descritivo (MD), tabela de
  desconexoes (Excel) e JSON v2 compativel com drawing-deip-diagrams.
  Use when the user wants to map process interfaces, build a DEIP from scratch,
  analyze process disconnections, or conduct a SIPOC-style workshop.

  <example>
  Context: User needs to map a business process from scratch
  user: "Preciso mapear as interfaces do processo de captacao de clientes PF"
  assistant: Inicia entrevista estruturada fase a fase, coleta interfaces via AskUserQuestion, avalia desconexoes e gera DEIP descritivo + tabela de desconexoes + JSON v2
  </example>

  <example>
  Context: User wants to analyze disconnections in an existing process
  user: "Quero identificar as desconexoes no processo de onboarding de assessores"
  assistant: Conduz entrevista para mapear interfaces atuais, avalia cada uma individualmente, classifica desconexoes por impacto e gera tabela Excel
  </example>
user-invocable: true
---

# Mapeamento de Interfaces de Processo (DEIP/SIPOC)

Conduz uma entrevista estruturada com o usuario para mapear todas as interfaces de um processo, avaliar desconexoes e gerar artefatos prontos para a skill `drawing-deip-diagrams`.

## Filosofia

> "Comece pelo que o processo entrega, depois descubra o que ele precisa."

A ordem de mapeamento e **Output-first** (nao segue a ordem do acronimo SIPOC/DEIP). Isso garante que o mapeamento seja orientado pelo **proposito do processo** — primeiro define-se o que precisa ser entregue, depois descobre-se o que e necessario para produzir.

## Dependencias

```
<this-skill>/
├── SKILL.md                              # Este arquivo
├── references/
│   ├── interview-guide.md                # Roteiro de entrevista com perguntas-sonda
│   └── disconnection-framework.md        # Framework de avaliacao de desconexoes
├── templates/
│   └── deip-descritivo.tmpl.md           # Template Markdown do DEIP descritivo
├── scripts/
│   └── generate-disconnection-table.py   # Gerador Excel (openpyxl)
└── assets/
    ├── m7-logo-dark.png                  # Logo para header Excel
    ├── m7-logo-offwhite.png
    └── m7-logo-favicon.png
```

## Artefatos de Saida

| Artefato | Formato | Consumidor |
|----------|---------|------------|
| DEIP JSON v2 | `.json` | Skill `drawing-deip-diagrams` (renderiza HTML visual) |
| DEIP Descritivo | `.md` | Documentacao do processo (leitura humana) |
| Tabela de Desconexoes | `.xlsx` | Analise de gaps e plano de acao |

**Pipeline**: `mapping-process-interfaces` → JSON v2 + MD + Excel → `drawing-deip-diagrams` → HTML visual

## Workflow

### Regras Gerais da Entrevista

1. **Uma pergunta por vez** — nunca sobrecarregar o usuario
2. **Sugerir quando possivel** — oferecer opcoes baseadas no contexto
3. **Usar `AskUserQuestion`** — para todas as interacoes estruturadas
4. **Inferir do contexto** — se o usuario ja forneceu informacao, nao perguntar de novo
5. **Validar antes de avancar** — confirmar dados coletados ao final de cada fase
6. **Manter progresso visivel** — usar `TodoWrite` para rastrear o andamento das fases

Para roteiro detalhado de perguntas, ver [interview-guide.md](references/interview-guide.md).

### Fase 1 — Identificar o Processo (N2)

Coletar metadados basicos do processo:

| Campo | Como coletar |
|-------|-------------|
| Nome do processo | Pergunta aberta |
| Codigo na cadeia de valor | Pergunta aberta (ex: "G2.3") |
| Responsavel | Pergunta aberta |
| Nivel BPM | `AskUserQuestion` com opcoes: N1 / N2 / N3 |
| Objetivo | Pergunta aberta: "Em uma frase, qual o proposito deste processo?" |

**Validacao**: Todos os campos preenchidos antes de avancar.

### Fase 2 — Mapear Saidas (Outputs) e Clientes

Comecar pelo output define o proposito do processo.

Para cada saida:
1. Perguntar: "O que este processo entrega? (documento, servico, informacao, decisao)"
2. Para cada saida identificada:
   - Nome e descricao breve
   - Cliente destinatario
   - Tipo do cliente: Interno / Externo / Regulador
3. Sugerir saidas com base no contexto e confirmar
4. Repetir ate: "O processo entrega mais algum produto/servico/informacao?"
5. Usuario confirma que mapeou todas as saidas

**Codificacao**: O1, O2, O3... (sequencial)

### Fase 3 — Mapear Entradas (Inputs) e Fornecedores

Orientar pelas saidas ja mapeadas.

Para cada entrada:
1. Perguntar orientado: "Para produzir [Output X], que insumos o processo precisa receber?"
2. Para cada entrada identificada:
   - Nome e descricao breve
   - Fornecedor de origem
   - Tipo do fornecedor: Interno / Externo / Sistema
3. Sugerir entradas implicitas (ex: se output e "contrato assinado", provavel input "documentos do cliente")
4. Repetir ate usuario confirmar que mapeou todas as entradas

**Codificacao**: I1, I2, I3... (sequencial)

### Fase 4 — Mapear Suporte

Identificar recursos necessarios para executar o processo.

Categorias a explorar:
- **Pessoas**: Equipe, headcount, perfis
- **Sistemas**: Softwares, plataformas, ferramentas
- **Equipamentos**: Hardware, maquinas, dispositivos
- **Infraestrutura**: Salas, redes, ambientes

Perguntar: "Quais recursos sao necessarios para que o processo funcione?"

**Codificacao**: S1, S2, S3... (sequencial)

### Fase 5 — Mapear Regulacao

Identificar documentos que regulam a transformacao.

Tipos a explorar:
- **Politica**: Politica interna da empresa
- **Norma**: Norma regulatoria do setor
- **Lei**: Legislacao aplicavel
- **Decreto**: Decreto governamental
- **POP**: Procedimento Operacional Padrao
- **Instrucao**: Instrucao de trabalho

Perguntar: "Quais leis, normas ou politicas internas regulam este processo?"

Se nenhuma identificada: registrar "Sem regulacao identificada" (status: neutral).

**Codificacao**: R1, R2, R3... (sequencial)

### Fase 6 — Construir Macrofluxo (N3)

Com inputs e outputs mapeados, construir as etapas de transformacao.

1. Apresentar ao usuario: "Dado que o processo recebe [lista de inputs] e deve entregar [lista de outputs], quais sao as etapas principais?"
2. Sugerir etapas com base no contexto
3. Validar cada etapa: formato verbo + complemento (ex: "Analisar documentacao", "Aprovar cadastro")
4. Limitar a **3-8 etapas** (regra DEIP de simplificacao; detalhe vai no BPMN)
5. Confirmar sequencia com usuario

### Fase 7 — Avaliar Interfaces e Identificar Desconexoes

Avaliar CADA interface individualmente usando `AskUserQuestion`.

**Ordem de avaliacao**: O1, O2... → I1, I2... → S1, S2... → R1, R2...

Para cada interface:

1. **Apresentar a interface** com contexto:
   > "Interface O1: o processo entrega [Saida] para [Cliente]. Esta interface esta funcionando adequadamente?"

2. **Perguntar status** via `AskUserQuestion`:
   - Conforme (funciona sem problemas)
   - Melhoria (ha oportunidade de melhoria)
   - Nao avaliado (sem informacao suficiente)

3. **Se melhoria**, seguir com:
   - Qual e a desconexao? (sugerir opcoes comuns — ver [disconnection-framework.md](references/disconnection-framework.md))
   - Qual o impacto? Alto / Medio / Baixo
   - Sugerir acao corretiva

**Sugestoes de desconexoes comuns** (oferecer como opcoes no AskUserQuestion):
- Handoff manual sujeito a erro
- Falta de POP/procedimento documentado
- Sistemas nao integrados
- SLA nao definido ou nao cumprido
- Retrabalho frequente
- Formato de entrega inadequado
- Informacao incompleta ou atrasada

### Fase 8 — Gerar Artefatos

Apos mapear e avaliar todas as interfaces:

**8.1 — Montar JSON v2**

Construir o JSON no formato v2 definido em `drawing-deip-diagrams/references/DEIP-STRUCTURE.md` secao 5. O JSON deve incluir:
- `metadata`: dados do processo
- `regulation`: array de regulacoes com status
- `suppliers`: array de fornecedores
- `inputs`: array de entradas com origin
- `macroflow`: array de etapas (strings)
- `outputs`: array de saidas com destination
- `customers`: array de clientes
- `support`: array de suportes
- `interfaces`: array completo com id, zone, provider/receiver, artifact, status, note

Salvar como `<nome-processo-kebab>-deip.json`.

**8.2 — Gerar DEIP Descritivo**

Usar o template em [deip-descritivo.tmpl.md](templates/deip-descritivo.tmpl.md) e preencher com os dados coletados.

Salvar como `<nome-processo-kebab>-deip-descritivo.md`.

**8.3 — Gerar Tabela de Desconexoes**

Preparar JSON de input para o script:

```json
{
  "metadata": { "processName": "", "code": "", "responsible": "", "level": "", "date": "", "version": "" },
  "interfaces": [ /* todas as interfaces com status e notes */ ],
  "disconnections": [
    { "id": "O1", "zone": "output", "item": "", "providerReceiver": "", "disconnection": "", "impact": "Alto|Medio|Baixo", "suggestedAction": "" }
  ]
}
```

Executar o script:

```bash
python <this-skill>/scripts/generate-disconnection-table.py \
  --input <nome-processo>-desconexoes-data.json \
  --output <nome-processo>-desconexoes.xlsx \
  --logo <this-skill>/assets/m7-logo-dark.png
```

**8.4 — Sugerir proximo passo**

> "O DEIP descritivo e a tabela de desconexoes foram gerados. Deseja gerar o DEIP visual HTML? Posso usar a skill `drawing-deip-diagrams` com o JSON v2 produzido."

## Validacao Pre-Geracao

Antes de gerar artefatos (Fase 8), verificar:

- [ ] Todas as 7 dimensoes preenchidas (regulacao pode ser "Sem regulacao identificada")
- [ ] Toda entrada tem fornecedor (coerencia input-supplier)
- [ ] Toda saida tem cliente (coerencia output-customer)
- [ ] Macrofluxo tem 3-8 etapas
- [ ] Interfaces com status melhoria tem observacao e impacto
- [ ] Sem itens duplicados
- [ ] Todas as interfaces codificadas (I/O/R/S + numero sequencial)

## Anti-Padroes

- **NAO pular fases** — seguir a ordem Output → Input → Suporte → Regulacao → Macrofluxo → Avaliacao
- **NAO gerar sem validar** — sempre confirmar dados com usuario antes da Fase 8
- **NAO misturar niveis** — DEIP e N2/N3; detalhe N4-N5 vai no BPMN
- **NAO forcar desconexoes** — se interface esta conforme, aceitar e seguir
- **NAO fazer mais de uma pergunta por vez** — entrevista, nao formulario
- **NAO inventar interfaces** — sugerir e esperar confirmacao do usuario

## Recursos Adicionais

- Para roteiro de entrevista detalhado: [interview-guide.md](references/interview-guide.md)
- Para framework de desconexoes: [disconnection-framework.md](references/disconnection-framework.md)
- Para template do DEIP descritivo: [deip-descritivo.tmpl.md](templates/deip-descritivo.tmpl.md)
- Para anatomia do DEIP e JSON schema: `drawing-deip-diagrams/references/DEIP-STRUCTURE.md`
