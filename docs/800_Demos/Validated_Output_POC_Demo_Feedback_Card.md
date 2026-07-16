# Validated Output POC Demo Feedback Card

## Status

```text
feedback_card: Validated Output POC Demo Feedback Card
status: ready-for-use
scenario_key: supra_2jz_gte_twin_turbo
primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic
launcher_script: scripts/run-validated-output-poc-demo.ps1
implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only
```

## When to use this card

Use this card immediately after a reviewer watches the validated one-command output POC demo.

```powershell
.\scripts\run-validated-output-poc-demo.ps1
```

The reviewer should see the browser UI open and should see terminal evidence that the final decision remains `needs_review` and `approval_allowed` remains `false`.

## Reviewer context

```text
ConstraintOS is showing a fixture-safe product demonstration where input constraints produce controlled output permutations, deterministic SVG graphics, structural validation evidence, and reviewer-facing artifacts. This is not final production artwork and does not authorize automatic approval.
```

## Feedback prompts

### 1. Product clarity

```text
Did the one-command demo clearly show that constraints define controlled output permutations?
Response:
```

### 2. Evidence confidence

```text
Did the validation report, review packet, browser summary, and launcher summary make the demo feel auditable?
Response:
```

### 3. Browser usability

```text
Could you understand the generated browser page without opening JSON files first?
Response:
```

### 4. Approval safety

```text
Was it clear that the system preserved needs_review and approval_allowed: false?
Response:
```

### 5. Product gap

```text
What is the most important missing capability before this feels like a complete product demo?
Response:
```

## Feedback classification

Choose one primary signal:

```text
strong_product_signal
mixed_product_signal
weak_product_signal
```

Choose any applicable tags:

```text
browser_clarity
artifact_traceability
validation_trust
workflow_simplicity
business_story
visual_specificity_gap
scope_confusion
approval_safety
```

## Follow-up decision rule

```text
If strong_product_signal dominates:
- Continue improving the validated demo path and browser-facing evidence.
- Preserve deterministic fixture-safe scope.
- Do not add real image generation yet.

If mixed_product_signal dominates:
- Improve the reviewer handoff, browser copy, and artifact traceability before adding capability.
- Keep the one-command launcher as the entry point.

If weak_product_signal dominates:
- Pause feature expansion.
- Rework the story around constraints, evidence, review blocking, and output expectations.
```

## Explicitly blocked scope

```text
- Real generated final graphics.
- Production artwork generation.
- Real local image input.
- local_file_path loading.
- file_uri loading.
- Artifact download.
- Network fetch.
- Image decoding.
- Pixel inspection.
- CV/OCR provider integration.
- Automatic approval.
```
