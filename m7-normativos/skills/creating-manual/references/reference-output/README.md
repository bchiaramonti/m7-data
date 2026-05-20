# Gold Reference — MAN-PERF-003

Este diretório contém o trio canônico que o agente `manual-design-reviewer`
usa como gabarito visual para comparar HTMLs gerados pela skill
`creating-manual`.

## Arquivos

- **MAN-PERF-003-gold.html** — manual de "Rituais de Gestão" da área de
  Performance, usado como ponto de calibração visual. Outros MANs devem
  ter estrutura visual análoga (11 páginas A4, header/footer idênticos,
  capa com mesma composição, BPMN/SIPOC/RACI/KPI/Cronograma seguindo o
  mesmo padrão, classes CSS dentro da allowlist).
- **MAN-PERF-003-gold.yaml** *(starter)* — sidecar canônico starter,
  reflete os metadados visíveis no HTML. Pode ser usado como ponto de
  partida para validar o pipeline de geração contra o gold.
- **MAN-PERF-003-gold.md** *(starter)* — MD-fonte da Fase 2 starter,
  demonstrando uso correto dos shortcodes do `component-catalog-manual.md`.

> **Nota**: os arquivos `.yaml` e `.md` são *starters* derivados por
> engenharia reversa do `.html`. A propriedade de **determinismo total**
> (rodar `generate-html-yaml.py --briefing gold.yaml --content gold.md`
> produz o `gold.html` byte-a-byte) **não é garantida** nesta versão
> inicial — o gold HTML foi gerado manualmente antes da skill existir e
> contém variações estilísticas que não estão capturadas no YAML+MD
> minimalistas. Para validação de regressão visual, use o agente
> `manual-design-reviewer` (comparação semântica), não diff binário.

## Como o agente usa

Quando invocado, `manual-design-reviewer` carrega o gold reference HTML
e compara com o artefato em revisão:

1. **Estrutura idêntica** — capa, 11 páginas, 10 seções numeradas
2. **Header/footer consistentes** — logo, separador, código, classificação
3. **Tipografia conformada** — TWK Everett, weight 400 em headings
4. **Paleta canônica** — `var(--vc-*)`, `var(--lime)`, `var(--off-white)` (sem hex literal)
5. **Allowlist de classes** — toda classe no HTML tem entrada catalogada
6. **Componentes procedurais** — BPMN com viewBox + setas conectadas,
   SIPOC 5-col completo, RACI 5×5 com cores semânticas, KPI/PPI simétricos,
   Cronograma com 5 cadências

Divergências que **não** são causadas por conteúdo diferente viram
ATENCAO ou CRITICO no relatório de review.

## Como atualizar

Se o template oficial mudar (ex.: adição de página nova, mudança em
classes estruturais), o gold reference precisa ser **regerado**:

1. Atualizar `assets/manual-m7-template.html` e/ou `m7-tokens.css`
2. Rodar `python scripts/generate-html-yaml.py` apontando para o
   BRIEFING + MD-fonte do MAN-PERF-003 (após melhorar os starters para
   produzir output idêntico ao gold)
3. Substituir os arquivos deste diretório
4. Bump de versão menor do plugin
5. Documentar no CHANGELOG o motivo da mudança

**Nunca edite manualmente o `MAN-PERF-003-gold.html`** — sempre regere via
script ou substitua por uma versão atualizada gerada pelo autor original.
