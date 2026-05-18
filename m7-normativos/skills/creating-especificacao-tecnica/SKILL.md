---
name: creating-especificacao-tecnica
description: >
  Cria documentos do tipo Especificação Técnica (ESP) para a M7 Investimentos, seguindo rigorosamente
  o template TPL-ESP e as diretrizes da POL-M7-001. Gera arquivo DOCX formatado com capa, controle do
  documento, sumário, e todas as 8 seções obrigatórias (Objetivo, Escopo, Fontes de Dados, Indicadores e
  Regras de Cálculo, Views e Queries, Regras de Negócio Técnicas, Validação e Troubleshooting,
  Dependências e Integrações), mais controle de versões.
  Use when the user asks to create a technical specification, write an ESP document, document calculations,
  specify data rules, or mentions especificação técnica, regras de cálculo, indicadores técnicos, queries SQL,
  fontes de dados, data pipeline, or needs a technical-level document detailing data sources, calculation rules,
  and system integrations.
user-invocable: true
---

# Criação de Especificação Técnica (ESP) — M7 Investimentos

Crie documentos de **Especificação Técnica** (nível técnico da hierarquia normativa M7) seguindo
100% o template TPL-ESP e as diretrizes da POL-M7-001.

## Filosofia

**"Uma especificação técnica responde: COM QUAIS DADOS e REGRAS DE CÁLCULO."**

A Especificação Técnica é o nível mais detalhado. Ela:
1. **Documenta fontes de dados** — origem, tipo, frequência, credenciais
2. **Define regras de cálculo** — fórmulas, unidades, periodicidade
3. **Registra queries e views** — SQL, pipelines, transformações
4. **Especifica regras técnicas** — arredondamento, nulos, classificações, exceções
5. **Mapeia dependências** — sistemas, APIs, integrações
6. **NÃO define princípios** — isso é POL
7. **NÃO define o que fazer** — isso é MAN
8. **NÃO ensina como executar** — isso é INS

## Contexto Normativo

- **Código**: `ESP-[AREA]-[NNN]`
- **Aprovador**: Analista responsável
- **Frequência de revisão**: Trimestral
- **Público-alvo**: Analistas e TI
- **Documento superior**: Código do MAN que orienta esta especificação
- **Documentos irmãos**: INSs do mesmo processo

Consulte [normative-standards.md](references/normative-standards.md) para detalhes completos.

## Assets e Templates (autocontidos nesta skill)

Esta skill contém todos os recursos necessários para gerar o DOCX final com 100% de fidelidade:

```
creating-especificacao-tecnica/
├── SKILL.md                                  ← estas instruções
├── references/
│   └── normative-standards.md                ← padrões de codificação e formatação
├── assets/
│   ├── TPL-ESP-Template-de-Especificacao-Tecnica.docx  ← template DOCX oficial
│   ├── m7-logo-dark.png                      ← logo M7 para fundos claros
│   └── m7-logo-offwhite.png                  ← logo M7 para fundos escuros
└── scripts/
    └── generate-docx.py                      ← script que clona o template e substitui placeholders
```

- **Template DOCX oficial**: [assets/TPL-ESP-Template-de-Especificacao-Tecnica.docx](assets/TPL-ESP-Template-de-Especificacao-Tecnica.docx)
  Contém TODA a formatação original: estilos, logo M7 no cabeçalho, cores, fontes, tabelas, rodapé.

- **Logo M7**: [assets/m7-logo-dark.png](assets/m7-logo-dark.png) e [assets/m7-logo-offwhite.png](assets/m7-logo-offwhite.png)
  Já embutidos no template, preservados automaticamente na clonagem.

- **Script gerador**: [scripts/generate-docx.py](scripts/generate-docx.py)
  Uso: `python scripts/generate-docx.py ESP --area PERF --numero 001 --titulo "Título" --doc-superior MAN-PERF-001 --output ./ESP-PERF-001.docx`

**REGRA CRÍTICA**: NUNCA construa o DOCX do zero com python-docx. SEMPRE clone o template oficial
usando o script `generate-docx.py` ou replicando a mesma abordagem:
1. Abrir `assets/TPL-ESP-Template-de-Especificacao-Tecnica.docx` como base
2. Substituir placeholders pelos valores reais
3. Adicionar seções de conteúdo
4. Salvar como novo arquivo

Isso garante que logo, cabeçalhos, rodapés, estilos e toda a formatação do template original
sejam preservados automaticamente.

## Estrutura Obrigatória do Documento

```
CAPA
  - "ESPECIFICAÇÃO TÉCNICA" (centralizado, 26pt, #17365D)
  - "ESP-[AREA]-[NNN]"
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
   O que esta especificação detalha tecnicamente.
   Quais indicadores, cálculos ou integrações?
   Máximo 2 parágrafos.

2. ESCOPO
   Quais indicadores, sistemas ou processos são cobertos.
   In-scope e out-of-scope explícitos.

3. FONTES DE DADOS
   Para cada fonte:
   | Nome | Tipo (BD, API, Planilha) | Credenciais/Acesso | Frequência de Atualização |
   Detalhar cada fonte com:
   - Nome e descrição
   - Tipo (database, API REST, arquivo CSV, planilha)
   - Como obter acesso
   - Frequência de atualização dos dados

4. INDICADORES E REGRAS DE CÁLCULO
   Para cada indicador, uma subseção:

   4.N [Nome do Indicador]
   | Campo | Valor |
   |-------|-------|
   | Nome | [Nome completo] |
   | Código | [Código do indicador] |
   | Fórmula | [Fórmula de cálculo] |
   | Unidade | [%, R$, qtd, dias...] |
   | Fonte(s) | [Nomes das fontes de dados] |
   | Periodicidade | [Diário, Semanal, Mensal...] |
   | Responsável | [Quem gera/valida] |

   Incluir exemplos numéricos quando útil.

5. VIEWS E QUERIES
   Para cada view/query:

   5.N [Nome da View/Query]
   - Descrição
   - Campos principais
   - Filtros aplicados
   - Código SQL (quando relevante)

   Usar blocos de código para SQL:
   ```sql
   SELECT campo1, campo2
   FROM tabela
   WHERE filtro = valor
   ```

6. REGRAS DE NEGÓCIO TÉCNICAS
   Regras especiais:
   - Arredondamento (casas decimais, método)
   - Tratamento de nulos (ignorar, zero, média)
   - Períodos de competência (mês fechado, acumulado)
   - Classificações e faixas
   - Exceções e edge cases
   Usar tabelas para regras condicionais:
   | Condição | Regra | Exemplo |

7. VALIDAÇÃO E TROUBLESHOOTING
   Validação de dados:
   - Sanity checks (ranges, totais, consistência)
   - Reconciliação com outras fontes
   Problemas comuns:
   | Problema | Causa | Solução Técnica |

8. DEPENDÊNCIAS E INTEGRAÇÕES
   Sistemas, APIs e processos que alimentam ou consomem estes dados.
   | Sistema/API | Direção (Entrada/Saída) | Frequência | Responsável |
   Incluir diagrama de fluxo de dados se útil.

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
| Título | Sim | Especificação de Cálculo de Indicadores de Performance |
| MAN superior | Sim | MAN-PERF-001 |
| Objetivo | Sim | Detalhar cálculos dos KPIs de performance |
| Escopo | Sim | Indicadores X, Y, Z do dashboard de performance |
| Elaborado por | Sim | Nome, Cargo |
| Aprovado por | Sim | Nome, Cargo (Analista responsável) |
| Fontes de dados | Sim | Bancos, APIs, planilhas |
| Indicadores e fórmulas | Sim | Nome, fórmula, unidade de cada indicador |
| Queries SQL | Não | Views e queries existentes |
| Regras especiais | Não | Arredondamento, nulos, exceções |
| Sistemas integrados | Sim | APIs, bancos, processos consumidores |

### Fase 2: Redação

1. **Objetivo** — Comece com "Esta especificação detalha..." ou "O objetivo desta especificação é..."
2. **Escopo** — Liste indicadores/sistemas cobertos e não cobertos
3. **Fontes de Dados** — Tabela detalhada com tipo, acesso e frequência
4. **Indicadores** — Uma subseção por indicador. Fórmula é OBRIGATÓRIA
5. **Views e Queries** — SQL formatado em blocos de código. Descreva filtros
6. **Regras Técnicas** — Tabelas para condições e exceções
7. **Validação** — Sanity checks concretos + troubleshooting com mínimo 3 itens
8. **Dependências** — Diagrama de fluxo de dados entre sistemas

### Fase 3: Formatação DOCX

Gere o arquivo .docx com `python-docx`:

**Configuração**: A4, margens (3cm sup, 2cm inf, 2.5cm esq, 2cm dir)

**Estilos**:
- Normal: Arial 11pt, #4F4E3C, espaçamento 1.15
- Heading 1: Arial 14pt Negrito, #424135
- Heading 2: Arial 13pt Negrito, #424135
- Heading 3: Arial 11pt Negrito, #424135

**Tabelas**: TableGrid, cabeçalho #424135 texto branco, linhas alternadas #F5F3E8

**Blocos de código SQL**: Usar fonte Courier New 9pt, fundo #F5F3E8

**Capa**: "ESPECIFICAÇÃO TÉCNICA", código, título, "Holding M7", versão

**Cabeçalho**: `[Título] | [Código] | v[Versão]`
**Rodapé**: `Holding M7  ·  [Código]  ·  Página [N]`

**Nome do arquivo**: `ESP-[AREA]-[NNN]-[Titulo-Kebab-Case].docx`

### Fase 4: Validação

- [ ] Código segue formato `ESP-[AREA]-[NNN]`?
- [ ] Todas as 8 seções presentes e na ordem correta?
- [ ] Tabela de Controle do Documento com "Documento superior" (MAN)?
- [ ] Fontes de Dados com tipo, acesso e frequência?
- [ ] Cada indicador tem fórmula, unidade, fonte e periodicidade?
- [ ] Queries SQL formatadas em blocos de código?
- [ ] Regras Técnicas cobrem arredondamento e nulos?
- [ ] Validação tem sanity checks e mínimo 3 troubleshooting?
- [ ] Dependências mapeiam entrada/saída com sistemas?
- [ ] Frequência de revisão = Trimestral?
- [ ] Aprovador = Analista responsável?
- [ ] Controle de Versões no final?

### Fase 5: Entrega

Pergunte ao usuário onde salvar.

## Regras Importantes

1. **Nível técnico** — ESP detalha "com quais dados e regras de cálculo", NUNCA "por quê" ou "como executar"
2. **Sempre referencia MAN** — Todo ESP tem um MAN como documento superior
3. **Aprovação pelo Analista** — O aprovador é o Analista responsável
4. **Revisão Trimestral** — Frequência fixa para ESPs
5. **Fórmulas obrigatórias** — Cada indicador DEVE ter fórmula explícita
6. **SQL formatado** — Queries em blocos de código com fonte monospace
7. **Validação técnica** — Sanity checks concretos, não genéricos
8. **Formato DOCX** — Output sempre .docx via python-docx
9. **Português brasileiro** — PT-BR formal corporativo

## Anti-Patterns

- **Nunca ser vago nas fórmulas** — "Calcular a produtividade" não é especificação. Dê a fórmula: `Produtividade = Entregas / Horas`
- **Nunca omitir fonte de dados** — Cada cálculo depende de dados. De onde vêm?
- **Nunca ignorar edge cases** — O que acontece com nulos? Com períodos incompletos? Com dados retroativos?
- **Nunca definir princípios** — "Valorizamos dados confiáveis" é POL, não ESP
- **Nunca ensinar passos** — "Abra o Power BI e clique em Atualizar" é INS, não ESP
- **Nunca omitir o MAN superior** — Toda ESP nasce de um MAN
- **Nunca referenciar documentos por nome** — Sempre usar código
