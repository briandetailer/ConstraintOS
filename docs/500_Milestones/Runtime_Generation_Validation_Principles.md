# Runtime Generation Validation Principles

## Purpose

ConstraintOS is not a better-prompting layer. It is a disciplined generation pipeline for nondeterministic execution systems where a generated output must be checked against an explicit specification before it can be accepted.

The project should continue to separate these concerns:

```text
specification -> planning -> execution -> independent validation -> evidence -> approval
```

This applies whether execution is performed by a model, a deterministic tool, a CAD system, a renderer, a compiler, or an external service.

## Core principles

### 1. Nondeterministic generation must not self-certify

Generated output is not accepted because the generating model, plugin, or executor says it is correct. Acceptance requires independent validation against explicit runtime contracts, constraints, artifacts, traces, and evidence.

### 2. Validation is independent from execution

Execution and validation are separate responsibilities. The executor may produce artifacts, reports, traces, or errors, but the validation boundary must be able to inspect those outputs without trusting the executor that produced them.

### 3. Evidence must be portable outside Python

The Python runtime can remain the implementation core, but enterprise adoption depends on language-neutral boundaries. Runtime reports, trace reports, contract registries, and evidence manifests must be JSON artifacts that external Node.js, .NET, Terraform, CI/CD, or audit tools can consume without importing Python modules.

### 4. Adoption should begin as a validation layer

ConstraintOS should be adoptable as a bolt-on validation and evidence layer before it asks teams to replace their existing generation stack. The first enterprise path should be:

```text
existing generation workflow -> ConstraintOS validation/evidence layer -> existing approval/release process
```

Replacing or orchestrating more of the generation stack can come later, after the validation layer proves useful.

### 5. CSL must be stress-tested early

The hardest long-term design risk is not the runtime kernel. It is the constraint language. CSL must become expressive enough for real dimensional, structural, artifact, and workflow rules without simply recreating a full CAD, rendering, or workflow system inside the constraint language.

CSL should be tested early against real, messy specifications rather than only toy examples.

### 6. The validator must itself be validated

As validators become more capable, ConstraintOS must answer: who validates the validator?

Validator trust should be built through:

- deterministic contract tests
- replay fixtures
- known-good and known-bad examples
- negative tests for malformed outputs
- versioned validation rules
- validator result evidence
- regression suites for previously accepted failures

### 7. Approval is a separate boundary

Validation is not the same as approval. A runtime can pass structural validation and still require human, business, regulatory, or domain-specific approval. ConstraintOS should preserve approval as an explicit downstream decision rather than hiding it inside execution.

## Design implications for Milestone 3+

Runtime contract work should continue to prioritize:

- versioned public contracts
- independent verifiers
- self-contained evidence bundles
- artifact-level provenance
- replayable runtime event streams
- portable JSON outputs
- negative tests for every contract verifier
- explicit mapping from producers to public contracts

## Near-term follow-up candidates

1. Create CSL spike fixtures from a non-trivial real-world specification.
2. Add validator-fixture tests with known-good and known-bad evidence bundles.
3. Add evidence bundle examples under docs or examples for external consumers.
4. Add Node.js/.NET/Terraform-facing consumption examples for contract registry and evidence manifests.
5. Define an approval-gate contract distinct from runtime validation.
