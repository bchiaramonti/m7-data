# Fase A · Entrevista & Crítica iterativa

Documento de apoio à [SKILL.md](../SKILL.md). Detalha a Fase A do pipeline: 5 blocos de entrevista, checkpoints leves por bloco e invocação do `process-critic` no fechamento.

## Sumário

1. [Princípios](#1-princípios)
2. [Bloco 1 · Identidade](#2-bloco-1--identidade)
3. [Bloco 2 · Estrutura macro](#3-bloco-2--estrutura-macro)
4. [Bloco 3 · Detalhamento dos primários](#4-bloco-3--detalhamento-dos-primários)
5. [Bloco 4 · Demais camadas](#5-bloco-4--demais-camadas)
6. [Bloco 5 · Confirmação + critic](#6-bloco-5--confirmação--critic)
7. [Loop de iteração](#7-loop-de-iteração)
8. [Como aplicar correções](#8-como-aplicar-correções)

---

## 1. Princípios

1. **Uma pergunta por vez** — nunca despeje 4-5 perguntas em série. Use `AskUserQuestion` para coletar.
2. **Inferir do contexto** — se o usuário já forneceu informação no briefing inicial, não pergunte de novo.
3. **Validar ao final de cada bloco** — checkpoints leves (heurísticas no prompt) confirmam que o bloco fechou consistente antes de avançar.
4. **TodoWrite para rastreamento** — um item por bloco. Marca `completed` ao validar.
5. **BRIEFING.md cresce em cada bloco** — não espera o final para escrever. Cada bloco completa uma seção do frontmatter YAML + as seções markdown relevantes.
6. **Push-back proativo** — se o usuário responde com algo que viola regra (ex.: nome com 5 palavras), corrija no momento, não acumule para o critic.

---

## 2. Bloco 1 · Identidade

**Objetivo**: preencher o cabeçalho do BRIEFING (`empresa`, `data_referencia`, `versao`, `area_documento`, `logo`).

**Perguntas** (use `AskUserQuestion`):

1. Nome da empresa e setor.
2. Escopo do diagrama (toda a holding? uma BU? um produto?).
3. Data de referência (mês/ano).
4. Logo próprio? (caso contrário usar M7 padrão).

**Inferência**:
- Slug deriva do nome (kebab-case sem acentos). Confirme com o usuário antes de salvar.
- Se o escopo é "BU específica", capture o nome no formato `bu:<nome>` (ex.: `bu:wealth`).

**Checkpoint** (heurísticas leves):
- [ ] Slug casa `^[a-z0-9-]+$`
- [ ] Data formatada `Mês / Ano` (ex.: `"Fev / 2026"`)
- [ ] Escopo é `holding` ou começa com `bu:` ou `produto:`
- [ ] Se logo ≠ "default", caminho fornecido aponta para PNG existente

**Saída** (BRIEFING parcial):
```yaml
empresa:
  nome: "{nome}"
  slug: "{slug}"
  setor: "{setor}"
  escopo: "{escopo}"
data_referencia: "{Mês / Ano}"
versao: "{MM/AA}"
area_documento: "{Área}"
logo: "default" | "{caminho}"
```

E preenche `## Contexto da empresa` no markdown (curto, 2-3 linhas que o usuário forneceu).

---

## 3. Bloco 2 · Estrutura macro

**Objetivo**: definir contagens por camada e listar os processos com nome (sem detalhar SIPOC ainda).

**Perguntas**:

1. Quantos **processos gerenciais** (estratégia, performance, compliance, orçamento)? Listar nomes (≤ 3 palavras cada).
2. Quantos **processos de apoio** (tech, jurídico, financeiro, pessoas, backoffice)? Listar nomes.
3. Os **primários** seguem `geração → núcleo → relacionamento` ou um fluxo linear? → escolhe **variante A** ou **B**.
4. Listar nomes dos primários (na ordem em que aparecem no fluxo).
5. (Variante A) Rótulo do bloco do núcleo (ex.: "Verticais de Produto", "Linhas de Negócio").

**Inferência**:
- Gerenciais geralmente são 3-5 (estratégia, performance, compliance, orçamento, governança).
- Primários geralmente são 3-9. Mais que 9 sinaliza escopo errado (talvez sejam subprocessos).
- Apoio geralmente são 3-6.

**Checkpoint** (heurísticas leves):
- [ ] Cada nome ≤ 3 palavras (regra NOME-LONGO)
- [ ] Cada camada ∈ `{gerencial, primario, apoio}` (regra CAMADA-PROIBIDA)
- [ ] Primários: 3-9 processos (regra PRIM-NUMERO)
- [ ] Variante: A ou B (regra VARIANTE-INVALIDA)
- [ ] Códigos atribuídos sequencialmente (G1..Gn, P1..Pn, A1..An), sem buracos

**Push-back proativo**:
- Se nome > 3 palavras, sugira contração com `&` ou abreviação ("Tecnologia da Informação" → "Tecnologia & Dados").
- Se primários < 3 ou > 9, confirme escopo: "Você está mapeando uma BU ou a holding inteira?"
- Se "Comercial" aparece como nome, peça especificação ("Geração de Demanda? Aquisição? Vendas?").

**Saída** (BRIEFING parcial):
```yaml
n1:
  variante: "A"
  rotulo_nucleo: "Verticais de Produto"
  total_processos: 18
  contagens: { gerenciais: 4, primarios: 9, apoio: 5 }

processos:
  - codigo: "G1"
    camada: "gerencial"
    nome: "Planejamento Estratégico"
    tooltip: []                      # vazio nesta etapa, preenche em Bloco 3-4
    # ...
```

---

## 4. Bloco 3 · Detalhamento dos primários

**Objetivo**: para cada primário, preencher `tooltip` (2-3 linhas), `highlight`, `blue_accent`, e SIPOC se `n2` ou `n4-pdf` está em `artefatos_a_gerar`.

**Perguntas (por processo)**:

1. **Tooltip** — 2-3 linhas telegráficas (o que faz, métrica/meta se houver).
2. **Foco estratégico?** — receberá `.highlight` (fundo lime). Limite: 2 na cadeia.
3. **Cross-sell / tech?** — receberá `.blue-accent` (fundo azul). Limite: 1 na cadeia.
4. (Se SIPOC) **Verbo + Objeto + Finalidade** — `Verbo` (1-2 palavras) `Objeto` `para Finalidade`.
5. (Se SIPOC) **Inputs** — 3-6 chips curtos (2-4 palavras): o que precisa chegar.
6. (Se SIPOC) **Outputs** — 3-6 chips curtos: o que o processo entrega para fora.
7. (Se SIPOC) **Owner** — Cargo + Fórum (ex.: `Head de Investimentos · Comitê de Alocação`).

**Inferência**:
- Para variantes A: identifique subcamada (`front`, `nucleo`, `back`) pela ordem de fluxo declarada no Bloco 2.
- Se o usuário descreveu a operação no contexto inicial, sugira tooltip baseado nessa descrição e peça confirmação.

**Checkpoint** (heurísticas leves):
- [ ] Tooltip 2-4 linhas (não vazio)
- [ ] Verbo não na lista proibida (regra VERB-GENERIC: Fazer/Realizar/Gerenciar/Executar/Cuidar/Tratar)
- [ ] Finalidade contém "para" (regra MISSAO-LISTA)
- [ ] Inputs e outputs disjuntos (regra IO-DUP)
- [ ] Inputs e outputs com 3-6 itens (regra CHIPS-FORA-FAIXA)
- [ ] Owner contém marcador de cargo (CEO/Head/Diretor/Comitê/etc.) — regra OWNER-PESSOA
- [ ] Total `highlight` ≤ 2, `blue_accent` ≤ 1 (regras HIGHLIGHT-EXCESSO / BLUE-EXCESSO)

**Push-back proativo**:
- Se verbo é "Gerenciar", ofereça opções: "Que tal `Construir`, `Operar`, `Garantir`, `Definir`, `Coordenar`?"
- Se input e output têm o mesmo termo, pergunte: "Esse item entra ou sai do processo? Decida."
- Se owner é nome próprio, peça cargo: "Pessoa muda; cargo permanece. Use `Head de X` ou `Diretor de Y`."

**Saída**: completa `tooltip`, `highlight`, `blue_accent`, e (se SIPOC) `sipoc` para cada primário no BRIEFING.

---

## 5. Bloco 4 · Demais camadas

**Objetivo**: completar gerenciais (com `frequencia` obrigatória) e apoio.

**Perguntas (por processo)**:

1. **Tooltip** — 2-3 linhas. Para gerenciais, **última linha deve começar com `Freq:`**.
2. **Frequência** (gerenciais) — Anual / Mensal / Semanal / Contínua / variantes (`Anual + revisões semestrais`).
3. (Se SIPOC) Verbo, Objeto, Finalidade, Inputs, Outputs, Owner — idêntico ao Bloco 3.

**Checkpoint** (heurísticas leves):
- [ ] Cada gerencial tem `frequencia` preenchida (regra GERENCIAL-SEM-FREQ)
- [ ] Cada gerencial tem `Freq:` na última linha do tooltip (regra GERENCIAL-TOOLTIP-FREQ)
- [ ] Demais checkpoints idênticos ao Bloco 3 (verbos, owners, IO-DUP)

**Saída**: BRIEFING completo até nível N1 + N2 (se `n2` em `artefatos_a_gerar`).

Se `n3` ou `n4-pdf` em `artefatos_a_gerar`, **continue** com a parte de mapa de interdependência:

### Bloco 4b · Mapa de interdependência (se aplicável)

**Perguntas**:

1. **Posição de cada processo no canvas** (left/top em %): use as colunas canônicas
   - Gerencial: `left: 8%`
   - Front-end: `left: 26%`
   - Núcleo (esquerda): `left: 44%`
   - Núcleo (direita): `left: 56%`
   - Back-end: `left: 74%`
   - Apoio: `top: 86-90%`, `left` distribuído entre 18% e 90%
2. **Relações** — para cada par de processos conectado:
   - `from`, `to`, `kind` (cliente / info / decisao), `label` (3-6 palavras), `forca` (se kind=cliente: strong/mid/soft)
3. **Fricções** — quais processos têm fricção operacional? (handoff falha, loop quebrado, dados fragmentados). Cada fricção marca `is_friction: true` + `text` descrevendo causa raiz.

**Checkpoint**:
- [ ] Toda relação tem `from` e `to` em `processos[]` (regra REL-ORFA)
- [ ] `kind=cliente` exige `forca` (regra FORCA-AUSENTE)
- [ ] Espinha dorsal de cliente existe (relações strong P1→P2→Pcore→Pback)
- [ ] Fricções ≤ 4 (regra FRICCAO-EXCESSO)
- [ ] Cada fricção tem `text` com causa raiz, não só sintoma (regra semântica FRICCAO-SEM-CAUSA)

---

## 6. Bloco 5 · Confirmação + critic

**Objetivo**: revisão final + invocação do `process-critic`.

**Passos**:

1. **Resumir o BRIEFING** ao usuário em 5-7 linhas:
   ```
   Você mapeou {N} processos ({G} gerenciais, {P} primários, {A} apoio).
   Variante: {A | B}.
   Artefatos a gerar: {n1, n2, n3, n4-pdf}.
   Highlights: {lista}. Blue accent: {processo}.
   Fricções: {N processos}.
   ```

2. **Pergunte**: "Algo que você quer ajustar antes da análise crítica final?"

3. **Rodar validador determinístico**:
   ```bash
   python3 scripts/check_briefing.py {path-do-briefing}.md --json
   ```
   Reporte ao usuário os bloqueadores e avisos (se houver).

4. **Invocar `process-critic`** (subagent):
   - Pass o caminho do BRIEFING
   - Critic devolve relatório markdown estruturado em Bloqueadores / Avisos / Sugestões / Veredicto

5. **Apresentar relatório** ao usuário e iniciar [Loop de iteração](#7-loop-de-iteração).

---

## 7. Loop de iteração

Política herdada de [`m7-analise-dados/agents/executive-communicator.md`](../../m7-analise-dados/agents/executive-communicator.md): **max 3 ciclos**.

```
Round N:
  1. process-critic devolve relatório
  2. Para cada bloqueador:
     - Apresente ao usuário via AskUserQuestion
     - Opções:
       a) "Corrigir: <sugestão do critic>"
       b) "Aceitar com rationale" → registra em validacao.bloqueadores_aceitos
       c) "Outro" → usuário fornece correção custom
     - Aplica correção no BRIEFING
  3. Para avisos: AskUserQuestion em batch ("Aplicar essas N sugestões?")
     - Default: aplicar tudo
     - Usuário pode des-selecionar individualmente
  4. Atualiza BRIEFING
  5. Re-roda check_briefing.py (deterministic) e process-critic (semantic)
  6. Se bloqueadores=0 → sai do loop
  7. Se bloqueadores > 0 e round < 3 → próximo round
  8. Se bloqueadores > 0 e round = 3 → escala
```

**Escalada (round 3+)**:
> "Após 3 rounds, persistem {N} bloqueadores não resolvidos. Opções:
> 1. Aplicar correções e rodar round 4 (não recomendado — sintoma de mapeamento estrutural raso)
> 2. Aceitar bloqueadores em `validacao.bloqueadores_aceitos` com rationale escrito
> 3. Pausar o mapeamento e reagendar entrevista com mais informação prévia"

---

## 8. Como aplicar correções

Quando o usuário aprova uma correção:

1. **Edita o BRIEFING.md** (Edit tool, no caminho do diretório de trabalho do usuário).
2. **Anota em `## Notas de iteração`** (markdown, no final do arquivo):
   ```markdown
   - {YYYY-MM-DD} — {regra} em {processo}: {antes} → {depois} ({motivo})
   ```
3. **Re-roda check_briefing.py** para confirmar que a correção não introduziu novos bloqueadores.

Quando o usuário **aceita um bloqueador** (decide seguir mesmo assim):

1. Adiciona em `validacao.bloqueadores_aceitos`:
   ```yaml
   bloqueadores_aceitos:
     - rule_id: "VERB-WEAK"
       where: "processos[15].sipoc.verbo (A3)"
       accepted_at: "2026-05-06"
       rationale: "Verbo 'Administrar' aceito porque A3 é por natureza administrativo. Alternativas (Construir/Operar) não são mais precisas para esse contexto específico."
   ```
2. Anota em `## Notas de iteração` que a exceção foi aceita.
3. **NÃO remove** o bloqueador da lista `validacao.bloqueadores` — fica como referência.

Auditável e justificável. Ninguém ignora silenciosamente uma regra.
