#!/usr/bin/env python3
"""
generate-html-yaml.py — Pipeline da Fase 3 de creating-politica.

Lê BRIEFING.md (YAML estruturado), valida contra normativo.schema.yaml,
e emite o par {slug}.yaml + {slug}.html (HTML montado a partir do template
oficial com todos os anchors de identidade/metadata espelhados).

CLI:
    python generate-html-yaml.py \\
        --briefing  BRIEFING-POL-GOV-003.md \\
        --output-dir <dir> \\
        [--content politica-foo.md] \\
        [--basename politica-foo] \\
        [--template <path>] \\
        [--schema <path>] \\
        [--validate-only]

Comportamento de conteúdo de seções (pages 3-15):
- Sem --content: mantém o conteúdo do template (que vem do exemplo POL-GOV-002).
  O usuário edita manualmente o HTML após a geração.
- Com --content: parsing simples por seção (## N. Nome) e injeção crua de
  HTML renderizado dentro de cada <main class="page-body">. Limitação atual:
  styling avançado (.principle-card, .doc-table) precisa de ajuste manual.

A regra inegociável (handoff §2): a estrutura/classes do HTML é INVARIANTE.
O script SÓ mexe nos valores espelhados — nunca em ordem de páginas, tags ou
classes.
"""
import argparse
import re
import sys
from datetime import date, datetime
from html import escape
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("ERRO: pyyaml não instalado. Rode: pip install pyyaml\n")
    sys.exit(2)


# =============================================================================
# Validation (custom, leve — schema usa keywords não-JSON-Schema)
# =============================================================================

ALLOWED_TIPO = {"POL", "MAN", "INS", "ESP"}
ALLOWED_AREA = {"GOV", "PERF", "INV", "CRE", "SEG", "UNI", "TEC", "PES", "M7"}
ALLOWED_STATUS = {"vigente", "revisao", "rascunho", "pendente", "vencido"}
ALLOWED_CLASSIF = {"Público", "Interno", "Confidencial", "Restrito"}
ALLOWED_REVISAO = {"Anual", "Semestral", "Trimestral", "Mensal", "Sob demanda"}

CODE_PATTERN = re.compile(r"^(POL|MAN|INS|ESP)-[A-Z]{2,4}-[0-9]{3}$")
VERSION_PATTERN = re.compile(r"^v?[0-9]+\.[0-9]+$")
PROC_PATTERN = re.compile(r"^(G[1-4]|P[1-9]|P1[0-2]|A[1-5])$")


def _err(path: str, msg: str) -> str:
    return f"  · {path}: {msg}"


def validate(data: dict) -> list:
    """Retorna lista de erros (vazia = válido)."""
    errs: list = []

    if data.get("schema_version") != "1.0":
        errs.append(_err("schema_version", "deve ser '1.0'"))

    # identity
    i = data.get("identity") or {}
    if not isinstance(i, dict):
        errs.append(_err("identity", "objeto obrigatório"))
    else:
        for f in ("code", "tipo", "area", "version", "status", "pages", "classif"):
            if f not in i:
                errs.append(_err(f"identity.{f}", "obrigatório"))
        if i.get("code") and not CODE_PATTERN.match(i["code"]):
            errs.append(_err("identity.code", f"deve casar {CODE_PATTERN.pattern}"))
        if i.get("tipo") and i["tipo"] not in ALLOWED_TIPO:
            errs.append(_err("identity.tipo", f"deve ser um de {sorted(ALLOWED_TIPO)}"))
        if i.get("area") and i["area"] not in ALLOWED_AREA:
            errs.append(_err("identity.area", f"deve ser um de {sorted(ALLOWED_AREA)}"))
        if i.get("status") and i["status"] not in ALLOWED_STATUS:
            errs.append(_err("identity.status", f"deve ser um de {sorted(ALLOWED_STATUS)}"))
        if i.get("classif") and i["classif"] not in ALLOWED_CLASSIF:
            errs.append(_err("identity.classif", f"deve ser um de {sorted(ALLOWED_CLASSIF)}"))
        if i.get("version") and not VERSION_PATTERN.match(i["version"]):
            errs.append(_err("identity.version", "deve casar v?\\d+\\.\\d+"))
        if "pages" in i and not isinstance(i["pages"], int):
            errs.append(_err("identity.pages", "deve ser inteiro"))

    # lifecycle
    l = data.get("lifecycle") or {}
    if not isinstance(l, dict):
        errs.append(_err("lifecycle", "objeto obrigatório"))
    else:
        status = (data.get("identity") or {}).get("status")
        for f in ("date", "nextReview"):
            if f not in l and status in {"vigente", "revisao", "vencido"}:
                errs.append(_err(f"lifecycle.{f}", f"obrigatório quando status={status}"))
        if "revisaoFreq" not in l:
            errs.append(_err("lifecycle.revisaoFreq", "obrigatório"))
        elif l["revisaoFreq"] not in ALLOWED_REVISAO:
            errs.append(_err("lifecycle.revisaoFreq", f"deve ser um de {sorted(ALLOWED_REVISAO)}"))

    # governance
    g = data.get("governance") or {}
    if not isinstance(g, dict):
        errs.append(_err("governance", "objeto obrigatório"))
    else:
        for f in ("owner", "parent", "processos"):
            if f not in g:
                errs.append(_err(f"governance.{f}", "obrigatório"))
        parent = g.get("parent")
        if parent is not None and not isinstance(parent, dict):
            errs.append(_err("governance.parent", "deve ser null ou objeto com {code, title}"))
        elif isinstance(parent, dict) and not CODE_PATTERN.match(parent.get("code", "")):
            errs.append(_err("governance.parent.code", f"deve casar {CODE_PATTERN.pattern}"))
        procs = g.get("processos") or []
        if not isinstance(procs, list):
            errs.append(_err("governance.processos", "deve ser lista"))
        else:
            for p in procs:
                if not PROC_PATTERN.match(str(p)):
                    errs.append(_err("governance.processos", f"item inválido: {p}"))

    # presentation
    p = data.get("presentation") or {}
    if not isinstance(p, dict):
        errs.append(_err("presentation", "objeto obrigatório"))
    else:
        for f in ("title_short", "title_full", "subtitle", "lede"):
            if f not in p:
                errs.append(_err(f"presentation.{f}", "obrigatório"))
        tf = p.get("title_full") or {}
        if not isinstance(tf, dict) or "parts" not in tf:
            errs.append(_err("presentation.title_full.parts", "obrigatório"))
        elif not isinstance(tf["parts"], list) or not tf["parts"]:
            errs.append(_err("presentation.title_full.parts", "lista não-vazia"))
        else:
            for idx, part in enumerate(tf["parts"]):
                if "text" not in part:
                    errs.append(_err(f"presentation.title_full.parts[{idx}].text", "obrigatório"))

    return errs


# =============================================================================
# Briefing parser
# =============================================================================

def parse_briefing(path: Path) -> dict:
    """
    Lê BRIEFING.md. Aceita três formatos:
    1. Pure YAML (.yaml ou .md sem markdown wrapping)
    2. Markdown com YAML em ```yaml ... ``` (primeiro bloco)
    3. Markdown com YAML frontmatter (---...---)
    """
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end < 0:
            raise ValueError(f"{path}: frontmatter YAML aberto sem fechamento")
        return yaml.safe_load(text[3:end])
    m = re.search(r"```ya?ml\n(.*?)\n```", text, re.DOTALL)
    if m:
        return yaml.safe_load(m.group(1))
    return yaml.safe_load(text)


# =============================================================================
# Render helpers
# =============================================================================

def short_date(date_label: str) -> str:
    """'18/05/2026' → '18/05/26'."""
    if not date_label or len(date_label) < 8:
        return date_label or ""
    return date_label[:6] + date_label[-2:]


def render_shell_h1(parts: list) -> str:
    """<h1>Texto<span class="accent">destaque</span>...</h1>"""
    out = []
    for p in parts:
        t = p["text"]
        if p.get("accent"):
            out.append(f'<span class="accent">{escape(t.strip())}</span>')
            # Preserva espaçamento original ao redor do accent
            if t.startswith(" "):
                out[-1] = " " + out[-1]
            if t.endswith(" "):
                out[-1] = out[-1] + " "
        else:
            out.append(escape(t))
    return f'<h1>{"".join(out)}</h1>'


def render_cover_title(parts: list) -> str:
    """<h1 class="cover-title">Texto<br><em>destaque</em>...</h1>

    Heurística de quebra: se a primeira parte é palavra curta (≤12 chars sem
    espaços trailing) e não tem break_before declarado nas seguintes, força
    <br> antes da segunda parte (handoff §4.2). Strip espaço ao redor do <br>.
    """
    out: list = []
    first_text_trim = (parts[0]["text"] or "").strip()
    auto_break = (
        len(first_text_trim) <= 12
        and len(parts) > 1
        and not any(pt.get("break_before") for pt in parts[1:])
    )

    for i, p in enumerate(parts):
        break_here = (p.get("break_before") and i > 0) or (auto_break and i == 1)
        if break_here:
            if out:
                out[-1] = out[-1].rstrip()
            out.append("<br>")

        t = p["text"]
        if break_here and t.startswith(" "):
            t = t.lstrip()

        if p.get("accent"):
            stripped = t.strip()
            chunk = f"<em>{escape(stripped)}</em>"
            if t.startswith(" "):
                chunk = " " + chunk
            if t.endswith(" "):
                chunk = chunk + " "
            out.append(chunk)
        else:
            out.append(escape(t))

    return f'<h1 class="cover-title">{"".join(out)}</h1>'


def render_tabs(siblings: list) -> str:
    if not siblings:
        return '<div class="tabs"></div>'
    parts = ['<div class="tabs">']
    for s in siblings:
        label = escape(s["label"])
        badge = f' <span class="num">{escape(s["badge"])}</span>' if s.get("badge") else ""
        if s.get("active"):
            parts.append(f'<div class="tab" data-active="true">{label}{badge}</div>')
        else:
            href = escape(s["href"], quote=True)
            parts.append(f'<a class="tab" href="{href}">{label}{badge}</a>')
    parts.append("</div>")
    return "\n        ".join(parts)


def render_side_toc(toc: list) -> str:
    rows = ['<nav class="side-toc" id="side-toc">']
    for item in toc:
        pg = str(item["page"]).zfill(2)
        label = escape(item["label"])
        rows.append(
            f'      <button class="item" data-target="{item["page"]}" '
            f'type="button"><span class="pgnum">{pg}</span>'
            f'<span class="lbl">{label}</span></button>'
        )
    rows.append("    </nav>")
    return "\n".join(rows)


def render_formal_toc(toc: list) -> str:
    """Sumário da página 2: itens com `section` ou `subsection: true`."""
    rows = ['<div class="toc">']
    for item in toc:
        if item.get("section"):
            m = re.match(r"^(\d+)\.\s*(.*)$", item["section"])
            if m:
                num, name = m.groups()
            else:
                num, name = "?", item["section"]
            rows.append(
                f'<div class="toc-item"><span class="num">{escape(num)}</span>'
                f'<span class="label">{escape(name)}</span>'
                f'<span class="pg">p. {item["page"]}</span></div>'
            )
        elif item.get("subsection"):
            label = item["label"]
            m = re.match(r"^([\d.]+)\s*[·\-]?\s*(.*)$", label)
            if m:
                num, name = m.groups()
            else:
                num, name = "", label
            rows.append(
                f'<div class="toc-item h2"><span class="num">{escape(num)}</span>'
                f'<span class="label">{escape(name)}</span>'
                f'<span class="pg">p. {item["page"]}</span></div>'
            )
    rows.append("</div>")
    return "\n        ".join(rows)


def render_side_meta(data: dict) -> str:
    i = data["identity"]
    l = data["lifecycle"]
    g = data["governance"]
    return (
        '<div class="side-meta">\n'
        f'      <div class="row"><span class="k">Código</span><span class="v">{escape(i["code"])}</span></div>\n'
        f'      <div class="row"><span class="k">Versão</span><span class="v">{escape(i.get("version_label", i["version"]))}</span></div>\n'
        f'      <div class="row"><span class="k">Próx. revisão</span><span class="v">{escape(l.get("nextReview_label", str(l.get("nextReview", ""))))}</span></div>\n'
        f'      <div class="row"><span class="k">Owner</span><span class="v">{escape(g["owner"])}</span></div>\n'
        "    </div>"
    )


def render_cover_grid(data: dict) -> str:
    i = data["identity"]
    l = data["lifecycle"]
    g = data["governance"]
    return (
        '<div class="cover-grid">\n'
        '          <div class="cell">\n'
        '            <div class="l">Versão</div>\n'
        f'            <div class="v mono">{escape(i.get("version_label", i["version"]))}</div>\n'
        '          </div>\n'
        '          <div class="cell">\n'
        '            <div class="l">Vigência</div>\n'
        f'            <div class="v">{escape(l.get("date_label", str(l.get("date", ""))))}</div>\n'
        '          </div>\n'
        '          <div class="cell">\n'
        '            <div class="l">Próxima revisão</div>\n'
        f'            <div class="v">{escape(l.get("nextReview_label", str(l.get("nextReview", ""))))}</div>\n'
        '          </div>\n'
        '          <div class="cell">\n'
        '            <div class="l">Responsável</div>\n'
        f'            <div class="v">{escape(g["owner"])}</div>\n'
        '          </div>\n'
        '        </div>'
    )


def render_kv_table(data: dict) -> str:
    i = data["identity"]
    l = data["lifecycle"]
    g = data["governance"]

    elaborado = g.get("elaboradoPor", "")
    if " · " in elaborado:
        first, rest = elaborado.split(" · ", 1)
        elab_html = f"<strong>{escape(first)}</strong> · {escape(rest)}"
    else:
        elab_html = f"<strong>{escape(elaborado)}</strong>"

    parent = g.get("parent")
    if isinstance(parent, dict):
        p_html = f'<span class="mono">{escape(parent["code"])}</span> · {escape(parent.get("title", ""))}'
    else:
        p_html = "—"

    rows = [
        ("Código", f'<span class="mono">{escape(i["code"])}</span>'),
        ("Versão", f'<span class="mono">{escape(i.get("version_label", i["version"]))}</span>'),
        ("Tipo", f'{escape(i.get("tipo_label", i["tipo"]))} <span class="mono">({escape(i["tipo"])})</span>'),
        ("Área", escape(i.get("area_label", i["area"]))),
        ("Data", escape(l.get("date_label", str(l.get("date", ""))))),
        ("Elaborado por", elab_html),
        ("Aprovado por", escape(g.get("aprovadoPor", ""))),
        ("Classificação", escape(i["classif"])),
        ("Revisão", escape(l["revisaoFreq"])),
        ("Documento superior", p_html),
    ]
    out = ['<table class="kv-table">', "        <tbody>"]
    for k, v in rows:
        out.append(f"          <tr><td>{k}</td><td>{v}</td></tr>")
    out.append("        </tbody>")
    out.append("      </table>")
    return "\n".join(out)


# =============================================================================
# HTML substitution (anchors)
# =============================================================================

def sub_once(html: str, pattern: str, replacement: str, anchor_name: str, count: int = 1) -> str:
    """Substituição regex com erro claro se não casar.

    Replacement é tratado como string literal — backslashes não são interpretados
    como backrefs. Para incluir grupos capturados, recapture-os por regex no
    próprio replacement template (não suportado neste helper — reescreva o
    pattern para englobar o contexto completo)."""
    new_html, n = re.subn(
        pattern,
        lambda m: replacement,
        html,
        count=count,
        flags=re.DOTALL,
    )
    if n == 0:
        raise RuntimeError(f"Anchor não encontrado: {anchor_name}\n  pattern: {pattern[:80]}...")
    return new_html


def apply_all_substitutions(html: str, data: dict) -> str:
    i = data["identity"]
    l = data["lifecycle"]
    g = data["governance"]
    p = data["presentation"]
    s = data.get("structure", {}) or {}
    links = data.get("links", {}) or {}

    code = i["code"]
    version = i["version"]
    version_label = i.get("version_label", version)
    date_label = l.get("date_label", str(l.get("date", "")))
    next_label = l.get("nextReview_label", str(l.get("nextReview", "")))
    short_d = short_date(date_label)
    short_n = short_date(next_label)
    title_short = p["title_short"]
    tipo_label = i.get("tipo_label", i["tipo"])
    area_label = i.get("area_label", i["area"])
    classif_label = i.get("classif_label", f"Uso interno · {i['classif']}")
    eyebrow_cat = p.get("eyebrow_categoria", "Documento de governança")
    section_label = p.get("page_label_section", area_label)

    # 1. <title>
    html = sub_once(
        html,
        r"<title>[^<]*</title>",
        f"<title>{escape(title_short)} — M7 Investimentos</title>",
        "title.head",
    )

    # 2. Shell header — doc-meta block (reconstrói o bloco inteiro)
    html = sub_once(
        html,
        r'<div class="doc-meta">\s*<img[^>]*alt="M7 Investimentos">\s*<div class="meta">\s*<span>[^<]*</span>\s*<span class="dot"></span>\s*<span>[^<]*</span>\s*<span class="dot"></span>\s*<span>[^<]*</span>\s*</div>\s*</div>',
        (
            '<div class="doc-meta">\n'
            '      <img src="assets/m7-logo-offwhite.png" alt="M7 Investimentos">\n'
            '      <div class="meta">\n'
            f'        <span>{escape(section_label)}</span><span class="dot"></span>\n'
            f'        <span>{escape(tipo_label)} · {escape(code)}</span><span class="dot"></span>\n'
            f'        <span>{escape(date_label)}</span>\n'
            '      </div>\n'
            '    </div>'
        ),
        "shell.meta",
    )

    # 3. Shell h1
    html = sub_once(
        html,
        r"<h1>[^<]*<span class=\"accent\">[^<]*</span>[^<]*</h1>|<h1>[^<]*</h1>(?=\s*<p class=\"lede\">)",
        render_shell_h1(p["title_full"]["parts"]),
        "shell.h1",
    )

    # 4. Shell lede
    html = sub_once(
        html,
        r'<p class="lede">[^<]*</p>',
        f'<p class="lede">{escape(p["lede"])}</p>',
        "shell.lede",
    )

    # 5. Shell strip cells
    html = sub_once(
        html,
        r'<div class="strip">.*?</div>\s*</div>\s*<div class="tabs">',
        (
            f'<div class="strip">\n'
            f'          <div class="cell"><div class="v">{escape(version)}</div><div class="l">Versão</div></div>\n'
            f'          <div class="cell"><div class="v">{i["pages"]}</div><div class="l">Páginas</div></div>\n'
            f'          <div class="cell"><div class="v">{escape(short_d)}</div><div class="l">Vigência</div></div>\n'
            f'          <div class="cell"><div class="v">{escape(short_n)}</div><div class="l">Próx. revisão</div></div>\n'
            f'        </div>\n      </div>\n      <div class="tabs">'
        ),
        "shell.strip",
    )

    # 6. Tabs
    siblings = links.get("siblings") or []
    if siblings:
        html = sub_once(
            html,
            r'<div class="tabs">.*?</div>\s*</div>\s*</div>\s*</header>',
            render_tabs(siblings) + "\n    </div>\n  </div>\n</header>",
            "shell.tabs",
        )

    # 7. Side TOC
    toc = s.get("toc") or []
    if toc:
        html = sub_once(
            html,
            r'<nav class="side-toc" id="side-toc">.*?</nav>',
            render_side_toc(toc),
            "side-toc",
        )

    # 8. Side meta
    html = sub_once(
        html,
        r'<div class="side-meta">.*?</div>\s*</aside>',
        render_side_meta(data) + "\n  </aside>",
        "side-meta",
    )

    # 9. Cover meta (cover-head) — reconstrói o bloco inteiro
    html = sub_once(
        html,
        r'<div class="cover-meta">\s*<img[^>]*alt="M7 Investimentos">\s*<div class="meta">\s*<span>[^<]*</span>\s*<span class="dot"></span>\s*<span class="hl">[^<]*</span>\s*<span class="dot"></span>\s*<span>[^<]*</span>\s*</div>\s*</div>',
        (
            '<div class="cover-meta">\n'
            '        <img src="assets/m7-logo-offwhite.png" alt="M7 Investimentos">\n'
            '        <div class="meta">\n'
            f'          <span>{escape(section_label)}</span><span class="dot"></span>\n'
            f'          <span class="hl">{escape(tipo_label)} · {escape(i["tipo"])}</span><span class="dot"></span>\n'
            f'          <span>{escape(date_label)}</span>\n'
            '        </div>\n'
            '      </div>'
        ),
        "cover.meta",
    )

    # 10. Cover eyebrow
    html = sub_once(
        html,
        r'<div class="cover-eyebrow">.*?</div>',
        (
            f'<div class="cover-eyebrow">\n'
            f"          <span>{escape(eyebrow_cat)}</span>\n"
            f'          <span>·</span>\n'
            f'          <span class="v">{escape(code)}</span>\n'
            f"        </div>"
        ),
        "cover.eyebrow",
    )

    # 11. Cover title
    html = sub_once(
        html,
        r'<h1 class="cover-title">.*?</h1>',
        render_cover_title(p["title_full"]["parts"]),
        "cover.title",
    )

    # 12. Cover subtitle
    html = sub_once(
        html,
        r'<p class="cover-subtitle">[^<]*</p>',
        f'<p class="cover-subtitle">{escape(p["subtitle"])}</p>',
        "cover.subtitle",
    )

    # 13. Cover grid
    html = sub_once(
        html,
        r'<div class="cover-grid">.*?</div>\s*</div>\s*<div class="cover-foot">',
        render_cover_grid(data) + "\n      </div>\n\n      <div class=\"cover-foot\">",
        "cover.grid",
    )

    # 14. Cover foot
    html = sub_once(
        html,
        r'<div class="cover-foot">\s*<span class="conf">[^<]*</span>\s*<span>[^<]*</span>\s*</div>',
        (
            f'<div class="cover-foot">\n'
            f'        <span class="conf">{escape(classif_label)}</span>\n'
            f'        <span>M7 Investimentos · {escape(code)} · {escape(version)}</span>\n'
            f"      </div>"
        ),
        "cover.foot",
    )

    # 15. KV-table (página 2)
    html = sub_once(
        html,
        r'<table class="kv-table">.*?</table>',
        render_kv_table(data),
        "controle.kv-table",
    )

    # 16. section-lede da página 2 (referencia o código)
    html = sub_once(
        html,
        r'<p class="section-lede">Identificação canônica do documento\. Toda referência cruzada usa o código <span class="mono">[^<]*</span>\.</p>',
        f'<p class="section-lede">Identificação canônica do documento. Toda referência cruzada usa o código <span class="mono">{escape(code)}</span>.</p>',
        "controle.section-lede",
    )

    # 17. Sumário formal (página 2)
    if toc:
        html = sub_once(
            html,
            r'<div class="toc">.*?</div>\s*</div>\s*<footer class="page-foot">',
            render_formal_toc(toc) + "\n    </div>\n\n    <footer class=\"page-foot\">",
            "controle.toc",
        )

    # 18. ph-title (×N páginas) — todas as ocorrências
    html = re.sub(
        r'<span class="ph-title">[^<]*</span>',
        f'<span class="ph-title">{escape(title_short)}</span>',
        html,
    )

    # 19. ph-meta (×N páginas) — código · versão
    html = re.sub(
        r'<span class="ph-meta">[^<]*</span>',
        f'<span class="ph-meta">{escape(code)} · {escape(version)}</span>',
        html,
    )

    # 20. pf-classif (×N páginas)
    html = re.sub(
        r'<span class="pf-classif">[^<]*</span>',
        f'<span class="pf-classif">{escape(classif_label)}</span>',
        html,
    )

    # 21. total-pg (×N) e #total-pages — JS atualiza em runtime; ainda assim
    # fixamos no static para PDFs gerados antes do JS rodar
    pages_n = str(i["pages"])
    html = re.sub(
        r'<span class="total-pg">[^<]*</span>',
        f'<span class="total-pg">{pages_n}</span>',
        html,
    )
    html = re.sub(
        r'<span id="total-pages">[^<]*</span>',
        f'<span id="total-pages">{pages_n}</span>',
        html,
    )

    return html


# =============================================================================
# Final validation pass
# =============================================================================

def assert_no_residual_pol_gov_002(html: str, data: dict) -> list:
    """Detecta resíduos do exemplo POL-GOV-002 que indicariam que algum anchor
    não foi substituído (exceto se o próprio doc gerado FOR POL-GOV-002)."""
    if data["identity"]["code"] == "POL-GOV-002":
        return []
    issues = []
    if "POL-GOV-002" in html:
        issues.append("Resíduo 'POL-GOV-002' no HTML — algum anchor não foi substituído")
    return issues


# =============================================================================
# Main
# =============================================================================

def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--briefing", required=True, help="Path para BRIEFING-{CODE}.md")
    parser.add_argument("--output-dir", required=True, help="Diretório de saída")
    parser.add_argument("--content", help="(Opcional) MD com conteúdo das 8 seções")
    parser.add_argument("--basename", help="Basename dos outputs (default: slug do código)")
    parser.add_argument("--template", help="HTML template (default: assets/politica-m7-template.html)")
    parser.add_argument("--schema-info", action="store_true", help="Imprime resumo do schema e sai")
    parser.add_argument("--validate-only", action="store_true", help="Só valida YAML, não gera HTML")
    args = parser.parse_args()

    if args.schema_info:
        print("Schema: normativo.schema.yaml v1.0")
        print(f"  tipo:       {sorted(ALLOWED_TIPO)}")
        print(f"  area:       {sorted(ALLOWED_AREA)}")
        print(f"  status:     {sorted(ALLOWED_STATUS)}")
        print(f"  classif:    {sorted(ALLOWED_CLASSIF)}")
        print(f"  revisaoFreq:{sorted(ALLOWED_REVISAO)}")
        return 0

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent

    template_path = Path(args.template) if args.template else skill_dir / "assets" / "politica-m7-template.html"
    if not template_path.exists():
        sys.stderr.write(f"ERRO: template não encontrado: {template_path}\n")
        return 2

    briefing_path = Path(args.briefing)
    if not briefing_path.exists():
        sys.stderr.write(f"ERRO: briefing não encontrado: {briefing_path}\n")
        return 2

    # Parse + validate
    try:
        data = parse_briefing(briefing_path)
    except Exception as e:
        sys.stderr.write(f"ERRO ao parsear briefing: {e}\n")
        return 2

    errs = validate(data)
    if errs:
        sys.stderr.write("VALIDAÇÃO DE SCHEMA FALHOU:\n")
        for e in errs:
            sys.stderr.write(e + "\n")
        return 1

    if args.validate_only:
        print("✓ YAML valida contra o schema")
        return 0

    # Output paths
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    basename = args.basename or slugify(data["identity"]["code"])
    yaml_out = output_dir / f"{basename}.yaml"
    html_out = output_dir / f"{basename}.html"

    # YAML
    yaml_out.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120),
        encoding="utf-8",
    )

    # HTML
    html = template_path.read_text(encoding="utf-8")
    try:
        html = apply_all_substitutions(html, data)
    except RuntimeError as e:
        sys.stderr.write(f"ERRO na substituição: {e}\n")
        return 3

    residuals = assert_no_residual_pol_gov_002(html, data)
    if residuals:
        sys.stderr.write("AVISOS:\n")
        for r in residuals:
            sys.stderr.write(f"  · {r}\n")

    if args.content:
        sys.stderr.write(
            "AVISO: --content ainda não implementa injeção de conteúdo de seções.\n"
            "       O HTML gerado preserva o conteúdo do template. Edite manualmente\n"
            "       as páginas 3-15 do HTML, OU aguarde a próxima iteração da skill.\n"
        )

    html_out.write_text(html, encoding="utf-8")

    print(f"✓ Gerado:")
    print(f"   {yaml_out}")
    print(f"   {html_out}")
    if residuals:
        print(f"⚠  {len(residuals)} aviso(s) — veja stderr")
    return 0


if __name__ == "__main__":
    sys.exit(main())
