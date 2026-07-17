# Research-to-Render Source Materialization Correction

## Status

```text
milestone: Research-to-Render Orchestration
correction: distinguish required, optional, and reference-only sources
status: implemented
observed_on: 2026-07-17
branch: phase-1-cli-tooling
```

## Trigger

The Raspberry Pi 5 source-package preparation run successfully reached the downloadable official assets but failed when the official Raspberry Pi hardware-documentation HTML page returned HTTP 403 to PowerShell `Invoke-WebRequest`.

The failed page was supporting terminology and component evidence. It was not the canonical visual source, selected rendering base, or required downloadable product brief.

## Root cause

The original materializer treated every source marked for ingestion as a mandatory binary download. It did not distinguish:

```text
- canonical source files required by the selected render mode
- optional fallback or dimensional sources
- authoritative web references that should remain URL-backed
```

As a result, one anti-automation response from a supporting HTML page blocked an otherwise valid package.

## Corrected source roles

```text
required
- failure blocks source-package preflight
- file must be present and SHA-256 recorded

optional
- materialization is attempted
- failure is recorded as a warning
- failure does not block the selected rendering mode

reference_only
- URL, authority, purpose, and usage-review state are recorded
- no automated download is attempted
- source remains available for evidence and terminology review
```

For the Raspberry Pi 5 locked top-view request:

```text
required
- official top-view source-plate PDF
- official product brief PDF

optional
- official STEP geometry fallback
- official mechanical drawing

reference_only
- official Raspberry Pi hardware-documentation HTML page
```

This matches the least-complex sufficient rendering rule. A locked top-view source-plate request must not be blocked because an unused geometry fallback or supporting web page could not be downloaded.

## Manifest changes

`source-package-manifest.json` version `1.2.0` now records:

```text
required_source_count
required_materialized_count
materialized_sources
referenced_sources
failure_count
failures
warning_count
warnings
preflight_status
```

Only missing or failed `required` sources can force `preflight_status: blocked`.

## Guardrails

```text
[x] Preserve the hardware-documentation URL and evidence role
[x] Do not retry or bypass a website's access control
[x] Do not discard source provenance because a page is not downloadable
[x] Keep canonical source digest verification mandatory
[x] Keep optional-source failures visible as warnings
[x] Keep production_ready false until downstream registry, render, and usage gates pass
```
