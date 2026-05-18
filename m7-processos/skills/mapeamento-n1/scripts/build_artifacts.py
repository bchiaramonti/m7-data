#!/usr/bin/env python3
"""mapeamento-n1 · gera N1, N2, N3 e N4 a partir do BRIEFING.md.

Le BRIEFING.md, valida com check_briefing.py, e gera os artefatos solicitados
em `artefatos_a_gerar`. Para N4, invoca build_n4.py + render_pdf.py.

Uso:
    python3 build_artifacts.py <briefing.md> <output_dir>
    python3 build_artifacts.py <briefing.md> <output_dir> --skip-pdf
    python3 build_artifacts.py <briefing.md> <output_dir> --skill-dir <path>

Pipeline:
    BRIEFING.md
      ├─ N1 → cadeia-de-valor-{slug}.html
      ├─ N2 → missao-do-processo-{slug}.html       (se em artefatos)
      ├─ N3 → mapa-de-interdependencia-{slug}.html (se em artefatos)
      └─ N4 → politica-{slug}.html                 (se em artefatos)
              └─ usuario exporta PDF via window.print() no navegador

Exit codes:
    0 = ok
    1 = erro de geracao
    2 = erro de uso
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("ERRO: PyYAML nao instalado.\n")
    sys.exit(2)


# ============================================================================
# Constantes
# ============================================================================

# data-layer no N3 = derivado de processos[].camada + n3.coluna
LAYER_MAP = {
    "gerencial": "G",
    "front": "P-front",
    "nucleo-l": "P-core",
    "nucleo-r": "P-core",
    "back": "P-back",
    "apoio": "A",
}

EDGE_CLASS_MAP = {
    ("cliente", "strong"): "e-cliente-strong",
    ("cliente", "mid"):    "e-cliente-mid",
    ("cliente", "soft"):   "e-cliente-soft",
    ("info", None):        "e-info",
    ("decisao", None):     "e-decisao",
}


# ============================================================================
# Helpers
# ============================================================================


def parse_briefing(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not m:
        raise ValueError("Frontmatter YAML nao encontrado.")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def escape_html(s) -> str:
    if not isinstance(s, str):
        s = str(s)
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def extract_section(body: str, heading: str) -> str:
    pattern = rf"##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|$)"
    m = re.search(pattern, body, re.DOTALL)
    if not m:
        return ""
    content = m.group(1).strip()
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL).strip()
    return content


def copy_assets(skill_dir: Path, output_dir: Path) -> None:
    """Copia CSS + fonts/ + assets/ para o diretorio de output.

    Idempotente: re-runs sobrescrevem CSS (preservando permissoes write)
    e mantem fonts/assets ja copiados (sao estaticos).
    """
    import os
    templates_dir = skill_dir / "templates"
    for css in ["m7-tokens.css", "m7-header-dark.css", "m7-print.css"]:
        src = templates_dir / css
        if not src.is_file():
            continue
        dst = output_dir / css
        # Re-runs: shutil.copy2 falha se dst e read-only.
        # Garantir write antes do overwrite. unlink() tambem funciona,
        # mas chmod preserva o stat history pra debugging.
        if dst.exists():
            os.chmod(dst, 0o644)
        shutil.copy2(src, dst)
    for sub in ["fonts", "assets"]:
        src = templates_dir / sub
        dst = output_dir / sub
        if src.is_dir() and not dst.exists():
            shutil.copytree(src, dst)


def percent_to_svg(left_pct: float, top_pct: float,
                   svg_w: int = 1000, svg_h: int = 600) -> tuple[float, float]:
    """Converte % do canvas neural para coordenadas no viewBox SVG."""
    return (left_pct / 100.0 * svg_w, top_pct / 100.0 * svg_h)


def bezier_path(x1: float, y1: float, x2: float, y2: float) -> str:
    """Curva Bezier suave entre dois pontos."""
    cx1 = x1 + (x2 - x1) * 0.4
    cy1 = y1
    cx2 = x2 - (x2 - x1) * 0.4
    cy2 = y2
    return f"M {x1:.0f} {y1:.0f} C {cx1:.0f} {cy1:.0f}, {cx2:.0f} {cy2:.0f}, {x2:.0f} {y2:.0f}"


def validate_briefing(briefing_path: Path, skill_dir: Path) -> bool:
    """Roda check_briefing.py. Devolve True se ok=true."""
    check_script = skill_dir / "scripts" / "check_briefing.py"
    if not check_script.is_file():
        sys.stderr.write(f"WARN: check_briefing.py nao encontrado em {check_script}\n")
        return True

    result = subprocess.run(
        [sys.executable, str(check_script), str(briefing_path), "--json"],
        capture_output=True, text=True,
    )
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        sys.stderr.write(f"WARN: check_briefing.py output nao parseado:\n{result.stdout[:200]}\n")
        return True
    if not data.get("ok"):
        sys.stderr.write("BLOQUEADORES detectados:\n")
        for b in data.get("bloqueadores", []):
            sys.stderr.write(f"  [{b['rule_id']}] {b['where']}: {b['message']}\n")
        return False
    avisos = data.get("avisos", [])
    if avisos:
        sys.stderr.write(f"AVISOS ({len(avisos)}, geracao prossegue):\n")
        for a in avisos[:5]:
            sys.stderr.write(f"  [{a['rule_id']}] {a['where']}\n")
        if len(avisos) > 5:
            sys.stderr.write(f"  ... mais {len(avisos)-5} aviso(s)\n")
    return True


# ============================================================================
# Build N1
# ============================================================================


def _render_process_box(p: dict, variante: str = "A") -> str:
    """Renderiza um <div class='process-box [highlight|blue-accent]'> completo.

    Usado para inserir processos extras alem do que o template hardcoded
    suporta (P1-P9 + G1-G4 + A1-A5). Tooltip respeita formato gerencial
    (3 linhas com 'Freq: X' na ultima) vs primario/apoio (ate 3 linhas).
    """
    codigo = escape_html(p.get("codigo", ""))
    nome = escape_html(p.get("nome", ""))
    tooltip = p.get("tooltip") or []

    cls = "process-box"
    if p.get("highlight"):
        cls += " highlight"
    elif p.get("blue_accent"):
        cls += " blue-accent"

    if variante == "B":
        # Variante linear: tooltip e uma string unica
        tooltip_html = "<br>".join(escape_html(l) for l in tooltip if l)
    else:
        # Variante A: tooltip e 3 linhas; gerencial inclui 'Freq: X'
        if p.get("camada") == "gerencial":
            freq = p.get("frequencia", "")
            linhas = (tooltip + ["", "", ""])[:2]
            tooltip_html = "<br>".join(
                escape_html(l) for l in [*linhas, f"Freq: {freq}"] if l
            )
        else:
            linhas = (tooltip + ["", "", ""])[:3]
            tooltip_html = "<br>".join(escape_html(l) for l in linhas if l)

    return (
        f'<div class="{cls}">'
        f'<div class="code">{codigo}</div>'
        f'<div class="name">{nome}</div>'
        f'<div class="tooltip">{tooltip_html}</div>'
        f'</div>'
    )


def _layer_by_label(soup, text: str):
    """Encontra <div class='layer'> cujo h3 contem o texto.

    Tolera variacao de case + acento. Devolve o elemento layer ou None.
    """
    text_norm = text.lower()
    for layer in soup.find_all("div", class_="layer"):
        h3 = layer.find("h3")
        if h3 and text_norm in h3.get_text(strip=True).lower():
            return layer
    return None


def _rebuild_container(container, processos: list, variante: str) -> None:
    """Limpa process-boxes do container e re-renderiza a partir do briefing.

    Preserva outros elementos filhos (ex.: .verticais-label, flow-arrow svg).
    """
    if container is None:
        return
    # Remove apenas os .process-box (preserva .verticais-label etc.)
    for pb in container.find_all("div", class_="process-box", recursive=False):
        pb.decompose()
    # Insere process-boxes do briefing na ordem
    from bs4 import BeautifulSoup
    for p in processos:
        html = _render_process_box(p, variante)
        new = BeautifulSoup(html, "html.parser")
        for child in list(new.contents):
            container.append(child)


def _inject_n1_processes(template_str: str, briefing_fm: dict) -> str:
    """Reconstroi dinamicamente os containers de processos no N1.

    Trata overflow alem dos slots hardcoded (P1-P9, G1-G4, A1-A5) e
    respeita as classificacoes camada/subcamada do briefing — fix do
    Bug 1 do report v2.0.3 (BRIEFINGs com >9 primarios truncavam).

    Para o BRIEFING M7 atual (12 primarios: P1,P2=front, P3-P11=nucleo,
    P12=back) o render dinamico re-organiza P9 do back-end hardcoded
    para o nucleo (subcamada correta) e injeta P12 no back-end.
    """
    from bs4 import BeautifulSoup
    n1 = briefing_fm.get("n1", {})
    variante = n1.get("variante", "A")
    processos = briefing_fm.get("processos") or []

    gerenciais = [p for p in processos if p.get("camada") == "gerencial"]
    primarios = [p for p in processos if p.get("camada") == "primario"]
    apoio = [p for p in processos if p.get("camada") == "apoio"]

    soup = BeautifulSoup(template_str, "html.parser")

    # Gerenciais — sempre flat
    ger_layer = _layer_by_label(soup, "gerenciais")
    if ger_layer:
        ger_content = ger_layer.find("div", class_="lane-content")
        _rebuild_container(ger_content, gerenciais, variante)

    # Apoio — sempre flat
    apoio_layer = _layer_by_label(soup, "apoio")
    if apoio_layer:
        apoio_content = apoio_layer.find("div", class_="lane-content")
        _rebuild_container(apoio_content, apoio, variante)

    # Primarios — variante A: front+nucleo+back; variante B: flat
    prim_layer = _layer_by_label(soup, "primários") or _layer_by_label(soup, "primarios")
    if not prim_layer:
        return str(soup)

    if variante == "A":
        # Front-end: subcamada=front; Nucleo: subcamada=nucleo; Back: subcamada=back
        front = [p for p in primarios if p.get("subcamada") == "front"]
        nucleo = [p for p in primarios if p.get("subcamada") == "nucleo"]
        back = [p for p in primarios if p.get("subcamada") == "back"]
        # Fallback: primarios sem subcamada vao para nucleo (caso comum)
        sem_sc = [p for p in primarios if not p.get("subcamada")]
        nucleo = nucleo + sem_sc

        front_div = prim_layer.find("div", class_="front-end")
        _rebuild_container(front_div, front, variante)
        grid_div = prim_layer.find("div", class_="verticais-grid")
        _rebuild_container(grid_div, nucleo, variante)
        back_div = prim_layer.find("div", class_="back-end")
        _rebuild_container(back_div, back, variante)
    else:
        # Variante linear: tudo flat dentro de lane-content
        prim_content = prim_layer.find("div", class_="lane-content")
        _rebuild_container(prim_content, primarios, variante)

    return str(soup)


def build_n1(briefing_fm: dict, body_md: str, skill_dir: Path, output_dir: Path) -> Path:
    """Gera cadeia-de-valor-{slug}.html a partir do BRIEFING."""
    empresa = briefing_fm.get("empresa", {})
    slug = empresa.get("slug", "empresa")
    n1 = briefing_fm.get("n1", {})
    variante = n1.get("variante", "A")
    contagens = n1.get("contagens", {})
    processos = briefing_fm.get("processos") or []

    # Selecionar template
    template_name = (
        "template-cadeia-de-valor.html" if variante == "A"
        else "template-cadeia-de-valor--linear.html"
    )
    template = (skill_dir / "templates" / template_name).read_text(encoding="utf-8")

    # Substituicoes globais
    artefatos = set(briefing_fm.get("artefatos_a_gerar") or [])
    n2_link = (f'<a class="tab" href="missao-do-processo-{slug}.html">Missão do processo</a>'
               if "n2" in artefatos else
               '<div class="tab">Missão do processo</div>')
    n3_link = (f'<a class="tab" href="mapa-de-interdependencia-{slug}.html">Mapa de interdependência</a>'
               if "n3" in artefatos else
               '<div class="tab">Mapa de interdependência</div>')
    n4_link = (f'<a class="tab" href="politica-{slug}.html">Política <span class="num">DOC</span></a>'
               if "n4-pdf" in artefatos else
               '<div class="tab">Política <span class="num">DOC</span></div>')

    # Total de verticais (variante A: subcamada=nucleo, variante B: total primarios)
    if variante == "A":
        n_verticais = sum(1 for p in processos
                          if p.get("camada") == "primario" and p.get("subcamada") == "nucleo")
    else:
        n_verticais = contagens.get("primarios", 0)

    replacements = {
        "{{NOME_DA_EMPRESA}}": escape_html(empresa.get("nome", "")),
        "{{AREA_DOCUMENTO}}": escape_html(briefing_fm.get("area_documento", "")),
        "{{DATA_REFERENCIA}}": escape_html(briefing_fm.get("data_referencia", "")),
        "{{LEDE_DOCUMENTO}}": escape_html(extract_section(body_md, "Lede do documento")),
        "{{TOTAL_PROCESSOS}}": str(n1.get("total_processos", len(processos))),
        "{{N_VERTICAIS}}": str(n_verticais),
        "{{VERSAO_CURTA}}": escape_html(briefing_fm.get("versao", "")),
        "{{N_GERENCIAIS}}": str(contagens.get("gerenciais", 0)),
        "{{N_PRIMARIOS}}": str(contagens.get("primarios", 0)),
        "{{N_APOIO}}": str(contagens.get("apoio", 0)),
    }

    # Variante A: rotulo do nucleo
    if variante == "A":
        replacements["{{ROTULO_NUCLEO}}"] = escape_html(n1.get("rotulo_nucleo", "Verticais"))

    # Substituir tabs (template ja tem <a class="tab" href="..."> ou <div class="tab">)
    template = re.sub(
        r'<a class="tab" href="template-missao-do-processo\.html">Missão do processo</a>',
        n2_link, template,
    )
    template = re.sub(
        r'<a class="tab" href="template-mapa-de-interdependencia\.html">Mapa de interdependência</a>',
        n3_link, template,
    )
    template = re.sub(
        r'<a class="tab" href="template-politica\.html">Política <span class="num">DOC</span></a>',
        n4_link, template,
    )
    # Variante linear tem div ao inves de a para Mapa (decisao do design oficial)
    template = re.sub(
        r'<div class="tab">Missão do processo</div>',
        n2_link if "n2" in artefatos else '<div class="tab">Missão do processo</div>',
        template,
    )
    template = re.sub(
        r'<div class="tab">Mapa de interdependência</div>',
        n3_link if "n3" in artefatos else '<div class="tab">Mapa de interdependência</div>',
        template,
    )

    # Por processo: substitui placeholders por codigo
    for p in processos:
        codigo = p.get("codigo", "")
        nome = p.get("nome", "")
        tooltip = p.get("tooltip") or []
        # Tooltip linhas (até 3)
        linhas = (tooltip + ["", "", ""])[:3]
        replacements[f"{{{{NOME_PROCESSO_{codigo}}}}}"] = escape_html(nome)
        replacements[f"{{{{NOME_{codigo}}}}}"] = escape_html(nome)  # variante linear
        replacements[f"{{{{LINHA_1_{codigo}}}}}"] = escape_html(linhas[0])
        replacements[f"{{{{LINHA_2_{codigo}}}}}"] = escape_html(linhas[1])
        replacements[f"{{{{LINHA_3_{codigo}}}}}"] = escape_html(linhas[2])
        if p.get("camada") == "gerencial":
            replacements[f"{{{{FREQUENCIA_{codigo}}}}}"] = escape_html(p.get("frequencia", ""))
        # Variante linear: tooltip completa em uma linha
        tooltip_full = "<br>".join(escape_html(l) for l in tooltip)
        replacements[f"{{{{TOOLTIP_{codigo}}}}}"] = tooltip_full

    for k, v in replacements.items():
        template = template.replace(k, v)

    # Render dinamico dos containers de processos: reconstroi front-end,
    # verticais-grid, back-end (variante A) ou primarios linear (variante B)
    # + gerenciais + apoio a partir do briefing. Resolve overflow (>9
    # primarios, >4 gerenciais, >5 apoio) e respeita subcamada=front/nucleo/
    # back declarada no BRIEFING (independente de qual placeholder foi usado
    # nas substituicoes string-based acima).
    #
    # Tambem aplica classes .highlight e .blue-accent corretamente atraves
    # de _render_process_box, dispensando o passo de regex pos-substituicao.
    template = _inject_n1_processes(template, briefing_fm)

    # Salvar
    output_path = output_dir / f"cadeia-de-valor-{slug}.html"
    output_path.write_text(template, encoding="utf-8")
    return output_path


# ============================================================================
# Build N2 (sidebar + paineis SIPOC)
# ============================================================================


def build_n2(briefing_fm: dict, body_md: str, skill_dir: Path, output_dir: Path) -> Path:
    empresa = briefing_fm.get("empresa", {})
    slug = empresa.get("slug", "empresa")
    n1 = briefing_fm.get("n1", {})
    contagens = n1.get("contagens", {})
    processos = briefing_fm.get("processos") or []
    artefatos = set(briefing_fm.get("artefatos_a_gerar") or [])

    template = (skill_dir / "templates" / "template-missao-do-processo.html").read_text(encoding="utf-8")

    # Header global
    n_verticais = sum(1 for p in processos
                      if p.get("camada") == "primario" and p.get("subcamada") == "nucleo")
    if n1.get("variante") == "B":
        n_verticais = contagens.get("primarios", 0)

    n1_link = f'<a class="tab" href="cadeia-de-valor-{slug}.html">Visao geral</a>'
    n3_link = (f'<a class="tab" href="mapa-de-interdependencia-{slug}.html">Mapa de interdependencia</a>'
               if "n3" in artefatos else
               '<div class="tab">Mapa de interdependencia</div>')

    # Replacements globais (chama mesmos placeholders)
    template = template.replace("{{NOME_DA_EMPRESA}}", escape_html(empresa.get("nome", "")))
    template = template.replace("{{AREA_DOCUMENTO}}", escape_html(briefing_fm.get("area_documento", "")))
    template = template.replace("{{DATA_REFERENCIA}}", escape_html(briefing_fm.get("data_referencia", "")))
    template = template.replace("{{TOTAL_PROCESSOS}}", str(n1.get("total_processos", len(processos))))
    template = template.replace("{{N_VERTICAIS}}", str(n_verticais))
    template = template.replace("{{VERSAO_CURTA}}", escape_html(briefing_fm.get("versao", "")))
    template = template.replace("{{LEDE_DOCUMENTO}}", escape_html(extract_section(body_md, "Lede do documento")))

    # Sidebar items + Painel SIPOC: vamos parsear o template para identificar onde injetar
    # Heuristica: no template, ha sidebar com lista de processos e painel de detalhes.
    # Para nao reescrever o template, fazemos uma estrategia simples: o template sera entregue
    # com todos os processos do BRIEFING substituidos diretamente nos placeholders existentes.

    # Estrategia robusta: gerar HTML completo via reescrita das duas areas chave (sidebar + painel)
    # usando BeautifulSoup
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(template, "html.parser")

    # 1) Sidebar: lista os processos agrupados em camadas
    sidebar = soup.find("aside", class_="mp-sidebar") or soup.find("aside")
    if sidebar:
        # Substituir conteudo da sidebar
        sidebar_html = render_n2_sidebar(processos)
        new_sidebar = BeautifulSoup(sidebar_html, "html.parser")
        sidebar.clear()
        for child in list(new_sidebar.contents):
            sidebar.append(child)

    # 2) Paineis SIPOC: o template tem os paineis hardcoded por processo M7 — substituir todos
    # Vou procurar todas <article id="..."> e substituir pelos do BRIEFING
    main_panel = soup.find("main", class_="mp-main") or soup.find("main")
    if main_panel:
        # Limpar artigos existentes (M7 hardcoded)
        for art in main_panel.find_all("article"):
            art.decompose()
        # Adicionar novos
        panels_html = render_n2_panels(processos)
        new_panels = BeautifulSoup(panels_html, "html.parser")
        for child in list(new_panels.contents):
            main_panel.append(child)

    # Tabs — repointar hrefs para os arquivos slug-based.
    # Tab ativa (Missao do processo) usa data-active="true" e fica intocada.
    for tab in soup.find_all(class_="tab"):
        href = tab.get("href", "") or ""
        text = tab.get_text(strip=True).lower()
        if "exemplo-m7-preenchido" in href or "cadeia-de-valor" in href or "visão geral" in text or "visao geral" in text:
            tab["href"] = f"cadeia-de-valor-{slug}.html"
        elif "mapa-de-interdependencia" in href or "mapa" in text:
            if "n3" in artefatos:
                tab["href"] = f"mapa-de-interdependencia-{slug}.html"
            else:
                tab.name = "div"
                if "href" in tab.attrs:
                    del tab.attrs["href"]
        elif "politica" in href or "política" in text:
            if "n4-pdf" in artefatos:
                tab["href"] = f"politica-{slug}.html"
            else:
                tab.name = "div"
                if "href" in tab.attrs:
                    del tab.attrs["href"]

    template = str(soup)
    output_path = output_dir / f"missao-do-processo-{slug}.html"
    output_path.write_text(template, encoding="utf-8")
    return output_path


def _camada_tag(camada: str, subcamada: str | None) -> str:
    """Texto do .mp-layer-tag a partir de camada + subcamada."""
    if camada == "gerencial":
        return "Camada gerencial"
    if camada == "apoio":
        return "Camada de apoio"
    if camada == "primario":
        if subcamada == "front":
            return "Camada primária · Front-end"
        if subcamada == "nucleo":
            return "Camada primária · Vertical"
        if subcamada == "back":
            return "Camada primária · Back-end"
        return "Camada primária"
    return ""


def render_n2_sidebar(processos: list) -> str:
    """HTML da sidebar do N2 — botoes mp-item agrupados por camada.

    Estrutura esperada pela CSS + JS do template-missao-do-processo.html:

        <div class="mp-group">
          <div class="mp-group-label">Gerenciais <span class="count">4</span></div>
          <button class="mp-item active" data-process-id="G1">
            <span class="code">G1</span><span>Planejamento Estrategico</span>
          </button>
          ...
        </div>

    Apenas o PRIMEIRO botao do PRIMEIRO grupo recebe `.active` (estado inicial
    visivel). JS do template toggles `.active` no clique e via hash da URL.
    """
    parts = []
    first = True
    for camada, label in [("gerencial", "Gerenciais"),
                          ("primario", "Primários"),
                          ("apoio", "Apoio")]:
        items = [p for p in processos if p.get("camada") == camada]
        if not items:
            continue
        parts.append(f'    <div class="mp-group">')
        parts.append(
            f'      <div class="mp-group-label">{escape_html(label)} '
            f'<span class="count">{len(items)}</span></div>'
        )
        for p in items:
            codigo = p.get("codigo", "")
            nome = p.get("nome", "")
            active_cls = " active" if first else ""
            first = False
            parts.append(
                f'      <button class="mp-item{active_cls}" data-process-id="{escape_html(codigo)}">'
                f'<span class="code">{escape_html(codigo)}</span>'
                f'<span>{escape_html(nome)}</span></button>'
            )
        parts.append("    </div>")
    return "\n" + "\n".join(parts) + "\n  "


def _render_n2_panel_sipoc(codigo: str, nome: str, camada_tag: str,
                            owner: str, verbo: str, objeto: str, finalidade: str,
                            inputs: list, outputs: list, is_active: bool) -> str:
    """Renderiza um <article class='mp-detail [active]' id='detail-{codigo}'> com SIPOC completo."""
    active_cls = " active" if is_active else ""
    # Limpa "para " inicial em finalidade — template ja tem "para" inline na missao
    finalidade_clean = re.sub(r"^para\s+", "", finalidade, flags=re.IGNORECASE).strip()
    chips_in = "\n            ".join(
        f'<span class="mp-chip">{escape_html(c)}</span>'
        for c in inputs
    )
    chips_out = "\n            ".join(
        f'<span class="mp-chip">{escape_html(c)}</span>'
        for c in outputs
    )
    arrow_svg = (
        '<svg viewBox="0 0 24 24"><path d="M5 12h14m-6-6l6 6-6 6"/></svg>'
    )
    # Constroi a missao no formato esperado: <span class="verb">VERBO</span> objeto <em>finalidade</em>
    # Apenas a finalidade (sem o "para") fica em <em>. O "para" e literal no template.
    if finalidade_clean:
        missao_html = (
            f'<span class="verb">{escape_html(verbo)}</span> {escape_html(objeto)} '
            f'<em>para {escape_html(finalidade_clean)}.</em>'
        )
    else:
        missao_html = (
            f'<span class="verb">{escape_html(verbo)}</span> {escape_html(objeto)}.'
        )
    return f"""    <article class="mp-detail{active_cls}" id="detail-{escape_html(codigo)}">
      <div class="mp-headline">
        <div class="left">
          <div class="mp-layer-tag">{escape_html(camada_tag)}</div>
          <h2 class="mp-process-name"><span class="code">{escape_html(codigo)}</span>{escape_html(nome)}</h2>
        </div>
        <div class="mp-owner">
          <span class="label">Owner</span>
          <span class="name">{escape_html(owner)}</span>
        </div>
      </div>

      <div class="sipoc">
        <div class="sipoc-col">
          <div class="sipoc-label">Inputs</div>
          <div class="mp-chips">
            {chips_in}
          </div>
        </div>
        <div class="sipoc-arrow" aria-hidden="true">{arrow_svg}</div>

        <div class="sipoc-col mission">
          <div class="sipoc-label">Missão</div>
          <p class="mp-mission">{missao_html}</p>
        </div>
        <div class="sipoc-arrow" aria-hidden="true">{arrow_svg}</div>

        <div class="sipoc-col">
          <div class="sipoc-label">Outputs</div>
          <div class="mp-chips">
            {chips_out}
          </div>
        </div>
      </div>
    </article>"""


def _render_n2_panel_empty(codigo: str, nome: str, is_active: bool) -> str:
    """Placeholder para processos sem SIPOC preenchido."""
    active_cls = " active" if is_active else ""
    return (
        f'    <article class="mp-detail{active_cls}" id="detail-{escape_html(codigo)}">'
        f'<div class="mp-empty"><div class="ic">{escape_html(codigo)}</div>'
        f'<div>{escape_html(nome)} · A preencher.</div></div></article>'
    )


def render_n2_panels(processos: list) -> str:
    """Cada processo vira <article class='mp-detail' id='detail-{codigo}'>.

    Apenas o PRIMEIRO processo (overall) recebe `.active`. CSS `.mp-detail`
    default e `display: none`; JS toggles `.active` no clique.

    Processos sem SIPOC viram empty placeholder (mas continuam clicaveis pela
    sidebar para preservar coerencia da navegacao).
    """
    panels = []
    first = True
    for p in processos:
        codigo = p.get("codigo", "")
        nome = p.get("nome", "")
        camada = p.get("camada", "")
        subcamada = p.get("subcamada")
        camada_tag = _camada_tag(camada, subcamada)

        sipoc = p.get("sipoc") or {}
        verbo = (sipoc.get("verbo") or "").strip()
        objeto = (sipoc.get("objeto") or "").strip()
        finalidade = (sipoc.get("finalidade") or "").strip()
        inputs = [c for c in (sipoc.get("inputs") or []) if c]
        outputs = [c for c in (sipoc.get("outputs") or []) if c]
        owner = (sipoc.get("owner") or "").strip()

        # Considera SIPOC "preenchido" se tem verbo (campo central)
        if verbo and objeto:
            panels.append(_render_n2_panel_sipoc(
                codigo, nome, camada_tag, owner,
                verbo, objeto, finalidade, inputs, outputs,
                is_active=first,
            ))
        else:
            panels.append(_render_n2_panel_empty(codigo, nome, is_active=first))
        first = False
    return "\n\n" + "\n\n".join(panels) + "\n  "


# ============================================================================
# Build N3 (mapa neural)
# ============================================================================


def build_n3(briefing_fm: dict, body_md: str, skill_dir: Path, output_dir: Path) -> Path:
    empresa = briefing_fm.get("empresa", {})
    slug = empresa.get("slug", "empresa")
    n1 = briefing_fm.get("n1", {})
    processos = briefing_fm.get("processos") or []
    relacoes = briefing_fm.get("relacoes") or []
    artefatos = set(briefing_fm.get("artefatos_a_gerar") or [])

    template = (skill_dir / "templates" / "template-mapa-de-interdependencia.html").read_text(encoding="utf-8")

    # Header globals
    template = template.replace("{{NOME_DA_EMPRESA}}", escape_html(empresa.get("nome", "")))
    template = template.replace("{{AREA_DOCUMENTO}}", escape_html(briefing_fm.get("area_documento", "")))
    template = template.replace("{{DATA_REFERENCIA}}", escape_html(briefing_fm.get("data_referencia", "")))
    template = template.replace("{{TOTAL_RELACOES}}", str(len(relacoes)))
    fricoes_count = sum(1 for p in processos if (p.get("n3") or {}).get("friction", {}).get("is_friction"))
    template = template.replace("{{TOTAL_FRICCOES}}", str(fricoes_count))
    template = template.replace("{{VERSAO_CURTA}}", escape_html(briefing_fm.get("versao", "")))
    template = template.replace("{{DATA_REVISAO}}", escape_html(briefing_fm.get("data_referencia", "")))
    template = template.replace("{{OWNER_DIAGRAMA}}", escape_html(briefing_fm.get("area_documento", "")))

    # Substituir nodes e edges via BeautifulSoup
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(template, "html.parser")

    neural = soup.find("div", class_="neural") or soup.find("div", id="neural")
    if not neural:
        raise ValueError("Template N3 nao tem <div class='neural'>")

    # Limpar nodes e paths existentes (M7 hardcoded)
    for node in neural.find_all("div", class_="node"):
        node.decompose()
    edges = neural.find("svg", class_="edges")
    if edges:
        for path in edges.find_all("path"):
            path.decompose()

    # Adicionar nodes do BRIEFING
    info_panel = neural.find("div", id="info-panel")
    insertion_point = info_panel if info_panel else neural

    nodes_html = render_n3_nodes(processos)
    nodes_soup = BeautifulSoup(nodes_html, "html.parser")
    if info_panel:
        for child in list(nodes_soup.contents):
            info_panel.insert_before(child)
    else:
        for child in list(nodes_soup.contents):
            neural.append(child)

    # Adicionar edges
    if edges:
        edges_html = render_n3_edges(relacoes, processos)
        edges_soup = BeautifulSoup(edges_html, "html.parser")
        for child in list(edges_soup.contents):
            edges.append(child)

    # Substituir RELATIONS no JS
    script_tag = None
    for s in soup.find_all("script"):
        if s.string and "RELATIONS" in s.string:
            script_tag = s
            break
    if script_tag:
        new_relations = render_n3_relations_js(relacoes)
        # Lambda como repl evita interpretar escape sequences (\u, \1, etc.)
        # — JSON com acentos (â, ã, é) produz `â` etc., e `re.sub` com
        # string como repl trataria isso como referencias de grupo invalidas
        # (re.error: bad escape \u). Lambda preserva como literal.
        new_relations_str = f"const RELATIONS = {new_relations};"
        new_script = re.sub(
            r"const RELATIONS = \[.*?\];",
            lambda m: new_relations_str,
            script_tag.string, count=1, flags=re.DOTALL,
        )
        script_tag.string = new_script

    # Tabs — repointar hrefs para os arquivos slug-based.
    for tab in soup.find_all(class_="tab"):
        href = tab.get("href", "") or ""
        text = tab.get_text(strip=True).lower()
        if "missao-do-processo" in href:
            if "n2" in artefatos:
                tab["href"] = f"missao-do-processo-{slug}.html"
            else:
                tab.name = "div"
                if "href" in tab.attrs:
                    del tab.attrs["href"]
        elif "exemplo-m7-preenchido" in href or "cadeia-de-valor" in href:
            tab["href"] = f"cadeia-de-valor-{slug}.html"
        elif "politica" in href or "política" in text:
            if "n4-pdf" in artefatos:
                tab["href"] = f"politica-{slug}.html"
            else:
                tab.name = "div"
                if "href" in tab.attrs:
                    del tab.attrs["href"]

    output_path = output_dir / f"mapa-de-interdependencia-{slug}.html"
    output_path.write_text(str(soup), encoding="utf-8")
    return output_path


def render_n3_nodes(processos: list) -> str:
    """HTML dos nodes (<div class='node'>) com posicoes %."""
    items = []
    for p in processos:
        n3 = p.get("n3") or {}
        if not n3:
            continue
        codigo = p.get("codigo", "")
        nome = p.get("nome", "")
        coluna = n3.get("coluna", "apoio")
        layer = LAYER_MAP.get(coluna, "A")
        pos = n3.get("posicao") or {}
        left = pos.get("left", 50)
        top = pos.get("top", 50)
        # Descricao para o painel info
        desc = ""
        if p.get("sipoc"):
            sipoc = p["sipoc"]
            desc = f"{sipoc.get('verbo', '')} {sipoc.get('objeto', '')}".strip()
        else:
            tooltip = p.get("tooltip") or []
            desc = " ".join(tooltip[:2])

        friction = n3.get("friction") or {}
        is_fr = friction.get("is_friction") and friction.get("text")

        attrs = (f'data-layer="{escape_html(layer)}" '
                 f'data-name="{escape_html(codigo)} · {escape_html(nome)}" '
                 f'data-desc="{escape_html(desc)}"')
        if is_fr:
            attrs += f' data-friction="true" data-friction-text="{escape_html(friction["text"])}"'

        items.append(
            f'<div class="node" {attrs} '
            f'style="left: {left}%; top: {top}%;">{escape_html(codigo)}</div>'
        )
    return "\n".join(items)


def render_n3_edges(relacoes: list, processos: list) -> str:
    """SVG <path> por relacao usando coordenadas % dos processos."""
    pos_by_code = {}
    for p in processos:
        n3 = p.get("n3") or {}
        pos = n3.get("posicao") or {}
        if pos.get("left") is not None and pos.get("top") is not None:
            pos_by_code[p.get("codigo")] = (pos["left"], pos["top"])

    paths = []
    for r in relacoes:
        f, t = r.get("from"), r.get("to")
        if f not in pos_by_code or t not in pos_by_code:
            continue
        x1, y1 = percent_to_svg(*pos_by_code[f])
        x2, y2 = percent_to_svg(*pos_by_code[t])
        kind = r.get("kind", "info")
        forca = r.get("forca") if kind == "cliente" else None
        css_class = EDGE_CLASS_MAP.get((kind, forca))
        if not css_class:
            css_class = "e-info"
        paths.append(f'<path class="{css_class}" d="{bezier_path(x1, y1, x2, y2)}"/>')

    return "\n".join(paths)


def render_n3_relations_js(relacoes: list) -> str:
    """Gera o array JS de relations — mesmo formato esperado pelo template."""
    items = []
    for r in relacoes:
        items.append(
            f'      {{ from: {json.dumps(r.get("from", ""))}, '
            f'to: {json.dumps(r.get("to", ""))}, '
            f'kind: {json.dumps(r.get("kind", ""))}, '
            f'label: {json.dumps(r.get("label", ""))} }}'
        )
    return "[\n" + ",\n".join(items) + "\n    ]"


# ============================================================================
# Politica helpers — render dinamico de chain-mini + proc-lists
# ============================================================================


# Mapeamento heuristico de A1..A5 → tipo (apenas usado como default quando
# o BRIEFING nao especifica .tipo). M7-aligned mas generico o suficiente.
APOIO_TIPO_DEFAULT = {
    "A1": "Habilitador",
    "A2": "Risco",
    "A3": "Capital",
    "A4": "Pessoas",
    "A5": "Operação",
}


def _render_chainmini_box(p: dict) -> str:
    """Card miniaturizado do chain-mini (page 4 da Politica)."""
    codigo = escape_html(p.get("codigo", ""))
    nome = escape_html(p.get("nome", ""))
    cls = "cprocess"
    if p.get("highlight"):
        cls += " lime"
    elif p.get("blue_accent"):
        cls += " blue"
    return (
        f'<div class="{cls}">'
        f'<div class="ccode">{codigo}</div>'
        f'<div class="cname">{nome}</div>'
        f'</div>'
    )


def _render_proc_card(p: dict, camada_kind: str) -> str:
    """Card .proc do proc-list (pages 5/6/7).

    camada_kind: 'gerencial' | 'primario' | 'apoio'
    Define qual meta-row aparece a direita (Freq | Meta/Camada | Tipo).
    """
    codigo = escape_html(p.get("codigo", ""))
    nome = escape_html(p.get("nome", ""))
    missao = escape_html(_format_missao(p.get("sipoc") or {})) or "—"
    owner = escape_html((p.get("sipoc") or {}).get("owner", "")) or "—"

    cls = "proc"
    # Page 6 (primarios): .highlight em verticais marcados; A1 blue ja
    # esta em apoio (page 7) e nao em primarios. Page 7 (apoio): A1 com .blue.
    if camada_kind == "primario" and p.get("highlight"):
        cls += " highlight"
    if camada_kind == "apoio" and p.get("blue_accent"):
        cls += " blue"

    # Meta-row depende da camada
    if camada_kind == "gerencial":
        freq = escape_html(p.get("frequencia", "")) or "—"
        meta_row = (
            f'<div class="m"><span class="k">Owner</span><span class="v">{owner}</span></div>'
            f'<div class="m"><span class="k">Freq.</span><span class="v">{freq}</span></div>'
        )
    elif camada_kind == "primario":
        sc = p.get("subcamada")
        if sc == "front":
            sub_label = ("Camada", "Front-end")
        elif sc == "back":
            sub_label = ("Camada", "Back-end")
        else:
            # vertical/nucleo: usa Meta
            meta_val = escape_html(p.get("meta", "")) or "—"
            sub_label = ("Meta", meta_val)
        meta_row = (
            f'<div class="m"><span class="k">Owner</span><span class="v">{owner}</span></div>'
            f'<div class="m"><span class="k">{escape_html(sub_label[0])}</span>'
            f'<span class="v">{sub_label[1]}</span></div>'
        )
    else:  # apoio
        tipo = p.get("tipo") or APOIO_TIPO_DEFAULT.get(p.get("codigo", ""), "—")
        meta_row = (
            f'<div class="m"><span class="k">Owner</span><span class="v">{owner}</span></div>'
            f'<div class="m"><span class="k">Tipo</span><span class="v">{escape_html(tipo)}</span></div>'
        )

    return (
        f'<div class="{cls}">'
        f'<div class="proc-code">{codigo}</div>'
        f'<div class="proc-main">'
        f'<div class="pname">{nome}</div>'
        f'<div class="pmission">{missao}</div>'
        f'</div>'
        f'<div class="proc-meta">{meta_row}</div>'
        f'</div>'
    )


def _inject_politica_processes(template_str: str, briefing_fm: dict) -> str:
    """Reconstroi dinamicamente as 4 listas de processos da Politica.

    Fix do Bug 1 do report v2.0.3 para a Politica (paralelo a `_inject_n1_processes`):
    - Page 4 "Estrutura da cadeia": chain-mini com front+verticais+back+gerenciais+apoio
    - Page 5 "Processos gerenciais": proc-list de gerenciais (Owner + Freq)
    - Page 6 "Processos primarios": proc-list (Owner + Meta para verticais; Camada para front/back)
    - Page 7 "Processos de apoio": proc-list (Owner + Tipo)
    """
    from bs4 import BeautifulSoup
    processos = briefing_fm.get("processos") or []
    gerenciais = [p for p in processos if p.get("camada") == "gerencial"]
    primarios = [p for p in processos if p.get("camada") == "primario"]
    apoio = [p for p in processos if p.get("camada") == "apoio"]

    front = [p for p in primarios if p.get("subcamada") == "front"]
    nucleo = [p for p in primarios if p.get("subcamada") == "nucleo" or not p.get("subcamada")]
    back = [p for p in primarios if p.get("subcamada") == "back"]

    soup = BeautifulSoup(template_str, "html.parser")

    # ── Page 4: chain-mini ───────────────────────────────────
    chain = soup.find("div", class_="chain-mini")
    if chain:
        clayers = chain.find_all("div", class_="clayer", recursive=False)
        # Esperado: 3 clayers — gerenciais, primarios, apoio
        for clayer in clayers:
            h3 = clayer.find("h3")
            if not h3:
                continue
            label = h3.get_text(strip=True).lower()
            if "gerenciais" in label:
                cc = clayer.find("div", class_="ccontent")
                for box in cc.find_all("div", class_="cprocess", recursive=False):
                    box.decompose()
                for p in gerenciais:
                    new = BeautifulSoup(_render_chainmini_box(p), "html.parser")
                    for child in list(new.contents):
                        cc.append(child)
            elif "primários" in label or "primarios" in label:
                cc = clayer.find("div", class_="ccontent")
                # Front-end: col-fb (primeiro)
                col_fbs = cc.find_all("div", class_="col-fb", recursive=False)
                if len(col_fbs) >= 2:
                    front_col, back_col = col_fbs[0], col_fbs[1]
                    for box in front_col.find_all("div", class_="cprocess", recursive=False):
                        box.decompose()
                    for p in front:
                        new = BeautifulSoup(_render_chainmini_box(p), "html.parser")
                        for child in list(new.contents):
                            front_col.append(child)
                    for box in back_col.find_all("div", class_="cprocess", recursive=False):
                        box.decompose()
                    for p in back:
                        new = BeautifulSoup(_render_chainmini_box(p), "html.parser")
                        for child in list(new.contents):
                            back_col.append(child)
                # Verticais: cverticais > cvgrid
                cvert = cc.find("div", class_="cverticais")
                if cvert:
                    cvgrid = cvert.find("div", class_="cvgrid")
                    if cvgrid:
                        for box in cvgrid.find_all("div", class_="cprocess", recursive=False):
                            box.decompose()
                        for p in nucleo:
                            new = BeautifulSoup(_render_chainmini_box(p), "html.parser")
                            for child in list(new.contents):
                                cvgrid.append(child)
            elif "apoio" in label:
                cc = clayer.find("div", class_="ccontent")
                for box in cc.find_all("div", class_="cprocess", recursive=False):
                    box.decompose()
                for p in apoio:
                    new = BeautifulSoup(_render_chainmini_box(p), "html.parser")
                    for child in list(new.contents):
                        cc.append(child)

    # ── Pages 5/6/7: proc-list por camada ────────────────────
    # Identificamos cada page pelo data-page-label da <article>
    page_to_camada = {
        "Processos Gerenciais": ("gerencial", gerenciais),
        "Processos Primários": ("primario", primarios),
        "Processos Primarios": ("primario", primarios),
        "Processos de Apoio": ("apoio", apoio),
    }
    for article in soup.find_all("article", class_="page"):
        label = article.get("data-page-label", "")
        spec = page_to_camada.get(label)
        if not spec:
            continue
        camada_kind, items = spec
        proc_list = article.find("div", class_="proc-list")
        if not proc_list:
            continue
        # Limpa cards .proc existentes
        for card in proc_list.find_all("div", class_="proc", recursive=False):
            card.decompose()
        # Rebuild
        for p in items:
            new = BeautifulSoup(_render_proc_card(p, camada_kind), "html.parser")
            for child in list(new.contents):
                proc_list.append(child)

    return str(soup)


# ============================================================================
# Build N4 (Politica) — HTML standalone com export PDF via window.print()
# ============================================================================


def _format_missao(sipoc: dict) -> str:
    """Concatena verbo + objeto + finalidade em uma sentenca."""
    if not sipoc:
        return ""
    verbo = (sipoc.get("verbo") or "").strip()
    objeto = (sipoc.get("objeto") or "").strip()
    finalidade = (sipoc.get("finalidade") or "").strip()
    finalidade_clean = re.sub(r"^para\s+", "", finalidade, flags=re.IGNORECASE).strip()
    if not verbo and not objeto:
        return ""
    parts = []
    if verbo:
        parts.append(verbo)
    if objeto:
        parts.append(objeto)
    base = " ".join(parts)
    if finalidade_clean:
        return f"{base} para {finalidade_clean}".strip()
    return base


def _format_versao_completa(politica: dict, fallback: str) -> str:
    """Deriva 'vX.Y · MM/AA' da versao vigente, com fallback para versao simples."""
    versoes = (politica.get("versoes") or []) if politica else []
    vigente = next((v for v in versoes
                    if isinstance(v, dict) and v.get("status") == "vigente"), None)
    if vigente:
        ver = (vigente.get("versao") or "").strip()
        data = (vigente.get("data") or "").strip()
        if ver and data:
            return f"{ver} · {data}"
        return ver or data or fallback
    return fallback


def build_politica(briefing_fm: dict, body_md: str,
                   skill_dir: Path, output_dir: Path) -> Path:
    """Gera politica-{slug}.html a partir do template-politica.html.

    Substituicao direta de placeholders — sem Jinja, sem includes. O template
    e standalone (1874 linhas) com 8 paginas A4 portrait + toolbar de export
    PDF via window.print(). Conteudo da politica vem da secao `politica:` do
    BRIEFING; meta por vertical vem de `processos[].meta`; SIPOC sample vem
    de `politica.sipoc_amostra` (2 codigos referenciando processos[]).
    """
    empresa = briefing_fm.get("empresa", {})
    slug = empresa.get("slug", "empresa")
    n1 = briefing_fm.get("n1", {})
    contagens = n1.get("contagens", {})
    processos = briefing_fm.get("processos") or []
    artefatos = set(briefing_fm.get("artefatos_a_gerar") or [])
    politica = briefing_fm.get("politica") or {}

    template = (skill_dir / "templates" / "template-politica.html").read_text(encoding="utf-8")

    # ── Identidade / cabecalho (compartilhado com N1/N2/N3) ──
    replacements = {
        "{{NOME_DA_EMPRESA}}": escape_html(empresa.get("nome", "")),
        "{{AREA_DOCUMENTO}}": escape_html(briefing_fm.get("area_documento", "")),
        "{{DATA_REFERENCIA}}": escape_html(briefing_fm.get("data_referencia", "")),
        "{{LEDE_DOCUMENTO}}": escape_html(extract_section(body_md, "Lede do documento")),
        "{{VERSAO_CURTA}}": escape_html(briefing_fm.get("versao", "")),
        "{{TOTAL_PROCESSOS}}": str(n1.get("total_processos", len(processos))),
        "{{N_GERENCIAIS}}": str(contagens.get("gerenciais", 0)),
        "{{N_PRIMARIOS}}": str(contagens.get("primarios", 0)),
        "{{N_APOIO}}": str(contagens.get("apoio", 0)),
        "{{ROTULO_NUCLEO}}": escape_html(n1.get("rotulo_nucleo", "Verticais")),
    }

    # ── Metadata da politica ──
    metadata = politica.get("metadata") or {}
    replacements.update({
        "{{CODIGO_DOCUMENTO}}": escape_html(metadata.get("codigo_documento", "")),
        "{{DATA_VIGENCIA}}": escape_html(metadata.get("data_vigencia", "")),
        "{{DATA_PROXIMA_REVISAO}}": escape_html(metadata.get("proxima_revisao", "")),
        "{{AREA_RESPONSAVEL}}": escape_html(metadata.get("area_responsavel", "")),
        "{{VERSAO_COMPLETA}}": escape_html(
            _format_versao_completa(politica, briefing_fm.get("versao", ""))),
    })

    # ── Versoes (vigente + ate 2 anteriores; template tem 3 linhas fixas) ──
    versoes = politica.get("versoes") or []
    vigente = next((v for v in versoes
                    if isinstance(v, dict) and v.get("status") == "vigente"), {})
    anteriores = [v for v in versoes
                  if isinstance(v, dict) and v.get("status") != "vigente"]
    replacements["{{ALTERACOES_VERSAO_ATUAL}}"] = escape_html(vigente.get("alteracoes", "—"))

    for i in (1, 2):
        v = anteriores[i - 1] if len(anteriores) >= i else {}
        replacements[f"{{{{VERSAO_ANTERIOR_{i}}}}}"] = escape_html(v.get("versao", "—"))
        replacements[f"{{{{DATA_VERSAO_ANTERIOR_{i}}}}}"] = escape_html(v.get("data", "—"))
        replacements[f"{{{{ALTERACOES_VERSAO_ANTERIOR_{i}}}}}"] = escape_html(v.get("alteracoes", "—"))
        replacements[f"{{{{RESPONSAVEL_VERSAO_ANTERIOR_{i}}}}}"] = escape_html(v.get("responsavel", "—"))

    # ── Aprovacoes (3 papeis) ──
    aprov = politica.get("aprovacoes") or {}
    for role_pt, role_key in [("ELABORADOR", "elaborador"),
                               ("REVISOR", "revisor"),
                               ("APROVADOR", "aprovador")]:
        r = aprov.get(role_key) or {}
        replacements[f"{{{{NOME_{role_pt}}}}}"] = escape_html(r.get("nome", ""))
        replacements[f"{{{{CARGO_{role_pt}}}}}"] = escape_html(r.get("cargo", ""))
        date_placeholder = {
            "ELABORADOR": "DATA_ELABORACAO",
            "REVISOR": "DATA_REVISAO",
            "APROVADOR": "DATA_APROVACAO",
        }[role_pt]
        replacements[f"{{{{{date_placeholder}}}}}"] = escape_html(r.get("data", ""))

    # ── Objetivo, escopo, doc relacionados ──
    objetivo_txt = (politica.get("objetivo_texto") or "").strip()
    replacements["{{TEXTO_OBJETIVO}}"] = escape_html(objetivo_txt)

    escopo = politica.get("escopo") or {}
    inclusoes = (escopo.get("inclusoes") or []) + ["", "", ""]
    exclusoes = (escopo.get("exclusoes") or []) + ["", ""]
    doc_rel = (escopo.get("doc_relacionados") or []) + ["", "", ""]
    for i in (1, 2, 3):
        replacements[f"{{{{ESCOPO_INCLUSAO_{i}}}}}"] = escape_html(inclusoes[i - 1] or "—")
        replacements[f"{{{{DOC_RELACIONADO_{i}}}}}"] = escape_html(doc_rel[i - 1] or "—")
    for i in (1, 2):
        replacements[f"{{{{ESCOPO_EXCLUSAO_{i}}}}}"] = escape_html(exclusoes[i - 1] or "—")

    # ── Governanca ──
    gov = politica.get("governanca") or {}
    replacements.update({
        "{{COMITE_REVISOR}}": escape_html(gov.get("comite_revisor", "")),
        "{{DOC_SLA}}": escape_html(gov.get("doc_sla", "")),
        "{{AREA_COMPLIANCE}}": escape_html(gov.get("area_compliance", "")),
    })

    # ─────────────────────────────────────────────────────────────────────
    # v2.1 placeholders — Politica formal de governanca (templates oficiais
    # v18/Mai/2026 reestruturaram o template-politica.html, removendo as
    # listas de processos e adicionando 10 paginas formais: Capa, Controle,
    # Objetivo, Definicoes, Principios, Diretrizes 5.1-5.7, Papeis,
    # Governanca, Disposicoes Finais).
    #
    # Mapeaveis do briefing atual: ~30 (metadata + datas curtas + texto
    # objetivo dividido em P1/P2 + doc relacionado expandido + defaults M7
    # para tipo/nivel/classificacao/cadencia/leds).
    #
    # NAO mapeaveis sem schema extension (~140): Principios 1-7, Diretrizes
    # 5.1-5.7 (titulos+intros+regras), Papeis 1-8, Indicadores 1-5,
    # Hierarquia normativa 1-4, Escala aprovacao 1-6, Gatilhos revisao 1-4,
    # Definicoes 1-12. Esses permanecem como {{...}} no output ate uma
    # futura release que estenda BRIEFING schema com politica.principios[],
    # politica.diretrizes[], politica.papeis[], etc.
    # ─────────────────────────────────────────────────────────────────────

    # Tipo de documento / hierarquia normativa (defaults M7 — politica
    # corporativa nivel 1, dentro de POL > NORM > SOP > INSTR)
    replacements["{{TIPO_DOCUMENTO}}"] = "Política"
    replacements["{{TIPO_DOCUMENTO_SIGLA}}"] = "POL"
    replacements["{{NIVEL_DOCUMENTO}}"] = "N1 · Política"
    replacements["{{CLASSIFICACAO_DOCUMENTO}}"] = "Uso interno · Confidencial"
    # Documento superior na hierarquia (defaults M7: ate aprovado, nao tem)
    replacements["{{CODIGO_DOC_SUPERIOR}}"] = "—"
    replacements["{{TITULO_DOC_SUPERIOR}}"] = "Esta política é o topo da hierarquia normativa"

    # Capa / titulo (derivam de empresa + tipo)
    empresa_nome = empresa.get("nome", "")
    titulo_completo = f"Política de processos · {empresa_nome}" if empresa_nome else "Política de processos"
    replacements["{{TITULO_DOCUMENTO}}"] = escape_html(titulo_completo)
    replacements["{{TITULO_LINHA1}}"] = "Política"
    replacements["{{TITULO_LINHA2}}"] = "de processos"
    replacements["{{TITULO_ACENTO}}"] = "processos"
    # Cover-specific (algumas variantes do template usam prefixos diferentes)
    replacements["{{COVER_TITULO_PREFIXO}}"] = "Política"
    replacements["{{COVER_TITULO_LINHA1}}"] = "Política"
    replacements["{{COVER_TITULO_SUFIXO}}"] = "de processos"
    replacements["{{COVER_TITULO_ACENTO}}"] = "de processos"
    cover_subtitulo = (
        extract_section(body_md, "Lede do documento")
        or f"Política formal de governança dos processos macro de {empresa_nome}."
    )
    replacements["{{COVER_SUBTITULO}}"] = escape_html(cover_subtitulo)

    # Datas curtas (DD/MM/AAAA -> DD/MM/AA)
    def _short_date(d: str) -> str:
        if not isinstance(d, str) or not d:
            return "—"
        # Tenta DD/MM/AAAA -> DD/MM/AA; senao devolve original
        m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", d.strip())
        if m:
            return f"{m.group(1)}/{m.group(2)}/{m.group(3)[2:]}"
        return d
    replacements["{{DATA_VIGENCIA_CURTA}}"] = escape_html(_short_date(metadata.get("data_vigencia", "")))
    replacements["{{DATA_PROXIMA_REVISAO_CURTA}}"] = escape_html(_short_date(metadata.get("proxima_revisao", "")))

    # Alteracoes da versao vigente (alias mais curto que ALTERACOES_VERSAO_ATUAL)
    replacements["{{ALTERACOES_VERSAO}}"] = escape_html(vigente.get("alteracoes", "—"))

    # Texto do objetivo: template novo divide em P1 e P2. Se o briefing
    # tiver objetivo multi-paragrafo, separa pelo primeiro \n\n; senao P2
    # fica vazio (fallback texto generico).
    if "\n\n" in objetivo_txt:
        p1, p2 = objetivo_txt.split("\n\n", 1)
    else:
        p1 = objetivo_txt
        p2 = ""
    replacements["{{TEXTO_OBJETIVO_P1}}"] = escape_html(p1)
    replacements["{{TEXTO_OBJETIVO_P2}}"] = escape_html(p2 or "—")

    # Escopo: oficial pede 3 inclusoes + 3 exclusoes (skill ja gerava
    # ESCOPO_INCLUSAO_1/2/3; ESCOPO_EXCLUSAO_1/2 mas template agora pede
    # tambem ESCOPO_EXCLUSAO_3).
    replacements["{{ESCOPO_EXCLUSAO_3}}"] = escape_html(exclusoes[2] or "—")

    # Documento relacionado expandido (oficial novo: DOC_REL_1_CODIGO,
    # _TITULO, _RELACAO). Skill antiga so tinha string flat — derivamos
    # heuristicamente.
    primeiro_doc = (escopo.get("doc_relacionados") or [""])[0]
    if " — " in primeiro_doc:
        cod, rest = primeiro_doc.split(" — ", 1)
        rel_tipo = "Referência"
    elif "(" in primeiro_doc and ")" in primeiro_doc:
        cod = primeiro_doc.split("(")[-1].rstrip(")")
        rest = primeiro_doc.split(" (")[0]
        rel_tipo = "Referência"
    else:
        cod = "—"
        rest = primeiro_doc or "—"
        rel_tipo = "Referência"
    replacements["{{DOC_REL_1_CODIGO}}"] = escape_html(cod)
    replacements["{{DOC_REL_1_TITULO}}"] = escape_html(rest)
    replacements["{{DOC_REL_1_RELACAO}}"] = escape_html(rel_tipo)

    # Vigencia + cadencia (defaults M7)
    replacements["{{TEXTO_VIGENCIA}}"] = escape_html(
        "Esta política entra em vigor na data de sua aprovação pela Diretoria "
        "Executiva e permanece vigente até substituição ou revogação formal "
        "por documento de mesmo nível ou superior. A revisão anual obrigatória "
        "não interrompe sua vigência."
    )
    replacements["{{CADENCIA_REVISAO}}"] = "Anual"
    replacements["{{REVISAO_PERIODICA_INTRO}}"] = escape_html(
        "A revisão periódica desta política segue cadência anual obrigatória, "
        "conduzida pelo comitê revisor designado em 8."
    )

    # Ledes das paginas (defaults M7 — texto introdutorio das secoes)
    replacements["{{LEDE_ESCOPO}}"] = escape_html(
        "Esta política aplica-se a todos os processos macro da cadeia de "
        "valor da empresa, com responsabilidades distribuídas conforme "
        "definido em 6."
    )
    replacements["{{LEDE_PRINCIPIOS}}"] = escape_html(
        "Os princípios abaixo orientam a interpretação e aplicação de "
        "todas as diretrizes desta política. Em caso de conflito entre "
        "diretrizes operacionais, prevalecem os princípios."
    )
    replacements["{{LEDE_PAPEIS}}"] = escape_html(
        "Esta política atribui responsabilidades a 8 papéis institucionais. "
        "Acúmulo de papéis é permitido desde que documentado."
    )

    # Total de paginas — conta <article class="page"> no template
    total_paginas = template.count('<article class="page')
    replacements["{{TOTAL_PAGINAS}}"] = str(total_paginas) if total_paginas else "10"

    # ── Por processo: nome, missao, owner, frequencia (gerenciais), meta (verticais) ──
    by_codigo = {p.get("codigo"): p for p in processos if p.get("codigo")}
    for p in processos:
        codigo = p.get("codigo", "")
        sipoc = p.get("sipoc") or {}
        replacements[f"{{{{NOME_PROCESSO_{codigo}}}}}"] = escape_html(p.get("nome", ""))
        replacements[f"{{{{MISSAO_{codigo}}}}}"] = escape_html(_format_missao(sipoc))
        replacements[f"{{{{OWNER_{codigo}}}}}"] = escape_html(sipoc.get("owner", ""))
        if p.get("camada") == "gerencial":
            replacements[f"{{{{FREQUENCIA_{codigo}}}}}"] = escape_html(p.get("frequencia", "—"))
        # META so para verticais (primarios + subcamada=nucleo)
        if p.get("camada") == "primario" and p.get("subcamada") == "nucleo":
            replacements[f"{{{{META_{codigo}}}}}"] = escape_html(p.get("meta", "—"))

    # ── SIPOC sample (2 processos featurados) ──
    amostra = politica.get("sipoc_amostra") or [None, None]
    for letra, idx in [("A", 0), ("B", 1)]:
        codigo_amostra = amostra[idx] if idx < len(amostra) else None
        p_amostra = by_codigo.get(codigo_amostra) if codigo_amostra else None
        sipoc_amostra = (p_amostra or {}).get("sipoc") or {}
        replacements[f"{{{{CODIGO_PROCESSO_SIPOC_{letra}}}}}"] = escape_html(codigo_amostra or "—")
        replacements[f"{{{{NOME_PROCESSO_SIPOC_{letra}}}}}"] = escape_html((p_amostra or {}).get("nome", "—"))
        replacements[f"{{{{OWNER_SIPOC_{letra}}}}}"] = escape_html(sipoc_amostra.get("owner", "—"))
        replacements[f"{{{{MISSAO_SIPOC_{letra}}}}}"] = escape_html(_format_missao(sipoc_amostra) or "—")
        inputs = (sipoc_amostra.get("inputs") or []) + ["", "", ""]
        outputs = (sipoc_amostra.get("outputs") or []) + ["", "", ""]
        for i in (1, 2, 3):
            replacements[f"{{{{INPUT_{letra}_{i}}}}}"] = escape_html(inputs[i - 1] or "—")
            replacements[f"{{{{OUTPUT_{letra}_{i}}}}}"] = escape_html(outputs[i - 1] or "—")

    # Aplicar todas as substituicoes
    for k, v in replacements.items():
        template = template.replace(k, v)

    # ── Tabs do header dark: repointar refs cross-artefato ──
    # Bug 4 fix do report v2.0.4: 3 hrefs apontavam para template-*.html
    # do design oficial em vez dos {tipo}-{slug}.html gerados pela skill.
    # Quando o artefato correspondente nao esta em artefatos_a_gerar,
    # converte para <div class="tab"> nao-navegavel (mesma logica dos
    # builds N1/N2/N3).
    n1_tab_repl = (
        f'<a class="tab" href="cadeia-de-valor-{slug}.html">'
        if "n1" in artefatos else
        '<div class="tab">'
    )
    n2_tab_repl = (
        f'<a class="tab" href="missao-do-processo-{slug}.html">'
        if "n2" in artefatos else
        '<div class="tab">'
    )
    n3_tab_repl = (
        f'<a class="tab" href="mapa-de-interdependencia-{slug}.html">'
        if "n3" in artefatos else
        '<div class="tab">'
    )
    # Substituir abertura da tag; fechamento (</a> vs </div>) ja casa
    # porque o template oficial usa <a> nas 3, e quando convertemos para
    # <div> precisamos converter </a> tambem.
    if "n1" in artefatos:
        template = template.replace(
            '<a class="tab" href="exemplo-m7-preenchido.html">',
            n1_tab_repl,
        )
    else:
        template = template.replace(
            '<a class="tab" href="exemplo-m7-preenchido.html">Visão geral <span class="num">N1</span></a>',
            '<div class="tab">Visão geral <span class="num">N1</span></div>',
        )
    if "n2" in artefatos:
        template = template.replace(
            '<a class="tab" href="template-missao-do-processo.html">',
            n2_tab_repl,
        )
    else:
        template = template.replace(
            '<a class="tab" href="template-missao-do-processo.html">Missão do processo</a>',
            '<div class="tab">Missão do processo</div>',
        )
    if "n3" in artefatos:
        template = template.replace(
            '<a class="tab" href="template-mapa-de-interdependencia.html">',
            n3_tab_repl,
        )
    else:
        template = template.replace(
            '<a class="tab" href="template-mapa-de-interdependencia.html">Mapa de interdependência</a>',
            '<div class="tab">Mapa de interdependência</div>',
        )

    # Render dinamico das listas de processos (chain-mini p4, proc-lists p5/6/7).
    # Resolve overflow (>9 primarios, >4 gerenciais, >5 apoio) e respeita
    # camada/subcamada do BRIEFING. Bug 1 fix do report v2.0.3.
    template = _inject_politica_processes(template, briefing_fm)

    # ── Salvar ──
    output_path = output_dir / f"politica-{slug}.html"
    output_path.write_text(template, encoding="utf-8")
    return output_path


# ============================================================================
# Main
# ============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera os 4 artefatos N1/N2/N3/N4 a partir do BRIEFING.")
    parser.add_argument("briefing", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--skill-dir", type=Path, default=None)
    parser.add_argument("--skip-pdf", action="store_true",
                       help="Gera N4.html mas pula o render do PDF")
    parser.add_argument("--skip-validate", action="store_true",
                       help="Pula validacao previa do BRIEFING")
    args = parser.parse_args()

    if not args.briefing.is_file():
        sys.stderr.write(f"ERRO: BRIEFING nao encontrado: {args.briefing}\n")
        return 2

    skill_dir = args.skill_dir or Path(__file__).resolve().parent.parent
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Validacao
    if not args.skip_validate:
        if not validate_briefing(args.briefing, skill_dir):
            sys.stderr.write("ERRO: BRIEFING tem bloqueadores. Use --skip-validate para ignorar.\n")
            return 1

    # Parse
    try:
        fm, body = parse_briefing(args.briefing)
    except (yaml.YAMLError, ValueError) as e:
        sys.stderr.write(f"ERRO ao parsear BRIEFING: {e}\n")
        return 1

    # Copiar assets primeiro
    copy_assets(skill_dir, output_dir)

    artefatos = set(fm.get("artefatos_a_gerar") or [])

    # Sequencial: N1 -> N2 -> N3 -> N4
    if "n1" in artefatos:
        n1_path = build_n1(fm, body, skill_dir, output_dir)
        size_kb = n1_path.stat().st_size / 1024
        print(f"OK · {n1_path} ({size_kb:.1f} KB)")

    if "n2" in artefatos:
        n2_path = build_n2(fm, body, skill_dir, output_dir)
        size_kb = n2_path.stat().st_size / 1024
        print(f"OK · {n2_path} ({size_kb:.1f} KB)")

    if "n3" in artefatos:
        n3_path = build_n3(fm, body, skill_dir, output_dir)
        size_kb = n3_path.stat().st_size / 1024
        print(f"OK · {n3_path} ({size_kb:.1f} KB)")

    if "n4-pdf" in artefatos:
        # Pre-condicao: N4 (Politica) requer N1+N2+N3 na sequencia rigida
        if not all(k in artefatos for k in ("n1", "n2", "n3")):
            sys.stderr.write("ERRO: n4-pdf requer n1, n2 e n3 em artefatos_a_gerar.\n")
            return 1

        n4_path = build_politica(fm, body, skill_dir, output_dir)
        size_kb = n4_path.stat().st_size / 1024
        print(f"OK · {n4_path} ({size_kb:.1f} KB)")
        if not args.skip_pdf:
            # Nota: a partir de v2.0.0 o PDF e gerado client-side via window.print()
            # no navegador do usuario. Abrir o HTML, clicar em "Exportar PDF" no
            # toolbar e marcar "Plano de fundo grafico" para preservar cores.
            print(f"     PDF: abra {n4_path.name} no navegador e clique 'Exportar PDF'")

    return 0


if __name__ == "__main__":
    sys.exit(main())
