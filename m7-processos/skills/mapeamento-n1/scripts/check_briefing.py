#!/usr/bin/env python3
"""mapeamento-n1 · validador deterministico do BRIEFING.md.

Aplica as regras de critique-rules.md que tem deteccao deterministica
(regex, cross-check, length, set diff). Regras semanticas (verbo fraco
contextualmente, missao como atividade, taxonomia) ficam para o
subagent process-critic.

Uso:
    python check_briefing.py <briefing.md>
    python check_briefing.py <briefing.md> --json    # output puro JSON

Exit codes:
    0 = ok (bloqueadores vazios)
    1 = bloqueadores presentes
    2 = erro de parsing (YAML invalido, secao ausente)
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "ERRO: PyYAML nao instalado. Rode: pip install -r requirements.txt\n"
    )
    sys.exit(2)


# ============================================================================
# Constantes das regras (espelham critique-rules.md)
# ============================================================================

VERBOS_PROIBIDOS = {"fazer", "realizar", "gerenciar", "executar", "cuidar", "tratar"}
VERBOS_FRACOS = {
    "administrar", "atuar", "lidar", "manter", "operacionalizar",
    "ocupar", "responder", "trabalhar", "assegurar", "prover",
    "atender", "ajudar", "auxiliar", "apoiar", "contribuir",
    "facilitar", "promover", "viabilizar", "suportar", "abranger",
    "envolver", "incluir", "compreender", "abordar", "encaminhar",
}
CAMADAS_VALIDAS = {"gerencial", "primario", "apoio"}
SUBCAMADAS_VALIDAS = {"front", "nucleo", "back"}
COLUNAS_VALIDAS = {"gerencial", "front", "nucleo-l", "nucleo-r", "back", "apoio"}
KINDS_VALIDOS = {"cliente", "info", "decisao"}
FORCAS_VALIDAS = {"strong", "mid", "soft"}
ARTEFATOS_VALIDOS = {"n1", "n2", "n3", "n4-pdf"}

# Politica · campos obrigatorios por sub-objeto (quando n4-pdf em artefatos)
POLITICA_METADATA_OBRIG = ["codigo_documento", "data_vigencia",
                            "proxima_revisao", "area_responsavel"]
POLITICA_APROV_PAPEIS = ["elaborador", "revisor", "aprovador"]
POLITICA_APROV_CAMPOS = ["nome", "cargo", "data"]
POLITICA_GOV_OBRIG = ["comite_revisor", "doc_sla", "area_compliance"]
POLITICA_VERSAO_CAMPOS = ["versao", "data", "alteracoes", "responsavel", "status"]

# Owner deve conter pelo menos um destes marcadores de cargo
MARCADORES_CARGO = re.compile(
    r"\b(CEO|CFO|COO|CTO|CMO|CIO|CHRO|CXO|"
    r"Head|Diretor|Diretora|Gerente|Coordenador|Coordenadora|"
    r"Comite|Comitê|Forum|Fórum|Conselho|"
    r"Lider|Líder|Owner|Especialista|Analista|Gestor|Gestora)\b",
    re.IGNORECASE,
)

# ============================================================================
# Estrutura de saida
# ============================================================================


class Issue:
    """Uma violacao detectada."""

    def __init__(self, rule_id: str, severity: str, where: str, message: str):
        self.rule_id = rule_id
        self.severity = severity
        self.where = where
        self.message = message

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "where": self.where,
            "message": self.message,
        }


# ============================================================================
# Helpers
# ============================================================================


def normalize(text: str) -> str:
    """Lowercase + tira acentos comuns + strip."""
    if not isinstance(text, str):
        return ""
    text = text.lower().strip()
    repl = str.maketrans("áàãâéêíóôõúç", "aaaaeeiooouc")
    return text.translate(repl)


def parse_briefing(path: Path) -> dict:
    """Le BRIEFING.md, extrai frontmatter YAML, devolve dict."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        raise ValueError("Frontmatter YAML nao encontrado (esperado entre `---` no topo).")
    return yaml.safe_load(m.group(1)) or {}


# ============================================================================
# Regras
# ============================================================================


def check_schema(briefing: dict, issues: list) -> None:
    """Campos raiz obrigatorios."""
    required = ["schema_version", "empresa", "data_referencia", "versao",
                "area_documento", "logo", "n1", "processos",
                "artefatos_a_gerar", "validacao"]
    for field in required:
        if field not in briefing:
            issues.append(Issue("SCHEMA-MISSING", "bloqueador", f"root.{field}",
                               f"Campo obrigatorio ausente: `{field}`"))

    if briefing.get("schema_version") != 1:
        issues.append(Issue("SCHEMA-VERSION", "bloqueador", "root.schema_version",
                           "schema_version deve ser 1 no MVP"))


def check_empresa(briefing: dict, issues: list) -> None:
    emp = briefing.get("empresa", {})
    for field in ["nome", "slug", "setor", "escopo"]:
        if not emp.get(field):
            issues.append(Issue("EMPRESA-INCOMPLETA", "bloqueador",
                               f"empresa.{field}", f"Campo obrigatorio ausente em empresa: {field}"))

    slug = emp.get("slug", "")
    if slug and not re.match(r"^[a-z0-9-]+$", slug):
        issues.append(Issue("SLUG-INVALIDO", "bloqueador", "empresa.slug",
                           f"slug deve ser kebab-case (a-z, 0-9, -). Valor: '{slug}'"))


def check_n1(briefing: dict, issues: list) -> None:
    n1 = briefing.get("n1", {})
    variante = n1.get("variante")
    if variante not in ("A", "B"):
        issues.append(Issue("VARIANTE-INVALIDA", "bloqueador", "n1.variante",
                           f"Variante deve ser 'A' ou 'B'. Valor: {variante!r}"))

    contagens = n1.get("contagens", {})
    if not isinstance(contagens, dict):
        issues.append(Issue("CONTAGENS-FORMATO", "bloqueador", "n1.contagens",
                           "Esperado dict com gerenciais/primarios/apoio"))
        return

    for camada in ["gerenciais", "primarios", "apoio"]:
        if camada not in contagens:
            issues.append(Issue("CONTAGENS-MISSING", "bloqueador",
                               f"n1.contagens.{camada}",
                               f"Contagem ausente: {camada}"))


def check_processos(briefing: dict, issues: list) -> None:
    """Validacoes do array de processos + cross-check com n1.contagens."""
    processos = briefing.get("processos", [])
    n1 = briefing.get("n1", {})
    contagens = n1.get("contagens", {})
    artefatos = set(briefing.get("artefatos_a_gerar", []))

    if not processos:
        issues.append(Issue("PROCESSOS-VAZIO", "bloqueador", "processos",
                           "Lista de processos esta vazia"))
        return

    # Contagem por camada
    cam_count = Counter()
    codigos = []
    highlight_count = 0
    blue_count = 0
    primarios_count = 0

    for i, p in enumerate(processos):
        where = f"processos[{i}]"
        codigo = p.get("codigo", f"<sem codigo idx={i}>")

        # Campos obrigatorios
        for field in ["codigo", "camada", "nome", "tooltip"]:
            if not p.get(field):
                issues.append(Issue("PROCESSO-INCOMPLETO", "bloqueador",
                                   f"{where}.{field} ({codigo})",
                                   f"Campo obrigatorio ausente: {field}"))

        # Codigo unico
        if p.get("codigo"):
            codigos.append(p["codigo"])

        # CAMADA-PROIBIDA
        camada = p.get("camada")
        if camada and camada not in CAMADAS_VALIDAS:
            issues.append(Issue("CAMADA-PROIBIDA", "bloqueador",
                               f"{where}.camada ({codigo})",
                               f"Camada invalida: {camada!r}. Use: gerencial | primario | apoio"))
        else:
            cam_count[camada] += 1

        # subcamada (so para primarios variante A)
        if camada == "primario":
            primarios_count += 1
            sc = p.get("subcamada")
            if sc and sc not in SUBCAMADAS_VALIDAS:
                issues.append(Issue("SUBCAMADA-INVALIDA", "bloqueador",
                                   f"{where}.subcamada ({codigo})",
                                   f"Subcamada invalida: {sc!r}. Use: front | nucleo | back"))

        # GERENCIAL-SEM-FREQ
        if camada == "gerencial":
            freq = p.get("frequencia")
            if not freq:
                issues.append(Issue("GERENCIAL-SEM-FREQ", "bloqueador",
                                   f"{where}.frequencia ({codigo})",
                                   "Processo gerencial sem campo `frequencia`. Defina: Anual | Mensal | Semanal | Continua | etc."))
            tooltip = p.get("tooltip", [])
            if tooltip and not any("Freq:" in t for t in tooltip):
                issues.append(Issue("GERENCIAL-TOOLTIP-FREQ", "aviso",
                                   f"{where}.tooltip ({codigo})",
                                   "Tooltip de processo gerencial deve incluir linha 'Freq: ...'"))

        # NOME-LONGO
        nome = p.get("nome", "")
        if nome and len(nome.split()) > 3:
            issues.append(Issue("NOME-LONGO", "aviso", f"{where}.nome ({codigo})",
                               f"Nome com {len(nome.split())} palavras. Maximo 3. Use '&' em vez de 'e'."))

        # highlight/blue
        if p.get("highlight"):
            highlight_count += 1
        if p.get("blue_accent"):
            blue_count += 1

        # SIPOC (se n2 ou n4-pdf vai ser gerado)
        if "n2" in artefatos or "n4-pdf" in artefatos:
            check_sipoc(p, where, issues)

        # N3 (se n3 ou n4-pdf vai ser gerado)
        if "n3" in artefatos or "n4-pdf" in artefatos:
            check_n3_node(p, where, issues)

    # Codigos duplicados
    dup = [c for c, n in Counter(codigos).items() if n > 1]
    if dup:
        issues.append(Issue("CODIGO-DUPLICADO", "bloqueador", "processos[].codigo",
                           f"Codigos repetidos: {dup}"))

    # Cross-check contagens
    expected = {
        "gerenciais": cam_count.get("gerencial", 0),
        "primarios": cam_count.get("primario", 0),
        "apoio": cam_count.get("apoio", 0),
    }
    for k, v in expected.items():
        if k in contagens and contagens[k] != v:
            issues.append(Issue("CONTAGEM-MISMATCH", "bloqueador",
                               f"n1.contagens.{k}",
                               f"Declarado {contagens[k]}, encontrado {v} processos com camada correspondente"))

    total_decl = n1.get("total_processos")
    total_real = len(processos)
    if total_decl is not None and total_decl != total_real:
        issues.append(Issue("TOTAL-MISMATCH", "bloqueador", "n1.total_processos",
                           f"Declarado {total_decl}, encontrado {total_real} processos"))

    # HIGHLIGHT-EXCESSO / BLUE-EXCESSO
    if highlight_count > 2:
        issues.append(Issue("HIGHLIGHT-EXCESSO", "aviso", "processos[].highlight",
                           f"{highlight_count} processos com .highlight. Padrao M7 e maximo 2."))
    if blue_count > 1:
        issues.append(Issue("BLUE-EXCESSO", "aviso", "processos[].blue_accent",
                           f"{blue_count} processos com .blue_accent. Padrao M7 e maximo 1."))

    # PRIM-NUMERO
    if primarios_count and (primarios_count < 3 or primarios_count > 9):
        issues.append(Issue("PRIM-NUMERO", "aviso", "processos[]",
                           f"{primarios_count} processos primarios. Faixa saudavel: 3-9. Confirme escopo."))


def check_sipoc(p: dict, where: str, issues: list) -> None:
    sipoc = p.get("sipoc")
    codigo = p.get("codigo", "?")
    if not sipoc:
        issues.append(Issue("SIPOC-AUSENTE", "bloqueador", f"{where}.sipoc ({codigo})",
                           "Bloco sipoc obrigatorio quando n2 ou n4-pdf esta em artefatos_a_gerar"))
        return

    # VERB-GENERIC
    verbo = (sipoc.get("verbo") or "").strip()
    if verbo:
        verbo_norm = normalize(verbo)
        if verbo_norm in VERBOS_PROIBIDOS:
            issues.append(Issue("VERB-GENERIC", "bloqueador",
                               f"{where}.sipoc.verbo ({codigo})",
                               f"Verbo proibido: {verbo!r}. Use Construir, Operar, Garantir, Definir, Validar, Coordenar."))
        elif verbo_norm.split()[0] in VERBOS_FRACOS:
            issues.append(Issue("VERB-WEAK", "aviso",
                               f"{where}.sipoc.verbo ({codigo})",
                               f"Verbo abstrato: {verbo!r}. Considere especificidade (ex.: Construir vs Trabalhar)."))
    else:
        issues.append(Issue("SIPOC-VERBO-VAZIO", "bloqueador",
                           f"{where}.sipoc.verbo ({codigo})", "Campo verbo vazio."))

    # MISSAO-LISTA (heuristica: se finalidade nao tem 'para' explicito, e missao curta)
    finalidade = (sipoc.get("finalidade") or "").strip()
    if finalidade and "para" not in normalize(finalidade):
        issues.append(Issue("MISSAO-LISTA", "aviso",
                           f"{where}.sipoc.finalidade ({codigo})",
                           "Finalidade deve explicitar o porque (apos 'para'). Reescreva no formato 'para X'."))

    # IO-DUP
    inputs = [normalize(c) for c in (sipoc.get("inputs") or []) if isinstance(c, str)]
    outputs = [normalize(c) for c in (sipoc.get("outputs") or []) if isinstance(c, str)]
    duplicados = set(inputs) & set(outputs)
    if duplicados:
        issues.append(Issue("IO-DUP", "bloqueador",
                           f"{where}.sipoc ({codigo})",
                           f"Termo aparece em inputs E outputs: {sorted(duplicados)}. Decida: entra ou sai do processo?"))

    # CHIPS-FORA-FAIXA
    if inputs and (len(inputs) < 3 or len(inputs) > 6):
        issues.append(Issue("CHIPS-FORA-FAIXA", "aviso",
                           f"{where}.sipoc.inputs ({codigo})",
                           f"{len(inputs)} inputs. Faixa: 3-6."))
    if outputs and (len(outputs) < 3 or len(outputs) > 6):
        issues.append(Issue("CHIPS-FORA-FAIXA", "aviso",
                           f"{where}.sipoc.outputs ({codigo})",
                           f"{len(outputs)} outputs. Faixa: 3-6."))

    # SIPOC-CHIP-LONGO
    for label, lst in [("inputs", sipoc.get("inputs") or []),
                       ("outputs", sipoc.get("outputs") or [])]:
        for j, chip in enumerate(lst):
            if isinstance(chip, str) and len(chip.split()) > 4:
                issues.append(Issue("SIPOC-CHIP-LONGO", "aviso",
                                   f"{where}.sipoc.{label}[{j}] ({codigo})",
                                   f"Chip com {len(chip.split())} palavras: {chip!r}. Maximo 4."))

    # OWNER-PESSOA
    owner = (sipoc.get("owner") or "").strip()
    if owner:
        if not MARCADORES_CARGO.search(owner):
            issues.append(Issue("OWNER-PESSOA", "bloqueador",
                               f"{where}.sipoc.owner ({codigo})",
                               f"Owner sem marcador de cargo: {owner!r}. Use Cargo (CEO, Head de X, Diretor, Comite Y...)."))
    else:
        issues.append(Issue("OWNER-VAZIO", "bloqueador",
                           f"{where}.sipoc.owner ({codigo})", "Campo owner vazio."))


def check_n3_node(p: dict, where: str, issues: list) -> None:
    n3 = p.get("n3")
    codigo = p.get("codigo", "?")
    if not n3:
        issues.append(Issue("N3-AUSENTE", "bloqueador", f"{where}.n3 ({codigo})",
                           "Bloco n3 obrigatorio quando n3 ou n4-pdf esta em artefatos_a_gerar"))
        return

    coluna = n3.get("coluna")
    if coluna not in COLUNAS_VALIDAS:
        issues.append(Issue("N3-COLUNA-INVALIDA", "bloqueador",
                           f"{where}.n3.coluna ({codigo})",
                           f"Coluna invalida: {coluna!r}. Use: {sorted(COLUNAS_VALIDAS)}"))

    pos = n3.get("posicao") or {}
    for axis in ("left", "top"):
        v = pos.get(axis)
        if v is None or not isinstance(v, (int, float)) or v < 0 or v > 100:
            issues.append(Issue("N3-POSICAO-INVALIDA", "bloqueador",
                               f"{where}.n3.posicao.{axis} ({codigo})",
                               f"Posicao deve ser numero 0-100 (%). Valor: {v!r}"))

    fr = n3.get("friction") or {}
    if fr.get("is_friction") and not (fr.get("text") or "").strip():
        issues.append(Issue("FRICTION-SEM-TEXT", "bloqueador",
                           f"{where}.n3.friction ({codigo})",
                           "is_friction=true exige campo text com descricao do problema."))


def check_relacoes(briefing: dict, issues: list) -> None:
    relacoes = briefing.get("relacoes") or []
    artefatos = set(briefing.get("artefatos_a_gerar", []))
    codigos_validos = {p.get("codigo") for p in briefing.get("processos", [])}

    if ("n3" in artefatos or "n4-pdf" in artefatos) and not relacoes:
        issues.append(Issue("RELACOES-VAZIO", "aviso", "relacoes",
                           "Lista de relacoes vazia mas N3 sera gerado. Mapa neural ficara sem arestas."))

    fricoes = sum(1 for p in briefing.get("processos", [])
                  if (p.get("n3") or {}).get("friction", {}).get("is_friction"))
    if fricoes > 4:
        issues.append(Issue("FRICCAO-EXCESSO", "aviso", "processos[].n3.friction",
                           f"{fricoes} fricoes marcadas. Padrao M7 e maximo 4 (mais perde forca semantica)."))

    pares = []
    for i, r in enumerate(relacoes):
        where = f"relacoes[{i}]"

        for field in ["from", "to", "kind", "label"]:
            if not r.get(field):
                issues.append(Issue("RELACAO-INCOMPLETA", "bloqueador",
                                   f"{where}.{field}",
                                   f"Campo obrigatorio ausente: {field}"))

        # REL-ORFA
        for direction in ("from", "to"):
            code = r.get(direction)
            if code and code not in codigos_validos:
                issues.append(Issue("REL-ORFA", "bloqueador",
                                   f"{where}.{direction}",
                                   f"Codigo {code!r} nao existe em processos[]"))

        kind = r.get("kind")
        if kind and kind not in KINDS_VALIDOS:
            issues.append(Issue("KIND-INVALIDO", "bloqueador",
                               f"{where}.kind",
                               f"kind invalido: {kind!r}. Use: cliente | info | decisao"))

        forca = r.get("forca")
        if kind == "cliente" and not forca:
            issues.append(Issue("FORCA-AUSENTE", "bloqueador",
                               f"{where}.forca",
                               "kind=cliente exige campo forca (strong | mid | soft)"))
        if forca and forca not in FORCAS_VALIDAS:
            issues.append(Issue("FORCA-INVALIDA", "bloqueador",
                               f"{where}.forca",
                               f"forca invalida: {forca!r}. Use: strong | mid | soft"))

        if r.get("from") and r.get("to"):
            pares.append((r["from"], r["to"]))

    # REL-DUPLICA: mesmo par com kinds diferentes
    par_kinds = {}
    for r in relacoes:
        key = (r.get("from"), r.get("to"))
        par_kinds.setdefault(key, set()).add(r.get("kind"))
    for key, kinds in par_kinds.items():
        if len(kinds) > 1:
            issues.append(Issue("REL-DUPLICA", "aviso", f"relacoes",
                               f"Par {key[0]}->{key[1]} tem multiplos kinds: {sorted(kinds)}. Escolha um dominante."))


def check_politica(briefing: dict, issues: list) -> None:
    """Valida secao politica: — obrigatoria se n4-pdf em artefatos_a_gerar.

    Politica reune metadata formal (codigo, vigencia, area), controle de versoes,
    aprovacoes (3 papeis com nome/cargo/data), objetivo narrativo, escopo
    (inclusoes/exclusoes/doc_relacionados), governanca e selecao de 2
    processos para a pagina de SIPOC sample.
    """
    artefatos = set(briefing.get("artefatos_a_gerar", []))
    if "n4-pdf" not in artefatos:
        return  # politica e opcional quando N4 nao sera gerado

    politica = briefing.get("politica")
    if not politica:
        issues.append(Issue("POLITICA-AUSENTE", "bloqueador", "politica",
                           "Secao politica: obrigatoria quando n4-pdf esta em artefatos_a_gerar"))
        return

    # metadata
    metadata = politica.get("metadata") or {}
    for f in POLITICA_METADATA_OBRIG:
        v = metadata.get(f)
        if not v or (isinstance(v, str) and v.strip() == ""):
            issues.append(Issue("POLITICA-META-VAZIO", "bloqueador",
                               f"politica.metadata.{f}",
                               f"Campo obrigatorio ausente em politica.metadata: {f}"))

    # versoes
    versoes = politica.get("versoes") or []
    if not versoes:
        issues.append(Issue("POLITICA-SEM-VERSAO", "bloqueador", "politica.versoes",
                           "Deve haver pelo menos 1 versao (a vigente atual)"))
    else:
        vigentes = [v for v in versoes
                    if isinstance(v, dict) and v.get("status") == "vigente"]
        if len(vigentes) != 1:
            issues.append(Issue("POLITICA-VIGENTE", "bloqueador", "politica.versoes",
                               f"Exatamente 1 versao deve ter status=vigente, encontrei {len(vigentes)}"))
        for i, v in enumerate(versoes):
            if not isinstance(v, dict):
                issues.append(Issue("POLITICA-VERSAO-FORMATO", "bloqueador",
                                   f"politica.versoes[{i}]",
                                   "Cada versao deve ser um dict com versao/data/alteracoes/responsavel/status"))
                continue
            for f in POLITICA_VERSAO_CAMPOS:
                val = v.get(f)
                if not val or (isinstance(val, str) and val.strip() == ""):
                    issues.append(Issue("POLITICA-VERSAO-INCOMPLETA", "bloqueador",
                                       f"politica.versoes[{i}].{f}",
                                       f"Campo obrigatorio ausente em versao: {f}"))
            status = v.get("status")
            if status and status not in ("vigente", "obsoleto"):
                issues.append(Issue("POLITICA-VERSAO-STATUS", "bloqueador",
                                   f"politica.versoes[{i}].status",
                                   f"status deve ser 'vigente' ou 'obsoleto'. Valor: {status!r}"))
        if len(versoes) > 3:
            issues.append(Issue("POLITICA-VERSOES-EXCESSO", "aviso", "politica.versoes",
                               f"{len(versoes)} versoes. Template suporta exatamente 3 linhas (vigente + 2 anteriores). Excedentes serao truncados."))

    # aprovacoes
    aprov = politica.get("aprovacoes") or {}
    for role in POLITICA_APROV_PAPEIS:
        r = aprov.get(role) or {}
        if not r:
            issues.append(Issue("POLITICA-APROV-AUSENTE", "bloqueador",
                               f"politica.aprovacoes.{role}",
                               f"Papel de aprovacao ausente: {role}"))
            continue
        if not isinstance(r, dict):
            issues.append(Issue("POLITICA-APROV-FORMATO", "bloqueador",
                               f"politica.aprovacoes.{role}",
                               "Cada papel deve ser um dict com nome/cargo/data"))
            continue
        for f in POLITICA_APROV_CAMPOS:
            val = r.get(f)
            if not val or (isinstance(val, str) and val.strip() == ""):
                issues.append(Issue("POLITICA-APROV-INCOMPLETO", "bloqueador",
                                   f"politica.aprovacoes.{role}.{f}",
                                   f"Campo obrigatorio: {f}"))

    # objetivo_texto
    obj = (politica.get("objetivo_texto") or "")
    obj_s = obj.strip() if isinstance(obj, str) else ""
    if not obj_s:
        issues.append(Issue("POLITICA-OBJ-VAZIO", "bloqueador", "politica.objetivo_texto",
                           "Texto do objetivo vazio. Escreva 2-4 linhas formais."))
    elif len(obj_s) < 40:
        issues.append(Issue("POLITICA-OBJ-CURTO", "aviso", "politica.objetivo_texto",
                           f"Objetivo com {len(obj_s)} caracteres. Recomenda-se 100-400."))

    # escopo
    escopo = politica.get("escopo") or {}
    inclusoes = escopo.get("inclusoes") or []
    exclusoes = escopo.get("exclusoes") or []
    doc_rel = escopo.get("doc_relacionados") or []
    if len(inclusoes) < 2:
        issues.append(Issue("POLITICA-INCLUSOES", "bloqueador", "politica.escopo.inclusoes",
                           f"Pelo menos 2 inclusoes. Encontrado: {len(inclusoes)}"))
    if len(inclusoes) > 3:
        issues.append(Issue("POLITICA-INCLUSOES-EXCESSO", "aviso",
                           "politica.escopo.inclusoes",
                           f"{len(inclusoes)} inclusoes. Template renderiza 3 — excedentes serao truncados."))
    if len(exclusoes) < 1:
        issues.append(Issue("POLITICA-EXCLUSOES", "aviso", "politica.escopo.exclusoes",
                           "Recomenda-se ao menos 1 exclusao (deixar claro o que NAO esta no escopo)."))
    if len(exclusoes) > 2:
        issues.append(Issue("POLITICA-EXCLUSOES-EXCESSO", "aviso",
                           "politica.escopo.exclusoes",
                           f"{len(exclusoes)} exclusoes. Template renderiza 2 — excedentes serao truncados."))
    if len(doc_rel) < 1:
        issues.append(Issue("POLITICA-DOC-REL", "aviso",
                           "politica.escopo.doc_relacionados",
                           "Recomenda-se ao menos 1 documento relacionado."))
    if len(doc_rel) > 3:
        issues.append(Issue("POLITICA-DOC-REL-EXCESSO", "aviso",
                           "politica.escopo.doc_relacionados",
                           f"{len(doc_rel)} documentos. Template renderiza 3 — excedentes serao truncados."))

    # governanca
    gov = politica.get("governanca") or {}
    for f in POLITICA_GOV_OBRIG:
        v = gov.get(f)
        if not v or (isinstance(v, str) and v.strip() == ""):
            issues.append(Issue("POLITICA-GOV-VAZIO", "bloqueador",
                               f"politica.governanca.{f}",
                               f"Campo obrigatorio ausente em politica.governanca: {f}"))

    # sipoc_amostra (cross-check com processos[])
    amostra = politica.get("sipoc_amostra") or []
    processos = briefing.get("processos", [])
    codigos_validos = {p.get("codigo") for p in processos if p.get("codigo")}
    processos_com_sipoc = {p.get("codigo") for p in processos
                           if p.get("sipoc") and (p.get("sipoc") or {}).get("verbo")}
    if len(amostra) != 2:
        issues.append(Issue("POLITICA-AMOSTRA-QTD", "bloqueador", "politica.sipoc_amostra",
                           f"Esperado exatamente 2 codigos para SIPOC sample, encontrei {len(amostra)}"))
    else:
        for i, c in enumerate(amostra):
            if not c or (isinstance(c, str) and c.startswith("{{")):
                issues.append(Issue("POLITICA-AMOSTRA-VAZIA", "bloqueador",
                                   f"politica.sipoc_amostra[{i}]",
                                   "Codigo vazio ou placeholder. Preencha com codigo real de processos[]."))
                continue
            if c not in codigos_validos:
                issues.append(Issue("POLITICA-AMOSTRA-ORFA", "bloqueador",
                                   f"politica.sipoc_amostra[{i}]",
                                   f"Codigo {c!r} nao existe em processos[]"))
            elif c not in processos_com_sipoc:
                issues.append(Issue("POLITICA-AMOSTRA-SEM-SIPOC", "bloqueador",
                                   f"politica.sipoc_amostra[{i}]",
                                   f"Processo {c} nao tem SIPOC preenchido — escolha outro processo com SIPOC."))


def check_processos_meta(briefing: dict, issues: list) -> None:
    """Se n4-pdf, verticais (primarios do nucleo) devem ter campo `meta`.

    P1/P2 (front) e P9 (back) sao excecoes — N4 mostra 'Camada' em vez de 'Meta'
    para esses casos. Apenas verticais do nucleo precisam declarar KR/meta.
    """
    artefatos = set(briefing.get("artefatos_a_gerar", []))
    if "n4-pdf" not in artefatos:
        return
    for i, p in enumerate(briefing.get("processos", [])):
        if p.get("camada") != "primario":
            continue
        codigo = p.get("codigo", "?")
        sc = p.get("subcamada")
        # Heuristica: verticais sao subcamada=nucleo, OU sem subcamada e nao P1/P2/P9
        is_vertical = (sc == "nucleo") or (sc is None and codigo not in ("P1", "P2", "P9"))
        if is_vertical and not (p.get("meta") or "").strip():
            issues.append(Issue("POLITICA-META-PRIM", "aviso",
                               f"processos[{i}].meta ({codigo})",
                               "Vertical (nucleo primario) sem campo `meta`. N4 (Politica) mostra Meta de cada vertical."))


def check_artefatos(briefing: dict, issues: list) -> None:
    arts = briefing.get("artefatos_a_gerar") or []
    invalidos = set(arts) - ARTEFATOS_VALIDOS
    if invalidos:
        issues.append(Issue("ARTEFATO-INVALIDO", "bloqueador", "artefatos_a_gerar",
                           f"Artefatos invalidos: {sorted(invalidos)}. Use: {sorted(ARTEFATOS_VALIDOS)}"))

    if "n4-pdf" in arts:
        for req in ("n1", "n2", "n3"):
            if req not in arts:
                issues.append(Issue("PDF-DEPENDENCIA", "bloqueador", "artefatos_a_gerar",
                                   f"n4-pdf requer {req!r} em artefatos_a_gerar (sequencia rigida)"))


def check_todos(briefing: dict, issues: list) -> None:
    """Detecta {{placeholders}} restantes nos campos string."""

    def walk(obj: Any, path: str) -> None:
        if isinstance(obj, str):
            if "{{" in obj and "}}" in obj:
                issues.append(Issue("PLACEHOLDER-NAO-RESOLVIDO", "aviso", path,
                                   f"Placeholder ainda presente: {obj!r}. Substitua antes de gerar artefatos."))
        elif isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")

    walk(briefing, "root")


# ============================================================================
# Entry point
# ============================================================================


def validate(briefing: dict) -> list:
    """Aplica todas as regras, devolve lista ordenada de Issue."""
    issues: list[Issue] = []
    check_schema(briefing, issues)
    check_empresa(briefing, issues)
    check_n1(briefing, issues)
    check_processos(briefing, issues)
    check_relacoes(briefing, issues)
    check_artefatos(briefing, issues)
    check_politica(briefing, issues)
    check_processos_meta(briefing, issues)
    check_todos(briefing, issues)

    # Ordena: bloqueadores primeiro, depois avisos
    severity_order = {"bloqueador": 0, "aviso": 1}
    issues.sort(key=lambda i: (severity_order.get(i.severity, 2), i.where))
    return issues


def format_human(issues: list, briefing: dict) -> str:
    """Output legivel para humano."""
    bloqueadores = [i for i in issues if i.severity == "bloqueador"]
    avisos = [i for i in issues if i.severity == "aviso"]

    lines = []
    nome = briefing.get("empresa", {}).get("nome", "(sem nome)")
    arts = briefing.get("artefatos_a_gerar", [])
    lines.append(f"\nBRIEFING: {nome}")
    lines.append(f"Artefatos: {', '.join(arts) or '(nenhum)'}")
    lines.append("")
    lines.append(f"Bloqueadores: {len(bloqueadores)}")
    lines.append(f"Avisos:       {len(avisos)}")
    lines.append("")

    if bloqueadores:
        lines.append("BLOQUEADORES (impedem geracao):")
        for i in bloqueadores:
            lines.append(f"  [{i.rule_id}] {i.where}")
            lines.append(f"      {i.message}")
        lines.append("")

    if avisos:
        lines.append("AVISOS (recomenda corrigir):")
        for i in avisos:
            lines.append(f"  [{i.rule_id}] {i.where}")
            lines.append(f"      {i.message}")
        lines.append("")

    if not bloqueadores and not avisos:
        lines.append("OK · pronto para Fase C (geracao de artefatos)")

    return "\n".join(lines)


def main() -> int:
    args = sys.argv[1:]
    json_mode = "--json" in args
    args = [a for a in args if not a.startswith("--")]

    if len(args) != 1:
        sys.stderr.write("Uso: python check_briefing.py <briefing.md> [--json]\n")
        return 2

    path = Path(args[0])
    if not path.is_file():
        sys.stderr.write(f"ERRO: arquivo nao encontrado: {path}\n")
        return 2

    try:
        briefing = parse_briefing(path)
    except yaml.YAMLError as e:
        sys.stderr.write(f"ERRO de parsing YAML: {e}\n")
        return 2
    except ValueError as e:
        sys.stderr.write(f"ERRO: {e}\n")
        return 2

    issues = validate(briefing)
    bloqueadores = [i for i in issues if i.severity == "bloqueador"]

    if json_mode:
        out = {
            "ok": not bloqueadores,
            "bloqueadores": [i.to_dict() for i in issues if i.severity == "bloqueador"],
            "avisos": [i.to_dict() for i in issues if i.severity == "aviso"],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(format_human(issues, briefing))

    return 1 if bloqueadores else 0


if __name__ == "__main__":
    sys.exit(main())
