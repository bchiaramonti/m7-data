# Schema · `ssot/processo-n2.md`

SSOT para `build/processo-n2.html` (BPMN end-to-end Cliente↔M7 + cards de subprocessos).

## Sumário

1. [Frontmatter YAML](#1-frontmatter-yaml)
2. [Seções markdown](#2-seções-markdown)
3. [Exemplo mínimo](#3-exemplo-mínimo)
4. [Regras de validação](#4-regras-de-validação)
5. [Bloqueadores conhecidos](#5-bloqueadores-conhecidos)

---

## 1. Frontmatter YAML

```yaml
---
schema_version: 1                    # obrigatorio, sempre 1 no MVP

n1_artifacts:                        # obrigatorio
  briefing:              <path>      # OBRIGATÓRIO. Path para BRIEFING.md da N1
  cadeia_de_valor:       <path>      # opcional
  missao_do_processo:    <path>      # opcional
  mapa_interdependencia: <path>      # opcional
  politica:              <path>      # opcional mas RECOMENDADO

processo:                            # obrigatorio
  code:         <string>             # regex ^P\d+(\.\d+)?$ ou ^G\d+$ etc. Ex: P5, G2, P5.1
  name:         <string>             # ex: "Crédito"
  slug:         <string>             # kebab-case. Ex: p5-credito
  camada:       <gerencial|primario|apoio>  # vinda do BRIEFING N1
  owner:        <string>             # cargo/comitê, NUNCA nome próprio
  receita_meta: <string>             # opcional. Ex: "R$ 22,6 MM"
  descricao:    <string>             # 1-2 frases. Vai virar lede do header

wbs:    <string>                     # ex: "WBS 3.2"
janela: <string>                     # ex: "12/05 → 30/05"
status: <string>                     # ex: "Em produção"

subprocessos:                        # 3-8 entradas. Ordem == fluxo BPMN.
  - id:       <string>               # kebab-case. Ex: p5-1
    code:     <string>               # ex: P5.1 (deve casar com regex code do processo)
    name:     <string>               # ex: "Originação"
    owner:    <string>               # cargo/comitê
    cadence:  <string>               # ex: "D+0 contínuo", "SLA 3-5d"
    sp_meta:  <string>               # timbre curto (3-6 palavras)
    sp_tech:  <string>               # CSV de sistemas-chave

interfaces:                          # exatamente 1 por subprocesso
  - code:    <string>                # deve casar com subprocessos[].code
    message: <string>                # "Cliente → M7: X / M7 → Cliente: Y"
---
```

---

## 2. Seções markdown

Após `---`:

```markdown
# Processo N2 · {processo.name}

## Lede
<paragrafo de 1-3 frases que entra no <p class="lede"> do header>

## Notas de iteracao
- decisao 1
- bloqueador-aceito (com rationale)
```

A seção `## Lede` é **obrigatória**; o validador checa que existe e tem ≥ 30 caracteres.

---

## 3. Exemplo mínimo

```yaml
---
schema_version: 1

n1_artifacts:
  briefing: "../mapeamento-m7/BRIEFING.md"

processo:
  code: "P5"
  name: "Crédito"
  slug: "p5-credito"
  camada: "primario"
  owner: "Diretor Comercial · Mesa Crédito"
  receita_meta: "R$ 22,6 MM"
  descricao: "FIDC Crédito, FIDC Serviços e Consignado privado/público."

wbs: "WBS 3.2"
janela: "12/05 → 30/05"
status: "Em produção"

subprocessos:
  - id: p5-1
    code: "P5.1"
    name: "Originação & Pré-análise"
    owner: "Comercial Crédito"
    cadence: "D+0 contínuo"
    sp_meta: "Multi-canal · pré-análise"
    sp_tech: "Bitrix24 · Boa Vista · Quod"
  # ... mais 4 subprocessos

interfaces:
  - code: "P5.1"
    message: "Cliente → M7: solicitação + dados / M7 → Cliente: pré-aprovação ou recusa"
  # ... mais 4 interfaces
---

# Processo N2 · Crédito

## Lede

O P5 Crédito é a vertical primária do grupo, com originação multi-canal e gestão de risco end-to-end. Decomposto em 5 subprocessos.

## Notas de iteracao
- Owner inicialmente foi "Filipe Costa" (nome próprio) - corrigido para cargo no Bloco 1 da entrevista
```

---

## 4. Regras de validação

Aplicadas por `check_ssot.py --target processo-n2`.

### Determinísticas (bloqueadores)
- **SCHEMA-MISSING** — campo raiz obrigatório ausente
- **N1-BRIEFING-AUSENTE** — `n1_artifacts.briefing` aponta para arquivo inexistente
- **N1-CODIGO-NAO-ENCONTRADO** — `processo.code` não consta em `processos[]` do BRIEFING N1 (parse o YAML do BRIEFING e procura `processos[*].codigo == processo.code`)
- **PROCESSO-CODE-INVALIDO** — não casa regex `^[PGA]\d+(\.\d+)?$` (ou variação válida do esquema N1)
- **SLUG-INVALIDO** — não é kebab-case
- **CAMADA-INVALIDA** — fora de {gerencial, primario, apoio}
- **OWNER-PESSOA** — owner não contém marcador de cargo (Diretor, Head, Comitê, Gerente, etc.)
- **SUBPROCESSOS-FAIXA** — count fora de [3..8]
- **SUBPROCESSO-INCOMPLETO** — falta campo obrigatório (id, code, name, owner, cadence, sp_meta, sp_tech)
- **SUBPROCESSO-CODE-DUP** — codes repetidos em subprocessos[]
- **INTERFACES-COUNT** — `interfaces.length != subprocessos.length`
- **INTERFACES-CODE-ORFA** — `interfaces[].code` não corresponde a nenhum `subprocessos[].code`
- **LEDE-AUSENTE** — falta seção `## Lede` ou conteúdo < 30 caracteres

### Determinísticas (avisos)
- **SP-META-LONGO** — sp_meta > 60 caracteres (não cabe no card)
- **SP-TECH-LONGO** — sp_tech > 80 caracteres
- **POLITICA-AUSENTE** — `n1_artifacts.politica` vazio (recomendado para rastreabilidade governança)

### Semânticas (delegadas ao `n2-interview-critic`)
Não são checadas aqui:
- Coerência entre `processo.descricao` e os 5 subprocessos
- Sequência BPMN faz sentido (P5.1 antecede P5.2 logicamente)
- Owner está consistente com a Política N1 (se anexada)

---

## 5. Bloqueadores conhecidos

| Rule ID | Quando aparece | Como corrigir |
|---|---|---|
| N1-CODIGO-NAO-ENCONTRADO | Você quer mapear P5 mas o BRIEFING N1 não tem P5 nos processos | Volte para `mapeamento-n1` e adicione P5 antes; ou mude `processo.code` para algo válido |
| OWNER-PESSOA | Escreveu "Filipe Costa" ao invés de cargo | Substitua por "Diretor Comercial · Mesa Crédito" |
| SUBPROCESSOS-FAIXA | Tentou mapear processo com 12 subprocessos | Reagrupe — 12 é granularidade N3, não N2 |
| INTERFACES-COUNT | 5 subprocessos mas 3 interfaces | Adicione 2 interfaces (uma por subproc.) |
