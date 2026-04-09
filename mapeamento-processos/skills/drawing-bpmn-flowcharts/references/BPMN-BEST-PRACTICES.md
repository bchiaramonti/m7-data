# Boas Praticas BPMN 2.0

Regras de qualidade para modelagem BPMN. Validadas pelo agent `bpmn-reviewer`.
Fonte: BPM CBOK 3.0, gestao-de-processos-book.md secao 6.4 e 5.5.

---

## 1. Nomenclatura de Atividades

### Regra

Atividades devem ser nomeadas com **verbo no infinitivo** ou **3a pessoa do singular** + complemento.

| Correto | Incorreto |
|---------|-----------|
| `Verificar proposta` | `Proposta` (substantivo sem acao) |
| `Analisar documento` | `Analise de documento` (substantivo) |
| `Aprovar solicitacao` | `Aprovacao` (substantivo) |
| `Registrar pedido` | `Pedido registrado` (passivo) |
| `Envia notificacao` | `Notificacao enviada` (passivo) |

### Anti-patterns

- Nomes genericos: "Processar", "Executar", "Fazer"
- Nomes longos demais (>5 palavras): quebrar em subprocesso
- Abreviacoes sem contexto: "Proc. Doc." (usar nome completo)

---

## 2. Gateways

### Regras obrigatorias

1. **Todo gateway de divergencia deve ter par de convergencia** do mesmo tipo
2. **Labels obrigatorios**: pergunta no gateway OU respostas nos fluxos de saida
3. **Caminho default**: todo XOR gateway deve ter caminho default (sem condicao)

### Formato de labels

| Gateway | Label no gateway | Labels nos fluxos |
|---------|-----------------|-------------------|
| **XOR** | Pergunta? (ex: "Aprovado?") | Respostas (ex: "Sim" / "Nao") |
| **AND** | — (nao precisa) | — (todos seguem) |
| **OR** | Pergunta geral | Condicoes (ex: "Se valor > 100k") |
| **Event-based** | — | Tipo do evento |

### Erros comuns

- Gateway sem label E sem labels nos fluxos
- XOR com mais de 3-4 saidas (considerar tabela de decisao)
- AND sem convergencia (fluxos "soltos")
- Misturar XOR e OR no mesmo ponto de decisao

---

## 3. Fluxo e Layout

### Direcao

- **Principal**: esquerda → direita
- **Alternativa** (processos longos): cima → baixo
- **NUNCA**: direita → esquerda ou baixo → cima no fluxo principal

### Cruzamentos

- **Evitar** cruzamento de linhas de fluxo
- Se inevitavel, usar "pontes" visuais (arco na linha que cruza)
- Reordenar lanes para minimizar cruzamentos

### Alinhamento

- Atividades na mesma lane devem estar alinhadas horizontalmente
- Gateways devem estar alinhados com as atividades que conectam
- Eventos de inicio a esquerda, eventos de fim a direita

---

## 4. Subprocessos

### Quando usar subprocesso

- 3+ atividades relacionadas que formam uma unidade logica
- Atividades que se repetem em multiplos pontos do fluxo
- Detalhamento que pertence a um nivel inferior (ex: N3 dentro de N2)
- Tratamento de erro complexo (boundary error event)

### Regras

- Subprocesso colapsado mostra marcador [+]
- Subprocesso expandido mostra conteudo com proprio start/end
- Nome do subprocesso segue mesma regra de atividades (verbo + complemento)
- Maximo 2 niveis de aninhamento (subprocesso dentro de subprocesso)

---

## 5. Pools e Lanes

### Pools

- Um pool = um processo de negocio completo OU um participante externo
- Message flow (tracejado) APENAS entre pools
- Sequence flow (solido) APENAS dentro de um pool

### Lanes

- Uma lane = um ator, area funcional ou papel
- Toda atividade deve estar posicionada na lane do executor
- Handoffs entre lanes devem ser explicitos (fluxo cruza fronteira da lane)
- Evitar mais de 5-6 lanes (agrupar atores similares)

### Visao logica (N1-N2)

- Pool unico sem lanes
- Ou pool com lanes representando subprocessos (nao areas)

### Visao fisica (N3-N5)

- Pool com lanes representando areas funcionais
- Milestone (divisao vertical) para fases do processo

---

## 6. Eventos

### Start Events

- **Exatamente 1** start event por processo (exceto event subprocess)
- Start event sempre na lane que inicia o processo
- Nome do trigger como tooltip (ex: "Cliente envia pedido")

### End Events

- **Pelo menos 1** end event por processo
- Cada caminho do fluxo deve terminar em um end event
- Usar end-error para caminhos de excecao
- Usar end-terminate para encerrar todos os caminhos paralelos

### Intermediate Events

- Usar timer para esperas: "Aguardar 3 dias uteis"
- Usar message-catch para integracao: "Receber resposta do sistema X"
- Boundary events (attached) para tratamento de erro/timeout em atividades

---

## 7. Checklist de Validacao

Use esta lista para validar qualquer diagrama BPMN:

### Estrutura

- [ ] Exatamente 1 start event?
- [ ] Pelo menos 1 end event?
- [ ] Todos os caminhos terminam em end event?
- [ ] Nenhum node "solto" (sem conexao)?

### Gateways

- [ ] Todo gateway de divergencia tem par de convergencia?
- [ ] Labels presentes em todos os gateways ou fluxos de saida?
- [ ] XOR gateways tem caminho default?
- [ ] Nenhum gateway com entrada E saida unicas (desnecessario)?

### Nomenclatura

- [ ] Atividades com verbo + complemento?
- [ ] Sem nomes genericos ou abreviados?
- [ ] Labels de gateway como perguntas claras?

### Layout

- [ ] Fluxo predominante esquerda → direita?
- [ ] Sem cruzamentos desnecessarios?
- [ ] Atividades alinhadas em suas lanes?

### Pools/Lanes

- [ ] Sequence flow dentro do pool?
- [ ] Message flow entre pools?
- [ ] Atividades na lane correta?

### Completude

- [ ] Regras de negocio documentadas para cada gateway?
- [ ] Data objects associados onde necessario?
- [ ] Annotations explicando pontos complexos?

### Validacao Estrutural XML (.bpmn)

- [ ] Todos os 5 namespaces declarados no `<bpmn:definitions>`? (bpmn, bpmndi, dc, di, xsi)
- [ ] Todo `<bpmn:sequenceFlow>` tem `sourceRef` e `targetRef` apontando para IDs existentes?
- [ ] Todo flow node lista seus flows em `<bpmn:incoming>` e `<bpmn:outgoing>`? (exceto start=somente outgoing, end=somente incoming)
- [ ] Todo node ID aparece em exatamente um `<bpmn:flowNodeRef>` dentro de uma lane?
- [ ] Todo elemento do modelo tem um `<bpmndi:BPMNShape>` correspondente no BPMNDiagram?
- [ ] Todo connection tem um `<bpmndi:BPMNEdge>` correspondente no BPMNDiagram?
- [ ] `bpmnElement` em cada shape/edge aponta para o ID correto?
- [ ] Todos os `id` sao unicos em todo o documento?
- [ ] Todo `<bpmn:participant>` tem `processRef` apontando para um `<bpmn:process>` existente?
- [ ] XOR gateways com `default` referenciam um sequence flow ID valido?
- [ ] Boundary events tem `attachedToRef` valido e NAO tem `<bpmn:incoming>`?
