# ADR-0002: Kernel and Platform Separation

Status: Accepted
Date: 2026-07-04

## Context
ConstraintOS is evolving from a documentation and CLI project into a broader platform architecture. Future capabilities may include hosted SaaS access, users, subscriptions, billing, encryption, tokenization, organizations, and enterprise controls.

These concerns are important, but they are not part of the deterministic core engine.

## Decision
ConstraintOS shall maintain a strict separation between the kernel and platform layers.

The kernel owns deterministic orchestration, specifications, compilation, validation, traceability, patching, regression baselines, and lifecycle rules.

The platform layer owns users, organizations, billing, subscriptions, authentication, cloud tenancy, hosted infrastructure, and commercial operations.

## Rationale
Keeping the kernel separate allows ConstraintOS to run locally, on a private server, in an enterprise environment, or behind a future SaaS platform without changing the core engine.

## Consequences

- The kernel remains deployable without SaaS dependencies.
- Commercial features can be added later without contaminating core architecture.
- The hosted platform can evolve independently.
- Enterprise and local deployments remain possible.
- SaaS user management and billing are banked for a future program.

## Related Documents

- ConstraintOS v1.0 Architecture Freeze
- ADR-0001 Constraint-First Platform
