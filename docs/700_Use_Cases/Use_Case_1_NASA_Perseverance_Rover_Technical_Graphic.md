# Use Case 1 - NASA Perseverance Rover Technical Graphic

## Purpose

Use this case to validate ConstraintOS against a real graphics-generation problem where visual accuracy matters more than style quality alone.

The goal is not simply to generate a good-looking rover image. The goal is to test whether the system can preserve subject identity, subsystem placement, labels, view constraints, style constraints, and approval evidence across controlled graphic permutations.

## Test subject

```text
NASA Perseverance rover annotated technical graphic / engineering atlas plate
```

## Why this is a strong graphics-validation case

```text
It is a real physical object.
It has complex geometry.
It has named subsystems.
It has multiple valid viewing angles.
It has enough public reference material.
It supports many graphic permutations.
It is easy to tell when the model hallucinates.
```

It is close to the LF4 engine problem, but safer for testing because public NASA/JPL reference material is widely available. The rover has concrete, named components and instruments such as Mastcam-Z, SuperCam, MEDA, MOXIE, PIXL, RIMFAX, SHERLOC, the robotic arm, wheels, mast, chassis, and sampling hardware.

## Target graphic

```text
A clean technical infographic plate of the NASA Perseverance rover,
shown in three-quarter view, with major instruments labeled,
plus controlled permutations for alternate views, style, label density,
and publishing format.
```

This is not just “make a rover picture.” The system must preserve the rover while varying the presentation.

## Required permutations

```text
Subject:
NASA Perseverance rover

Views:
1. front-left three-quarter view
2. side profile
3. top-down schematic
4. instrument-location callout plate

Styles:
1. clean engineering manual
2. educational poster
3. grayscale patent-style line art
4. simplified flat-vector classroom diagram

Label density:
1. no labels
2. major subsystem labels only
3. full instrument labels
4. full labels plus short function descriptions

Output formats:
1. square social preview
2. landscape poster
3. book-page illustration
4. transparent-background rover cutout
```

## Subject identity constraints

```text
- The subject must be NASA’s Perseverance Mars rover.
- It must not become Curiosity, Opportunity, Spirit, a generic rover, a lunar rover, or a fictional rover.
- It must retain six wheels.
- It must retain a central rover chassis.
- It must retain a mast/camera head.
- It must retain a robotic arm with an instrument turret.
- It must show the rover as an unmanned robotic vehicle, not a crewed vehicle.
```

## Geometry constraints

```text
- Six wheels must remain visible or logically present.
- Wheel arrangement must follow rocker-bogie rover layout.
- Mast must rise from the rover body, not from the arm.
- Robotic arm must attach to the front/body area, not the rear power unit.
- Instrument turret must be at the end of the robotic arm.
- Deck-mounted instruments must remain on or near the rover body.
- The rover must not gain tank tracks, solar panels, cockpit glass, human seats, or animal-like legs.
```

## Instrument constraints

```text
- Mastcam-Z must be associated with the mast/camera head.
- SuperCam must be associated with the mast unit.
- PIXL must be associated with the arm/turret region.
- SHERLOC must be associated with the arm/turret region.
- MOXIE must be represented as an internal/body-mounted technology payload, not an external antenna.
- RIMFAX must be associated with the lower/rear underside antenna region.
- MEDA must be represented as environmental sensors, not as a camera cluster.
```

## Labeling constraints

```text
- Labels must not point to empty space.
- Labels must not duplicate the same instrument in conflicting locations.
- Labels must not invent non-existent systems.
- Label text must remain legible.
- If uncertain, omit the label rather than fabricate placement.
```

## Style constraints

```text
- Style may change, but subject geometry may not.
- Educational simplification is allowed.
- Fictionalization is not allowed.
- Decorative Mars background is allowed only if it does not obscure the rover or labels.
- NASA logo use should be avoided in generated output unless explicitly allowed by a later policy.
```

## Evidence constraints

```text
- Every required subsystem must be traceable to a reference list.
- Any generated output must produce a pass/fail checklist.
- Any missing, ambiguous, or incorrectly placed subsystem must mark the image as needs_review.
```

## User-facing request

```text
Create a technical infographic of the NASA Perseverance rover in a clean engineering-manual style.
Show the rover from a front-left three-quarter view.
Label Mastcam-Z, SuperCam, MEDA, MOXIE, PIXL, RIMFAX, SHERLOC, robotic arm, wheels, mast, and chassis.
Do not invent parts.
If a component location is uncertain, mark it for review instead of guessing.
```

## ConstraintOS runtime mapping

```text
spec.json:
- subject
- target graphic
- required view
- required style
- required labels
- forbidden substitutions
- output format

workers.json:
- reference collector
- constraint builder
- image prompt generator
- image evaluator
- evidence manifest generator
- approval reviewer

policy.json:
- must preserve subject identity
- must preserve required geometry
- must include required labels
- must reject hallucinated labels
- must mark uncertainty as needs_review
```

## Expected run outputs

```text
1. Final image prompt
2. Negative prompt / forbidden elements
3. Generated image candidate
4. Constraint checklist
5. Evidence report
6. Approval result
```

## Example approval result

```text
decision: needs_review

passed:
- six-wheel rover layout present
- mast visible
- robotic arm visible
- technical infographic style preserved
- major labels included

failed:
- RIMFAX label placement ambiguous
- MOXIE represented as external object instead of body/internal payload

required action:
- regenerate with stricter instrument-placement constraints
```

## Core validation question

This test should answer:

```text
Can ConstraintOS preserve a complex, real-world engineering subject across style, view, label-density, and output-format permutations while rejecting plausible-looking but incorrect graphics?
```

If ConstraintOS cannot keep Perseverance from becoming a generic Mars rover, it will not keep the LF4 from becoming a generic GM V6.
