# Geração HTML → PDF · Documento Oficial (N4)

Documento de apoio à [SKILL.md](../SKILL.md). Cobre o pipeline de renderização do PDF: drivers disponíveis, configuração, troubleshooting e limitações conhecidas.

## Sumário

1. [Drivers disponíveis](#1-drivers-disponíveis)
2. [Setup inicial](#2-setup-inicial)
3. [Uso do `render_pdf.py`](#3-uso-do-render_pdfpy)
4. [Modo compacto automático](#4-modo-compacto-automático)
5. [Limitações conhecidas](#5-limitações-conhecidas)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. Drivers disponíveis

A skill suporta dois drivers para HTML → PDF, seguindo o padrão estabelecido em [`m7-projects/scripts/build_opr.py`](../../../../m7-operations/m7-projects/skills/generating-status-materials/scripts/build_opr.py) e [`m7-apresentacoes/scripts/render.py`](../../../../m7-creative/m7-apresentacoes/skills/generating-presentation/scripts/render.py).

### Playwright (driver primário) — **recomendado**

- Engine: Chromium headless (~180 MB).
- Suporta CSS Paged Media Module Level 3 completo.
- `@page` named pages, `@font-face` com `font-display: swap`, `print-color-adjust`, gradientes radiais — tudo respeita.
- `prefer_css_page_size=True` no `page.pdf()` faz o Playwright usar `@page { size: A4 landscape }` declarado em CSS — crítico para alternar orientação no meio do documento.
- Detecta `document.body.scrollHeight` para acionar modo compacto se conteúdo estoura A4.

### WeasyPrint (fallback)

- Puro Python (~30 MB).
- Roda sem browser — útil quando Chromium não pode ser instalado (CI minimal, container, ambiente offline).
- Limitações:
  - `@page :first { margin: 0 }` nem sempre respeitado (capa pode receber footer indesejado).
  - Named pages (`page: cover`, `page: landscape`) com bugs ocasionais — versão landscape pode renderizar como retrato.
  - `font-display: swap` ignorado — usa o primeiro source disponível.
  - JS não executa — HTML deve estar pronto antes de virar PDF.
  - Sem detecção de overflow real (modo compacto precisa ser ligado proativamente).

### Decisão automática

`render_pdf.py` tenta Playwright primeiro. Se `playwright` não está instalado ou Chromium não está baixado, fallback automático para WeasyPrint. Mensagem warning impressa em stderr.

---

## 2. Setup inicial

### Opção A — Playwright (recomendado)

```bash
cd skills/mapeamento-n1
pip install -r scripts/requirements.txt
playwright install chromium
```

`playwright install chromium` baixa o browser uma vez (~180 MB, vai para `~/.cache/ms-playwright/`). Subsequentes invocações reutilizam.

### Opção B — Apenas WeasyPrint (sem browser)

```bash
cd skills/mapeamento-n1
pip install -r scripts/requirements.txt
pip install weasyprint
```

WeasyPrint requer dependências nativas do sistema (cairo, pango, gdk-pixbuf). Em macOS:
```bash
brew install pango gdk-pixbuf libffi
```
Em Debian/Ubuntu:
```bash
apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

---

## 3. Uso do `render_pdf.py`

### Sintaxe básica

```bash
python3 scripts/render_pdf.py <input.html> <output.pdf>
```

Exemplo:
```bash
cd /tmp/mapeamento-acme
python3 /path/to/skills/mapeamento-n1/scripts/render_pdf.py \
    documento-oficial-acme.html \
    documento-oficial-acme.pdf
```

Saída:
```
OK · documento-oficial-acme.pdf (3.42 MB)
     driver=playwright  compact=False  pages=24
```

### Flags

| Flag | Descrição |
|---|---|
| `--driver playwright` (default) | Tenta Playwright; fallback para WeasyPrint se falhar |
| `--driver weasyprint` | Usa só WeasyPrint (skip Playwright) |
| `--no-compact` | Desabilita modo compacto automático |

### Pré-condição: assets ao lado do HTML

O HTML referencia `m7-tokens.css`, `m7-header-dark.css`, `m7-print.css`, fontes em `fonts/` e logos em `assets/`. Esses arquivos **devem estar no mesmo diretório do HTML** (caminhos relativos).

A Fase C copia automaticamente quando gera o documento. Se for rodar `render_pdf.py` standalone, certifique-se de copiar antes:

```bash
cp templates/m7-tokens.css      /tmp/mapeamento-acme/
cp templates/m7-header-dark.css /tmp/mapeamento-acme/
cp templates/m7-print.css       /tmp/mapeamento-acme/
cp -r templates/fonts           /tmp/mapeamento-acme/
cp -r templates/assets          /tmp/mapeamento-acme/
```

### Exit codes

- `0` — PDF gerado com sucesso.
- `1` — Erro durante render (falha no Playwright, exception, etc.).
- `2` — Erro de uso (arquivo não existe, argumento inválido).

---

## 4. Modo compacto automático

### Detecção (Playwright apenas)

Após render inicial, executa JS:
```js
const pages = document.querySelectorAll('.page:not(.page--cover):not(.page--landscape)');
for (const p of pages) {
    if (p.scrollHeight > 1123) return true;  // A4 portrait @ 96dpi
}
return false;
```

Se alguma `.page` retrato excede 1123px de altura, ativa `body.compact` e re-renderiza. Páginas landscape e capa são ignoradas (têm dimensões diferentes).

### O que o `.compact` faz (em `m7-print.css`)

Reduz `padding`, `gap`, `font-size` em zonas específicas — **sem mexer na fonte do conteúdo principal** (preserva legibilidade):

```css
body.compact .section-title-print { font-size: 20pt; }   /* 24pt → 20pt */
body.compact .process-page .pp-name { font-size: 18pt; } /* 22pt → 18pt */
body.compact .process-page .mp-mission-text { font-size: 12pt; } /* 14pt → 12pt */
body.compact .process-page .sipoc-col-mission,
body.compact .process-page .sipoc-col-side { padding: 6mm 4mm; } /* 8mm 6mm → 6mm 4mm */
```

### Quando o compact não basta

Se o documento ainda excede A4 mesmo com compact, o Playwright **não** trunca — gera o PDF assim mesmo. O `pdf-validator` detecta no checklist visual e reporta.

Causas comuns:
- Texto de SIPOC com `inputs` muito longos (chip de 6+ palavras).
- `## Objetivo do diagrama` no BRIEFING com 3+ parágrafos.
- Mais de 1 fricção com texto muito longo.

Mitigação: revisar o BRIEFING para encurtar campos longos.

---

## 5. Limitações conhecidas

### Tamanho do PDF

Esperado: 3-6 MB para um BRIEFING completo (18 processos, 6 verticais, 28 relações). Causas:
- Fontes TWK Everett (6 OTF × ~80KB cada = 480KB) embedadas.
- Logo PNG (~30KB).
- Backgrounds com `print_background=True`.

Aceitável até 12 MB. Se passa disso, considerar:
- Subset de fontes (Chromium normalmente faz, mas pode falhar em casos específicos).
- Comprimir logos antes de copiar.
- Verificar se `m7-print.css` não está duplicando regras enormes.

### Compatibilidade entre PDF viewers

Testado em:
- Adobe Reader (macOS, Windows) — render perfeito.
- Preview macOS — render perfeito.
- Chrome PDF viewer — render perfeito, mas a animação de fricção do N3 é estática (esperado).
- Firefox PDF.js — render OK; ocasionalmente cores ligeiramente diferentes em gradientes.

### Hyperlinks

`<a href="...">` no HTML viram hyperlinks clicáveis no PDF (Playwright + WeasyPrint preservam). Útil para anexos / referências do BRIEFING.

### Animações

Animações CSS (ex.: halo pulsante das fricções no N3) **são removidas** em modo print pelo `@media print { .node[data-friction="true"] { animation: none !important; } }` em `m7-print.css`. Resultado: estático no PDF, dinâmico no HTML standalone.

---

## 6. Troubleshooting

### "Playwright não está instalado"

```
RuntimeError: Playwright nao instalado. Rode:
  pip install -r requirements.txt
  playwright install chromium
```

Solução: rodar os 2 comandos. `playwright install chromium` é separado do `pip install` — baixa o browser.

### "Capa renderiza com footer/margem"

Causa provável: WeasyPrint não respeitou `@page :first { margin: 0 }`.

Solução: rodar com Playwright. Se WeasyPrint é mandatório, aceitar que a capa tem 18mm de margem e o footer aparece — não bloqueia entrega.

### "Mapa neural N3 não está em landscape"

Causa provável: WeasyPrint não respeitou `@page landscape` declarado via `page: landscape`.

Solução: forçar Playwright (`--driver playwright`). Em ambiente sem Chromium, fallback é mapa em retrato comprimido (ainda funcional, menos elegante).

### "Texto cortado em meio de processo SIPOC"

Causa: `break-inside: avoid` em `.sipoc-bloc` não funcionou (CSS pre-Paged-Media-3 ou WeasyPrint).

Solução:
1. Verificar que `m7-print.css` está sendo carregado (Chrome devtools > Network).
2. Se persiste em WeasyPrint, encurtar chips ou aceitar corte.

### "Footer não aparece"

Causa: `@page @bottom-center { content: ... }` não suportado pelo viewer.

Solução: garantir Playwright. WeasyPrint suporta `@page @bottom-center` mas exige `@page` blocks fora de `@media print`. Verificar `m7-print.css` está usando `@page` no nível raiz.

### "Tamanho do PDF passou de 12 MB"

Causa: Chromium não fez subset de fontes (ocorre em algumas versões).

Solução:
1. Verificar versão do Playwright (`pip show playwright` — atualizar para >=1.40).
2. Reduzir número de pesos de fonte usados em CSS (TWK Everett vem com 6; talvez só 3 são usados de fato).
3. Aceitar até 15 MB para casos com 30+ processos.

### "Erro: Browser falhou ao iniciar"

Causa: Chromium não baixado ou corrompido.

Solução:
```bash
playwright install --force chromium
```

---

## Resumo

| Cenário | Driver recomendado |
|---|---|
| Desenvolvimento local em máquina M7 | Playwright |
| Render local em Linux com browser permitido | Playwright |
| CI/CD com cache de Chromium | Playwright |
| Container minimal sem browser | WeasyPrint (com aviso de limitações) |
| Validação rápida sem cuidado de paginação | WeasyPrint |
| Documento final de qualidade | Playwright (sempre) |

Para o caso M7 e a maioria dos casos, **sempre Playwright**. WeasyPrint é fallback de emergência, não escolha de produção.
