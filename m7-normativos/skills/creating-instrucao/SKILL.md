---
name: creating-instrucao
description: >
  Cria documentos do tipo Instrução (INS) para a M7 Investimentos, seguindo rigorosamente o template
  TPL-INS e as diretrizes da POL-M7-001. Gera arquivo DOCX formatado com capa, controle do documento,
  sumário, e todas as 7 seções obrigatórias (Objetivo, Aplicabilidade, Pré-requisitos, Procedimento,
  Critérios de Qualidade, Resolução de Problemas, Referências), mais controle de versões.
  Use when the user asks to create an instruction, write an INS document, draft a step-by-step procedure,
  create instrução, or mentions instrução de trabalho, procedimento operacional, passo a passo, how-to,
  or needs an operational-level document that teaches how to execute an activity step by step.
user-invocable: true
---

# Criação de Instrução (INS) — M7 Investimentos

Crie documentos de **Instrução** (nível operacional da hierarquia normativa M7) seguindo
100% o template TPL-INS e as diretrizes da POL-M7-001.

## Filosofia

**"Uma instrução responde: COMO FAZER, passo a passo."**

A Instrução é o nível operacional. Ela:
1. **Ensina a execução** — cada passo numerado, específico e verificável
2. **Define pré-requisitos** — o que deve estar pronto antes de começar
3. **Estabelece critérios de qualidade** — como saber se fez certo
4. **Resolve problemas comuns** — troubleshooting para os erros mais frequentes
5. **NÃO define princípios** — isso é POL
6. **NÃO define regras de negócio** — isso é MAN
7. **NÃO detalha cálculos técnicos** — isso é ESP

## Contexto Normativo

- **Código**: `INS-[AREA]-[NNN]`
- **Aprovador**: Líder do processo
- **Frequência de revisão**: Trimestral
- **Público-alvo**: Executores (quem faz a atividade)
- **Documento superior**: Código do MAN que orienta esta instrução
- **Documentos irmãos**: ESPs com detalhamento técnico relacionado

Consulte [normative-standards.md](references/normative-standards.md) para detalhes completos.

## Assets e Templates (autocontidos nesta skill)

Esta skill contém todos os recursos necessários para gerar o DOCX final com 100% de fidelidade:

```
creating-instrucao/
├── SKILL.md                           ← estas instruções
├── references/
│   └── normative-standards.md         ← padrões de codificação e formatação
├── assets/
│   ├── TPL-INS-Template-de-Instrucao.docx ← template DOCX oficial (com logo, estilos, cabeçalho/rodapé)
│   ├── m7-logo-dark.png               ← logo M7 para fundos claros
│   └── m7-logo-offwhite.png           ← logo M7 para fundos escuros
└── scripts/
    └── generate-docx.py               ← script que clona o template e substitui placeholders
```

- **Template DOCX oficial**: [assets/TPL-INS-Template-de-Instrucao.docx](assets/TPL-INS-Template-de-Instrucao.docx)
  Contém TODA a formatação original: estilos, logo M7 no cabeçalho, cores, fontes, tabelas, rodapé.

- **Logo M7**: [assets/m7-logo-dark.png](assets/m7-logo-dark.png) e [assets/m7-logo-offwhite.png](assets/m7-logo-offwhite.png)
  Já embutidos no template, preservados automaticamente na clonagem.

- **Script gerador**: [scripts/generate-docx.py](scripts/generate-docx.py)
  Uso: `python scripts/generate-docx.py INS --area PERF --numero 001 --titulo "Título" --doc-superior MAN-PERF-001 --output ./INS-PERF-001.docx`

**REGRA CRÍTICA**: NUNCA construa o DOCX do zero com python-docx. SEMPRE clone o template oficial
usando o script `generate-docx.py` ou replicando a mesma abordagem:
1. Abrir `assets/TPL-INS-Template-de-Instrucao.docx` como base
2. Substituir placeholders pelos valores reais
3. Adicionar seções de conteúdo
4. Salvar como novo arquivo

Isso garante que logo, cabeçalhos, rodapés, estilos e toda a formatação do template original
sejam preservados automaticamente.

## Estrutura Obrigatória do Documento

```
CAPA
  - "INSTRUÇÃO" (centralizado, 26pt, #17365D)
  - "INS-[AREA]-[NNN]"
  - "[Título do Documento]"
  - "Holding M7"
  - "Versão 1.0  |  DD/MM/AAAA"
  --- QUEBRA DE PÁGINA ---

CONTROLE DO DOCUMENTO (tabela de metadados)
  - Documento superior: código do MAN pai
  - Revisão: Trimestral
  --- QUEBRA DE PÁGINA ---

SUMÁRIO

1. OBJETIVO
   O que esta instrução ensina. Qual atividade? Resultado esperado?
   Máximo 2 parágrafos.

2. APLICABILIDADE
   Quando seguir esta instrução. Por quem? Sob quais condições?
   Listar explicitamente:
   - Quem deve seguir
   - Em quais situações
   - Frequência (se aplicável)

3. PRÉ-REQUISITOS
   O que deve estar pronto antes de iniciar:
   - Acessos necessários (sistemas, permissões)
   - Dados/informações disponíveis
   - Materiais/ferramentas
   - Aprovações prévias
   Usar tabela:
   | Pré-requisito | Descrição | Como Obter |

4. PROCEDIMENTO
   Passo a passo da execução.
   Organizar em fases/etapas:

   4.1 Fase 1: [Nome da Fase] (ex: Preparação)
       Passo 1: [Ação específica]
       Passo 2: [Ação específica]
       ...

   4.2 Fase 2: [Nome da Fase] (ex: Execução)
       Passo 1: [Ação específica]
       ...

   4.3 Fase 3: [Nome da Fase] (ex: Pós-execução)
       Passo 1: [Ação específica]
       ...

   REGRAS para cada passo:
   - Numerar sequencialmente dentro de cada fase
   - Ser específico: "Acesse sistema X > Menu Y > Opção Z"
   - Incluir screenshots se necessário
   - Indicar resultado esperado de cada passo
   - Sinalizar pontos de atenção com "ATENÇÃO:" ou "IMPORTANTE:"

5. CRITÉRIOS DE QUALIDADE
   Como saber se foi feito corretamente:
   | Critério | Descrição | Verificação |
   Incluir checkpoints DTO (Dono/Testador/Operador) se aplicável.

6. RESOLUÇÃO DE PROBLEMAS
   Problemas comuns e soluções:
   | Problema | Causa Provável | Solução |
   Começar com 3-5 problemas mais frequentes.
   Expandir conforme experiência.

7. REFERÊNCIAS
   Listar o MAN pai e ESPs irmãs:
   | Código | Título | Relação |
   Incluir links para sistemas e dashboards.

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
| Título | Sim | Instrução de Fechamento Mensal de Performance |
| MAN superior | Sim | MAN-PERF-001 |
| Objetivo | Sim | Ensinar o processo de fechamento mensal |
| Aplicabilidade | Sim | Analistas de Performance, mensal |
| Elaborado por | Sim | Nome, Cargo |
| Aprovado por | Sim | Nome, Cargo (Líder do processo) |
| Atividade detalhada | Sim | Descrição da atividade e suas etapas |
| Pré-requisitos | Sim | Acessos, dados, ferramentas necessárias |
| Problemas conhecidos | Não | Erros comuns e soluções |
| ESPs relacionadas | Não | Códigos de especificações técnicas |

### Fase 2: Redação

1. **Objetivo** — Comece com "Esta instrução orienta..." ou "O objetivo desta instrução é..."
2. **Aplicabilidade** — Seja explícito: quem, quando, em quais condições
3. **Pré-requisitos** — Tabela com cada item e como obtê-lo
4. **Procedimento** — Organize em fases. Cada passo: ação + resultado esperado
   - Use subsections (4.1, 4.2, 4.3) para cada fase
   - Numere passos dentro de cada fase
   - Seja específico: nomes de sistemas, menus, campos, botões
   - Marque pontos críticos com "ATENÇÃO:" ou "IMPORTANTE:"
5. **Critérios de Qualidade** — Checkpoints mensuráveis e verificáveis
6. **Resolução de Problemas** — Tabela com mínimo 3 problemas comuns
7. **Referências** — MAN pai + ESPs irmãs, todos com código

### Fase 3: Formatação DOCX

Gere o arquivo .docx com `python-docx`:

**Configuração**: A4, margens (3cm sup, 2cm inf, 2.5cm esq, 2cm dir)

**Estilos**:
- Normal: Arial 11pt, #4F4E3C, espaçamento 1.15
- Heading 1: Arial 14pt Negrito, #424135
- Heading 2: Arial 13pt Negrito, #424135
- Heading 3: Arial 11pt Negrito, #424135

**Tabelas**: TableGrid, cabeçalho #424135 texto branco, linhas alternadas #F5F3E8

**Capa**: "INSTRUÇÃO", código, título, "Holding M7", versão

**Cabeçalho**: `[Título] | [Código] | v[Versão]`
**Rodapé**: `Holding M7  ·  [Código]  ·  Página [N]`

**Nome do arquivo**: `INS-[AREA]-[NNN]-[Titulo-Kebab-Case].docx`

### Fase 4: Validação

- [ ] Código segue formato `INS-[AREA]-[NNN]`?
- [ ] Todas as 7 seções presentes e na ordem correta?
- [ ] Tabela de Controle do Documento com "Documento superior" (MAN)?
- [ ] Pré-requisitos listados em tabela?
- [ ] Procedimento organizado em fases com passos numerados?
- [ ] Cada passo é específico (sistema, menu, campo, botão)?
- [ ] Critérios de Qualidade são mensuráveis?
- [ ] Resolução de Problemas tem mínimo 3 itens?
- [ ] Referências listam MAN pai e ESPs com código?
- [ ] Frequência de revisão = Trimestral?
- [ ] Aprovador = Líder do processo?
- [ ] Controle de Versões no final?

### Fase 5: Entrega

Pergunte ao usuário onde salvar.

## Regras Importantes

1. **Nível operacional** — INS ensina "como fazer", com ações concretas e sequenciais
2. **Sempre referencia MAN** — Todo INS tem um MAN como documento superior
3. **Aprovação pelo Líder** — O aprovador é o Líder do processo
4. **Revisão Trimestral** — Frequência fixa para INSs
5. **Passos numerados** — Cada ação tem número e resultado esperado
6. **Específico** — Nomes de sistema, menu, campo, botão — nunca genérico
7. **Troubleshooting** — Mínimo 3 problemas/soluções na seção 6
8. **Formato DOCX** — Output sempre .docx via python-docx
9. **Português brasileiro** — PT-BR formal corporativo

## Anti-Patterns

- **Nunca ser genérico** — "Acesse o sistema e faça a exportação" não é instrução. Diga QUAL sistema, QUAL menu, QUAL botão
- **Nunca definir princípios** — "Valorizamos a qualidade" é POL, não INS
- **Nunca definir regras de negócio** — "O limite de aprovação é R$ 50k" é MAN, não INS
- **Nunca omitir pré-requisitos** — Se alguém não conseguir seguir por falta de acesso, a INS falhou
- **Nunca pular Resolução de Problemas** — Os erros comuns SERÃO encontrados. Antecipe
- **Nunca omitir o MAN superior** — Toda INS nasce de um MAN
- **Nunca usar aprovador acima de Líder** — INS é aprovada pelo Líder do processo
