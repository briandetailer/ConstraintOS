# ADR-0003: Production Runtime Outside the Kernel

Status: Accepted
Date: 2026-07-04

## Context
ConstraintOS now has kernel components for specifications, compilation, validation, patching, lifecycle, review, rendering boundaries, storage references, and deterministic atlas builds.

A production deployment will eventually need an API server, job queue, worker pool, storage services, observability, metrics, authentication, and possibly hosted SaaS infrastructure.

## Decision
The production runtime shall be treated as a layer outside the ConstraintOS kernel.

The runtime may call kernel functions, schedule jobs, coordinate workers, and persist artifacts, but it must not become the source of truth for constraints, validation semantics, approval rules, or artifact correctness.

## Rationale
Keeping runtime concerns outside the kernel preserves local execution, enterprise deployment, and future SaaS deployment without changing core engine behavior.

## Consequences

- The kernel remains deterministic and deployable without an API server.
- Runtime jobs are orchestration records, not authoritative specifications.
- Workers execute tasks through kernel contracts.
- Auth, tenancy, and billing remain future platform concerns.
- Metrics and observability report behavior but do not decide correctness.

## Related Documents

- ConstraintOS v1.0 Architecture Freeze
- ADR-0002 Kernel and Platform Separation
