# Manual de Rituais de Gestão (MAN-PERF-003)

> **Nota**: starter MD para validação do pipeline. Representa o gold reference
> MAN-PERF-003 em formato canônico de Fase 2. Para byte-exatidão com o gold
> HTML, este MD precisa ser refinado iterativamente — não é a fonte original
> do gold (que foi gerado manualmente antes da skill existir).

## 1. Objetivo

Executar a cadência estruturada de rituais de gestão nos níveis tático (N2) e operacional (N3) das quatro verticais da Holding M7, garantindo que desvios de meta sejam identificados rapidamente, contramedidas sejam definidas via PDCA e boas práticas sejam padronizadas via SDCA.

Este manual define **o que fazer, quem faz, quais indicadores monitorar** e o que esperar como resultado de cada etapa do processo. O gestor é o dono do ritual; Performance facilita e apresenta dados, mas não decide.

## 2. Escopo

Este manual operacionaliza diretrizes de `POL-PERF-001 · Política de Performance`. Em caso de divergência, prevalecem os princípios e limites da política superior.

**Aplica-se a:**
- Rituais **N2 (tático, mensal, 90 min)** e **N3 (operacional, semanal, 60 min)** nas 4 verticais.
- Planejamento, preparação de materiais, distribuição, condução do ritual e registro de decisões.
- Gestores N2/N3, área de Performance e participantes designados das verticais.

**Não se aplica a:**
- Rituais estratégicos N1 (governança institucional) — regidos por POL-GOV-001.
- Definição de metas anuais — regida por SMP de Planejamento.
- Avaliações individuais de performance — regidas por POL-PES-001.

## 3. Definições

| Termo | Definição |
|-------|-----------|
| Briefing do Ritual | Documento em Markdown com pauta, contexto, pontos de atenção e sugestões analíticas, enviado ao Gestor antes do ritual para preparação. |
| Contramedida | Ação corretiva definida no ritual para tratar desvio de meta, com responsável, prazo e indicador vinculado. Registrada conforme INS-PERF-001. |
| Cowork (Claude) | Ferramenta de automação baseada em IA que gera materiais pré-ritual e auxilia na transcrição e geração de atas pós-ritual. |
| N2 / N3 | Níveis hierárquicos dos rituais: N2 é tático (mensal, 90 min); N3 é operacional (semanal, 60 min). |
| PDCA | Plan-Do-Check-Act — ciclo de melhoria contínua usado para tratar desvios de meta. |
| SDCA | Standardize-Do-Check-Act — ciclo de padronização usado para perenizar boas práticas. |
| Vertical | Unidade de negócio da Holding M7 (Crédito, Investimentos, Câmbio, Securitização). |

## 4. Visão Geral do Processo

Processo G2.3 (Rituais de Gestão) opera dentro do macroprocesso **G2 — Gestão de Performance**. Compreende 5 etapas sequenciais que vão do planejamento da pauta ao registro de decisões.

### 4.1 · Missão do processo

Garantir cadência estruturada de acompanhamento de performance que combina velocidade (rituais semanais N3) com profundidade (rituais mensais N2), traduzindo desvios em ações concretas via PDCA e perenizando aprendizados via SDCA.

### 4.2 · SIPOC

| Suppliers | Inputs | Process | Outputs | Customers |
|-----------|--------|---------|---------|-----------|
| Verticais de negócio | Indicadores e metas | E1 · Planejar | Pauta validada | Gestor N2/N3 |
| Performance | Histórico do último ritual | E2 · Preparar | Briefing + PPTX | Participantes |
| Cowork (Claude) | Dados consolidados | E3 · Distribuir | Material enviado | Gestor N2/N3 |
| Gestor N2/N3 | Ata anterior | E4 · Conduzir | Decisões registradas | Diretoria |
|              |        | E5 · Registrar & ata | Ata + plano | Comitê de Performance |

### 4.3 · Interfaces e dependências

Interfaces principais: **Performance** (provê briefing e dados), **Cowork** (gera materiais pré-ritual), **Gestor N2/N3** (conduz e decide), **INS-PERF-001** (registro formal de contramedidas), **POL-PERF-001** (diretrizes superiores).

### 4.4 · Fluxograma BPMN

:::diagrama
caption: Fig 1 · Fluxograma BPMN do processo de Rituais de Gestão (G2.3)

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 320">
  <!-- Evento início -->
  <circle cx="48" cy="65" r="14" class="bpmn-event-start"/>
  <text x="48" y="95" class="bpmn-event-label">Início</text>

  <!-- Tasks lane superior -->
  <g><rect class="bpmn-task" x="96" y="48" width="110" height="34" rx="4"/><text class="bpmn-task-label" x="151" y="65">E1 · Planejar</text></g>
  <g><rect class="bpmn-task" x="224" y="48" width="110" height="34" rx="4"/><text class="bpmn-task-label" x="279" y="65">E2 · Preparar</text></g>
  <g><rect class="bpmn-task" x="352" y="48" width="110" height="34" rx="4"/><text class="bpmn-task-label" x="407" y="65">E3 · Distribuir</text></g>

  <!-- Task lane inferior (E4 + E5) -->
  <g><rect class="bpmn-task" x="352" y="183" width="110" height="34" rx="4"/><text class="bpmn-task-label" x="407" y="200">E4 · Conduzir</text></g>
  <g><rect class="bpmn-task" x="730" y="48" width="140" height="34" rx="4"/><text class="bpmn-task-label" x="800" y="65">E5 · Registrar & ata</text></g>

  <!-- Gateway -->
  <g><path class="bpmn-gateway" d="M 510,178 L 532,200 L 510,222 L 488,200 Z"/><path class="bpmn-gateway-mark" d="M 502,192 L 518,208 M 518,192 L 502,208"/><text class="bpmn-task-label" x="510" y="244">Meta atingida?</text></g>

  <!-- Tasks de saída -->
  <g><rect class="bpmn-task" x="560" y="148" width="140" height="30" rx="4"/><text class="bpmn-task-label" x="630" y="163">Padronizar · SDCA</text></g>
  <g><rect class="bpmn-task" x="560" y="252" width="140" height="30" rx="4"/><text class="bpmn-task-label" x="630" y="267">Contramedida · PDCA</text></g>

  <!-- Evento fim 1 -->
  <circle cx="900" cy="163" r="14" class="bpmn-event-end"/>
  <text x="900" y="193" class="bpmn-event-label">Concluído</text>
</svg>
:::

**Narrativa do fluxo:**

1. **E1–E3** são executadas por Performance + Cowork: planejamento da pauta, preparação dos materiais (briefing markdown + PPTX), distribuição assíncrona ao Gestor com 24h de antecedência.
2. **E4** é o ritual em si, conduzido pelo Gestor N2. Ao final, aplica-se o Modelo de 4 Cenários: meta OK → padronização **SDCA**; meta NOK → contramedida **PDCA**.
3. **E5** registra decisões na ata, vincula contramedidas a indicadores e responsáveis, e dispara INS-PERF-001 para registro formal das ações.

## 5. Regras de Negócio

As regras a seguir governam a cadência e a estrutura dos rituais. Devem ser respeitadas em todas as verticais.

### 5.1 · Cadência e duração

1. **RN-01** · Rituais **N2** (táticos) com frequência mínima mensal e duração máxima de **90 min**; rituais **N3** (operacionais) com frequência mínima semanal e duração máxima de **60 min**.
2. **RN-02** · O Gestor N2 ou N3 é o único responsável pela decisão final no ritual; Performance facilita mas não decide.
3. **RN-03** · Materiais (briefing + PPTX) devem ser distribuídos com **24h** de antecedência ao ritual; sem material, o ritual é remarcado.

### 5.2 · Decisões e registro

4. **RN-04** · Toda contramedida (cenário PDCA) deve ter responsável, prazo e indicador vinculado. Sem esses três campos, a contramedida não é aceita.
5. **RN-05** · Padronizações (cenário SDCA) devem ser documentadas em SOP/INS antes do próximo ritual.
6. **RN-06** · A ata do ritual deve ser publicada em até **48h** após o ritual; ausência de ata invalida as decisões do ritual seguinte.

### 5.3 · Exceções permitidas

| Exceção | Aprovador |
|---------|-----------|
| Adiar ritual N2 em até 7 dias por agenda do Gestor | Head de Performance |
| Reduzir frequência de N3 para quinzenal por 2 ciclos | Diretoria + Head de Performance |

## 6. Papéis e Responsabilidades

A matriz RACI a seguir define responsabilidades das 5 atividades-chave do processo. Para detalhes de cada papel, ver POL-PERF-001.

### 6.1 · Matriz RACI

| Atividade | Gestor N2/N3 | Performance | Cowork | Participantes | Diretoria |
|-----------|--------------|-------------|--------|---------------|-----------|
| E1 · Planejar pauta | A | R | C | I | I |
| E2 · Preparar materiais | C | A | R | I | I |
| E3 · Distribuir | I | A | R | I | I |
| E4 · Conduzir ritual | A,R | C | I | C | I |
| E5 · Registrar ata | A | R | C | I | I |

**Legenda**: R = Responsible · A = Accountable · C = Consulted · I = Informed

## 7. Indicadores

Indicadores monitorados pelo processo. KPIs medem resultado; PPIs medem execução.

### 7.1 · KPIs — indicadores de resultado

| Nome | Fórmula | Meta | Frequência | Fonte |
|------|---------|------|------------|-------|
| Aderência a metas N2 | (Verticais com meta atingida / Total verticais) × 100 | ≥ 75% | Mensal | Dashboard Performance |
| Tempo de tratamento de desvio | Média (dias entre identificação e contramedida) | ≤ 5 dias | Mensal | INS-PERF-001 |

### 7.2 · PPIs — indicadores de processo

| Nome | Fórmula | Meta | Frequência | Fonte |
|------|---------|------|------------|-------|
| Pontualidade do briefing | (Briefings entregues em até 24h antes / Total briefings) × 100 | ≥ 95% | Semanal | Cowork logs |
| Aderência à pauta | (Itens pauta executados / Itens pauta planejados) × 100 | ≥ 90% | Semanal | Ata do ritual |

## 8. Cronograma e Frequência

Cadência das atividades do processo ao longo do ano.

| Cadência | Ritual / Atividade | Output |
|----------|--------------------|--------|
| Diária | — | — |
| Semanal | Ritual N3 (operacional, 60 min) | Ata + plano semanal |
| Mensal | Ritual N2 (tático, 90 min) | Ata + contramedidas/padronizações |
| Trimestral | Revisão de indicadores e metas | Relatório QBR |
| Semestral | Revisão deste manual | Versão aprovada + changelog |

## 9. Critérios de Qualidade

Como avaliar se o processo está funcionando bem:

1. **DTO-01** — 100% dos rituais N2 acontecem na frequência mensal definida (mensurado: presença na ata).
2. **DTO-02** — Briefings distribuídos em até 24h antes do ritual em ≥ 95% dos casos.
3. **DTO-03** — Toda contramedida do cenário PDCA tem responsável, prazo e indicador vinculados.
4. **DTO-04** — Atas publicadas em até 48h após o ritual em ≥ 90% dos casos.
5. **DTO-05** — Zero ritual realizado sem material pré-distribuído (regra dura).

## 10. Documentos Relacionados

| Código | Título | Tipo |
|--------|--------|------|
| POL-PERF-001 | Política de Performance | Documento superior |
| INS-PERF-001 | Instrução de registro de contramedidas | Subordinado |
| INS-PERF-002 | Instrução de preparação de briefing | Subordinado |
| ESP-PERF-001 | Especificação técnica do dashboard Performance | Subordinado |

---

**Controle de Versões**

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| v1.0 | 19/05/2026 | Bruno Chiaramonti · Head de Desempenho | Versão inicial. |
