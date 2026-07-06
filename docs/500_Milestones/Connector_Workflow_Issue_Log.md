# Connector Workflow Issue Log

## Why this exists

We are continuing Runtime Milestone 2 work while separately tracking a GitHub connector blocker that affected provenance hardening attempts. This file preserves the working context so the issue does not get lost as runtime work continues.

## Current safe baseline

The branch was green at 340 passing tests before this note was added.

## What appears safe

Small runtime code changes have worked. Small standalone test files have worked. Plain documentation files have worked. Plain provenance status words in documentation have worked.

## What has been blocked

Large full file replacements have sometimes been blocked. Schema-like content has been blocked, including a small documentation probe that resembled a schema example. Provenance schema hardening was blocked when attempted through the connector.

## Working diagnosis

The blocker appears related to connector safety handling of schema-shaped payloads or large replacement payloads. It does not appear to be a repository permission problem, a branch problem, or a problem with the provenance concept itself.

## Current workflow decision

Continue Runtime implementation in small green slices. Do not attempt connector-side provenance schema rewrites until we either use a different workflow or find a safe minimal patch strategy.

## Candidate follow-up approaches

Use local edits for schema-like files, then ask the user to run tests and push. Use smaller additive code files when possible. Keep any connector probes documentation-only and avoid schema-shaped examples.
