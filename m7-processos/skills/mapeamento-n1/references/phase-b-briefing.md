# Fase B · BRIEFING.md (single source of truth)

Documento de apoio à [SKILL.md](../SKILL.md). Define o schema canônico do BRIEFING que liga a Fase A (entrevista crítica) à Fase C (produção dos 4 artefatos).

## Sumário

1. [Por que SSOT](#1-por-que-ssot)
2. [Estrutura geral](#2-estrutura-geral)
3. [Schema completo do frontmatter](#3-schema-completo-do-frontmatter)
4. [Seções markdown](#4-seções-markdown)
5. [Validação](#5-validação)
6. [Convenções](#6-convenções)

---

## 1. Por que SSOT

O BRIEFING.md é o **único contrato** entre a fase de entrevista e a fase de produção. Vantagens:

- **Auditabilidade**: humanos revisam o BRIEFING antes de gerar artefatos. Mais barato corrigir aqui do que regenerar HTML/PDF.
- **Idempotência**: regenerar artefatos sem refazer entrevista. Trocar o template não afeta os dados.
- **Rastreabilidade**: histórico de iteração fica em `## Notas de iteração` (auditoria).
- **Validação determinística**: `check_briefing.py` roda sem custo de API — bloqueia geração de artefato malformado.
- **Composição**: outras skills/scripts podem consumir o BRIEFING (ex.: gerar Excel de processos, alimentar ClickUp tasks).

---

## 2. Estrutura geral

```
mapeamento-{slug}.briefing.md
├── Frontmatter YAML  (parseável por máquina)
│   ├── empresa { nome, slug, setor, escopo }
│   ├── data_referencia, versao, area_documento, logo
│   ├── n1 { variante, rotulo_nucleo, total_processos, contagens }
│   ├── processos[]   ← lista canônica (todos os campos por processo)
│   ├── relacoes[]    ← alimenta RELATIONS do N3
│   ├── artefatos_a_gerar[]
│   └── validacao { bloqueadores, avisos, todos, bloqueadores_aceitos }
│
└── Seções Markdown   (legíveis por humano)
    ├── # Briefing — Cadeia de Valor {empresa}
    ├── ## Objetivo do diagrama
    ├── ## Lede do documento
    ├── ## Contexto da empresa
    ├── ## Notas de iteração
    └── ## Anexos / referências
```

---

## 3. Schema completo do frontmatter

### 3.1 — Campos raiz

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `schema_version` | int | ✓ | Sempre `1` no MVP. Bumpa quando schema breaking. |
| `empresa` | object | ✓ | Identidade da empresa-alvo (ver 3.2). |
| `data_referencia` | string | ✓ | Mês/ano legível (ex.: `"Fev / 2026"`). Aparece no header dos artefatos. |
| `versao` | string | ✓ | Versão compacta (ex.: `"02/26"`). Aparece no strip do header. |
| `area_documento` | string | ✓ | Área owner do documento (ex.: `"Estrategia"`). |
| `logo` | string | ✓ | `"default"` (usa M7) ou caminho relativo a um PNG. |
| `n1` | object | ✓ | Configuração do diagrama N1 (ver 3.3). |
| `processos` | list | ✓ | Lista canônica de processos (ver 3.4). |
| `relacoes` | list | – | Lista de relações para o N3 (ver 3.5). Vazia se N3 não será gerado. |
| `artefatos_a_gerar` | list | ✓ | Subset de `["n1", "n2", "n3", "n4-pdf"]`. |
| `validacao` | object | ✓ | Resultado da validação (preenchido por scripts/critic). |

### 3.2 — `empresa`

| Campo | Tipo | Obrigatório | Notas |
|---|---|---|---|
| `nome` | string | ✓ | Nome legal/comercial (ex.: `"M7 Investimentos"`). |
| `slug` | string | ✓ | kebab-case sem acentos. Usado em nomes de arquivo. |
| `setor` | string | ✓ | Setor/segmento (ex.: `"Wealth management"`). |
| `escopo` | string | ✓ | `holding` ou `bu:<nome>` ou `produto:<nome>`. |

### 3.3 — `n1`

| Campo | Tipo | Obrigatório | Notas |
|---|---|---|---|
| `variante` | string | ✓ | `A` (master, default) ou `B` (linear). |
| `rotulo_nucleo` | string | A | Rótulo do bloco do núcleo (variante A). Ex.: `"Verticais de Produto"`. |
| `total_processos` | int | ✓ | Soma de gerenciais + primarios + apoio. |
| `contagens` | object | ✓ | `{ gerenciais, primarios, apoio }` — todos int. |

`check_briefing.py` cross-valida: `total_processos == sum(contagens.values()) == len(filtered processos[])`.

### 3.4 — `processos[]` (cada item)

| Campo | Tipo | Obrigatório | Notas |
|---|---|---|---|
| `codigo` | string | ✓ | `G1..Gn`, `P1..Pn`, `A1..An`. Único na lista. |
| `camada` | string | ✓ | `gerencial` \| `primario` \| `apoio`. |
| `subcamada` | string | – | `front` \| `nucleo` \| `back` — só se `camada=primario` e `n1.variante=A`. |
| `nome` | string | ✓ | Max 3 palavras. Use `&` em vez de "e". |
| `tooltip` | list[string] | ✓ | 2-4 linhas telegráficas. Para gerenciais, última linha começa com `Freq:`. |
| `frequencia` | string | gerencial | Obrigatório se `camada=gerencial`. Valores: `Anual`, `Mensal`, `Semanal`, `Continua`, ou variantes (`Anual + revisões semestrais`). |
| `highlight` | bool | ✓ | Se `true`, vira `.process-box highlight` (fundo lime). Max 2 na cadeia. |
| `blue_accent` | bool | ✓ | Se `true`, vira `.process-box blue-accent` (fundo azul). Max 1 na cadeia. |
| `sipoc` | object | n2 | Obrigatório se `n2` em `artefatos_a_gerar`. Ver 3.4.1. |
| `n3` | object | n3 | Obrigatório se `n3` ou `n4-pdf` em `artefatos_a_gerar`. Ver 3.4.2. |

#### 3.4.1 — `sipoc`

| Campo | Tipo | Obrigatório | Notas |
|---|---|---|---|
| `verbo` | string | ✓ | 1-2 palavras. Não pode ser `Fazer\|Realizar\|Gerenciar\|Executar\|Cuidar\|Tratar` (regra VERB-GENERIC). |
| `objeto` | string | ✓ | Substantivo claro. |
| `finalidade` | string | ✓ | Vem depois de "para". Explicita o porquê. |
| `inputs` | list[string] | ✓ | 3-6 chips. 2-4 palavras cada. |
| `outputs` | list[string] | ✓ | 3-6 chips. **Não pode repetir** itens de `inputs` (regra IO-DUP). |
| `owner` | string | ✓ | Cargo + (opcional) fórum. Não pode ser nome próprio (regra OWNER-PESSOA). |

#### 3.4.2 — `n3`

| Campo | Tipo | Obrigatório | Notas |
|---|---|---|---|
| `coluna` | string | ✓ | `gerencial` \| `front` \| `nucleo-l` \| `nucleo-r` \| `back` \| `apoio`. |
| `posicao` | object | ✓ | `{ left: int, top: int }` em `%` (0-100). |
| `friction.is_friction` | bool | ✓ | Se `true`, recebe halo pulsante vermelho no mapa. |
| `friction.text` | string | friction | Obrigatório se `is_friction=true`. Descreve o problema. |

### 3.5 — `relacoes[]` (cada item)

| Campo | Tipo | Obrigatório | Notas |
|---|---|---|---|
| `from` | string | ✓ | Código de processo. **Deve existir** em `processos[]` (regra REL-ORFA). |
| `to` | string | ✓ | Código de processo. **Deve existir** em `processos[]`. |
| `kind` | string | ✓ | `cliente` \| `info` \| `decisao`. |
| `label` | string | ✓ | 3-6 palavras. Descreve o que flui. |
| `forca` | string | cliente | `strong` \| `mid` \| `soft`. Obrigatório se `kind=cliente`. Define espessura da aresta. |

---

## 4. Seções markdown

Após o frontmatter, 5 seções fixas (em português, ordem rígida):

### 4.1 — `# Briefing — Cadeia de Valor {empresa}`

Header H1 com nome da empresa interpolado. Linha de status logo abaixo:
```markdown
> **Status**: rascunho · **Owner**: Bruno Chiaramonti · **Atualizado**: 2026-05-06
```

### 4.2 — `## Objetivo do diagrama`

2-3 linhas. Por que mapear **agora**? Qual decisão este diagrama suporta? Ex.:
> Documentar a cadeia atual antes do redesenho do CRM (H1-03), para que o novo fluxo de dados respeite as fronteiras de processo existentes.

### 4.3 — `## Lede do documento`

1-2 linhas. **Aparece literalmente** no campo `lede` do header do N1 (`{{LEDE_DOCUMENTO}}` → este texto).

### 4.4 — `## Contexto da empresa`

Setor, modelo de negócio, BUs, segmentação, qualquer referência relevante. Pode ter sub-bullets.

### 4.5 — `## Notas de iteração`

**Mantida pela skill** (não apagar histórico). Cada entrada é uma linha com `- {data} — {fato}`. Audita decisões tomadas durante a Fase A.

### 4.6 — `## Anexos / referências`

Links para PE, brandbook, cadeia anterior, briefings. Mantém em formato `- Nome: link://...`.

---

## 5. Validação

### Determinística (sempre roda primeiro)
`scripts/check_briefing.py <arquivo>` — saída JSON. Roda:
- Schema YAML (campos obrigatórios, tipos)
- Cross-checks (`contagens` vs `processos[]`, total)
- Regras de [`critique-rules.md`](critique-rules.md) que tem detecção determinística

Saída: `{ "ok": bool, "bloqueadores": [...], "avisos": [...] }`. Sai com código 0 se ok=true, 1 se bloqueadores != [].

### LLM (`process-critic` subagent)
Roda **depois** do determinístico. Aplica regras semânticas (verbos abstratos, missão como atividade, taxonomia incoerente). Devolve relatório markdown estruturado.

Detalhes em [`phase-a-entrevista-critica.md`](phase-a-entrevista-critica.md).

---

## 6. Convenções

- **Encoding**: UTF-8 sem BOM. Acentos permitidos em strings (frontmatter), mas não no `slug`.
- **YAML strings**: aspas duplas para strings com `:` ou `,`. Plain (sem aspas) caso contrário.
- **Listas inline**: ok para chips curtos (`inputs: ["a", "b", "c"]`). Listas longas usam formato `-`.
- **Comentários**: `#` no YAML para anotar campos opcionais ou exemplos. **Nunca** comente campos obrigatórios.
- **Datas**: formato livre nas seções markdown, mas `data_referencia` é `"Mês / Ano"` (com espaços).
- **Não duplicar**: `total_processos` é redundante com `len(processos[])` mas obrigatório — humano revisa o número diretamente.
- **`{{placeholder}}`**: aceito como valor de string apenas durante rascunho. `check_briefing.py` reporta como TODO. Bloqueia geração se não resolvido.
