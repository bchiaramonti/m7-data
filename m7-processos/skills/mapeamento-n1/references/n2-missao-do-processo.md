# N2 · Missão do Processo (SIPOC) — regras detalhadas

Documento de apoio à [SKILL.md](../SKILL.md). Cobre o nível N2: SIPOC simplificado por processo (Inputs → Missão → Outputs), com sidebar de navegação e Owner.

## Sumário

1. [Objetivo e quando usar](#1-objetivo-e-quando-usar)
2. [Estrutura do template](#2-estrutura-do-template)
3. [Roteiro de entrevista por processo](#3-roteiro-de-entrevista-por-processo)
4. [Regras de preenchimento](#4-regras-de-preenchimento)
5. [Checklist de validação](#5-checklist-de-validação)
6. [Anti-padrões](#6-anti-padrões)

---

## 1. Objetivo e quando usar

Enquanto o N1 mostra **o todo** (3 camadas, todos os processos), o N2 detalha **um processo por vez** no formato SIPOC simplificado:

```
[Inputs]  →  [Missão]  →  [Outputs]
                ↑
            Owner do processo
```

Use `template-missao-do-processo.html` quando o usuário pedir:
- "missão dos processos", "SIPOC", "detalhar processo X"
- "o que cada processo faz", "entregas de cada processo"
- "N2 / segundo nível da cadeia de valor"

**Pré-requisito**: a N1 já existe (codes G1..Gn, P1..Pn, A1..An estão definidos). A sidebar do N2 reflete exatamente os processos da N1.

---

## 2. Estrutura do template

### Sidebar esquerda (180px)
- Lista todos os processos da N1 agrupados em **Gerenciais / Primários / Apoio**
- Cada item tem código (G1, P3, A1…) e nome
- Clique navega entre processos via JS local
- Hash deep-link funciona (`#G1`, `#P3` na URL abre o processo correspondente)

### Painel direito (área restante)
Para o processo selecionado, mostra:

- **Headline**: código + nome (ex.: `G1 Planejamento Estratégico`), tag de camada, Owner inline minimalista (`OWNER · CEO · Comitê Estratégico`)
- **Três blocos lado a lado**, ocupando toda a altura disponível:
  - **Inputs** (esquerda, fundo branco): chips com gatilhos/insumos
  - **Missão** (centro, fundo verde-caqui escuro com barra lime): texto **Verbo + Objeto + Finalidade**, com `<span class="verb">` no verbo (renderiza em lime) e `<em>` na finalidade após "para"
  - **Outputs** (direita, fundo branco): chips com entregas/resultados

### Centralização vertical
Os 3 blocos centralizam o **conteúdo** verticalmente (não os labels — labels ficam no topo do bloco). Isso é intencional: respira melhor quando há poucos chips.

---

## 3. Roteiro de entrevista por processo

Faça um bloco curto **para cada processo** após a N1 estar fechada. Caminhe processo a processo, do G1 ao An.

### Bloco por processo (4 perguntas)

1. **Missão** — Em uma frase, qual é:
   - O **verbo** principal (1-2 palavras: Definir, Construir, Operar, Garantir…)?
   - O **objeto** (o que o processo produz/gere)?
   - A **finalidade** (para quê, qual o resultado para o cliente/negócio)?

2. **Inputs** — 3 a 6 itens: o que precisa existir/chegar para o processo rodar. Cada um vira um chip curto (2-4 palavras).

3. **Outputs** — 3 a 6 itens: o que o processo entrega para fora dele (artefatos, decisões, sinais). Cada um vira um chip curto.

4. **Owner** — Cargo responsável + (opcional) fórum/comitê de governança. Formato: `Cargo · Fórum`. Exemplos:
   - `CEO · Comitê Estratégico`
   - `Head de Investimentos`
   - `CFO · Comitê de Riscos`

**Não** pergunte tudo de uma vez. Não "despeje" 4 perguntas em série — faça uma, espere resposta, próxima.

---

## 4. Regras de preenchimento

### Verbo
- **1-2 palavras**, sem objeto direto colado.
- Bons: `Definir`, `Construir e gerir`, `Operar e evoluir`, `Garantir`, `Entregar`.
- Ruins: `Fazer`, `Realizar`, `Gerenciar` — genéricos demais. Force especificidade.
- Renderiza em lime (cor accent) e dá o tom do processo.

### Objeto
- Substantivo claro, sem qualificadores excessivos.
- Bons: `o direcionamento estratégico de longo prazo`, `carteiras de investimento personalizadas`.
- Ruins: `as coisas`, `o que precisa ser feito`.

### Finalidade
- Vem depois de "**para**". Explicita o **porquê**, não o **como**.
- Bons:
  - `para alinhar investimentos, estrutura e cultura às oportunidades`
  - `para fazer o patrimônio do cliente crescer`
- Ruins:
  - `para fazer reuniões mensais` (isso é como, não porquê)
  - `para reduzir custos` (vago demais sem objeto)
- Renderiza em opacidade 85% (texto secundário).

### Chips (Inputs / Outputs)
- **2-4 palavras** cada chip.
- **Maiúscula só na primeira letra** (sentence case). Ex.: `Plano estratégico aprovado`, `Comitê de investimentos`.
- **Nada de SLAs, métricas ou números** aqui — esses entram em N3/N4 (fora do escopo desta skill).
- **Inputs ≠ Outputs**: nenhum item repetido entre os dois lados. Se o usuário propor o mesmo item em ambos, pergunte: *"isso entra ou sai do processo?"*

### Owner
- **Sempre cargo** (ou cargo + comitê), nunca nome próprio.
- Formato: `OWNER · {Cargo} · {Fórum opcional}`.
- Renderização: minúsculas para o label `OWNER`, e cargo/fórum em capitalize. Já é tratado pelo CSS.

### Cobertura
- **TODOS** os processos da N1 devem aparecer na sidebar.
- Se algum ainda não foi mapeado em entrevista, deixe a sidebar listando-o e o painel com placeholder (`{{VERBO_X}} {{OBJETO_X}}`).
- Não esconda processos não preenchidos — isso quebra a consistência com a N1.

---

## 5. Checklist de validação

Antes de entregar, confirmar:

- [ ] **Sidebar consistente com N1** — exatamente os mesmos códigos e nomes da cadeia de valor.
- [ ] **Verbo + Objeto + Finalidade** em cada missão preenchida — com `<span class="verb">` no verbo e `<em>` na finalidade após "para".
- [ ] **Inputs e Outputs**: 3-6 chips cada, nenhum repetido entre os dois.
- [ ] **Owners são cargos/comitês** — nunca nomes próprios.
- [ ] **Hash deep-link funciona** — abrir `arquivo.html#G1` mostra o processo G1.
- [ ] **Tabs do header navegam** — N1 e N3 (se gerados) acessíveis.
- [ ] **Placeholders restantes** — só admite `{{VERBO_X}} {{OBJETO_X}}` etc. em processos ainda não mapeados (combinar com o usuário). Os campos de header (`{{NOME_DA_EMPRESA}}`, etc.) **devem** estar preenchidos.
- [ ] **CSS irmãos** — `m7-tokens.css`, `m7-header-dark.css`, `assets/`, `fonts/` no mesmo diretório do HTML.
- [ ] **Centralização vertical** — labels Inputs/Missão/Outputs no topo dos blocos, conteúdo centralizado verticalmente.

---

## 6. Anti-padrões

- ❌ **Listar atividades ou passos no lugar da missão**. SIPOC é "o quê", não "como".
  - Errado: `Realizar reuniões mensais com diretoria, revisar KPIs e ajustar metas`
  - Certo (verbo+objeto+finalidade): `Acompanhar a execução estratégica para corrigir desvios e proteger metas anuais`

- ❌ **Misturar input com output**. Se "plano estratégico" aparece nos dois lados, está errado em algum.
  - Pergunte: *"esse item entra no processo (alguém me dá) ou sai (eu produzo e entrego)?"*

- ❌ **Verbo genérico** (`Fazer`, `Realizar`, `Gerenciar`). Force especificidade — ajude com sinônimos: `Construir`, `Operar`, `Validar`, `Definir`, `Garantir`, `Entregar`, `Coordenar`, `Monitorar`.

- ❌ **Owner como nome próprio**. Sempre cargo (`Head de X`, `CFO`, `Comitê Y`). Pessoa muda; cargo permanece.

- ❌ **Tooltips, ícones decorativos, números gigantes**. Mantém a estética do N1: minimalista, tipográfica, sem "decorações de PowerPoint".

- ❌ **Esconder processos não mapeados da sidebar**. Quebra consistência. Deixe placeholder visível.

- ❌ **Misturar BUs e camadas em N2**. O N2 é por processo, um por vez. Não tente comparar 2 processos no mesmo painel.
