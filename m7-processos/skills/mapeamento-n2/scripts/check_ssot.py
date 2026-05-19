#!/usr/bin/env python3
"""mapeamento-n2 · validador deterministico dos 4 SSOT MDs.

Aplica as regras de critique-rules.md que tem deteccao deterministica
(regex, cross-check, length, set diff, enum). Regras semanticas ficam
para os subagents n2-interview-critic (Fase A) e n2-build-critic (Fase C).

Uso:
    python check_ssot.py --target processo-n2 ssot/processo-n2.md
    python check_ssot.py --target sipocs       ssot/sipocs.md
    python check_ssot.py --target jornada-cx   ssot/jornada-cx.md
    python check_ssot.py --target data-lake    ssot/data-lake.md
    python check_ssot.py --all ssot/

    python check_ssot.py --target X file.md --json    # output puro JSON
    python check_ssot.py --target X file.md --human   # output legivel (default)

Exit codes:
    0 = ok (bloqueadores vazios em todos os targets rodados)
    1 = bloqueadores presentes em pelo menos 1 target
    2 = erro de parsing (YAML invalido, secao ausente, arquivo nao existe)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "ERRO: PyYAML nao instalado. Rode: pip install -r requirements.txt\n"
    )
    sys.exit(2)


# ============================================================================
# Constantes (espelham critique-rules.md e references/ssot-*.md)
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
ROW_IDS_JORNADA = ["touchpoint", "action", "mot", "pain"]
ROW_IDS_DATALAKE = ["systems", "data"]
TONES_VALIDOS = {"a", "b", "c", "d", "e"}
PAIN_TONES = {"+", "-", "~"}
MOT_INTENSITIES = {1, 2, 3}
DATA_KINDS = {"CRM", "PII", "Score", "Bureau", "Doc", "Contrato",
              "Lastro", "Tesouraria", "Cobranca", "Cobrança", "KPI"}
REG_CODES = {"R1", "R2", "R3", "R4"}
SUP_CODES = {"S1", "S2", "S3", "S4"}

PROCESSO_CODE_RE = re.compile(r"^[PGA]\d+(\.\d+)?$")
SUBPROC_CODE_RE = re.compile(r"^[PGA]\d+\.\d+$")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")

MARCADORES_CARGO = re.compile(
    r"\b(CEO|CFO|COO|CTO|CMO|CIO|CHRO|CXO|"
    r"Head|Diretor|Diretora|Gerente|Coordenador|Coordenadora|"
    r"Comite|Comitê|Forum|Fórum|Conselho|Mesa|"
    r"Lider|Líder|Owner|Especialista|Analista|Gestor|Gestora|"
    r"Tesouraria|Servicing|Backoffice|BO|Cobranca|Cobrança|"
    r"Originador|Comercial|Juridico|Jurídico|Risco|Compliance|Operacoes|Operações)\b",
    re.IGNORECASE,
)


# ============================================================================
# Issue tracking
# ============================================================================


class Issue:
    def __init__(self, rule_id: str, severity: str, where: str, message: str):
        self.rule_id = rule_id
        self.severity = severity  # "bloqueador" | "aviso"
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
    if not isinstance(text, str):
        return ""
    text = text.lower().strip()
    repl = str.maketrans("áàãâéêíóôõúç", "aaaaeeiooouc")
    return text.translate(repl)


def parse_frontmatter(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"SSOT nao encontrado: {path}")
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        raise ValueError(
            f"Frontmatter YAML nao encontrado em {path} (esperado entre `---` no topo)."
        )
    return yaml.safe_load(m.group(1)) or {}


def extract_section(path: Path, header: str) -> str:
    text = path.read_text(encoding="utf-8")
    pattern = rf"^{re.escape(header)}\s*\n(.*?)(?=\n##\s|\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def has_cargo_marker(owner: str) -> bool:
    if not owner:
        return False
    return bool(MARCADORES_CARGO.search(owner))


# ============================================================================
# CHECK · processo-n2.md
# ============================================================================


def check_processo_n2(path: Path, issues: list) -> dict:
    """Valida ssot/processo-n2.md. Retorna o frontmatter parseado para uso em cross-checks."""
    fm = parse_frontmatter(path)

    # SCHEMA-MISSING
    required = ["schema_version", "n1_artifacts", "processo", "wbs", "janela",
                "status", "subprocessos", "interfaces"]
    for field in required:
        if field not in fm:
            issues.append(Issue("SCHEMA-MISSING", "bloqueador", f"root.{field}",
                               f"Campo obrigatorio ausente: {field}"))

    if fm.get("schema_version") != 1:
        issues.append(Issue("SCHEMA-VERSION", "bloqueador", "root.schema_version",
                           "schema_version deve ser 1"))

    # N1 handoff
    n1a = fm.get("n1_artifacts", {})
    briefing_path = n1a.get("briefing")
    if not briefing_path:
        issues.append(Issue("N1-BRIEFING-AUSENTE", "bloqueador", "n1_artifacts.briefing",
                           "Path do BRIEFING.md da N1 obrigatorio"))
    else:
        # Resolve relativo ao SSOT MD
        resolved = (path.parent / briefing_path).resolve()
        if not resolved.exists():
            issues.append(Issue("N1-BRIEFING-AUSENTE", "bloqueador", "n1_artifacts.briefing",
                               f"Arquivo nao existe: {briefing_path} (resolvido: {resolved})"))
        else:
            # Carrega BRIEFING e checa se processo.code esta em processos[]
            try:
                briefing = parse_frontmatter(resolved)
                processo_code = (fm.get("processo") or {}).get("code")
                if processo_code:
                    codes_n1 = {p.get("codigo") for p in (briefing.get("processos") or [])}
                    if processo_code not in codes_n1:
                        issues.append(Issue("N1-CODIGO-NAO-ENCONTRADO", "bloqueador",
                                           "processo.code",
                                           f"Code {processo_code!r} nao esta em processos[] "
                                           f"do BRIEFING N1. Encontrados: {sorted(c for c in codes_n1 if c)}"))
            except Exception as e:
                issues.append(Issue("N1-BRIEFING-INVALIDO", "bloqueador", "n1_artifacts.briefing",
                                   f"Falha ao ler BRIEFING N1: {e}"))

    if not n1a.get("politica"):
        issues.append(Issue("POLITICA-AUSENTE", "aviso", "n1_artifacts.politica",
                           "Recomendado para rastreabilidade governanca"))

    # processo
    proc = fm.get("processo") or {}
    code = proc.get("code", "")
    if code and not PROCESSO_CODE_RE.match(code):
        issues.append(Issue("PROCESSO-CODE-INVALIDO", "bloqueador", "processo.code",
                           f"Code {code!r} nao casa regex ^[PGA]\\d+(\\.\\d+)?$"))

    slug = proc.get("slug", "")
    if slug and not SLUG_RE.match(slug):
        issues.append(Issue("SLUG-INVALIDO", "bloqueador", "processo.slug",
                           f"Slug deve ser kebab-case. Valor: {slug!r}"))

    camada = proc.get("camada")
    if camada and camada not in CAMADAS_VALIDAS:
        issues.append(Issue("CAMADA-INVALIDA", "bloqueador", "processo.camada",
                           f"Fora de {CAMADAS_VALIDAS}. Valor: {camada!r}"))

    owner = proc.get("owner", "")
    if owner and not has_cargo_marker(owner):
        issues.append(Issue("OWNER-PESSOA", "bloqueador", "processo.owner",
                           f"Owner sem marcador de cargo: {owner!r}. "
                           f"Use Diretor/Head/Gerente/Comite/Mesa/etc."))

    # subprocessos
    subprocs = fm.get("subprocessos") or []
    if not 3 <= len(subprocs) <= 8:
        issues.append(Issue("SUBPROCESSOS-FAIXA", "bloqueador", "subprocessos",
                           f"Count {len(subprocs)} fora de [3..8]. "
                           f"Granularidade N2 = 3-8 subprocs. Mais que isso e N3."))

    codes_seen = []
    for i, sp in enumerate(subprocs):
        where = f"subprocessos[{i}]"
        for f in ["id", "code", "name", "owner", "cadence", "sp_meta", "sp_tech"]:
            if not sp.get(f):
                issues.append(Issue("SUBPROCESSO-INCOMPLETO", "bloqueador",
                                   f"{where}.{f}", f"Campo ausente: {f}"))

        sp_code = sp.get("code", "")
        if sp_code:
            codes_seen.append(sp_code)

        sp_owner = sp.get("owner", "")
        if sp_owner and not has_cargo_marker(sp_owner):
            issues.append(Issue("OWNER-PESSOA", "bloqueador", f"{where}.owner",
                               f"Owner sem marcador de cargo: {sp_owner!r}"))

        sp_meta = sp.get("sp_meta", "")
        if sp_meta and len(sp_meta) > 60:
            issues.append(Issue("SP-META-LONGO", "aviso", f"{where}.sp_meta",
                               f"{len(sp_meta)} chars (max 60 cabe no card)"))

        sp_tech = sp.get("sp_tech", "")
        if sp_tech and len(sp_tech) > 80:
            issues.append(Issue("SP-TECH-LONGO", "aviso", f"{where}.sp_tech",
                               f"{len(sp_tech)} chars (max 80)"))

    dup = [c for c, n in Counter(codes_seen).items() if n > 1]
    if dup:
        issues.append(Issue("SUBPROCESSO-CODE-DUP", "bloqueador", "subprocessos[].code",
                           f"Codes duplicados: {dup}"))

    # interfaces
    interfaces = fm.get("interfaces") or []
    if len(interfaces) != len(subprocs):
        issues.append(Issue("INTERFACES-COUNT", "bloqueador", "interfaces",
                           f"interfaces.length={len(interfaces)} != subprocessos.length={len(subprocs)}"))

    if_codes = {i.get("code") for i in interfaces}
    sp_codes = set(codes_seen)
    orfas = if_codes - sp_codes
    if orfas:
        issues.append(Issue("INTERFACES-CODE-ORFA", "bloqueador", "interfaces[].code",
                           f"Codes que nao correspondem a nenhum subproc: {sorted(c for c in orfas if c)}"))

    # Lede
    lede = extract_section(path, "## Lede")
    if not lede or len(lede) < 30:
        issues.append(Issue("LEDE-AUSENTE", "bloqueador", "secao `## Lede`",
                           "Falta secao `## Lede` ou conteudo < 30 chars"))

    return fm


# ============================================================================
# CHECK · sipocs.md
# ============================================================================


def check_sipocs(path: Path, issues: list) -> dict:
    fm = parse_frontmatter(path)

    for f in ["schema_version", "processo_ref", "slug", "subprocessos"]:
        if f not in fm:
            issues.append(Issue("SCHEMA-MISSING", "bloqueador", f"root.{f}",
                               f"Campo ausente: {f}"))

    subprocs = fm.get("subprocessos") or []
    for i, sp in enumerate(subprocs):
        where = f"subprocessos[{i}]"
        sp_code = sp.get("code", f"<idx={i}>")
        loc = f"{where} ({sp_code})"

        for f in ["id", "code", "name", "purpose", "cadence", "owner",
                  "sistemas", "volume", "inputs", "outputs", "etapas",
                  "regulacao", "suporte"]:
            if not sp.get(f) and sp.get(f) != []:  # array vazio reportado por outras regras
                issues.append(Issue("SUBPROC-INCOMPLETO", "bloqueador",
                                   f"{loc}.{f}", f"Campo ausente: {f}"))

        # purpose
        purpose = (sp.get("purpose") or "").strip()
        if not purpose:
            issues.append(Issue("PURPOSE-VAZIO", "bloqueador",
                               f"{loc}.purpose", "Purpose vazio"))
        elif len(purpose) < 30:
            issues.append(Issue("PURPOSE-VAZIO", "bloqueador",
                               f"{loc}.purpose", f"Purpose muito curto ({len(purpose)} chars, min 30)"))
        else:
            first_word = normalize(purpose).split()[0] if purpose else ""
            if first_word in VERBOS_PROIBIDOS:
                issues.append(Issue("VERB-GENERIC", "bloqueador",
                                   f"{loc}.purpose",
                                   f"Verbo proibido: {first_word!r}. "
                                   f"Use Capturar/Avaliar/Decidir/Estruturar/Liberar/Monitorar."))
            elif first_word in VERBOS_FRACOS:
                issues.append(Issue("VERB-WEAK", "aviso", f"{loc}.purpose",
                                   f"Verbo abstrato: {first_word!r}. Considere especificidade."))
            if len(purpose) > 200:
                issues.append(Issue("PURPOSE-LONGO", "aviso", f"{loc}.purpose",
                                   f"{len(purpose)} chars (>200 quebra layout)"))

        # owner
        owner = sp.get("owner", "")
        if owner and not has_cargo_marker(owner):
            issues.append(Issue("OWNER-PESSOA", "bloqueador", f"{loc}.owner",
                               f"Owner sem marcador de cargo: {owner!r}"))

        # inputs / outputs
        inputs = sp.get("inputs") or []
        outputs = sp.get("outputs") or []
        if not 3 <= len(inputs) <= 5:
            issues.append(Issue("IO-COUNT", "bloqueador", f"{loc}.inputs",
                               f"Length {len(inputs)} fora de [3..5]"))
        if not 3 <= len(outputs) <= 5:
            issues.append(Issue("IO-COUNT", "bloqueador", f"{loc}.outputs",
                               f"Length {len(outputs)} fora de [3..5]"))

        # IO-DUP
        in_whats = {normalize(i.get("what", "")) for i in inputs if i.get("what")}
        out_whats = {normalize(o.get("what", "")) for o in outputs if o.get("what")}
        dups = in_whats & out_whats
        dups.discard("")
        if dups:
            issues.append(Issue("IO-DUP", "bloqueador", f"{loc}.outputs[].what",
                               f"Outputs duplicam inputs (pass-through?): {sorted(dups)}"))

        # details
        for j, inp in enumerate(inputs):
            if not inp.get("detail"):
                issues.append(Issue("DETAIL-AUSENTE", "aviso",
                                   f"{loc}.inputs[{j}].detail",
                                   "Sem detail (perde info no DEIP)"))
        for j, out in enumerate(outputs):
            if not out.get("detail"):
                issues.append(Issue("DETAIL-AUSENTE", "aviso",
                                   f"{loc}.outputs[{j}].detail",
                                   "Sem detail"))

        # etapas
        etapas = sp.get("etapas") or []
        if not 4 <= len(etapas) <= 8:
            issues.append(Issue("ETAPAS-FAIXA", "bloqueador", f"{loc}.etapas",
                               f"Length {len(etapas)} fora de [4..8]"))
        for j, et in enumerate(etapas):
            if isinstance(et, str) and len(et) > 80:
                issues.append(Issue("ETAPA-LONGA", "aviso", f"{loc}.etapas[{j}]",
                                   f"{len(et)} chars (>80)"))

        # regulacao
        reg = sp.get("regulacao") or []
        if not 2 <= len(reg) <= 4:
            issues.append(Issue("REG-FAIXA", "bloqueador", f"{loc}.regulacao",
                               f"Length {len(reg)} fora de [2..4]"))
        for j, r in enumerate(reg):
            if r.get("code") and r.get("code") not in REG_CODES:
                issues.append(Issue("REG-CODE-INVALIDO", "bloqueador",
                                   f"{loc}.regulacao[{j}].code",
                                   f"Code {r['code']!r} fora de {REG_CODES}"))
            if not r.get("detail"):
                issues.append(Issue("DETAIL-AUSENTE", "aviso",
                                   f"{loc}.regulacao[{j}].detail", "Sem detail"))

        # suporte
        sup = sp.get("suporte") or []
        if not 2 <= len(sup) <= 4:
            issues.append(Issue("SUP-FAIXA", "bloqueador", f"{loc}.suporte",
                               f"Length {len(sup)} fora de [2..4]"))
        for j, s in enumerate(sup):
            if s.get("code") and s.get("code") not in SUP_CODES:
                issues.append(Issue("SUP-CODE-INVALIDO", "bloqueador",
                                   f"{loc}.suporte[{j}].code",
                                   f"Code {s['code']!r} fora de {SUP_CODES}"))
            if not s.get("detail"):
                issues.append(Issue("DETAIL-AUSENTE", "aviso",
                                   f"{loc}.suporte[{j}].detail", "Sem detail"))

    return fm


# ============================================================================
# CHECK · jornada-cx.md
# ============================================================================


def check_jornada_cx(path: Path, issues: list) -> dict:
    fm = parse_frontmatter(path)

    for f in ["schema_version", "processo_ref", "slug", "processos", "rows"]:
        if f not in fm:
            issues.append(Issue("SCHEMA-MISSING", "bloqueador", f"root.{f}",
                               f"Campo ausente: {f}"))

    processos = fm.get("processos") or []
    n_procs = len(processos)
    if n_procs < 1:
        issues.append(Issue("PROCESSOS-VAZIO", "bloqueador", "processos",
                           "Lista processos[] vazia"))

    for i, p in enumerate(processos):
        if p.get("tone") and p["tone"] not in TONES_VALIDOS:
            issues.append(Issue("TONE-INVALIDO", "bloqueador",
                               f"processos[{i}].tone",
                               f"Tone {p['tone']!r} fora de {TONES_VALIDOS}"))

    rows = fm.get("rows") or []
    if len(rows) != 4:
        issues.append(Issue("ROWS-COUNT", "bloqueador", "rows",
                           f"rows.length={len(rows)} != 4"))

    row_ids = [r.get("id") for r in rows]
    invalid_ids = set(row_ids) - set(ROW_IDS_JORNADA) - {None}
    if invalid_ids:
        issues.append(Issue("ROWS-ID-INVALIDO", "bloqueador", "rows[].id",
                           f"IDs invalidos: {sorted(invalid_ids)}. Aceitos: {ROW_IDS_JORNADA}"))

    dup_ids = [rid for rid, n in Counter(row_ids).items() if n > 1 and rid]
    if dup_ids:
        issues.append(Issue("ROWS-ID-DUP", "bloqueador", "rows[].id",
                           f"IDs duplicados: {dup_ids}"))

    for i, row in enumerate(rows):
        rid = row.get("id")
        cells = row.get("cells") or []
        if len(cells) != n_procs and n_procs > 0:
            issues.append(Issue("CELLS-COUNT", "bloqueador", f"rows[{i}]({rid}).cells",
                               f"cells.length={len(cells)} != processos.length={n_procs}"))

        if rid == "touchpoint":
            for j, c in enumerate(cells):
                if isinstance(c, str) and len(c) > 100:
                    issues.append(Issue("TOUCHPOINT-LONGO", "aviso",
                                       f"rows[{i}].cells[{j}]",
                                       f"{len(c)} chars (>100)"))
        elif rid == "action":
            for j, c in enumerate(cells):
                if isinstance(c, str) and len(c) > 120:
                    issues.append(Issue("ACTION-LONGO", "aviso",
                                       f"rows[{i}].cells[{j}]",
                                       f"{len(c)} chars (>120)"))
        elif rid == "mot":
            for j, c in enumerate(cells):
                if not isinstance(c, dict):
                    continue
                intensity = c.get("intensity")
                if intensity not in MOT_INTENSITIES:
                    issues.append(Issue("MOT-INTENSITY-INVALIDA", "bloqueador",
                                       f"rows[{i}].cells[{j}].intensity",
                                       f"Valor {intensity!r} fora de {MOT_INTENSITIES}"))
                items = c.get("items") or []
                if not items:
                    issues.append(Issue("MOT-ITEMS-VAZIO", "bloqueador",
                                       f"rows[{i}].cells[{j}].items",
                                       "Items vazio"))
                for k, item in enumerate(items):
                    if isinstance(item, str) and len(item) > 80:
                        issues.append(Issue("MOT-ITEM-LONGO", "aviso",
                                           f"rows[{i}].cells[{j}].items[{k}]",
                                           f"{len(item)} chars (>80)"))
        elif rid == "pain":
            for j, c in enumerate(cells):
                if not isinstance(c, dict):
                    continue
                tone = c.get("tone")
                if tone not in PAIN_TONES:
                    issues.append(Issue("PAIN-TONE-INVALIDO", "bloqueador",
                                       f"rows[{i}].cells[{j}].tone",
                                       f"Valor {tone!r} fora de {PAIN_TONES}"))
                items = c.get("items") or []
                if not items:
                    issues.append(Issue("PAIN-ITEMS-VAZIO", "bloqueador",
                                       f"rows[{i}].cells[{j}].items",
                                       "Items vazio"))
                for k, item in enumerate(items):
                    if isinstance(item, str) and not item.startswith('"'):
                        issues.append(Issue("PAIN-ITEM-SEM-ASPAS", "aviso",
                                           f"rows[{i}].cells[{j}].items[{k}]",
                                           "Recomendado formato fala-do-cliente entre aspas"))

    return fm


# ============================================================================
# CHECK · data-lake.md
# ============================================================================


def check_data_lake(path: Path, issues: list) -> dict:
    fm = parse_frontmatter(path)

    for f in ["schema_version", "processo_ref", "slug", "processos",
              "rows", "marts", "consumers"]:
        if f not in fm:
            issues.append(Issue("SCHEMA-MISSING", "bloqueador", f"root.{f}",
                               f"Campo ausente: {f}"))

    processos = fm.get("processos") or []
    n_procs = len(processos)

    for i, p in enumerate(processos):
        if p.get("tone") and p["tone"] not in TONES_VALIDOS:
            issues.append(Issue("TONE-INVALIDO", "bloqueador",
                               f"processos[{i}].tone",
                               f"Tone {p['tone']!r} fora de {TONES_VALIDOS}"))

    rows = fm.get("rows") or []
    if len(rows) != 2:
        issues.append(Issue("ROWS-COUNT", "bloqueador", "rows",
                           f"rows.length={len(rows)} != 2"))

    row_ids = [r.get("id") for r in rows]
    invalid_ids = set(row_ids) - set(ROW_IDS_DATALAKE) - {None}
    if invalid_ids:
        issues.append(Issue("ROWS-ID-INVALIDO", "bloqueador", "rows[].id",
                           f"IDs invalidos: {sorted(invalid_ids)}. Aceitos: {ROW_IDS_DATALAKE}"))

    for i, row in enumerate(rows):
        rid = row.get("id")
        cells = row.get("cells") or []
        if len(cells) != n_procs and n_procs > 0:
            issues.append(Issue("CELLS-COUNT", "bloqueador", f"rows[{i}]({rid}).cells",
                               f"cells.length={len(cells)} != processos.length={n_procs}"))

        if rid == "systems":
            for j, c in enumerate(cells):
                if not c:
                    issues.append(Issue("SYSTEMS-VAZIO", "bloqueador",
                                       f"rows[{i}].cells[{j}]",
                                       "Array de sistemas vazio"))
                if isinstance(c, list):
                    for k, sys_name in enumerate(c):
                        if isinstance(sys_name, str) and len(sys_name) > 30:
                            issues.append(Issue("SYSTEM-NOME-LONGO", "aviso",
                                               f"rows[{i}].cells[{j}][{k}]",
                                               f"{len(sys_name)} chars (>30)"))
        elif rid == "data":
            for j, c in enumerate(cells):
                if not c:
                    issues.append(Issue("DATA-VAZIO", "bloqueador",
                                       f"rows[{i}].cells[{j}]",
                                       "Array de dados vazio"))
                if isinstance(c, list):
                    for k, item in enumerate(c):
                        if not isinstance(item, dict):
                            continue
                        for f in ["name", "where", "kind"]:
                            if not item.get(f):
                                issues.append(Issue("DATA-INCOMPLETO", "bloqueador",
                                                   f"rows[{i}].cells[{j}][{k}].{f}",
                                                   f"Campo ausente: {f}"))
                        kind = item.get("kind")
                        if kind and kind not in DATA_KINDS:
                            issues.append(Issue("KIND-INVALIDO", "bloqueador",
                                               f"rows[{i}].cells[{j}][{k}].kind",
                                               f"Kind {kind!r} fora do enum {sorted(DATA_KINDS)}"))
                        where = item.get("where", "")
                        if where and len(where) < 8:
                            issues.append(Issue("DATA-WHERE-AUSENTE", "aviso",
                                               f"rows[{i}].cells[{j}][{k}].where",
                                               f"where muito curto ({where!r})"))

    # marts
    marts = fm.get("marts") or {}
    dim = marts.get("dim") or []
    fact = marts.get("fact") or []

    if len(dim) < 3:
        issues.append(Issue("MARTS-DIM-FAIXA", "bloqueador", "marts.dim",
                           f"Length {len(dim)} < 3"))
    if len(fact) < 3:
        issues.append(Issue("MARTS-FACT-FAIXA", "bloqueador", "marts.fact",
                           f"Length {len(fact)} < 3"))

    for i, d in enumerate(dim):
        name = d.get("name", "")
        if name and not name.startswith("dim_"):
            issues.append(Issue("MART-DIM-NOME-INVALIDO", "bloqueador",
                               f"marts.dim[{i}].name",
                               f"Nome {name!r} nao comeca com 'dim_'"))
    for i, f in enumerate(fact):
        name = f.get("name", "")
        if name and not name.startswith("fact_"):
            issues.append(Issue("MART-FACT-NOME-INVALIDO", "bloqueador",
                               f"marts.fact[{i}].name",
                               f"Nome {name!r} nao comeca com 'fact_'"))

    # consumers
    consumers = fm.get("consumers") or []
    if len(consumers) < 4:
        issues.append(Issue("CONSUMERS-FAIXA", "bloqueador", "consumers",
                           f"Length {len(consumers)} < 4"))

    tiers = [c.get("tier") for c in consumers if c.get("tier")]
    dup_tiers = [t for t, n in Counter(tiers).items() if n > 1]
    if dup_tiers:
        issues.append(Issue("CONSUMER-TIER-DUP", "bloqueador", "consumers[].tier",
                           f"Tiers duplicados: {dup_tiers}"))

    return fm


# ============================================================================
# Cross-checks transversais (--all)
# ============================================================================


def cross_checks(parsed: dict, issues: list) -> None:
    """parsed = {target: frontmatter_dict} para os 4 MDs."""
    pn2 = parsed.get("processo-n2") or {}
    sip = parsed.get("sipocs") or {}
    jor = parsed.get("jornada-cx") or {}
    dlk = parsed.get("data-lake") or {}

    sp_codes_pn2 = [s.get("code") for s in (pn2.get("subprocessos") or []) if s.get("code")]
    sp_codes_sip = [s.get("code") for s in (sip.get("subprocessos") or []) if s.get("code")]
    sp_codes_jor = [s.get("code") for s in (jor.get("processos") or []) if s.get("code")]
    sp_codes_dlk = [s.get("code") for s in (dlk.get("processos") or []) if s.get("code")]

    if pn2 and sip:
        if set(sp_codes_pn2) != set(sp_codes_sip):
            diff = (set(sp_codes_pn2) ^ set(sp_codes_sip))
            issues.append(Issue("SUBPROC-MISMATCH", "bloqueador",
                               "sipocs.md vs processo-n2.md",
                               f"Set de codes difere. Symmetric diff: {sorted(diff)}"))
        elif sp_codes_pn2 != sp_codes_sip:
            issues.append(Issue("SUBPROC-ORDEM-MISMATCH", "aviso",
                               "sipocs.md vs processo-n2.md",
                               f"Ordem difere: pn2={sp_codes_pn2} sip={sp_codes_sip}"))

    if pn2 and jor:
        if set(sp_codes_pn2) != set(sp_codes_jor):
            diff = (set(sp_codes_pn2) ^ set(sp_codes_jor))
            issues.append(Issue("JORNADA-PROCESSOS-MISMATCH", "bloqueador",
                               "jornada-cx.md vs processo-n2.md",
                               f"Set de codes difere. Symmetric diff: {sorted(diff)}"))

    if pn2 and dlk:
        if set(sp_codes_pn2) != set(sp_codes_dlk):
            diff = (set(sp_codes_pn2) ^ set(sp_codes_dlk))
            issues.append(Issue("DATALAKE-PROCESSOS-MISMATCH", "bloqueador",
                               "data-lake.md vs processo-n2.md",
                               f"Set de codes difere. Symmetric diff: {sorted(diff)}"))


# ============================================================================
# Output
# ============================================================================


def render_human(issues: list, target: str) -> str:
    lines = [f"\n=== {target} ==="]
    bloq = [i for i in issues if i.severity == "bloqueador"]
    avi = [i for i in issues if i.severity == "aviso"]

    if not bloq and not avi:
        lines.append("  ✓ Nenhum bloqueador, nenhum aviso. Pronto para Fase C.")
        return "\n".join(lines)

    if bloq:
        lines.append(f"\n  ✗ BLOQUEADORES ({len(bloq)}):")
        for i in bloq:
            lines.append(f"    [{i.rule_id}] {i.where}")
            lines.append(f"        {i.message}")
    if avi:
        lines.append(f"\n  ⚠ AVISOS ({len(avi)}):")
        for i in avi:
            lines.append(f"    [{i.rule_id}] {i.where}")
            lines.append(f"        {i.message}")
    return "\n".join(lines)


# ============================================================================
# Main
# ============================================================================


TARGETS = ["processo-n2", "sipocs", "jornada-cx", "data-lake"]

CHECKERS = {
    "processo-n2": check_processo_n2,
    "sipocs": check_sipocs,
    "jornada-cx": check_jornada_cx,
    "data-lake": check_data_lake,
}


def main():
    parser = argparse.ArgumentParser(description="Validador deterministico dos SSOT MDs (mapeamento-n2)")
    parser.add_argument("--target", choices=TARGETS, help="Qual MD validar")
    parser.add_argument("--all", action="store_true",
                       help="Roda os 4 targets + cross-checks. Argumento posicional = pasta ssot/")
    parser.add_argument("--json", action="store_true", help="Output JSON puro")
    parser.add_argument("--human", action="store_true", help="Output legivel (default)")
    parser.add_argument("path", help="Path do SSOT MD (ou pasta ssot/ se --all)")
    args = parser.parse_args()

    output_mode = "json" if args.json else "human"
    all_results = {}
    all_issues_flat = []

    try:
        if args.all:
            ssot_dir = Path(args.path)
            if not ssot_dir.is_dir():
                sys.stderr.write(f"ERRO: --all requer pasta ssot/, recebido: {ssot_dir}\n")
                sys.exit(2)

            parsed_all = {}
            for target in TARGETS:
                target_path = ssot_dir / f"{target}.md"
                if not target_path.exists():
                    issue = Issue("FILE-MISSING", "bloqueador", str(target_path),
                                 f"SSOT {target}.md ausente em {ssot_dir}")
                    all_results[target] = [issue]
                    all_issues_flat.append(issue)
                    continue
                issues = []
                try:
                    fm = CHECKERS[target](target_path, issues)
                    parsed_all[target] = fm
                except Exception as e:
                    issues.append(Issue("PARSE-ERROR", "bloqueador", str(target_path),
                                       f"Falha no parse: {e}"))
                all_results[target] = issues
                all_issues_flat.extend(issues)

            cross_issues = []
            cross_checks(parsed_all, cross_issues)
            all_results["__cross__"] = cross_issues
            all_issues_flat.extend(cross_issues)
        else:
            if not args.target:
                sys.stderr.write("ERRO: --target obrigatorio (ou use --all)\n")
                sys.exit(2)
            issues = []
            try:
                CHECKERS[args.target](Path(args.path), issues)
            except Exception as e:
                issues.append(Issue("PARSE-ERROR", "bloqueador", args.path,
                                   f"Falha: {e}"))
            all_results[args.target] = issues
            all_issues_flat = issues

    except Exception as e:
        sys.stderr.write(f"ERRO inesperado: {e}\n")
        sys.exit(2)

    # Output
    if output_mode == "json":
        out = {
            "targets": {t: [i.to_dict() for i in lst] for t, lst in all_results.items()},
            "bloqueadores": [i.to_dict() for i in all_issues_flat if i.severity == "bloqueador"],
            "avisos": [i.to_dict() for i in all_issues_flat if i.severity == "aviso"],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for target, lst in all_results.items():
            print(render_human(lst, target))

        total_bloq = sum(1 for i in all_issues_flat if i.severity == "bloqueador")
        total_avi = sum(1 for i in all_issues_flat if i.severity == "aviso")
        print(f"\n{'=' * 60}")
        print(f"TOTAL: {total_bloq} bloqueadores · {total_avi} avisos")
        print('=' * 60)

    total_bloq = sum(1 for i in all_issues_flat if i.severity == "bloqueador")
    sys.exit(1 if total_bloq > 0 else 0)


if __name__ == "__main__":
    main()
