# {{TITLE}} — Diagrama BPMN

> Gerado em {{DATE}} pela skill `drawing-bpmn-flowcharts` (v{{SKILL_VERSION}})
> Arquivo BPMN: [{{NAME}}.bpmn]({{NAME}}.bpmn)
> Nivel BPM CBOK: **{{LEVEL}}** · Versao: {{VERSION}} · Autor: {{AUTHOR}}

---

## 1. Sumario do processo

{{SUMMARY}}

---

## 2. Atividades por lane

| Lane | Atividades | Tipo |
|---|---|---|
{{LANE_TABLE_ROWS}}

---

## 3. Pontos de decisao (gateways)

{{GATEWAY_LIST}}

<!-- Formato esperado:
### {{gateway.label}}
- **Tipo**: {{XOR | AND | OR | Event-based}}
- **Lane**: {{lane.name}}
- **Caminhos**:
  - "Sim" → {{target1.label}}
  - "Nao" → {{target2.label}} (default)
- **Regra de negocio**: {{rule_or_question}}
-->

---

## 4. Validacao de notacao BPMN 2.0

Status por categoria (✅ pass · ⚠ warning · ❌ fail). Detalhes em `references/bpmn-notation-essentials.md`.

### Categoria 4.1 — Eventos
{{NOTATION_EVENTS}}

### Categoria 4.2 — Gateways
{{NOTATION_GATEWAYS}}

### Categoria 4.3 — Naming
{{NOTATION_NAMING}}

### Categoria 4.4 — Flow Direction
{{NOTATION_FLOW}}

### Categoria 4.5 — Pools & Lanes
{{NOTATION_POOLS}}

### Categoria 4.6 — Subprocesses
{{NOTATION_SUBPROCESSES}}

### Categoria 4.7 — Completude / XML Estrutural
{{NOTATION_COMPLETENESS}}

**Resumo**: ✅ {{NOTATION_PASS_COUNT}} pass · ⚠ {{NOTATION_WARNING_COUNT}} warnings · ❌ {{NOTATION_FAIL_COUNT}} fails

---

## 5. Validacao de legibilidade

Resultado dos 5 detectores geometricos (de `references/readability-rules.md`):

| Detector | Status | Observacao |
|---|---|---|
| Edge crosses node | {{STATUS_EDGE_CROSSES_NODE}} | {{NOTE_EDGE_CROSSES_NODE}} |
| Edge overlap | {{STATUS_EDGE_OVERLAP}} | {{NOTE_EDGE_OVERLAP}} |
| Label overflow | {{STATUS_LABEL_OVERFLOW}} | {{NOTE_LABEL_OVERFLOW}} |
| Aspect-ratio violation | {{STATUS_ASPECT_RATIO}} | {{NOTE_ASPECT_RATIO}} |
| RTL flow | {{STATUS_RTL_FLOW}} | {{NOTE_RTL_FLOW}} |

**Iteracoes de relayout aplicadas**: {{LAYOUT_ITERATIONS}} (max 3)

---

## 6. Aderencia ao Design System M7-2026

| Item | Status | Detalhe |
|---|---|---|
| Namespace `bioc:` declarado | {{STATUS_BIOC_NS}} | {{NOTE_BIOC_NS}} |
| Cores aplicadas conforme tabela | {{STATUS_COLORS}} | {{NOTE_COLORS}} |
| Apenas 1 startEvent com lime | {{STATUS_LIME_USE}} | {{NOTE_LIME_USE}} |
| Sem branco frio (`#ffffff`) | {{STATUS_NO_COLD_WHITE}} | {{NOTE_NO_COLD_WHITE}} |
| Edges com stroke `#424135` | {{STATUS_EDGE_STROKE}} | {{NOTE_EDGE_STROKE}} |

> Nota: `bioc:` e suportado por Camunda Modeler 7+, Camunda 8 e bpmn-js. Bizagi e Signavio ignoram silenciosamente.

---

## 7. Agentes de IA no diagrama

{{AI_AGENTS_SECTION}}

<!-- Esta secao so aparece se ha nodes do tipo aiAgentTask ou adHocSubProcess com aiAgent. Formato:

### {{aiAgent.label}}
- **Padrao**: Human triggers AI / AI suggests + human decides / Multi-agent collaboration / Fallback escalation
- **Tipo**: aiAgentTask (single-call) / adHocSubProcess (agentic) / orchestrator
- **Modelo**: claude-3-5-sonnet
- **Tools** (se ad-hoc): ["consulta_gold_layer", "enrich_crm", "gerar_html", "validar_regras"]
- **Exit condition**: agent.confidence > 0.85 OR iteration > 5
- **Governance**:
  - Quem aprova: {{role}}
  - Quem audita: {{role}}
  - Como recuperar: {{rollback strategy}}
- **Risco residual**: {{ex: hallucination em campos numericos — mitigado por validacao posterior}}

-->

---

## 8. Issues residuais e sugestoes manuais

{{RESIDUAL_ISSUES}}

<!-- Esta secao so aparece se max iteracoes de relayout foi atingida sem convergencia. Formato:

> Apos 3 iteracoes de relayout, persistem os seguintes issues. Recomendado ajuste manual no Camunda Modeler:

- **edge-crosses-node** em e7 cruza n4: reordenar lanes manualmente OU dividir em subprocess
- **label-overflow** em n12 ("Validar conformidade regulatoria com area de auditoria interna"): nome muito longo, sugerir abreviacao ou virar subprocess

-->

---

## 9. Observacoes do mapeamento

{{OBSERVATIONS}}

<!-- Espaco para o usuario adicionar contexto, decisoes tomadas, premissas, gaps identificados. Pode incluir:
- Atores secundarios nao representados (justificativa)
- Excecoes nao mapeadas (lista para iteracao futura)
- Indicadores de monitoramento sugeridos
- Regras de negocio referenciadas (links para POPs)
-->

---

## 10. Como visualizar

O arquivo `.bpmn` gerado abre em:

- **Camunda Modeler 7+ / 8**: download + double-click. Renderiza com cores M7-2026.
- **bpmn.io demo**: https://demo.bpmn.io/ — drag-and-drop do arquivo
- **bpmn-js viewer (HTML embed)**: integrar via npm `bpmn-js` em pagina HTML — Camunda 8 SaaS faz isso automaticamente
- **Bizagi / Signavio**: renderiza o BPMN core, mas ignora `bioc:` (cores) e `zeebe:` (AI agents)

Para fidelidade total ao M7-2026 (TWK Everett, gestos visuais), use bpmn-js com CSS custom (fora do escopo desta skill).
