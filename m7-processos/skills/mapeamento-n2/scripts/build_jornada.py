#!/usr/bin/env python3
"""build_jornada.py · Camada 3 da Fase C.

Gera/atualiza window.P5_JOURNEY dentro de build/journey-{slug}-{cod}.js
+ copia build/jornada-cx.html estatico.

Gate (entrada):
    - build/sipoc-deip.html existe (Camada 2 OK)
    - build/dados-{slug}-{cod}.js existe
    - check_ssot.py --target jornada-cx passa

Uso:
    python build_jornada.py --ssot-dir ssot/ --out build/
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _build_common import (
    TEMPLATES_DIR, bootstrap, parse_ssot, run_check_ssot, write_js_block,
    info, success, error,
)


def js_repr(value):
    return json.dumps(value, ensure_ascii=False, indent=2)


def build_jornada(ssot_dir: Path, out_dir: Path) -> None:
    info(f"Iniciando Camada 3 · Jornada CX (ssot={ssot_dir}, out={out_dir})")

    # 1. Gate: Camada 2
    sipoc_html = out_dir / "sipoc-deip.html"
    if not sipoc_html.exists():
        raise RuntimeError(
            f"GATE: {sipoc_html} nao existe. Rode `build_sipoc.py` antes."
        )
    processo_fm = parse_ssot(ssot_dir / "processo-n2.md")
    slug = (processo_fm.get("processo") or {}).get("slug", "processo")
    code = (processo_fm.get("processo") or {}).get("code", "P").lower()
    dados_js = out_dir / f"dados-{slug}-{code}.js"
    if not dados_js.exists():
        raise RuntimeError(
            f"GATE: {dados_js} nao existe. Rode `build_sipoc.py` antes."
        )
    info(f"✓ Gate: {sipoc_html.name} e {dados_js.name} encontrados")

    # 2. Gate: SSOT valido
    run_check_ssot(ssot_dir, "jornada-cx")
    info("✓ check_ssot.py --target jornada-cx passou")

    # 3. Bootstrap
    bootstrap(out_dir)

    # 4. Parse SSOT
    jornada_fm = parse_ssot(ssot_dir / "jornada-cx.md")
    journey_obj = {
        "processos": jornada_fm.get("processos", []),
        "rows": jornada_fm.get("rows", []),
    }

    # 5. Escrever bloco P5_JOURNEY no journey-{slug}-{cod}.js
    journey_js_path = out_dir / f"journey-{slug}-{code}.js"
    block_content = f"window.P5_JOURNEY = {js_repr(journey_obj)};"
    write_js_block(journey_js_path, "P5_JOURNEY", block_content)
    info(f"✓ Bloco P5_JOURNEY escrito em {journey_js_path}")

    # 6. Copiar HTML shell estatico
    html_src = TEMPLATES_DIR / "html" / "jornada-cx.html"
    html_dst = out_dir / "jornada-cx.html"
    if not html_dst.exists():
        html_content = html_src.read_text(encoding="utf-8")
        html_content = html_content.replace("journey-P5-credito.js", f"journey-{slug}-{code}.js")
        html_dst.write_text(html_content, encoding="utf-8")
        info(f"✓ HTML shell: {html_dst}")

    success("Camada 3 OK.")
    info(f"Próximo passo: revise build/jornada-cx.html no browser, depois rode `build_datalake.py`")


def main():
    parser = argparse.ArgumentParser(description="Build Camada 3 (Jornada CX)")
    parser.add_argument("--ssot-dir", type=Path, default=Path("ssot/"))
    parser.add_argument("--out", type=Path, default=Path("build/"))
    args = parser.parse_args()

    try:
        build_jornada(args.ssot_dir.resolve(), args.out.resolve())
    except FileNotFoundError as e:
        error(str(e))
        sys.exit(2)
    except RuntimeError as e:
        error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
