# ConstraintOS Architecture Book

Status: Draft
Milestone: Beta 1

## Purpose
The Architecture Book is the canonical technical explanation of ConstraintOS. It consolidates phased design work into a coherent system manual.

## 1. Introduction
ConstraintOS is a deterministic orchestration layer for AI-driven production workflows. It coordinates specifications, compilers, renderers, validators, runtime workers, and human approval.

## 2. Product Vision
ConstraintOS exists because prompt-driven generation alone is insufficient for repeatable production. The system must separate intent, constraints, execution, validation, and approval.

## 3. Core Principle
ConstraintOS does not generate content. It governs production.

## 4. Kernel
The kernel owns correctness semantics: specifications, constraints, compilation, validation, review, patching, and lifecycle behavior.

## 5. Constraint Specification Language
CSL defines artifact requirements, constraints, acceptance criteria, validation methods, and traceability.

## 6. Compiler
The compiler translates structured specifications into renderer- or executor-facing instructions while preserving unsupported constraints.

## 7. Validation Engine
Validation evaluates artifacts against explicit constraints and schemas. It must be independent from generation.

## 8. Artifact Lifecycle
Artifacts move through draft, compiled, rendered, reviewed, approved, patched, and archived states.

## 9. Storage
Storage backends persist artifacts and references without becoming the authority over correctness.

## 10. Runtime
The runtime coordinates jobs, queues, workers, leases, retries, failures, and observability.

## 11. Worker System
Workers execute registered job handlers. They do not own correctness semantics.

## 12. API
The API exposes kernel and runtime capabilities while preserving the kernel/platform boundary.

## 13. CLI
The CLI provides local development, validation, traceability, registry reporting, and artifact operations.

## 14. Schema Registry
The schema registry is the central source for artifact family detection and schema lookup.

## 15. Observability
Observability reports operational state: workers, queue, failures, runtime health, and readiness.

## 16. Renderer Orchestration
Renderer orchestration is the next major product frontier. ConstraintOS should orchestrate tools such as Blender, vector processors, and publishing systems without becoming those tools.

## 17. Hosted Platform
The hosted platform will add users, organizations, billing, tenancy, subscriptions, encryption, and user-facing workflow management. These concerns remain outside the kernel.

## 18. Roadmap
Beta 1 stabilizes the kernel and developer experience. Beta 2 introduces renderer orchestration. Beta 3 introduces multi-model execution. Release Candidate 1 targets hosted runtime readiness.
