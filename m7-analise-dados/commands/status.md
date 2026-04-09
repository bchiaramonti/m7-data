---
description: Mostra o progresso da análise atual, fase corrente e sugere próximo passo
---

# Analysis Status

## Objetivo

Ler o CLAUDE.md do projeto de análise e apresentar uma visão clara do progresso, indicando a fase atual e o próximo passo recomendado.

## Processo

### 1. Localizar CLAUDE.md

Procurar `CLAUDE.md` no diretório atual. Se não encontrar:
"Nenhum projeto de análise encontrado. Execute `/m7-analise-dados:initializing-analysis` para criar um."

### 2. Parsear estado

Ler o CLAUDE.md e extrair:
- **Metadata**: título, objetivo, audiência, período
- **Tabela de status**: parsear a tabela de fases e identificar status de cada uma (✅/⬜)
- **Fase atual**: primeira fase com status ⬜ (ou última ✅ se todas completas)

### 3. Verificar artefatos físicos

Confirmar existência real dos artefatos (não confiar apenas na tabela):

| Fase | Artefato | Caminho |
|------|----------|---------|
| 0 | CLAUDE.md | `./CLAUDE.md` |
| 0 | BRIEFING.md | `./docs/BRIEFING.md` |
| 1 | DATA-PROFILE.md | `./DATA-PROFILE.md` |
| 2 | PLANO-ANALISE.md | `./PLANO-ANALISE.md` |
| 2 | INDICADORES.md | `./docs/INDICADORES.md` |
| 3 | Relatório | `./output/relatorio-*.md` |
| 3 | Outputs data-scientist | `./output/data-scientist/*.md` |

Se houver divergência entre tabela e arquivos físicos (ex: tabela diz ⬜ mas artefato existe), sinalizar.

### 4. Calcular progresso

- Contar fases com ✅ / total de fases obrigatórias (0-3 = 4 fases)

### 5. Apresentar visual

```
Análise: [Título da Análise]
Audiência: [audiência] | Período: [período]

Pipeline:
  [✅] 0 Setup
  [✅] 1 Discovery
  [>>] 2 Planejamento          ← fase atual
  [  ] 3 Execução

Progresso: 2/4 fases (50%)

Artefatos da fase atual:
  ✅ docs/BRIEFING.md
  ⬜ PLANO-ANALISE.md
  ⬜ docs/INDICADORES.md

Próximo passo: [sugestão contextual]
```

### 6. Sugerir próximo passo

| Estado | Sugestão |
|--------|----------|
| Fase com artefatos pendentes | "Execute `/m7-analise-dados:next` para avançar" |
| Fase recém-concluída, sem review | "Execute `/m7-analise-dados:review` para validar consistência" |
| Todas as fases obrigatórias ✅ | "Análise completa! Execute `/m7-analise-dados:review` para revisão final." |
| Divergência tabela vs arquivos | "Divergência detectada: [artefato] existe mas tabela marca ⬜. Atualize o CLAUDE.md." |
