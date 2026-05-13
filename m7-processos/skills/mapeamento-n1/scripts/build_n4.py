#!/usr/bin/env python3
"""[DEPRECATED 2026-05] mapeamento-n1 · monta o documento oficial (N4) HTML.

================================================================================
DEPRECATION NOTICE
================================================================================
A partir de 2026-05 o template N4 (template-documento-oficial.html) e
STANDALONE — nao usa Jinja includes, nao parseia fragmentos de N1/N3.
A skill agora faz substituicao direta de ~120 placeholders no template.

Este script (que orquestrava Jinja {% include %} + BeautifulSoup parsing)
NAO e mais invocado pelo fluxo padrao da skill.

ARQUITETURA ATUAL:
- Skill le BRIEFING.md (com secao politica:)
- Skill substitui placeholders no template-documento-oficial.html
- Skill grava documento-oficial-{slug}.html no diretorio do usuario
- Usuario abre no navegador e exporta PDF via toolbar (window.print())

Veja references/n4-documento-oficial.md §3 (arquitetura atual) e §7 (legacy).
================================================================================

Pipeline LEGACY (pre-2026-05):
    BRIEFING.md  +  N1.html  +  N3.html  ──▶  documento-oficial-{slug}.html

Substitui placeholders globais, extrai fragmentos dos diagramas N1/N2/N3 ja
renderizados, gera as paginas SIPOC iteradas (uma por processo), gera tabela
de relacoes, lista de fricoes e notas de iteracao.

Uso:
    python3 build_n4.py <briefing.md> <output_dir> [--skill-dir <path>]

Argumentos:
    briefing.md     Caminho do BRIEFING.md (frontmatter YAML obrigatorio).
    output_dir      Diretorio onde N1/N2/N3 ja existem e onde o N4.html sera escrito.
    --skill-dir     Caminho da skill mapeamento-n1 (default: parent do script).
                    Necessario para copiar template + assets.

Exit codes:
    0 = ok
    1 = erro (BRIEFING invalido, N1/N2/N3 ausentes, etc.)
    2 = uso incorreto
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("ERRO: PyYAML nao instalado. Rode: pip install -r requirements.txt\n")
    sys.exit(2)

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.stderr.write("ERRO: beautifulsoup4 nao instalado. Rode: pip install beautifulsoup4\n")
    sys.exit(2)


# ============================================================================
# Constantes
# ============================================================================

CAMADA_LABEL = {
    "gerencial": "Gerencial",
    "primario": "Primario",
    "apoio": "Apoio",
}

KIND_HTML_CLASS = {
    "cliente": "rel-kind-cliente",
    "info": "rel-kind-info",
    "decisao": "rel-kind-decisao",
}

KIND_LABEL = {
    "cliente": "Cliente",
    "info": "Informacao",
    "decisao": "Governanca",
}

FORCA_LABEL = {
    "strong": "Forte",
    "mid": "Medio",
    "soft": "Fraco",
    None: "—",
}


# ============================================================================
# Parser do BRIEFING.md
# ============================================================================


def parse_briefing(path: Path) -> tuple[dict, str]:
    """Devolve (frontmatter dict, markdown body)."""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not m:
        raise ValueError("Frontmatter YAML nao encontrado.")
    fm = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)
    return fm, body


def extract_section(body: str, heading: str) -> str:
    """Extrai conteudo de uma secao ## do markdown.

    Devolve as linhas entre `## {heading}` e o proximo `## ` ou EOF,
    com comentarios HTML <!-- ... --> removidos.
    """
    pattern = rf"##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|$)"
    m = re.search(pattern, body, re.DOTALL)
    if not m:
        return ""
    content = m.group(1).strip()
    # Remove HTML comments
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL).strip()
    return content


def md_to_simple_html(text: str) -> str:
    """Converte markdown simples (paragrafos, listas, **bold**) para HTML basico."""
    if not text:
        return ""

    blocks = re.split(r"\n\s*\n", text.strip())
    out = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Lista de bullets
        if re.match(r"^\s*[-*]\s", block):
            items = []
            for line in block.split("\n"):
                line = line.strip()
                if line.startswith(("- ", "* ")):
                    items.append(f"<li>{format_inline(line[2:])}</li>")
            out.append("<ul>" + "".join(items) + "</ul>")
        else:
            out.append(f"<p>{format_inline(block)}</p>")

    return "\n".join(out)


def format_inline(text: str) -> str:
    """Inline markdown: **bold**, *italic*, `code`."""
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*])\*([^*]+)\*(?![*])", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


# ============================================================================
# Extracao de fragmentos dos templates renderizados
# ============================================================================


def extract_chain_container(n1_html_path: Path) -> str:
    """Extrai o bloco <div class='chain-container'> do N1 ja renderizado."""
    soup = BeautifulSoup(n1_html_path.read_text(encoding="utf-8"), "html.parser")
    chain = soup.find("div", class_="chain-container")
    if not chain:
        raise ValueError(f"N1 nao tem <div class='chain-container'>: {n1_html_path}")
    return str(chain)


def extract_neural_block(n3_html_path: Path) -> tuple[str, str]:
    """Extrai (<div class='neural'>, <script>) do N3 ja renderizado.

    Devolve tupla com bloco do mapa (sem painel info) + script de hover.
    """
    soup = BeautifulSoup(n3_html_path.read_text(encoding="utf-8"), "html.parser")
    neural = soup.find("div", class_="neural")
    if not neural:
        raise ValueError(f"N3 nao tem <div class='neural'>: {n3_html_path}")

    # Em PDF nao ha hover, entao remove o info-panel (visualmente quebrado)
    info_panel = neural.find("div", id="info-panel")
    if info_panel:
        info_panel.decompose()

    # Script: pegar o ultimo <script> antes do </body> (o que tem RELATIONS)
    scripts = soup.find_all("script")
    relations_script = ""
    for s in scripts:
        if s.string and "RELATIONS" in s.string:
            relations_script = ""  # PDF estatico nao precisa do JS
            break

    return str(neural), relations_script


# ============================================================================
# Renderers de blocos repetidos
# ============================================================================


def render_sipoc_pages(processos: list, empresa_nome: str, total_processos: int) -> str:
    """Gera HTML de uma <article class='page process-page'> por processo.

    Cada pagina vira uma quebra de pagina no PDF.
    """
    pages = []
    for p in processos:
        sipoc = p.get("sipoc")
        if not sipoc:
            continue  # Processo sem SIPOC nao gera pagina

        camada = p.get("camada", "")
        camada_label = CAMADA_LABEL.get(camada, camada.title())
        codigo = p.get("codigo", "?")
        nome = p.get("nome", "?")
        owner = sipoc.get("owner", "")
        verbo = sipoc.get("verbo", "")
        objeto = sipoc.get("objeto", "")
        finalidade = sipoc.get("finalidade", "")

        chips_inputs = "\n".join(
            f'<div class="mp-chip">{escape_html(c)}</div>'
            for c in (sipoc.get("inputs") or [])
        )
        chips_outputs = "\n".join(
            f'<div class="mp-chip">{escape_html(c)}</div>'
            for c in (sipoc.get("outputs") or [])
        )

        # Finalidade pode ja vir com "para" ou nao — normalizar
        finalidade_clean = re.sub(r"^para\s+", "", finalidade, flags=re.IGNORECASE).strip()

        page_html = f"""<article class="page process-page">
  <div class="pg-runner-header">
    <span class="runner-l">03 · Missao · {escape_html(camada_label)}</span>
    <span class="runner-r">{escape_html(empresa_nome)}</span>
  </div>

  <div class="pp-headline">
    <span class="pp-code-prefix">{escape_html(codigo)}</span>
    <span class="pp-name">{escape_html(nome)}</span>
    <span class="pp-camada-tag">{escape_html(camada_label)}</span>
  </div>

  <div class="pp-owner">
    OWNER · <span class="v">{escape_html(owner)}</span>
  </div>

  <div class="sipoc-bloc">
    <div class="sipoc-col sipoc-col-side">
      <div class="sipoc-label">Inputs</div>
      <div class="mp-chips">
{chips_inputs}
      </div>
    </div>
    <div></div>
    <div class="sipoc-col sipoc-col-mission">
      <div class="sipoc-label">Missao</div>
      <p class="mp-mission-text">
        <span class="verb">{escape_html(verbo)}</span>
        {escape_html(objeto)}
        <em>para {escape_html(finalidade_clean)}</em>.
      </p>
    </div>
    <div></div>
    <div class="sipoc-col sipoc-col-side">
      <div class="sipoc-label">Outputs</div>
      <div class="mp-chips">
{chips_outputs}
      </div>
    </div>
  </div>
</article>"""
        pages.append(page_html)

    return "\n\n".join(pages)


def render_relations_table(relacoes: list) -> str:
    """Gera <tr> por relacao."""
    rows = []
    for r in relacoes:
        kind = r.get("kind", "")
        forca = r.get("forca")
        css_class = KIND_HTML_CLASS.get(kind, "")
        kind_label = KIND_LABEL.get(kind, kind.title())
        forca_label = FORCA_LABEL.get(forca, "—")

        rows.append(f"""<tr>
  <td><span class="rel-code">{escape_html(r.get("from", ""))}</span></td>
  <td><span class="rel-code">{escape_html(r.get("to", ""))}</span></td>
  <td><span class="{css_class}">{escape_html(kind_label)}</span></td>
  <td>{escape_html(forca_label)}</td>
  <td>{escape_html(r.get("label", ""))}</td>
</tr>""")
    return "\n".join(rows)


def render_frictions_list(processos: list) -> str:
    """Gera <div class='friction-item'> por processo com is_friction=true."""
    items = []
    for p in processos:
        n3 = p.get("n3", {})
        friction = n3.get("friction", {}) if n3 else {}
        if not friction.get("is_friction"):
            continue

        codigo = p.get("codigo", "?")
        nome = p.get("nome", "?")
        text = friction.get("text", "")

        items.append(f"""<div class="friction-item">
  <div class="friction-code">⚠ {escape_html(codigo)}</div>
  <div class="friction-text"><strong>{escape_html(nome)}.</strong> {escape_html(text)}</div>
</div>""")

    if not items:
        return '<div class="friction-text" style="color: var(--vc-300); font-style: italic;">Nenhuma friccao estrutural identificada neste mapeamento.</div>'

    return "\n".join(items)


def render_iteration_notes(body_md: str) -> str:
    """Extrai linhas de '## Notas de iteracao' e converte cada linha em <li>."""
    section = extract_section(body_md, "Notas de iteração")
    if not section:
        section = extract_section(body_md, "Notas de iteracao")  # fallback sem acento
    if not section:
        return '<li style="color: var(--vc-300); font-style: italic;">Sem notas de iteracao registradas.</li>'

    items = []
    for line in section.split("\n"):
        line = line.strip()
        if line.startswith(("- ", "* ")):
            items.append(f"<li>{format_inline(line[2:])}</li>")

    if not items:
        return '<li style="color: var(--vc-300); font-style: italic;">Sem notas registradas.</li>'

    return "\n".join(items)


# ============================================================================
# Helpers
# ============================================================================


def escape_html(s) -> str:
    if not isinstance(s, str):
        s = str(s)
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def count_verticais(processos: list, variante: str) -> int:
    """Verticais = subcamada=nucleo (variante A) ou contagem de primarios (B)."""
    if variante == "A":
        return sum(1 for p in processos
                   if p.get("camada") == "primario" and p.get("subcamada") == "nucleo")
    return sum(1 for p in processos if p.get("camada") == "primario")


def copy_assets(skill_dir: Path, output_dir: Path) -> list:
    """Copia CSS, fontes e logos para o output_dir. Devolve lista de caminhos copiados."""
    templates_dir = skill_dir / "templates"
    copied = []

    # CSS files
    for css in ["m7-tokens.css", "m7-header-dark.css", "m7-print.css"]:
        src = templates_dir / css
        if src.is_file():
            dst = output_dir / css
            shutil.copy2(src, dst)
            copied.append(dst.name)

    # fonts/ (recursive)
    fonts_src = templates_dir / "fonts"
    fonts_dst = output_dir / "fonts"
    if fonts_src.is_dir() and not fonts_dst.exists():
        shutil.copytree(fonts_src, fonts_dst)
        copied.append("fonts/ (6 OTF)")

    # assets/ (logos)
    assets_src = templates_dir / "assets"
    assets_dst = output_dir / "assets"
    if assets_src.is_dir() and not assets_dst.exists():
        shutil.copytree(assets_src, assets_dst)
        copied.append("assets/ (3 PNG)")

    return copied


# ============================================================================
# Main
# ============================================================================


def build(briefing_path: Path, output_dir: Path, skill_dir: Path) -> Path:
    fm, body = parse_briefing(briefing_path)

    empresa = fm.get("empresa", {})
    slug = empresa.get("slug", "empresa")
    empresa_nome = empresa.get("nome", "")
    n1 = fm.get("n1", {})
    contagens = n1.get("contagens", {})
    processos = fm.get("processos") or []
    relacoes = fm.get("relacoes") or []

    # Localizar N1 e N3 no output_dir (esperado: ja gerados pela skill)
    n1_path = output_dir / f"cadeia-de-valor-{slug}.html"
    n3_path = output_dir / f"mapa-de-interdependencia-{slug}.html"

    artefatos = set(fm.get("artefatos_a_gerar") or [])
    if "n4-pdf" in artefatos:
        if not n1_path.is_file():
            raise FileNotFoundError(f"N1 ausente: {n1_path}")
        if not n3_path.is_file():
            raise FileNotFoundError(f"N3 ausente: {n3_path}")

    # Carregar template
    template_path = skill_dir / "templates" / "template-documento-oficial.html"
    template = template_path.read_text(encoding="utf-8")

    # Extracoes
    n1_diagrama = extract_chain_container(n1_path) if n1_path.is_file() else "<!-- N1 nao gerado -->"
    n3_diagrama, _ = extract_neural_block(n3_path) if n3_path.is_file() else ("<!-- N3 nao gerado -->", "")

    # Substituicoes globais
    replacements = {
        "{{NOME_DA_EMPRESA}}": escape_html(empresa_nome),
        "{{AREA_DOCUMENTO}}": escape_html(fm.get("area_documento", "")),
        "{{DATA_REFERENCIA}}": escape_html(fm.get("data_referencia", "")),
        "{{LEDE_DOCUMENTO}}": escape_html(extract_section(body, "Lede do documento")),
        "{{TOTAL_PROCESSOS}}": str(n1.get("total_processos", len(processos))),
        "{{N_VERTICAIS}}": str(count_verticais(processos, n1.get("variante", "A"))),
        "{{VERSAO_CURTA}}": escape_html(fm.get("versao", "")),
        "{{N_GERENCIAIS}}": str(contagens.get("gerenciais", 0)),
        "{{N_PRIMARIOS}}": str(contagens.get("primarios", 0)),
        "{{N_APOIO}}": str(contagens.get("apoio", 0)),
        "{{TOTAL_RELACOES}}": str(len(relacoes)),
        "{{TOTAL_FRICCOES}}": str(sum(1 for p in processos
                                      if (p.get("n3") or {}).get("friction", {}).get("is_friction"))),
        "{{OBJETIVO_DOCUMENTO}}": md_to_simple_html(extract_section(body, "Objetivo do diagrama")),
        "{{CONTEXTO_EMPRESA}}": md_to_simple_html(extract_section(body, "Contexto da empresa")),
        "{{N1_DIAGRAMA_EMBEDADO}}": n1_diagrama,
        "{{N3_DIAGRAMA_EMBEDADO}}": n3_diagrama,
        "{{LINHAS_RELACOES}}": render_relations_table(relacoes),
        "{{LISTA_FRICCOES}}": render_frictions_list(processos),
        "{{LISTA_NOTAS_ITERACAO}}": render_iteration_notes(body),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    # Substituicao do bloco repetido SIPOC (entre marcadores de comentario)
    sipoc_pages_html = render_sipoc_pages(processos, empresa_nome, n1.get("total_processos", 0))
    pattern = (
        r"<!-- INICIO BLOCO REPETIDO POR PROCESSO -->.*?<!-- FIM BLOCO REPETIDO -->"
    )
    template = re.sub(pattern, sipoc_pages_html, template, flags=re.DOTALL)

    # Salvar
    output_html = output_dir / f"documento-oficial-{slug}.html"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_html.write_text(template, encoding="utf-8")

    # Copiar assets se ainda nao copiados
    copy_assets(skill_dir, output_dir)

    return output_html


def main() -> int:
    parser = argparse.ArgumentParser(description="Monta documento oficial N4 a partir do BRIEFING.")
    parser.add_argument("briefing", type=Path, help="Caminho do BRIEFING.md")
    parser.add_argument("output_dir", type=Path, help="Diretorio de saida (onde N1/N2/N3 ja existem)")
    parser.add_argument(
        "--skill-dir",
        type=Path,
        default=None,
        help="Caminho da skill mapeamento-n1 (default: parent do script)",
    )

    args = parser.parse_args()

    if not args.briefing.is_file():
        sys.stderr.write(f"ERRO: BRIEFING nao encontrado: {args.briefing}\n")
        return 2

    skill_dir = args.skill_dir or Path(__file__).resolve().parent.parent
    if not (skill_dir / "templates" / "template-documento-oficial.html").is_file():
        sys.stderr.write(f"ERRO: template-documento-oficial.html nao encontrado em {skill_dir}/templates/\n")
        return 2

    try:
        output_html = build(args.briefing, args.output_dir, skill_dir)
    except FileNotFoundError as e:
        sys.stderr.write(f"ERRO: {e}\n")
        sys.stderr.write("Gere N1 e N3 primeiro (Fase C sequencial).\n")
        return 1
    except (ValueError, yaml.YAMLError) as e:
        sys.stderr.write(f"ERRO: {e}\n")
        return 1

    size_kb = output_html.stat().st_size / 1024
    print(f"OK · {output_html} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
