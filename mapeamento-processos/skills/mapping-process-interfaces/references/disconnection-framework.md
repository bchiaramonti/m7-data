# Framework de Desconexoes — Avaliacao de Interfaces de Processo

Referencia para identificacao, classificacao e priorizacao de desconexoes em interfaces de processo.

---

## 1. O que e uma Desconexao

Uma desconexao e uma **falha ou gap na interface** entre o processo e uma entidade externa (fornecedor, cliente, regulador, recurso de suporte). Desconexoes comprometem a eficiencia, qualidade e conformidade do processo.

> "Se a interface e o ponto de contato, a desconexao e o atrito nesse ponto."

---

## 2. Os 4 Tipos de Interface

Cada processo tem 4 tipos de interface que podem apresentar desconexoes:

### 2.1 Fornecedor → Entrada

**Pergunta-chave**: O fornecedor entrega o insumo no formato, prazo e qualidade corretos?

| Desconexao | Descricao | Exemplo |
|-----------|-----------|---------|
| Informacao incompleta | Input chega sem todos os campos necessarios | Lead sem telefone de contato |
| Prazo nao cumprido | Input chega atrasado | Documentos entregues apos prazo de analise |
| Formato inadequado | Input vem em formato que requer conversao | Dados em PDF quando sistema precisa de planilha |
| Fornecedor indefinido | Nao esta claro quem e responsavel pelo input | Pedido chega por email sem remetente padrao |
| Qualidade inconsistente | Input varia em qualidade entre entregas | Relatorios com criterios diferentes a cada vez |

### 2.2 Entrada → Processo

**Pergunta-chave**: O processo consegue consumir a entrada adequadamente?

| Desconexao | Descricao | Exemplo |
|-----------|-----------|---------|
| Sistemas nao integrados | Input requer digitacao manual no sistema | Copiar dados de email para CRM manualmente |
| Validacao ausente | Input nao e verificado antes do processamento | Documento aceito sem conferir assinatura |
| Gargalo de recepcao | Input acumula esperando processamento | Pilha de pedidos nao triados |
| Duplicidade de entrada | Mesmo input registrado em multiplos sistemas | Cadastro feito no CRM e na planilha |

### 2.3 Processo → Saida

**Pergunta-chave**: O processo produz a saida de forma consistente e com qualidade?

| Desconexao | Descricao | Exemplo |
|-----------|-----------|---------|
| Retrabalho frequente | Saida e devolvida para correcao | Proposta rejeitada por erro de calculo |
| Saida incompleta | Produto entregue sem todos os componentes | Relatorio sem anexos obrigatorios |
| SLA nao definido | Nao ha prazo acordado para entrega | Cliente nao sabe quando recebera resposta |
| Variabilidade de qualidade | Qualidade depende de quem executa | Pareceres com profundidade diferente por analista |
| Falta de POP | Nao ha procedimento documentado para producao | Processo depende de conhecimento tacito |

### 2.4 Saida → Cliente

**Pergunta-chave**: O cliente recebe o que precisa, quando precisa, no formato que precisa?

| Desconexao | Descricao | Exemplo |
|-----------|-----------|---------|
| Canal inadequado | Saida entregue por meio nao adequado | Relatorio enviado por email quando deveria estar no sistema |
| Expectativa desalinhada | Cliente espera algo diferente do que recebe | Relatorio detalhado quando queria resumo executivo |
| Feedback inexistente | Cliente nao tem como reportar problemas | Nao ha canal para reclamacao sobre a entrega |
| Timing incorreto | Saida chega fora do momento util | Relatorio mensal entregue na segunda quinzena |

---

## 3. Taxonomia de Desconexoes

Classificacao consolidada para uso na tabela de desconexoes:

| Codigo | Tipo | Descricao |
|--------|------|-----------|
| D01 | Informacao incompleta | Input/output com campos ou dados faltantes |
| D02 | Prazo nao cumprido | Entrega fora do prazo acordado ou esperado |
| D03 | Formato inadequado | Entrega em formato que requer conversao ou adaptacao |
| D04 | Sistemas nao integrados | Necessidade de digitacao manual ou transferencia entre sistemas |
| D05 | Handoff manual | Transferencia entre areas depende de acao humana (email, reuniao) |
| D06 | Falta de POP | Ausencia de procedimento documentado |
| D07 | SLA nao definido | Sem acordo de nivel de servico para a interface |
| D08 | Retrabalho frequente | Saida devolvida para correcao com frequencia |
| D09 | Qualidade inconsistente | Variabilidade na qualidade dependendo de quem executa |
| D10 | Validacao ausente | Input aceito sem verificacao de completude/correcao |
| D11 | Duplicidade | Mesmo dado registrado em multiplos sistemas/documentos |
| D12 | Feedback inexistente | Sem canal para retorno sobre qualidade da interface |
| D13 | Responsavel indefinido | Nao esta claro quem e dono da interface |
| D14 | Regulacao nao atendida | Processo nao cumpre requisito normativo |
| D15 | Recurso insuficiente | Suporte (pessoas, sistema, equipamento) inadequado |

---

## 4. Escala de Impacto

| Nivel | Criterio | Exemplos |
|-------|----------|---------|
| **Alto** | Paralisa o processo, gera risco regulatorio/financeiro, ou afeta o cliente final | Processo parado por falta de aprovacao; multa regulatoria; perda de cliente |
| **Medio** | Gera retrabalho significativo, atraso no ciclo, ou custo adicional | Refazer relatorio; atraso de 2+ dias; horas extras |
| **Baixo** | Inconveniencia operacional, impacto menor na rotina | Copiar dados manualmente; espera de 1 hora; ajuste cosmetico |

### Criterios de Decisao

Para classificar o impacto, considerar:

1. **Frequencia**: Acontece diariamente? Semanalmente? Raramente?
2. **Abrangencia**: Afeta 1 pessoa ou toda a equipe/area?
3. **Reversibilidade**: O dano e recuperavel? Quanto tempo leva?
4. **Consequencia externa**: O cliente final percebe? Ha implicacao regulatoria?

---

## 5. Matriz Impacto x Frequencia

Para priorizar acoes corretivas:

```
                    FREQUENCIA
                    Raro    Ocasional  Frequente
Impacto Alto    | Planejar | Priorizar | URGENTE  |
Impacto Medio   | Monitorar| Planejar  | Priorizar|
Impacto Baixo   | Aceitar  | Monitorar | Planejar |
```

| Acao | Significado |
|------|-------------|
| **URGENTE** | Acao imediata — risco ao processo/cliente |
| **Priorizar** | Incluir no proximo ciclo de melhoria |
| **Planejar** | Agendar para tratamento futuro |
| **Monitorar** | Acompanhar indicadores sem acao imediata |
| **Aceitar** | Risco aceitavel, nao requer acao |

---

## 6. Sugestoes de Acao por Tipo de Desconexao

| Desconexao | Acoes Tipicas |
|-----------|--------------|
| D01 — Informacao incompleta | Criar checklist de completude; automatizar validacao na entrada |
| D02 — Prazo nao cumprido | Definir SLA formal; criar alerta automatico de prazo |
| D03 — Formato inadequado | Padronizar template de entrega; implementar integracao |
| D04 — Sistemas nao integrados | Avaliar integracao via API/RPA; criar interface automatica |
| D05 — Handoff manual | Digitalizar handoff; criar workflow automatizado |
| D06 — Falta de POP | Documentar procedimento; validar com executores |
| D07 — SLA nao definido | Negociar SLA com fornecedor/cliente; registrar em acordo formal |
| D08 — Retrabalho frequente | Identificar causa raiz; implementar verificacao pre-entrega |
| D09 — Qualidade inconsistente | Padronizar criterios; criar checklist de qualidade |
| D10 — Validacao ausente | Implementar gate de verificacao; automatizar validacao |
| D11 — Duplicidade | Definir sistema master; eliminar registros paralelos |
| D12 — Feedback inexistente | Criar canal de retorno; implementar pesquisa de satisfacao |
| D13 — Responsavel indefinido | Designar dono da interface; documentar RACI |
| D14 — Regulacao nao atendida | Mapear gap regulatorio; plano de adequacao |
| D15 — Recurso insuficiente | Dimensionar necessidade; solicitar recurso adicional |

---

## 7. Exemplo Completo de Avaliacao

### Interface I2: Cliente prospect → Documentos pessoais

**Avaliacao:**
- Status: **Melhoria** 🔴
- Desconexao: D01 — Informacao incompleta
- Descricao: "Documentos chegam frequentemente incompletos — falta comprovante de renda em 40% dos casos"
- Impacto: **Medio** — gera retrabalho de solicitacao e atraso de 3 dias no ciclo
- Frequencia: **Frequente**
- Priorizacao: **Priorizar** (Medio x Frequente)
- Acao sugerida: "Criar checklist digital de documentos obrigatorios com upload guiado; enviar ao cliente antes da reuniao"

### Interface O1: Cliente cadastrado → Gestao de Carteira

**Avaliacao:**
- Status: **Conforme** 🟢
- Nota: "Cadastro e automaticamente transferido via sistema apos aprovacao do compliance"
