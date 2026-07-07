# CI Package Install Hardening Decisions

## Status

```text
milestone: CI Package Install Hardening
date: 2026-07-07
baseline: 487 passed
runtime_package_install_workflow: green after hardening
```

This decision record closes the remaining decision items after Runtime package-install verification and narrow workflow hardening.

## Decision 1: CI expansion

```text
decision: keep the focused package-install matrix; do not expand the full test suite into a Python matrix yet
```

The Runtime package-install workflow remains the Python-version matrix gate for installed package behavior across Python 3.10, 3.11, and 3.12.

The standard CI workflow remains the normal full-suite source-tree confidence path.

Rationale:

```text
[x] package-install drift risk is already covered by the focused matrix
[x] full-suite matrix expansion would add runtime cost and noise before a demonstrated need
[x] full-suite matrix can be revisited if package-install failures or Python-version-specific runtime defects appear
```

## Decision 2: Version after alpha.26

```text
decision: the next Runtime-capable package candidate should advance to 1.0.0-alpha.27
```

The current package identity remains `1.0.0-alpha.26` until an explicit version-bump commit is made.

The next package artifact or release-candidate handoff should use `1.0.0-alpha.27` so that the post-alpha.26 CI hardening and distribution decisions are traceable.

Rationale:

```text
[x] alpha.26 already represents the verified Runtime packaging baseline
[x] CI hardening occurred after alpha.26 verification
[x] advancing the next package candidate avoids reusing the same alpha identity for a materially different release-candidate posture
```

## Decision 3: Distribution path

```text
decision: use internal GitHub Actions artifact handoff before any formal package publishing path
```

Runtime distribution should remain internal for now.

The next distribution-oriented milestone should produce downloadable GitHub Actions build artifacts from the package-install or release-candidate workflow.

Formal registry publishing is deferred.

Rationale:

```text
[x] GitHub Actions artifacts fit the current private-repository workflow
[x] artifact handoff supports review before public or registry publishing
[x] formal package publishing should wait until release identity, audience, and support expectations are settled
```

## Resulting milestone state

```text
[x] Runtime release packaging readiness closed
[x] Runtime release-candidate packaging guide added
[x] Runtime package-install workflow added
[x] Confirm package-install workflow passes on GitHub Actions
[x] Add workflow result evidence to closeout notes
[x] Apply narrow package-install workflow hardening
[x] Decide whether to expand CI to full-suite plus package-install matrix
[x] Decide whether version advances after alpha.26
[x] Decide whether distribution stays internal or moves to packaged artifact handoff
```

## Follow-up implementation candidates

```text
1. Add GitHub Actions artifact upload for built wheel and source distribution
2. Add alpha.27 version-bump commit when cutting the next package candidate
3. Add release-candidate artifact handoff notes after the first artifact-producing run
```

## Guardrails

```text
[x] Do not reopen Runtime Milestone 3
[x] Do not reopen closed approval-gate tracks
[x] Keep CI hardening separate from Runtime feature work
[x] Keep artifact handoff internal until publishing decisions are explicit
```