# Phase 13: Production Runtime Planning and API / Job-Worker Architecture

Status: Complete Baseline
Version: 1.0.0-alpha.13

## Purpose
Phase 13 introduces production runtime planning while preserving the architecture freeze: the runtime coordinates kernel execution but does not become part of the deterministic kernel.

## Implemented Scope

- Runtime planning module
- Runtime job model
- Worker profile model
- Runtime configuration model
- Metric event model
- Runtime config JSON Schema
- Runtime job JSON Schema
- Worker profile JSON Schema
- Metric event JSON Schema
- Runtime tests
- Runtime examples
- ADR-0003: Production Runtime Outside the Kernel

## Runtime Philosophy

The runtime schedules and coordinates work. The kernel defines correctness.

## Runtime Layer Responsibilities

- API boundary
- job queue
- worker coordination
- runtime configuration
- metrics and observability
- operational status
- deployment-specific scheduling

## Kernel Responsibilities Retained

- CSL semantics
- compiler behavior
- validation rules
- compliance reports
- review gate semantics
- patch generation
- lifecycle rules
- approval semantics

## Design Rules

1. Runtime may call kernel functions.
2. Runtime may schedule and coordinate workers.
3. Runtime may emit metrics.
4. Runtime must not own correctness semantics.
5. Runtime must not own auth, billing, tenancy, or subscriptions.
6. Runtime must remain deployable locally before SaaS concerns are added.

## Recommended Phase 14

Phase 14 should introduce API contract planning:

1. API route specification
2. Request and response schemas
3. Kernel service boundary
4. Dry-run endpoint examples
5. Error response model
6. OpenAPI draft
