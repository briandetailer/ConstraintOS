# Phase 10: Renderer Plugin Execution Boundaries and Artifact Output Storage

Status: Complete Baseline
Version: 1.0.0-alpha.10

## Purpose
Phase 10 introduces render job and output-reference concepts without enabling live renderer execution. This establishes the boundary between the ConstraintOS kernel and future renderer plugin runtimes.

## Implemented Scope

- Render job model
- Output reference model
- Dry-run render job execution
- Artifact manifest output update helper
- Render job JSON Schema
- Output reference JSON Schema
- Renderer registry JSON Schema
- Render job tests
- Example render job
- Example output reference
- Example renderer registry
- Package version bumped to `1.0.0-alpha.10`

## Renderer Execution Philosophy

Renderers remain execution backends. They receive compiled instructions and produce output references. They do not own validation, approval, state transitions, or source specifications.

## Output Reference Philosophy

ConstraintOS should track outputs by reference rather than embedding binary assets directly in kernel records. This allows storage to be local, cloud-based, repository-backed, or object-store-backed without changing compiler or validator behavior.

## Design Rules

1. Render jobs must be explicit objects.
2. Renderer execution must return structured responses.
3. Output references must include artifact ID, renderer, URI, media type, and metadata.
4. Dry-run execution must remain available for tests.
5. Live renderer calls remain deferred.
6. Artifact manifests may link outputs without owning storage implementation details.
7. Renderer registries describe available plugins without executing them.

## Recommended Phase 11
Phase 11 should introduce storage backend abstraction and artifact repository management:

1. Storage backend protocol
2. Local filesystem storage adapter
3. Object reference schema
4. Artifact repository layout
5. Output persistence tests
6. Storage-independent manifest updates
