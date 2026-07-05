# Phase 26: Repository Auditor

Status: Stage 1 Complete
Version: 1.0.0-alpha.26

## Purpose
Phase 26 starts the repository stabilization sprint by adding a repeatable repository auditor. Instead of producing a one-time manual audit, ConstraintOS can now inspect a repository and generate structured health, coverage, debt, and beta-readiness reports.

## Implemented Scope

- Repository auditor module
- Repository audit aggregate model
- Schema coverage report
- Artifact coverage report
- Technical debt report
- Beta readiness report
- Markdown audit renderer
- Repository audit schema
- Repository auditor tests
- `constraintos repo-audit` CLI command
- YAML, JSON, and Markdown audit output
- Package version bumped to `1.0.0-alpha.26`

## Audit Families

- inventory
- schema coverage
- artifact coverage
- technical debt
- beta readiness

## CLI Usage

```bash
constraintos repo-audit --repo-root . --format yaml --output reports/repository_audit.yaml
constraintos repo-audit --repo-root . --format json --output reports/repository_audit.json
constraintos repo-audit --repo-root . --format markdown --output reports/repository_audit.md
```

## Design Rules

1. Repository audits must be generated from actual repository files.
2. The auditor must be reusable in CI.
3. Audit output must be machine-readable and human-readable.
4. Beta readiness must be derived from audit evidence.
5. The auditor must not hide blockers.

## Recommended Next Stage

Run the auditor in CI or a local clone, review the generated blockers, and use its output to drive the rest of Phase 26 stabilization.
