# Runtime Release Notes Draft: 1.0.0-alpha.26

## Status

Draft release notes for the Runtime-capable alpha release candidate.

This document prepares release communication only. It does not change the package version, publish a package, tag a release, or reopen closed Runtime milestone tracks.

## Release identity

```text
package: constraintos
version: 1.0.0-alpha.26
track: Runtime-capable alpha release candidate
confirmed baseline: 487 passed
```

## Highlights

- Runtime package discovery now includes the `runtime` package tree and excludes Runtime tests from packaged discovery.
- Runtime-facing console scripts are registered for execution, evidence generation, and approval report generation.
- Runtime CLI dependencies are declared in package metadata.
- Runtime evidence and approval help behavior has executable coverage.
- Installed Runtime command help has executable coverage.
- Installed Runtime evidence and approval workflows have executable coverage from sample inputs.
- Source-tree Runtime module parity is covered for help, evidence dispatch, approval dispatch, missing command errors, and unknown command errors.
- Runtime evidence and approval artifact paths are covered and documented.
- Runtime release/packaging readiness checklist is fully closed.
- Runtime package install validation workflow has been added for release-candidate package smoke checks.

## Runtime commands

```text
cos-runtime
cos-runtime-evidence
cos-runtime-approval
```

## Validation summary

User-confirmed full-suite baseline after Runtime Release / Packaging Readiness closeout:

```text
487 passed
```

Additional package-install validation is defined in:

```text
.github/workflows/runtime-package-install.yml
```

## Release candidate checklist

```text
[x] Runtime Release / Packaging Readiness closed
[x] Release candidate packaging guide added
[x] Package install validation workflow added
[x] Release notes draft added
[ ] CI package install validation has run successfully
[ ] Release tag decision made
[ ] Distribution/publishing decision made
```

## Closed tracks preserved

```text
Runtime Milestone 3
Post-Milestone 3 Approval Gates
Approval CLI follow-up
Approval policy examples
Approval policy enforcement
Approval workflow guide
```

## Notes for final release publication

Before publishing or tagging, confirm whether `1.0.0-alpha.26` is the intended release-candidate identifier or whether the version should be advanced to a new alpha number.
