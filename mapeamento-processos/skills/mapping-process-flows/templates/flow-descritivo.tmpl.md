# {{titulo_processo}} — Descritivo do Fluxo

> **Substituicoes**: Todos os campos `{{campo}}` devem ser preenchidos com os dados coletados na entrevista.
> Este arquivo e gerado pela skill `mapping-process-flows`. Remova esta instrucao apos preenchimento.

---

## 1. Identificacao

| Campo | Valor |
|-------|-------|
| **Processo** | {{titulo_processo}} |
| **Codigo** | {{codigo_processo}} |
| **Nivel BPM** | {{nivel}} |
| **Responsavel** | {{responsavel}} |
| **Versao** | {{versao}} |
| **Data** | {{data}} |
| **Arquivo BPMN** | `{{nome_arquivo}}.bpmn` |

---

## 2. Objetivo

{{objetivo_processo}}

---

## 3. Participantes

{{#if_pools_multiplos}}
### Pools

| Pool | Descricao |
|------|-----------|
{{#cada_pool}}
| **{{pool.nome}}** | {{pool.descricao}} |
{{/cada_pool}}
{{/if_pools_multiplos}}

{{#if_lanes}}
### Lanes — {{pool_principal.nome}}

| Lane | Ator / Responsavel |
|------|-------------------|
{{#cada_lane}}
| {{lane.id}} | {{lane.nome}} |
{{/cada_lane}}
{{/if_lanes}}

{{#if_nivel_n1_n2}}
*Processo de nivel logico ({{nivel}}). Sem divisao por atores.*
{{/if_nivel_n1_n2}}

---

## 4. Evento de Inicio

| Campo | Valor |
|-------|-------|
| **Trigger** | {{trigger_descricao}} |
| **Tipo** | {{trigger_tipo}} |
| **Iniciado por** | {{trigger_ator}} |

---

## 5. Narrativa do Fluxo — Caminho Feliz

{{descricao_caminho_feliz_introducao}}

{{#cada_passo_caminho_feliz}}
**{{passo.numero}}.** {{passo.descricao}}
- *Executor*: {{passo.lane}}
- *Tipo de atividade*: {{passo.tipo}}
{{#se_passo_tem_nota}}
- *Nota*: {{passo.nota}}
{{/se_passo_tem_nota}}

{{/cada_passo_caminho_feliz}}

---

## 6. Pontos de Decisao

{{#se_sem_gateways}}
*Sem pontos de decisao identificados — processo de fluxo linear.*
{{/se_sem_gateways}}

{{#cada_gateway}}
### Gateway {{gateway.numero}}: {{gateway.label}}

| Campo | Valor |
|-------|-------|
| **Tipo** | {{gateway.tipo}} |
| **Lane** | {{gateway.lane}} |
| **Posicao no fluxo** | Apos "{{gateway.atividade_anterior}}" |

**Ramos de saida:**

| Condicao | Proximo passo | Padrao? |
|----------|---------------|---------|
{{#cada_ramo}}
| {{ramo.condicao}} | {{ramo.destino}} | {{ramo.is_default}} |
{{/cada_ramo}}

**Convergencia**: {{gateway.convergencia_descricao}}

{{/cada_gateway}}

---

## 7. Excecoes e Eventos Intermediarios

{{#se_nivel_n1_n2}}
*Nivel logico ({{nivel}}). Excecoes nao modeladas neste nivel.*
{{/se_nivel_n1_n2}}

{{#se_sem_excecoes}}
*Nenhuma excecao ou evento intermediario identificado.*
{{/se_sem_excecoes}}

{{#cada_excecao}}
### {{excecao.numero}}. {{excecao.nome}}

| Campo | Valor |
|-------|-------|
| **Tipo** | {{excecao.tipo}} |
| **Atividade associada** | {{excecao.atividade_pai}} |
| **Condicao** | {{excecao.condicao}} |
| **Caminho resultante** | {{excecao.caminho_saida}} |

{{/cada_excecao}}

---

## 8. Eventos de Fim

| Evento | Tipo | Descricao |
|--------|------|-----------|
{{#cada_fim}}
| {{fim.label}} | {{fim.tipo}} | {{fim.descricao}} |
{{/cada_fim}}

---

## 9. Artefatos e Dados

{{#se_sem_artefatos}}
*Nenhum artefato ou dado especifico mapeado.*
{{/se_sem_artefatos}}

{{#se_tem_artefatos}}
| Artefato | Tipo | Atividades relacionadas |
|----------|------|------------------------|
{{#cada_artefato}}
| {{artefato.nome}} | {{artefato.tipo}} | {{artefato.atividades}} |
{{/cada_artefato}}
{{/se_tem_artefatos}}

---

## 10. Observacoes e Gaps Identificados

{{#se_sem_observacoes}}
*Nenhuma observacao ou gap identificado durante o mapeamento.*
{{/se_sem_observacoes}}

{{#cada_observacao}}
- **{{observacao.categoria}}**: {{observacao.descricao}}
{{/cada_observacao}}

---

## 11. Proximos Passos

- [ ] Revisar este descritivo com o responsavel pelo processo
- [ ] Gerar o arquivo `.bpmn` via skill `drawing-bpmn-flowcharts` usando o JSON de input
- [ ] Validar o BPMN gerado com o agente `bpmn-reviewer`
- [ ] Abrir o `.bpmn` no Camunda Modeler ou bpmn.io para validacao visual
- [ ] Alinhar com o DEIP correspondente (nivel N2) via skill `mapping-process-interfaces`

---

*Gerado por: skill `mapping-process-flows` — Plugin mapeamento-processos*
*Data de geracao: {{data}}*
