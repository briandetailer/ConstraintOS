# Phase 6: Patch Packages and Regression Baselines

Status: Complete Baseline
Version: 0.6

## Purpose
Phase 6 introduces targeted correction and regression-protection concepts. The system can now produce patch packages from compliance reports and establish regression baselines for approved artifacts.

## Implemented Scope

- Patch package model
- Failed constraint model
- Patch instruction generation
- Regression baseline generation
- Patch package JSON Schema
- Regression baseline JSON Schema
- CLI `new-patch` command
- CLI `new-baseline` command
- Patch and regression tests
- Package version bumped to 0.6.0

## Patch Philosophy

Patch packages must correct failed or uncertain constraints without disturbing passing constraints. This is a direct response to whole-output regeneration drift.

## Regression Philosophy

Approved artifacts become baselines. Later revisions must be compared against approved constraints to prevent regressions.

## Design Rules

1. Patch instructions must list only failed, uncertain, or evidence-blocked constraints.
2. Patch instructions must explicitly preserve passing constraints.
3. Regression baselines must record approved constraints.
4. Blocker and major regressions are not allowed by default.
5. Patch packages are renderer-independent.
6. Live renderer calls remain deferred.

## CLI Usage

```bash
constraintos new-patch PATCH-0001 examples/compliance/VAL-0001.yaml --output patches/PATCH-0001.yaml
```

```bash
constraintos new-baseline PLATE-0001 0.1 VAL-0001 --constraints C-0001,C-0002 --output baselines/PLATE-0001_0.1.yaml
```

## Recommended Phase 7

Phase 7 should introduce artifact storage and lifecycle management:

1. Artifact manifest schema
2. Output reference model
3. Artifact state transitions
4. Approval record schema
5. Archive policy
6. Lifecycle CLI commands
