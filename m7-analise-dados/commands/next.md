---
description: Avança para o próximo passo do pipeline de análise, verificando entry criteria e invocando a skill correspondente
---

# Analysis Next

## Objetivo

Determinar a próxima fase pendente do pipeline, verificar se os pré-requisitos estão atendidos, e invocar a skill correspondente para executá-la.

## Processo

### 1. Localizar CLAUDE.md

Procurar `CLAUDE.md` no diretório atual. Se não encontrar:
"Nenhum projeto de análise encontrado. Execute `/m7-analise-dados:initializing-analysis` para criar um."

### 2. Determinar fase atual

Ler a tabela de status do CLAUDE.md. Encontrar a **primeira fase com status ⬜ Pendente**.

Se todas as fases (0-3) estão ✅:
- "Pipeline completo! Todas as fases foram concluídas."
- PARAR

### 3. Verificar entry criteria

Para a fase identificada, verificar os pré-requisitos:

| Fase | Entry Criteria | Como verificar |
|------|----------------|----------------|
| **1 — Discovery** | BRIEFING.md preenchido | `docs/BRIEFING.md` existe e não tem apenas placeholders |
| **2 — Planejamento** | Objetivo e audiência definidos | `docs/BRIEFING.md` tem objetivo e audiência preenchidos |
| **3 — Execução** | PLANO-ANALISE.md existe | `./PLANO-ANALISE.md` existe e tem métricas definidas |

Se entry criteria **NÃO atendidos**:

```
Não é possível avançar para a Fase [N] — [Nome].

Pré-requisitos não atendidos:
  ⬜ [descrição do que falta]

Ação necessária: [o que fazer para resolver]
```

PARAR — não avançar.

### 4. Tratar Fase 1 como opcional

A Fase 1 (Discovery) pode ser pulada. Se a próxima fase pendente é 1:

Perguntar ao usuário: "A Fase 1 (Discovery) é opcional. Deseja executá-la ou pular para Fase 2 (Planejamento)?"

- Se **executar**: continuar com Fase 1
- Se **pular**: marcar Fase 1 como ⏭️ Pulada no CLAUDE.md e avançar para Fase 2

### 5. Invocar a skill correspondente

Mapear fase → skill e executar:

| Fase | Skill | Invocação |
|------|-------|-----------|
| 1 | `exploring-data-sources` | Seguir SKILL.md — EDA sobre as fontes de dados |
| 2 | `planning-analysis` | Seguir SKILL.md — entrevista colaborativa + gerar PLANO-ANALISE.md |
| 3 | `generating-executive-reports` | Seguir SKILL.md — pipeline data-scientist → executive-communicator |

**Importante**: Executar a skill com o contexto do projeto. Informar à skill:
- Diretório de trabalho: diretório atual
- Objetivo e audiência: do CLAUDE.md
- Artefatos existentes: listar o que já foi produzido

### 6. Atualizar CLAUDE.md

Após a skill concluir com sucesso:

1. Atualizar a tabela de status: `⬜ Pendente` → `✅ Completa`
2. Atualizar a linha "> **Fase atual**:" para refletir o novo estado
3. Se há próxima fase: indicar qual é

### 7. Sugerir próximo passo

```
Fase [N] — [Nome] concluída ✅

Artefato(s) gerado(s):
  [caminho do artefato]

Próximo passo:
  - /m7-analise-dados:review — validar consistência dos dados desta fase
  - /m7-analise-dados:next — avançar para Fase [N+1] — [Nome]
  - /m7-analise-dados:status — ver progresso geral
```

## Casos Especiais

### Fase já em andamento

Se a skill correspondente à fase atual já foi parcialmente executada (ex: data-scientist extraiu dados mas executive-communicator ainda não gerou relatório na Fase 3):
- Não reiniciar a fase do zero
- Continuar de onde parou, lendo outputs existentes

### Erro durante execução

Se a skill falhar ou o usuário cancelar:
- NÃO atualizar o status no CLAUDE.md
- Informar o que aconteceu e como retomar
- Sugerir: "Execute `/m7-analise-dados:next` novamente para retomar"
