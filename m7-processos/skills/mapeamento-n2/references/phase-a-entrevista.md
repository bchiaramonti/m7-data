# Fase A · Entrevista crítica

Documento de apoio à [SKILL.md](../SKILL.md) · Fase A.

## Sumário

1. [Filosofia](#1-filosofia)
2. [Os 5 blocos](#2-os-5-blocos)
3. [Como conduzir checkpoints](#3-como-conduzir-checkpoints)
4. [Anexos como respostas válidas](#4-anexos-como-respostas-válidas)
5. [Invocação do n2-interview-critic](#5-invocação-do-n2-interview-critic)
6. [Loop de iteração (max 3 rounds)](#6-loop-de-iteração-max-3-rounds)
7. [Output: entrevista.md](#7-output-entrevistamd)

---

## 1. Filosofia

A Fase A **não produz o SSOT**. Produz o **material bruto exaustivo** que vai virar SSOT na Fase B.

Por que separar? Porque o usuário pensa em linguagem de negócio, não em YAML. Forçar a estrutura YAML durante a entrevista interrompe o raciocínio. A entrevista vira um log estruturado de perguntas+respostas; a Fase B traduz em SSOT.

Vantagem secundária: se o usuário anexa um doc de referência (Manual operacional, PE, política N1), a entrevista marca **"respondida por anexo X"** em vez de transcrever — preserva rastreabilidade e evita duplicação.

---

## 2. Os 5 blocos

Cada bloco tem perguntas numeradas (Q1.1, Q1.2, ...) e respostas anotadas. Use [`../ENTREVISTA.tmpl.md`](../ENTREVISTA.tmpl.md) como esqueleto.

| Bloco | Quando rodar | Duração típica | Saída |
|---|---|---|---|
| **1 · Contexto N1** | Sempre primeiro. Lê BRIEFING N1 e Política se existir | 5-10 min | Seção `## Bloco 1` |
| **2 · Decomposição** | Após confirmar Bloco 1 | 10-15 min | Tabela de N subprocessos |
| **3 · SIPOC** | Para cada subproc., um sub-bloco. **Não é o build SIPOC** — é só captura | 15-25 min/subproc. | Seção `## SIPOC · {code}` (xN) |
| **4 · Jornada CX** | Depois de TODOS os SIPOCs capturados | 15-20 min | Seção `## Jornada CX` (4 rows × N) |
| **5 · Data Lake** | Depois da Jornada CX | 15-20 min | Seção `## Data Lake` (systems+data xN + marts+consumers globais) |

Total típico: 90-120 min para um processo de 5 subprocessos com usuário preparado e anexos.

### Checkpoint ao final de cada bloco

Antes de avançar, valide com o usuário:
- "Confirma que os N subprocessos cobrem o end-to-end? Falta algo entre P5.2 e P5.3?"
- "Owner do P5.3 — você falou 'Filipe' (nome próprio). Qual o cargo/comitê? (Skill bloqueia owner como nome próprio)"

Anote no `entrevista.md` os checkpoints aceitos. Se houve correção, **edite a resposta original** e adicione `[corrigido em checkpoint]`.

---

## 3. Como conduzir checkpoints

**Heurísticas leves no prompt**, sem rodar `check_ssot.py` ainda (porque o SSOT ainda não existe). Padrões a observar:

- **Verbo genérico no Bloco 3 (purpose)** — "fazer", "realizar", "gerenciar" → pedir reformulação ("Construir, Operar, Garantir, Validar, Coordenar")
- **Owner com nome próprio** → reformular para cargo/comitê
- **inputs == outputs no SIPOC** → "Isso seria pass-through; o subprocesso não transforma. Faltou algo no meio?"
- **Etapas com < 4 ou > 8 passos** → discutir granularidade (não é N3, é N2 — passos macro)
- **MoT sem inflexão emocional clara** → "Esse momento muda algo na percepção do cliente? Se não, vire só Action"
- **Pain points sem aspas no formato cliente-fala** → "Como o cliente literalmente diria isso?"
- **Data kind fora do enum** → pedir reclassificação ({CRM, PII, Score, Bureau, Doc, Contrato, Lastro, Tesouraria, Cobrança, KPI})

---

## 4. Anexos como respostas válidas

Quando o usuário envia um doc no início (ex.: `politica-m7.html` da N1, manual operacional anterior, PE 2026):

1. **Liste o doc na seção `## Anexos consultados`** com checkbox marcado
2. Para cada bloco/pergunta que o doc cobre, anote `**R**: respondida por anexo `politica-m7.html` §4.2 — citado abaixo` e cole 1-2 linhas de citação
3. **Só pergunte ao usuário o que o anexo não cobriu**

Exemplo: se a Política N1 já lista os 3 papéis aprovadores (Elaborador / Revisor / Aprovador) e seus cargos, no Bloco 1 a pergunta "quem é o owner?" pode ser respondida por anexo. **Mas confirme** com o usuário: "A Política diz `Diretor Comercial` — esse é o owner do P5 também ou é outro?"

---

## 5. Invocação do n2-interview-critic

Ao final do **Bloco 5**, antes de declarar a Fase A pronta:

```
Invoke agent: n2-interview-critic
Args: path=entrevista.md, round=1
```

O agent lê `entrevista.md` + `references/critique-rules.md` e devolve markdown com:
- **Bloqueadores** — gaps semânticos que impedem Fase B (campos vazios, owners genéricos, fronteiras fuzzy não resolvidas)
- **Avisos** — recomendado corrigir mas não bloqueia
- **Sugestões livres** — observações analíticas

Cole o output na seção `## Validação final · n2-interview-critic` do `entrevista.md`.

---

## 6. Loop de iteração (max 3 rounds)

```
Round 1: invoca critic → relatório
  ├── 0 bloqueadores? → Fase A pronta, avança para Fase B
  └── X bloqueadores? → usuário corrige no entrevista.md (responde perguntas em aberto, refina respostas) → Round 2
Round 2: re-invoca critic → relatório
  ├── 0 bloqueadores? → avança
  └── X bloqueadores? → Round 3
Round 3: re-invoca critic
  ├── 0 bloqueadores? → avança
  └── X bloqueadores? → ESCALA: opções: (1) aceitar bloqueador com rationale escrito em `## Validação final`,
                        (2) pausar e re-entrevistar com mais informação prévia
```

**Não há Round 4.** Se chegou a 3 com bloqueadores, é sintoma de mapeamento estrutural raso — voltar pra fonte é mais eficiente que iterar.

---

## 7. Output: entrevista.md

O arquivo final fica em `{diretorio-trabalho}/entrevista.md` (não em `ssot/` — ssot/ é só para os 4 MDs canônicos da Fase B).

Estrutura:
```
entrevista.md
├── frontmatter pequeno (data, entrevistador, entrevistados, ref BRIEFING N1, round)
├── ## Anexos consultados
├── ## Bloco 1 · Contexto N1
├── ## Bloco 2 · Decomposição
├── ## Bloco 3 · SIPOC · {code-1}     (xN)
├── ## Bloco 4 · Jornada CX
├── ## Bloco 5 · Data Lake
├── ## Notas livres da entrevista
└── ## Validação final · n2-interview-critic     (output do agent, atualiza por round)
```

Não envie `entrevista.md` para nenhum downstream — ela é só insumo para a Fase B. Mantenha no diretório de trabalho para auditoria.
