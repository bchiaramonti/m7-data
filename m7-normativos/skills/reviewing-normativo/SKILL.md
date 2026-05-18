---
name: reviewing-normativo
description: >
  Realiza QA (Quality Assurance) completo de documentos normativos M7, verificando aderência ao template,
  referências cruzadas, codificação, nomenclatura, completude e conformidade com a POL-M7-001. Analisa
  qualquer tipo de normativo (POL, MAN, INS, ESP) e produz relatório diagnóstico com issues categorizadas
  (CRÍTICO, ATENÇÃO, SUGESTÃO) e correções específicas.
  Use when the user asks to review a normative document, check compliance, validate template adherence,
  verify cross-references, audit documentation, QA a policy/manual/instruction/specification, or mentions
  revisar normativo, verificar aderência, QA de documento, compliance check, referências cruzadas,
  validar template, or auditar documentação corporativa.
user-invocable: true
---

# Revisão e QA de Normativos — M7 Investimentos

Realize verificação completa de qualidade (QA) em documentos normativos M7,
garantindo 100% de aderência à POL-M7-001 e aos templates oficiais.

## Assets e Templates (autocontidos nesta skill)

Esta skill contém os 4 templates DOCX oficiais como referência para verificação de aderência:

```
reviewing-normativo/
├── SKILL.md                                  ← estas instruções
├── references/
│   └── normative-standards.md                ← padrões de codificação e formatação
└── assets/
    ├── TPL-POL-Template-de-Politica.docx     ← template oficial POL
    ├── TPL-MAN-Template-de-Manual.docx       ← template oficial MAN
    ├── TPL-INS-Template-de-Instrucao.docx    ← template oficial INS
    └── TPL-ESP-Template-de-Especificacao-Tecnica.docx  ← template oficial ESP
```

Use estes templates como **referência canônica** para validar se o documento revisado segue
a estrutura, seções e formatação corretas. Abra o template com python-docx para comparar
estilos, seções e metadados quando necessário.

## Filosofia

**"Um normativo só tem valor se estiver correto, completo e conectado à hierarquia."**

A revisão de QA verifica 6 dimensões:
1. **Aderência ao template** — todas as seções presentes, na ordem correta
2. **Codificação** — formato `[TIPO]-[AREA]-[NNN]` correto
3. **Referências cruzadas** — documentos superiores, subordinados e irmãos corretos
4. **Nomenclatura** — termos, nomes e códigos consistentes
5. **Completude** — campos obrigatórios preenchidos, sem placeholders
6. **Conformidade** — regras da POL-M7-001 respeitadas (aprovador, frequência, hierarquia)

## Framework de Análise

### Dimensão 1: Aderência ao Template

Verifique se o documento segue **exatamente** o template correspondente ao seu tipo.

#### Template POL (Política) — 8 seções obrigatórias
```
1. Objetivo
2. Escopo
3. Definições (tabela)
4. Princípios (mín. 3, máx. 8, cada um com título + explicação)
5. Diretrizes (subseções temáticas)
6. Papéis e Responsabilidades (tabela com 3 níveis)
7. Governança (7.1 Revisão, 7.2 Indicadores, 7.3 Exceções)
8. Disposições Finais (8.1 Vigência, 8.2 Documentos relacionados)
+ Controle do Documento (após capa)
+ Controle de Versões (final)
```

#### Template MAN (Manual) — 10 seções obrigatórias
```
1. Objetivo
2. Escopo e Aplicabilidade (referencia POL superior)
3. Definições e Glossário
4. Visão Geral do Processo (macro, DEIP, fluxo)
5. Regras de Negócio (por tema/etapa)
6. Papéis e Responsabilidades (RACI se multi-área)
7. Indicadores (KPIs/PPIs com fórmula, fonte, meta, frequência)
8. Cronograma / Frequência
9. Critérios de Qualidade (checkpoints DTO)
10. Documentos Relacionados (INSs e ESPs)
+ Controle do Documento (com "Documento superior")
+ Controle de Versões
```

#### Template INS (Instrução) — 7 seções obrigatórias
```
1. Objetivo
2. Aplicabilidade (quem, quando, condições)
3. Pré-requisitos (tabela: item, descrição, como obter)
4. Procedimento (fases com passos numerados, específicos)
5. Critérios de Qualidade (checkpoints mensuráveis)
6. Resolução de Problemas (tabela: problema, causa, solução — mín. 3)
7. Referências (MAN pai + ESPs irmãs)
+ Controle do Documento (com "Documento superior")
+ Controle de Versões
```

#### Template ESP (Especificação Técnica) — 8 seções obrigatórias
```
1. Objetivo
2. Escopo (in-scope / out-of-scope)
3. Fontes de Dados (tabela: nome, tipo, acesso, frequência)
4. Indicadores e Regras de Cálculo (fórmula obrigatória por indicador)
5. Views e Queries (SQL em blocos de código)
6. Regras de Negócio Técnicas (arredondamento, nulos, exceções)
7. Validação e Troubleshooting (sanity checks + mín. 3 problemas)
8. Dependências e Integrações (sistemas entrada/saída)
+ Controle do Documento (com "Documento superior")
+ Controle de Versões
```

### Dimensão 2: Codificação

Verificar:
- [ ] Formato `[TIPO]-[AREA]-[NNN]` correto
- [ ] TIPO corresponde ao conteúdo real (POL ≠ procedimentos, MAN ≠ passo a passo)
- [ ] AREA é válida: M7, PERF, INV, CRE, UNI, SEG
- [ ] NNN é 3 dígitos zero-padded
- [ ] Código no Controle do Documento = código na capa = código no cabeçalho
- [ ] Código não duplica documento existente

### Dimensão 3: Referências Cruzadas

```
Regras de referência por tipo:

POL → Não tem documento superior (exceto sub-políticas)
      Lista MANs subordinados em "Documentos relacionados"

MAN → Documento superior = POL (obrigatório)
      Referencia POL em "Escopo e Aplicabilidade"
      Lista INSs e ESPs em "Documentos Relacionados"

INS → Documento superior = MAN (obrigatório)
      Lista MAN pai e ESPs irmãs em "Referências"

ESP → Documento superior = MAN (obrigatório)
      Lista dependências de sistema em "Dependências e Integrações"
```

Verificar:
- [ ] Documento superior preenchido (exceto POL de topo)
- [ ] Código do documento superior existe e é do tipo correto na hierarquia
- [ ] Todos os documentos referenciados usam CÓDIGO (não nome/título)
- [ ] Referências cruzadas são bidirecionais (se MAN lista INS, INS deve listar MAN)
- [ ] Nenhum código referenciado é inválido ou inexistente

### Dimensão 4: Nomenclatura

Verificar:
- [ ] Título na capa = título no cabeçalho = título no Controle do Documento
- [ ] Termos definidos na seção "Definições" são usados consistentemente
- [ ] Nomes de sistemas, áreas e processos são consistentes ao longo do documento
- [ ] Siglas são definidas na primeira ocorrência
- [ ] Nomes de papéis na tabela de responsabilidades = nomes usados no corpo

### Dimensão 5: Completude

Verificar:
- [ ] CAPA completa: tipo, código, título, "Holding M7", versão, data
- [ ] CONTROLE DO DOCUMENTO: todos os campos obrigatórios preenchidos
- [ ] Nenhum placeholder restante (ex: "[inserir aqui]", "TODO", "TBD")
- [ ] Tabelas obrigatórias presentes e preenchidas (não vazias)
- [ ] Seções obrigatórias não estão em branco ou com texto genérico
- [ ] CONTROLE DE VERSÕES no final com pelo menos versão 1.0
- [ ] Data no formato DD/MM/AAAA (não MM/DD ou YYYY-MM-DD)

### Dimensão 6: Conformidade POL-M7-001

Verificar conforme tipo:

| Regra | POL | MAN | INS | ESP |
|-------|-----|-----|-----|-----|
| Aprovador correto | Diretoria | Head de área | Líder do processo | Analista responsável |
| Frequência de revisão | Anual | Semestral | Trimestral | Trimestral |
| Classificação | Interno | Interno | Interno | Interno |
| Documento superior | Nenhum* | POL | MAN | MAN |
| Nível hierárquico correto | Não detalha "como" | Não detalha passos | Não define princípios | Não define processos |

(*) exceto sub-políticas

**Verificação de conteúdo no nível correto:**
- POL com passos operacionais → CRÍTICO (deveria ser INS)
- MAN com SQL ou fórmulas detalhadas → CRÍTICO (deveria ser ESP)
- INS definindo princípios ou limites estratégicos → CRÍTICO (deveria ser POL)
- ESP ensinando passos de execução → CRÍTICO (deveria ser INS)

## Workflow

### Fase 1: Identificar o Documento

1. Leia o documento fornecido pelo usuário
2. Identifique o tipo pelo código ou conteúdo: POL, MAN, INS ou ESP
3. Identifique a versão e data
4. Carregue o template de referência correspondente

### Fase 2: Análise Dimensional

Execute a verificação em todas as 6 dimensões, na ordem:
1. Aderência ao template
2. Codificação
3. Referências cruzadas
4. Nomenclatura
5. Completude
6. Conformidade POL-M7-001

Para cada issue encontrada, classifique:

| Severidade | Critério | Exemplo |
|------------|----------|---------|
| **CRÍTICO** | Violação de regra obrigatória, template incorreto, hierarquia quebrada | Seção ausente, aprovador errado, conteúdo no nível errado |
| **ATENÇÃO** | Incompletude, inconsistência, risco de ambiguidade | Placeholder não substituído, referência sem código, tabela incompleta |
| **SUGESTÃO** | Melhoria de qualidade, clareza ou organização | Termo sem definição, tabela útil não incluída, ordem melhorável |

### Fase 3: Validação de Referências Cruzadas (Deep Check)

Se o usuário fornecer acesso a outros documentos do repositório:
1. Verifique se os códigos referenciados existem
2. Verifique se as referências são bidirecionais
3. Verifique se a hierarquia está correta (POL → MAN → INS/ESP)
4. Liste documentos órfãos (referenciados mas inexistentes)
5. Liste referências pendentes (documento existe mas não é referenciado)

### Fase 4: Gerar Relatório

Produza o relatório no seguinte formato:

```markdown
# Revisão de QA: [Código] — [Título]

**Tipo**: [POL / MAN / INS / ESP]
**Versão analisada**: [X.X]
**Data da revisão**: [DD/MM/AAAA]
**Score geral**: [A / B / C / D]

## Scoring
- **A**: 0 críticos, ≤ 2 atenções
- **B**: 0 críticos, 3+ atenções
- **C**: 1-2 críticos
- **D**: 3+ críticos

## Issues Encontradas

### CRÍTICO (deve corrigir)

#### [Título da issue]
- **Dimensão**: [Template / Codificação / Referências / Nomenclatura / Completude / Conformidade]
- **Localização**: [Seção, campo ou tabela afetada]
- **Encontrado**: [O que está errado]
- **Esperado**: [O que deveria ser]
- **Correção**: [Ação específica para resolver]

### ATENÇÃO (deveria corrigir)
[Mesma estrutura]

### SUGESTÃO (pode melhorar)
[Mesma estrutura]

## Resumo por Dimensão

| Dimensão | Status | Issues |
|----------|--------|--------|
| Aderência ao template | [OK / FALHA] | [contagem] |
| Codificação | [OK / FALHA] | [contagem] |
| Referências cruzadas | [OK / FALHA] | [contagem] |
| Nomenclatura | [OK / FALHA] | [contagem] |
| Completude | [OK / FALHA] | [contagem] |
| Conformidade POL-M7-001 | [OK / FALHA] | [contagem] |

## Checklist de Referências Cruzadas

| Código Referenciado | Existe? | Referência Bidirecional? | Status |
|---------------------|---------|--------------------------|--------|
| [código] | [Sim/Não/Não verificado] | [Sim/Não/N/A] | [OK/FALHA] |

## Próximos Passos
1. [Ação prioritária 1]
2. [Ação prioritária 2]
3. [...]
```

## Regras Importantes

1. **Diagnóstico, não reescrita** — A skill produz um relatório de QA, NÃO reescreve o documento
2. **Específico** — Cada issue com localização exata e correção concreta
3. **Hierarquia importa** — Conteúdo no nível errado é SEMPRE CRÍTICO
4. **Códigos, não nomes** — Referências devem ser por código
5. **Bidirecionais** — Se A referencia B, B deve referenciar A
6. **Scoring objetivo** — A/B/C/D baseado em contagem de issues por severidade
7. **Português brasileiro** — Relatório em PT-BR formal

## Anti-Patterns

- **Nunca ser vago** — "A seção 5 precisa melhorar" não é QA. Diga O QUE está errado e COMO corrigir
- **Nunca reescrever** — Produza diagnóstico, não versão corrigida (a menos que o usuário peça)
- **Nunca ignorar hierarquia** — Conteúdo no nível errado compromete toda a arquitetura normativa
- **Nunca aprovar documento incompleto** — Se faltam seções obrigatórias, é CRÍTICO
- **Nunca pular referências cruzadas** — Documentos desconectados da hierarquia perdem contexto
- **Nunca inventar issues** — Se está conforme, diga que está conforme. QA honesto
- **Nunca verificar formatação visual** — QA verifica estrutura e conteúdo, não estilo de fonte
