# Universal Image Job Product

## Status

```text
milestone: Universal Image Job Product
status: active
started_on: 2026-07-20
branch: phase-1-cli-tooling
current_checkpoint: persistent image-job service, CLI, API, and local web UI implemented
next_checkpoint: automatic dynamic reference packaging for newly discovered sources
```

## Product statement

ConstraintOS is a persistent request-to-publication system for creating source-backed technical imagery from user constraints.

The product is not a collection of scenario scripts. A Toyota engine, NASA rover, Raspberry Pi board, or a subject never previously discussed must enter through the same Image Job contract.

## Image Job lifecycle

```text
job accepted
        ↓
constraint compilation
        ↓
clarification when materially necessary
        ↓
request-derived research planning
        ↓
live authoritative source discovery
        ↓
source evaluation and render-strategy selection
        ↓
dynamic reference preparation
        ↓
reference-conditioned generation or verified-geometry rendering
        ↓
independent constraint validation
        ↓
bounded validator-directed repair
        ↓
human review
        ↓
deterministic annotation and publication finishing
```

Every job owns a durable workspace containing:

```text
job.json
submitted-request.json
request.json
research-plan.json
discovered-sources.json
orchestration.json
events.jsonl
reference package and derived images
generation package and candidates
validation evidence
repair lineage
publication artifacts
```

## Implemented product surfaces

### Local web application

```text
runtime.product.api:app
```

The initial browser interface supports:

```text
- paste a new natural-language image request
- create a persistent job
- optionally launch live research immediately
- list recent jobs
- inspect job state, blockers, artifacts, and events
- resume research-ready jobs
```

The API exposes:

```text
GET  /health
GET  /api/jobs
POST /api/jobs
GET  /api/jobs/{job_id}
POST /api/jobs/{job_id}/research
POST /api/jobs/{job_id}/clarification
GET  /api/jobs/{job_id}/artifacts/{artifact_key}
```

The Windows launcher is:

```powershell
.\scripts\start-constraintos-product.ps1
```

It loads the DPAPI-protected OpenAI credential, creates the persistent job root, opens the browser, and starts the local Uvicorn server.

### Product CLI

```text
cos-image-job
```

Commands:

```text
cos-image-job create
cos-image-job show
cos-image-job list
cos-image-job research
cos-image-job resume
```

Natural-language example:

```powershell
cos-image-job create `
  --request "Create a cutaway technical illustration of a diaphragm vacuum pump showing the diaphragm, connecting rod, eccentric drive, inlet valve, and outlet valve." `
  --run-research
```

Structured applications may submit exact subject, viewpoint, features, visual constraints, prohibitions, and review policy without using the intake model.

## Persistent job store

`FileJobStore` provides:

```text
- collision-resistant job IDs
- atomic job and artifact writes
- append-only JSONL event history
- durable artifact indexing
- job listing and retrieval
- workspace-bound artifact access
```

Jobs never gain production approval from intake, research, generation, validation, or repair workers. Approval remains a distinct human decision.

## Constraint intake

Natural-language requests are compiled through a strict structured-output contract.

The compiler extracts:

```text
- subject
- output kind
- viewpoint
- required visible features
- forbidden features
- illustration style
- composition
- palette
- background
- surface treatment
- label strategy
- output size and quality
- repeatability and authority requirements
- novel-view requirement
- assumptions
- unresolved questions
```

It does not perform web research during intake and may not invent factual components absent from the request. Publication-safe defaults are recorded as assumptions. Material ambiguities become durable clarification blockers.

## Research handoff

A research-ready job uses the generalized `ResearchToRenderOrchestrator` and live `OpenAIWebDiscoveryProvider`.

Outputs include:

```text
- request-derived search plan
- structured discovered source records
- feature-coverage evaluation
- rejected source reasons
- selected canonical and annotation sources
- selected production mode
- preflight blockers and validation gates
```

Supported strategy outcomes remain:

```text
reference_conditioned_generation
geometry_render
source_plate_annotation
reference_bundle_only
```

The product does not require a pre-registered scenario to reach research and strategy selection.

## Current boundary

A completely new subject now reaches:

```text
request intake
→ normalized constraints
→ persistent job
→ live research
→ evidence evaluation
→ production-mode selection
```

The remaining hard boundary is automatic conversion of newly discovered sources into a generation-ready reference package.

Current research-complete jobs therefore enter:

```text
status: reference_preparation_required
stage: reference_preparation
```

This is deliberate and visible. The product may not silently reuse a web page, select an arbitrary PDF raster, or claim unsupported geometry.

## Next implementation slice: Dynamic Reference Packaging

The next checkpoint must support:

```text
1. Download canonical image, PDF, and geometry sources into the job workspace.
2. Record HTTP metadata, hashes, source role, and usage-review state.
3. Preserve reference-only web pages without treating access failures as fatal.
4. Extract candidate rasters from PDFs and webpages.
5. Select the controlling visual reference against the request and source evidence.
6. Produce contact sheets or review artifacts when selection is uncertain.
7. Normalize ordinary PNG, JPEG, and WebP sources.
8. Route STEP, GLB, and other geometry to a geometry-preparation worker.
9. Produce a generic derived-reference manifest consumable by candidate generation.
10. Advance the Image Job automatically to generation-ready or fail closed with explicit blockers.
```

After that slice, the existing candidate generation, validation, and repair workers will be attached to the Image Job service and API.

## Implemented files

```text
runtime/product/__init__.py
runtime/product/models.py
runtime/product/store.py
runtime/product/intake.py
runtime/product/service.py
runtime/product/cli.py
runtime/product/api.py

scripts/start-constraintos-product.ps1

tests/test_product_image_jobs.py
tests/test_product_constraint_intake.py
```

## Acceptance criteria for this checkpoint

```text
1. A subject never previously registered can create a persistent job.
2. Natural-language and structured requests use the same normalized contract.
3. Job state survives process restarts.
4. Every stage emits durable events and artifacts.
5. Live research is request-driven, not scenario-driven.
6. Evidence gaps and clarification needs remain visible blockers.
7. Render strategy derives from constraints and source classes.
8. The local product can be launched without manually exporting an API key.
9. The browser and CLI operate over the same job store and service.
10. Production approval remains false throughout automated stages.
```
