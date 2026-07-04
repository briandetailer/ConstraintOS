# Phase 5: Renderer Adapter Contracts

Status: Complete Baseline
Version: 0.5

## Purpose
Phase 5 defines the boundary between ConstraintOS and future rendering engines. The goal is to prevent renderer-specific behavior from leaking into the constraint model, compiler, validation system, or repository structure.

## Implemented Scope

- Renderer adapter protocol
- Renderer profile dataclass
- Render request dataclass
- Render response dataclass
- Dry-run renderer adapter
- Renderer profile JSON Schema
- Compiler result JSON Schema
- Dry-run renderer profile fixture
- Adapter contract tests
- Package version bumped to 0.5.0

## Design Rules

1. Renderers are execution backends, not sources of truth.
2. Renderer adapters must receive compiled instructions, not full project history.
3. Renderer adapters must not validate their own outputs.
4. Renderer adapters must not mutate CSL specifications.
5. Unsupported renderer capabilities must be exposed through renderer profiles.
6. Live renderer calls remain deferred until the adapter boundary is stable.

## Adapter Objects

### RendererProfile
Declares renderer capabilities.

### RenderRequest
Contains renderer name, artifact ID, compiled instruction, and metadata.

### RenderResponse
Contains renderer status, output reference, messages, and metadata.

### RendererAdapter
Protocol for future live renderer integrations.

## Dry-Run Renderer
The dry-run renderer exists only to test system boundaries. It returns a structured response without calling any external service.

## Recommended Phase 6
Phase 6 should introduce patch instruction packages and regression baselines:

1. Patch package schema
2. Patch compiler target
3. Regression baseline schema
4. Compare approved vs revised artifact metadata
5. Patch workflow tests
6. Still no live renderer calls
