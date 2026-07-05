# Technical Debt Register

Status: Active
Version: 1.0.0-alpha.26

## Purpose
This register records known cleanup work that does not block the beta candidate. It turns scanner findings into intentional engineering decisions.

## Current Audit Result

The repository auditor reports beta readiness as `ready` while marking technical debt as `review`.

Current review items:

- code-note files: 1
- scaffold-marker files: 10

These items are not beta blockers because schema coverage and artifact coverage both pass.

## Decisions

| Category | Count | Status | Decision | Target |
|---|---:|---|---|---|
| Code-note files | 1 | Accepted for beta | Review during Runtime milestone setup | Runtime Milestone |
| Scaffold-marker files | 10 | Accepted for beta | Keep as explicit boundaries for future runtime/platform work | Runtime and Platform Milestones |

## Release Policy

For `v1.0.0-beta.1`, technical debt is acceptable when all of the following are true:

1. Repository audit status is `ready`.
2. Schema coverage is `pass`.
3. Artifact coverage is `pass`.
4. Duplicate ID count is zero.
5. Invalid YAML count is zero.
6. Remaining cleanup items are recorded here.

## Follow-up Policy

Before `v1.0.0`, each item in this register should be either:

- implemented,
- converted into a GitHub issue,
- assigned to a named milestone, or
- removed because it is no longer relevant.

## Rationale

The remaining cleanup items are concentrated around future execution boundaries and productization work. Those areas are intentionally deferred until the Runtime and Platform milestones so the beta candidate can preserve a clean kernel/runtime separation.
