# Beta 1 Technical Debt Register

Status: Initial Baseline
Milestone: Beta 1

## Purpose
This register tracks known technical debt that must be resolved before ConstraintOS can be considered a stable beta product.

## Debt Items

### TD-001: Legacy CLI Special-Case Detection

- **Area:** CLI / Validation
- **Severity:** High
- **Description:** The CLI now uses the central schema registry for schema detection, but some special-case record extraction branches remain.
- **Impact:** Future artifact families may still require CLI edits if the registry is not made fully authoritative.
- **Resolution:** Complete registry-backed record extraction and remove unnecessary legacy branches.

### TD-002: Repository-Wide Validation Not Proven Green

- **Area:** CI / Validation
- **Severity:** High
- **Description:** The repository has grown rapidly and full validation across all examples has not been confirmed after recent runtime and documentation additions.
- **Impact:** CI may fail when validation is manually run or when changes merge to protected branches.
- **Resolution:** Run controlled validation, record failures, and fix examples or schemas.

### TD-003: Duplicate ID Audit Not Dedicated

- **Area:** Artifact Integrity
- **Severity:** Medium
- **Description:** Duplicate ID detection exists as part of validation behavior, but there is no dedicated audit command or report artifact.
- **Impact:** Duplicate IDs may be harder to diagnose as artifact families grow.
- **Resolution:** Add dedicated `constraintos id-audit` command and structured report.

### TD-004: Documentation Fragmentation

- **Area:** Documentation
- **Severity:** Medium
- **Description:** Much of the architecture exists as phase-specific documentation rather than consolidated manuals.
- **Impact:** New users and contributors may struggle to understand the system coherently.
- **Resolution:** Create Architecture Book, Developer Guide, User Guide, CLI Manual, and Schema Reference.

### TD-005: Renderer Orchestration Not Yet Implemented

- **Area:** Product Capability
- **Severity:** High
- **Description:** Renderer orchestration is central to the product vision but remains planned rather than implemented.
- **Impact:** ConstraintOS cannot yet demonstrate its core production value proposition end-to-end.
- **Resolution:** Target Beta 2 for Blender/SVG/vector workflow orchestration.

### TD-006: Durable Runtime Services Deferred

- **Area:** Runtime
- **Severity:** Medium
- **Description:** Queue, storage, workers, leases, and observability are local/in-memory scaffolds.
- **Impact:** Not production-ready for long-running or hosted workloads.
- **Resolution:** Introduce durable backend adapters after beta stabilization.

### TD-007: Workflow Notifications Managed by Reduced Trigger Scope

- **Area:** CI
- **Severity:** Low
- **Description:** Working-branch push validation was disabled to stop notification flooding.
- **Impact:** Working branch requires manual validation discipline.
- **Resolution:** Restore stricter checks once validation is green and notification strategy is controlled.

## Beta 1 Exit Criteria

- TD-001 through TD-004 must be resolved or reduced to low severity.
- TD-005 and TD-006 may remain deferred if clearly documented for Beta 2 and later.
- CI must have a controlled green baseline.
