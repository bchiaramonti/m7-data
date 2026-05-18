# Padrões Normativos M7 — Referência Completa

Extraído da POL-M7-001: Política de Gestão por Processos e Padronização.

> **Pipeline de geração**: a Fase 3 da skill produz um par `{slug}.html` + `{slug}.yaml`
> (não mais DOCX). Detalhes de formatação visual estão no template HTML
> (`assets/politica-m7-template.html`) e os anchors YAML→HTML em
> [normativo-schema.md](normativo-schema.md).

## Hierarquia Normativa

| Nível | Código | Tipo | Pergunta que Responde | Público-Alvo | Aprovador |
|-------|--------|------|----------------------|--------------|-----------|
| Estratégico | POL | Política | "Por quê e dentro de quais limites?" | Toda a organização | Diretoria |
| Tático | MAN | Manual | "O que fazer e o que esperar?" | Gestores e líderes | Head de área |
| Operacional | INS | Instrução | "Como fazer, passo a passo?" | Executores | Líder do processo |
| Técnico | ESP | Especificação Técnica | "Com quais dados e regras de cálculo?" | Analistas, TI | Analista responsável |

Documentos de nível superior orientam e restringem os de nível inferior.

## Sistema de Codificação

Formato: `[TIPO]-[AREA]-[NNN]`

| Componente | Descrição | Valores Válidos |
|------------|-----------|-----------------|
| TIPO | Tipo de documento | `POL`, `MAN`, `INS`, `ESP` |
| AREA | Área ou processo | `GOV`, `PERF`, `INV`, `CRE`, `SEG`, `UNI`, `TEC`, `PES`, `M7` |
| NNN | Número sequencial (3 dígitos, zero-padded) | `001`, `002`, `003`... |

Exemplos:
- `POL-GOV-002`: Política Geral de Governança Corporativa
- `POL-M7-001`: Política de Gestão por Processos
- `MAN-INV-001`: Manual de Operação do Funil Investimentos
- `INS-PERF-001`: Instrução de Fechamento Mensal de Performance
- `ESP-PERF-001`: Especificação de Cálculo de Indicadores

## Ciclo de Vida do Documento

| Etapa | Responsável | Descrição |
|-------|-------------|-----------|
| 1. Elaboração | Analista / Líder | Redigir conforme template padrão |
| 2. Revisão | Pares / Stakeholders | Revisar conteúdo, coerência, aplicabilidade |
| 3. Aprovação | Conforme hierarquia | Aprovação formal |
| 4. Publicação | Performance | Publicar no repositório oficial, comunicar |
| 5. Treinamento | Líder do Processo | Treinar equipe no novo padrão |
| 6. Verificação | Performance / Líder | Avaliar aderência |
| 7. Revisão periódica | Dono do documento | Atualizar conforme frequência definida |

## Frequências de Revisão

| Tipo | Frequência |
|------|------------|
| POL (Política) | Anual |
| MAN (Manual) | Semestral |
| INS (Instrução) | Trimestral |
| ESP (Especificação Técnica) | Trimestral |

## Status do Documento (campo `identity.status`)

| Status | Significado |
|--------|-------------|
| `vigente` | Aprovado e em vigor |
| `revisao` | Revisão periódica em andamento |
| `rascunho` | Em elaboração — não publicado |
| `pendente` | Previsto pela hierarquia, ainda não iniciado |
| `vencido` | Fora do prazo de revisão obrigatória |

## Quando Documentar é Obrigatório

- Novo processo implementado
- Processo existente remodelado
- Atividade com alto impacto em qualidade, segurança, custo ou compliance
- Dependência de conhecimento tácito em pessoas específicas
- Processos recorrentes (rituais, reuniões, rotinas) instituídos ou alterados

## Estrutura de Conteúdo de uma POL

Toda Política deve conter, na ordem:

1. **Objetivo** — propósito (1-2 parágrafos)
2. **Escopo** — cobertura: "aplica-se a..." + "não se aplica a..."
3. **Definições** — termos técnicos em tabela alfabética
4. **Princípios** — 3-8 itens; cada um com título + parágrafo explicativo
5. **Diretrizes** — regras organizadas em subseções (5.1, 5.2...)
6. **Papéis & Responsabilidades** — tabela com 3+ papéis cobrindo Estratégico/Tático/Operacional
7. **Governança** — 7.1 Revisão; 7.2 Indicadores; 7.3 Escalonamento de Exceções
8. **Disposições Finais** — Vigência + Documentos relacionados

## Regras de Referência Cruzada

- Todo documento referencia seu documento superior via `governance.parent.code`
- MAN lista INS e ESP relacionados em "Documentos Relacionados"
- INS lista MAN e ESP relacionados em "Referências"
- ESP lista dependências de sistema em "Dependências e Integrações"
- POL lista documentos relacionados em "Disposições Finais"
- **Sempre usar código do documento** para referências cruzadas (ex: `MAN-INV-001`), nunca texto livre

## Indicadores de Governança

| Indicador | Fórmula | Frequência | Meta |
|-----------|---------|------------|------|
| Cobertura documental | Processos documentados / Processos mapeados | Trimestral | >= 80% |
| Atualização de documentos | Dentro da validade / Total documentos | Trimestral | >= 90% |
| Aderência ao padrão | Conformes ao template / Total documentos | Semestral | 100% |

## Escalonamento de Exceções

| Tipo de Exceção | Aprovador |
|-----------------|-----------|
| Formato ou template do documento | Head de Área |
| Prazo ou cadência de revisão | Head de Área |
| Dispensa de documentação obrigatória | Diretoria |
| Alteração na hierarquia normativa | Diretoria |
