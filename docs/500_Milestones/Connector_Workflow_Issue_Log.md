# Connector Workflow Issue Log

## Why this exists

We continued Runtime Milestone 2 work while separately tracking a GitHub connector blocker that affected some provenance, documentation, issue-comment, and standalone test-file attempts. This file preserves the working context so the blocker does not get lost as runtime work continues.

## Current safe baseline

The branch was green at 355 passing tests before Runtime Milestone 2 closeout documentation was added.

## What appears safe

Small runtime code changes have generally worked. Existing test-file edits have generally worked. Plain documentation files have generally worked. Many small additive runtime files have worked.

## What has been blocked

Large full-file replacements have sometimes been blocked. Schema-like content has been blocked, including a small documentation probe that resembled a schema example. Provenance schema hardening was blocked when attempted through the connector. Some issue comments and some standalone runtime test-file creations have also been blocked.

## Working diagnosis

The blocker appears related to connector safety handling of some payload shapes or replacement patterns. It does not appear to be a repository permission problem, a branch problem, or a problem with the underlying ConstraintOS concepts.

## Current workflow decision

Continue implementation in small green slices. Prefer existing-file edits when creating a new standalone file is blocked. Use a local handoff patch or ZIP only when the connector blocks required source changes that cannot be safely routed through existing files.

## Candidate follow-up approaches

Use local edits for schema-like files, then ask the user to run tests and push. Use smaller additive code files when possible. Keep connector probes documentation-only and avoid schema-shaped examples. Track the blocker as workflow risk, not as a Runtime Milestone 2 completion blocker.
