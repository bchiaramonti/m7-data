#!/usr/bin/env python3
"""build_sipoc.py · Camada 2 da Fase C.

Itera processo-a-processo (--subproc P5.X) ou todos (--all-subproc).
Gera/atualiza build/dados-{slug}-{cod}.js (window.P5_DATA equivalente)
+ copia build/sipoc-deip.html e build/sipoc-deip.js estaticos.

Gate (entrada):
    - build/processo-n2.html existe (Camada 1 OK)
    - check_ssot.py --target sipocs passa

Uso:
    python build_sipoc.py --ssot-dir ssot/ --out build/ --subproc P5.1
    python build_sipoc.py --ssot-dir ssot/ --out build/ --all-subproc
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _build_common import (
    TEMPLATES_DIR, bootstrap, parse_ssot, run_check_ssot,
    info, success, error, slugify_code,
)


def js_repr(value):
    """Representa valor Python como literal JS valido."""
    return json.dumps(value, ensure_ascii=False, indent=2)


def generate_dados_js(processo_fm: dict, sipocs_fm: dict, subproc_filter: list = None) -> str:
    """Gera o conteudo do dados-{slug}-{cod}.js.

    Se subproc_filter informado, so hidrata esses subprocs (resto vira placeholder).
    Senao, hidrata todos.
    """
    proc = processo_fm.get("processo", {})
    all_subs = sipocs_fm.get("subprocessos", [])

    if subproc_filter:
        sub_set = set(subproc_filter)
        # Para subprocs nao filtrados, mantemos placeholder (eles sao adicionados em chamadas futuras)
        # Aqui simplificamos: incluimos todos os subprocs do sipocs.md, mesmo que o filtro tenha so 1
        # (consistencia com check_ssot que exige sipocs.md completo). Filtro afeta so a mensagem de log.
        pass

    interfaces = processo_fm.get("interfaces", [])

    data_obj = {
        "meta": {
            "code": proc.get("code", ""),
            "name": proc.get("name", ""),
            "camada": proc.get("camada", ""),
            "owner": proc.get("owner", ""),
            "receita_meta": proc.get("receita_meta", ""),
            "descricao": proc.get("descricao", ""),
        },
        "subprocessos": all_subs,
        "interfaces": interfaces,
    }

    js_content = f"""/* ===================================================================
   {proc.get('code', '')} {proc.get('name', '')} — Dados N2 (DEIPs)
   Gerado por build_sipoc.py. NAO editar manualmente.
   =================================================================== */

window.P5_DATA = {js_repr(data_obj)};
"""
    return js_content


def build_sipoc(ssot_dir: Path, out_dir: Path,
                subproc: str = None, all_subproc: bool = False) -> None:
    info(f"Iniciando Camada 2 · SIPOC/DEIP (subproc={subproc or 'ALL' if all_subproc else 'first-only'})")

    # 1. Gate: Camada 1 OK
    processo_html = out_dir / "processo-n2.html"
    if not processo_html.exists():
        raise RuntimeError(
            f"GATE: {processo_html} nao existe. Rode `build_processo.py` primeiro."
        )
    info(f"✓ Gate: {processo_html} encontrado")

    # 2. Gate: SSOT valido
    run_check_ssot(ssot_dir, "sipocs")
    info("✓ check_ssot.py --target sipocs passou")

    # 3. Bootstrap (idempotente)
    bootstrap(out_dir)

    # 4. Parse SSOTs
    processo_fm = parse_ssot(ssot_dir / "processo-n2.md")
    sipocs_fm = parse_ssot(ssot_dir / "sipocs.md")
    slug = (processo_fm.get("processo") or {}).get("slug", "processo")
    code = (processo_fm.get("processo") or {}).get("code", "P").lower()

    # 5. Filtro de subproc para mensagem
    all_codes = [s.get("code") for s in sipocs_fm.get("subprocessos", [])]
    if subproc and not all_subproc:
        if subproc not in all_codes:
            raise ValueError(f"--subproc {subproc!r} nao encontrado em sipocs.md. "
                           f"Disponiveis: {all_codes}")
        subproc_filter = [subproc]
        info(f"Hidratando subproc {subproc} (outros mantidos como estao no SSOT)")
    else:
        subproc_filter = None
        info(f"Hidratando todos os {len(all_codes)} subprocs: {all_codes}")

    # 6. Gerar JS data file
    dados_js = generate_dados_js(processo_fm, sipocs_fm, subproc_filter)
    dados_path = out_dir / f"dados-{slug}-{code}.js"
    dados_path.write_text(dados_js, encoding="utf-8")
    info(f"✓ JS data file: {dados_path}")

    # 7. Copiar HTML shell estatico
    html_src = TEMPLATES_DIR / "html" / "sipoc-deip.html"
    html_dst = out_dir / "sipoc-deip.html"
    if not html_dst.exists():
        # Customizar o <script src> para apontar para o JS gerado
        html_content = html_src.read_text(encoding="utf-8")
        html_content = html_content.replace("dados-P5-credito.js", f"dados-{slug}-{code}.js")
        html_dst.write_text(html_content, encoding="utf-8")
        info(f"✓ HTML shell: {html_dst}")

    # 8. Copiar JS renderer estatico
    renderer_src = TEMPLATES_DIR / "html" / "sipoc-deip.js"
    renderer_dst = out_dir / "sipoc-deip.js"
    if not renderer_dst.exists():
        shutil.copy2(renderer_src, renderer_dst)
        info(f"✓ JS renderer: {renderer_dst}")

    msg = f"Camada 2 OK. Subproc {subproc}." if subproc and not all_subproc else "Camada 2 OK."
    success(msg)

    # 9. Sugerir próximo passo
    if subproc and not all_subproc:
        # Encontra próximo subproc
        try:
            idx = all_codes.index(subproc)
            if idx + 1 < len(all_codes):
                next_sp = all_codes[idx + 1]
                info(f"Próximo: revise build/sipoc-deip.html?sp={slugify_code(subproc)} "
                     f"no browser, depois rode `build_sipoc.py --subproc {next_sp}`")
            else:
                info("Último subproc. Próximo passo: rode `build_jornada.py`")
        except ValueError:
            pass
    else:
        info("Próximo passo: revise build/sipoc-deip.html, depois rode `build_jornada.py`")


def main():
    parser = argparse.ArgumentParser(description="Build Camada 2 (SIPOC/DEIP)")
    parser.add_argument("--ssot-dir", type=Path, default=Path("ssot/"))
    parser.add_argument("--out", type=Path, default=Path("build/"))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--subproc", type=str, help="Code do subproc (ex: P5.1)")
    group.add_argument("--all-subproc", action="store_true",
                      help="Hidrata todos os subprocs de uma vez (use so apos validar 1 a 1)")
    args = parser.parse_args()

    try:
        build_sipoc(args.ssot_dir.resolve(), args.out.resolve(),
                    args.subproc, args.all_subproc)
    except FileNotFoundError as e:
        error(str(e))
        sys.exit(2)
    except (RuntimeError, ValueError) as e:
        error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
