# M7 Design System aplicado a BPMN

Tabela de cores M7-2026 por tipo de elemento BPMN, sintaxe XML para aplicar via extensoes Camunda (`bioc:`), e regras de tipografia. Foco no fluxo Camunda: o `.bpmn` final e exibido via bpmn-js viewer (HTML embed) ou no Camunda Modeler.

## Sumario

1. [Filosofia](#1-filosofia)
2. [Tabela de cores por elemento BPMN](#2-tabela-de-cores-por-elemento-bpmn)
3. [Sintaxe XML (extensoes bioc: da Camunda)](#3-sintaxe-xml-extensoes-bioc-da-camunda)
4. [Tipografia](#4-tipografia)
5. [Compatibilidade entre ferramentas](#5-compatibilidade-entre-ferramentas)
6. [Anti-padroes M7-2026 herdados](#6-anti-padroes-m7-2026-herdados)
7. [Referencia canonica](#7-referencia-canonica)

---

## 1. Filosofia

M7-2026 e **editorial, nao corporativo**. Em BPMN isso significa **3 niveis hierarquicos** de fundo + acentos pontuais:

```
Nivel 1 (pool/halo)  Pool             #fffdef  warm off-white (aroma M7)
Nivel 2 (raia)       Lane             #ffffff  branco (contraste maximo p/ tasks)
Nivel 3 (conteudo)   Task / Subproc   #fdfbe5  off-white esverdeado (destaca sobre lane branca)
Nivel 4 (decisao)    Gateway          #fef3a8  amarelo palido (accent de decisao)
Acento foco          Start            #eef77c  lime cheio
Acento termino       End (todos)      #b8000f  vermelho M7 WCAG-safe
```

Principios que se aplicam:

- **Verde caqui (`#424135`) como ancora**: stroke de quase tudo (incluindo edges)
- **Hierarquia por contraste forte**: pool warm → lane branca (raia "vazia") → conteudo levemente esverdeado (destaca sobre branco) → accent amarelo no ponto de decisao. Leitor identifica papeis sem precisar ler labels
- **Acentos so onde precisa**: lime (start) e vermelho (end) marcam ponta a ponta. Amarelo palido (gateway) chama atencao SEM gritar
- **Preto puro (`#000000`) e proibido**; branco puro (`#ffffff`) **e permitido apenas em raias BPMN** — excecao do contexto BPMN (justificada abaixo). Em qualquer outra parte do diagrama (pool, tasks, eventos), branco frio continua proibido
- **Nenhum gradiente**: sombras sutis se necessarias, nada mais

> **Nota sobre `#ffffff` em lanes (excecao BPMN):** o anti-pattern M7-2026 canonico proibe branco frio em backgrounds. **Em BPMN, lanes brancas sao excecao justificada** porque (a) BPMN e artefato tecnico onde contraste maximo entre raia e tarefas e necessario para leitura rapida, e (b) o pool externo (`#fffdef`) ja garante o aroma warm da marca. Nao propagar essa excecao para outros artefatos M7 (Cadeia de Valor, SIPOC, Documento Oficial — todos seguem o anti-pattern original sem branco frio).
>
> **Nota sobre `#fef3a8`:** este amarelo palido nao existe no design system M7-2026 canonico (`mapeamento-n1/references/design-system-m7.md`). E uma cor exclusiva do contexto BPMN, justificada porque BPMN tem mais primitivos visuais (4 categorias: container, conteudo, decisao, terminal) do que outros artefatos M7 (que se contentam com 3 cores). **Nao propagar para outros artefatos M7.**

A ideia e que mesmo um diagrama BPMN — naturalmente tecnico — carregue a marca M7 ao ser exibido via bpmn-js no documento oficial.

---

## 2. Tabela de cores por elemento BPMN

> Atualizada em v1.2.0 (2026-05-08) para diferenciar visualmente container (lane) de conteudo (task) e introduzir accent de decisao no gateway.

| Elemento | bioc:fill | bioc:stroke | Justificativa |
|---|---|---|---|
| **startEvent** (fluxo principal) | `#eef77c` | `#424135` | Lime accent unico, marca o inicio |
| **startEvent-message / startEvent-timer / startEvent-signal** | `#fdfbe5` | `#424135` | Inicios secundarios em off-white esverdeado (igual task) |
| **endEvent** (sucesso) | `#b8000f` | `#424135` | Vermelho M7 WCAG-safe — termino do processo |
| **endEvent-error** | `#b8000f` | `#424135` | Mesmo vermelho — error termina processo |
| **endEvent-terminate** | `#600000` | `#424135` | Vermelho escuro — encerramento total |
| **intermediateEvent** (qualquer) | `#fdfbe5` | `#424135` | Off-white esverdeado, mesmo nivel hierarquico de task |
| **task / userTask** | `#fdfbe5` | `#424135` | Card off-white esverdeado — contraste sobre lane |
| **serviceTask** | `#fdfbe5` | `#424135` | Mesmo card; o icone de engrenagem ja sinaliza tipo |
| **scriptTask** | `#fdfbe5` | `#424135` | Mesmo card; o icone de doc ja sinaliza |
| **sendTask / receiveTask** | `#fdfbe5` | `#424135` | Mesmo card; envelope ja sinaliza |
| **subProcess** (collapsed) | `#fdfbe5` | `#424135` (stroke 2px) | Borda mais grossa diferencia de task |
| **subProcess** (expanded) | `#fdfbe5` | `#424135` (stroke 2px) | Mesmo, mas com conteudo dentro |
| **adHocSubProcess** (AI agent) | `#eef77c` (subtle, 15% opacity bg) | `#424135` (stroke 2px) | Lime sutil sinaliza zona nao-deterministica |
| **exclusiveGateway** (XOR) | `#fef3a8` | `#424135` | Amarelo palido — accent de decisao |
| **parallelGateway** (AND) | `#fef3a8` | `#424135` | Mesmo amarelo, simbolo + diferencia |
| **inclusiveGateway** (OR) | `#fef3a8` | `#424135` | Mesmo amarelo, simbolo O diferencia |
| **eventBasedGateway** | `#fef3a8` | `#424135` | Mesmo amarelo, pentagono diferencia |
| **Pool** | `#fffdef` (bg) | `#424135` | Container externo — warm off-white (aroma M7) |
| **Lane** | `#ffffff` (bg) | `#424135` | Raia interna — branca (excecao BPMN; contraste maximo para tasks). Label segue cor padrao do bpmn-js (preto sobre branco). Para customizar cor da label: CSS no consumer (HTML embed). |
| **dataObject / dataStore** | `#f6f6f5` | `#8a8981` | Cinza esverdeado sutil — artefato secundario |
| **textAnnotation** | (sem fill) | `#66655b` | Comentario discreto |

### Mudancas v1.1 → v1.2

| Elemento | v1.1 (uniforme) | v1.2 (diferenciado) |
|---|---|---|
| Task / Subprocess | `#fffdef` (igual lane) | `#fdfbe5` (off-white esverdeado) |
| Gateway | `#fffdef` (igual task) | `#fef3a8` (amarelo palido) |
| End (sucesso) | `#424135` (verde caqui) | `#b8000f` (vermelho) |
| End (terminate) | `#28271f` (verde escuro) | `#600000` (vermelho escuro) |

### Mudanca v1.2.0 → v1.2.1

| Elemento | v1.2.0 | v1.2.1 |
|---|---|---|
| Lane | `#fffdef` (warm off-white, contraste fraco com task) | `#ffffff` (branco — contraste maximo para tasks) |

Pool mantem `#fffdef` (aroma M7); lanes brancas funcionam como "raias vazias" classicas de BPMN, com tasks `#fdfbe5` se destacando claramente.

### Cores nao usadas (intencional)

- `#000000` (preto puro) — substituido por `#424135` (verde caqui)
- `#ffffff` (branco frio) — substituido por `#fffdef` (off-white)
- `#0000ff`, `#00ff00`, `#ff0000` (cores primarias saturadas) — exceto `#b8000f` para erro WCAG-safe

---

## 3. Sintaxe XML (extensoes bioc: da Camunda)

A extensao `bioc:` (BPMN.io Color) e suportada nativamente por Camunda Modeler 7+, Camunda 8 e bpmn-js. E o padrao de fato no ecossistema Camunda.

### Namespace declaration

Adicionar ao `<bpmn:definitions>`:

```xml
<bpmn:definitions
  xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:bioc="http://bpmn.io/schema/bpmn/biocolor/1.0"
  xmlns:color="http://www.omg.org/spec/BPMN/non-normative/color/1.0"
  ...>
```

> **Nota:** alguns rendering libs aceitam tanto `bioc:` quanto `color:`. Por seguranca, declarar ambos namespaces e aplicar via `bioc:` (mais comum).

### Aplicar em BPMNShape

```xml
<bpmndi:BPMNShape id="n1_di"
                  bpmnElement="n1"
                  bioc:stroke="#424135"
                  bioc:fill="#eef77c">
  <dc:Bounds x="252" y="122" width="36" height="36" />
</bpmndi:BPMNShape>
```

### Aplicar em BPMNEdge

Edges normalmente nao precisam de fill, apenas stroke:

```xml
<bpmndi:BPMNEdge id="e1_di"
                 bpmnElement="e1"
                 bioc:stroke="#424135">
  <di:waypoint x="288" y="140" />
  <di:waypoint x="370" y="140" />
</bpmndi:BPMNEdge>
```

### Pool e Lane (labels com fundo invertido)

Pool e Lane recebem o stroke padrao, mas o **label** da lane vai sobre fundo `#424135`. Isso nao se aplica via `bioc:` — depende do CSS do bpmn-js viewer (ver `templates/embed.tmpl.html`).

---

## 4. Tipografia

BPMN nao tem suporte nativo para `font-family` via Diagram Interchange. A solucao e:

1. **No `.bpmn`**: nao especificar fonte — fica padrao da ferramenta
2. **No HTML embed (bpmn-js)**: aplicar `font-family: 'TWK Everett', Arial, sans-serif` via CSS:

```css
.djs-element .djs-label,
.djs-element text {
  font-family: 'TWK Everett', Arial, sans-serif !important;
  font-weight: 400 !important;  /* M7-2026: nunca bold */
  font-size: 11px;
}
```

3. **Documentar** no `-descritivo.md` que para fidelidade total ao M7-2026 (TWK Everett), usar o HTML embed; ferramentas BPMN externas usarao a fonte padrao.

### Anti-pattern de tipografia M7

- ❌ **Bold (700) em labels** — quebra a estetica M7-2026
- ❌ **Italic em labels normais** — usar apenas em annotations (texto auxiliar)
- ❌ **Font sans-serif moderna** (Inter, Helvetica) — usar TWK Everett ou Arial fallback

---

## 5. Compatibilidade entre ferramentas

| Ferramenta | bioc:fill / bioc:stroke | Notas |
|---|---|---|
| **Camunda Modeler 7+** | ✅ Suporte nativo | Usado para edicao no fluxo M7 |
| **Camunda 8 / SaaS** | ✅ Suporte nativo | Usado para execucao |
| **bpmn-js (viewer)** | ✅ Suporte nativo | Usado no HTML embed |
| **bpmn-js (modeler)** | ✅ Editor visual de cores | Permite ajuste manual posterior |
| **Bizagi Modeler** | ⚠ Ignora silenciosamente | Renderiza com cores padrao |
| **Signavio** | ⚠ Ignora silenciosamente | Renderiza com cores padrao |
| **Visio (BPMN stencil)** | ❌ Nao suporta | Nao recomendado |

A skill **assume Camunda + bpmn-js** como ambiente alvo (o que e usado pela M7).

---

## 6. Anti-padroes M7-2026 herdados

Heranca de `m7-processos/skills/mapeamento-n1/references/design-system-m7.md` + especificos do contexto BPMN:

- ❌ **Tasks com mesma cor da lane**: invisibilidade visual. Task `#fdfbe5` deve contrastar com lane `#ffffff` (regra v1.2.1)
- ❌ **Gateway com mesma cor de task**: ponto de decisao precisa chamar atencao. Gateway `#fef3a8` (amarelo palido) e o accent (regra v1.2)
- ❌ **End event verde caqui (`#424135`)**: confunde com stroke. End sempre vermelho `#b8000f` (regra v1.2)
- ❌ **Branco frio (`#ffffff`) em fills de pool/task/event/gateway**: apenas em lanes (excecao BPMN). Pool e `#fffdef`; tasks/eventos/gateways seguem suas cores especificas
- ❌ **Lane warm (`#fffdef`) em vez de branca**: regra v1.2.1 mudou para `#ffffff` para contraste maximo com tasks `#fdfbe5`. Lane warm reduz drasticamente a leitura visual
- ❌ **Lime em texto corrido ou em mais de 1 elemento**: lime e accent — start event apenas
- ❌ **Bold em labels**: peso 400 (regular) e assinatura M7
- ❌ **Gradientes em fills**: sombras sutis ok, gradiente nao
- ❌ **Mais de 1 amarelo no diagrama**: amarelo palido (`#fef3a8`) e exclusivo de gateway. Outras tonalidades amarelo = ruido
- ❌ **Centralizar todos os labels**: lane labels uppercase ficam alinhados a esquerda
- ❌ **Adicionar sombras pesadas em shapes**: BPMN ja e tecnico, nao precisa de glamour visual
- ❌ **Adicionar logos / ornamentos no diagrama**: BPMN e funcional, nao decorativo

---

## 7. Referencia canonica

Para tokens M7-2026 fora do escopo BPMN (escala tipografica completa, paleta de status, escala verde-caqui de 10 tons, raios de borda, sombras), consultar:

- `../mapeamento-n1/references/design-system-m7.md` (mesmo plugin, runtime)

Esta reference (`m7-bpmn-styling.md`) cobre apenas o subset aplicavel a BPMN. Mudancas no design system canonico devem ser propagadas aqui em uma versao futura.

---

## Checklist de aplicacao M7 no `.bpmn` gerado (v1.2)

A skill verifica automaticamente em **Fase 4** e reporta no `-descritivo.md`:

- [ ] Namespace `bioc:` declarado em `<bpmn:definitions>`
- [ ] Todo `<bpmndi:BPMNShape>` tem atributos `bioc:fill` e `bioc:stroke`
- [ ] Cores aplicadas batem com a tabela v1.2.1 por tipo de elemento
- [ ] Apenas 1 startEvent com lime fill (`#eef77c`); demais starts com `#fdfbe5`
- [ ] Tasks/Subprocessos com fill `#fdfbe5` (off-white esverdeado, destaca sobre lane branca)
- [ ] Gateways com fill `#fef3a8` (amarelo palido — accent de decisao)
- [ ] End events com fill `#b8000f` (vermelho M7)
- [ ] Pool com fill `#fffdef` (warm off-white — aroma M7)
- [ ] Lane com fill `#ffffff` (branco — excecao BPMN, contraste maximo para tasks)
- [ ] Nenhum task/event/gateway com `#ffffff` (proibido fora de lanes)
- [ ] Nenhum element com `#000000` (sempre `#424135`)
- [ ] Edges tem `bioc:stroke="#424135"` (padrao M7)

Se algum item falha, registrar warning no descritivo (nao bloqueia construcao).
