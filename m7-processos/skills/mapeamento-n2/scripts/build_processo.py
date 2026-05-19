#!/usr/bin/env python3
"""build_processo.py · Camada 1 da Fase C.

Gera build/processo-n2.html a partir de ssot/processo-n2.md.

Gate (entrada):
    - n1_artifacts.briefing existe
    - processo.code ∈ processos[] do BRIEFING N1
    - check_ssot.py --target processo-n2 passa (exit 0)

Output:
    - build/processo-n2.html (renderizado)
    - build/m7-tokens.css, m7-header-dark.css, mapeamento.css, mapeamento-views.css
    - build/fonts/*.otf, build/assets/*.png

Uso:
    python build_processo.py --ssot-dir ssot/ --out build/
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Import compartilhado
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _build_common import (
    TEMPLATES_DIR, bootstrap, parse_ssot, extract_section, render_template,
    check_no_placeholder, run_check_ssot, info, success, warn, error,
)


def build_processo(ssot_dir: Path, out_dir: Path) -> None:
    info(f"Iniciando Camada 1 · Processo N2 (ssot={ssot_dir}, out={out_dir})")

    # 1. Gate: validar SSOT
    run_check_ssot(ssot_dir, "processo-n2")
    info("✓ check_ssot.py --target processo-n2 passou")

    # 2. Bootstrap
    bootstrap(out_dir)
    info("✓ Bootstrap (CSS/fonts/assets) OK")

    # 3. Parse SSOT
    ssot_path = ssot_dir / "processo-n2.md"
    fm = parse_ssot(ssot_path)
    proc = fm.get("processo", {})
    subprocs = fm.get("subprocessos", [])
    interfaces = fm.get("interfaces", [])
    lede = extract_section(ssot_path, "## Lede")

    # 4. Construir mapping de placeholders
    mapping = {
        "CODE": proc.get("code", ""),
        "NOME_PROCESSO": proc.get("name", ""),
        "SLUG_PROCESSO": proc.get("slug", ""),
        "OWNER": proc.get("owner", ""),
        "RECEITA_META": proc.get("receita_meta", ""),
        "DESCRICAO": proc.get("descricao", ""),
        "LEDE": lede,
        "WBS": fm.get("wbs", ""),
        "JANELA": fm.get("janela", ""),
        "STATUS": fm.get("status", ""),
    }

    mapping["N_SUBPROCS"] = str(len(subprocs))

    # ===== M7_SUBPROC_BUTTONS: botões da pool M7 (1 por subproc, com seq-mini entre eles) =====
    btn_parts = []
    for i, sp in enumerate(subprocs):
        sp_id = sp.get('id', '')
        btn = f"""              <button class="subproc" data-sipoc="{sp_id}">
                <div class="sp-code">{sp.get('code', '')}</div>
                <div class="sp-name">{sp.get('name', '')}</div>
                <div class="sp-meta">{sp.get('sp_meta', '')}</div>
                <div class="sp-tech">{sp.get('sp_tech', '')}</div>
                <span class="sp-cadence">{sp.get('cadence', '')}</span>
              </button>"""
        btn_parts.append(btn)
        if i < len(subprocs) - 1:
            btn_parts.append('              <div class="seq-mini"></div>')
    mapping["M7_SUBPROC_BUTTONS"] = "\n".join(btn_parts)

    # ===== CLIENTE_ROW: eventos + mensagens da pool Cliente (1 elemento por subproc) =====
    # Cada subproc tem 1 interface (mensagem cliente↔M7) mostrada acima dele.
    # 1º subproc => start event; último => end event ou msg-recv; resto => cliente-msg.
    iface_by_code = {i.get('code'): i.get('message', '') for i in interfaces}
    cli_parts = []
    n = len(subprocs)
    for i, sp in enumerate(subprocs):
        sp_code = sp.get('code', '')
        msg = iface_by_code.get(sp_code, '')
        # Resumo curto da mensagem para o cliente-msg (1ª metade antes do "/" se houver)
        msg_short = msg.split('/')[0].strip().split('→')[-1].strip()[:80]
        if i == 0:
            elem = f'              <div class="ev start" title="{msg_short}"></div>'
        elif i == n - 1:
            elem = f'              <div class="ev end" title="{msg_short}"></div>'
        else:
            elem = f'              <div class="cliente-msg">{msg_short}</div>'
        cli_parts.append(elem)
        if i < n - 1:
            cli_parts.append('              <div class="cliente-spacer"></div>')
    mapping["CLIENTE_ROW"] = "\n".join(cli_parts)

    # 5. Render
    template_path = TEMPLATES_DIR / "html" / "processo-n2.tmpl.html"
    rendered = render_template(template_path, mapping)
    output_path = out_dir / "processo-n2.html"
    output_path.write_text(rendered, encoding="utf-8")
    info(f"✓ Renderizado: {output_path}")

    # 6. Validar
    remaining = check_no_placeholder(output_path)
    if remaining:
        error(f"PLACEHOLDER-RESTANTE: {len(remaining)} ocorrencia(s) em {output_path}")
        for line_no, content in remaining[:10]:
            error(f"  L{line_no}: {content[:120]}")
        sys.exit(1)

    success(f"Camada 1 OK. Output: {output_path}")
    info("Próximo passo: revise o HTML no browser, depois rode `build_sipoc.py --subproc {ID}` para cada subprocesso")


def main():
    parser = argparse.ArgumentParser(description="Build Camada 1 (Processo N2)")
    parser.add_argument("--ssot-dir", type=Path, default=Path("ssot/"),
                       help="Pasta com os 4 SSOT MDs")
    parser.add_argument("--out", type=Path, default=Path("build/"),
                       help="Pasta de output")
    args = parser.parse_args()

    try:
        build_processo(args.ssot_dir.resolve(), args.out.resolve())
    except FileNotFoundError as e:
        error(str(e))
        sys.exit(2)
    except RuntimeError as e:
        error(f"GATE FALHOU: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
