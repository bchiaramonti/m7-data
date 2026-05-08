---
name: drawing-bpmn-flowcharts
description: >-
  Constroi diagramas BPMN 2.0 a partir de JSON estruturado, descricao
  conversacional ou markdown narrativo. Gera arquivos .bpmn (XML portatil,
  abre em Camunda Modeler / bpmn.io / Bizagi) com auto-layout deterministico,
  validacao de legibilidade iterativa (sem sobreposicoes, sem cruzar nos,
  sem texto trincado) e cores do design system M7-2026 via extensoes bpmndi.
  Use when the user asks to generate, build, draw, model, or create a BPMN
  diagram, flowchart, or process flow; or when the user provides activities,
  lanes, or gateways and wants a .bpmn file.
user-invocable: true
---

# drawing-bpmn-flowcharts — Construtor de diagramas BPMN 2.0 com qualidade M7

> "BPMN bonito esconde mapeamento ruim — mas BPMN feio esconde valor que existe."

Skill que gera arquivos `.bpmn` (BPMN 2.0 XML padrao, portatil) com auto-layout deterministico, validacao iterativa de legibilidade, validacao de notacao embutida e cores do design system M7-2026 via extensoes `bpmndi:fillColor` / `bpmndi:strokeColor`.

## Filosofia

- **BPMN como saida portatil**: o `.bpmn` abre em Camunda Modeler, bpmn.io, Bizagi, Signavio. Sem dependencia de tool. **A skill gera apenas o `.bpmn` — nao gera HTML, PDF ou qualquer outro formato. A renderizacao downstream (ex: bpmn-js viewer embed em HTML) e responsabilidade do consumidor**.
- **Camunda como ambiente alvo**: a skill aplica extensoes `bioc:` (cores) e `zeebe:` (AI agents) — padrao do ecossistema Camunda 7+ / 8.8+. Outras ferramentas (Bizagi, Signavio) renderizam o BPMN core mas podem ignorar metadata de cor/agente.
- **Determinismo > LLM em geometria**: layout e validacao geometrica vao para scripts Python (stdlib). LLM raciocina sobre conteudo, nao sobre coordenadas.
- **Qualidade visual e gate, nao desejo**: validador iterativo nao deixa passar diagrama com sobreposicao, linha cruzando no, ou texto trincado.
- **M7 e identidade, nao decoracao**: cores aplicadas via extensoes `bioc:` para que o diagrama carregue a marca em qualquer ferramenta Camunda-compatible.
- **AI agents sao cidadaos de primeira classe**: a skill suporta o padrao Camunda 8.8+ via ad-hoc sub-process com tools — o jeito canonico de modelar comportamento nao-deterministico (LLM-driven) preservando auditabilidade do BPMN classico.

## Estrutura desta skill

```
drawing-bpmn-flowcharts/
├── SKILL.md                              # entrypoint (este arquivo)
├── references/
│   ├── bpmn-notation-essentials.md      # catalogo BPMN 2.0 + checklist de validacao
│   ├── auto-layout-algorithm.md         # algoritmo de layout deterministico
│   ├── readability-rules.md             # detectores geometricos + relayout
│   ├── m7-bpmn-styling.md               # tabela de cores M7 por elemento
│   └── ai-agents-bpmn.md                # ad-hoc sub-process + AI agents (Camunda 8.8+)
├── templates/
│   ├── bpmn-skeleton.tmpl.xml           # esqueleto XML com 5 namespaces
│   ├── input-schema.tmpl.json           # schema do JSON de input
│   └── descritivo.tmpl.md               # template do relatorio companion
├── scripts/
│   ├── compute_auto_layout.py           # calcula coords e waypoints
│   ├── validate_bpmn_readability.py     # valida geometria do .bpmn
│   └── requirements.txt                 # vazio (stdlib only)
└── examples/
    ├── exemplo-onboarding-input.json    # input de exemplo
    ├── exemplo-onboarding.bpmn          # output gerado
    └── exemplo-onboarding-descritivo.md # relatorio companion
```

## Quick start

Caminho mais curto, dado um JSON pronto seguindo o schema:

```bash
# 1. Calcular layout
python3 scripts/compute_auto_layout.py input.json > layout.json

# 2. Renderizar XML (preencher templates/bpmn-skeleton.tmpl.xml com layout.json)
#    Esta etapa e feita pela skill (LLM monta o XML lendo input + layout)

# 3. Validar legibilidade
python3 scripts/validate_bpmn_readability.py output.bpmn
# -> {"passed": true, "issues": []}
```

Inputs aceitos pela skill:
- **JSON estruturado** seguindo `templates/input-schema.tmpl.json`
- **Descricao conversacional** em portugues (skill faz parse semantico para JSON)
- **Markdown narrativo** com listas de atividades e gateways (skill extrai)

Em todos os casos, a skill converte para o JSON canonico antes de prosseguir.

### Suporte a AI Agents

Quando o processo envolve decisao nao-deterministica (LLM-driven), use:

- **`aiAgentTask`** para single-call (ex: classificar tom de email)
- **`adHocSubProcess`** com `aiAgent` para uso agentico (ex: agente decide quais tools chamar e em que ordem)

A skill aplica as extensoes Camunda (`zeebe:taskDefinition`, `zeebe:adHoc`) e renderiza o ad-hoc com fill lime sutil para diferenciar visualmente. Detalhes em [`references/ai-agents-bpmn.md`](references/ai-agents-bpmn.md), incluindo os 4 padroes canonicos (Human triggers AI / AI suggests + human decides / Multi-agent / Fallback).

## Workflow (7 fases)

### Fase 1 — Parse & Normalizacao do input

1. Detectar formato (JSON / conversacional / markdown)
2. Se JSON: validar contra `templates/input-schema.tmpl.json`
3. Se conversacional ou markdown: extrair entidades e gerar JSON canonico
   - Pools / lanes
   - Atividades (verbo + complemento)
   - Gateways (com pergunta + respostas nos flows)
   - Eventos de inicio/fim/intermediarios
   - Sequencias e mensagens
4. Salvar `<nome>-input.json` na pasta de trabalho

### Fase 2 — Validacao de notacao (pre-construcao)

Aplicar checklist de [`references/bpmn-notation-essentials.md`](references/bpmn-notation-essentials.md). Bloquear construcao se houver erros das categorias:

- **Estrutura**: exatamente 1 start, todo path termina em end, sem nodes soltos
- **Gateways**: divergencia → convergencia do mesmo tipo, XOR com default, labels presentes
- **Naming**: atividades com verbo+complemento, sem nomes genericos, gateway como pergunta
- **Pools/lanes**: sequence flow dentro de pool, message flow entre pools, atividade na lane do executor

Reportar ao usuario com sugestoes concretas. Nao prosseguir ate corrigir.

### Fase 3 — Auto-layout deterministico

```bash
python3 scripts/compute_auto_layout.py <nome>-input.json > <nome>-layout.json
```

O script implementa o algoritmo descrito em [`references/auto-layout-algorithm.md`](references/auto-layout-algorithm.md):
1. Topological sort (rank dos nodes a partir de start events)
2. Agrupar por lane × rank
3. Calcular alturas das lanes
4. Atribuir Y centrado na lane
5. Atribuir X baseado no rank
6. Gerar waypoints (exit-right, enter-left, intermediarios para cross-lane)

Output: `<nome>-layout.json` com bounds de cada shape e waypoints de cada edge.

### Fase 4 — Aplicar M7 styling (paleta v1.2)

Consultar tabela em [`references/m7-bpmn-styling.md`](references/m7-bpmn-styling.md). Para cada shape, aplicar `bioc:fill` e `bioc:stroke` (extensao Camunda) com **3 niveis hierarquicos** + acentos:

| Nivel | Elemento | bioc:fill | bioc:stroke |
|---|---|---|---|
| Pool/halo | Pool | `#fffdef` (warm off-white — aroma M7) | `#424135` |
| Raia | Lane | `#ffffff` (branco — excecao BPMN, contraste maximo) | `#424135` |
| Conteudo | Task / Subprocess | `#fdfbe5` (off-white esverdeado, destaca sobre lane branca) | `#424135` |
| Decisao | Gateway (XOR/AND/OR) | `#fef3a8` (amarelo palido — accent) | `#424135` |
| Foco | Start event (fluxo principal) | `#eef77c` (lime cheio) | `#424135` |
| Termino | End event (todos) | `#b8000f` (vermelho M7 WCAG-safe) | `#424135` |

Hierarquia visual: pool warm (halo M7) → lane branca (raia) → task esverdeada (destaque) → gateway amarelo (accent) → start lime → end vermelho.

### Fase 5 — Renderizacao do `.bpmn` + validacao iterativa

1. Montar `.bpmn` lendo `templates/bpmn-skeleton.tmpl.xml` e preenchendo com input + layout + styling
2. Salvar `<nome>.bpmn`
3. Rodar validador de legibilidade:
   ```bash
   python3 scripts/validate_bpmn_readability.py <nome>.bpmn
   ```
4. Se `passed: false`, aplicar estrategia de relayout conforme [`references/readability-rules.md`](references/readability-rules.md):
   - Cruzamento de linha sobre no → reordenar lanes (barycentric) ou desviar waypoint
   - Edges sobrepostos → adicionar waypoint intermediario
   - Label overflow → quebrar label em 2 linhas ou aumentar dimensao do node em 20%
   - Aspect-ratio guard → restaurar dimensao padrao
   - RTL flow > 30% → repensar ordem dos ranks
5. Re-rodar Fase 3 + 4 + 5 (max 3 iteracoes)
6. Se ainda falha apos 3 iteracoes: registrar issues residuais no descritivo com sugestao manual

### Fase 6 — Validacao final de notacao (pos-layout)

Re-checar com [`references/bpmn-notation-essentials.md`](references/bpmn-notation-essentials.md):

- Bidirectional refs corretas (incoming/outgoing match sourceRef/targetRef)
- Todo flow node em exatamente 1 `flowNodeRef` da sua lane
- Boundary events com `attachedToRef` valido (sem incoming)
- BPMNDiagram completo (todo elemento tem shape, todo edge tem waypoints)
- 5 namespaces declarados

### Fase 7 — Escrever artefatos

Gerar 2 arquivos na pasta de trabalho:

1. `<nome>.bpmn` — XML BPMN 2.0 portatil
2. `<nome>-descritivo.md` — preenchendo `templates/descritivo.tmpl.md` com:
   - Sumario do processo
   - Tabela de atividades por lane
   - Lista de gateways e pontos de decisao
   - **Checklist de notacao** (7 categorias com ✅/⚠/❌)
   - **Relatorio de legibilidade** (5 validadores)
   - **Aderencia ao M7-2026**
   - **Issues residuais** (se max iteracoes atingido)
   - Observacoes e sugestoes manuais

## Output

A skill gera **apenas** os arquivos abaixo. **Nao** gera HTML, PDF, ou qualquer outro formato — a renderizacao downstream (ex: bpmn-js viewer embed em HTML) e responsabilidade do consumidor do `.bpmn`.

| Arquivo | Conteudo |
|---|---|
| `<nome>.bpmn` | BPMN 2.0 XML completo (collaboration + processes + diagram com bounds e waypoints + `bioc:fill`/`bioc:stroke` nas shapes + extensoes `zeebe:` para AI agents quando aplicavel) |
| `<nome>-descritivo.md` | Narrativa + checklist de notacao + relatorio de legibilidade + aderencia M7 + issues residuais + (se houver AI agents) secao de governance |

## Quando NAO usar esta skill

- Usuario quer um diagrama em formato proprietario (Visio, Lucidchart) → outra skill
- Usuario quer um diagrama N1 de cadeia de valor → use `mapeamento-n1` deste mesmo plugin
- Usuario quer um diagrama de arquitetura tecnica (UML, C4, ER) → outra skill
- Usuario quer apenas analisar (nao construir) um BPMN existente → futura skill `reviewing-bpmn` ou agent ad-hoc

## Anti-patterns

- ❌ **Pular Fase 2** (validacao de notacao pre-construcao). Construir um diagrama incorreto e re-fazer e mais caro que validar antes.
- ❌ **Inventar atividades sem confirmar com o usuario**. Se o input e ambiguo, pergunte. Nao adivinhe.
- ❌ **Exceder 3 iteracoes de relayout**. Se nao convergiu em 3 ciclos, o problema e estrutural — escreva no descritivo e peca ajuda ao usuario.
- ❌ **Usar branco frio (`#ffffff`) em fills**. M7-2026 e off-white (`#fffdef`). Branco frio quebra a estetica.
- ❌ **Usar lime (`#eef77c`) em texto corrido ou em mais de 1-2 elementos**. Lime e accent — start event apenas. Mais que isso vira ruido visual.
- ❌ **Usar bold em labels de elementos BPMN**. M7-2026 usa peso 400 (regular). Bold quebra a hierarquia.
- ❌ **Assumir que toda ferramenta BPMN renderiza `bioc:fill`**. Bizagi pode ignorar. Documentar a limitacao no descritivo.
- ❌ **Modificar dimensoes padrao** (Event 36×36, Task 100×80, Gateway 50×50) sem motivo. Distorcao quebra a leitura.
- ❌ **Permitir flow direita→esquerda no fluxo principal**. Loop-back e a unica excecao. Caso contrario, reordenar.

## Lembretes

- **Salvar arquivos com nomes em kebab-case sem acentos** (compatibilidade cross-platform)
- **Usar IDs descritivos** no JSON: `n1`, `e1` para nodes/edges; `lane-comercial`, `pool-empresa` para containers
- **Sempre referenciar o design system canonico** em `m7-processos/skills/mapeamento-n1/references/design-system-m7.md` para tokens M7-2026 fora do escopo BPMN (tipografia, escalas)
- **Scripts sao stdlib only** (xml.etree.ElementTree, json, math). Nao importar numpy, lxml, etc.

## Recursos

- [bpmn-notation-essentials.md](references/bpmn-notation-essentials.md) — catalogo BPMN 2.0 + checklist de validacao (7 categorias)
- [auto-layout-algorithm.md](references/auto-layout-algorithm.md) — algoritmo deterministico (constantes, pseudocodigo, heuristicas)
- [readability-rules.md](references/readability-rules.md) — 5 detectores geometricos + estrategias de relayout
- [m7-bpmn-styling.md](references/m7-bpmn-styling.md) — tabela de cores M7 + sintaxe XML
- [ai-agents-bpmn.md](references/ai-agents-bpmn.md) — ad-hoc sub-process + AI agents (Camunda 8.8+) + 4 padroes canonicos
- [templates/bpmn-skeleton.tmpl.xml](templates/bpmn-skeleton.tmpl.xml) — esqueleto XML
- [templates/input-schema.tmpl.json](templates/input-schema.tmpl.json) — schema do JSON de input
- [templates/descritivo.tmpl.md](templates/descritivo.tmpl.md) — template do descritivo
- [scripts/compute_auto_layout.py](scripts/compute_auto_layout.py) — auto-layout
- [scripts/validate_bpmn_readability.py](scripts/validate_bpmn_readability.py) — validador geometrico
- [examples/](examples/) — exemplo end-to-end
- Design system canonico (M7-2026): `../mapeamento-n1/references/design-system-m7.md`
