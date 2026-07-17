# Research-to-Render Orchestration

## Status

```text
milestone: Research-to-Render Orchestration
status: active
started_on: 2026-07-17
branch: phase-1-cli-tooling
trigger: ConstraintOS must research each book-imagery request and create new constrained artwork from that evidence
current_checkpoint: reference-conditioned generation package, candidate generator, and independent visual validator implemented
next_checkpoint: run the Raspberry Pi reference-conditioned candidate through the provider and review validation evidence
```

## Product intent

ConstraintOS exists to populate required imagery for a publication from user-supplied constraints. Research material is evidence supplied to the generation pipeline. It is not automatically the final artwork.

```text
book image request
        ↓
constraint extraction and normalization
        ↓
request-derived web research
        ↓
authority, relevance, and capability evaluation
        ↓
versioned and hashed reference package
        ↓
generation-constraint compiler
        ↓
reference-conditioned image-generation worker
        ↓
generated candidate artwork
        ↓
independent reference + constraint validation
        ↓
repair / rerender / reject / manual review
        ↓
deterministic labels, callouts, and publication finishing
```

The Toyota, NASA, Raspberry Pi, and other examples are regression fixtures for this general mechanism. They do not define separate hardcoded products.

## Drift correction

The first source-backed implementation stopped at deterministic source extraction and source-plate annotation. That was useful for provenance and repeatability, but it omitted the central product stage: creating new imagery from the researched reference package.

The corrected distinction is:

```text
request: annotate this exact source image
→ source_plate_annotation

request: create new book artwork using this evidence
→ reference_conditioned_generation

request: create a new viewpoint supported by verified geometry
→ geometry_render

insufficient visual or geometry evidence
→ reference_bundle_only
```

A matching source image is therefore not the final book illustration unless the request explicitly asks to annotate that source image.

## Generalized Raspberry Pi request

```text
Create a repeatable top-view technical I/O plate of a Raspberry Pi 5.
Research authoritative references first.
Preserve the real board layout.
Show all required connectors.
Do not invent hidden or unsupported components.
Create new publication-ready technical artwork.
Do not generate labels inside the raster.
```

Required visible features:

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

Visual constraints include a locked orthographic top view, complete uncropped board, publication-ready controlled linework, white background, restrained grayscale and blue palette, and clean space for deterministic annotations.

## Research architecture

### Constraint parser

`ConstraintRequest` normalizes subject, output type, viewpoint, required visible features, forbidden features, repeatability, source-authority requirements, labeling strategy, exploratory-generation policy, and manual-review requirements.

The request fixture also carries explicit `visual_output` constraints:

```text
- illustration style
- composition
- palette
- background
- surface treatment
- label strategy
- output size
- quality
- candidate count
```

### Research planner and discovery

The planner derives searches from the request rather than a scenario key. It searches for official product imagery, technical documentation, mechanical drawings, and verified geometry.

Two discovery modes remain available:

```text
recorded_source_fixture
- deterministic regression testing
- no API credits

openai_responses_web_search
- live request-driven research
- strict structured source records
- URLs must be discovered rather than invented
```

### Source evaluation

Each required feature must be supported by selected evidence or reported unsupported. Non-authoritative candidates are rejected when authority is required.

Source classes limit what the system may do:

```text
official_web_2d_source_plate
- binding identity, geometry, placement, proportion, and viewpoint reference
- supports reference-conditioned generation for a matching requested view
- supports direct annotation only when explicitly requested

official_web_3d_geometry / verified_local_geometry
- supports normalized deterministic rendering
- supports novel locked views
- may also produce controlled generation references

official_web_mechanical_drawing
- supporting dimensional evidence
- cannot silently become a component-rich base image

official documentation
- identity, terminology, component inventory, and validation evidence
- does not create imagery by itself
```

## Reference-conditioned generation package

`candidate_generation.py` compiles the request, render plan, and extracted reference manifest into a provider-neutral generation package.

The package records:

```text
- request ID and subject
- selected production mode
- exact required visible features
- exact forbidden features
- explicit visual-output constraints
- canonical reference file and SHA-256
- binding reference roles
- compiled prompt and prompt SHA-256
- provider/tool configuration
- candidate count
- required post-generation workers
```

The compiled prompt requires a **new illustration** while treating the attached source as binding evidence for identity, silhouette, proportions, orientation, component count, and relative placement. It prohibits generic substitution, invented geometry, cropped required features, generated labels, dimensions, arrows, title blocks, and unrelated scenery.

The reference is sent to the image worker as a high-detail image input. The image-generation tool is configured for an edit/reference-conditioned action with high input fidelity. Generated PNG candidates and their SHA-256 digests are recorded in `generated-candidate-manifest.json`.

Provider generation cannot approve its own output.

## Independent visual constraint validation

`candidate_validation.py` sends the authoritative reference and generated candidate to a separate validation call.

It requires strict structured evidence for:

```text
- subject identity
- requested viewpoint
- every exact required visible feature
- every exact forbidden feature
- requested visual style
- reference fidelity
- repair instructions
```

Validation is fail-closed:

```text
any failed check
→ rejected

any uncertain check and no failed check
→ needs_review

all checks pass
→ machine_passed, but manual review still required

missing, duplicated, or unexpected constraint checks
→ rejected
```

The validator writes per-candidate evidence and a candidate-validation manifest. It never enables automatic production approval.

## Annotation and publication finishing

The image model creates the base illustration and composition. It does not create production typography.

After a candidate passes automated validation and human review:

```text
approved generated base illustration
        ↓
registered component anchors
        ↓
deterministic SVG labels and leader lines
        ↓
layout bounds and typography checks
        ↓
publication export
```

This preserves the original book workflow: AI-generated illustration, deterministic technical text and finishing.

## Repeatability definition

Reference-conditioned generation is stochastic. ConstraintOS must not claim byte-identical image output from repeated provider calls.

Repeatability for this mode means:

```text
- same normalized request schema
- same researched reference package and digests
- same compiled constraints and prompt digest
- same provider/tool configuration
- candidate artifact digests recorded
- every candidate evaluated by the same validation schema
- failed candidates repaired, rerendered, or rejected
```

Byte-repeat comparison remains appropriate for deterministic source annotation and deterministic geometry rendering, not for stochastic candidate generation.

## Implemented artifacts

```text
runtime/research_to_render/models.py
runtime/research_to_render/orchestrator.py
runtime/research_to_render/discovery.py
runtime/research_to_render/cli.py
runtime/research_to_render/source_plate.py
runtime/research_to_render/candidate_generation.py
runtime/research_to_render/candidate_validation.py

config/research-to-render-examples/raspberry-pi-5-io-plate-request.json
config/research-to-render-examples/raspberry-pi-5-discovered-sources.json
config/research-source-plate-extraction/raspberry-pi-5-product-brief-v1.json
config/technical-reference-source-registry.json

scripts/exercise-research-to-render.ps1
scripts/prepare-technical-reference-source-package.ps1
scripts/prepare-raspberry-pi-5-source-plate.ps1
scripts/generate-raspberry-pi-5-candidates.ps1

tests/test_research_to_render_orchestration.py
tests/test_research_to_render_cli.py
tests/test_research_to_render_discovery.py
tests/test_research_source_plate_extraction.py
tests/test_reference_conditioned_candidate_generation.py
tests/test_reference_conditioned_candidate_validation.py
```

Installed CLIs:

```text
cos-research-render
cos-extract-source-plate
cos-generate-candidates
cos-validate-generated-candidates
```

## Implementation slices

```text
[x] Add request and source models
[x] Add request-derived research planner
[x] Add authoritative source evaluator
[x] Add live and recorded source discovery
[x] Add registry-driven source materialization
[x] Extract and hash a canonical visual reference
[x] Add explicit visual-generation constraints
[x] Distinguish direct annotation from new-artwork generation
[x] Add reference-conditioned generation-package compiler
[x] Supply the canonical reference image to the image worker
[x] Add generated-candidate artifact manifests and hashes
[x] Add independent strict visual constraint validator
[x] Add Windows compile / generate / validate exercise
[ ] Run the first live reference-conditioned Raspberry Pi candidate
[ ] Review machine validation evidence and candidate image
[ ] Add repair/rerender loop
[ ] Add post-approval deterministic annotation stage
[ ] Add generalized Workbench request UI
[ ] Apply the generalized mechanism to the book illustration inventory
```

## Acceptance criteria

```text
1. A new request can enter the pipeline without a hardcoded renderer route.
2. Research searches derive from the request and its required features.
3. Every selected source has authority, provenance, role, and usage state.
4. Every required visual feature is supported or explicitly blocked.
5. A reference image is used as generation evidence, not mistaken for final artwork.
6. All delivered visual constraints are compiled into the generation package.
7. The actual reference image is supplied to the generation worker.
8. The image worker produces a new candidate illustration rather than a text-only or source-copy artifact.
9. Generated text and technical labels are prohibited in candidate rasters.
10. Candidate images and provider requests are digest-traceable.
11. An independent worker validates the candidate against the reference and every constraint.
12. Missing or uncertain validation evidence cannot silently pass.
13. Failed candidates are repaired, rerendered, or rejected.
14. Human review remains mandatory.
15. Deterministic labels and publication finishing occur only after candidate approval.
16. The resulting mechanism can be applied to the image inventory for the book.
```
