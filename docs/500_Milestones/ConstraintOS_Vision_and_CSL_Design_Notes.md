# ConstraintOS — Vision & CSL Design Notes

Compiled from working discussion. This captures the project vision, CSL design decisions made so far, and Claude's critique points that should remain active in future architecture discussions.

## Problem

AI-driven generation is nondeterministic by default. The same prompt, model, or renderer can produce different outputs run to run, which makes production pipelines unrepeatable, unauditable, and untrustworthy wherever precision matters: engineering drawings, manufacturing specs, compliance-heavy artifacts, or any workflow where close enough is not acceptable.

## Vision

ConstraintOS is a deterministic orchestration platform for AI-driven production workflows. It separates specification, execution, validation, and approval so results are repeatable across models, rendering engines, and time.

## Mission

Build an operating system for AI production that coordinates LLMs, renderers, validators, and human review while preserving traceability, auditability, and deterministic outputs.

## Core principles

1. Specifications are authoritative.
2. Constraints are explicit and testable.
3. Rendering is orchestrated, not improvised.
4. Validation is independent of generation.
5. Every artifact is traceable.
6. Humans approve; automation executes.

## Product pillars

### Constraint Specification Language (CSL)

A declarative language for expressing the rules, dimensions, geometric relationships, and logical constraints that any generated output must satisfy.

### Kernel and compiler

Parses and compiles CSL specs into executable constraint sets.

### Validation engine

Independently checks generated output against the compiled spec. Pass/fail is deterministic, not a judgment call by the generator.

### Runtime and worker orchestration

Schedules and coordinates generation, rendering, and validation jobs across models and engines.

### Schema registry

Versioned store of constraint schemas and spec definitions.

### Artifact store

Versioned, traceable store of every generated output and its provenance.

### Renderer plugins

Pluggable interfaces to rendering engines, so outputs stay engine-agnostic.

### API and CLI

Programmatic and command-line access to the full pipeline.

### Hosted platform, future

Managed version of the above for teams that do not want to self-host.

## Beta 1 goals

- Green CI.
- Stable schema registry.
- Complete documentation.
- Deterministic validation: same spec plus same input produces the same pass/fail result every time.
- Production-ready developer experience: CLI/API usable end-to-end without hand-holding.

## Long-term roadmap

- Beta 2: Renderer orchestration.
- Beta 3: Multi-model execution.
- RC1: Hosted runtime.
- 1.0: Commercial SaaS platform.

## Integration model

Teams should not have to replace their existing stack to use ConstraintOS. Entry points should be provided for .NET, C#, Node.js, JavaScript, and additional languages/runtimes over time.

Teams plug into ConstraintOS and results are sent back to their own stack. ConstraintOS acts first as a validation/orchestration layer, not as a replacement generation environment.

Implications for this model:

- API surfaces and SDKs need to feel native per language ecosystem, not like a generic REST bolt-on.
- Sync vs. async execution needs to be deliberate. Teams may need call-and-wait for CI/build loops and submit-and-poll or webhook flow for longer jobs.
- The schema registry needs to make spec/integration version mismatches obvious rather than silently validating against a stale schema.

## CSL design decisions

Detailed object contract: `CSL_Minimum_Viable_Object_Shape.md` defines the current minimum viable CSL v1 document, entity, constraint, group, and validation result shapes.

### Format

CSL should be JSON/YAML-based, not a custom DSL for v1.

Rationale:

- Entry points are programmatic: .NET/C#/Node/JavaScript calling in.
- JSON/YAML keeps parsing simple.
- JSON/YAML works naturally with a schema registry and versioning.
- A thin DSL that compiles down to the same JSON/YAML can remain a possible future convenience, but it is not a v1 requirement.

### Constraint types

Constraints are split into two categories.

Dimensional constraints are the base/default type. These cover scalar bounds and tolerances, such as a dimension needing to fall between X and Y.

Relational or geometric constraints are optional overlay types. These include relationships such as parallel, concentric, perpendicular, degree-based angular rules, and similar relations between named entities.

### Groups as the composability layer

Constraints can be conjoined or related through a group layer.

Groups support:

- AND
- OR
- NOT

AND and OR are standard multi-child combinators.

NOT is unary. It wraps a single constraint or group and inverts its result. This is useful for cases such as keep-out zones, where a feature must not overlap a region, instead of forcing everything into inverted tolerance math.

Nesting is recursive and supports mixed operators. A group can contain other groups, and different branches of the tree can use different operators. This mirrors real-world tolerance stacks, such as:

```text
(A AND B) OR (C AND D)
```

### Failure and audit reporting

Full tree recording is the chosen default approach.

Every constraint, group, and branch in the evaluation tree is logged, regardless of whether it was strictly necessary to the final pass/fail result. For example, OR branches that could have short-circuited still get recorded.

This supports the principle that every artifact is traceable. Audit logs should show exactly which path was evaluated and why a group passed or failed, not only the top-level result.

Tradeoff:

- Full tree recording costs more in validation speed and artifact size than summary-only reporting.
- A future verbose vs. summary mode in the artifact store may help manage this at scale without abandoning full tree recording as the default.

Open consideration:

When NOT wraps a group, the tree should record the inner group's real pre-inversion pass/fail result alongside NOT's inverted result. Audit logs should remain readable, for example: inner check passed, so NOT correctly failed the constraint.

## Open CSL questions

### Entity referencing

How should constraints point at specific named geometric entities, such as edges, holes, datums, planes, faces, anchors, or regions, so relational constraints are unambiguous?

Likely direction: entity IDs live on the base dimensional or geometric constraint object, with groups referencing those IDs. This is not confirmed yet.

### Templates and macros

Should reusable constraint bundles be supported, such as a fastener hole pattern, alignment stack, clearance rule, or material-specific tolerance bundle?

Open question: are templates/macros first-class in v1, or does every spec start fully expanded?

### Versioning field

A `csl_version` or equivalent field should likely be baked into every spec from the start. This avoids retrofitting versioning once specs exist in the wild.

## Claude critique captured for design planning

The following points should remain active as stress tests for the architecture:

### Nondeterminism is the real pain

Nondeterminism in AI generation is a real, unsolved pain point, and it gets worse as more of the pipeline is delegated to models. In domains where output must match a spec exactly, the system cannot rely on the generator usually getting it right.

### The architecture instinct is right

Separating spec, execution, validation, and approval mirrors safety-critical software and hardware workflows:

```text
spec -> build -> independent test -> sign-off
```

ConstraintOS should build that discipline into AI-generation workflows in a first-class way.

### Independent validation is the central principle

Validation independent of generation is the single most important principle. AI tooling often conflates model confidence with correctness. ConstraintOS must explicitly reject that pattern.

### CSL is the hardest part

The hardest part may not be the kernel, compiler, or validator architecture. It may be CSL itself.

CSL must be expressive enough to cover real CAD/dimensional/geometric rules without becoming as complicated as the CAD software itself. This needs early prototyping against a real, gnarly spec rather than a toy example.

### Adoption path matters

ConstraintOS should be adoptable as a validation layer bolted onto existing generation pipelines before it asks users to replace their stack. That is likely the easiest path to real usage data and enterprise adoption.

### Validate the validator

The system must decide early how trust in the validation engine will be built. As CSL and constraint types grow, the validator itself becomes load-bearing and must have its own tests, fixtures, failure examples, versioning, and evidence.

## Near-term discussion queue

1. Define the minimum viable CSL object shape.
2. Decide whether `csl_version` is mandatory in every spec from day one.
3. Prototype entity referencing for a non-trivial geometric example.
4. Choose one real, messy spec to stress-test CSL.
5. Define the first validator evidence payload.
6. Decide whether approval-gate results become their own contract.
7. Define CI/build-loop integration expectations: sync, async, polling, and webhooks.
8. Sketch Node.js and .NET SDK ergonomics from the consumer's point of view.
