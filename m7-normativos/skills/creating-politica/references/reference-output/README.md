# Gold Reference — POL-GOV-001

Este diretório contém o trio canônico que o agente
`politica-design-reviewer` usa como gabarito visual para comparar HTMLs
gerados pela skill `creating-politica`.

## Arquivos

- **POL-GOV-001-gold.html** — versão purificada de POL-GOV-001 (já era o
  HTML mais limpo dos 3 gerados em v3.x, sem componentes ad-hoc). É o
  ponto de calibração: outras POLs devem ter estrutura visual análoga
  (header/footer idênticos, capa com mesma composição, paginação A4
  igual, classes CSS dentro da allowlist).
- **POL-GOV-001-gold.yaml** — sidecar canônico do gold reference.
- **POL-GOV-001-gold.md** — MD-fonte da Fase 2, demonstrando uso correto
  dos shortcodes do `component-catalog.md`.

## Como o agente usa

Quando invocado, `politica-design-reviewer` carrega o gold reference HTML
e compara com o artefato em revisão:

1. **Estrutura idêntica** — capa, controle, 8 seções, versões, aprovações
2. **Header/footer consistentes** — logo, separador, código, classificação
3. **Tipografia conformada** — TWK Everett, weight 400 em headings
4. **Paleta canônica** — `var(--vc-*)`, `var(--lime)`, `var(--off-white)` (sem hex literal)
5. **Allowlist de classes** — toda classe no HTML tem entrada catalogada

Divergências que **não** são causadas por conteúdo diferente viram
ATENCAO ou CRITICO no relatório de review.

## Como atualizar

Se o template oficial mudar (ex.: adição de página nova, mudança em
classes estruturais), o gold reference precisa ser **regerado**:

1. Atualizar `politica-m7-template.html` e/ou `m7-tokens.css`
2. Rodar `python scripts/generate-html-yaml.py` apontando para o
   BRIEFING + MD-fonte do POL-GOV-001
3. Substituir os arquivos deste diretório
4. Bump de versão menor do plugin
5. Documentar no CHANGELOG o motivo da mudança

**Nunca edite manualmente o `POL-GOV-001-gold.html`** — sempre regere via
script. Edição manual quebra a propriedade "gold é determinístico a partir
do MD+YAML".
