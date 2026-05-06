# Regras de Crítica · BRIEFING.md

Catálogo das regras aplicadas ao BRIEFING durante a Fase A (entrevista crítica). Cada regra tem **ID estável**, severidade, descrição, mecânica de detecção e exemplos bom × ruim.

Regras determinísticas (regex / cross-check / set diff) são executadas por [`scripts/check_briefing.py`](../scripts/check_briefing.py). Regras semânticas exigem LLM e são aplicadas pelo subagent [`process-critic`](../agents/process-critic.md).

## Sumário

1. [Severidades](#severidades)
2. [Regras determinísticas](#regras-determinísticas)
3. [Regras semânticas (process-critic)](#regras-semânticas-process-critic)
4. [Como reportar uma violação](#como-reportar-uma-violação)
5. [Convenções de auditoria](#convenções-de-auditoria)

---

## Severidades

| Severidade | Comportamento |
|---|---|
| **bloqueador** | Impede a Fase C (geração de artefatos). Usuário deve corrigir ou explicitamente registrar exceção em `validacao.bloqueadores_aceitos` no BRIEFING. |
| **aviso** | Recomenda correção mas não bloqueia. Vai para `validacao.avisos`. Aparece no warning de geração. |

Política: bloqueadores são reservados para violações que comprometem **integridade do mapeamento** (campo obrigatório ausente, código órfão, owner inválido, missão sem finalidade). Avisos são para questões de **qualidade que podem deslizar** se justificadas (verbo fraco contextualmente aceito, chip levemente longo, processo de fronteira de camada).

---

## Regras determinísticas

Aplicadas por `scripts/check_briefing.py`. Detecção sem LLM.

### Schema e estrutura

| ID | Severidade | Detecção | Mensagem |
|---|---|---|---|
| **SCHEMA-MISSING** | bloqueador | Campo raiz obrigatório ausente | `Campo obrigatorio ausente: {field}` |
| **SCHEMA-VERSION** | bloqueador | `schema_version != 1` | Bumpa schema quando breaking change |
| **EMPRESA-INCOMPLETA** | bloqueador | Campo de `empresa.{nome,slug,setor,escopo}` ausente | Identidade incompleta |
| **SLUG-INVALIDO** | bloqueador | Slug não casa `^[a-z0-9-]+$` | Sem acentos, kebab-case |
| **VARIANTE-INVALIDA** | bloqueador | `n1.variante ∉ {A, B}` | Use A (master) ou B (linear) |
| **CONTAGENS-FORMATO** | bloqueador | `n1.contagens` não é dict | Esperado `{gerenciais, primarios, apoio}` |
| **CONTAGENS-MISSING** | bloqueador | Faltando uma das 3 chaves | Todas obrigatórias |

### Cross-checks numéricos

| ID | Severidade | Detecção | Mensagem |
|---|---|---|---|
| **CONTAGEM-MISMATCH** | bloqueador | `contagens[k]` ≠ `len(processos com camada=k)` | Inconsistência declarada vs real |
| **TOTAL-MISMATCH** | bloqueador | `total_processos` ≠ `len(processos[])` | Total declarado errado |
| **CODIGO-DUPLICADO** | bloqueador | Mesmo `codigo` em > 1 processo | Códigos devem ser únicos |
| **PROCESSOS-VAZIO** | bloqueador | `processos[]` vazio | Mapeamento sem processos |

### Camadas e processos

| ID | Severidade | Detecção | Mensagem |
|---|---|---|---|
| **CAMADA-PROIBIDA** | bloqueador | `camada ∉ {gerencial, primario, apoio}` | Sem 4ª camada |
| **SUBCAMADA-INVALIDA** | bloqueador | `subcamada ∉ {front, nucleo, back}` | Só para primários variante A |
| **PROCESSO-INCOMPLETO** | bloqueador | `codigo`, `camada`, `nome` ou `tooltip` ausente | Campos básicos obrigatórios |
| **GERENCIAL-SEM-FREQ** | bloqueador | `camada=gerencial` sem `frequencia` | Define cadência |
| **GERENCIAL-TOOLTIP-FREQ** | aviso | Tooltip sem linha `Freq: ...` | Padrão visual M7 |
| **NOME-LONGO** | aviso | Nome com > 3 palavras | Use `&` em vez de `e` |
| **HIGHLIGHT-EXCESSO** | aviso | > 2 processos com `highlight: true` | Limite M7: 2 |
| **BLUE-EXCESSO** | aviso | > 1 processo com `blue_accent: true` | Limite M7: 1 |
| **PRIM-NUMERO** | aviso | < 3 ou > 9 primários | Faixa saudável: 3-9 |

### SIPOC

| ID | Severidade | Detecção | Mensagem |
|---|---|---|---|
| **SIPOC-AUSENTE** | bloqueador | Bloco `sipoc` faltando quando `n2` em artefatos | SIPOC obrigatório se gera N2 |
| **VERB-GENERIC** | bloqueador | Verbo ∈ `{Fazer, Realizar, Gerenciar, Executar, Cuidar, Tratar}` | Use Construir, Operar, Garantir... |
| **VERB-WEAK** | aviso | Verbo ∈ lista de 25 fracos (Trabalhar, Atuar, Lidar...) | Considere especificidade |
| **SIPOC-VERBO-VAZIO** | bloqueador | `verbo` é string vazia | Defina o verbo principal |
| **MISSAO-LISTA** | aviso | `finalidade` sem "para" explícito | Reescreva no formato `para X` |
| **IO-DUP** | bloqueador | Termo aparece em `inputs` E `outputs` | Decida: entra ou sai? |
| **CHIPS-FORA-FAIXA** | aviso | `inputs` ou `outputs` < 3 ou > 6 itens | Faixa: 3-6 |
| **SIPOC-CHIP-LONGO** | aviso | Chip com > 4 palavras | Encurte |
| **OWNER-PESSOA** | bloqueador | Owner sem marcador de cargo (CEO, Head, Diretor, Comitê...) | Sempre cargo, nunca nome próprio |
| **OWNER-VAZIO** | bloqueador | Campo `owner` vazio | Define o cargo responsável |

### N3 (mapa neural)

| ID | Severidade | Detecção | Mensagem |
|---|---|---|---|
| **N3-AUSENTE** | bloqueador | Bloco `n3` faltando quando `n3` ou `n4-pdf` em artefatos | N3 obrigatório se gera mapa |
| **N3-COLUNA-INVALIDA** | bloqueador | `coluna` fora de `{gerencial, front, nucleo-l, nucleo-r, back, apoio}` | 6 colunas válidas |
| **N3-POSICAO-INVALIDA** | bloqueador | `posicao.left` ou `posicao.top` fora de [0, 100] | Em % do canvas |
| **FRICTION-SEM-TEXT** | bloqueador | `is_friction=true` sem `text` preenchido | Descreva o problema |
| **FRICCAO-EXCESSO** | aviso | > 4 processos com fricção | Limite M7: 4 |

### Relações

| ID | Severidade | Detecção | Mensagem |
|---|---|---|---|
| **RELACOES-VAZIO** | aviso | `relacoes[]` vazia mas N3 será gerado | Mapa neural sem arestas |
| **RELACAO-INCOMPLETA** | bloqueador | `from`, `to`, `kind` ou `label` ausente | Campos básicos obrigatórios |
| **REL-ORFA** | bloqueador | `from` ou `to` não existe em `processos[]` | Typo ou processo removido? |
| **KIND-INVALIDO** | bloqueador | `kind ∉ {cliente, info, decisao}` | 3 tipos canônicos |
| **FORCA-AUSENTE** | bloqueador | `kind=cliente` sem `forca` | strong / mid / soft |
| **FORCA-INVALIDA** | bloqueador | `forca ∉ {strong, mid, soft}` | 3 níveis canônicos |
| **REL-DUPLICA** | aviso | Mesmo par `(from, to)` com kinds diferentes | Escolha kind dominante |

### Artefatos

| ID | Severidade | Detecção | Mensagem |
|---|---|---|---|
| **ARTEFATO-INVALIDO** | bloqueador | Item fora de `{n1, n2, n3, n4-pdf}` | 4 artefatos válidos |
| **PDF-DEPENDENCIA** | bloqueador | `n4-pdf` listado sem `n1`/`n2`/`n3` | Sequência rígida |

### Placeholders

| ID | Severidade | Detecção | Mensagem |
|---|---|---|---|
| **PLACEHOLDER-NAO-RESOLVIDO** | aviso | String contém `{{...}}` | Substitua antes de gerar |

---

## Regras semânticas (process-critic)

Aplicadas pelo subagent [`process-critic`](../agents/process-critic.md). Exigem LLM porque envolvem julgamento.

### MISSAO-COMO-ATIVIDADE

**Severidade**: bloqueador
**Detecção**: A missão (`verbo + objeto + finalidade`) descreve **passos** ou **atividades** em vez do propósito. Tipicamente quando há vírgulas múltiplas, conectores "e", ausência de finalidade clara.

**Exemplo ruim**:
```yaml
verbo: "Realizar"
objeto: "reuniões mensais com diretoria, revisar KPIs e ajustar metas"
finalidade: ""
```

**Exemplo bom**:
```yaml
verbo: "Acompanhar"
objeto: "a execução estratégica"
finalidade: "para corrigir desvios e proteger metas anuais"
```

### TAXONOMIA-INCOERENTE

**Severidade**: aviso
**Detecção**: Processo classificado em camada que não combina com seu conteúdo. Tipicamente:
- Processo com verbo "Atender", "Vender", "Operar cliente" classificado em `apoio`
- Processo de "Política", "Diretriz", "Aprovação" classificado em `primario`
- Processo com `frequencia` (Mensal, Semanal) classificado em `apoio` ou `primario`

**Exemplo ruim**:
```yaml
- codigo: "A1"
  camada: "apoio"
  nome: "Comercial Empresarial"
  sipoc: { verbo: "Vender" }
```

**Sugestão**: Reclassificar como `primario`. Apoio é serviço/infra interna; comercial gera receita direta.

### NOME-AMBIGUO

**Severidade**: aviso
**Detecção**: Nome do processo é genérico demais para identificar o que faz.
- "Operações", "Gestão", "Atendimento" sem qualificador
- "Comercial" sem indicar fronteira (B2B? B2C? alta renda?)

**Exemplo ruim**: `Comercial`
**Exemplo bom**: `Aquisicao & Onboarding`, `Vendas Wealth`

### SIPOC-INPUT-FANTASMA

**Severidade**: bloqueador
**Detecção**: Input citado não tem origem clara em outro processo do mapeamento. Tipicamente "magia" — algo que aparece sem origem.

**Exemplo ruim**:
```yaml
inputs: ["Decisão estratégica do board"]   # se G1 não está mapeado
```

**Sugestão**: Mapear o processo que produz o input ou marcar input como "external" no formato `(externo) Decisão do board`.

### SIPOC-OUTPUT-ORFAO

**Severidade**: aviso
**Detecção**: Output citado não é consumido por nenhum outro processo nem citado nas relações.

**Exemplo**: Processo G2 produz "Relatório de aderência" mas nenhum outro processo recebe esse output.

**Sugestão**: Mapear processo que consome ou marcar como output terminal (consumo externo, ex.: regulador, board).

### FRONTEIRA-FUZZY

**Severidade**: aviso
**Detecção**: Dois processos têm responsabilidades sobrepostas (mesmos inputs e/ou outputs muito similares).

**Exemplo**: P1 "Geração de Demanda" e P2 "Aquisição & Onboarding" ambos com input `Lead bruto` e output `Lead qualificado`.

**Sugestão**: Esclarecer fronteira (P1 entrega MQL; P2 converte MQL em SQL/cliente).

### CICLO-COMPLETO-AUSENTE

**Severidade**: aviso
**Detecção**: Para verticais (núcleo), espera-se que o ciclo `front → núcleo → back → loop` esteja presente nas relações. Se P1/P2 não conectam ao núcleo, ou núcleo não conecta ao back-end, há quebra de jornada.

**Sugestão**: Adicionar relações de cliente que fechem o ciclo, ou explicitar que jornada termina no núcleo (`P3 → P9` direto).

### FRICCAO-SEM-CAUSA

**Severidade**: aviso
**Detecção**: Texto de fricção descreve **sintoma** (`perde leads`) sem causa raiz (`por quê`?).

**Exemplo ruim**: `Handoff falha`
**Exemplo bom**: `Handoff manual P1→P2 perde 20% dos leads. Sem CRM unificado, lead esfria entre marketing e comercial.`

---

## Como reportar uma violação

Tanto o validador determinístico quanto o `process-critic` reportam no formato:

```markdown
## Bloqueadores
- [REGRA-ID] {where} — {message}
  Sugestão: {ação concreta}

## Avisos
- [REGRA-ID] {where} — {message}
  Sugestão: {ação concreta}

## Sugestões livres (opcional)
- {observação semântica que não casa com nenhuma regra}
```

`{where}` cita o caminho YAML do problema (ex.: `processos[3].sipoc.owner (P3)`). Permite o usuário ir direto ao ponto.

---

## Convenções de auditoria

Quando o usuário aceita um bloqueador (decide seguir mesmo assim), registra em `validacao.bloqueadores_aceitos`:

```yaml
bloqueadores_aceitos:
  - rule_id: "VERB-GENERIC"
    where: "processos[15].sipoc.verbo (A3)"
    accepted_at: "2026-05-06"
    rationale: "Verbo aceito porque A3 (Financeiro) é por natureza administrativo. Usar 'Administrar' é mais preciso que alternativas para esse contexto."
```

Quando aceita uma sugestão do critic, anota em `## Notas de iteração` no markdown:

```markdown
- 2026-05-06 — verbo `Gerenciar` em G2 substituído por `Garantir` (sugestão do critic)
- 2026-05-06 — `Plano estratégico` aparecia em input e output de G1, mantido só no output
```

Histórico **não é apagado**. Audita decisões e justifica desvios em revisões futuras.
