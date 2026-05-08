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

M7-2026 e **editorial, nao corporativo**. Em BPMN isso significa:

- **Verde caqui (`#424135`) como ancora**: stroke de quase tudo, fundo de pool/lane labels
- **Off-white (`#fffdef`) como respiro**: fill de fluxo (tasks, gateways, lanes)
- **Lime (`#eef77c`) como acento pontual**: APENAS no start event do fluxo principal
- **Preto puro (`#000000`) e branco frio (`#ffffff`) sao proibidos**: quebram a estetica warm
- **Nenhum gradiente**: sombras sutis se necessarias, nada mais

A ideia e que mesmo um diagrama BPMN — naturalmente tecnico — carregue a marca M7 ao ser exibido via bpmn-js no documento oficial.

---

## 2. Tabela de cores por elemento BPMN

| Elemento | bioc:fill | bioc:stroke | Justificativa |
|---|---|---|---|
| **startEvent** (fluxo principal) | `#eef77c` | `#424135` | Lime accent unico, marca o inicio |
| **startEvent-message / startEvent-timer / startEvent-signal** | `#fffdef` | `#424135` | Inicios secundarios em off-white |
| **endEvent** (sucesso) | `#424135` | `#424135` | Verde caqui solido — fim feliz |
| **endEvent-error** | `#b8000f` | `#424135` | Status error WCAG (vermelho safe) |
| **endEvent-terminate** | `#28271f` | `#28271f` | Verde escuro 700 — encerramento total |
| **intermediateEvent** (qualquer) | `#fffdef` | `#424135` | Off-white com contorno verde |
| **task / userTask** | `#fffdef` | `#424135` | Card off-white, contorno fino |
| **serviceTask** | `#fffdef` | `#424135` | Mesmo card; o icone de engrenagem ja sinaliza tipo |
| **scriptTask** | `#fffdef` | `#424135` | Mesmo card; o icone de doc ja sinaliza |
| **sendTask / receiveTask** | `#fffdef` | `#424135` | Mesmo card; envelope ja sinaliza |
| **subProcess** (collapsed) | `#fffdef` | `#424135` (stroke 2px) | Borda mais grossa diferencia de task |
| **subProcess** (expanded) | `#fffdef` | `#424135` (stroke 2px) | Mesmo, mas com conteudo dentro |
| **adHocSubProcess** (AI agent) | `#eef77c` (subtle, 15% opacity bg) | `#424135` (stroke 2px) | Lime sutil sinaliza zona nao-deterministica |
| **exclusiveGateway** (XOR) | `#fffdef` | `#424135` | Diamante off-white com X visivel |
| **parallelGateway** (AND) | `#fffdef` | `#424135` | Diamante off-white com + visivel |
| **inclusiveGateway** (OR) | `#fffdef` | `#424135` | Diamante off-white com O visivel |
| **eventBasedGateway** | `#fffdef` | `#424135` | Diamante com pentagono |
| **Pool** | `#fffdef` (bg) | `#424135` | Container externo |
| **Lane** | `#fffdef` (bg) | `#424135` | Container interno; label `#fffdef` sobre fundo `#424135` |
| **dataObject / dataStore** | `#f6f6f5` | `#8a8981` | Cinza esverdeado sutil — artefato secundario |
| **textAnnotation** | (sem fill) | `#66655b` | Comentario discreto |

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

Heranca de `m7-processos/skills/mapeamento-n1/references/design-system-m7.md`:

- ❌ **Branco frio (`#ffffff`) em fills**: sempre `#fffdef` (off-white warm)
- ❌ **Lime em texto corrido ou em mais de 1 elemento**: lime e accent — start event apenas
- ❌ **Bold em labels**: peso 400 (regular) e assinatura M7
- ❌ **Gradientes em fills**: sombras sutis ok, gradiente nao
- ❌ **Multiplas cores acentuadas no mesmo diagrama**: 1 lime + 1 verde caqui + 1 vermelho de erro = teto. Mais que isso = ruido
- ❌ **Centralizar todos os labels**: lane labels uppercase ficam alinhados a esquerda
- ❌ **Adicionar sombras pesadas em shapes**: BPMN ja e tecnico, nao precisa de glamour visual
- ❌ **Adicionar logos / ornamentos no diagrama**: BPMN e funcional, nao decorativo

---

## 7. Referencia canonica

Para tokens M7-2026 fora do escopo BPMN (escala tipografica completa, paleta de status, escala verde-caqui de 10 tons, raios de borda, sombras), consultar:

- `../mapeamento-n1/references/design-system-m7.md` (mesmo plugin, runtime)

Esta reference (`m7-bpmn-styling.md`) cobre apenas o subset aplicavel a BPMN. Mudancas no design system canonico devem ser propagadas aqui em uma versao futura.

---

## Checklist de aplicacao M7 no `.bpmn` gerado

A skill verifica automaticamente em **Fase 4** e reporta no `-descritivo.md`:

- [ ] Namespace `bioc:` declarado em `<bpmn:definitions>`
- [ ] Todo `<bpmndi:BPMNShape>` tem atributos `bioc:fill` e `bioc:stroke`
- [ ] Cores aplicadas batem com a tabela acima por tipo de elemento
- [ ] Apenas 1 startEvent com lime fill (`#eef77c`)
- [ ] Nenhum element com `#ffffff` ou `#000000` (proibidos)
- [ ] Edges tem `bioc:stroke="#424135"` (padrao M7)

Se algum item falha, registrar warning no descritivo (nao bloqueia construcao).
