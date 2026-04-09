# Roteiro de Entrevista — Mapeamento de Interfaces de Processo

Guia detalhado de perguntas para cada fase do mapeamento DEIP. Use como referencia durante a entrevista com o usuario.

---

## Principios de Facilitacao

1. **Uma pergunta por vez** — nunca fazer multiplas perguntas simultaneamente
2. **Escutar antes de sugerir** — deixar o usuario descrever, depois complementar
3. **Sugerir com base em padroes** — oferecer opcoes quando o contexto permite
4. **Validar periodicamente** — ao final de cada fase, apresentar resumo e confirmar
5. **Nao julgar** — toda resposta e valida; desconexoes serao avaliadas na Fase 7
6. **Registrar tudo** — mesmo itens que parecem obvios podem revelar desconexoes

---

## Fase 1 — Identificacao do Processo

### Perguntas Principais

| # | Pergunta | Tipo | Formato AskUserQuestion |
|---|----------|------|------------------------|
| 1.1 | "Qual o nome do processo que vamos mapear?" | Aberta | Texto livre |
| 1.2 | "Este processo tem um codigo na cadeia de valor? (ex: G2.3, P1.1)" | Aberta | Texto livre |
| 1.3 | "Quem e o responsavel (dono do processo)?" | Aberta | Texto livre |
| 1.4 | "Em que nivel BPM estamos mapeando?" | Opcoes | N1 (Processo de Negocio) / N2 (Subprocesso) / N3 (Funcao) |
| 1.5 | "Em uma frase, qual o proposito deste processo?" | Aberta | Texto livre |

### Perguntas-Sonda (Probing)

- "Este processo faz parte de qual macroprocesso (N1)?"
- "Quantas areas participam deste processo?"
- "Existe documentacao atual sobre este processo? (POP, manual, fluxo)"
- "Quando foi a ultima vez que este processo foi revisado?"

### Red Flags

- Processo sem dono definido → registrar como desconexao potencial
- Nome generico (ex: "Processo de gestao") → pedir especificacao
- Nivel incorreto (usuario descreve tarefas N5 quando deveria ser N2) → orientar

---

## Fase 2 — Saidas e Clientes (Outputs)

### Pergunta de Abertura

> "Vamos comecar pelo que o processo entrega. Quando este processo termina, o que ele produz? Pode ser um documento, servico, informacao, decisao, produto fisico..."

### Perguntas de Detalhamento (por saida)

| # | Pergunta | Tipo |
|---|----------|------|
| 2.1 | "Qual o nome desta saida?" | Aberta |
| 2.2 | "Pode descrever brevemente o que e?" | Aberta |
| 2.3 | "Quem recebe esta saida? (cliente interno, externo, regulador)" | Opcoes + Aberta |
| 2.4 | "O cliente e Interno, Externo ou Regulador?" | Opcoes |

### Perguntas-Sonda

- "Alem de [saida X], o processo gera mais algum subproduto?"
- "Ha alguma saida que vai para reguladores ou orgaos de controle?"
- "Existe algum relatorio, notificacao ou comunicacao que o processo gera?"
- "Ha alguma saida intermediaria que alimenta outro processo?"

### Padroes Comuns de Saidas por Tipo de Processo

| Tipo de Processo | Saidas Tipicas |
|-----------------|----------------|
| Comercial | Proposta, contrato, cadastro, relatorio de vendas |
| Financeiro | Pagamento, conciliacao, relatorio financeiro, nota fiscal |
| RH | Admissao, folha de pagamento, avaliacao, treinamento |
| Compliance | Parecer, relatorio de conformidade, comunicacao ao regulador |
| TI | Sistema entregue, ticket resolvido, backup, relatorio SLA |
| Operacional | Produto, entrega, laudo, ordem de servico |

### Fechamento da Fase

> "Ate agora mapeamos [N] saidas: [lista]. O processo entrega mais alguma coisa que nao mencionamos?"

---

## Fase 3 — Entradas e Fornecedores (Inputs)

### Pergunta de Abertura

> "Agora que sabemos o que o processo entrega, vamos descobrir o que ele precisa para funcionar. Para produzir [Output 1], que insumos o processo precisa receber?"

### Perguntas de Detalhamento (por entrada)

| # | Pergunta | Tipo |
|---|----------|------|
| 3.1 | "Qual o nome deste insumo?" | Aberta |
| 3.2 | "Pode descrever brevemente?" | Aberta |
| 3.3 | "Quem fornece este insumo?" | Aberta |
| 3.4 | "O fornecedor e Interno, Externo ou Sistema?" | Opcoes |

### Perguntas-Sonda

- "Para produzir [Output Y], precisa de mais algum insumo alem dos ja listados?"
- "Ha alguma informacao que vem de sistemas (automatica)?"
- "Existe algum gatilho que inicia este processo? (pedido, evento, calendario)"
- "Ha insumos que vem de processos anteriores na cadeia de valor?"

### Tecnica de Vinculacao Input-Output

Para cada output mapeado, perguntar explicitamente quais inputs sao necessarios para produzi-lo. Isso garante que nenhum input fique orfao e que a logica de transformacao fique clara.

```
Output O1 (Cliente cadastrado)
  ← Input I1 (Lead qualificado) — de Marketing
  ← Input I2 (Documentos pessoais) — de Cliente

Output O2 (Ficha cadastral)
  ← Input I1 (Lead qualificado) — de Marketing
  ← Input I3 (Dados complementares) — de Sistema CRM
```

### Fechamento da Fase

> "Mapeamos [N] entradas de [M] fornecedores: [lista]. Falta algum insumo que o processo precisa para funcionar?"

---

## Fase 4 — Suporte

### Pergunta de Abertura

> "Agora vamos mapear os recursos necessarios para o processo funcionar. Quais equipes, sistemas, equipamentos ou infraestrutura sao necessarios?"

### Perguntas por Categoria

| Categoria | Pergunta |
|-----------|----------|
| Pessoas | "Quantas pessoas trabalham neste processo? Quais perfis?" |
| Sistemas | "Quais sistemas/ferramentas sao usados? (CRM, ERP, Excel, email)" |
| Equipamentos | "Ha equipamentos especificos necessarios? (impressora, scanner, hardware)" |
| Infraestrutura | "Ha necessidade de salas, redes, ambientes especificos?" |

### Perguntas-Sonda

- "Ha algum sistema critico sem o qual o processo para?"
- "A equipe e dedicada ou compartilhada com outros processos?"
- "Ha dependencia de fornecedores externos de TI/servicos?"

### Fechamento da Fase

> "Mapeamos [N] recursos de suporte: [lista]. Falta algum recurso necessario?"

---

## Fase 5 — Regulacao

### Pergunta de Abertura

> "Quais leis, normas, politicas internas ou procedimentos regulam este processo?"

### Perguntas por Tipo

| Tipo | Pergunta |
|------|----------|
| Leis | "Ha legislacao federal, estadual ou municipal aplicavel?" |
| Normas | "Ha normas regulatorias do setor? (CVM, BACEN, ANBIMA, SUSEP)" |
| Politicas | "Ha politicas internas da empresa que governam este processo?" |
| POPs | "Existe POP (Procedimento Operacional Padrao) documentado?" |
| Instrucoes | "Ha instrucoes de trabalho formalizadas?" |

### Perguntas-Sonda

- "Ha regulacoes que deveriam existir mas nao existem?"
- "Alguma regulacao esta desatualizada?"
- "Ha conflito entre regulacoes diferentes?"
- "Existe auditoria ou controle sobre o cumprimento dessas regulacoes?"

### Se Nenhuma Regulacao

Se o usuario nao identifica nenhuma regulacao, registrar como "Sem regulacao identificada" com status neutral. Isso nao e necessariamente uma desconexao — nem todo processo e regulado formalmente.

### Fechamento da Fase

> "Mapeamos [N] regulacoes: [lista]. Ha mais alguma norma ou politica que governa este processo?"

---

## Fase 6 — Macrofluxo (N3)

### Pergunta de Abertura

> "Dado que o processo recebe [resumo de inputs] e deve entregar [resumo de outputs], quais sao as etapas principais para essa transformacao? (3 a 8 passos)"

### Regras de Validacao

- Cada etapa deve usar formato **verbo + complemento** (ex: "Analisar documentacao", nao "Documentacao")
- Minimo 3, maximo 8 etapas
- Nivel de detalhe N3 (funcao/macro) — nao descer para tarefas N4-N5
- Sequencia logica: inicio → transformacao → entrega

### Perguntas-Sonda

- "Entre [etapa X] e [etapa Y], ha alguma verificacao ou aprovacao?"
- "Ha alguma etapa que pode ser executada em paralelo?"
- "Qual etapa e a mais critica / onde mais ocorrem problemas?"
- "Ha alguma etapa que envolve espera ou handoff entre areas?"

### Verbos Recomendados para Etapas

| Categoria | Verbos |
|-----------|--------|
| Recepcao | Receber, Coletar, Captar, Registrar |
| Analise | Analisar, Verificar, Avaliar, Classificar |
| Decisao | Aprovar, Rejeitar, Selecionar, Priorizar |
| Execucao | Elaborar, Processar, Calcular, Executar |
| Comunicacao | Notificar, Comunicar, Enviar, Publicar |
| Entrega | Entregar, Distribuir, Disponibilizar, Formalizar |

### Fechamento da Fase

> "O macrofluxo ficou assim: [lista numerada]. A sequencia esta correta? Quer ajustar alguma etapa?"

---

## Fase 7 — Avaliacao de Interfaces

### Introducao

> "Agora vamos avaliar cada interface individualmente. Para cada uma, vou perguntar se esta funcionando adequadamente ou se ha oportunidade de melhoria."

### Template de Pergunta (por interface)

Para outputs:
> "Interface [On]: O processo entrega **[saida]** para **[cliente]**. Esta interface funciona adequadamente?"

Para inputs:
> "Interface [In]: **[fornecedor]** entrega **[entrada]** para o processo. Esta interface funciona adequadamente?"

Para suporte:
> "Interface [Sn]: O processo depende de **[recurso]** ([tipo]). Este recurso esta disponivel e adequado?"

Para regulacao:
> "Interface [Rn]: O processo e regulado por **[documento]** ([tipo]). O processo esta em conformidade?"

### Opcoes AskUserQuestion

```
Opcoes:
1. Conforme — funciona sem problemas
2. Melhoria — ha oportunidade de melhoria
3. Nao avaliado — sem informacao suficiente
```

### Se Melhoria — Follow-up

Pergunta 1: "Qual e a desconexao nesta interface?"
```
Opcoes sugeridas (adaptar ao contexto):
1. Handoff manual sujeito a erro
2. Falta de POP/procedimento documentado
3. Sistemas nao integrados
4. SLA nao definido ou nao cumprido
5. Retrabalho frequente
6. Formato de entrega inadequado
7. Informacao incompleta ou atrasada
(+ Outro — texto livre)
```

Pergunta 2: "Qual o impacto desta desconexao?"
```
Opcoes:
1. Alto — paralisa processo, gera risco, afeta cliente final
2. Medio — gera retrabalho ou atraso significativo
3. Baixo — inconveniencia, impacto operacional menor
```

Pergunta 3 (opcional): "Ha alguma acao corretiva que voce sugere?"

### Ordem de Avaliacao

Seguir a mesma ordem do mapeamento: Outputs → Inputs → Suporte → Regulacao.

---

## Tecnicas Gerais de Entrevista

### Quando o Usuario Nao Sabe Responder

- Registrar como "Nao avaliado" (status: neutral)
- Nao forcar: "Tudo bem, podemos voltar a este item depois"
- Sugerir fonte: "Quem poderia nos ajudar com essa informacao?"

### Quando o Usuario Fala Demais

- Agradecer: "Otimas informacoes!"
- Redirecionar: "Para o nivel do DEIP, vamos simplificar em [resumo]. O detalhe vai no BPMN depois."
- Registrar detalhes como notas para fases futuras

### Quando o Usuario Contradiz Respostas Anteriores

- Nao confrontar diretamente
- Apresentar ambas versoes: "Antes voce mencionou [X], agora [Y]. Qual das duas melhor representa a realidade?"
- Registrar a versao confirmada
