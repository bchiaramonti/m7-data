---
name: drawing-bpmn-flowcharts
description: "Generates BPMN 2.0 XML files (.bpmn) compatible with Camunda Modeler, bpmn.io, and Bizagi, plus a descriptive Markdown file (.md) for each process. Supports all BPMN elements (events, activities, gateways, pools/lanes), auto-layout for diagram interchange, and full BPMN 2.0 namespace compliance. Input via structured JSON or conversational description. Use when the user asks to draw, create, or generate a process flowchart, BPMN diagram, or process map."
---

# BPMN 2.0 XML Generator

Generate standard BPMN 2.0 XML files (.bpmn) that open in Camunda Modeler, bpmn.io, Bizagi, or any compliant BPMN tool. Each process also gets a descriptive Markdown file with flow narrative.

## Philosophy

> "Nao desenhe caixas. Revele o fluxo de valor."

This skill generates **portable BPMN 2.0 XML** — the industry standard for process interchange. No proprietary formats, no visual dependencies, no build tools. The `.bpmn` file opens in any BPMN editor for visual editing and can be executed by process engines like Camunda.

## What This Adds

| Aspect | Manual Diagram | This Skill |
|--------|---------------|------------|
| Format | Proprietary tool file | Standard BPMN 2.0 XML (.bpmn) |
| Notation | Varies by author | BPMN 2.0 OMG standard |
| Portability | Locked in tool | Opens in Camunda, bpmn.io, Bizagi, Signavio |
| Layout | Manual positioning | Auto-layout with diagram interchange coordinates |
| Documentation | Separate document | Paired `-descritivo.md` with flow narrative |
| Version control | Binary diff | Git-friendly XML text diff |
| Reusability | Requires re-export | JSON data → regenerate anytime |

## Self-Contained Dependencies

```
<this-skill>/
├── SKILL.md                        # This file
└── references/
    ├── BPMN-NOTATION.md            # Complete BPMN 2.0 element catalog + JSON schema
    ├── BPMN-BEST-PRACTICES.md      # Quality rules and validation checklist
    └── BPMN-XML-REFERENCE.md       # XML generation rules, auto-layout, examples
```

## Workflow

### Phase 1: Gather Process Definition

Collect the process definition from the user. Accept two input modes:

**Mode A — Conversational**: Ask the user to describe the process step by step:
1. What is the process name and level (N1-N5)?
2. Who are the participants (areas/actors → lanes)?
3. What are the main steps (activities)?
4. What decisions exist (gateways)?
5. How does it start and end (events)?
6. Are there parallel paths or loops?

Convert the answers into the JSON schema defined in [BPMN-NOTATION.md](references/BPMN-NOTATION.md#8-schema-json-de-input).

**Mode B — Structured JSON**: Accept a pre-built JSON following the schema. Validate it against the expected structure.

### Phase 2: Validate & Structure

Before generating, validate the process definition:

1. **Structural completeness**:
   - Exactly 1 start event per process
   - At least 1 end event
   - All paths reach an end event
   - No disconnected nodes

2. **Gateway pairing**:
   - Every diverging gateway has a converging pair
   - XOR gateways have labels on all outgoing flows
   - XOR gateways have a default path

3. **Naming conventions** (see [BPMN-BEST-PRACTICES.md](references/BPMN-BEST-PRACTICES.md)):
   - Activities use verb + complement (infinitive or 3rd person)
   - No generic names ("Processar", "Executar")
   - Gateway labels as questions ("Aprovado?")

4. **Level-appropriate elements**:
   - N1-N2 (logical): no lanes, simple events/gateways only
   - N3-N5 (physical): lanes, all event/gateway types, boundary events

Report any issues to the user and suggest fixes before proceeding.

### Phase 3: Generate .bpmn XML + Descriptive Markdown

#### Step 3a — Generate `.bpmn` file

Read [BPMN-XML-REFERENCE.md](references/BPMN-XML-REFERENCE.md) for complete XML generation rules and the auto-layout algorithm. Then:

1. Build the XML document following the BPMN 2.0 structure:
   - `<bpmn:definitions>` root element with all 5 required namespace declarations
   - `<bpmn:collaboration>` containing `<bpmn:participant>` elements (one per pool) and `<bpmn:messageFlow>` elements (if any)
   - One `<bpmn:process>` per pool, each containing:
     - `<bpmn:laneSet>` with lanes and `<bpmn:flowNodeRef>` lists
     - All flow nodes (events, tasks, gateways) with `<bpmn:incoming>`/`<bpmn:outgoing>` children
     - All `<bpmn:sequenceFlow>` elements with `sourceRef`/`targetRef`
     - Artifacts (data objects, annotations, associations)
   - `<bpmndi:BPMNDiagram>` containing `<bpmndi:BPMNPlane>` with:
     - A `<bpmndi:BPMNShape>` (with `<dc:Bounds>`) for every pool, lane, and flow node
     - A `<bpmndi:BPMNEdge>` (with `<di:waypoint>`) for every connection

2. Compute layout coordinates using the auto-layout algorithm defined in BPMN-XML-REFERENCE.md (Section 4)

3. Save as `<process-name>.bpmn`

#### Step 3b — Generate descriptive Markdown

Generate a structured Markdown file with these sections:

1. **Cabecalho** — Process metadata (title, level, version, date, author)
2. **Participantes** — Table listing each pool and its lanes
3. **Narrativa do Fluxo** — Step-by-step walkthrough of the happy path, written as numbered prose
4. **Pontos de Decisao** — Each gateway with its question, conditions, and resulting paths
5. **Interfaces** — Message flows between pools (if multi-pool), describing who sends what to whom
6. **Artefatos** — Data objects, data stores, and annotations referenced in the process
7. **Observacoes** — Gaps identified, assumptions made, and improvement opportunities

Save as `<process-name>-descritivo.md`

### Phase 4: Review & Refine

After generation:
1. Suggest the user open the `.bpmn` file in Camunda Modeler, bpmn.io, or Bizagi
2. Offer to invoke the `bpmn-reviewer` agent for notation validation
3. Accept feedback and regenerate with adjustments

## Input Format

Two modes supported (see Phase 1). The JSON schema:

```json
{
  "metadata": {
    "title": "string — Process name",
    "level": "string — N1|N2|N3|N4|N5",
    "version": "string — e.g. 1.0",
    "date": "string — YYYY-MM-DD",
    "author": "string"
  },
  "pools": [
    {
      "id": "string",
      "name": "string",
      "isExecutable": "boolean (optional, default false)",
      "lanes": [{ "id": "string", "name": "string" }]
    }
  ],
  "nodes": [
    {
      "id": "string",
      "type": "string — see BPMN-NOTATION.md for all types",
      "label": "string",
      "lane": "string — lane id",
      "pool": "string — pool id",
      "description": "string — maps to bpmn:documentation (optional)",
      "attachedTo": "string — activity id for boundary events (optional)"
    }
  ],
  "edges": [
    {
      "id": "string",
      "type": "string — sequenceFlow | messageFlow | association",
      "source": "string — source node id",
      "target": "string — target node id",
      "label": "string — edge label (optional)",
      "isDefault": "boolean — marks XOR gateway default path (optional)",
      "condition": "string — formal expression for conditional flows (optional)"
    }
  ]
}
```

Full schema documentation with field descriptions in [BPMN-NOTATION.md](references/BPMN-NOTATION.md#8-schema-json-de-input).

## Output

Two files per process:

**`<process-name>.bpmn`** — Valid BPMN 2.0 XML with:
- Full namespace compliance (bpmn, bpmndi, dc, di, xsi)
- Process model: collaboration, participants, processes, lane sets, flow nodes, sequence/message flows
- Diagram interchange: BPMNShapes with Bounds and BPMNEdges with waypoints for auto-layout
- Bidirectional flow references (incoming/outgoing on every flow node)
- Compatible with Camunda Modeler, bpmn.io, Bizagi, Signavio, and any BPMN 2.0 compliant tool
- No proprietary extensions — pure OMG BPMN 2.0

**`<process-name>-descritivo.md`** — Structured Markdown with:
- Process metadata and participants table
- Happy-path flow narrative as numbered steps
- Decision points with conditions and paths
- Inter-pool interfaces (message flows)
- Artifacts referenced
- Observations and improvement opportunities

## BPMN Elements Supported

Full catalog with XML element mapping in [BPMN-NOTATION.md](references/BPMN-NOTATION.md). Summary:

| Category | Elements |
|----------|----------|
| **Events** | Start (none, message, timer, signal), Intermediate (none, message, timer, error, signal), End (none, message, error, terminate) |
| **Activities** | Task, User Task, Service Task, Script Task, Send Task, Receive Task, Subprocess |
| **Gateways** | Exclusive (XOR), Parallel (AND), Inclusive (OR), Event-based |
| **Connections** | Sequence Flow, Message Flow, Association |
| **Divisions** | Pools, Lanes, Milestones |
| **Artifacts** | Data Object, Data Store, Group, Annotation |

## Additional Resources

- For complete BPMN element specifications and XML mapping: [BPMN-NOTATION.md](references/BPMN-NOTATION.md)
- For quality validation rules: [BPMN-BEST-PRACTICES.md](references/BPMN-BEST-PRACTICES.md)
- For XML generation rules, auto-layout algorithm, and annotated example: [BPMN-XML-REFERENCE.md](references/BPMN-XML-REFERENCE.md)
- For notation validation after generation: invoke the `bpmn-reviewer` agent
