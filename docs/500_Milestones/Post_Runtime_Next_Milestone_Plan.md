# Post Runtime Packaging Next Milestone Plan

## Status

Runtime Release / Packaging Readiness is complete with a user-confirmed baseline of:

```text
487 passed
```

Runtime package-install GitHub Actions verification is confirmed successful for release-candidate head SHA `861fd25386d8d1845bbf33195ca4247f64f6007a`.

This plan starts after the Runtime release packaging closeout and does not reopen Runtime Milestone 3 or closed Runtime approval-gate tracks.

## Recommended next milestone

```text
Milestone: CI Package Install Hardening
```

## Why this is next

The Runtime package is ready enough for release-candidate packaging checks, but the next risk is environment drift between source-tree tests and installed package behavior.

The package-install validation workflow has been added, run successfully on GitHub Actions, and recorded in the Runtime release packaging closeout notes. CI Package Install Hardening can now continue with CI expansion, version, and distribution decisions without reopening closed Runtime feature tracks.

## Milestone goals

```text
[x] Runtime release packaging readiness closed
[x] Runtime release-candidate packaging guide added
[x] Runtime package-install workflow added
[x] Confirm package-install workflow passes on GitHub Actions
[x] Add workflow result evidence to closeout notes
[ ] Apply narrow package-install workflow hardening
[ ] Decide whether to expand CI to full-suite plus package-install matrix
[ ] Decide whether version advances after alpha.26
[ ] Decide whether distribution stays internal or moves to packaged artifact handoff
```

## Workflow result evidence

```text
workflow: runtime-package-install.yml
run_url: https://github.com/briandetailer/ConstraintOS/actions/runs/28882053354
status: completed
conclusion: success
head_sha: 861fd25386d8d1845bbf33195ca4247f64f6007a
reported_by: gh run view
reported_on: 2026-07-07
```

## Suggested slices

### Slice 1: CI workflow verification

Completed. Runtime package-install verification passed on GitHub Actions and result evidence was recorded.

### Slice 2: Narrow package-install workflow hardening

Recommended next hardening changes:

```text
[ ] Remove stale dist/ before package build
[ ] Run python -m pip check after wheel installation
[ ] Run installed CLI command smoke checks from a temporary directory outside the repository tree
```

Rationale: these checks reduce the chance that a workflow accidentally passes because of stale build outputs or source-tree import shadowing.

### Slice 3: CI expansion decision

Decide whether to keep package-install validation as a focused workflow or expand CI coverage into a full-suite plus package-install matrix.

### Slice 4: Version decision

Decide whether the next package identifier remains `1.0.0-alpha.26` or advances to a new alpha number.

### Slice 5: Distribution decision

Decide whether to use local wheel artifacts, GitHub Actions artifacts, or a formal package publishing path.

### Slice 6: Next functional milestone selection

After package-install hardening is stable, select the next functional milestone.

## Candidate functional milestones after CI hardening

```text
1. Runtime CI/CD integration examples
2. Runtime package artifact handoff workflow
3. Constraint pack execution integration
4. Runtime observability handoff cleanup
5. CLI usability polish for Runtime operators
```

## Guardrails

```text
[x] Do not reopen Runtime Milestone 3
[x] Do not reopen closed approval-gate tracks
[x] Do not claim local tests passed unless actually run
[x] Keep user-confirmed baseline explicit
[x] Keep release/distribution decisions separate from readiness evidence
[x] Keep CI hardening separate from Runtime feature work
```