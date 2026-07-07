# Use Case 2 - NREL 5-MW Wind Turbine Nacelle / Drivetrain Cutaway

## Purpose

Use this case to validate ConstraintOS against a renewable-energy engineering graphic where geometry, subsystem placement, power-flow direction, and label accuracy all matter.

The goal is not simply to draw a wind turbine. The goal is to test whether the system can preserve a known utility-scale horizontal-axis turbine architecture while generating controlled cutaway and schematic permutations.

## Test subject

```text
NREL offshore 5-MW baseline wind turbine nacelle / drivetrain technical graphic
```

## Why this is a strong graphics-validation case

```text
It is a public, documented engineering reference model.
It has fixed high-level properties: 5 MW, upwind, three-bladed, variable-speed, collective-pitch turbine.
It has named subsystems across rotor, nacelle, drivetrain, controls, tower, and yaw/pitch systems.
It supports both exterior and cutaway graphics.
It exposes common AI-image failures such as wrong blade count, fictional nacelle contents, and incorrect generator/gearbox placement.
```

## Reference basis

```text
Primary reference:
NREL/TP-500-38060
Definition of a 5-MW Reference Wind Turbine for Offshore System Development

Key reference facts:
- 5 MW rating
- upwind configuration
- three blades
- variable-speed, collective-pitch control
- high-speed, multiple-stage gearbox drivetrain
- 126 m rotor diameter
- 3 m hub diameter
- 90 m hub height
```

## Target graphic

```text
A labeled technical cutaway of the NREL 5-MW wind turbine nacelle and rotor drivetrain,
showing the rotor, hub, low-speed shaft, gearbox, high-speed shaft, generator, brake,
yaw system, pitch system, nacelle housing, and tower interface.
```

This is not just “make a wind turbine.” The system must preserve the turbine architecture while varying the view and visual style.

## Required permutations

```text
Subject:
NREL offshore 5-MW baseline horizontal-axis wind turbine

Views:
1. full turbine exterior elevation
2. nacelle cutaway side view
3. drivetrain-only schematic
4. rotor-to-generator power-flow diagram
5. nacelle inset on full turbine poster

Styles:
1. clean engineering manual
2. grayscale patent-style line art
3. educational classroom diagram
4. exploded technical illustration
5. flat-vector infographic

Label density:
1. no labels
2. major subsystem labels only
3. full drivetrain labels
4. labels plus short function descriptions

Output formats:
1. landscape poster
2. square social preview
3. book-page illustration
4. transparent-background turbine cutout
5. detailed nacelle-only diagram
```

## Subject identity constraints

```text
- The subject must be a horizontal-axis utility-scale wind turbine.
- It must represent the NREL offshore 5-MW baseline turbine concept.
- It must have exactly three blades.
- It must be an upwind turbine: rotor in front of the tower/nacelle relative to wind direction.
- It must not become a vertical-axis turbine.
- It must not become a small residential turbine.
- It must not include solar panels, sails, propellers unrelated to the rotor, or aircraft-like wings.
```

## Geometry constraints

```text
- Rotor must connect to the hub.
- Hub must connect to the nacelle.
- Nacelle must sit on top of the tower through the yaw bearing/system.
- Main shaft / low-speed shaft must run from the hub into the nacelle.
- Gearbox must sit between low-speed shaft and generator in geared drivetrain views.
- Generator must be behind the gearbox, not inside the blade hub.
- Tower must support the nacelle; nacelle must not float.
- Blade count must remain three in every view where the rotor is visible.
```

## Subsystem constraints

```text
- Blades must connect to pitch bearings or pitch mechanism at the hub.
- Hub must be distinct from nacelle housing.
- Low-speed shaft must connect hub to gearbox.
- Gearbox must connect low-speed shaft to high-speed shaft/generator.
- Generator must be downstream of the gearbox in the drivetrain path.
- Brake must be represented near the drivetrain, not on the blade tips.
- Yaw system must be at the nacelle/tower interface.
- Cooling/control electronics may be shown inside the nacelle but must not replace the gearbox or generator.
```

## Labeling constraints

```text
- Labels must not point to empty space.
- Labels must not assign the generator to the rotor hub.
- Labels must not duplicate gearbox/generator in conflicting locations.
- Labels must not invent components such as combustion engines, fuel tanks, exhaust pipes, or solar inverters.
- If a subsystem is not visible in a selected view, mark it hidden or omit it rather than fabricating it.
```

## Style constraints

```text
- Style may change, but turbine architecture may not.
- Educational simplification is allowed.
- Fictionalization is not allowed.
- Cutaway views may expose nacelle internals but must preserve exterior nacelle/tower relationships.
- Background wind farm scenery is allowed only if it does not obscure the turbine or labels.
```

## Evidence constraints

```text
- Every required subsystem must trace to the reference list or accepted turbine architecture.
- Any generated output must produce a pass/fail checklist.
- Any incorrect blade count, wrong turbine class, missing drivetrain path, or impossible component placement must mark the image as needs_review.
```

## User-facing request

```text
Create a labeled technical cutaway of the NREL 5-MW wind turbine nacelle in a clean engineering-manual style.
Show the rotor hub, low-speed shaft, gearbox, high-speed shaft, generator, brake, yaw system, pitch system, nacelle housing, and tower interface.
Preserve a three-bladed upwind horizontal-axis turbine.
Do not invent parts.
If a component location is uncertain or hidden, mark it for review instead of guessing.
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
- drivetrain path requirements
- output format

workers.json:
- reference collector
- constraint builder
- image prompt generator
- image evaluator
- evidence manifest generator
- approval reviewer

policy.json:
- must preserve three-blade upwind turbine identity
- must preserve nacelle/tower/rotor geometry
- must preserve drivetrain order
- must include required labels
- must reject hallucinated components
- must mark uncertainty as needs_review
```

## Expected run outputs

```text
1. Final image prompt
2. Negative prompt / forbidden elements
3. Generated image candidate
4. Geometry and label checklist
5. Evidence report
6. Approval result
```

## Example approval result

```text
decision: needs_review

passed:
- three-blade rotor present
- nacelle mounted on tower
- rotor connected to hub
- gearbox and generator shown inside nacelle
- technical cutaway style preserved

failed:
- generator label points to hub region
- yaw system omitted from tower/nacelle interface

required action:
- regenerate with stricter drivetrain-order and yaw-system constraints
```

## Core validation question

```text
Can ConstraintOS preserve a utility-scale wind turbine drivetrain and nacelle architecture across cutaway, exterior, schematic, and educational graphics while rejecting plausible but mechanically wrong illustrations?
```
