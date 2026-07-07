# Runtime Release Candidate Packaging

## Purpose

This guide defines the release-candidate packaging flow for Runtime-capable ConstraintOS builds.

It starts after Runtime Release / Packaging Readiness has been closed and keeps Runtime Milestone 3 and the closed Runtime approval-gate tracks closed.

## Current release candidate identity

```text
package: constraintos
version: 1.0.0-alpha.26
track: Runtime-capable alpha release candidate
```

## Preconditions

```text
[x] Runtime Release / Packaging Readiness is complete
[x] Full-suite baseline is user-confirmed at 487 passed
[x] Runtime console scripts are registered
[x] Runtime package discovery includes runtime*
[x] Runtime tests are excluded from package discovery
[x] Runtime dependencies are declared
```

## Build commands

Run from the repository root:

```powershell
python -m pip install --upgrade pip build
Remove-Item -Recurse -Force .\dist -ErrorAction SilentlyContinue
python -m build
```

Expected outputs:

```text
dist/constraintos-1.0.0a26.tar.gz
dist/constraintos-1.0.0a26-py3-none-any.whl
```

## Local install smoke check

Install the built wheel into a clean virtual environment, then run:

```powershell
cos-runtime --help
cos-runtime-evidence --help
cos-runtime-approval --help
```

Then generate Runtime evidence and approval artifacts from sample inputs:

```powershell
cos-runtime-evidence --spec path/to/spec.json --workers path/to/workers.json --output-dir artifacts/runtime-evidence --format json
cos-runtime-approval --evidence-manifest artifacts/runtime-evidence/evidence/RUNTIME-0001.json --evidence-artifact-id ARTIFACT-0004 --policy path/to/policy.json --decided-by policy-owner --decided-at 2026-07-06T00:00:00Z --output-dir artifacts/runtime-approval --format json
```

## Release candidate decision rule

A Runtime release candidate is package-ready when:

```text
[x] python -m build completes
[x] wheel installation succeeds in a clean environment
[x] cos-runtime --help exits successfully
[x] cos-runtime-evidence --help exits successfully
[x] cos-runtime-approval --help exits successfully
[x] cos-runtime-evidence generates evidence artifacts
[x] cos-runtime-approval generates an approval report
[x] full-suite baseline remains 487 passed or is explicitly updated with an explained delta
```

## Non-goals

This guide does not publish a package, create a GitHub release, tag a commit, or reopen closed Runtime milestone tracks.
