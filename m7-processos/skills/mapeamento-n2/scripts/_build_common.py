"""mapeamento-n2 · helpers compartilhados pelos build_*.py.

Funcoes principais:
    - bootstrap(out_dir): copia CSS/fonts/assets do templates/ para out_dir/
    - parse_ssot(path): le frontmatter YAML do SSOT MD e devolve dict
    - load_n1_briefing(path): le BRIEFING.md da N1 e devolve dict
    - render_template(path, mapping): str.replace de {{key}} por mapping[key]
    - check_no_placeholder(path): grep por {{ no arquivo, raise se encontrar
    - run_check_ssot(ssot_dir, target): chama check_ssot.py e raise se bloqueador
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "ERRO: PyYAML nao instalado. Rode: pip install -r requirements.txt\n"
    )
    sys.exit(2)


SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
SCRIPTS_DIR = SKILL_DIR / "scripts"


# ============================================================================
# Bootstrap: copia assets estaticos para out_dir
# ============================================================================


def bootstrap(out_dir: Path) -> None:
    """Copia CSS/fonts/assets/sipoc-deip.js para out_dir, se ausentes.

    Idempotente — nao sobrescreve se ja existe.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "fonts").mkdir(exist_ok=True)
    (out_dir / "assets").mkdir(exist_ok=True)

    # CSS files
    for css in ["m7-tokens.css", "m7-header-dark.css",
                "mapeamento.css", "mapeamento-views.css"]:
        src = TEMPLATES_DIR / css
        dst = out_dir / css
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)

    # Fonts (4 .otf)
    for otf in (TEMPLATES_DIR / "fonts").glob("*.otf"):
        dst = out_dir / "fonts" / otf.name
        if not dst.exists():
            shutil.copy2(otf, dst)

    # Assets (3 .png)
    for png in (TEMPLATES_DIR / "assets").glob("*.png"):
        dst = out_dir / "assets" / png.name
        if not dst.exists():
            shutil.copy2(png, dst)


# ============================================================================
# SSOT parsing
# ============================================================================


def parse_ssot(path: Path) -> dict:
    """Le frontmatter YAML de um SSOT MD. Retorna dict (vazio se frontmatter ausente)."""
    if not path.exists():
        raise FileNotFoundError(f"SSOT nao encontrado: {path}")
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        raise ValueError(
            f"Frontmatter YAML nao encontrado em {path} (esperado entre `---` no topo)."
        )
    return yaml.safe_load(m.group(1)) or {}


def extract_section(path: Path, header: str) -> str:
    """Extrai conteudo de uma secao markdown (ate proximo '## ' ou EOF).

    Args:
        path: path do MD
        header: ex.: '## Lede'

    Returns:
        conteudo da secao (sem o header), strip
    """
    text = path.read_text(encoding="utf-8")
    pattern = rf"^{re.escape(header)}\s*\n(.*?)(?=\n##\s|\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not m:
        return ""
    return m.group(1).strip()


def load_n1_briefing(path: Path) -> dict:
    """Le BRIEFING.md da N1 e devolve frontmatter YAML como dict."""
    if not path.exists():
        raise FileNotFoundError(f"BRIEFING N1 nao encontrado: {path}")
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        raise ValueError(f"Frontmatter YAML nao encontrado no BRIEFING N1: {path}")
    return yaml.safe_load(m.group(1)) or {}


# ============================================================================
# Template rendering (str.replace de {{key}})
# ============================================================================


def render_template(template_path: Path, mapping: dict) -> str:
    """Le template e substitui {{key}} por mapping[key].

    Chaves nao presentes em mapping ficam como estao no output — o check
    posterior (check_no_placeholder) vai sinalizar.
    """
    text = template_path.read_text(encoding="utf-8")
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text


def check_no_placeholder(path: Path) -> list:
    """Procura por {{ no arquivo. Retorna lista de (linha, conteudo) onde encontrou."""
    matches = []
    text = path.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), 1):
        if "{{" in line:
            matches.append((i, line.strip()))
    return matches


# ============================================================================
# Slug helpers
# ============================================================================


def slugify_code(code: str) -> str:
    """Converte 'P5.1' em 'p5-1' (formato id do JS data)."""
    return code.lower().replace(".", "-")


# ============================================================================
# JS data file helpers (read/write parcial de blocks)
# ============================================================================


JS_BLOCK_START = "/* === BLOCK:{name} === */"
JS_BLOCK_END = "/* === ENDBLOCK:{name} === */"


def write_js_block(js_path: Path, block_name: str, content: str) -> None:
    """Escreve ou substitui um bloco delimitado dentro de um arquivo JS.

    Se o arquivo nao existe, cria com header + bloco.
    Se o bloco existe, substitui in-place.
    Se o bloco nao existe, anexa ao final.
    """
    start = JS_BLOCK_START.format(name=block_name)
    end = JS_BLOCK_END.format(name=block_name)
    block = f"{start}\n{content}\n{end}\n"

    if not js_path.exists():
        js_path.write_text(
            f"/* journey/data file gerado por mapeamento-n2. NAO editar manualmente. */\n\n{block}",
            encoding="utf-8",
        )
        return

    text = js_path.read_text(encoding="utf-8")
    pattern = rf"{re.escape(start)}.*?{re.escape(end)}\n?"
    if re.search(pattern, text, re.DOTALL):
        new_text = re.sub(pattern, block, text, flags=re.DOTALL)
    else:
        new_text = text.rstrip() + "\n\n" + block
    js_path.write_text(new_text, encoding="utf-8")


# ============================================================================
# Validation gate
# ============================================================================


def run_check_ssot(ssot_dir: Path, target: str) -> dict:
    """Roda check_ssot.py --target {target} e retorna o JSON parseado.

    Raise RuntimeError se exit code != 0 (ou seja, ha bloqueadores).
    """
    ssot_file = ssot_dir / f"{target}.md"
    if not ssot_file.exists():
        raise FileNotFoundError(f"SSOT nao encontrado para validacao: {ssot_file}")

    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "check_ssot.py"),
        "--target", target,
        "--json",
        str(ssot_file),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        parsed = json.loads(result.stdout) if result.stdout else {"bloqueadores": [], "avisos": []}
    except json.JSONDecodeError:
        parsed = {"bloqueadores": [], "avisos": [],
                  "raw_stdout": result.stdout, "raw_stderr": result.stderr}

    if result.returncode != 0:
        bloqueadores = parsed.get("bloqueadores", [])
        raise RuntimeError(
            f"check_ssot.py reportou {len(bloqueadores)} bloqueador(es) em {target}.md:\n"
            + "\n".join(f"  - [{b.get('rule_id')}] {b.get('where')}: {b.get('message')}"
                        for b in bloqueadores)
        )
    return parsed


# ============================================================================
# Output helpers
# ============================================================================


def info(msg: str) -> None:
    print(f"\033[36m[mapeamento-n2]\033[0m {msg}")


def success(msg: str) -> None:
    print(f"\033[32m[mapeamento-n2 ✓]\033[0m {msg}")


def warn(msg: str) -> None:
    print(f"\033[33m[mapeamento-n2 ⚠]\033[0m {msg}")


def error(msg: str) -> None:
    print(f"\033[31m[mapeamento-n2 ✗]\033[0m {msg}", file=sys.stderr)
