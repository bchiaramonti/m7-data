# DEIP Descritivo — {{processName}}

> Diagrama de Escopo, Interface e Processos — Mapeamento descritivo completo

| Campo | Valor |
|-------|-------|
| **Codigo** | {{code}} |
| **Responsavel** | {{responsible}} |
| **Nivel BPM** | {{level}} |
| **Data** | {{date}} |
| **Versao** | {{version}} |

---

## Objetivo do Processo

{{objective}}

---

## Saidas e Clientes

| # | Saida | Descricao | Cliente | Tipo | Status |
|---|-------|-----------|---------|------|--------|
{{#outputs}}
| {{id}} | {{name}} | {{description}} | {{customer}} | {{customerType}} | {{statusIcon}} |
{{/outputs}}

---

## Entradas e Fornecedores

| # | Entrada | Descricao | Fornecedor | Tipo | Status |
|---|---------|-----------|------------|------|--------|
{{#inputs}}
| {{id}} | {{name}} | {{description}} | {{supplier}} | {{supplierType}} | {{statusIcon}} |
{{/inputs}}

---

## Macrofluxo (N3)

{{#macroflow}}
{{index}}. {{step}}
{{/macroflow}}

---

## Regulacao

| # | Documento | Tipo | Status | Observacao |
|---|-----------|------|--------|------------|
{{#regulation}}
| {{id}} | {{name}} | {{type}} | {{statusIcon}} | {{note}} |
{{/regulation}}

{{#noRegulation}}
> Sem regulacao identificada.
{{/noRegulation}}

---

## Suporte

| # | Recurso | Tipo | Detalhe |
|---|---------|------|---------|
{{#support}}
| {{id}} | {{name}} | {{type}} | {{detail}} |
{{/support}}

---

## Resumo de Interfaces

| Zona | Total | Conforme | Melhoria | Nao Avaliado |
|------|-------|----------|----------|-------------|
| Saidas (O) | {{outputsTotal}} | {{outputsConforme}} | {{outputsMelhoria}} | {{outputsNeutral}} |
| Entradas (I) | {{inputsTotal}} | {{inputsConforme}} | {{inputsMelhoria}} | {{inputsNeutral}} |
| Suporte (S) | {{supportTotal}} | {{supportConforme}} | {{supportMelhoria}} | {{supportNeutral}} |
| Regulacao (R) | {{regulationTotal}} | {{regulationConforme}} | {{regulationMelhoria}} | {{regulationNeutral}} |
| **Total** | **{{totalInterfaces}}** | **{{totalConforme}}** | **{{totalMelhoria}}** | **{{totalNeutral}}** |

---

## Analise de Desconexoes

{{#hasDisconnections}}
| # | Interface | Zona | Desconexao | Impacto | Acao Sugerida |
|---|-----------|------|------------|---------|---------------|
{{#disconnections}}
| {{seq}} | {{id}} | {{zone}} | {{description}} | {{impact}} | {{suggestedAction}} |
{{/disconnections}}
{{/hasDisconnections}}

{{#noDisconnections}}
> Nenhuma desconexao identificada. Todas as interfaces estao conformes.
{{/noDisconnections}}

---

## Proximos Passos

- [ ] Gerar DEIP visual HTML (`drawing-deip-diagrams`)
- [ ] Detalhar fluxograma BPMN (`drawing-bpmn-flowcharts`)
- [ ] Validar BPMN com `bpmn-reviewer`
{{#hasDisconnections}}
- [ ] Tratar desconexoes de impacto Alto
- [ ] Planejar melhorias para desconexoes de impacto Medio
{{/hasDisconnections}}

---

*Gerado por `mapping-process-interfaces` | Metodologia BPM CBOK | {{date}}*
