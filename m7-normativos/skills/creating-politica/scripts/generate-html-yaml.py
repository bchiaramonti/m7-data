#!/usr/bin/env python3
"""
generate-html-yaml.py — Pipeline da Fase 3 de creating-politica (v4.0).

Estratégia: o template oficial `politica-m7-template.html` (versão isolada)
tem 145 placeholders `{{...}}` explícitos. O script:

1. Parseia BRIEFING.md (YAML) e valida contra normativo.schema.yaml
2. Opcionalmente parseia politica-{slug}.md — valida MD (sem <style>, sem
   style="...", sem classes ad-hoc), expande shortcodes (:::papel-card,
   :::callout, etc) e extrai conteúdo das 8 seções
3. Constrói dicionário de 145 placeholders → valores
4. INLINEIA CSS + fonts (base64) + logos (base64) no HTML — output autocontido
5. Substitui todos os placeholders via str.replace
6. Valida zero placeholders residuais, zero paths relativos, e zero classes
   CSS fora da allowlist do component-catalog.md
7. Escreve trio {slug}.html + {slug}.yaml + {slug}.review.md (stub)

A v4.0 introduz **separação rígida entre conteúdo (MD canônico) e
apresentação (template + shortcodes catalogados)**:

- MD da Fase 2 aceita SOMENTE markdown padrão + shortcodes do catálogo
  (component-catalog.md). HTML inline com classes ou <style> é rejeitado.
- O HTML final tem allowlist de classes CSS — qualquer classe fora dela
  aborta a geração.
- O .review.md gerado é STUB; a skill orquestradora deve invocar o agente
  `politica-design-reviewer` para preencher com o relatório real (gate
  obrigatório Score >= B antes da entrega).

CLI:
    python generate-html-yaml.py \\
        --briefing  BRIEFING-POL-GOV-003.md \\
        --output-dir <dir> \\
        [--content politica-foo.md] \\
        [--basename politica-foo] \\
        [--template <path>] \\
        [--validate-only] \\
        [--no-inline]
"""
import argparse
import base64
import re
import sys
from html import escape
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("ERRO: pyyaml não instalado. Rode: pip install pyyaml\n")
    sys.exit(2)


# =============================================================================
# Schema validation (custom — schema usa keywords não-JSON-Schema)
# =============================================================================

ALLOWED_TIPO = {"POL", "MAN", "INS", "ESP"}
ALLOWED_AREA = {"GOV", "PERF", "INV", "CRE", "SEG", "UNI", "TEC", "PES"}
ALLOWED_STATUS = {"vigente", "revisao", "rascunho", "pendente", "vencido"}
ALLOWED_CLASSIF = {"Público", "Interno", "Confidencial", "Restrito"}
ALLOWED_REVISAO = {"Anual", "Semestral", "Trimestral", "Mensal", "Sob demanda"}
ALLOWED_ESCOPO = {"holding", "transversal", "processo"}

CODE_PATTERN = re.compile(r"^(POL|MAN|INS|ESP)-[A-Z]{2,4}-[0-9]{3}$")
VERSION_PATTERN = re.compile(r"^v?[0-9]+\.[0-9]+$")
PROC_PATTERN = re.compile(r"^(G[1-4]|P[1-9]|P1[0-2]|A[1-5])$")


# =============================================================================
# Shortcodes do Catálogo (component-catalog.md) e Allowlist de classes CSS
# =============================================================================
#
# Princípio: o MD da Fase 2 é canônico de conteúdo. Toda apresentação visual
# vem de classes CSS já declaradas no template. Quando o autor precisa de um
# bloco visual especial, usa um shortcode `:::nome ... :::` listado abaixo.
#
# Para adicionar shortcode novo: ver "Como adicionar um shortcode novo" em
# references/component-catalog.md. Não adicionar ad-hoc neste script.

SHORTCODE_CATALOG = {
    "papel-card",
    "papel-card-separador",
    "callout",
    "callout-info",
    "callout-alerta",
    "callout-exemplo",
    "indicador",
    "diagrama",
    "processo-grid",
}

# Classes CSS permitidas no HTML final. Validação pós-render rejeita qualquer
# classe fora desta allowlist. Mantenha sincronizado com component-catalog.md.
#
# Reflete as classes que o template oficial `politica-m7-template.html`
# emite + classes adicionadas pelos shortcodes.
CSS_ALLOWLIST = {
    # Documento e shell
    "doc", "shell-main", "toolbar", "export", "navbtn",
    # Página A4
    "page", "page-head", "page-body", "page-foot",
    "ph-left", "ph-sep", "ph-title", "ph-meta",
    "pf-classif", "pf-page",
    # Capa
    "cover", "cover-head", "cover-body", "cover-foot",
    "cover-eyebrow", "cover-grid", "cover-meta",
    "cover-title", "cover-subtitle",
    # Seção
    "section", "section-lede", "section-title",
    "section-eyebrow", "section-num",
    # Tipografia auxiliar
    "sub", "subsub", "muted", "muted-empty",
    "chip", "mono", "tag", "hl",
    "twocol", "label", "meta", "divider", "dot", "sep",
    "v", "l", "num", "counter", "pg", "conf",
    # Tabelas estruturadas
    "kv-table", "doc-table", "cell",
    # Princípios
    "principles", "principle", "principle-card", "principle-row",
    "pn", "pt", "pd",
    # Aprovações / role
    "approval-card", "approval-grid", "role", "sig-line",
    # Sumário (TOC)
    "toc", "toc-item", "toc-num", "toc-title", "toc-page",
    "total-pg",
    # Conteúdo: what/who/where (cards de identidade)
    "what", "who",
    # Tipografia (m7-tokens.css)
    "text-display-1", "text-display-2",
    "text-h1", "text-h2", "text-h3", "text-h4",
    "text-body-1", "text-body-2", "text-body-3",
    "text-button", "text-label", "text-muted", "text-mono",
    "wcag-pass", "wcag-fail", "wcag-marg",
    # Nav/Layout (m7-tokens.css)
    "m7-nav", "m7-nav-inner", "m7-nav-logo", "m7-nav-links",
    "ds-tag",
    "m7-foot", "m7-foot-inner",
    "container", "stack", "row", "grid", "active",
    # Shortcode: papel-card (.inv-*)
    "inv-card", "inv-title", "inv-owner", "inv-block",
    "inv-sep", "inv-sep-title", "inv-sep-desc",
    # Shortcode: callout
    "callout", "callout-title", "callout-tag",
    "callout-alerta", "callout-exemplo",
    # Shortcode: indicador
    "indicador-card", "indicador-nome", "indicador-meta",
    # Shortcode: diagrama (.embed-svg)
    "embed-svg", "embed-svg-caption",
    # Shortcode: processo-grid (.skill-proc-*)
    "skill-proc-block", "skill-proc-card",
    "skill-proc-title", "skill-proc-owner",
    "skill-camada-sep", "skill-camada-title",
}


def _err(path: str, msg: str) -> str:
    return f"  · {path}: {msg}"


def normalize_governance(data: dict) -> None:
    """Auto-deriva governance.escopo quando ausente. Muta `data` in-place.

    Regras (vide handoff §3.6):
      - 0 ou 1 processo → "processo"
      - múltiplos       → "transversal"
      - "holding" NUNCA é auto-derivado — exige declaração explícita
        (proteção contra docs que cobrem P1-P12 mas são semanticamente
        transversais e não holding).
    """
    g = data.get("governance")
    if not isinstance(g, dict) or "escopo" in g:
        return
    procs = g.get("processos") or []
    g["escopo"] = "processo" if len(procs) <= 1 else "transversal"


def validate(data: dict) -> list:
    errs: list = []
    if data.get("schema_version") != "1.0":
        errs.append(_err("schema_version", "deve ser '1.0'"))

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

    g = data.get("governance") or {}
    if not isinstance(g, dict):
        errs.append(_err("governance", "objeto obrigatório"))
    else:
        for f in ("owner", "parent", "processos", "escopo"):
            if f not in g:
                errs.append(_err(f"governance.{f}", "obrigatório"))
        parent = g.get("parent")
        if isinstance(parent, dict) and not CODE_PATTERN.match(parent.get("code", "")):
            errs.append(_err("governance.parent.code", f"deve casar {CODE_PATTERN.pattern}"))
        procs = g.get("processos") or []
        if not isinstance(procs, list):
            errs.append(_err("governance.processos", "deve ser lista"))
        else:
            for p in procs:
                if not PROC_PATTERN.match(str(p)):
                    errs.append(_err("governance.processos", f"item inválido: {p}"))
        if "escopo" in g and g["escopo"] not in ALLOWED_ESCOPO:
            errs.append(_err("governance.escopo", f"deve ser um de {sorted(ALLOWED_ESCOPO)}"))

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
# Shortcode parser + validador de MD (v4.0)
# =============================================================================

SHORTCODE_OPEN_RE = re.compile(r"^:::([a-z][a-z0-9-]*)\s*$", re.MULTILINE)
SHORTCODE_BLOCK_RE = re.compile(
    r"^:::([a-z][a-z0-9-]*)\s*\n(.*?)^:::\s*$",
    re.MULTILINE | re.DOTALL,
)


def _parse_shortcode_attrs(body_text: str) -> tuple:
    """Separa attrs `chave: valor` no topo do shortcode do corpo livre.

    Convenção: attrs vão no topo, uma por linha, formato `chave: valor`.
    A primeira linha em branco encerra a seção de attrs. Aceita chaves
    com acento (título, descrição, fórmula, frequência) — normaliza para
    sem acento internamente.
    """
    attrs: dict = {}
    body_lines: list = []
    body_started = False
    lines = body_text.split("\n")

    for line in lines:
        if body_started:
            body_lines.append(line)
            continue
        stripped = line.strip()
        if not stripped:
            body_started = True
            continue
        # Heurística: linha começa com letra minúscula/acento, tem ':', primeiro
        # token sem espaços. Senão, é início do corpo livre.
        m = re.match(r"^([a-zçãéíóúâêô-]+):\s*(.+)$", stripped, re.IGNORECASE)
        if m and not stripped.startswith(("-", "*", "#", "|", "<", ">")):
            key = _norm_attr_key(m.group(1))
            attrs[key] = m.group(2).strip()
        else:
            body_started = True
            body_lines.append(line)

    # Remove trailing empty lines do corpo
    while body_lines and not body_lines[-1].strip():
        body_lines.pop()
    return attrs, "\n".join(body_lines).strip()


def _norm_attr_key(key: str) -> str:
    """Normaliza chave de attr: lowercase + sem acento + sem espaço."""
    key = key.lower().strip()
    repl = {
        "á": "a", "â": "a", "ã": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "ô": "o", "õ": "o",
        "ú": "u",
        "ç": "c",
    }
    for src, dst in repl.items():
        key = key.replace(src, dst)
    return key


def _attr(attrs: dict, *keys: str, default: str = "") -> str:
    """Lookup multi-chave (aceita variações com/sem acento)."""
    for k in keys:
        if k in attrs:
            return attrs[k]
        nk = _norm_attr_key(k)
        if nk in attrs:
            return attrs[nk]
    return default


def render_shortcode(name: str, attrs: dict, body: str) -> str:
    """Converte um shortcode parseado em HTML usando classes da allowlist."""

    if name == "papel-card":
        titulo = escape(_attr(attrs, "titulo", "título"))
        owner = escape(_attr(attrs, "owner", "responsavel", "responsável"))
        body_html = markdown_to_html(body) if body.strip() else ""
        # Cada <p> do corpo vira <p class="inv-block">
        body_html = re.sub(r"<p>", '<p class="inv-block">', body_html)
        owner_html = f'\n  <p class="inv-owner">Owner: {owner}</p>' if owner else ""
        return (
            '<div class="inv-card">\n'
            f'  <h4 class="inv-title">{titulo}</h4>{owner_html}\n'
            f'  {body_html}\n'
            '</div>'
        )

    if name == "papel-card-separador":
        titulo = escape(_attr(attrs, "titulo", "título"))
        descricao = escape(_attr(attrs, "descricao", "descrição"))
        desc_html = f'\n  <p class="inv-sep-desc">{descricao}</p>' if descricao else ""
        return (
            '<div class="inv-sep">\n'
            f'  <h4 class="inv-sep-title">{titulo}</h4>{desc_html}\n'
            '</div>'
        )

    if name in {"callout", "callout-info", "callout-alerta", "callout-exemplo"}:
        variant_class = ""
        if name == "callout-alerta":
            variant_class = " callout-alerta"
        elif name == "callout-exemplo":
            variant_class = " callout-exemplo"
        tag = escape(_attr(attrs, "tag"))
        titulo = escape(_attr(attrs, "titulo", "título"))
        title_inner = ""
        if tag:
            title_inner += f'<span class="callout-tag">{tag}</span>'
        if titulo:
            title_inner += titulo
        title_html = (
            f'\n  <span class="callout-title">{title_inner}</span>'
            if title_inner else ""
        )
        body_html = markdown_to_html(body) if body.strip() else ""
        return (
            f'<div class="callout{variant_class}">{title_html}\n'
            f'  {body_html}\n'
            '</div>'
        )

    if name == "indicador":
        nome = escape(_attr(attrs, "nome"))
        formula = escape(_attr(attrs, "formula", "fórmula"))
        freq = escape(_attr(attrs, "frequencia", "frequência"))
        meta = escape(_attr(attrs, "meta"))
        meta_items = []
        if formula:
            meta_items.append(f"    <dt>Fórmula:</dt><dd>{formula}</dd>")
        if freq:
            meta_items.append(f"    <dt>Frequência:</dt><dd>{freq}</dd>")
        if meta:
            meta_items.append(f"    <dt>Meta:</dt><dd>{meta}</dd>")
        meta_html = "\n".join(meta_items)
        return (
            '<div class="indicador-card">\n'
            f'  <h4 class="indicador-nome">{nome}</h4>\n'
            '  <dl class="indicador-meta">\n'
            f'{meta_html}\n'
            '  </dl>\n'
            '</div>'
        )

    if name == "diagrama":
        caption = escape(_attr(attrs, "caption"))
        # Body aceita <svg>...</svg> OU <img src="...">
        # SVG é preservado intacto; img é preservado com seus atributos
        svg_match = re.search(r"<svg\b.*?</svg>", body, re.DOTALL | re.IGNORECASE)
        img_match = re.search(r'<img\b[^>]*?/?>', body, re.IGNORECASE)
        if svg_match:
            content = svg_match.group(0)
        elif img_match:
            content = img_match.group(0)
        else:
            content = body.strip()
        caption_html = (
            f'\n<p class="embed-svg-caption">{caption}</p>'
            if caption else ""
        )
        return (
            '<div class="embed-svg">\n'
            f'  {content}\n'
            f'</div>{caption_html}'
        )

    if name == "processo-grid":
        camada = escape(_attr(attrs, "camada"))
        descricao = escape(_attr(attrs, "descricao", "descrição"))
        cards: list = []
        for line in body.split("\n"):
            m = re.match(r"^\s*[-*]\s+(.+?)\s*\|\s*(.+)$", line)
            if m:
                titulo = escape(m.group(1).strip())
                owner = escape(m.group(2).strip())
                cards.append(
                    '  <div class="skill-proc-card">\n'
                    f'    <h4 class="skill-proc-title">{titulo}</h4>\n'
                    f'    <p class="skill-proc-owner">{owner}</p>\n'
                    '  </div>'
                )
        cards_html = "\n".join(cards)
        sep_html = ""
        if camada:
            desc_html = f'\n  <p>{descricao}</p>' if descricao else ""
            sep_html = (
                '<div class="skill-camada-sep">\n'
                f'  <h4 class="skill-camada-title">{camada}</h4>{desc_html}\n'
                '</div>\n'
            )
        return f'{sep_html}<div class="skill-proc-block">\n{cards_html}\n</div>'

    # Fallback: shortcode desconhecido (não deveria chegar aqui — validação
    # roda antes da expansão).
    return f"<!-- unknown shortcode: {escape(name)} -->"


# Armazenamento global temporário dos blocos HTML expandidos a partir de
# shortcodes. Usado por expand_shortcodes/restore_shortcodes para fazer
# stash similar ao SVG — protege o HTML do shortcode contra a python-markdown
# (que envolveria em <p> se visse o <div> no meio de texto). Reset a cada
# `parse_content_md` para evitar vazamento entre execuções.
_SC_BLOCKS: list = []


def expand_shortcodes(text: str) -> str:
    """Substitui blocos `:::nome\\n...\\n:::` por placeholders únicos.

    Os HTMLs renderizados ficam armazenados em `_SC_BLOCKS`; o texto retornado
    tem `@@SC_BLOCK_N@@` no lugar de cada shortcode. Após `markdown_to_html`
    processar o texto, `restore_shortcodes(html)` substitui de volta.

    Esse padrão (idêntico ao usado para SVG inline) evita que a python-markdown
    serialize o HTML do shortcode como prosa.
    """
    _SC_BLOCKS.clear()

    def repl(m: "re.Match") -> str:
        name = m.group(1).strip()
        body_text = m.group(2)
        attrs, body = _parse_shortcode_attrs(body_text)
        rendered = render_shortcode(name, attrs, body)
        _SC_BLOCKS.append(rendered)
        # Isolado por \n\n para que o placeholder fique em parágrafo próprio
        return f"\n\n@@SC_BLOCK_{len(_SC_BLOCKS) - 1}@@\n\n"

    return SHORTCODE_BLOCK_RE.sub(repl, text)


def restore_shortcodes(html: str) -> str:
    """Substitui placeholders `@@SC_BLOCK_N@@` pelos HTMLs originais.

    Remove o wrap `<p>...</p>` que a markdown lib adiciona em torno do
    placeholder (esperado: placeholder vira parágrafo solo após `\\n\\n`).
    """
    for i, block in enumerate(_SC_BLOCKS):
        placeholder = f"@@SC_BLOCK_{i}@@"
        html = html.replace(f"<p>{placeholder}</p>", block)
        html = html.replace(placeholder, block)
    return html


def validate_md_content(md_text: str, md_path: Path) -> list:
    """Valida o MD da Fase 2 (creating-politica v4.0).

    Bloqueia:
      - <style>...</style>           (design vem do template, não do MD)
      - style="..." inline           (idem)
      - <svg>...</svg> fora de :::diagrama  (forçar shortcode)
      - <tag class="X"> com X fora da CSS_ALLOWLIST
      - :::nome ... ::: com nome fora de SHORTCODE_CATALOG
      - :::nome sem fechamento :::

    Não bloqueia:
      - Markdown padrão (h2, h3, listas, tabelas, **bold**, etc)
      - Comentários HTML (<!-- ... -->)
      - <br>, <hr>, <code> sem class
      - <!-- /page-break --> (marker convencional da Fase 2)
    """
    errs: list = []
    name = md_path.name

    # 1. <style>...</style> proibido
    for m in re.finditer(r"<style\b[^>]*>.*?</style>", md_text, re.DOTALL | re.IGNORECASE):
        line_no = md_text[:m.start()].count("\n") + 1
        snippet = re.sub(r"\s+", " ", m.group(0))[:80]
        errs.append(_err(
            f"{name}:linha {line_no}",
            f"<style> block proibido — design vem do template/shortcodes. "
            f"Trecho: '{snippet}…'"
        ))

    # 2. style="..." inline proibido
    for m in re.finditer(r'\bstyle\s*=\s*"[^"]*"', md_text, re.IGNORECASE):
        line_no = md_text[:m.start()].count("\n") + 1
        errs.append(_err(
            f"{name}:linha {line_no}",
            f"style=\"...\" inline proibido — use classe do component-catalog."
        ))

    # 3. Stash shortcodes válidos para não checar conteúdo deles na validação
    md_stripped = SHORTCODE_BLOCK_RE.sub("", md_text)

    # 4. <svg> só dentro de :::diagrama (no md_stripped já não tem)
    for m in re.finditer(r"<svg\b", md_stripped, re.IGNORECASE):
        line_no = md_stripped[:m.start()].count("\n") + 1
        errs.append(_err(
            f"{name}:linha {line_no}",
            "<svg> fora de shortcode :::diagrama. "
            "Envolva o SVG com :::diagrama ... :::"
        ))

    # 5. Classes em elementos HTML do MD fora da allowlist
    pattern = re.compile(
        r'<(div|span|p|section|article|figure|aside|table|tr|td|th|h[1-6]|ul|ol|li|dl|dt|dd|header|footer|nav|main|button|a)\b[^>]*\bclass\s*=\s*"([^"]+)"',
        re.IGNORECASE,
    )
    for m in pattern.finditer(md_stripped):
        tag = m.group(1).lower()
        classes_str = m.group(2)
        line_no = md_stripped[:m.start()].count("\n") + 1
        for cls in classes_str.split():
            if cls and cls not in CSS_ALLOWLIST:
                errs.append(_err(
                    f"{name}:linha {line_no}",
                    f"classe '{cls}' em <{tag}> fora da allowlist do "
                    f"component-catalog. Use shortcode (:::papel-card, "
                    f":::callout, :::indicador, :::diagrama, :::processo-grid) "
                    f"ou markdown padrão."
                ))

    # 6. Shortcodes inválidos ou sem fechamento
    open_names = [(m.group(1), m.start()) for m in SHORTCODE_OPEN_RE.finditer(md_text)]
    closed_set = set()
    for m in SHORTCODE_BLOCK_RE.finditer(md_text):
        closed_set.add(m.start())

    # Reconstrói posições de abertura que tiveram fechamento
    closed_opens: set = set()
    for m in SHORTCODE_BLOCK_RE.finditer(md_text):
        closed_opens.add(m.start())

    for name_sc, pos in open_names:
        # É fechamento? `:::` puro também casa o regex de abertura (group 1 vazio)
        if not name_sc:
            continue
        line_no = md_text[:pos].count("\n") + 1
        if name_sc not in SHORTCODE_CATALOG:
            errs.append(_err(
                f"{name}:linha {line_no}",
                f"shortcode ':::{name_sc}' inválido. "
                f"Allowlist: {sorted(SHORTCODE_CATALOG)}"
            ))
        if pos not in closed_opens:
            errs.append(_err(
                f"{name}:linha {line_no}",
                f"shortcode ':::{name_sc}' aberto sem fechamento ':::'."
            ))

    return errs


def validate_html_classes(html: str) -> list:
    """Valida que todas as classes CSS no HTML pertencem à CSS_ALLOWLIST.

    Roda APÓS substituição de placeholders e inline_assets — pega:
      - Hex literal CSS injetado por leak
      - Shortcode renderizado com classe não-catalogada
      - Classe ad-hoc no MD que escapou da validação prévia
    """
    errs: list = []
    bad_classes: dict = {}  # cls -> contagem
    for m in re.finditer(r'\bclass\s*=\s*"([^"]+)"', html):
        for cls in m.group(1).split():
            if not cls or cls in CSS_ALLOWLIST:
                continue
            bad_classes[cls] = bad_classes.get(cls, 0) + 1
    for cls, count in sorted(bad_classes.items()):
        errs.append(_err(
            "HTML output",
            f"classe '{cls}' (x{count}) fora da allowlist do component-catalog. "
            f"Provável causa: hex literal CSS injetado, shortcode mal renderizado, "
            f"ou classe ad-hoc no MD que escapou da validação."
        ))
    return errs


def validate_html_no_inline_styles(html: str, template_html: str = "") -> list:
    """Detecta `<style>` ou `style="..."` injetados além do baseline do template.

    Baseline esperado:
      - `<style>` blocks: 2 (1 do template + 1 do m7-tokens.css inlinado por
        `inline_assets`). Se template_html for fornecido, usa contagem real.
      - `style="..."` inline: conta no template (legítimos) e exige que o
        HTML final tenha exatamente a mesma quantidade.

    MD não pode introduzir nenhum dos dois — a validação prévia
    (`validate_md_content`) já garante isso. Esta função é defesa em
    profundidade contra leak via shortcode mal-renderizado ou edição
    direta do template.
    """
    errs: list = []

    expected_styles = 2  # default: 1 template + 1 css inlinado
    expected_inline = 12  # default conhecido do template atual
    if template_html:
        # Conta no template e adiciona 1 pelo inline_assets (m7-tokens.css)
        expected_styles = len(re.findall(
            r"<style\b[^>]*>.*?</style>", template_html, re.DOTALL | re.IGNORECASE
        )) + 1
        expected_inline = len(re.findall(
            r'\bstyle\s*=\s*"[^"]+"', template_html
        ))

    style_blocks = re.findall(r"<style\b[^>]*>.*?</style>", html, re.DOTALL | re.IGNORECASE)
    if len(style_blocks) > expected_styles:
        errs.append(_err(
            "HTML output",
            f"{len(style_blocks)} blocos <style> (esperado {expected_styles}: "
            f"template + m7-tokens.css). Blocos extras indicam CSS injetado "
            f"além do baseline."
        ))

    inline_styles = re.findall(r'\bstyle\s*=\s*"[^"]+"', html)
    if len(inline_styles) > expected_inline:
        diff = len(inline_styles) - expected_inline
        errs.append(_err(
            "HTML output",
            f"{len(inline_styles)} atributos style=\"...\" inline (esperado "
            f"{expected_inline} do template). {diff} adicionais sugerem leak."
        ))

    return errs


# =============================================================================
# Briefing & content MD parsers
# =============================================================================

def parse_briefing(path: Path) -> dict:
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


def split_by_h2(text: str) -> dict:
    """Quebra MD em {section_key: body} onde key é '1.', '2.', etc."""
    sections: dict = {}
    current_key = None
    current_body: list = []
    for line in text.split("\n"):
        m = re.match(r"^##\s+(\d+)\.\s", line)
        if m:
            if current_key is not None:
                sections[current_key] = "\n".join(current_body).strip()
            current_key = m.group(1) + "."
            current_body = []
        elif current_key is not None:
            current_body.append(line)
    if current_key is not None:
        sections[current_key] = "\n".join(current_body).strip()
    return sections


def extract_md_table(text: str) -> list:
    """Extrai linhas da primeira tabela markdown (skip header + separador)."""
    rows: list = []
    seen_header = False
    seen_separator = False
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not seen_header:
                seen_header = True
                continue
            if not seen_separator and all(re.match(r"^[\s\-:]*$", c) for c in cells):
                seen_separator = True
                continue
            if seen_separator:
                rows.append(cells)
        elif seen_header and seen_separator:
            break
    return rows


def extract_bullets(text: str) -> list:
    """Extrai itens '- foo' ou '* foo' de uma lista markdown."""
    return [m.group(1).strip() for m in re.finditer(r"^\s*[-*]\s+(.+?)$", text, re.MULTILINE)]


def parse_content_md(path: Path) -> dict:
    """Lê politica-{slug}.md e extrai valores para os placeholders de conteúdo.

    Em v4.0: o texto é validado (sem <style>, sem style="...", sem classes
    ad-hoc, sem <svg> solto) e tem shortcodes expandidos ANTES de qualquer
    parseamento de seções. Erros de validação são propagados via exceção
    para abortar a Fase 3 com mensagem clara.
    """
    text = path.read_text(encoding="utf-8")

    # v4.0 — validação prévia + expansão de shortcodes
    md_errs = validate_md_content(text, path)
    if md_errs:
        msg = "VALIDAÇÃO DO MD FALHOU:\n" + "\n".join(md_errs)
        raise ValueError(msg)
    text = expand_shortcodes(text)

    sections = split_by_h2(text)
    out: dict = {}

    # 1. Objetivo — 2 parágrafos
    body = sections.get("1.", "")
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    out["TEXTO_OBJETIVO_P1"] = paragraphs[0] if len(paragraphs) >= 1 else ""
    out["TEXTO_OBJETIVO_P2"] = paragraphs[1] if len(paragraphs) >= 2 else ""

    # 2. Escopo — lede + inclusões + exclusões
    body = sections.get("2.", "")
    lede_m = re.match(r"^(.+?)(?=\n\s*\*\*|\n\s*-\s)", body, re.DOTALL)
    out["LEDE_ESCOPO"] = lede_m.group(1).strip() if lede_m else (body.strip().split("\n\n")[0] if body else "")
    incl_block_m = re.search(
        r"(?:\*\*Aplica-se a[^*\n]*\*\*|###+\s+Aplica-se a[^\n]*)\s*\n((?:\s*[-*]\s+.+\n?)+)",
        body,
    )
    excl_block_m = re.search(
        r"(?:\*\*N[aã]o se aplica[^*\n]*\*\*|###+\s+N[aã]o se aplica[^\n]*)\s*\n((?:\s*[-*]\s+.+\n?)+)",
        body,
    )
    incl_items = extract_bullets(incl_block_m.group(1)) if incl_block_m else []
    excl_items = extract_bullets(excl_block_m.group(1)) if excl_block_m else []
    if not incl_items and not excl_items:
        all_bullets = extract_bullets(body)
        incl_items = all_bullets[:3]
        excl_items = all_bullets[3:6]
    for n in range(3):
        out[f"ESCOPO_INCLUSAO_{n+1}"] = incl_items[n] if n < len(incl_items) else ""
        out[f"ESCOPO_EXCLUSAO_{n+1}"] = excl_items[n] if n < len(excl_items) else ""

    # 3. Definições — tabela 2 col
    rows = extract_md_table(sections.get("3.", ""))
    for n in range(12):
        if n < len(rows) and len(rows[n]) >= 2:
            out[f"DEF_TERMO_{n+1}"] = rows[n][0]
            out[f"DEF_TEXTO_{n+1}"] = rows[n][1]
        else:
            out[f"DEF_TERMO_{n+1}"] = ""
            out[f"DEF_TEXTO_{n+1}"] = ""

    # 4. Princípios — lede + h3 com parágrafo
    body = sections.get("4.", "")
    h3_re = re.compile(r"^###\s+(.+?)$", re.MULTILINE)
    matches = list(h3_re.finditer(body))
    out["LEDE_PRINCIPIOS"] = (body[:matches[0].start()].strip() if matches else body.strip())
    for n in range(7):
        if n < len(matches):
            title = matches[n].group(1).strip()
            start = matches[n].end()
            end = matches[n + 1].start() if n + 1 < len(matches) else len(body)
            desc = body[start:end].strip()
            out[f"PRINCIPIO_{n+1}_TITULO"] = title
            out[f"PRINCIPIO_{n+1}_DESCRICAO"] = desc
        else:
            out[f"PRINCIPIO_{n+1}_TITULO"] = ""
            out[f"PRINCIPIO_{n+1}_DESCRICAO"] = ""

    # 5. Diretrizes — lede + sumário (lista) + conteúdo livre + page-breaks
    body = sections.get("5.", "")
    sumario_m = re.search(r"\*\*Sum[áa]rio[^*]*\*\*\s*\n((?:\s*[-*]\s+.+\n?)+)", body)
    if sumario_m:
        sumario_items = extract_bullets(sumario_m.group(1))
        sumario_html = "<ul>\n" + "\n".join(f"  <li>{s}</li>" for s in sumario_items) + "\n</ul>"
        out["LEDE_DIRETRIZES"] = body[: sumario_m.start()].strip()
        out["SUMARIO_DIRETRIZES"] = sumario_html
        after_sumario = body[sumario_m.end():].strip()
    else:
        ps = re.split(r"\n\s*\n", body, maxsplit=1)
        out["LEDE_DIRETRIZES"] = ps[0].strip() if ps else ""
        out["SUMARIO_DIRETRIZES"] = ""
        after_sumario = ps[1].strip() if len(ps) > 1 else ""

    # Split conteúdo de Diretrizes por marker <!-- /page-break --> (#7).
    # Chunk 0 vai para CONTEUDO_DIRETRIZES (página existente); chunks 1..N
    # ficam armazenados como _diretrizes_extra_chunks_md para o
    # build_extra_diretrizes_pages renderizar como <article> adicionais.
    raw_chunks = re.split(r"<!--\s*/?page-break\s*-->", after_sumario)
    raw_chunks = [c.strip() for c in raw_chunks if c.strip()]
    out["CONTEUDO_DIRETRIZES"] = restore_shortcodes(markdown_to_html(raw_chunks[0])) if raw_chunks else ""
    out["_diretrizes_chunk0_md"] = raw_chunks[0] if raw_chunks else ""
    out["_diretrizes_extra_chunks_md"] = raw_chunks[1:] if len(raw_chunks) > 1 else []

    # 6. Papéis — lede + tabela 3 col
    body = sections.get("6.", "")
    rows = extract_md_table(body)
    table_start = body.find("|")
    out["LEDE_PAPEIS"] = body[:table_start].strip() if table_start > 0 else (body.strip().split("\n\n")[0] if body else "")
    for n in range(8):
        if n < len(rows) and len(rows[n]) >= 3:
            out[f"PAPEL_{n+1}_NIVEL"] = rows[n][0]
            out[f"PAPEL_{n+1}_NOME"] = rows[n][1]
            out[f"PAPEL_{n+1}_RESPONSABILIDADES"] = rows[n][2]
        else:
            out[f"PAPEL_{n+1}_NIVEL"] = ""
            out[f"PAPEL_{n+1}_NOME"] = ""
            out[f"PAPEL_{n+1}_RESPONSABILIDADES"] = ""

    # 7. Governança — Revisão (intro + gatilhos) + Indicadores + Exceções
    body = sections.get("7.", "")
    rev_m = re.search(
        r"###+\s*(?:\d+(?:\.\d+)?\s*[·\-.]\s*)?Revis[aã]o[^\n]*\n(.+?)(?=^###|\Z)",
        body, re.DOTALL | re.MULTILINE,
    )
    if rev_m:
        rev_block = rev_m.group(1)
        rev_ps = re.split(r"\n\s*\n", rev_block, maxsplit=1)
        out["REVISAO_PERIODICA_INTRO"] = rev_ps[0].strip()
        gatilhos = extract_bullets(rev_block)
    else:
        out["REVISAO_PERIODICA_INTRO"] = ""
        gatilhos = []
    for n in range(4):
        out[f"GATILHO_REVISAO_{n+1}"] = gatilhos[n] if n < len(gatilhos) else ""

    # Coleta blocos de tabela (uma tabela por seção: indicadores, depois exceções)
    all_tables: list = []
    in_table = False
    current_block: list = []
    for line in body.split("\n"):
        if line.strip().startswith("|"):
            current_block.append(line)
            in_table = True
        else:
            if in_table and current_block:
                all_tables.append("\n".join(current_block))
                current_block = []
                in_table = False
    if in_table and current_block:
        all_tables.append("\n".join(current_block))

    ind_rows = extract_md_table(all_tables[0]) if len(all_tables) >= 1 else []
    exc_rows = extract_md_table(all_tables[1]) if len(all_tables) >= 2 else []

    for n in range(5):
        if n < len(ind_rows) and len(ind_rows[n]) >= 4:
            out[f"INDICADOR_{n+1}_NOME"] = ind_rows[n][0]
            out[f"INDICADOR_{n+1}_FORMULA"] = ind_rows[n][1]
            out[f"INDICADOR_{n+1}_FREQ"] = ind_rows[n][2]
            out[f"INDICADOR_{n+1}_META"] = ind_rows[n][3]
        else:
            out[f"INDICADOR_{n+1}_NOME"] = ""
            out[f"INDICADOR_{n+1}_FORMULA"] = ""
            out[f"INDICADOR_{n+1}_FREQ"] = ""
            out[f"INDICADOR_{n+1}_META"] = ""

    for n in range(6):
        if n < len(exc_rows) and len(exc_rows[n]) >= 2:
            out[f"ESCALA_TIPO_{n+1}"] = exc_rows[n][0]
            out[f"ESCALA_APROVADOR_{n+1}"] = exc_rows[n][1]
        else:
            out[f"ESCALA_TIPO_{n+1}"] = ""
            out[f"ESCALA_APROVADOR_{n+1}"] = ""

    # 8. Disposições finais — Vigência + tabela doc relacionado
    body = sections.get("8.", "")
    vig_m = re.search(
        r"###+\s*(?:\d+(?:\.\d+)?\s*[·\-.]\s*)?Vig[eê]ncia[^\n]*\n(.+?)(?=^###|\Z)",
        body, re.DOTALL | re.MULTILINE,
    )
    out["TEXTO_VIGENCIA"] = vig_m.group(1).strip() if vig_m else ""

    # v3.2.0 fix #5 — popular até 10 slots DOC_REL dinamicamente
    # Slots não usados ficam vazios e são removidos pelo _strip_empty_slots()
    # após substituição de placeholders. Se TODOS os 10 ficarem vazios, o
    # cleanup pass injeta um fallback row "Nenhum documento subordinado vinculado..."
    rows = extract_md_table(body)
    MAX_DOC_REL = 10
    for i in range(MAX_DOC_REL):
        slot = i + 1
        if i < len(rows) and len(rows[i]) >= 3:
            out[f"DOC_REL_{slot}_CODIGO"]  = rows[i][0]
            out[f"DOC_REL_{slot}_TITULO"]  = rows[i][1]
            out[f"DOC_REL_{slot}_RELACAO"] = rows[i][2]
        else:
            out[f"DOC_REL_{slot}_CODIGO"]  = ""
            out[f"DOC_REL_{slot}_TITULO"]  = ""
            out[f"DOC_REL_{slot}_RELACAO"] = ""

    return out


def _md_inline_lite(text: str) -> str:
    """Helper local de inline markdown — definido aqui para evitar forward-ref
    no fallback de markdown_to_html. inline_markdown() (mais abaixo) é o
    nome público; este é só uma cópia evitando dependência circular."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def _md_isolate_html_blocks(text: str) -> str:
    """Adiciona linha em branco entre `</div|p|table|figure|aside|section>`
    e o próximo elemento markdown (#, |, -, *). A python-markdown precisa
    desse delimitador para reconhecer o fim do bloco HTML e processar a
    tabela/heading/list que vem depois (anomalia #6 do patch proposal)."""
    return re.sub(
        r"(</(?:div|p|table|figure|aside|section)>)\n(?=[#|*\-]\s)",
        r"\1\n\n",
        text,
    )


def _md_fallback(text: str) -> str:
    """Conversor markdown→HTML mínimo (parágrafos, listas, h3/h4, inline, tabelas).
    Usado quando a lib `markdown` não está instalada."""
    parts: list = []
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        if block.startswith("### "):
            parts.append(f"<h3>{_md_inline_lite(block[4:].strip())}</h3>")
        elif block.startswith("#### "):
            parts.append(f"<h4>{_md_inline_lite(block[5:].strip())}</h4>")
        elif _is_md_table(block):
            parts.append(_md_render_table(block))
        elif re.match(r"^\s*[-*]\s", block):
            items = extract_bullets(block)
            items_inline = [_md_inline_lite(i) for i in items]
            parts.append("<ul>\n" + "\n".join(f"  <li>{i}</li>" for i in items_inline) + "\n</ul>")
        else:
            parts.append(f"<p>{_md_inline_lite(block)}</p>")
    return "\n".join(parts)


def _is_md_table(block: str) -> bool:
    """Detecta se o bloco é uma tabela markdown (header + separator + rows)."""
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    if len(lines) < 2:
        return False
    if not (lines[0].startswith("|") and lines[0].endswith("|")):
        return False
    if not re.match(r"^\|[\s\-:|]+\|$", lines[1]):
        return False
    return True


def _md_render_table(block: str) -> str:
    """Renderiza tabela markdown como <table>. Inline md aplicado a cada célula."""
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    header_cells = [c.strip() for c in lines[0].strip("|").split("|")]
    body_rows = []
    for line in lines[2:]:
        if line.startswith("|") and line.endswith("|"):
            body_rows.append([c.strip() for c in line.strip("|").split("|")])

    thead = "<thead><tr>" + "".join(
        f"<th>{_md_inline_lite(c)}</th>" for c in header_cells
    ) + "</tr></thead>"
    tbody_rows = []
    for row in body_rows:
        tbody_rows.append(
            "<tr>" + "".join(f"<td>{_md_inline_lite(c)}</td>" for c in row) + "</tr>"
        )
    tbody = "<tbody>" + "".join(tbody_rows) + "</tbody>"
    return f"<table>\n{thead}\n{tbody}\n</table>"


def markdown_to_html(text: str) -> str:
    """Conversor markdown→HTML para blocos ricos (CONTEUDO_DIRETRIZES).

    Tenta usar a lib `markdown` (mais completa); se não disponível, usa um
    fallback inline. Antes do parse:
      - Stash `<svg>...</svg>` (anomalia #5: a lib quebra o DOM do SVG)
      - Isola blocos HTML para que tabelas/listas após `</div>` sejam parseadas
        corretamente (anomalia #6)
    """
    if not text.strip():
        return ""

    # Patch #5 — stash <svg> antes do parse
    svg_blocks: list = []

    def _stash_svg(m: "re.Match") -> str:
        svg_blocks.append(m.group(0))
        return f"\n\n@@SVG_BLOCK_{len(svg_blocks) - 1}@@\n\n"

    text_safe = re.sub(r"<svg\b[^>]*>.*?</svg>", _stash_svg, text, flags=re.DOTALL)

    # Patch #6 — garantir linha em branco entre HTML block e markdown
    text_safe = _md_isolate_html_blocks(text_safe)

    try:
        import markdown as md_lib  # type: ignore
        # md_in_html: trata <div>...</div> como block-level (não envolve em <p>)
        html_out = md_lib.markdown(
            text_safe,
            extensions=["tables", "fenced_code", "md_in_html"],
        )
    except ImportError:
        html_out = _md_fallback(text_safe)

    # Restaurar <svg> intactos (remover wrapper <p> que a lib pode injetar)
    for i, svg in enumerate(svg_blocks):
        placeholder = f"@@SVG_BLOCK_{i}@@"
        html_out = html_out.replace(f"<p>{placeholder}</p>", svg)
        html_out = html_out.replace(placeholder, svg)

    return html_out


# =============================================================================
# Placeholder builder
# =============================================================================

def split_name_cargo(s: str) -> tuple:
    if not s:
        return "", ""
    if " · " in s:
        first, rest = s.split(" · ", 1)
        return first.strip(), rest.strip()
    return s.strip(), ""


def split_cover_title(parts: list) -> dict:
    """Decompõe title_full.parts em LINHA1/PREFIXO/ACENTO/SUFIXO."""
    accent_idx = next((idx for idx, pt in enumerate(parts) if pt.get("accent")), -1)
    if accent_idx >= 0:
        prefix_full = "".join(pt["text"] for pt in parts[:accent_idx])
        accent = parts[accent_idx]["text"].strip()
        suffix = "".join(pt["text"] for pt in parts[accent_idx + 1:]).strip()
        m = re.match(r"^(\S+)\s+(.*)$", prefix_full.strip())
        if m and len(m.group(1)) <= 12:
            return {
                "COVER_TITULO_LINHA1": m.group(1),
                "COVER_TITULO_PREFIXO": m.group(2).strip(),
                "COVER_TITULO_ACENTO": accent,
                "COVER_TITULO_SUFIXO": suffix,
            }
        return {
            "COVER_TITULO_LINHA1": prefix_full.strip(),
            "COVER_TITULO_PREFIXO": "",
            "COVER_TITULO_ACENTO": accent,
            "COVER_TITULO_SUFIXO": suffix,
        }
    text = "".join(pt["text"] for pt in parts).strip()
    m = re.match(r"^(\S+)\s+(.*)$", text)
    if m and len(m.group(1)) <= 12:
        return {
            "COVER_TITULO_LINHA1": m.group(1),
            "COVER_TITULO_PREFIXO": m.group(2),
            "COVER_TITULO_ACENTO": "",
            "COVER_TITULO_SUFIXO": "",
        }
    return {
        "COVER_TITULO_LINHA1": text,
        "COVER_TITULO_PREFIXO": "",
        "COVER_TITULO_ACENTO": "",
        "COVER_TITULO_SUFIXO": "",
    }


def build_placeholders(data: dict, content_md) -> dict:
    """Mapeia YAML + (opcional) MD → dict com os 145 placeholders."""
    i = data["identity"]
    l = data["lifecycle"]
    g = data["governance"]
    p = data["presentation"]

    date_label = l.get("date_label", str(l.get("date", "")))
    next_label = l.get("nextReview_label", str(l.get("nextReview", "")))

    nome_e, cargo_e = split_name_cargo(g.get("elaboradoPor", ""))
    nome_a, cargo_a = split_name_cargo(g.get("aprovadoPor", ""))
    nome_r, cargo_r = split_name_cargo(g.get("revisor", ""))

    # v3.2.0 fix #4 — parent null fallback semântico
    # Quando governance.parent é null OU dict sem 'code', renderiza "N/A · Política
    # raiz da hierarquia normativa M7" em vez de "<span class='mono'></span> · " solto.
    parent_raw = g.get("parent")
    if parent_raw is None or (isinstance(parent_raw, dict) and not parent_raw.get("code")):
        parent = {
            "code": "N/A",
            "title": "Política raiz da hierarquia normativa M7",
        }
    else:
        parent = parent_raw if isinstance(parent_raw, dict) else {}

    cover_pieces = split_cover_title(p["title_full"]["parts"])

    out: dict = {
        "CODIGO_DOCUMENTO": i["code"],
        "TIPO_DOCUMENTO": i.get("tipo_label", i["tipo"]),
        "TIPO_DOCUMENTO_SIGLA": i["tipo"],
        "NIVEL_DOCUMENTO": i["tipo"],
        "AREA_DOCUMENTO": i.get("area_label", i["area"]),
        "TITULO_DOCUMENTO": p["title_short"],
        "NOME_DA_EMPRESA": "M7 Investimentos",
        "VERSAO_CURTA": i["version"],
        "VERSAO_COMPLETA": i.get("version_label", i["version"]),
        "CLASSIFICACAO_DOCUMENTO": i.get("classif_label", i["classif"]),
        "TOTAL_PAGINAS": str(i.get("pages", 16)),
        "DATA_REFERENCIA": date_label,
        "DATA_VIGENCIA": date_label,
        "DATA_PROXIMA_REVISAO": next_label,
        "DATA_ELABORACAO": date_label,
        "DATA_REVISAO": date_label,
        "DATA_APROVACAO": date_label,
        "CADENCIA_REVISAO": l["revisaoFreq"],
        "COVER_SUBTITULO": p["subtitle"],
        "AREA_RESPONSAVEL": g["owner"],
        "NOME_ELABORADOR": nome_e,
        "CARGO_ELABORADOR": cargo_e,
        "NOME_APROVADOR": nome_a,
        "CARGO_APROVADOR": cargo_a,
        "NOME_REVISOR": nome_r,
        "CARGO_REVISOR": cargo_r,
        "CODIGO_DOC_SUPERIOR": parent.get("code", ""),
        "TITULO_DOC_SUPERIOR": parent.get("title", ""),
        "ALTERACOES_VERSAO": "Versão inicial.",
    }
    out.update(cover_pieces)

    content_keys = (
        ["TEXTO_OBJETIVO_P1", "TEXTO_OBJETIVO_P2", "LEDE_ESCOPO"]
        + [f"ESCOPO_INCLUSAO_{n}" for n in range(1, 4)]
        + [f"ESCOPO_EXCLUSAO_{n}" for n in range(1, 4)]
        + [f"DEF_TERMO_{n}" for n in range(1, 13)]
        + [f"DEF_TEXTO_{n}" for n in range(1, 13)]
        + ["LEDE_PRINCIPIOS"]
        + [f"PRINCIPIO_{n}_TITULO" for n in range(1, 8)]
        + [f"PRINCIPIO_{n}_DESCRICAO" for n in range(1, 8)]
        + ["LEDE_DIRETRIZES", "SUMARIO_DIRETRIZES", "CONTEUDO_DIRETRIZES"]
        + ["LEDE_PAPEIS"]
        + [f"PAPEL_{n}_NIVEL" for n in range(1, 9)]
        + [f"PAPEL_{n}_NOME" for n in range(1, 9)]
        + [f"PAPEL_{n}_RESPONSABILIDADES" for n in range(1, 9)]
        + ["REVISAO_PERIODICA_INTRO"]
        + [f"GATILHO_REVISAO_{n}" for n in range(1, 5)]
        + [f"INDICADOR_{n}_{fld}" for n in range(1, 6) for fld in ("NOME", "FORMULA", "FREQ", "META")]
        + [f"ESCALA_TIPO_{n}" for n in range(1, 7)]
        + [f"ESCALA_APROVADOR_{n}" for n in range(1, 7)]
        + ["TEXTO_VIGENCIA", "DOC_REL_1_CODIGO", "DOC_REL_1_TITULO", "DOC_REL_1_RELACAO"]
    )
    for k in content_keys:
        out.setdefault(k, "")

    if content_md and content_md.exists():
        out.update(parse_content_md(content_md))

    # Aplicar markdown inline (bold/italic/link) nos campos de texto que vão
    # para o HTML mas NÃO são placeholders de bloco rico. CONTEUDO_DIRETRIZES /
    # SUMARIO_DIRETRIZES já vêm como HTML do markdown_to_html().
    inline_md_fields = (
        ["TEXTO_OBJETIVO_P1", "TEXTO_OBJETIVO_P2", "LEDE_ESCOPO"]
        + [f"ESCOPO_INCLUSAO_{n}" for n in range(1, 4)]
        + [f"ESCOPO_EXCLUSAO_{n}" for n in range(1, 4)]
        + [f"DEF_TEXTO_{n}" for n in range(1, 13)]
        + ["LEDE_PRINCIPIOS"]
        + [f"PRINCIPIO_{n}_DESCRICAO" for n in range(1, 8)]
        + ["LEDE_DIRETRIZES", "LEDE_PAPEIS"]
        + [f"PAPEL_{n}_RESPONSABILIDADES" for n in range(1, 9)]
        + ["REVISAO_PERIODICA_INTRO"]
        + [f"GATILHO_REVISAO_{n}" for n in range(1, 5)]
        + ["TEXTO_VIGENCIA", "DOC_REL_1_RELACAO"]
    )
    for k in inline_md_fields:
        if k in out and out[k]:
            out[k] = inline_markdown(out[k])

    return out


def inline_markdown(text: str) -> str:
    """Conversor inline-only: **bold**, *italic*, [link](url), `code`.

    Não toca blocos (parágrafos, listas, headings) — o template já tem
    estrutura HTML; processar blocos seria invasivo. Para conteúdo rico
    use markdown_to_html().
    """
    if not text:
        return text
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


# =============================================================================
# Asset inlining
# =============================================================================

def inline_css_with_fonts(css: str, fonts_dir: Path) -> str:
    """Substitui url("fonts/X.otf") por data: URIs base64 dentro do CSS."""
    def repl(m: "re.Match") -> str:
        rel = m.group(1)
        font_path = fonts_dir / Path(rel).name
        if not font_path.exists():
            return m.group(0)
        b64 = base64.b64encode(font_path.read_bytes()).decode("ascii")
        return f'url(data:font/otf;base64,{b64}) format("opentype")'

    # Casa tanto `url("fonts/X.otf")` quanto `url("fonts/X.otf") format("opentype")`
    return re.sub(
        r'url\("([^"]+\.otf)"\)(?:\s+format\("opentype"\))?',
        repl,
        css,
    )


def inline_assets(html: str, assets_dir: Path) -> str:
    """Inlina CSS (com fonts base64) e logos no HTML → output autocontido."""
    css_path = assets_dir / "m7-tokens.css"
    if css_path.exists():
        css_content = css_path.read_text(encoding="utf-8")
        css_inlined = inline_css_with_fonts(css_content, assets_dir / "fonts")
        html = re.sub(
            r'<link rel="stylesheet" href="m7-tokens\.css">',
            f'<style>\n/* m7-tokens.css inlined with base64 fonts */\n{css_inlined}\n</style>',
            html,
        )

    for logo_name in ("m7-logo-dark.png", "m7-logo-offwhite.png", "m7-logo-favicon.png"):
        logo_path = assets_dir / logo_name
        if logo_path.exists():
            b64 = base64.b64encode(logo_path.read_bytes()).decode("ascii")
            data_uri = f"data:image/png;base64,{b64}"
            html = html.replace(f"assets/{logo_name}", data_uri)

    return html


# =============================================================================
# Pós-processamento do HTML renderizado
# =============================================================================

def inject_m7_classes(html: str) -> str:
    """Adiciona classes M7 em <table>, <h3>, <h4> sem classe.

    A markdown lib emite tags semânticas sem aplicar classes M7. Esta função
    injeta `.doc-table`, `.sub`, `.subsub` via lookahead negativo — preserva
    elementos que já têm classe (ex.: `.proc-title`, `.camada-title`, `.kv-table`).
    """
    html = re.sub(r'<table(?![^>]*class=)', '<table class="doc-table"', html)
    html = re.sub(r'<h3(?![^>]*class=)', '<h3 class="sub"', html)
    html = re.sub(r'<h4(?![^>]*class=)', '<h4 class="subsub"', html)
    return html


def _strip_empty_slots(html: str) -> str:
    """Remove blocos de slot vazios deixados pelo template HTML estático (v3.2+).

    Anomalia #2: `<div class="principle">` com `<div class="pt"></div>` vazio.
    Anomalia #3: `<tr>` em `<table data-table="papeis">` com `<strong></strong>` vazio.
    Anomalia #5: `<tr>` em `<table data-table="doc-related">` com 3 cells vazias.

    Quando a tabela `doc-related` fica com 0 linhas após cleanup, injeta um
    fallback row "Nenhum documento subordinado vinculado nesta versão." em
    cell única `<td colspan="3" class="muted-empty">`.

    Idempotente: rodar 2x produz mesmo output. Regex permissivo (`\\s*`) lida
    com whitespace/newlines variados deixados pelo template+substituição.
    """
    # 1. Remove .principle blocks com <div class="pt"> vazio (anomalia #2)
    html = re.sub(
        r'\s*<div class="principle">\s*<div class="pn">P\d+</div>\s*'
        r'<div class="pt">\s*</div>\s*<div class="pd">\s*</div>\s*</div>',
        '',
        html,
    )

    # 2. Remove <tr> com <strong></strong> vazio em <table data-table="papeis"> (anomalia #3)
    def _clean_papeis(m: "re.Match") -> str:
        table = m.group(0)
        table = re.sub(
            r'\s*<tr>\s*<td>\s*<strong>\s*</strong>\s*</td>\s*'
            r'<td>\s*(?:<span[^>]*>\s*</span>\s*)?</td>\s*'
            r'<td>\s*</td>\s*</tr>',
            '',
            table,
        )
        return table
    html = re.sub(
        r'<table class="doc-table" data-table="papeis">.*?</table>',
        _clean_papeis,
        html,
        flags=re.DOTALL,
    )

    # 3. Remove <tr> totalmente vazios em <table data-table="doc-related"> (anomalia #5)
    #    Se zero <tr> sobrarem no <tbody>, injeta fallback row.
    def _clean_doc_related(m: "re.Match") -> str:
        table = m.group(0)
        table = re.sub(
            r'\s*<tr>\s*<td>\s*<span class="mono">\s*</span>\s*</td>\s*'
            r'<td>\s*</td>\s*<td>\s*</td>\s*</tr>',
            '',
            table,
        )
        # Se zero tr's em tbody, injeta fallback informativo
        tbody_match = re.search(r'<tbody>(.*?)</tbody>', table, re.DOTALL)
        if tbody_match and not re.search(r'<tr\b', tbody_match.group(1)):
            fallback = (
                '\n            <tr><td colspan="3" class="muted-empty">'
                'Nenhum documento subordinado vinculado nesta versão.'
                '</td></tr>\n          '
            )
            table = table.replace(
                tbody_match.group(0),
                f'<tbody>{fallback}</tbody>',
            )
        return table
    html = re.sub(
        r'<table class="doc-table" data-table="doc-related">.*?</table>',
        _clean_doc_related,
        html,
        flags=re.DOTALL,
    )

    return html


def _estimate_chunk_height(md: str) -> int:
    """Estima altura em px do chunk renderizado em A4 (largura ~174mm).

    Heurística conservadora — bate dentro de ±15% para conteúdo típico.
    Usada para alertar autor quando um page-break é necessário antes que
    `overflow: hidden` corte o conteúdo (page-body útil ≈ 960px).
    """
    h = 0
    # Cards (qualquer classe `*-card` no MD): ~180px cada
    h += len(re.findall(r'<div\s+class="[^"]*-card[^"]*"', md)) * 180
    # Tabelas markdown: header (28px) + ~35px por linha
    table_lines = len(re.findall(r"^\s*\|.*\|\s*$", md, re.MULTILINE))
    if table_lines:
        h += 28 + max(0, table_lines - 2) * 35  # -2 = header + separator
    # SVG inline (assume aspect ratio + width 100%)
    if "<svg" in md:
        h += 540
    # Headings
    h += len(re.findall(r"^###\s", md, re.MULTILINE)) * 30
    h += len(re.findall(r"^####\s", md, re.MULTILINE)) * 22
    # Bullets
    h += len(re.findall(r"^\s*[-*]\s+", md, re.MULTILINE)) * 22
    # Parágrafos não-HTML/não-heading/não-list/não-tabela
    paras = 0
    for line in md.split("\n"):
        s = line.strip()
        if not s:
            continue
        if s.startswith(("<", "#", "|", "-", "*")):
            continue
        paras += 1
    h += paras * 22  # linha média (parágrafos longos quebrarão em múltiplas)
    return h


def build_extra_diretrizes_pages(content_md, placeholders: dict) -> str:
    """Renderiza os chunks 1..N de Diretrizes como <article class="page">.

    O chunk 0 já está em CONTEUDO_DIRETRIZES (página existente do template).
    Os chunks adicionais (gerados por <!-- /page-break --> no MD) viram páginas
    extras inseridas via {{EXTRA_DIRETRIZES_PAGES}}.

    O JS do template auto-numera todas as `.page` no load, então
    `Página ? de ?` aqui é só placeholder visual antes do JS rodar.

    Emite warning no stderr quando o chunk estimado > 900px (margem de
    segurança em relação ao page-body útil de ~960px). Threshold no chunk 0
    também (cadernal — exibido com índice 1 para o autor).
    """
    # Validação de altura do chunk 0 (CONTEUDO_DIRETRIZES renderizado)
    chunks_md = placeholders.get("_diretrizes_extra_chunks_md") or []
    chunk0_md = placeholders.get("_diretrizes_chunk0_md", "")
    if chunk0_md:
        est = _estimate_chunk_height(chunk0_md)
        if est > 900:
            sys.stderr.write(
                f"⚠  Chunk Diretrizes #1 estimado em {est}px — pode exceder "
                f"altura do page-body A4 (~960px) e ser cortado por overflow:hidden.\n"
                f"   Adicione <!-- /page-break --> antes de elementos pesados.\n"
            )

    if not chunks_md:
        return ""

    # Validar chunks extras (1..N)
    for i, chunk_md in enumerate(chunks_md, start=2):
        est = _estimate_chunk_height(chunk_md)
        if est > 900:
            sys.stderr.write(
                f"⚠  Chunk Diretrizes #{i} estimado em {est}px — pode exceder "
                f"altura do page-body A4 (~960px) e ser cortado por overflow:hidden.\n"
                f"   Adicione <!-- /page-break --> antes de elementos pesados.\n"
            )

    chunks = chunks_md

    code = placeholders.get("CODIGO_DOCUMENTO", "")
    version = placeholders.get("VERSAO_CURTA", "")
    title = placeholders.get("TITULO_DOCUMENTO", "")
    classif = placeholders.get("CLASSIFICACAO_DOCUMENTO", "")

    parts: list = []
    for chunk_md in chunks:
        chunk_html = restore_shortcodes(markdown_to_html(chunk_md))
        parts.append(
            '\n  <!-- ════════════════════════════════════════════════════════════\n'
            '       Diretrizes (continuação) — auto-paginação\n'
            '       ════════════════════════════════════════════════════════════ -->\n'
            '  <article class="page" data-page-label="Diretrizes (cont.)">\n'
            '    <header class="page-head">\n'
            '      <div class="ph-left">\n'
            '        <img src="assets/m7-logo-dark.png" alt="M7">\n'
            '        <div class="ph-sep"></div>\n'
            f'        <span class="ph-title">{escape(title)}</span>\n'
            '      </div>\n'
            f'      <span class="ph-meta">{escape(code)} · {escape(version)}</span>\n'
            '    </header>\n'
            '    <div class="page-body">\n'
            f'      {chunk_html}\n'
            '    </div>\n'
            '    <footer class="page-foot">\n'
            f'      <span class="pf-classif">{escape(classif)}</span>\n'
            '      <span class="pf-page">Página <strong>?</strong> de <span class="total-pg">?</span></span>\n'
            '    </footer>\n'
            '  </article>\n'
        )
    return "".join(parts)


def inline_external_images(html: str, base_dir: Path) -> str:
    """Inlina <img src="<path-relativo>"> como data: URI.

    Escaneia tags <img src="..."> e, se o src for path relativo a um arquivo
    local existente em base_dir, converte para base64. Preserva data: URIs
    e URLs http(s) inalteradas. Útil para imagens externas referenciadas no
    MD da Fase 2 (ex.: SVG de cadeia de valor).
    """
    SUPPORTED = {"svg": "image/svg+xml", "png": "image/png",
                 "jpg": "image/jpeg", "jpeg": "image/jpeg",
                 "gif": "image/gif", "webp": "image/webp"}

    def repl(m: "re.Match") -> str:
        prefix = m.group(1)
        src = m.group(2)
        suffix = m.group(3)
        if src.startswith(("data:", "http://", "https://", "//")):
            return m.group(0)
        img_path = (base_dir / src).resolve()
        if not img_path.exists() or not img_path.is_file():
            sys.stderr.write(f"⚠  imagem não encontrada: {src} (relativo a {base_dir})\n")
            return m.group(0)
        ext = img_path.suffix.lstrip(".").lower()
        mime = SUPPORTED.get(ext, "application/octet-stream")
        b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")
        return f'{prefix}data:{mime};base64,{b64}{suffix}'

    return re.sub(r'(<img\s+[^>]*?src=")([^"]+)(")', repl, html)


# =============================================================================
# Main
# =============================================================================

def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--briefing", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--content", help="MD com conteúdo das 8 seções")
    parser.add_argument("--basename")
    parser.add_argument("--template")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--no-inline", action="store_true",
                        help="Não inlinear CSS/fonts/logos (debug)")
    args = parser.parse_args()

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

    try:
        data = parse_briefing(briefing_path)
    except Exception as e:
        sys.stderr.write(f"ERRO ao parsear briefing: {e}\n")
        return 2

    normalize_governance(data)

    errs = validate(data)
    if errs:
        sys.stderr.write("VALIDAÇÃO DE SCHEMA FALHOU:\n")
        for e in errs:
            sys.stderr.write(e + "\n")
        return 1

    if args.validate_only:
        print("✓ YAML valida contra o schema")
        return 0

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    basename = args.basename or slugify(data["identity"]["code"])
    yaml_out = output_dir / f"{basename}.yaml"
    html_out = output_dir / f"{basename}.html"

    yaml_out.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=120),
        encoding="utf-8",
    )

    content_md = Path(args.content) if args.content else None
    try:
        placeholders = build_placeholders(data, content_md)
    except ValueError as ve:
        sys.stderr.write(str(ve) + "\n")
        sys.stderr.write(
            "\nO MD da Fase 2 quebrou a separação design/conteúdo. Corrija os\n"
            "itens acima e re-execute. Detalhes em "
            "references/component-catalog.md\n"
        )
        return 1

    # Extra Diretrizes pages (#7): se MD tem <!-- /page-break --> na seção 5,
    # build_extra_diretrizes_pages retorna o HTML das páginas adicionais; o
    # primeiro chunk já está em CONTEUDO_DIRETRIZES.
    placeholders["EXTRA_DIRETRIZES_PAGES"] = build_extra_diretrizes_pages(
        content_md, placeholders
    )

    html = template_path.read_text(encoding="utf-8")

    for key, val in placeholders.items():
        # Skip chaves internas (prefixo _) e valores não-string.
        if key.startswith("_") or not isinstance(val, str):
            continue
        html = html.replace("{{" + key + "}}", val)

    # inline_assets DEPOIS da substituição: assim os <img src="assets/m7-logo-*.png">
    # das páginas extras de Diretrizes (geradas via {{EXTRA_DIRETRIZES_PAGES}})
    # também viram base64.
    if not args.no_inline:
        html = inline_assets(html, skill_dir / "assets")

    # Pós-processamento: injetar classes M7 em tags da markdown lib + inline
    # imagens externas referenciadas no MD do autor.
    html = inject_m7_classes(html)
    if content_md and content_md.exists():
        html = inline_external_images(html, content_md.parent)

    # v3.2.0 — auto-cleanup de slots vazios (Princípios, Papéis, DOC_REL).
    # Internaliza os workarounds que viviam em postprocess-{CODE}.py para que
    # operadores remotos (Claude COWORK) recebam HTML correto no primeiro passe.
    html = _strip_empty_slots(html)

    residuals = set(re.findall(r"\{\{([A-Z_0-9]+)\}\}", html))
    warnings: list = []
    if residuals:
        warnings.append(f"placeholders não substituídos: {sorted(residuals)}")
    if not args.no_inline and re.search(r'(?:href|src)="(?:assets/|fonts/|m7-tokens\.css)', html):
        warnings.append("paths relativos restantes após inline")

    # v4.0 — validação pós-render do HTML final
    # Carrega template puro como baseline para contagem de style legítimos
    template_baseline = template_path.read_text(encoding="utf-8")
    html_class_errs = validate_html_classes(html)
    html_style_errs = validate_html_no_inline_styles(html, template_baseline)
    fatal_errs = html_class_errs + html_style_errs
    if fatal_errs:
        sys.stderr.write("VALIDAÇÃO DO HTML FINAL FALHOU:\n")
        for e in fatal_errs:
            sys.stderr.write(e + "\n")
        sys.stderr.write(
            "\nCausa provável: shortcode mal-renderizado, classe ad-hoc, ou\n"
            "<style> injetado no MD que escapou da validação. Confira o MD\n"
            "da Fase 2 contra references/component-catalog.md.\n"
        )
        return 1

    html_out.write_text(html, encoding="utf-8")

    # v4.0 — stub do .review.md (gate de design review)
    review_path = output_dir / f"{basename}.review.md"
    code = data.get("identity", {}).get("code", "POL-UNKNOWN")
    titulo = data.get("presentation", {}).get("title_short", "")
    review_path.write_text(
        f"# Design Review: {code} · {titulo}\n\n"
        f"**Arquivo**: `{html_out}`\n"
        f"**Status**: PENDING — invoque o agente `politica-design-reviewer`\n"
        f"**Score esperado para entrega**: ≥ B\n\n"
        "---\n\n"
        "Este arquivo é um stub gerado pelo script `generate-html-yaml.py`.\n"
        "O conteúdo real do design review é produzido pelo agente\n"
        "`politica-design-reviewer` ao analisar o HTML acima.\n\n"
        "Para preencher este review:\n\n"
        "1. Invoque o agente: `Task(subagent_type='politica-design-reviewer', ...)`\n"
        f"2. Forneça os caminhos do HTML, YAML, MD-fonte e code `{code}`\n"
        "3. O agente sobrescreverá este arquivo com o relatório completo\n"
        "   (Score A/B/C/D + issues categorizadas + Quick Fix CSS)\n"
        "4. Score < B bloqueia a entrega — corrija o MD/BRIEFING e re-execute\n",
        encoding="utf-8",
    )

    size_kb = html_out.stat().st_size // 1024
    print("✓ Gerado:")
    print(f"   {yaml_out}")
    print(f"   {html_out}  ({size_kb} KB)")
    print(f"   {review_path}  (stub — invoque politica-design-reviewer)")
    for w in warnings:
        sys.stderr.write(f"⚠  {w}\n")
    return 0 if not residuals else 3


if __name__ == "__main__":
    sys.exit(main())
