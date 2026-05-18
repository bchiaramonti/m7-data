---
name: creating-manual
description: >
  Cria documentos do tipo Manual (MAN) para a M7 Investimentos, seguindo rigorosamente o template
  TPL-MAN e as diretrizes da POL-M7-001. Gera arquivo DOCX formatado com capa, controle do documento,
  sumário, e todas as 10 seções obrigatórias (Objetivo, Escopo e Aplicabilidade, Definições e Glossário,
  Visão Geral do Processo, Regras de Negócio, Papéis e Responsabilidades, Indicadores, Cronograma/Frequência,
  Critérios de Qualidade, Documentos Relacionados), mais controle de versões.
  Use when the user asks to create a manual, write a MAN document, draft a manual de operação,
  or mentions manual M7, manual de processo, operational manual, or needs a tactical-level document
  that defines what to do, roles, indicators and business rules for a process.
user-invocable: true
---

# Criação de Manual (MAN) — M7 Investimentos

Crie documentos de **Manual** (nível tático da hierarquia normativa M7) seguindo
100% o template TPL-MAN e as diretrizes da POL-M7-001.

## Filosofia

**"Um manual responde: O QUE FAZER e O QUE ESPERAR."**

O Manual é o nível tático da hierarquia. Ele:
1. **Descreve o processo** — visão macro, entradas, saídas, interfaces
2. **Define regras de negócio** — critérios de decisão, limites, exceções permitidas
3. **Atribui papéis** — quem faz o quê, com quais competências
4. **Estabelece indicadores** — como medir se o processo funciona (KPIs e PPIs)
5. **NÃO detalha passos** — isso é papel da Instrução (INS)
6. **NÃO detalha cálculos** — isso é papel da Especificação Técnica (ESP)

## Contexto Normativo

- **Código**: `MAN-[AREA]-[NNN]`
- **Aprovador**: Head de área
- **Frequência de revisão**: Semestral
- **Público-alvo**: Gestores e líderes
- **Documento superior**: Código da POL que orienta este manual
- **Documentos subordinados**: INSs e ESPs que detalham este manual

Consulte [normative-standards.md](references/normative-standards.md) para detalhes completos.

## Assets e Templates (autocontidos nesta skill)

Esta skill contém todos os recursos necessários para gerar o DOCX final com 100% de fidelidade:

```
creating-manual/
├── SKILL.md                           ← estas instruções
├── references/
│   └── normative-standards.md         ← padrões de codificação e formatação
├── assets/
│   ├── TPL-MAN-Template-de-Manual.docx    ← template DOCX oficial (com logo, estilos, cabeçalho/rodapé)
│   ├── m7-logo-dark.png               ← logo M7 para fundos claros
│   └── m7-logo-offwhite.png           ← logo M7 para fundos escuros
└── scripts/
    └── generate-docx.py               ← script que clona o template e substitui placeholders
```

- **Template DOCX oficial**: [assets/TPL-MAN-Template-de-Manual.docx](assets/TPL-MAN-Template-de-Manual.docx)
  Contém TODA a formatação original: estilos, logo M7 no cabeçalho, cores, fontes, tabelas, rodapé.

- **Logo M7**: [assets/m7-logo-dark.png](assets/m7-logo-dark.png) e [assets/m7-logo-offwhite.png](assets/m7-logo-offwhite.png)
  Já embutidos no template, preservados automaticamente na clonagem.

- **Script gerador**: [scripts/generate-docx.py](scripts/generate-docx.py)
  Uso: `python scripts/generate-docx.py MAN --area PERF --numero 001 --titulo "Título" --doc-superior POL-M7-001 --output ./MAN-PERF-001.docx`

**REGRA CRÍTICA**: NUNCA construa o DOCX do zero com python-docx. SEMPRE clone o template oficial
usando o script `generate-docx.py` ou replicando a mesma abordagem:
1. Abrir `assets/TPL-MAN-Template-de-Manual.docx` como base
2. Substituir placeholders pelos valores reais
3. Adicionar seções de conteúdo
4. Salvar como novo arquivo

Isso garante que logo, cabeçalhos, rodapés, estilos e toda a formatação do template original
sejam preservados automaticamente.

## Estrutura Obrigatória do Documento

```
CAPA
  - "MANUAL" (centralizado, 26pt, #17365D)
  - "MAN-[AREA]-[NNN]"
  - "[Título do Documento]"
  - "Holding M7"
  - "Versão 1.0  |  DD/MM/AAAA"
  --- QUEBRA DE PÁGINA ---

CONTROLE DO DOCUMENTO (tabela de metadados)
  - Inclui campo "Documento superior" com código da POL pai
  - Revisão: Semestral
  --- QUEBRA DE PÁGINA ---

SUMÁRIO

1. OBJETIVO
   Propósito do manual. Qual processo ou tema? Qual a proposta de valor?
   Máximo 2 parágrafos.

2. ESCOPO E APLICABILIDADE
   Onde se aplica: áreas, verticais, processos.
   DEVE referenciar a POL superior pelo código.
   Incluir o que está fora do escopo.

3. DEFINIÇÕES E GLOSSÁRIO
   Termos específicos deste manual, complementando as definições da POL.
   | Termo | Definição |

4. VISÃO GERAL DO PROCESSO
   Descrição macro: objetivo, entradas, saídas, interfaces.
   Usar modelo DEIP (Diagrama de Escopo, Interface e Processos) se aplicável.
   Incluir diagrama de fluxo simplificado.
   Descrever as macro-etapas do processo.

5. REGRAS DE NEGÓCIO
   Regras que governam o processo:
   - Critérios de decisão
   - Limites e restrições
   - Exceções permitidas
   Organizar por tema ou etapa do processo.
   Usar tabelas para classificações e regras condicionais.

6. PAPÉIS E RESPONSABILIDADES
   Papéis, responsabilidades e competências necessárias.
   Usar tabela RACI se processo multi-área:
   | Atividade | Responsável | Aprovador | Consultado | Informado |
   Caso contrário:
   | Papel | Responsabilidades | Competências |

7. INDICADORES
   KPIs (resultado) e PPIs (processo).
   Para cada indicador:
   | Nome | Fórmula | Fonte de Dados | Meta | Frequência |
   Referenciar a ESP relacionada quando houver detalhamento técnico.

8. CRONOGRAMA / FREQUÊNCIA
   Cadências de execução, calendário de rituais, datas de revisão.
   | Atividade | Frequência | Responsável | Entregável |

9. CRITÉRIOS DE QUALIDADE
   Como avaliar qualidade do processo:
   - Critérios de aceite
   - Checkpoints de verificação (DTO — Dono / Testador / Operador)
   | Checkpoint | Critério | Verificador | Momento |

10. DOCUMENTOS RELACIONADOS
    Listar INSs e ESPs vinculados:
    | Código | Título | Relação |

CONTROLE DE VERSÕES
   | Versão | Data | Autor | Alterações |
   | 1.0 | DD/MM/AAAA | [Autor] | Versão inicial. |
```

## Workflow

### Fase 1: Coleta de Informações

Colete do usuário (1 pergunta por vez):

| Campo | Obrigatório | Exemplo |
|-------|-------------|---------|
| Área (AREA) | Sim | PERF, INV, CRE, UNI, SEG, M7 |
| Número (NNN) | Sim | 001 |
| Título | Sim | Manual de Operação do Funil de Investimentos |
| POL superior | Sim | POL-M7-001 |
| Objetivo | Sim | Orientar a operação do funil de captação |
| Escopo | Sim | Área de Investimentos, todas as verticais |
| Elaborado por | Sim | Nome, Cargo |
| Aprovado por | Sim | Nome, Cargo (Head de área) |
| Processo descrito | Sim | Nome e descrição macro do processo |
| Regras de negócio | Sim | Principais regras e critérios |
| Papéis envolvidos | Sim | Responsáveis por cada atividade |
| Indicadores | Sim | KPIs e PPIs do processo |
| INSs e ESPs existentes | Não | Códigos de documentos subordinados |

### Fase 2: Redação

1. **Objetivo** — Comece com "Este manual orienta..." ou "O objetivo deste manual é..."
2. **Escopo e Aplicabilidade** — Referencie a POL: "Este manual implementa as diretrizes da [POL-AREA-NNN]..."
3. **Definições** — Complemente (não repita) as definições da POL. Ordem alfabética
4. **Visão Geral** — Descreva o processo como um todo. Use diagrama de fluxo se possível
5. **Regras de Negócio** — Organize por tema/etapa. Use "deve" (obrigatório) e "pode" (opcional)
6. **Papéis** — Tabela RACI para multi-área, tabela simples caso contrário
7. **Indicadores** — Cada um com fórmula, fonte, meta e frequência. Referencie ESP se aplicável
8. **Cronograma** — Calendário de atividades recorrentes com responsável
9. **Critérios de Qualidade** — Checkpoints mensuráveis com verificador definido
10. **Documentos Relacionados** — Liste INSs e ESPs usando códigos

### Fase 3: Formatação DOCX

Gere o arquivo .docx com `python-docx`:

**Configuração**: A4, margens (3cm sup, 2cm inf, 2.5cm esq, 2cm dir)

**Estilos**:
- Normal: Arial 11pt, #4F4E3C, espaçamento 1.15
- Heading 1: Arial 14pt Negrito, #424135
- Heading 2: Arial 13pt Negrito, #424135
- Heading 3: Arial 11pt Negrito, #424135

**Tabelas**: TableGrid, cabeçalho #424135 texto branco, linhas alternadas #F5F3E8

**Capa**: "MANUAL", código, título, "Holding M7", versão

**Cabeçalho**: `[Título] | [Código] | v[Versão]`
**Rodapé**: `Holding M7  ·  [Código]  ·  Página [N]`

**Nome do arquivo**: `MAN-[AREA]-[NNN]-[Titulo-Kebab-Case].docx`

### Fase 4: Validação

- [ ] Código segue formato `MAN-[AREA]-[NNN]`?
- [ ] Todas as 10 seções presentes e na ordem correta?
- [ ] Tabela de Controle do Documento completa com "Documento superior"?
- [ ] Referência à POL superior na seção 2 (Escopo e Aplicabilidade)?
- [ ] Visão Geral tem descrição macro do processo?
- [ ] Regras de Negócio organizadas por tema/etapa?
- [ ] Papéis cobrem todos os envolvidos no processo?
- [ ] Indicadores têm fórmula, fonte, meta e frequência?
- [ ] Critérios de Qualidade são mensuráveis?
- [ ] Documentos Relacionados listam INSs e ESPs com código?
- [ ] Frequência de revisão = Semestral?
- [ ] Aprovador = Head de área?
- [ ] Controle de Versões no final?

### Fase 5: Entrega

Pergunte ao usuário onde salvar.

## Regras Importantes

1. **Nível tático** — MAN define "o que fazer" e "o que esperar", NUNCA "como fazer passo a passo"
2. **Sempre referencia POL** — Todo MAN tem um documento superior (POL)
3. **Aprovação pelo Head** — O aprovador DEVE ser Head de área
4. **Revisão Semestral** — Frequência fixa para MANs
5. **RACI para multi-área** — Se o processo envolve múltiplas áreas, use tabela RACI
6. **Indicadores mensuráveis** — Cada indicador com fórmula concreta
7. **Lista INS e ESP** — Seção 10 obrigatoriamente lista os documentos subordinados
8. **Formato DOCX** — Output sempre .docx via python-docx
9. **Português brasileiro** — PT-BR formal corporativo

## Anti-Patterns

- **Nunca detalhar passos operacionais** — "Abra o sistema X, clique em Y" é INS, não MAN
- **Nunca detalhar cálculos** — "A fórmula SQL é SELECT..." é ESP, não MAN
- **Nunca omitir a POL superior** — Todo MAN nasce de uma POL
- **Nunca criar indicadores sem fórmula** — "Medir produtividade" não é indicador
- **Nunca pular Critérios de Qualidade** — Sem critérios, não há como avaliar o processo
- **Nunca usar aprovador abaixo de Head** — MAN exige Head de área
- **Nunca referenciar documentos por nome** — Sempre usar código
