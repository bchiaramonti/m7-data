# Onboarding de Lead M7 — Diagrama BPMN

> Gerado em 2026-05-08 pela skill `drawing-bpmn-flowcharts` (v1.1.0)
> Arquivo BPMN: [exemplo-onboarding.bpmn](exemplo-onboarding.bpmn)
> Nivel BPM CBOK: **N3** · Versao: 1.0 · Autor: Bruno Chiaramonti

---

## 1. Sumario do processo

Processo de captacao e ativacao de novos clientes M7 a partir de um lead recebido. Tres areas envolvidas: Comercial (qualificacao inicial), Compliance (validacao KYC), Operacoes (abertura efetiva de conta). Caminhos terminais: cliente ativo, lead descartado, ou bloqueio por compliance.

---

## 2. Atividades por lane

| Lane | Atividades | Tipo |
|---|---|---|
| Comercial | Qualificar lead | userTask |
| Compliance | Validar KYC | userTask |
| Operacoes | Abrir conta | serviceTask |

Eventos terminais distribuidos por lane:
- Comercial: "Lead descartado" (descarte na qualificacao)
- Compliance: "Bloqueado por compliance" (KYC negado)
- Operacoes: "Cliente ativo" (sucesso)

---

## 3. Pontos de decisao (gateways)

### "Aprovado?" (n3)
- **Tipo**: exclusiveGateway (XOR)
- **Lane**: Comercial
- **Caminhos**:
  - "Sim" → Validar KYC (n4)
  - "Nao" → Lead descartado (n8) — **default**
- **Regra de negocio**: lead atende criterios M7 (perfil, ticket, segmento)?

### "KYC ok?" (n5)
- **Tipo**: exclusiveGateway (XOR)
- **Lane**: Compliance
- **Caminhos**:
  - "Sim" → Abrir conta (n6)
  - "Nao" → Bloqueado por compliance (n9) — **default**
- **Regra de negocio**: documentos validos + checks regulatorios sem alerta?

---

## 4. Validacao de notacao BPMN 2.0

Status por categoria (✅ pass · ⚠ warning · ❌ fail).

### Categoria 4.1 — Eventos
- ✅ Exatamente 1 start event (n1: "Lead recebido")
- ✅ 3 end events (n7, n8, n9) cobrindo todos os caminhos
- ✅ Todos os paths terminam em end event
- ✅ Start event na lane do iniciador (Comercial)

### Categoria 4.2 — Gateways
- ✅ XOR "Aprovado?" tem caminho default (e4)
- ✅ XOR "KYC ok?" tem caminho default (e7)
- ✅ Labels presentes em todos os fluxos de saida ("Sim"/"Nao")
- ⚠ Gateways nao tem convergencia explicita — caminhos terminam em end events distintos. OK para este modelo (cada path tem destino terminal proprio)

### Categoria 4.3 — Naming
- ✅ Todas atividades com verbo + complemento ("Qualificar lead", "Validar KYC", "Abrir conta")
- ✅ Gateways como pergunta ("Aprovado?", "KYC ok?")
- ✅ Edges como resposta ("Sim", "Nao")

### Categoria 4.4 — Flow Direction
- ✅ Fluxo predominante esquerda → direita
- ✅ Sem cruzamentos sobre nodes
- ✅ Atividades alinhadas em suas lanes

### Categoria 4.5 — Pools & Lanes
- ✅ 1 pool ("M7 Investimentos") com 3 lanes
- ✅ Atividades na lane do executor
- ✅ Sem message flows (processo intra-organizacional)

### Categoria 4.6 — Subprocesses
- ✅ Sem subprocesses neste exemplo (3 atividades nao justificam agrupamento)

### Categoria 4.7 — Completude / XML Estrutural
- ✅ 5 namespaces declarados (bpmn, bpmndi, dc, di, xsi)
- ✅ Bidirectional refs corretas
- ✅ Todo node em exatamente 1 flowNodeRef
- ✅ Todo elemento tem BPMNShape; todo edge tem BPMNEdge
- ✅ IDs unicos no documento

**Resumo**: ✅ 23 pass · ⚠ 1 warning · ❌ 0 fails

---

## 5. Validacao de legibilidade

Resultado dos 5 detectores geometricos:

| Detector | Status | Observacao |
|---|---|---|
| Edge crosses node | ✅ pass | Nenhum edge cruza node nao-extremo |
| Edge overlap | ✅ pass | Sem segmentos colineares > 20px (excluindo origem comum de gateways) |
| Label overflow | ⚠ warning | "Qualificar lead" sugere split em 2 linhas (caberia em 1, mas leitura melhora) |
| Aspect-ratio violation | ✅ pass | Todas as dimensoes seguem padrao BPMN |
| RTL flow | ✅ pass | 0 flows direita → esquerda (fluxo 100% LTR) |

**Iteracoes de relayout aplicadas**: 1 de 3 (passou na primeira iteracao)

---

## 6. Aderencia ao Design System M7-2026 (paleta v1.2)

| Item | Status | Detalhe |
|---|---|---|
| Namespace `bioc:` declarado | ✅ | http://bpmn.io/schema/bpmn/biocolor/1.0 |
| Cores aplicadas conforme tabela v1.2 | ✅ | Lane warm `#fffdef` · Task off-white esverdeado `#fdfbe5` · Gateway amarelo palido `#fef3a8` · End vermelho `#b8000f` |
| Apenas 1 startEvent com lime | ✅ | n1 ("Lead recebido") com `bioc:fill="#eef77c"` |
| Tasks contrastam com lanes | ✅ | Tasks `#fdfbe5` sobre lanes `#fffdef` (contraste sutil mas visivel) |
| Gateways tem realce | ✅ | n3 ("Aprovado?") e n5 ("KYC ok?") com `bioc:fill="#fef3a8"` |
| End events sao todos vermelhos | ✅ | n7 (sucesso), n8 (descarte), n9 (bloqueio) — todos `bioc:fill="#b8000f"` |
| Sem branco frio (`#ffffff`) | ✅ | Todos os fills usam `#fffdef`, `#fdfbe5`, `#fef3a8`, `#eef77c`, ou `#b8000f` |
| Edges com stroke `#424135` | ✅ | 8/8 edges com stroke verde caqui |

> Nota: `bioc:` e suportado por Camunda Modeler 7+, Camunda 8 e bpmn-js. Bizagi e Signavio ignoram silenciosamente.

---

## 7. Agentes de IA no diagrama

Este exemplo nao contem agentes de IA. Para um exemplo com `aiAgentTask` ou `adHocSubProcess` agentic, consultar [`references/ai-agents-bpmn.md`](../references/ai-agents-bpmn.md).

---

## 8. Issues residuais e sugestoes manuais

Sem issues residuais. O diagrama passou em todas as validacoes na primeira iteracao de layout.

Sugestao opcional (warning): aplicar quebra de linha no label "Qualificar lead" para n2 (renderiza melhor em ferramentas com fonte ligeiramente diferente).

---

## 9. Observacoes do mapeamento

- **Tres caminhos terminais** sao intencionais: o processo modela 3 desfechos distintos com SLAs proprios. Em uma evolucao futura, considerar:
  - Adicionar timer events para SLA de qualificacao (ex: 2 dias uteis)
  - Boundary error event em "Validar KYC" para tratar falhas tecnicas (sistema de KYC indisponivel)
- **Sem subprocess para "Validar KYC"**: na realidade, KYC envolve 4-5 sub-tarefas (consulta receita, OFAC, COAF, etc.). Para um modelo N4-N5, virar `subProcess` expandido. Para este nivel N3 (visao funcional), manter como atividade unica
- **Indicadores de monitoramento sugeridos**:
  - Tempo medio de qualificacao (lead → decisao "Aprovado?")
  - Taxa de aprovacao em qualificacao
  - Tempo medio de KYC
  - Taxa de bloqueio por compliance (% de leads aprovados que sao bloqueados em KYC)
  - Lead time end-to-end (lead recebido → cliente ativo)

---

## 10. Como visualizar

O arquivo `.bpmn` gerado abre em:

- **Camunda Modeler 7+ / 8**: download + double-click. Renderiza com cores M7-2026.
- **bpmn.io demo**: https://demo.bpmn.io/ — drag-and-drop do arquivo
- **bpmn-js viewer (HTML embed)**: integrar via npm `bpmn-js` em pagina HTML — Camunda 8 SaaS faz isso automaticamente
- **Bizagi / Signavio**: renderiza o BPMN core, mas ignora `bioc:` (cores) e `zeebe:` (AI agents)

Para fidelidade total ao M7-2026 (TWK Everett, gestos visuais), use bpmn-js com CSS custom (fora do escopo desta skill).
