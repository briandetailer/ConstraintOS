# ConstraintOS Engineering Standards Manual

Status: Draft
Milestone: Beta 1

## Purpose
This manual defines the engineering rules for ConstraintOS. It exists to keep the project coherent as it grows from a prototype into a product.

## Prime Directive
ConstraintOS does not generate content. It governs production.

LLMs may generate. Renderers may render. Validators may inspect. Humans may approve. ConstraintOS orchestrates, constrains, validates, records, and reproduces the workflow.

## Repository Standards

### Naming

- Artifact IDs must be stable and unique.
- Schema files must use lowercase kebab-case names.
- Python modules must use lowercase snake_case names.
- Phase documents must include status and version when applicable.

### Schema Standards

- Every artifact family must have a JSON Schema unless explicitly documented as legacy or temporary.
- Every schema-backed artifact family must be registered in the schema registry.
- Schemas define structure, not business strategy.

### Validation Standards

- Validation must be deterministic.
- Validation must not depend on live model output.
- Validators should report structured failures.
- Human approval is a separate gate from automated validation.

### Testing Standards

- Every new module should have tests.
- Tests should avoid external services unless explicitly marked integration-only.
- Runtime scaffolds should remain local and deterministic in Beta 1.

### Documentation Standards

- Every major subsystem needs a specification document.
- Deferred work must be captured in the Deferred Work Register.
- Technical debt must be captured in the Technical Debt Register.
- Architecture changes must update the Architecture Book or Product Charter when they alter system philosophy.

### Runtime Standards

- Local runtime may use in-memory scaffolds.
- Production runtime must use durable, observable services.
- Runtime orchestration must not redefine kernel correctness.

### Plugin Standards

- Plugins must declare capabilities.
- Plugins must declare unsupported constraints.
- Plugins must not silently ignore blocker constraints.
- Plugin output must be traceable to input specifications.

## Release Standards

A beta release requires:

- Green CI baseline.
- Installation instructions.
- Quickstart path.
- Known issues list.
- Release notes.
- Documented deferred work.

## Governance

Future contributions should be evaluated against the Vision & Product Charter, Architecture Book, and this Engineering Standards Manual.
