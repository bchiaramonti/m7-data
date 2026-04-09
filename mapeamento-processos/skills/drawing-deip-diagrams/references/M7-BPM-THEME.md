# M7-BPM Theme — Design Tokens para Diagramas de Processos

Design tokens M7-2026 mapeados para elementos BPM (fluxogramas BPMN e diagramas DEIP).
Fonte: Brandbook M7 Investimentos 2026 + design-tokens.md (m7-design-system).

---

## Tipografia

```css
font-family: "twkEverett", "twkEverett Fallback", Arial, Helvetica, sans-serif;
```

### Font-face declarations

```css
@font-face {
  font-family: twkEverett;
  src: url("https://multi7.com.br/_next/static/media/TWKEverett_Regular-s.p.4411e19a.otf") format("opentype");
  font-weight: 400; font-display: swap;
}
@font-face {
  font-family: twkEverett;
  src: url("https://multi7.com.br/_next/static/media/TWKEverett_Medium-s.p.784da8c1.otf") format("opentype");
  font-weight: 500; font-display: swap;
}
@font-face {
  font-family: twkEverett;
  src: url("https://multi7.com.br/_next/static/media/TWKEverett_Bold-s.p.e7df9fc8.otf") format("opentype");
  font-weight: 700; font-display: swap;
}
@font-face {
  font-family: twkEverett Fallback;
  src: local(Arial);
  ascent-override: 91.9%; descent-override: 19.2%;
  line-gap-override: 9.1%; size-adjust: 109.91%;
}
```

### Escala tipografica BPM

| Elemento | Peso | Tamanho | Uso |
|----------|------|---------|-----|
| Titulo do diagrama | 700 | 24px | Header principal |
| Nome do processo/pool | 700 | 16px | Pools, lanes |
| Label de atividade | 500 | 13px | Dentro de retangulos BPMN |
| Label de gateway | 400 | 12px | Perguntas de decisao |
| Label de conexao | 400 | 11px | Sim/Nao, condicoes |
| Anotacoes | 400 | 11px | Notas explicativas |
| Metadata (data, versao) | 400 | 11px | Footer |

---

## Paleta de Cores — Elementos BPM

### Cores base

```css
:root {
  /* M7-2026 Brand */
  --verde-caqui: #424135;
  --verde-caqui-600: #35342a;
  --verde-caqui-700: #28271f;
  --verde-caqui-400: #66655b;
  --verde-caqui-300: #8a8981;
  --verde-caqui-200: #aeada8;
  --verde-caqui-100: #d0d0cc;
  --verde-caqui-50: #f6f6f5;
  --off-white: #fffdef;
  --off-white-600: #cccabe;
  --off-white-800: #66655f;
  --lime: #eef77c;
  --lime-soft: rgba(238,247,124,0.15);
  --white: #ffffff;

  /* Status */
  --success: #4CAF50;
  --error: #E46962;
  --warning: #F59E0B;
  --info: #0066ff;

  /* Data series */
  --blue: #0066ff;
  --amber: #F59E0B;
  --purple: #8B5CF6;
  --teal: #14B8A6;

  /* Layout */
  --radius: 12px;
  --radius-sm: 8px;
  --shadow-sm: 0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
  --transition: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Mapeamento: elemento BPMN → cor

| Elemento BPMN | Fundo | Borda | Texto | Icone |
|----------------|-------|-------|-------|-------|
| **Start Event** | `--white` | `--success` 2px | — | `--success` |
| **Intermediate Event** | `--white` | `--verde-caqui-300` 2px | — | `--verde-caqui` |
| **End Event** | `--error` fill | `--error` 3px | — | `--white` |
| **User Task** | `--off-white` | `--verde-caqui` 1.5px | `--verde-caqui` | `--verde-caqui-400` |
| **Service Task** | `--verde-caqui-50` | `--verde-caqui` 1.5px | `--verde-caqui` | `--info` |
| **Script Task** | `--verde-caqui-50` | `--verde-caqui` 1.5px | `--verde-caqui` | `--purple` |
| **Subprocess** | `--off-white` | `--verde-caqui` 1.5px dashed | `--verde-caqui` | — |
| **XOR Gateway** | `--white` | `--verde-caqui` 1.5px | `--verde-caqui` | X |
| **AND Gateway** | `--white` | `--verde-caqui` 1.5px | `--verde-caqui` | + |
| **OR Gateway** | `--white` | `--verde-caqui` 1.5px | `--verde-caqui` | O |
| **Pool (header)** | `--verde-caqui` | — | `--off-white` | — |
| **Pool (body)** | `--white` | `--verde-caqui-200` 1px | — | — |
| **Lane (header)** | `--verde-caqui-50` | `--verde-caqui-200` 1px | `--verde-caqui` | — |
| **Sequence Flow** | — | `--verde-caqui` 1.5px | `--verde-caqui-400` | Arrow |
| **Message Flow** | — | `--verde-caqui-300` 1.5px dashed | `--verde-caqui-400` | Circle+Arrow |
| **Data Object** | `--white` | `--verde-caqui-300` 1px | `--verde-caqui-400` | — |
| **Annotation** | transparent | `--verde-caqui-200` left 1px | `--verde-caqui-400` | — |

### Mapeamento: elemento DEIP → cor

| Elemento DEIP | Fundo | Borda | Texto |
|---------------|-------|-------|-------|
| **Header** | `--verde-caqui` | — | `--off-white` |
| **Regulacao band** | `--verde-caqui-50` | `--verde-caqui-200` bottom | `--verde-caqui` |
| **Reg badge conforme** | `rgba(76,175,80,0.08)` | `--success` 1px | `#2e7d32` |
| **Reg badge melhoria** | `rgba(228,105,98,0.08)` | `--error` 1px | `#c62828` |
| **Side stripe (Entradas/Saidas)** | `--verde-caqui` | — | `--off-white` |
| **Panel header** | — | `--verde-caqui-100` bottom | `--verde-caqui-400` |
| **Interface pair row** | `--white` | `--verde-caqui-50` bottom | `--verde-caqui` |
| **Interface circle conforme** | `--success` fill | — | `--white` 8px bold |
| **Interface circle melhoria** | `--error` fill | — | `--white` 8px bold |
| **Interface circle neutral** | `--verde-caqui-300` fill | — | `--white` 8px bold |
| **Process banner** | `--verde-caqui` | — | `--off-white` |
| **Macro box** | `--white` | `--verde-caqui-200` 2px dashed | `--verde-caqui` |
| **Chevron step** | `--verde-caqui` | — (clip-path) | `--off-white` |
| **Chevron step hover** | `--verde-caqui-700` | — (clip-path) | `--off-white` |
| **Suporte band** | `--verde-caqui-50` | `--verde-caqui-200` top | `--verde-caqui` |
| **Support tag** | `--white` | `--verde-caqui-200` 1px | `--verde-caqui` |

### Interface circle dimensions

| Propriedade | Valor |
|-------------|-------|
| Diametro | 22px |
| Font size | 8px |
| Font weight | 700 |
| Border radius | 50% |
| Clip-path chevron | `polygon(0 0, calc(100%-14px) 0, 100% 50%, calc(100%-14px) 100%, 0 100%, 14px 50%)` |

---

## Espacamento

| Token | Valor | Uso |
|-------|-------|-----|
| Padding atividade | 12px 16px | Dentro de retangulos de atividade |
| Gap entre elementos | 40px horizontal, 30px vertical | Entre nodes no fluxograma |
| Lane header width | 36px | Rotulo vertical da lane |
| Pool padding | 16px | Margem interna do pool |
| DEIP cell padding | 16px | Padding de cada celula do DEIP |
| DEIP gap | 0 | Sem gap entre celulas (bordas compartilhadas) |

---

## Dimensoes SVG

| Elemento | Largura | Altura | Raio |
|----------|---------|--------|------|
| Task | 160px | 48px | 8px |
| Subprocess | 180px | 56px | 8px |
| Event (circle) | 36px | 36px | 18px |
| Gateway (diamond) | 44px | 44px | — |
| Data Object | 36px | 44px | — |

---

## Tema alternativo: BPMN Classic

Para uso fora do contexto M7, aplicar override:

```css
:root[data-theme="bpmn-classic"] {
  --verde-caqui: #333333;
  --verde-caqui-50: #f5f5f5;
  --verde-caqui-100: #e0e0e0;
  --verde-caqui-200: #cccccc;
  --verde-caqui-300: #999999;
  --verde-caqui-400: #666666;
  --off-white: #ffffff;
  --lime: #2196F3;
  --success: #4CAF50;
  --error: #f44336;
}
```
