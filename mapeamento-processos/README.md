# Mapeamento de Processos

Plugin de mapeamento e construcao de processos BPM para o [Cowork](https://claude.com/product/cowork). Gere fluxogramas BPMN 2.0 como arquivos XML (.bpmn) compativeis com Camunda Modeler/bpmn.io/Bizagi e Diagramas DEIP como HTML autocontido. Segue a metodologia BPM CBOK com notacao padronizada.

## O que faz

Este plugin da ao Claude a capacidade de mapear processos de ponta a ponta:

- **DEIP (escopo)** — Defina as fronteiras do processo antes de desenha-lo: regulacao, fornecedores, entradas, macrofluxo, saidas, clientes e suporte. Sinalizacao automatica por cores (conforme/melhoria).
- **BPMN (fluxo)** — Gere fluxogramas completos em notacao BPMN 2.0 como arquivos XML (.bpmn) compativeis com Camunda, bpmn.io e Bizagi. Pools, lanes, gateways, eventos e atividades. Dois niveis: logica (N1-N2) e fisica (N3-N5).
- **Analise metodologica** — Agents especializados decompoe processos em 5 niveis (N1-N5), identificam gaps e validam notacao.

## Skills

O plugin tem dois pares de skills simetricas — uma skill de **mapeamento** (entrevista estruturada) e uma de **geracao** (artefato tecnico):

| Par | Skill de Mapeamento | Skill de Geracao |
|-----|---------------------|-----------------|
| **DEIP** | `mapping-process-interfaces` | `drawing-deip-diagrams` |
| **BPMN** | `mapping-process-flows` | `drawing-bpmn-flowcharts` |

| Skill | Descricao |
|-------|-----------|
| `mapping-process-flows` | Entrevista estruturada (8 fases) para mapear o fluxo de atividades de um processo. Coleta participantes, eventos, atividades, gateways e excecoes, adaptando ao nivel de modelagem (N1–N5). Gera JSON para `drawing-bpmn-flowcharts` + descritivo Markdown |
| `drawing-bpmn-flowcharts` | Gera arquivos BPMN 2.0 XML (.bpmn) compativeis com Camunda Modeler, bpmn.io e Bizagi, acompanhados de descritivo Markdown (.md). Auto-layout para diagram interchange, suporte completo a pools/lanes/gateways/eventos |
| `mapping-process-interfaces` | Entrevista estruturada (8 fases) para mapear interfaces de processo (DEIP/SIPOC). Coleta dimensoes output-first, avalia desconexoes e gera DEIP JSON v2 + descritivo Markdown + tabela de desconexoes Excel |
| `drawing-deip-diagrams` | Gera Diagramas DEIP interativos como HTML autocontido. Layout CSS Grid com 5 colunas, badges de status por cor, macrofluxo visual e otimizacao para impressao A4 landscape |

**Fluxo recomendado**: `process-analyst` (analisar) → `mapping-process-interfaces` (escopo DEIP) → `drawing-deip-diagrams` (visual DEIP) → `mapping-process-flows` (mapeamento BPMN) → `drawing-bpmn-flowcharts` (fluxo BPMN) → `bpmn-reviewer` (validar)

## Agents

Subagentes especializados que Claude invoca automaticamente em contexto isolado.

| Agent | Quando e invocado | Output |
|-------|--------------------|--------|
| `process-analyst` | Decomposicao, analise e validacao de processos BPM N1-N5. Classifica processos, elabora DEIPs, identifica gaps e sugere indicadores | Relatorio de mapeamento com gap analysis e recomendacoes |
| `bpmn-reviewer` | Validacao de notacao BPMN apos geracao de fluxograma. Verifica eventos, gateways, nomenclatura, direcao de fluxo e completude | Checklist de conformidade com status por regra |

## Exemplos de Uso

### Mapear fluxo BPMN por entrevista (sem saber o JSON)

```
Voce: Preciso mapear o fluxo do processo de aprovacao de credito.

Claude: [Inicia entrevista com mapping-process-flows]
        [Coleta participantes, caminho feliz, decisoes, excecoes via AskUserQuestion]
        [Gera JSON bpmn-input.json pronto para drawing-bpmn-flowcharts]
        [Desenha o .bpmn com auto-layout e descritivo .md]
        [Valida notacao com bpmn-reviewer]
```

### Mapear um processo do zero (DEIP + BPMN completo)

```
Voce: Preciso mapear o processo de captacao de clientes PF da M7.

Claude: [Analisa o contexto com process-analyst]
        [Conduz entrevista de interfaces com mapping-process-interfaces]
        [Gera DEIP interativo com sinalizacao de interfaces]
        [Conduz entrevista de fluxo com mapping-process-flows]
        [Constroi fluxograma BPMN com pools e lanes]
        [Valida notacao com bpmn-reviewer]
```

### Gerar DEIP a partir de descricao

```
Voce: Crie um DEIP para o processo de onboarding de novos assessores.
      Fornecedores: RH, Compliance, TI. Clientes: Assessor, Gestao.

Claude: [Completa as dimensoes faltantes via entrevista]
        [Gera HTML com layout DEIP classico]
        [Sinaliza interfaces com oportunidade de melhoria]
```

### Desenhar BPMN a partir de JSON

```
Voce: Tenho esse JSON com o fluxo. Gere o diagrama BPMN.
      [cola JSON estruturado]

Claude: [Valida estrutura do JSON]
        [Gera .bpmn XML + descritivo .md com auto-layout]
        [Sugere melhorias de nomenclatura]
```

## Referencia Metodologica

- **BPM CBOK 3.0/4.0** — ABPMP (classificacao, niveis, governanca)
- **Capacitacao em Gestao por Processos** — Instituto Aquila / Votorantim Cimentos (2018)
- **BPMN 2.0** — OMG (notacao padrao)
- **Lean** — 7 desperdicios aplicados a processos administrativos

## Design System (DEIP)

O design system M7-2026 aplica-se aos Diagramas DEIP (HTML autocontido):

| Elemento | Valor |
|----------|-------|
| Fonte | TWK Everett |
| Cor primaria | `#424135` Verde Caqui |
| Background | `#fffdef` Off-White |
| Acento | `#eef77c` Lime |
| Conforme | `#4CAF50` Verde |
| Melhoria | `#E46962` Vermelho |

Os fluxogramas BPMN sao gerados como XML padrao (.bpmn) sem estilizacao visual — a aparencia e controlada pela ferramenta de visualizacao (Camunda Modeler, bpmn.io, etc.).
