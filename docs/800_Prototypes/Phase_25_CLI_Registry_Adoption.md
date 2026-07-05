# Phase 25: CLI Registry Adoption

Status: Complete Baseline
Version: 1.0.0-alpha.25

## Purpose
Phase 25 wires the central schema registry into the CLI. The CLI now uses the shared registry for schema detection, record extraction support, registry diagnostics, and registry reporting.

## Implemented Scope

- CLI imports the central schema registry.
- CLI `detect_schema` delegates to registry-backed lookup.
- CLI record extraction uses registered artifact keys before special rules.
- CLI schema exemption list derives from registered keys.
- Added `constraintos registry-report` command.
- Added `constraintos registry-check` command.
- Added CLI registry adoption tests.
- Package version bumped to `1.0.0-alpha.25`.

## Design Rules

1. CLI schema lookup must come from the central registry.
2. Registered artifact families should not need duplicated CLI schema tables.
3. Special rule handling remains explicit for legacy shapes and compound detections.
4. Registry diagnostics must be available through CLI commands.
5. Full repository validation remains a stabilization concern.

## Deferred

- Complete removal of all legacy special-case record extraction branches.
- Full example validation audit from the connector environment.
- Duplicate ID audit command.

## Recommended Phase 26

Phase 26 should become a repository stabilization sprint:

1. Run full example validation.
2. Audit duplicate IDs.
3. Check every schema reference.
4. Generate complete registry report.
5. Produce architecture book draft.
6. Prepare beta release candidate plan.
