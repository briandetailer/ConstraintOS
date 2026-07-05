# Beta 1 Deferred Work Register

Status: Initial Baseline
Milestone: Beta 1

## Purpose
This register captures deferred work that is intentionally not required for the first stabilized beta, but must remain visible so it does not disappear into undocumented technical debt.

## Deferred Work

### DW-001: Full Renderer Orchestration

- **Target:** Beta 2
- **Description:** Implement deterministic orchestration of external renderers such as Blender, SVG/vector tooling, and publication tools.
- **Reason Deferred:** Requires stable kernel, registry, validation, and artifact lifecycle first.

### DW-002: Hosted SaaS Platform

- **Target:** Release Candidate / 1.0
- **Description:** Add users, organizations, subscriptions, billing, tenant isolation, encryption, and hosted UI.
- **Reason Deferred:** Commercial platform concerns should not contaminate the kernel or local runtime design.

### DW-003: Durable Queue Backend

- **Target:** Post-Beta 1 Runtime Hardening
- **Description:** Replace or augment in-memory queue with durable broker/database adapters.
- **Reason Deferred:** In-memory scaffolding is sufficient for local beta validation.

### DW-004: Cloud Object Storage Adapter

- **Target:** Post-Beta 1 Runtime Hardening
- **Description:** Add object storage support for artifacts and build outputs.
- **Reason Deferred:** Local storage abstraction already exists; cloud storage requires deployment assumptions.

### DW-005: Plugin SDK

- **Target:** Beta 2 or Beta 3
- **Description:** Define a plugin development model for renderers, validators, and external tools.
- **Reason Deferred:** Plugin contracts should follow the first real renderer orchestration implementation.

### DW-006: Multi-LLM Provider Abstraction

- **Target:** Beta 3
- **Description:** Define model-provider abstraction for OpenAI, Anthropic, local models, and future providers.
- **Reason Deferred:** The current priority is deterministic orchestration and validation, not provider diversity.

### DW-007: Production Authentication and Authorization

- **Target:** Release Candidate
- **Description:** Add identity, roles, permissions, organization boundaries, and secure API access.
- **Reason Deferred:** Auth belongs to the future platform layer, not the kernel.

### DW-008: Runtime Dashboard

- **Target:** Post-Beta 1 Runtime UX
- **Description:** Visualize queue status, workers, failures, leases, and runtime health.
- **Reason Deferred:** Observability reports exist; UI/dashboard can follow stable runtime semantics.

## Rule
Deferred work must remain visible in this register and should be promoted into active roadmap items only when the prerequisite architectural layer is stable.
