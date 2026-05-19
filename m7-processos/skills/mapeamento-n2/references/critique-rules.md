# Catálogo de regras de crítica · mapeamento-n2

Catálogo usado por:
- `scripts/check_ssot.py` (regras **determinísticas** — regex, set diff, length, enum)
- `agents/n2-interview-critic.md` (regras **semânticas** — leitura crítica)
- `agents/n2-build-critic.md` (regras **de build** — HTML/JS render)

## Convenções de severidade

- **bloqueador** — impede avanço (Fase A → B ou B → C)
- **aviso** — recomendado corrigir, não bloqueia
- **sugestão** — observação livre, decisão do usuário

---

## Regras determinísticas (check_ssot.py)

### Estruturais (todos os MDs)

| Rule ID | Severidade | Onde | Descrição |
|---|---|---|---|
| SCHEMA-MISSING | bloqueador | root | Campo raiz obrigatório ausente |
| SCHEMA-VERSION | bloqueador | root.schema_version | Deve ser 1 no MVP |
| YAML-INVALIDO | bloqueador | parsing | Frontmatter YAML mal formado |
| SLUG-INVALIDO | bloqueador | slug | Não é kebab-case |

### N1 handoff (processo-n2.md)

| Rule ID | Severidade | Onde | Descrição |
|---|---|---|---|
| N1-BRIEFING-AUSENTE | bloqueador | n1_artifacts.briefing | Arquivo não existe no path informado |
| N1-CODIGO-NAO-ENCONTRADO | bloqueador | processo.code | Code não consta em processos[] do BRIEFING N1 |
| POLITICA-AUSENTE | aviso | n1_artifacts.politica | Recomendado para rastreabilidade |

### Processo N2 (processo-n2.md)

| Rule ID | Severidade | Onde | Descrição |
|---|---|---|---|
| PROCESSO-CODE-INVALIDO | bloqueador | processo.code | Não casa regex `^[PGA]\d+(\.\d+)?$` |
| CAMADA-INVALIDA | bloqueador | processo.camada | Fora de {gerencial, primario, apoio} |
| OWNER-PESSOA | bloqueador | processo.owner / subprocessos[].owner | Falta marcador de cargo |
| SUBPROCESSOS-FAIXA | bloqueador | subprocessos | Count fora de [3..8] |
| SUBPROCESSO-INCOMPLETO | bloqueador | subprocessos[i].* | Falta id/code/name/owner/cadence/sp_meta/sp_tech |
| SUBPROCESSO-CODE-DUP | bloqueador | subprocessos[] | Codes repetidos |
| INTERFACES-COUNT | bloqueador | interfaces | Length ≠ subprocessos.length |
| INTERFACES-CODE-ORFA | bloqueador | interfaces[i].code | Não casa nenhum subprocessos[].code |
| LEDE-AUSENTE | bloqueador | seção `## Lede` | Falta seção ou < 30 chars |
| SP-META-LONGO | aviso | subprocessos[].sp_meta | > 60 chars (não cabe no card) |
| SP-TECH-LONGO | aviso | subprocessos[].sp_tech | > 80 chars |

### SIPOC (sipocs.md)

| Rule ID | Severidade | Onde | Descrição |
|---|---|---|---|
| VERB-GENERIC | bloqueador | subprocessos[].purpose | Começa com {fazer, realizar, gerenciar, executar, cuidar, tratar} |
| VERB-WEAK | aviso | subprocessos[].purpose | Verbo abstrato (lista da N1) |
| PURPOSE-VAZIO | bloqueador | subprocessos[].purpose | Vazio ou < 30 chars |
| PURPOSE-LONGO | aviso | subprocessos[].purpose | > 200 chars |
| IO-DUP | bloqueador | subprocessos[i].outputs[].what | Duplicado em inputs[].what (pass-through) |
| IO-COUNT | bloqueador | subprocessos[].inputs/outputs | Length fora de [3..5] |
| ETAPAS-FAIXA | bloqueador | subprocessos[].etapas | Length fora de [4..8] |
| ETAPA-LONGA | aviso | subprocessos[].etapas[i] | > 80 chars |
| REG-FAIXA | bloqueador | subprocessos[].regulacao | Length fora de [2..4] |
| SUP-FAIXA | bloqueador | subprocessos[].suporte | Length fora de [2..4] |
| REG-CODE-INVALIDO | bloqueador | subprocessos[].regulacao[].code | Fora de {R1..R4} |
| SUP-CODE-INVALIDO | bloqueador | subprocessos[].suporte[].code | Fora de {S1..S4} |
| DETAIL-AUSENTE | aviso | inputs/outputs/regulacao/suporte | Sem `detail` |

### Jornada CX (jornada-cx.md)

| Rule ID | Severidade | Onde | Descrição |
|---|---|---|---|
| ROWS-COUNT | bloqueador | rows | Length ≠ 4 |
| ROWS-ID-INVALIDO | bloqueador | rows[].id | Fora de {touchpoint, action, mot, pain} |
| ROWS-ID-DUP | bloqueador | rows[] | IDs repetidos |
| CELLS-COUNT | bloqueador | rows[].cells | Length ≠ processos.length |
| MOT-INTENSITY-INVALIDA | bloqueador | rows[id=mot].cells[].intensity | Fora de {1, 2, 3} |
| MOT-ITEMS-VAZIO | bloqueador | rows[id=mot].cells[].items | Vazio |
| PAIN-TONE-INVALIDO | bloqueador | rows[id=pain].cells[].tone | Fora de {+, -, ~} |
| PAIN-ITEMS-VAZIO | bloqueador | rows[id=pain].cells[].items | Vazio |
| TONE-INVALIDO | bloqueador | processos[].tone | Fora de {a, b, c, d, e} |
| PAIN-ITEM-SEM-ASPAS | aviso | rows[id=pain].cells[].items[] | Não começa com `"` |

### Data Lake (data-lake.md)

| Rule ID | Severidade | Onde | Descrição |
|---|---|---|---|
| ROWS-COUNT | bloqueador | rows | Length ≠ 2 |
| ROWS-ID-INVALIDO | bloqueador | rows[].id | Fora de {systems, data} |
| KIND-INVALIDO | bloqueador | rows[id=data].cells[][].kind | Fora do enum |
| MARTS-DIM-FAIXA | bloqueador | marts.dim | Length < 3 |
| MARTS-FACT-FAIXA | bloqueador | marts.fact | Length < 3 |
| CONSUMERS-FAIXA | bloqueador | consumers | Length < 4 |
| MART-DIM-NOME-INVALIDO | bloqueador | marts.dim[].name | Não começa com `dim_` |
| MART-FACT-NOME-INVALIDO | bloqueador | marts.fact[].name | Não começa com `fact_` |
| CONSUMER-TIER-DUP | bloqueador | consumers[] | Tier repetido |

### Cross-checks transversais (`check_ssot.py --all`)

| Rule ID | Severidade | Onde | Descrição |
|---|---|---|---|
| SUBPROC-MISMATCH | bloqueador | sipocs.md vs processo-n2.md | Set de codes difere |
| SUBPROC-ORDEM-MISMATCH | aviso | sipocs.md vs processo-n2.md | Ordem difere |
| JORNADA-PROCESSOS-MISMATCH | bloqueador | jornada-cx.md vs processo-n2.md | Set de codes difere |
| DATALAKE-PROCESSOS-MISMATCH | bloqueador | data-lake.md vs processo-n2.md | Set de codes difere |
| DATALAKE-MARTS-CONSUMERS-ORFAOS | aviso | data-lake.md | Algum mart sem consumer ou vice-versa |

---

## Regras semânticas (n2-interview-critic)

| Rule ID | Severidade | Descrição |
|---|---|---|
| MISSAO-COMO-ATIVIDADE | bloqueador | Purpose descreve passos em vez de finalidade (~"Receber, validar e enviar") |
| FRONTEIRA-FUZZY | bloqueador | 2 subprocessos com escopo sobreposto sem critério claro de transição |
| SIPOC-INPUT-FANTASMA | aviso | input.from cita subproc/ator que não existe na cadeia |
| SIPOC-OUTPUT-ORFAO | aviso | output.to não é consumido por ninguém (subproc seguinte não cita esse input) |
| MOT-SEM-INFLEXAO | aviso | Item de MoT é descrição operacional, não inflexão emocional |
| PAIN-CORPORATIVO | aviso | Pain item não é fala do cliente, é interpretação do gestor |
| PAIN-MONOTONO | sugestão | Todos os subprocs têm pain tone `-` (provavelmente faltou nuance) |
| MOT-INTENSIDADE-MONOTONA | sugestão | Todos os MoT têm intensity=3 (perde gradiente) |
| MART-SEM-CONSUMER | aviso | Mart `dim_X` ou `fact_X` não tem consumer que claramente o usa |
| CONSUMER-SEM-MART | aviso | Consumer descreve uso de dado que não está em marts[] |
| REGULACAO-INADEQUADA | aviso | Regulação não aderente ao setor (ex.: FIDC sem CVM 175) |
| TAXONOMIA-INCOERENTE | bloqueador | Processo classificado em camada errada (puxa do BRIEFING N1) |

---

## Regras de build (n2-build-critic)

| Rule ID | Severidade | Descrição |
|---|---|---|
| PLACEHOLDER-RESTANTE | bloqueador | `{{...}}` ainda presente no HTML gerado |
| JS-OBJETO-MALFORMADO | bloqueador | Erro de sintaxe JS no `dados-*.js` ou `journey-*.js` |
| SUBPROC-COUNT-MISMATCH | bloqueador | Quantidade de cards/colunas no HTML difere de subprocessos[] no SSOT |
| ASSETS-AUSENTES | bloqueador | CSS, font, ou logo faltando em `build/` |
| TABS-QUEBRADAS | bloqueador | Nav tabs apontam para arquivo inexistente |
| LEDE-VAZIA | aviso | `<p class="lede">` vazio no HTML (ssot/processo-n2.md tem Lede mas escapou no build) |
