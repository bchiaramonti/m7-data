# m7-normativos

Plugin para criacao e revisao de documentos normativos da M7 Investimentos, seguindo rigorosamente a POL-M7-001 (Politica de Gestao por Processos e Padronizacao) e os templates oficiais.

## O que faz

Gera documentos DOCX 100% aderentes aos templates oficiais M7, com logo, cabecalho/rodape, estilos, tabelas formatadas e codificacao correta. Tambem realiza QA de documentos existentes.

## Hierarquia Normativa

```
POL (Politica)          ← Estrategico: por que e dentro de quais limites
  └── MAN (Manual)      ← Tatico: o que fazer e o que esperar
        ├── INS (Instrucao)          ← Operacional: como fazer, passo a passo
        └── ESP (Especificacao Tecnica)  ← Tecnico: dados e regras de calculo
```

## Componentes

### Agente

| Agente | Modelo | Descricao |
|--------|--------|-----------|
| **governance-writer** | Opus | Especialista em documentacao corporativa. Identifica o tipo, coleta informacoes e coordena as skills |

### Skills

| Skill | Tipo | Descricao |
|-------|------|-----------|
| **creating-politica** | POL | Cria Politicas — principios, diretrizes, governanca |
| **creating-manual** | MAN | Cria Manuais — processos, regras de negocio, indicadores |
| **creating-instrucao** | INS | Cria Instrucoes — procedimentos passo a passo |
| **creating-especificacao-tecnica** | ESP | Cria Especificacoes Tecnicas — dados, calculos, queries |
| **reviewing-normativo** | QA | Revisa qualquer normativo verificando aderencia, codificacao, referencias cruzadas |

### Autocontencao

Cada skill contem dentro de si:
- **Template DOCX oficial** — preserva logo, estilos, cabecalho/rodape
- **Logo M7** — dark e offwhite
- **Script Python** — `generate-docx.py` que clona o template e substitui placeholders
- **Referencias** — `normative-standards.md` com todas as regras da POL-M7-001

## Uso

```
# Criar uma politica
"Crie uma politica de seguranca da informacao para a M7"

# Criar um manual
"Crie um manual de operacao do funil de investimentos"

# Criar uma instrucao
"Crie uma instrucao de fechamento mensal de performance"

# Criar uma especificacao tecnica
"Crie uma especificacao de calculo dos KPIs de performance"

# Revisar um normativo existente
"Revise o MAN-PERF-001 e verifique se esta aderente ao template"
```

## Codificacao

Formato: `[TIPO]-[AREA]-[NNN]`

- **TIPO**: POL, MAN, INS, ESP
- **AREA**: M7, PERF, INV, CRE, UNI, SEG
- **NNN**: 3 digitos (001, 002...)

## Dependencias

- Python 3.x
- python-docx (`pip install python-docx`)
