# exemplo-build-p5/

Diretório destinado ao output da Fase C rodada sobre o `examples/exemplo-ssot-p5/`.

## Como gerar localmente

```bash
cd skills/mapeamento-n2/

# 1. Validar SSOTs
python3 scripts/check_ssot.py --all examples/exemplo-ssot-p5/

# 2. Build em camadas
python3 scripts/build_processo.py  --ssot-dir examples/exemplo-ssot-p5/ --out examples/exemplo-build-p5/
python3 scripts/build_sipoc.py     --ssot-dir examples/exemplo-ssot-p5/ --out examples/exemplo-build-p5/ --all-subproc
python3 scripts/build_jornada.py   --ssot-dir examples/exemplo-ssot-p5/ --out examples/exemplo-build-p5/
python3 scripts/build_datalake.py  --ssot-dir examples/exemplo-ssot-p5/ --out examples/exemplo-build-p5/

# 3. Abrir no browser
open examples/exemplo-build-p5/processo-n2.html
```

## Referencia visual

O output deve ser visualmente equivalente aos arquivos em `/Users/bchiaramonti/Downloads/process-mapping-n2.zip` (gabarito original do P5 Crédito).

Este diretório é mantido vazio no repositório (apenas com este README) para que o smoke test gere fresh em cada teste.
