# Changelog

## [1.3.2] - 2026-04-06

### Added
- Base64 (.b64) companions for all PNG assets in `drawing-deip-diagrams/assets/` and `mapping-process-interfaces/assets/` — enables self-contained HTML generation

## [1.3.1] - 2026-03-09

### Fixed
- `plugin.json`: removidos campos não-padrão `skills` e `agents` que impediam o carregamento do plugin no Claude.ai

## [1.3.0] - 2026-03-09

### Added
- Skill `mapping-process-flows`: entrevista estruturada para mapeamento de fluxo BPMN (dupla complementar de `drawing-bpmn-flowcharts`)
  - Workflow de 8 fases: Identificacao → Participantes → Evento de Inicio → Caminho Feliz → Gateways → Excecoes → Eventos de Fim → Artefatos
  - Adaptacao por nivel de modelagem: N1–N2 (logico, sem lanes) vs N3–N5 (fisico, com lanes e todos os elementos)
  - Coleta de pools, lanes, atividades, gateways (XOR/AND/OR/Event-based), boundary events e eventos intermediarios
  - Geracao de JSON no schema exato consumido por `drawing-bpmn-flowcharts` (sem reformatacao manual)
  - Validacao pre-geracao: estrutura de eventos, pareamento de gateways, nomenclatura de atividades
  - 2 artefatos de saida:
    - BPMN Input JSON (`-bpmn-input.json`): contrato consumido diretamente por `drawing-bpmn-flowcharts`
    - Descritivo do Fluxo (`-descritivo.md`): narrativa estruturada com caminho feliz, decisoes, excecoes
  - Referencia `interview-guide.md`: roteiro de entrevista com perguntas-sonda por fase e por nivel
  - Referencia `bpmn-flow-elements.md`: tabela "o usuario diz → elemento BPMN correto" para todos os tipos de no e conexao
  - Template `flow-descritivo.tmpl.md`: template Markdown com estrutura completa do descritivo do fluxo
- Simetria completa de skills: `mapping-process-interfaces` ↔ `drawing-deip-diagrams` / `mapping-process-flows` ↔ `drawing-bpmn-flowcharts`

## [1.2.0] - 2026-03-04

### Added
- Skill `mapping-process-interfaces`: entrevista estruturada para mapeamento de interfaces DEIP/SIPOC
  - Workflow de 8 fases: Identificacao → Outputs → Inputs → Suporte → Regulacao → Macrofluxo → Avaliacao → Geracao
  - Ordem output-first (orientado pelo proposito do processo, nao pela ordem do acronimo)
  - Iteracao com usuario via AskUserQuestion em todas as fases
  - Avaliacao individual de cada interface (conforme/melhoria/nao avaliado)
  - Identificacao de desconexoes com classificacao de impacto (Alto/Medio/Baixo)
  - 3 artefatos de saida:
    - DEIP JSON v2 (contrato consumido por `drawing-deip-diagrams`)
    - DEIP Descritivo (Markdown com template)
    - Tabela de Desconexoes (Excel .xlsx com branding M7-2026)
  - Referencia `interview-guide.md`: roteiro de entrevista com perguntas-sonda por fase
  - Referencia `disconnection-framework.md`: taxonomia D01-D15, escala de impacto, matriz priorizacao
  - Template `deip-descritivo.tmpl.md`: template Markdown com placeholders Mustache-style
  - Script `generate-disconnection-table.py`: gerador Excel via openpyxl com 3 abas (Desconexoes, Todas as Interfaces, Resumo), logo M7, formatacao condicional por impacto, auto-filtro
  - Assets: logos M7 copiados para self-containment

## [1.1.7] - 2026-03-04

### Changed
- Skill `drawing-deip-diagrams`: realce nos titulos Regulacao e Suporte (v2.5.2)
  - `.band-label` com fundo pill `verde-caqui-100`, cor primaria `verde-caqui`, font 10px
  - Padding e border-radius para efeito badge sutil

## [1.1.6] - 2026-03-04

### Fixed
- Skill `drawing-deip-diagrams`: linhas separadoras dos paineis input/output invisiveis (v2.5.1)
  - `border-bottom` dos `.iface-row` alterado de `verde-caqui-50` para `white` (mesma cor do fundo)
  - Layout e espacamento preservados (border mantido, apenas cor alterada)

## [1.1.5] - 2026-03-04

### Changed
- Skill `drawing-deip-diagrams`: header light + logo dark PNG (v2.5)
  - Header refatorado para fundo light (off-white), fora do container — mesmo estilo dos artefatos G2.2/G2.3
  - Logo M7 como PNG dark (m7-logo-dark.png) em fundo claro — identico aos demais artefatos
  - h1 com nome do processo, subtitulo "DEIP", meta e botoes a direita
  - Botoes com borda verde-caqui-100 em fundo transparente (light mode)
  - Cabecalho do painel de entradas: "Fornecedor" agora right-aligned proximo ao "#" (corrigido)
  - Assets: copiados m7-logo-dark.png e m7-logo-favicon.png do design-system-m7

## [1.1.4] - 2026-03-03

### Fixed
- Skill `drawing-deip-diagrams`: logo M7 visivel no header (v2.4)
  - Substituido `<img>` base64 PNG por SVG inline vetorial
  - PNG com tracos finos desaparecia em tamanhos pequenos (anti-aliasing do browser)
  - SVG `<text>` renderiza "M7" com nitidez em qualquer escala
  - Fallback de fonte: TWK Everett → Arial → sans-serif

## [1.1.3] - 2026-03-03

### Changed
- Skill `drawing-deip-diagrams`: refinamentos de layout e macrofluxo (v2.3)
  - Botoes (Copiar JSON, Imprimir) movidos para dentro do header a direita
  - Logo M7 com `object-fit: contain` para evitar compressao
  - Macrofluxo: banner chevron grande + lista numerada de etapas (substituindo chevrons individuais)
  - Faixas de regulacao/suporte com `min-height: 64px` para cards verticais
  - Legenda: adicionado circulo cinza = "Sem avaliacao"
  - Alinhamento de tipo (Sistema/Interno/Externo) na coluna de entrada replicando formato da saida
  - Toolbar externa removida

## [1.1.2] - 2026-03-03

### Changed
- Skill `drawing-deip-diagrams`: regulacao e suporte como cards verticais pareados (v2.2)
  - Regulacao: Provedor → [Rn] → Documento (mesmo formato visual de entradas/saidas)
  - Suporte: Recurso → [Sn] → Provedor (mesmo formato visual de entradas/saidas)
  - Campo `provider` adicionado ao schema de regulacao e suporte
  - Distribuicao vertical de entradas/saidas com `space-evenly` (sem espacos em branco)
  - Distribuicao horizontal de regulacao/suporte com `space-evenly`

## [1.1.1] - 2026-03-03

### Changed
- Skill `drawing-deip-diagrams`: refinamentos visuais no template DEIP (v2.1)
  - Cabecalho branded com logo M7 embutido em base64
  - Paineis de entradas/saidas centralizados verticalmente (sem espacos em branco)
  - Faixas de regulacao/suporte centralizadas horizontalmente
  - Regulacoes mostram tipo do provedor (Lei, Politica, etc.)
  - Suportes mostram tipo do recurso (Sistemas, Pessoas, etc.)
  - Chevrons estritamente lineares (sem quebra de linha)
- Asset: logo M7 copiado para assets/ (self-contained)

## [1.1.0] - 2026-03-03

### Changed
- Skill `drawing-deip-diagrams`: redesign completo do template DEIP (v2)
  - Layout single-page: cabe em uma pagina sem scroll vertical (A4 landscape)
  - Macrofluxo chevron: etapas como setas horizontais com CSS clip-path (substituindo boxes verticais)
  - Interfaces codificadas: circulos numerados com prefixo de zona (I1, O1, R1, S1) para mapeamento de desconexoes
  - Pares visuais: Fornecedor→[In]→Insumo e Produto→[On]→Cliente na mesma linha
  - Faixas laterais verticais "Entradas" e "Saidas" como orientacao visual
  - Tres status de interface: conforme (verde), melhoria (vermelho), neutro (cinza)
  - Tooltips em circulos melhoria mostram nota de desconexao
  - Motor `normalizeData()` para backward-compat: JSON v1 (arrays separados) auto-gera interfaces v2
- Referencia DEIP-STRUCTURE.md: secao 3.8 (Interfaces), schema v2 com array `interfaces`, referencia Votorantim/Aquila
- Referencia M7-BPM-THEME.md: tokens para circulos de interface, chevrons, process banner
- SKILL.md: workflow atualizado com coleta pareada, formato v2, dimensao #8 (Interfaces)

## [1.0.0] - 2026-03-02

### Added
- Plugin `mapeamento-processos` para mapeamento e construcao de processos BPM
- Skill `drawing-bpmn-flowcharts`: gera arquivos BPMN 2.0 XML (.bpmn) compativeis com Camunda Modeler, bpmn.io e Bizagi
  - Referencia completa de mapeamento JSON → XML (BPMN-XML-REFERENCE.md)
  - Catalogo de notacao BPMN 2.0 com coluna XML Element (BPMN-NOTATION.md)
  - Boas praticas e checklist de validacao estrutural XML (BPMN-BEST-PRACTICES.md)
  - Algoritmo de auto-layout para diagram interchange (coordenadas BPMNDiagram)
  - Suporte a pools, lanes, 14 tipos de evento, 7 tipos de atividade, 4 gateways, 3 tipos de conexao
  - Output duplo: `.bpmn` XML + `-descritivo.md` Markdown
- Skill `drawing-deip-diagrams`: gera Diagramas DEIP interativos como HTML autocontido
  - Layout CSS Grid 5 colunas, badges de status, macrofluxo visual
  - Template deip-base.html com design system M7-2026
- Agent `process-analyst`: decomposicao e analise de processos BPM N1-N5
- Agent `bpmn-reviewer`: validacao de notacao BPMN 2.0 com checklist de 7 categorias + validacao XML
- Entrada no marketplace.json
