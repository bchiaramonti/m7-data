#!/usr/bin/env python3
"""build_datalake.py · Camada 4 da Fase C.

Gera/atualiza window.P5_DATALAKE dentro de build/journey-{slug}-{cod}.js
(mesmo arquivo de Camada 3, completando-o) + copia build/data-lake.html.

Gate (entrada):
    - build/journey-{slug}-{cod}.js existe (Camada 3 OK)
    - check_ssot.py --target data-lake passa

Uso:
    python build_datalake.py --ssot-dir ssot/ --out build/
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


def build_datalake(ssot_dir: Path, out_dir: Path) -> None:
    info(f"Iniciando Camada 4 · Data Lake (ssot={ssot_dir}, out={out_dir})")

    # 1. Gate: Camada 3
    processo_fm = parse_ssot(ssot_dir / "processo-n2.md")
    slug = (processo_fm.get("processo") or {}).get("slug", "processo")
    code = (processo_fm.get("processo") or {}).get("code", "P").lower()
    journey_js = out_dir / f"journey-{slug}-{code}.js"
    if not journey_js.exists():
        raise RuntimeError(
            f"GATE: {journey_js} nao existe. Rode `build_jornada.py` antes."
        )
    info(f"✓ Gate: {journey_js.name} encontrado")

    # 2. Gate: SSOT valido
    run_check_ssot(ssot_dir, "data-lake")
    info("✓ check_ssot.py --target data-lake passou")

    # 3. Bootstrap
    bootstrap(out_dir)

    # 4. Parse SSOT
    dlk_fm = parse_ssot(ssot_dir / "data-lake.md")
    datalake_obj = {
        "processos": dlk_fm.get("processos", []),
        "rows": dlk_fm.get("rows", []),
        "marts": dlk_fm.get("marts", {}),
        "consumers": dlk_fm.get("consumers", []),
    }

    # 5. Escrever bloco P5_DATALAKE no mesmo journey-{slug}-{cod}.js
    block_content = f"window.P5_DATALAKE = {js_repr(datalake_obj)};"
    write_js_block(journey_js, "P5_DATALAKE", block_content)
    info(f"✓ Bloco P5_DATALAKE adicionado em {journey_js}")

    # 6. Copiar HTML shell
    html_src = TEMPLATES_DIR / "html" / "data-lake.html"
    html_dst = out_dir / "data-lake.html"
    if not html_dst.exists():
        html_content = html_src.read_text(encoding="utf-8")
        html_content = html_content.replace("journey-P5-credito.js", f"journey-{slug}-{code}.js")
        html_dst.write_text(html_content, encoding="utf-8")
        info(f"✓ HTML shell: {html_dst}")

    success("Camada 4 OK · pipeline completo.")
    info("Pipeline N2 finalizado. Abra cada arquivo em build/ no browser:")
    info("  - build/processo-n2.html")
    info("  - build/sipoc-deip.html")
    info("  - build/jornada-cx.html")
    info("  - build/data-lake.html")


def main():
    parser = argparse.ArgumentParser(description="Build Camada 4 (Data Lake)")
    parser.add_argument("--ssot-dir", type=Path, default=Path("ssot/"))
    parser.add_argument("--out", type=Path, default=Path("build/"))
    args = parser.parse_args()

    try:
        build_datalake(args.ssot_dir.resolve(), args.out.resolve())
    except FileNotFoundError as e:
        error(str(e))
        sys.exit(2)
    except RuntimeError as e:
        error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
