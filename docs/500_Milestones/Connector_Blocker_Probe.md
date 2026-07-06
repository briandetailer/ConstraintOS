# Connector Blocker Probe

## Current observations

Accepted writes:

- Runtime scheduler update.
- Runtime scheduler tests update.
- Runtime execution model update.
- Runtime execution export update.
- Small standalone execution request builder test file.
- Documentation-only files.

Blocked writes:

- Full replacement of validation CLI file.
- Full replacement of provenance manifest schema.
- New provenance runtime checker modules.
- Rejected provenance YAML example.
- Full replacement of execution test file.

## Working hypothesis

The blocker appears sensitive to some combination of large replacement payloads, validation/schema/security-adjacent terminology, and possibly provenance status examples. It is not a simple branch permission issue and not a blanket block on code, tests, docs, or runtime changes.

## Safer pattern

Prefer smaller additive files and narrow updates. Avoid full-file rewrites when a small file or focused update can carry the same behavior.
