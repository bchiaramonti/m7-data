---
name: drawing-deip-diagrams
description: "Generates interactive DEIP (Diagrama de Escopo, Interface e Processos) as self-contained HTML files. Shows regulation, suppliers, inputs, macroflow (chevron), outputs, customers, and support with numbered interface circles (I1, O1, R1, S1) color-coded by compliance (green=conforme, red=melhoria, gray=neutral). Single-page fit, A4 landscape print. Use when the user asks to create a DEIP, scope diagram, process interface diagram, or needs to map inputs/outputs of a process."
---

# DEIP Generator — Diagrama de Escopo, Interface e Processos

Generate interactive, print-ready DEIP diagrams as self-contained HTML files following the BPM CBOK methodology.

## Philosophy

> "Antes de desenhar o fluxo, entenda as fronteiras."

The DEIP is the **first artifact** in process mapping — it defines scope, interfaces, and relationships before any BPMN flowchart is drawn. This skill is **self-contained** — it bundles the HTML template and M7-2026 design tokens.

## What This Adds

| Aspect | Manual DEIP (PowerPoint) | This Skill |
|--------|--------------------------|------------|
| Format | Static slide | Interactive HTML with tooltips |
| Interfaces | Unlabeled arrows | Numbered circles (I1, O1, R1, S1) with color status |
| Relationships | Separate columns | Paired rows: Supplier→[In]→Input, Output→[On]→Customer |
| Macroflow | Boxes or text | Horizontal chevron arrows |
| Layout | Variable size | Single-page fit (no scroll), A4 landscape print |
| Reusability | Locked in PPTX | JSON data → regenerate anytime |
| Validation | Manual review | Completeness + interface coherence check |

## Self-Contained Dependencies

```
<this-skill>/
├── SKILL.md                        # This file
├── templates/
│   └── deip-base.html              # HTML+CSS+JS DEIP template (v2)
└── references/
    ├── DEIP-STRUCTURE.md            # Complete DEIP anatomy, JSON schema v1+v2
    ├── DEIP-EXAMPLES.md             # Inventory of existing DEIPs in vault
    └── M7-BPM-THEME.md             # Design tokens for BPM diagrams
```

## Workflow

### Phase 1: Gather DEIP Data

Collect the 7+1 dimensions of the DEIP. Accept two input modes:

**Mode A — Conversational Interview**: Ask the user sequentially:

1. **Metadata**: What is the process name, code, responsible area, BPM level (N1-N5)?
2. **Regulacao**: What laws, policies, norms, or procedures regulate this process? For each, is the interface conforme (🟢) or has improvement opportunities (🔴)?
3. **Fornecedores + Entradas**: Who delivers what inputs to this process? Pair each supplier with its input — these become numbered interfaces (I1, I2, ...).
4. **Macrofluxo**: What are the 3-8 main steps of the process? (simplified, not full BPMN)
5. **Saidas + Clientes**: What does the process deliver and to whom? Pair each output with its customer — these become numbered interfaces (O1, O2, ...).
6. **Suporte**: What resources are needed? (people with headcount, systems, equipment)

For each interface (input/output/regulation), explicitly ask about the status: conforme, melhoria, or not yet assessed.

Convert answers into the JSON schema defined in [DEIP-STRUCTURE.md](references/DEIP-STRUCTURE.md#5-json-schema-de-input).

**Mode B — Structured JSON**: Accept pre-built JSON. Validate against schema. The engine auto-generates interfaces from v1 format if the `interfaces` array is absent.

### Phase 2: Validate Completeness

Before generating, check all dimensions:

1. **All dimensions filled**: Every section has at least 1 item. If regulation is absent, explicitly note "Sem regulacao identificada"
2. **Interface coherence**: Every input has a corresponding supplier (paired via `origin`). Every output has a corresponding customer (paired via `destination`)
3. **Macroflow length**: Between 3-8 steps (simplification rule)
4. **Status annotations**: Interfaces marked as 🔴 must have an observation note explaining the gap
5. **No duplicates**: Each item appears once in its respective dimension
6. **Interface numbering**: All interfaces are coded with zone prefix (I, O, R, S) + sequential number

Report gaps to the user and suggest completion before proceeding.

### Phase 3: Generate HTML

1. Read the template at `templates/deip-base.html`
2. Replace `window.DEIP_DATA` with the validated JSON (preferably v2 format with `interfaces` array)
3. Update `{{PROCESS_NAME}}` in the `<title>` tag
4. Save as `<process-name>-deip.html` in the workspace

The template renders:
- **Header**: Process name, code, responsible, level, version, date (compact)
- **Regulation band**: Badges with [Rn] circles + document names
- **Left panel**: Paired rows — Fornecedor → [In] → Insumo
- **Center panel**: Process banner + horizontal chevron macroflow
- **Right panel**: Paired rows — Produto → [On] → Cliente
- **Support band**: Tags with [Sn] circles
- **Footer**: Color legend and methodology reference
- **Interactivity**: Hover on 🔴 circles shows improvement notes

### Phase 4: Review & Annotate

After generation:
1. Review the output with the user
2. Suggest interfaces that might be 🔴 based on common patterns (missing POPs, manual handoffs, system gaps)
3. Offer to invoke `process-analyst` agent for deeper analysis
4. Accept feedback and regenerate with adjustments

## Input Format

The template accepts two JSON formats. **v2 is recommended** (includes `interfaces` array). v1 (legacy) is auto-converted by the rendering engine.

See [DEIP-STRUCTURE.md](references/DEIP-STRUCTURE.md#5-json-schema-de-input) for the complete schema with examples.

Key fields:

```json
{
  "metadata": { "processName": "", "code": "", "responsible": "", "date": "", "level": "", "version": "" },
  "regulation": [{ "name": "", "type": "", "status": "conforme|melhoria", "note": "" }],
  "suppliers": [{ "name": "", "type": "Interno|Externo|Sistema", "status": "" }],
  "inputs": [{ "name": "", "description": "", "origin": "supplier-name", "status": "" }],
  "macroflow": ["step 1", "step 2", "..."],
  "outputs": [{ "name": "", "destination": "customer-name", "status": "" }],
  "customers": [{ "name": "", "type": "Interno|Externo|Regulador", "status": "" }],
  "support": [{ "name": "", "type": "Pessoas|Sistemas|Equipamentos|Infraestrutura" }],
  "interfaces": [{ "id": "I1", "zone": "input", "provider": "", "artifact": "", "status": "", "note": "" }]
}
```

## Output

A single self-contained HTML file with:
- **Single-page layout**: No vertical scroll — fits viewport and A4 landscape
- **Chevron macroflow**: Horizontal arrow-shaped steps in the center
- **Numbered interface circles**: I1, O1, R1, S1 — green (conforme), red (melhoria), gray (neutral)
- **Paired interface rows**: Supplier→[In]→Input and Output→[On]→Customer on same line
- **Vertical side labels**: "Entradas" (left) and "Saidas" (right) as orientation
- **Print optimized**: A4 landscape via Ctrl+P (toolbar hidden, colors preserved)
- **Copy JSON**: Button to copy the v2-normalized source data for future editing
- **M7-2026 theme**: TWK Everett font, verde-caqui palette, lime accent
- **No external dependencies**: all CSS, JS, and fonts inline or CDN-resilient

## DEIP Dimensions Summary

| # | Dimension | Position | Content |
|---|-----------|----------|---------|
| 0 | Metadata | Header | Process name, code, responsible, level, date |
| 1 | Regulacao | Top band | Laws, norms, policies with [Rn] circle status |
| 2+3 | Entradas | Left panel | Paired: Fornecedor → [In] → Insumo |
| 4 | Macrofluxo | Center | 3-8 chevron steps |
| 5+6 | Saidas | Right panel | Paired: Produto → [On] → Cliente |
| 7 | Suporte | Bottom band | Resources with [Sn] circles |
| 8 | Interfaces | All zones | Coded connections (I/O/R/S prefix) for disconnection mapping |

## Additional Resources

- For DEIP anatomy and rules: [DEIP-STRUCTURE.md](references/DEIP-STRUCTURE.md)
- For real-world DEIP examples: [DEIP-EXAMPLES.md](references/DEIP-EXAMPLES.md)
- For color/typography specifications: [M7-BPM-THEME.md](references/M7-BPM-THEME.md)
- For process decomposition before DEIP: invoke the `process-analyst` agent
