# Fase B · 4 MDs canônicos como SSOT

Documento de apoio à [SKILL.md](../SKILL.md) · Fase B.

## Sumário

1. [Por que 4 MDs separados (vs 1 BRIEFING)](#1-por-que-4-mds-separados-vs-1-briefing)
2. [Ordem de preenchimento](#2-ordem-de-preenchimento)
3. [Validação por MD](#3-validação-por-md)
4. [Gate para Fase C](#4-gate-para-fase-c)
5. [Schemas detalhados](#5-schemas-detalhados)

---

## 1. Por que 4 MDs separados (vs 1 BRIEFING)

A N1 usa **1 BRIEFING.md monolítico** que mistura dados de N1 + N2 + N3 + N4. Custo: validador de 763 linhas, iteração que afeta tudo a cada correção.

A N2 quebra em **4 MDs canônicos** (`ssot/processo-n2.md`, `ssot/sipocs.md`, `ssot/jornada-cx.md`, `ssot/data-lake.md`), cada um:

- **Auto-suficiente para regenerar seu artefato visual** (1:1 com a estrutura JS do gabarito)
- **Validável independentemente** (`check_ssot.py --target {nome}`)
- **Iterável sem afetar os outros** (corrigir Data Lake nunca toca SIPOC)

Custo: 4 schemas em vez de 1, e a coerência entre MDs (ex.: subprocessos[].code em `processo-n2.md` deve casar com subprocessos[].code em `sipocs.md`) vira responsabilidade do validador transversal `check_ssot.py --all`.

---

## 2. Ordem de preenchimento

A ordem é **rígida** porque um MD usa código/nomes do anterior:

```
1. processo-n2.md   ← define subprocessos[] canônicos (code, name, owner, cadence)
2. sipocs.md        ← consome subprocessos[].code; detalha purpose/I/O/etapas/reg/sup
3. jornada-cx.md    ← consome processos[] (mesma ordem); preenche 4 rows
4. data-lake.md     ← consome processos[] (mesma ordem); preenche 2 rows + marts/consumers globais
```

**Não pule para o passo 4 antes do passo 1.** Se o código P5.1 muda em `processo-n2.md`, ele precisa propagar para os outros 3 — mais fácil regenerar do que sincronizar.

---

## 3. Validação por MD

```bash
python3 scripts/check_ssot.py --target processo-n2 ssot/processo-n2.md
python3 scripts/check_ssot.py --target sipocs ssot/sipocs.md
python3 scripts/check_ssot.py --target jornada-cx ssot/jornada-cx.md
python3 scripts/check_ssot.py --target data-lake ssot/data-lake.md

# Atalho para os 4 + checks transversais (códigos casam entre MDs):
python3 scripts/check_ssot.py --all ssot/
```

**Exit code 1** se há bloqueadores. Output JSON `{bloqueadores: [...], avisos: [...]}` por padrão; `--human` para output legível.

Regras específicas por MD: ver [`ssot-processo-n2.md`](ssot-processo-n2.md), [`ssot-sipocs.md`](ssot-sipocs.md), [`ssot-jornada-cx.md`](ssot-jornada-cx.md), [`ssot-data-lake.md`](ssot-data-lake.md).

### Regras transversais (`--all`)

- **N1-BRIEFING-AUSENTE** — `n1_artifacts.briefing` aponta para arquivo inexistente
- **N1-CODIGO-NAO-ENCONTRADO** — `processo.code` (ex.: P5) não consta em `processos[]` do BRIEFING N1
- **SUBPROC-MISMATCH** — `processo-n2.md.subprocessos[].code` != `sipocs.md.subprocessos[].code` (set diff)
- **JORNADA-PROCESSOS-MISMATCH** — `jornada-cx.md.processos[].code` != `processo-n2.md.subprocessos[].code`
- **DATALAKE-PROCESSOS-MISMATCH** — idem para `data-lake.md`
- **DATALAKE-MARTS-CONSUMERS-ORFAOS** — algum mart não tem consumer correspondente OU vice-versa

---

## 4. Gate para Fase C

A Fase C só inicia se:
```bash
python3 scripts/check_ssot.py --all ssot/
echo $?   # deve ser 0
```

Bloqueadores no `--all` impedem o build. Se o usuário insiste em avançar com bloqueadores, **registre em `processo-n2.md` na seção `## Notas de iteracao`** com rationale:

```markdown
- [bloqueador-aceito] SUBPROC-MISMATCH em P5.3:
  sipocs.md usa código "P5.3" mas processo-n2.md tem "P5.3a"
  Aceito porque o subproc. está em refactoring; será unificado na próxima versao.
```

`check_ssot.py` ainda reporta o bloqueador, mas a presença no markdown documenta a decisão para auditoria.

---

## 5. Schemas detalhados

| MD | Reference | Validação resumida |
|---|---|---|
| `processo-n2.md` | [`ssot-processo-n2.md`](ssot-processo-n2.md) | code ∈ regex, slug kebab, 3-8 subprocessos, owner ≠ nome próprio, interfaces.length == subprocessos.length |
| `sipocs.md` | [`ssot-sipocs.md`](ssot-sipocs.md) | purpose sem verbo proibido, inputs ≠ outputs, etapas 4-8, regulacao+suporte ≥ 2 |
| `jornada-cx.md` | [`ssot-jornada-cx.md`](ssot-jornada-cx.md) | 4 rows preenchidas, mot.intensity ∈ {1,2,3}, pain.tone ∈ {+,-,~} |
| `data-lake.md` | [`ssot-data-lake.md`](ssot-data-lake.md) | kind ∈ enum, marts.dim ≥ 3, marts.fact ≥ 3, consumers ≥ 4 |
