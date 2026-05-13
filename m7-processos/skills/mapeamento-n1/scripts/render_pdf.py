#!/usr/bin/env python3
"""[DEPRECATED 2026-05] mapeamento-n1 · render documento oficial HTML -> PDF.

================================================================================
DEPRECATION NOTICE
================================================================================
A partir de 2026-05 o N4 (Politica) usa abordagem CLIENT-SIDE:
- Template novo: template-documento-oficial.html (standalone, 1660 linhas)
- Export: usuario abre HTML no navegador e clica em "Exportar PDF" (toolbar)
- window.print() + @page A4 gera o PDF nativamente (~500KB tipico)

Este script NAO e mais invocado pelo fluxo padrao da skill.

QUANDO AINDA USAR:
- Geracao server-side automatizada (CI, batch headless)
- PDF de N1/N2/N3 individuais (renderizar a pagina standalone como PDF)
- Casos extremos onde window.print() do usuario falha em fontes/cores

ALTERNATIVA RECOMENDADA: usuario abre documento-oficial-{slug}.html no
navegador dele e usa Cmd+P -> Salvar como PDF. Veja
references/n4-documento-oficial.md §3 e §7.
================================================================================

Adaptado de m7-apresentacoes/.../scripts/render.py e m7-projects/.../build_opr.py
(padrão Playwright primário + WeasyPrint fallback do marketplace M7).

Uso:
    python3 render_pdf.py <input.html> <output.pdf>
    python3 render_pdf.py <input.html> <output.pdf> --landscape
    python3 render_pdf.py <input.html> <output.pdf> --no-compact

Features:
    - Driver primário: Playwright + Chromium headless
    - Fallback: WeasyPrint (puro Python, ~30MB)
    - prefer_css_page_size=True respeita @page named pages do CSS
       (necessário para mapa N3 em landscape no meio do documento)
    - print_background=True obrigatório para capa fullbleed verde-caqui
    - Detecção de overflow A4 -> ativa body.compact e re-renderiza
    - Exit codes: 0=ok, 1=erro de geração, 2=erro de uso/dependência

Requer: pip install -r requirements.txt
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Constantes A4 em pixels @ 96dpi (Chromium default)
A4_HEIGHT_PX = 1123
A4_WIDTH_PX = 794


# ============================================================================
# Driver primário: Playwright
# ============================================================================


def render_with_playwright(
    input_html: Path,
    output_pdf: Path,
    enable_compact: bool = True,
) -> dict:
    """Renderiza HTML -> PDF via Playwright + Chromium.

    Devolve dict com {'driver': 'playwright', 'compact_applied': bool, 'pages': int}.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        raise RuntimeError(
            "Playwright nao instalado. Rode:\n"
            "  pip install -r requirements.txt\n"
            "  playwright install chromium"
        ) from e

    abs_input = input_html.resolve()
    abs_output = output_pdf.resolve()
    abs_output.parent.mkdir(parents=True, exist_ok=True)

    compact_applied = False

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(f"file://{abs_input}", wait_until="networkidle", timeout=30000)
            page.emulate_media(media="print")

            # Detecta overflow A4 - se primeira section .page excede 1123px, ativa compact
            if enable_compact:
                try:
                    overflow_detected = page.evaluate(
                        """() => {
                            const pages = document.querySelectorAll('.page:not(.page--cover):not(.page--landscape)');
                            for (const p of pages) {
                                if (p.scrollHeight > 1123) return true;
                            }
                            return false;
                        }"""
                    )
                    if overflow_detected:
                        page.evaluate("document.body.classList.add('compact')")
                        page.wait_for_load_state("networkidle")
                        compact_applied = True
                except Exception as e:
                    # Detecção falhou - segue sem compact (não bloquear render)
                    sys.stderr.write(f"WARN: detecção de overflow falhou: {e}\n")

            page.pdf(
                path=str(abs_output),
                format="A4",
                # Margens 0 — controle 100% pelo CSS @page (named pages funcionam)
                margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                print_background=True,
                prefer_css_page_size=True,
            )

            # Conta páginas (best-effort: count `.page` no DOM)
            try:
                pages_count = page.evaluate("document.querySelectorAll('.page').length")
            except Exception:
                pages_count = 0
        finally:
            browser.close()

    return {
        "driver": "playwright",
        "compact_applied": compact_applied,
        "pages": pages_count,
    }


# ============================================================================
# Fallback: WeasyPrint
# ============================================================================


def render_with_weasyprint(input_html: Path, output_pdf: Path) -> dict:
    """Fallback: WeasyPrint puro Python.

    Limitações conhecidas:
        - @page :first nem sempre respeita (capa pode receber footer)
        - Named pages (page: cover/toc/landscape) suporta com bugs ocasionais
        - font-display: swap ignorado (usa o primeiro source disponível)
        - JS não executa (HTML deve ser estático antes de virar PDF)
    """
    try:
        from weasyprint import HTML, CSS
    except ImportError as e:
        raise RuntimeError(
            "WeasyPrint nao instalado. Para fallback rode:\n"
            "  pip install weasyprint"
        ) from e

    abs_input = input_html.resolve()
    abs_output = output_pdf.resolve()
    abs_output.parent.mkdir(parents=True, exist_ok=True)

    HTML(filename=str(abs_input)).write_pdf(
        target=str(abs_output),
        # Stylesheet override só se @page do CSS não funcionar bem
        stylesheets=None,
    )

    return {"driver": "weasyprint", "compact_applied": False, "pages": 0}


# ============================================================================
# Orquestrador
# ============================================================================


def render(
    input_html: Path,
    output_pdf: Path,
    prefer: str = "playwright",
    enable_compact: bool = True,
) -> dict:
    """Tenta renderizar com o driver preferido; se falhar, tenta o outro."""
    if prefer == "playwright":
        try:
            return render_with_playwright(input_html, output_pdf, enable_compact)
        except RuntimeError as e:
            sys.stderr.write(f"WARN: Playwright indisponível: {e}\n")
            sys.stderr.write("Tentando fallback WeasyPrint...\n")
            return render_with_weasyprint(input_html, output_pdf)
    elif prefer == "weasyprint":
        return render_with_weasyprint(input_html, output_pdf)
    else:
        raise ValueError(f"prefer inválido: {prefer!r}. Use playwright ou weasyprint.")


# ============================================================================
# CLI
# ============================================================================


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Renderiza HTML do documento oficial -> PDF (M7-2026 paginado)."
    )
    parser.add_argument("input_html", type=Path, help="Caminho do .html de entrada")
    parser.add_argument("output_pdf", type=Path, help="Caminho do .pdf de saída")
    parser.add_argument(
        "--driver",
        choices=["playwright", "weasyprint"],
        default="playwright",
        help="Driver preferido (default: playwright; weasyprint é fallback)",
    )
    parser.add_argument(
        "--no-compact",
        action="store_true",
        help="Desabilita modo compacto automático (Playwright apenas)",
    )

    args = parser.parse_args()

    if not args.input_html.is_file():
        sys.stderr.write(f"ERRO: arquivo de entrada não encontrado: {args.input_html}\n")
        return 2

    if args.input_html.suffix.lower() != ".html":
        sys.stderr.write(f"AVISO: extensão de entrada não é .html: {args.input_html.suffix}\n")

    try:
        result = render(
            args.input_html,
            args.output_pdf,
            prefer=args.driver,
            enable_compact=not args.no_compact,
        )
    except (RuntimeError, ValueError) as e:
        sys.stderr.write(f"ERRO: {e}\n")
        return 1
    except Exception as e:
        sys.stderr.write(f"ERRO inesperado: {type(e).__name__}: {e}\n")
        return 1

    out = args.output_pdf
    size_mb = out.stat().st_size / 1024 / 1024 if out.exists() else 0
    print(f"OK · {out} ({size_mb:.2f} MB)")
    print(f"     driver={result['driver']}  compact={result['compact_applied']}  pages={result['pages']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
