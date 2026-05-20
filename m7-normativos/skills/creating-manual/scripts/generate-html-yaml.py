#!/usr/bin/env python3
"""
generate-html-yaml.py — Pipeline da Fase 3 de creating-manual (v1.0).

Estratégia: o template oficial `manual-m7-template.html` tem 149 placeholders
`{{...}}` explícitos, espalhados em 11 páginas A4 com estruturas procedurais
manual-específicas (BPMN, SIPOC, RACI 5×5, KPI/PPI, Cronograma de rituais,
DTO de qualidade). O script:

1. Parseia BRIEFING.md (YAML) e valida contra normativo.schema.yaml
2. Opcionalmente parseia manual-{slug}.md — valida MD (sem <style>, sem
   style="...", sem classes ad-hoc), expande shortcodes (:::papel-card,
   :::callout, :::raci, etc) e extrai conteúdo das 10 seções
3. Constrói dicionário de 149 placeholders → valores
4. INLINEIA CSS + fonts (base64) + logos (base64) no HTML — output autocontido
5. Substitui todos os placeholders via str.replace
6. Valida zero placeholders residuais, zero paths relativos, e zero classes
   CSS fora da allowlist do component-catalog-manual.md
7. Escreve trio {slug}.html + {slug}.yaml + {slug}.review.md (stub)

A v1.0 espelha a arquitetura da skill `creating-politica` v4.0, com
**separação rígida entre conteúdo (MD canônico) e apresentação (template +
shortcodes catalogados)**:

- MD da Fase 2 aceita SOMENTE markdown padrão + shortcodes do catálogo
  (component-catalog-manual.md). HTML inline com classes ou <style> é rejeitado.
- O HTML final tem allowlist de classes CSS — qualquer classe fora dela
  aborta a geração.
- O .review.md gerado é STUB; a skill orquestradora deve invocar o agente
  `manual-design-reviewer` para preencher com o relatório real (gate
  obrigatório Score >= B antes da entrega).

CLI:
    python generate-html-yaml.py \\
        --briefing  BRIEFING-MAN-PERF-003.md \\
        --output-dir <dir> \\
        [--content manual-rituais-de-gestao.md] \\
        [--basename MAN-PERF-003] \\
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
    "raci",
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
    # Shortcode: raci (matriz adicional via shortcode)
    "raci-extra",
    # Manual-specific: BPMN classes
    "bpmn-frame", "bpmn-head", "bpmn-head-code", "bpmn-head-title",
    "bpmn-canvas", "bpmn-pool", "bpmn-lane-strip", "bpmn-lane-bg",
    "bpmn-lane-label", "bpmn-lane-divider",
    "bpmn-task", "bpmn-task-header", "bpmn-task-label",
    "bpmn-event-start", "bpmn-event-end", "bpmn-event-label",
    "bpmn-gateway", "bpmn-gateway-mark",
    "bpmn-flow", "bpmn-flow-label", "bpmn-flow-label-bg",
    "bpmn-arrow-fill", "bpmn-legend", "bpmn-caption",
    "alt",  # modifier para .bpmn-lane-bg.alt
    # Manual-specific: SIPOC
    "sipoc", "is-process",
    # Manual-specific: RACI 5×5 (template + shortcode)
    "raci-table", "raci-cell",
    "raci-r", "raci-a", "raci-c", "raci-i",
    "raci-legend", "activity", "activity-h", "step",
    # Manual-specific: indicadores (KPI/PPI cards)
    "kpi-grid", "kpi-card", "ppi",
    "formula", "freq", "name", "out",
    # Manual-specific: cronograma
    "timeline", "ritual",
    # Manual-specific: qualidade
    "dto-list", "item",
    # Misc Manual classes do template
    "h", "navbtn", "twocol", "col", "h2",
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

    if name == "raci":
        titulo = escape(_attr(attrs, "titulo", "título"))
        # Parsear tabela markdown 5×5 do corpo
        rows = []
        seen_header = False
        seen_sep = False
        for line in body.split("\n"):
            s = line.strip()
            if s.startswith("|") and s.endswith("|"):
                cells = [c.strip() for c in s.strip("|").split("|")]
                if not seen_header:
                    header_cells = cells
                    seen_header = True
                    continue
                if not seen_sep and all(re.match(r"^[\s\-:]*$", c) for c in cells):
                    seen_sep = True
                    continue
                if seen_sep:
                    rows.append(cells)
        if not seen_header or not rows:
            return f'<!-- raci shortcode com tabela inválida: {escape(body[:80])} -->'

        # Render header
        thead = "<thead><tr>" + "".join(
            f'<th{" class=\"activity-h\"" if i == 0 else ""}>{escape(c)}</th>'
            for i, c in enumerate(header_cells)
        ) + "</tr></thead>"
        # Render body
        tr_html = []
        for row in rows:
            cells_out = []
            for i, c in enumerate(row):
                if i == 0:
                    cells_out.append(f'<td class="activity">{_md_inline_lite(c)}</td>')
                else:
                    code = c.upper().strip()
                    if code in {"R", "A", "C", "I"}:
                        cells_out.append(
                            f'<td><span class="raci-cell raci-{code.lower()}">{code}</span></td>'
                        )
                    else:
                        # múltiplos códigos (ex: "A,R") → mostra primeira letra
                        first = code.split(",")[0].strip() if "," in code else code
                        if first in {"R", "A", "C", "I"}:
                            cells_out.append(
                                f'<td><span class="raci-cell raci-{first.lower()}">{escape(code)}</span></td>'
                            )
                        else:
                            cells_out.append(f'<td>{escape(c)}</td>')
            tr_html.append("<tr>" + "".join(cells_out) + "</tr>")
        tbody = "<tbody>" + "".join(tr_html) + "</tbody>"
        title_html = f'<h4 class="sub">{titulo}</h4>\n  ' if titulo else ""
        return (
            '<div class="raci-extra">\n'
            f'  {title_html}<table class="raci-table">\n'
            f'    {thead}\n'
            f'    {tbody}\n'
            '  </table>\n'
            '</div>'
        )

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
                    f":::callout, :::indicador, :::diagrama, :::processo-grid, :::raci) "
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
    """Lê manual-{slug}.md e extrai valores para os placeholders de conteúdo.

    Em v1.0: o texto é validado (sem <style>, sem style="...", sem classes
    ad-hoc, sem <svg> solto) e tem shortcodes expandidos ANTES de qualquer
    parseamento de seções. Erros de validação são propagados via exceção
    para abortar a Fase 3 com mensagem clara.

    O MD tem 10 seções (h2 numerados 1-10) que mapeiam para 149 placeholders
    do template-manual.html:

      1. Objetivo                    → TEXTO_OBJETIVO_P1/P2
      2. Escopo                      → LEDE_ESCOPO, ESCOPO_INCLUSAO_1..3, ESCOPO_EXCLUSAO_1..3
      3. Definições                  → DEF_TERMO_1..10, DEF_TEXTO_1..10
      4. Visão Geral                 → LEDE_VISAO_GERAL, MISSAO_PROCESSO, SIPOC_*, TEXTO_INTERFACES, BPMN_*
      5. Regras de Negócio           → LEDE_REGRAS, REGRAS_TEMA_1..2, REGRA_01..06, EXCECAO_1..2, APROVADOR_EXCECAO_1..2
      6. Papéis e Responsabilidades  → LEDE_PAPEIS, RACI_PAPEL_1..5, RACI_ATIV_1..5
      7. Indicadores                 → LEDE_INDICADORES, KPI_1..2_*, PPI_1..2_*
      8. Cronograma                  → LEDE_CRONOGRAMA, CRONO_{DIARIO,SEMANAL,MENSAL,TRIMESTRAL,SEMESTRAL}_{RITUAL,OUT}
      9. Critérios de Qualidade      → LEDE_QUALIDADE, DTO_01..05
      10. Documentos Relacionados    → REL_CODIGO_1..4, REL_NOME_1..4, REL_TIPO_1..4, CODIGO_ESP
    """
    text = path.read_text(encoding="utf-8")

    # v1.0 — validação prévia + expansão de shortcodes
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

    # 2. Escopo — lede + inclusões + exclusões (3 cada)
    body = sections.get("2.", "")
    lede_m = re.match(r"^(.+?)(?=\n\s*\*\*|\n\s*-\s|\n\s*###)", body, re.DOTALL)
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

    # 3. Definições — tabela 2 col (10 slots)
    rows = extract_md_table(sections.get("3.", ""))
    for n in range(10):
        if n < len(rows) and len(rows[n]) >= 2:
            out[f"DEF_TERMO_{n+1}"] = rows[n][0]
            out[f"DEF_TEXTO_{n+1}"] = rows[n][1]
        else:
            out[f"DEF_TERMO_{n+1}"] = ""
            out[f"DEF_TEXTO_{n+1}"] = ""

    # 4. Visão Geral — LEDE + Missão (4.1) + SIPOC (4.2) + Interfaces (4.3) + BPMN (4.4)
    body = sections.get("4.", "")

    # lede = texto antes de qualquer h3
    h3_m = re.search(r"^###\s+", body, re.MULTILINE)
    out["LEDE_VISAO_GERAL"] = body[: h3_m.start()].strip() if h3_m else body.strip().split("\n\n")[0]

    # 4.1 Missão do processo
    missao_m = re.search(
        r"###+\s*(?:\d+\.\d+\s*[·\-.]\s*)?Miss[aã]o[^\n]*\n(.+?)(?=^###|\Z)",
        body, re.DOTALL | re.MULTILINE,
    )
    out["MISSAO_PROCESSO"] = (missao_m.group(1).strip() if missao_m else "").split("\n\n")[0]

    # 4.2 SIPOC — tabela 5 col (S, I, P, O, C). Cada coluna tem 3 itens (P tem 4).
    sipoc_m = re.search(
        r"###+\s*(?:\d+\.\d+\s*[·\-.]\s*)?SIPOC[^\n]*\n(.+?)(?=^###|\Z)",
        body, re.DOTALL | re.MULTILINE,
    )
    sipoc_block = sipoc_m.group(1) if sipoc_m else ""
    sipoc_rows = extract_md_table(sipoc_block)
    # Cada linha da tabela = (S, I, P, O, C) para um índice. Coletamos colunas.
    for n in range(3):
        out[f"SIPOC_S_{n+1}"] = sipoc_rows[n][0] if n < len(sipoc_rows) and len(sipoc_rows[n]) >= 1 else ""
        out[f"SIPOC_I_{n+1}"] = sipoc_rows[n][1] if n < len(sipoc_rows) and len(sipoc_rows[n]) >= 2 else ""
        out[f"SIPOC_O_{n+1}"] = sipoc_rows[n][3] if n < len(sipoc_rows) and len(sipoc_rows[n]) >= 4 else ""
        out[f"SIPOC_C_{n+1}"] = sipoc_rows[n][4] if n < len(sipoc_rows) and len(sipoc_rows[n]) >= 5 else ""
    for n in range(4):
        out[f"SIPOC_P_{n+1}"] = sipoc_rows[n][2] if n < len(sipoc_rows) and len(sipoc_rows[n]) >= 3 else ""

    # 4.3 Interfaces e dependências
    inter_m = re.search(
        r"###+\s*(?:\d+\.\d+\s*[·\-.]\s*)?Interfaces[^\n]*\n(.+?)(?=^###|\Z)",
        body, re.DOTALL | re.MULTILINE,
    )
    out["TEXTO_INTERFACES"] = (inter_m.group(1).strip() if inter_m else "").split("\n\n")[0]

    # 4.4 Fluxograma BPMN — extrai narrativa textual (3 parágrafos) e título/caption.
    # O diagrama SVG vem como :::diagrama (já expandido por expand_shortcodes
    # mas o conteúdo SVG fica no _SC_BLOCKS — preserva como CONTEUDO_BPMN).
    # No template, BPMN_EVT_INICIO/TASK_N/etc são placeholders SVG fixos
    # preenchidos via texto curto se autor declarar no MD via :::diagrama
    # opcional com attrs. Para simplificar v1.0, deixamos defaults legíveis
    # se autor não declarar nada.
    bpmn_m = re.search(
        r"###+\s*(?:\d+\.\d+\s*[·\-.]\s*)?Fluxograma\s+BPMN[^\n]*\n(.+?)(?=^##|\Z)",
        body, re.DOTALL | re.MULTILINE,
    )
    bpmn_block = bpmn_m.group(1) if bpmn_m else ""
    # Narrativa: bullets numerados (1. 2. 3.) ou paragraphs após "Narrativa do fluxo"
    narrativa_m = re.search(
        r"\*\*Narrativa[^*]*\*\*\s*\n(.+?)(?=\Z)",
        bpmn_block, re.DOTALL,
    )
    if narrativa_m:
        narr_text = narrativa_m.group(1).strip()
        # Procura por bullets numerados "1. " "2. " "3. "
        narrs = re.findall(r"^\s*\d+\.\s+(.+?)(?=^\s*\d+\.|\Z)", narr_text, re.DOTALL | re.MULTILINE)
        if not narrs:
            narrs = [p.strip() for p in re.split(r"\n\s*\n", narr_text) if p.strip()]
    else:
        narrs = []
    for n in range(3):
        out[f"BPMN_NARRATIVA_{n+1}"] = narrs[n].strip() if n < len(narrs) else ""

    # BPMN título/caption — defaults se MD não declarar
    out.setdefault("BPMN_DIAGRAMA_TITULO", "Fluxograma BPMN do processo")
    out.setdefault("BPMN_CAPTION", "Fig 1 · Visão do fluxo")

    # BPMN elementos — extrai do :::diagrama attrs (se autor declarou) ou
    # deixa vazio (template já tem texto default em alguns slots).
    # Heurística: pega tasks/eventos da narrativa se aparecerem como bold
    bpmn_defaults = {
        "BPMN_EVT_INICIO": "Início",
        "BPMN_TASK_1": "E1 · Tarefa 1",
        "BPMN_TASK_2": "E2 · Tarefa 2",
        "BPMN_TASK_3": "E3 · Tarefa 3",
        "BPMN_TASK_4": "E4 · Tarefa 4",
        "BPMN_GATEWAY_1": "Decisão?",
        "BPMN_EVT_FIM_1": "Concluído",
        "BPMN_EVT_FIM_2": "",
    }
    for k, v in bpmn_defaults.items():
        out.setdefault(k, v)

    # 5. Regras de Negócio — LEDE + 2 temas + 6 regras + 2 exceções com aprovadores
    body = sections.get("5.", "")
    h3_m = re.search(r"^###\s+", body, re.MULTILINE)
    out["LEDE_REGRAS"] = body[: h3_m.start()].strip() if h3_m else body.strip().split("\n\n")[0]

    h3_matches = list(re.finditer(r"^###\s+(?:\d+\.\d+\s*[·\-.]\s*)?(.+?)$", body, re.MULTILINE))
    tema_titles = []
    for h3 in h3_matches:
        title = h3.group(1).strip()
        # Pula h3 "Exceções permitidas"
        if not re.search(r"exce[cç][oõ]es", title, re.IGNORECASE):
            tema_titles.append(title)
    out["REGRAS_TEMA_1"] = tema_titles[0] if len(tema_titles) >= 1 else ""
    out["REGRAS_TEMA_2"] = tema_titles[1] if len(tema_titles) >= 2 else ""

    # 6 regras numeradas RN-XX (case-insensitive)
    regra_matches = re.findall(
        r"\*\*RN-?\d+\*\*\s*[·\-.]?\s*(.+?)(?=\n\s*\d+\.|\n\s*\*\*RN-?\d+|\n\s*###|\Z)",
        body, re.DOTALL,
    )
    if not regra_matches:
        # Fallback: bullets numerados na seção 5
        regra_matches = re.findall(
            r"^\s*\d+\.\s+(.+?)(?=^\s*\d+\.|^###|\Z)",
            body, re.DOTALL | re.MULTILINE,
        )
    for n in range(6):
        slot = f"REGRA_0{n+1}"
        out[slot] = regra_matches[n].strip() if n < len(regra_matches) else ""

    # Exceções (tabela 2 col) na sub-seção "Exceções permitidas"
    exc_m = re.search(
        r"###+\s*(?:\d+\.\d+\s*[·\-.]\s*)?Exce[cç][oõ]es[^\n]*\n(.+?)(?=^###|\Z)",
        body, re.DOTALL | re.MULTILINE,
    )
    exc_rows = extract_md_table(exc_m.group(1) if exc_m else "")
    for n in range(2):
        out[f"EXCECAO_{n+1}"] = exc_rows[n][0] if n < len(exc_rows) and len(exc_rows[n]) >= 1 else ""
        out[f"APROVADOR_EXCECAO_{n+1}"] = exc_rows[n][1] if n < len(exc_rows) and len(exc_rows[n]) >= 2 else ""

    # 6. Papéis e Responsabilidades — LEDE + RACI 5×5
    body = sections.get("6.", "")
    h3_m = re.search(r"^###\s+", body, re.MULTILINE)
    out["LEDE_PAPEIS"] = body[: h3_m.start()].strip() if h3_m else body.strip().split("\n\n")[0]

    # RACI table — primeira tabela na seção 6
    raci_rows = extract_md_table(body)
    # Header da tabela RACI vira RACI_PAPEL_1..5 (extrai do MD diretamente)
    # Parse manual do header
    header_m = re.search(r"^\|\s*Atividade\s*\|(.+?)\|$", body, re.MULTILINE | re.IGNORECASE)
    if header_m:
        papel_cells = [c.strip() for c in header_m.group(1).split("|")]
        for n in range(5):
            out[f"RACI_PAPEL_{n+1}"] = papel_cells[n] if n < len(papel_cells) else ""
    else:
        for n in range(5):
            out[f"RACI_PAPEL_{n+1}"] = ""

    # Atividades = primeira coluna de cada linha
    for n in range(5):
        if n < len(raci_rows) and len(raci_rows[n]) >= 1:
            out[f"RACI_ATIV_{n+1}"] = raci_rows[n][0]
        else:
            out[f"RACI_ATIV_{n+1}"] = ""

    # 7. Indicadores — LEDE + 2 KPIs (tabela 7.1) + 2 PPIs (tabela 7.2)
    body = sections.get("7.", "")
    h3_m = re.search(r"^###\s+", body, re.MULTILINE)
    out["LEDE_INDICADORES"] = body[: h3_m.start()].strip() if h3_m else body.strip().split("\n\n")[0]

    kpi_block_m = re.search(
        r"###+\s*(?:\d+\.\d+\s*[·\-.]\s*)?KPI[^\n]*\n(.+?)(?=^###|\Z)",
        body, re.DOTALL | re.MULTILINE | re.IGNORECASE,
    )
    ppi_block_m = re.search(
        r"###+\s*(?:\d+\.\d+\s*[·\-.]\s*)?PPI[^\n]*\n(.+?)(?=^###|\Z)",
        body, re.DOTALL | re.MULTILINE | re.IGNORECASE,
    )
    kpi_rows = extract_md_table(kpi_block_m.group(1) if kpi_block_m else "")
    ppi_rows = extract_md_table(ppi_block_m.group(1) if ppi_block_m else "")

    for n in range(2):
        if n < len(kpi_rows) and len(kpi_rows[n]) >= 5:
            out[f"KPI_{n+1}_NOME"]    = kpi_rows[n][0]
            out[f"KPI_{n+1}_FORMULA"] = kpi_rows[n][1]
            out[f"KPI_{n+1}_META"]    = kpi_rows[n][2]
            out[f"KPI_{n+1}_FREQ"]    = kpi_rows[n][3]
            out[f"KPI_{n+1}_FONTE"]   = kpi_rows[n][4]
        else:
            out[f"KPI_{n+1}_NOME"]    = ""
            out[f"KPI_{n+1}_FORMULA"] = ""
            out[f"KPI_{n+1}_META"]    = ""
            out[f"KPI_{n+1}_FREQ"]    = ""
            out[f"KPI_{n+1}_FONTE"]   = ""

        if n < len(ppi_rows) and len(ppi_rows[n]) >= 5:
            out[f"PPI_{n+1}_NOME"]    = ppi_rows[n][0]
            out[f"PPI_{n+1}_FORMULA"] = ppi_rows[n][1]
            out[f"PPI_{n+1}_META"]    = ppi_rows[n][2]
            out[f"PPI_{n+1}_FREQ"]    = ppi_rows[n][3]
            out[f"PPI_{n+1}_FONTE"]   = ppi_rows[n][4]
        else:
            out[f"PPI_{n+1}_NOME"]    = ""
            out[f"PPI_{n+1}_FORMULA"] = ""
            out[f"PPI_{n+1}_META"]    = ""
            out[f"PPI_{n+1}_FREQ"]    = ""
            out[f"PPI_{n+1}_FONTE"]   = ""

    # 8. Cronograma — LEDE + tabela 3 col (Cadência, Ritual, Output) — 5 linhas
    body = sections.get("8.", "")
    h3_m = re.search(r"^###\s+", body, re.MULTILINE)
    table_start = body.find("|")
    out["LEDE_CRONOGRAMA"] = (
        body[: h3_m.start()].strip() if h3_m
        else (body[: table_start].strip() if table_start > 0 else body.strip().split("\n\n")[0])
    )

    crono_rows = extract_md_table(body)
    crono_map = {
        "diari": "DIARIO", "diaria": "DIARIO",
        "semanal": "SEMANAL",
        "mensal": "MENSAL",
        "trimestral": "TRIMESTRAL",
        "semestral": "SEMESTRAL",
        "anual": "ANUAL",
    }
    # Default vazio
    for cad in ("DIARIO", "SEMANAL", "MENSAL", "TRIMESTRAL", "SEMESTRAL"):
        out[f"CRONO_{cad}_RITUAL"] = ""
        out[f"CRONO_{cad}_OUT"] = ""
    for row in crono_rows:
        if len(row) >= 3:
            cad_key = row[0].lower().strip()
            for key_pattern, cad in crono_map.items():
                if cad_key.startswith(key_pattern):
                    out[f"CRONO_{cad}_RITUAL"] = row[1]
                    out[f"CRONO_{cad}_OUT"] = row[2]
                    break

    # 9. Critérios de Qualidade — LEDE + 5 critérios DTO_01..05
    body = sections.get("9.", "")
    h3_m = re.search(r"^###\s+", body, re.MULTILINE)
    list_start_m = re.search(r"^\s*\d+\.\s+", body, re.MULTILINE)
    if h3_m:
        out["LEDE_QUALIDADE"] = body[: h3_m.start()].strip()
    elif list_start_m:
        out["LEDE_QUALIDADE"] = body[: list_start_m.start()].strip()
    else:
        out["LEDE_QUALIDADE"] = body.strip().split("\n\n")[0]

    # Critérios numerados "1. DTO-01 — ..." OU "1. **DTO-01** ..."
    dto_matches = re.findall(
        r"^\s*\d+\.\s+(.+?)(?=^\s*\d+\.|^###|^##|\Z)",
        body, re.DOTALL | re.MULTILINE,
    )
    for n in range(5):
        slot = f"DTO_0{n+1}"
        out[slot] = dto_matches[n].strip() if n < len(dto_matches) else ""

    # 10. Documentos Relacionados — tabela 3 col (Código, Título, Tipo) — 4 slots
    body = sections.get("10.", "")
    rel_rows = extract_md_table(body)
    for n in range(4):
        slot = n + 1
        if n < len(rel_rows) and len(rel_rows[n]) >= 3:
            out[f"REL_CODIGO_{slot}"] = rel_rows[n][0]
            out[f"REL_NOME_{slot}"]   = rel_rows[n][1]
            out[f"REL_TIPO_{slot}"]   = rel_rows[n][2]
        else:
            out[f"REL_CODIGO_{slot}"] = ""
            out[f"REL_NOME_{slot}"]   = ""
            out[f"REL_TIPO_{slot}"]   = ""
    # CODIGO_ESP — primeiro doc relacionado que começa com "ESP-"
    esp_code = ""
    for row in rel_rows:
        if row and row[0].startswith("ESP-"):
            esp_code = row[0]
            break
    out["CODIGO_ESP"] = esp_code

    # ALTERACOES_VERSAO — última seção (controle de versões via tabela após "---")
    full_text = path.read_text(encoding="utf-8")
    cv_m = re.search(r"Controle de Vers[oõ]es[^\n]*\n(.+?)(?=\Z)", full_text, re.DOTALL | re.IGNORECASE)
    if cv_m:
        cv_rows = extract_md_table(cv_m.group(1))
        if cv_rows and len(cv_rows[0]) >= 4:
            out["ALTERACOES_VERSAO"] = cv_rows[0][3]

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
    """Mapeia YAML + (opcional) MD → dict com os 149 placeholders."""
    i = data["identity"]
    l = data["lifecycle"]
    g = data["governance"]
    p = data["presentation"]

    date_label = l.get("date_label", str(l.get("date", "")))
    next_label = l.get("nextReview_label", str(l.get("nextReview", "")))

    nome_e, cargo_e = split_name_cargo(g.get("elaboradoPor", ""))
    nome_a, cargo_a = split_name_cargo(g.get("aprovadoPor", ""))

    # parent fallback (manual sempre tem parent — POL ou MAN sibling)
    parent_raw = g.get("parent")
    if parent_raw is None or (isinstance(parent_raw, dict) and not parent_raw.get("code")):
        parent = {
            "code": "N/A",
            "title": "Manual raiz",
        }
    else:
        parent = parent_raw if isinstance(parent_raw, dict) else {}

    cover_pieces = split_cover_title(p["title_full"]["parts"])

    # Processo macro — manual-específico
    process_owner_full = g.get("process_owner", g.get("aprovadoPor", ""))
    nome_po, cargo_po = split_name_cargo(process_owner_full)
    codigo_processo = g.get("codigo_processo", "")
    if not codigo_processo:
        procs = g.get("processos") or []
        codigo_processo = procs[0] if procs else ""

    out: dict = {
        "CODIGO_DOCUMENTO": i["code"],
        "TIPO_DOCUMENTO": i.get("tipo_label", i["tipo"]),
        "AREA_DOCUMENTO": i.get("area_label", i["area"]),
        "TITULO_DOCUMENTO": p["title_short"],
        "NOME_DA_EMPRESA": "M7 Investimentos",
        "VERSAO_CURTA": i["version"],
        "VERSAO_COMPLETA": i.get("version_label", i["version"]),
        "CLASSIFICACAO_DOCUMENTO": i.get("classif_label", i["classif"]),
        "TOTAL_PAGINAS": str(i.get("pages", 11)),
        "DATA_REFERENCIA": date_label,
        "DATA_VIGENCIA": date_label,
        "DATA_PROXIMA_REVISAO": next_label,
        "COVER_SUBTITULO": p["subtitle"],
        "NOME_ELABORADOR": nome_e,
        "CARGO_ELABORADOR": cargo_e,
        "NOME_APROVADOR": nome_a,
        "CARGO_APROVADOR": cargo_a,
        "CODIGO_DOC_SUPERIOR": parent.get("code", ""),
        "TITULO_DOC_SUPERIOR": parent.get("title", ""),
        "ALTERACOES_VERSAO": "Versão inicial.",
        # Processo macro — manual-específico
        "NOME_PROCESSO": g.get("nome_processo", p.get("title_short", "")),
        "CODIGO_PROCESSO": codigo_processo,
        "PROCESS_OWNER": nome_po,
        "PROCESS_OWNER_CARGO": cargo_po,
    }
    out.update(cover_pieces)

    # Pre-popular todos os 149 placeholders com string vazia para garantir
    # que residuals fiquem zerados se o MD não preencher algum.
    content_keys = (
        ["TEXTO_OBJETIVO_P1", "TEXTO_OBJETIVO_P2", "LEDE_ESCOPO"]
        + [f"ESCOPO_INCLUSAO_{n}" for n in range(1, 4)]
        + [f"ESCOPO_EXCLUSAO_{n}" for n in range(1, 4)]
        + [f"DEF_TERMO_{n}" for n in range(1, 11)]
        + [f"DEF_TEXTO_{n}" for n in range(1, 11)]
        + ["LEDE_VISAO_GERAL", "MISSAO_PROCESSO", "TEXTO_INTERFACES"]
        + [f"SIPOC_S_{n}" for n in range(1, 4)]
        + [f"SIPOC_I_{n}" for n in range(1, 4)]
        + [f"SIPOC_P_{n}" for n in range(1, 5)]
        + [f"SIPOC_O_{n}" for n in range(1, 4)]
        + [f"SIPOC_C_{n}" for n in range(1, 4)]
        + ["BPMN_DIAGRAMA_TITULO", "BPMN_CAPTION",
           "BPMN_EVT_INICIO", "BPMN_EVT_FIM_1", "BPMN_EVT_FIM_2",
           "BPMN_TASK_1", "BPMN_TASK_2", "BPMN_TASK_3", "BPMN_TASK_4",
           "BPMN_GATEWAY_1",
           "BPMN_NARRATIVA_1", "BPMN_NARRATIVA_2", "BPMN_NARRATIVA_3"]
        + ["LEDE_REGRAS", "REGRAS_TEMA_1", "REGRAS_TEMA_2"]
        + [f"REGRA_0{n}" for n in range(1, 7)]
        + ["EXCECAO_1", "EXCECAO_2", "APROVADOR_EXCECAO_1", "APROVADOR_EXCECAO_2"]
        + ["LEDE_PAPEIS"]
        + [f"RACI_PAPEL_{n}" for n in range(1, 6)]
        + [f"RACI_ATIV_{n}" for n in range(1, 6)]
        + ["LEDE_INDICADORES"]
        + [f"KPI_{n}_{fld}" for n in range(1, 3)
           for fld in ("NOME", "FORMULA", "META", "FREQ", "FONTE")]
        + [f"PPI_{n}_{fld}" for n in range(1, 3)
           for fld in ("NOME", "FORMULA", "META", "FREQ", "FONTE")]
        + ["LEDE_CRONOGRAMA"]
        + [f"CRONO_{cad}_{fld}" for cad in ("DIARIO", "SEMANAL", "MENSAL", "TRIMESTRAL", "SEMESTRAL")
           for fld in ("RITUAL", "OUT")]
        + ["LEDE_QUALIDADE"]
        + [f"DTO_0{n}" for n in range(1, 6)]
        + [f"REL_CODIGO_{n}" for n in range(1, 5)]
        + [f"REL_NOME_{n}" for n in range(1, 5)]
        + [f"REL_TIPO_{n}" for n in range(1, 5)]
        + ["CODIGO_ESP"]
    )
    for k in content_keys:
        out.setdefault(k, "")

    if content_md and content_md.exists():
        out.update(parse_content_md(content_md))

    # Aplicar markdown inline (bold/italic/link) nos campos de texto puro
    inline_md_fields = (
        ["TEXTO_OBJETIVO_P1", "TEXTO_OBJETIVO_P2", "LEDE_ESCOPO"]
        + [f"ESCOPO_INCLUSAO_{n}" for n in range(1, 4)]
        + [f"ESCOPO_EXCLUSAO_{n}" for n in range(1, 4)]
        + [f"DEF_TEXTO_{n}" for n in range(1, 11)]
        + ["LEDE_VISAO_GERAL", "MISSAO_PROCESSO", "TEXTO_INTERFACES"]
        + ["LEDE_REGRAS"]
        + [f"REGRA_0{n}" for n in range(1, 7)]
        + ["EXCECAO_1", "EXCECAO_2"]
        + ["LEDE_PAPEIS", "LEDE_INDICADORES", "LEDE_CRONOGRAMA", "LEDE_QUALIDADE"]
        + [f"BPMN_NARRATIVA_{n}" for n in range(1, 4)]
        + [f"DTO_0{n}" for n in range(1, 6)]
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
    """Remove blocos de slot vazios deixados pelo template HTML estático (v1.0 manual).

    Manual tem estruturas diferentes da política:
      - RACI: matriz fixa 5×5, células vazias ficam visíveis (sem cleanup
        agressivo, autor pode declarar "—" se quiser)
      - BPMN: SVG fixo no template, placeholders vazios apenas mostram labels
        vazios (cleanup não trivial em SVG)
      - SIPOC: 5 cols × 3-4 itens cada — cleanup remove <li> com texto vazio
      - DOC_REL: tabela 4 rows, cleanup remove rows totalmente vazias
      - DTO: lista 5 critérios, cleanup remove <li> vazios

    Idempotente: rodar 2x produz mesmo output.
    """
    # 1. SIPOC — remove <li> vazios em colunas .sipoc .col ul li
    html = re.sub(
        r'\s*<li>\s*</li>',
        '',
        html,
    )

    # 2. DOC_REL — remove <tr> com todas as células vazias (templ usa data-table="doc-related" se existir, senão linha por linha)
    html = re.sub(
        r'\s*<tr>\s*<td>\s*</td>\s*<td>\s*</td>\s*<td>\s*</td>\s*</tr>',
        '',
        html,
    )
    html = re.sub(
        r'\s*<tr>\s*<td>\s*<span class="mono">\s*</span>\s*</td>\s*'
        r'<td>\s*</td>\s*<td>\s*</td>\s*</tr>',
        '',
        html,
    )

    # 3. KPI/PPI cards com .name vazio (sem indicador declarado)
    html = re.sub(
        r'\s*<div class="kpi-card(?:\s+ppi)?">\s*'
        r'<span class="label">[^<]*</span>\s*'
        r'<div class="name">\s*</div>.*?</div>\s*</div>',
        '',
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
    parser.add_argument("--content", help="MD com conteúdo das 10 seções")
    parser.add_argument("--basename")
    parser.add_argument("--template")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--no-inline", action="store_true",
                        help="Não inlinear CSS/fonts/logos (debug)")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    template_path = Path(args.template) if args.template else skill_dir / "assets" / "manual-m7-template.html"
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

    # Verificações soft (warnings, não bloqueiam) específicas de MAN
    tipo = data.get("identity", {}).get("tipo")
    if tipo == "MAN":
        revFreq = data.get("lifecycle", {}).get("revisaoFreq")
        if revFreq and revFreq != "Semestral":
            sys.stderr.write(
                f"⚠  lifecycle.revisaoFreq='{revFreq}' (default MAN=Semestral)\n"
            )
        aprovRole = data.get("governance", {}).get("aprovador_role")
        if aprovRole and aprovRole != "Head de área":
            sys.stderr.write(
                f"⚠  governance.aprovador_role='{aprovRole}' (default MAN=Head de área)\n"
            )

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
            "references/component-catalog-manual.md\n"
        )
        return 1

    html = template_path.read_text(encoding="utf-8")

    for key, val in placeholders.items():
        # Skip chaves internas (prefixo _) e valores não-string.
        if key.startswith("_") or not isinstance(val, str):
            continue
        html = html.replace("{{" + key + "}}", val)

    # inline_assets DEPOIS da substituição
    if not args.no_inline:
        html = inline_assets(html, skill_dir / "assets")

    # Pós-processamento: injetar classes M7 em tags da markdown lib + inline
    # imagens externas referenciadas no MD do autor.
    html = inject_m7_classes(html)
    if content_md and content_md.exists():
        html = inline_external_images(html, content_md.parent)

    # Auto-cleanup de slots vazios (DOC_REL, SIPOC li, KPI/PPI sem nome)
    html = _strip_empty_slots(html)

    residuals = set(re.findall(r"\{\{([A-Z_0-9]+)\}\}", html))
    warnings: list = []
    if residuals:
        warnings.append(f"placeholders não substituídos: {sorted(residuals)}")
    if not args.no_inline and re.search(r'(?:href|src)="(?:assets/|fonts/|m7-tokens\.css)', html):
        warnings.append("paths relativos restantes após inline")

    # v1.0 — validação pós-render do HTML final
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
            "da Fase 2 contra references/component-catalog-manual.md.\n"
        )
        return 1

    html_out.write_text(html, encoding="utf-8")

    # Stub do .review.md (gate de design review obrigatório)
    review_path = output_dir / f"{basename}.review.md"
    code = data.get("identity", {}).get("code", "MAN-UNKNOWN")
    titulo = data.get("presentation", {}).get("title_short", "")
    review_path.write_text(
        f"# Design Review: {code} · {titulo}\n\n"
        f"**Arquivo**: `{html_out}`\n"
        f"**Status**: PENDING — invoque o agente `manual-design-reviewer`\n"
        f"**Score esperado para entrega**: ≥ B\n\n"
        "---\n\n"
        "Este arquivo é um stub gerado pelo script `generate-html-yaml.py`.\n"
        "O conteúdo real do design review é produzido pelo agente\n"
        "`manual-design-reviewer` ao analisar o HTML acima.\n\n"
        "Para preencher este review:\n\n"
        "1. Invoque o agente: `Task(subagent_type='manual-design-reviewer', ...)`\n"
        f"2. Forneça os caminhos do HTML, YAML, MD-fonte e code `{code}`\n"
        "3. O agente sobrescreverá este arquivo com o relatório completo\n"
        "   (Score A/B/C/D + issues categorizadas em 9 dimensões + Quick Fix CSS)\n"
        "4. Score < B bloqueia a entrega — corrija o MD/BRIEFING e re-execute\n",
        encoding="utf-8",
    )

    size_kb = html_out.stat().st_size // 1024
    print("✓ Gerado:")
    print(f"   {yaml_out}")
    print(f"   {html_out}  ({size_kb} KB)")
    print(f"   {review_path}  (stub — invoque manual-design-reviewer)")
    for w in warnings:
        sys.stderr.write(f"⚠  {w}\n")
    return 0 if not residuals else 3


if __name__ == "__main__":
    sys.exit(main())
