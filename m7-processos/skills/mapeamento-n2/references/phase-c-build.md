# Fase C · Build em camadas com gates

Documento de apoio à [SKILL.md](../SKILL.md) · Fase C.

## Sumário

1. [Princípio: cascata com gates explícitos](#1-princípio-cascata-com-gates-explícitos)
2. [Sequência das 4 camadas](#2-sequência-das-4-camadas)
3. [Iteração subprocesso-a-subprocesso no SIPOC](#3-iteração-subprocesso-a-subprocesso-no-sipoc)
4. [Bootstrap (CSS/fonts/assets)](#4-bootstrap-cssfontsassets)
5. [Validação por camada](#5-validação-por-camada)
6. [Idempotência e re-runs](#6-idempotência-e-re-runs)

---

## 1. Princípio: cascata com gates explícitos

**Cada artefato é insumo do próximo.** Por isso a Fase C tem 4 scripts entrypoint independentes (não 1 com flag), cada um declarando seu **gate** (arquivo esperado em `build/`):

| Script | Gate (entrada) | Output |
|---|---|---|
| `build_processo.py` | `n1_artifacts.briefing` existe + `processo.code` ∈ BRIEFING N1 | `build/processo-n2.html` + bootstrap |
| `build_sipoc.py` | `build/processo-n2.html` existe | `build/sipoc-deip.html` + `build/sipoc-deip.js` + `build/dados-{slug}-{cod}.js` |
| `build_jornada.py` | `build/sipoc-deip.html` + `build/dados-{slug}-{cod}.js` existem | `build/jornada-cx.html` + parte `P5_JOURNEY` de `build/journey-{slug}-{cod}.js` |
| `build_datalake.py` | `build/journey-{slug}-{cod}.js` existe (parcial) | `build/data-lake.html` + parte `P5_DATALAKE` de `build/journey-{slug}-{cod}.js` |

Gate falhou → script aborta com mensagem clara: `"GATE: build/processo-n2.html não encontrado. Rode build_processo.py primeiro."`

---

## 2. Sequência das 4 camadas

### Camada 1 · Processo N2

```bash
python3 scripts/build_processo.py --ssot-dir ssot/ --out build/
```

Substitui ~30 placeholders em `templates/html/processo-n2.tmpl.html`:
- Header: `{{NOME_PROCESSO}}`, `{{CODE}}`, `{{LEDE}}`, `{{WBS}}`, `{{OWNER}}`, `{{JANELA}}`, `{{STATUS}}`
- Cards: por subprocesso `{{CODE_N}}`, `{{NAME_N}}`, `{{OWNER_N}}`, `{{CADENCE_N}}`, `{{SP_META_N}}`, `{{SP_TECH_N}}`
- Interfaces: por mensagem `{{MSG_N}}`

**Confirma com usuário antes da Camada 2.** Mostra path do HTML gerado e sugere `open build/processo-n2.html`.

### Camada 2 · SIPOC/DEIP (iterativa)

Ver [seção 3](#3-iteração-subprocesso-a-subprocesso-no-sipoc) abaixo.

### Camada 3 · Jornada CX

```bash
python3 scripts/build_jornada.py --ssot-dir ssot/ --out build/
```

Lê `ssot/jornada-cx.md` e **escreve a parte `window.P5_JOURNEY`** do arquivo `build/journey-{slug}-{cod}.js`. Se o arquivo já existe (das camadas anteriores), apenas reescreve o bloco `P5_JOURNEY` (regex de início e fim do bloco). Copia `jornada-cx.html` estático.

### Camada 4 · Data Lake

```bash
python3 scripts/build_datalake.py --ssot-dir ssot/ --out build/
```

Lê `ssot/data-lake.md` e **completa o `build/journey-{slug}-{cod}.js`** adicionando/reescrevendo `window.P5_DATALAKE`. Copia `data-lake.html` estático.

---

## 3. Iteração subprocesso-a-subprocesso no SIPOC

Esta é a **única camada com loop interno**. Por subprocesso (em ordem de `processo-n2.md`):

```bash
python3 scripts/build_sipoc.py --ssot-dir ssot/ --out build/ --subproc P5.1
# (revisa visualmente em build/sipoc-deip.html?sp=p5-1)
# (opcional: invoca n2-build-critic apenas neste DEIP)
# (confirma com usuário)

python3 scripts/build_sipoc.py --ssot-dir ssot/ --out build/ --subproc P5.2
# (...)
```

### O que acontece internamente

O `build/dados-{slug}-{cod}.js` tem estrutura:
```js
window.P5_DATA = {
  meta: { /* hidratado na 1a chamada, do processo-n2.md */ },
  subprocessos: [
    /* P5.1 hidratado quando build_sipoc.py --subproc P5.1 rodou */
    /* P5.2 placeholder ate rodar build_sipoc.py --subproc P5.2 */
  ],
  interfaces: [ /* hidratado da 1a chamada */ ],
};
```

A 1a chamada (`--subproc P5.1`) cria o esqueleto completo com `meta`, `interfaces`, e array `subprocessos` com objetos placeholder para todos. Chamadas subsequentes só **substituem** o objeto do subproc. específico.

### Atalho: rodar TODOS subprocessos de uma vez (não recomendado)

```bash
python3 scripts/build_sipoc.py --ssot-dir ssot/ --out build/ --all-subproc
```

**Use só se já validou um a um antes.** Para a primeira rodada, sempre vá um por vez — é o ponto-chave do princípio iterativo da skill.

---

## 4. Bootstrap (CSS/fonts/assets)

O `_build_common.py` expõe `bootstrap(out_dir)` que copia, **apenas se ausente**:
- `m7-tokens.css`, `m7-header-dark.css`, `mapeamento.css`, `mapeamento-views.css` → `out_dir/`
- `fonts/*.otf` (4 arquivos) → `out_dir/fonts/`
- `assets/*.png` (3 arquivos) → `out_dir/assets/`

Cada `build_*.py` chama `bootstrap()` antes de gerar seu HTML. Operação idempotente — não duplica se já existir.

---

## 5. Validação por camada

Após cada `build_*.py`, o script:

1. Verifica que **nenhum `{{` sobrou** no HTML gerado (regex search)
2. Reporta tamanho do output e arquivos criados
3. Sugere ao usuário: `"Abra build/{html} e confirme. Depois rode build_{próxima}.py"`

Opcional: invocar `n2-build-critic` (subagent) para validação semântica:
- Para Camada 1: "5 cards de subprocessos batem com 5 entradas em processo-n2.md?"
- Para Camada 2 (por subproc.): "DEIP do P5.1 tem 3 inputs, 3 outputs, 5 etapas? Está dentro do range?"
- Para Camadas 3 e 4: "4 rows × N colunas preenchidas? Marts/consumers visíveis no inventário?"

---

## 6. Idempotência e re-runs

Todos os 4 scripts são **idempotentes**: rodá-los duas vezes produz o mesmo output. Útil quando:

- Você editou `ssot/sipocs.md` para corrigir 1 inputs[] → rode só `build_sipoc.py --subproc {ID}` daquele
- Você editou `ssot/processo-n2.md` para mudar o WBS → rode `build_processo.py` (não precisa rebuildar SIPOC/Jornada/Data Lake; HTMLs deles não dependem do WBS)

**Exceção: mudou a lista de subprocessos em `processo-n2.md`** → rode TODOS os 4 builds, pois o conjunto canônico afeta todos os JS data files.
