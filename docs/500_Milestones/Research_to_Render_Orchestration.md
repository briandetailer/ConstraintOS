# Research-to-Render Orchestration

## Status

```text
milestone: Research-to-Render Orchestration
status: active
started_on: 2026-07-17
branch: phase-1-cli-tooling
trigger: user clarified that ConstraintOS must research each imagery request rather than begin from a pre-registered renderer
current_checkpoint: request-driven research, capability selection, source materialization, and deterministic PDF source-plate extraction implemented
next_checkpoint: review extracted Raspberry Pi source plate and build its component-anchor and label registry
```

## Product intent

ConstraintOS accepts an imagery request and its constraints, researches reference material for that request, determines what the evidence supports, creates imagery using the selected evidence-backed method, and validates the output against the original constraints.

```text
request + constraints
        ↓
constraint normalization
        ↓
research planning
        ↓
web source discovery
        ↓
source authority and relevance evaluation
        ↓
capability classification
        ↓
versioned reference package
        ↓
source-backed render planning
        ↓
deterministic or research-conditioned imagery
        ↓
constraint and evidence validation
        ↓
manual review + provenance report
```

The Toyota and NASA paths remain regression fixtures. They do not define the user-facing architecture.

## New example outside the original fixture set

The first generalized request is:

```text
Create a repeatable top-view technical I/O plate of a Raspberry Pi 5.
Find authoritative references first.
Show and label the requested connectors.
Preserve the real board layout.
Do not invent hidden or unsupported components.
```

Required visible features include:

```text
- 40-pin GPIO header
- dual micro-HDMI ports
- two USB 3.0 ports
- two USB 2.0 ports
- Gigabit Ethernet
- USB-C power
- MIPI camera/display connectors
- PCIe FFC connector
- RTC battery connector
- PWM fan connector
```

The fixture does not identify a prebuilt scenario key as the source of truth. The request supplies subject, viewpoint, required visible features, forbidden features, repeatability, source-authority, labeling, exploratory-generation, and review constraints.

## Research architecture

### Constraint parser

`ConstraintRequest` normalizes the user request into executable fields. Required visible features may not be empty, and authority, repeatability, labeling, viewpoint, exploratory-generation, and review requirements are explicit.

### Research planner

The planner generates subject-specific searches for:

```text
- official product documentation
- official mechanical drawings
- official STEP/CAD/3D geometry
- official component and connector documentation
```

Research stops only after subject identity, requested-feature coverage, source provenance, usage-review state, and a supported rendering mode have been resolved or explicitly reported incomplete.

### Source discovery

Two modes are supported:

```text
recorded_source_fixture
- deterministic regression testing
- no API credits
- known source inventory

openai_responses_web_search
- live request-driven web research
- uses Responses API web search
- uses strict JSON-schema output
- requires OPENAI_API_KEY
- records response ID, model, search queries, and candidate count
```

The live discovery prompt prohibits invented URLs and returns source evidence only. It does not ask the model to generate imagery.

### Source evaluation

When authoritative sources are required, non-authoritative candidates are rejected. Each requested feature must be backed by at least one selected source or reported unsupported.

A source class determines capability:

```text
official_web_2d_source_plate
- may support deterministic fixed-view annotation

official_web_3d_geometry
verified_local_geometry
- may support deterministic geometry rendering and novel locked views

official_web_mechanical_drawing
- supporting dimensional evidence only
- cannot be promoted automatically into a component-rich source plate

official_web_*_documentation
- identity, terminology, connector inventory, and label evidence
- not a base image by itself
```

## Least-complex sufficient rendering rule

ConstraintOS selects the least-complex authoritative method that satisfies the request.

For the Raspberry Pi 5 locked top-view request:

```text
selected_mode: source_plate_annotation
reason: authoritative_fixed_view_source_plate_satisfies_requested_view_without_geometry_reconstruction
canonical_source: official Raspberry Pi product-brief top-view image
annotation_evidence: official product brief + official hardware documentation
mechanical_evidence: official mechanical drawing
geometry_fallback: official Raspberry Pi STEP package
```

For a request that changes only the viewpoint to a novel locked oblique view:

```text
selected_mode: geometry_render
reason: verified_geometry_required_for_requested_view_or_no_suitable_fixed_source_plate
canonical_source: official Raspberry Pi STEP package
```

This prevents both overuse of stochastic generation and unnecessary 3D reconstruction.

## Deterministic source-plate extraction

The selected Raspberry Pi source plate is an embedded raster on page index 1 of the official product brief. ConstraintOS does not redraw it.

The registered extraction workflow:

```text
1. read source-package-manifest.json
2. locate rpi5-official-top-view-source-plate-2026
3. verify the downloaded PDF SHA-256
4. open the registered page
5. enumerate embedded rasters
6. select the largest raster satisfying minimum dimensions and pixel area
7. preserve the extracted encoded image bytes
8. calculate output SHA-256
9. write source-plate-extraction-manifest.json
10. leave production_ready and approval_allowed false
```

The extraction contract explicitly prohibits automatic component identification and production approval. It creates the canonical visual asset needed for the next anchor-registration slice; it does not claim that labels are already validated.

## Fail-closed state

The source-plate path remains blocked until:

```text
- source package is materialized and SHA-256 verified
- source plate is extracted and manually reviewed
- fixed-view contract is registered
- requested component anchors are registered
- approved label strings are linked to official evidence
- deterministic SVG render preset is registered
- usage terms are reviewed
```

The geometry fallback remains blocked until:

```text
- STEP archive is materialized and SHA-256 verified
- archive is extracted
- geometry is normalized
- component inventory is registered
- camera and render preset are locked
- repeat-render comparison is implemented
- usage terms are reviewed
```

## Implemented artifacts

```text
runtime/research_to_render/models.py
runtime/research_to_render/orchestrator.py
runtime/research_to_render/discovery.py
runtime/research_to_render/cli.py
runtime/research_to_render/source_plate.py
config/research-to-render-examples/raspberry-pi-5-io-plate-request.json
config/research-to-render-examples/raspberry-pi-5-discovered-sources.json
config/research-source-plate-extraction/raspberry-pi-5-product-brief-v1.json
config/technical-reference-source-registry.json
scripts/exercise-research-to-render.ps1
scripts/prepare-technical-reference-source-package.ps1
scripts/prepare-raspberry-pi-5-source-plate.ps1
tests/test_research_to_render_orchestration.py
tests/test_research_to_render_cli.py
tests/test_research_to_render_discovery.py
tests/test_research_source_plate_extraction.py
```

Installed CLIs:

```text
cos-research-render
cos-extract-source-plate
```

## Implementation slices

```text
[x] Add request and source models
[x] Add request-derived research planner
[x] Add authoritative source evaluator
[x] Add source-class capability classifier
[x] Add least-complex sufficient render-mode selection
[x] Add deterministic recorded-source fixture mode
[x] Add live OpenAI Responses web-search discovery adapter
[x] Add strict source-discovery JSON schema
[x] Add research-to-render CLI
[x] Add Windows exercise script
[x] Make source-package materializer registry-driven
[x] Add Raspberry Pi 5 request outside the original four examples
[x] Register official Raspberry Pi source plate, STEP, drawing, and documentation
[x] Register deterministic product-brief source-plate extraction contract
[x] Add digest-verified embedded-raster extraction worker
[x] Add Windows source-plate preparation script
[ ] Materialize and hash Raspberry Pi source package on Windows
[ ] Extract and visually review official top-view source plate on Windows
[ ] Build Raspberry Pi component-anchor and label registry
[ ] Add deterministic Raspberry Pi SVG plate renderer
[ ] Add repeat-render comparison
[ ] Add Workbench request input for generalized orchestration
[ ] Run live discovery and compare it with recorded fixture
[ ] Record visual acceptance evidence
```

## Acceptance criteria

```text
1. A new request can be planned without adding a hardcoded application route.
2. Research queries derive from the request subject and required features.
3. Live discovery returns web-found source candidates using a strict schema.
4. Non-authoritative sources are rejected when authority is required.
5. Every required visible feature is evidenced or explicitly unsupported.
6. Source capability may not exceed its source class.
7. Mechanical drawings cannot silently become component-rich base plates.
8. A sufficient fixed source plate is preferred over unnecessary geometry reconstruction.
9. Novel viewpoints select verified geometry when available.
10. Image generation is not required for the Raspberry Pi technical plate.
11. Source-document and extracted-image digests are recorded.
12. Extracted source bytes are preserved without model-generated alteration.
13. Rendering remains fail-closed until anchor, preset, repeatability, and usage gates pass.
14. Final imagery is validated against the original request and preserves manual review.
```
