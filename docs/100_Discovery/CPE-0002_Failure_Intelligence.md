# CPE-0002 Failure Intelligence

Status: Draft
Version: 0.1

## Purpose
Failure Intelligence is the requirements database for ConstraintOS. Every major feature should trace to one or more observed or anticipated failure modes.

## Failure Families

### F100 Constraint Failures
Failures where explicit instructions, rules, or requirements are not preserved or satisfied.

- FR-0001 Constraint Non-Determinism
- FR-0002 Constraint Omission
- FR-0003 Partial Compliance
- FR-0004 Priority Inversion
- FR-0005 Constraint Ambiguity

### F200 Geometry Failures
Failures where physical, spatial, or structural relationships are wrong.

- FR-0006 Geometry Drift
- FR-0007 Incorrect Topology
- FR-0008 Component Substitution
- FR-0009 Scale Inconsistency
- FR-0010 Missing Assembly

### F300 Continuity Failures
Failures across revisions, views, or related artifacts.

- FR-0011 Revision Regression
- FR-0012 Camera Drift
- FR-0013 Style Drift
- FR-0014 Label Drift
- FR-0015 Cross-Artifact Inconsistency

### F400 Knowledge Failures
Failures caused by missing, unsupported, or invented knowledge.

- FR-0016 Hallucinated Feature
- FR-0017 Unsupported Assumption
- FR-0018 Canonical Substitution
- FR-0019 Evidence Gap
- FR-0020 Terminology Error

### F500 Publishing Failures
Failures in page, document, or production output.

- FR-0021 Caption Mismatch
- FR-0022 Broken Reference
- FR-0023 Layout Violation
- FR-0024 Typography Violation
- FR-0025 Artifact Version Mismatch

### F600 Validation Failures
Failures in the ability to test or verify output.

- FR-0026 Untestable Requirement
- FR-0027 Missing Acceptance Criteria
- FR-0028 Validator Disagreement
- FR-0029 Incomplete Traceability
- FR-0030 Confidence Misrepresentation

### F700 Workflow Failures
Failures in process, governance, review, and approval.

- FR-0031 Human Review Inconsistency
- FR-0032 Lost Revision
- FR-0033 Missing Approval
- FR-0034 Unlogged Exception
- FR-0035 Scope Creep

## Root Cause Model

Most failures appear to originate from one or more of these systemic causes:

1. Probabilistic generation without symbolic state.
2. Long natural-language prompts used as informal specifications.
3. Whole-output regeneration instead of localized correction.
4. No independent validation layer.
5. No canonical asset or evidence model.
6. No traceability from source knowledge to output.
7. Human approval without structured acceptance criteria.

## Mitigation Strategy
ConstraintOS mitigates these failures through:

- Atomic constraints
- Machine-readable specifications
- Renderer-specific compilers
- Independent validation
- Compliance reports
- Canonical assets
- Failure registry
- Regression tests
- Explicit approval records

## Traceability Principle
Every requirement, validator, compiler behavior, and workflow rule must trace to at least one failure mode or strategic principle.
