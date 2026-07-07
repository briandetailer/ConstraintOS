# Use Case 3 - Hydroelectric Dam / Powerhouse Cross-Section

## Purpose

Use this case to validate ConstraintOS against a civil / hydraulic / electrical infrastructure graphic where flow direction, component order, and process logic matter.

The goal is not simply to draw a dam. The goal is to test whether the system can preserve the functional sequence of a conventional hydroelectric plant from reservoir to penstock to turbine to generator to transmission.

## Test subject

```text
Conventional hydroelectric dam and powerhouse cross-section
```

## Why this is a strong graphics-validation case

```text
It combines civil infrastructure, hydraulics, mechanical systems, and electrical generation.
It has a clear process flow that can be checked visually.
It has named components with expected relative locations.
It supports cross-section, schematic, classroom, and engineering-manual styles.
It exposes common AI-image failures such as impossible water flow, misplaced turbines, submerged generators, and decorative but nonfunctional dams.
```

## Reference basis

```text
Primary reference:
U.S. Energy Information Administration hydropower explanation

Key reference facts:
- Hydropower uses moving water.
- The volume of water flow and elevation change/head determine available energy.
- At hydropower plants, water flows through a pipe or penstock.
- Water pushes turbine blades.
- The turbine spins a generator to produce electricity.
- Conventional storage systems use reservoirs created by dams and release water through turbines as needed.
```

## Target graphic

```text
A labeled technical cross-section of a conventional hydroelectric dam and powerhouse,
showing the reservoir, dam wall, intake, trash rack, penstock, turbine, generator,
powerhouse, transformer, transmission line, spillway, tailrace, and water-flow arrows.
```

This is not just “make a dam picture.” The system must preserve the hydraulic and electrical process.

## Required permutations

```text
Subject:
Conventional hydroelectric dam and powerhouse

Views:
1. side cross-section through dam and powerhouse
2. simplified classroom flow diagram
3. powerhouse cutaway
4. reservoir-to-grid process-flow schematic
5. pumped-storage comparison variant

Styles:
1. clean engineering manual
2. educational poster
3. grayscale patent-style line art
4. simplified flat-vector classroom diagram
5. infrastructure atlas plate

Label density:
1. no labels
2. major subsystem labels only
3. full infrastructure labels
4. labels plus short function descriptions

Output formats:
1. landscape poster
2. book-page illustration
3. square social preview
4. transparent-background dam cross-section elements
5. black-and-white printable worksheet
```

## Subject identity constraints

```text
- The subject must be a conventional hydroelectric dam / powerhouse system unless the variant explicitly asks for pumped storage.
- It must include water as the energy source.
- It must include a dam/reservoir relationship or explicitly state if using run-of-river.
- It must not become a coal, nuclear, geothermal, tidal, or generic factory power plant.
- It must not show combustion engines or smokestacks as the primary generation mechanism.
```

## Geometry and process constraints

```text
- Reservoir must be upstream and higher than the downstream tailrace for a conventional dam cross-section.
- Intake must connect reservoir water to the penstock.
- Penstock must carry water from the intake toward the turbine.
- Turbine must be downstream of the penstock and inside or near the powerhouse.
- Generator must be mechanically coupled to the turbine, not floating in the reservoir.
- Transformer and transmission lines must be on the electrical-output side, not in the water path.
- Spillway must be distinct from the penstock/turbine path.
- Tailrace must receive water after it passes through the turbine.
- Water-flow arrows must not contradict gravity/head unless the variant is pumped storage.
```

## Component constraints

```text
- Dam wall must retain water and create head.
- Reservoir must be behind/upstream of the dam.
- Intake/trash rack must be at the reservoir side.
- Penstock must be a pipe or conduit, not a decorative stream.
- Turbine must be positioned where high-energy water can turn it.
- Generator must be dry or housed, not submerged in the penstock.
- Transformer must connect to transmission lines.
- Spillway must route excess water around/over/through the dam without being mislabeled as the turbine.
```

## Labeling constraints

```text
- Labels must not point to empty space.
- Labels must not confuse penstock with spillway.
- Labels must not place turbine in reservoir without a functional water path.
- Labels must not show electrical transmission lines carrying water.
- Labels must not invent unrelated industrial equipment.
- If a component is hidden in a cross-section, label it as hidden or omit it rather than fabricating a visible object.
```

## Style constraints

```text
- Style may change, but process order may not.
- Educational simplification is allowed.
- Fictionalization is not allowed.
- Background landscape is allowed only if it does not obscure the cross-section or labels.
- Flow arrows must remain legible and directionally consistent.
```

## Evidence constraints

```text
- Every required component must trace to the reference list or accepted hydropower process.
- Any generated output must produce a pass/fail checklist.
- Any wrong flow direction, impossible component placement, or missing turbine/generator relationship must mark the image as needs_review.
```

## User-facing request

```text
Create a labeled cross-section of a conventional hydroelectric dam and powerhouse in a clean engineering-manual style.
Show the reservoir, dam wall, intake, trash rack, penstock, turbine, generator, powerhouse, transformer, transmission line, spillway, tailrace, and water-flow arrows.
Preserve the correct water path from reservoir to penstock to turbine to tailrace.
Do not invent unrelated power-plant equipment.
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
- hydraulic-flow constraints
- electrical-output constraints
- output format

workers.json:
- reference collector
- constraint builder
- image prompt generator
- process-flow evaluator
- image evaluator
- evidence manifest generator
- approval reviewer

policy.json:
- must preserve hydropower subject identity
- must preserve hydraulic flow direction
- must preserve turbine/generator relationship
- must include required labels
- must reject unrelated power-plant components
- must mark uncertainty as needs_review
```

## Expected run outputs

```text
1. Final image prompt
2. Negative prompt / forbidden elements
3. Generated image candidate
4. Hydraulic-flow checklist
5. Component-placement checklist
6. Evidence report
7. Approval result
```

## Example approval result

```text
decision: rejected

passed:
- reservoir and dam shown
- penstock included
- turbine and generator labeled
- transmission line shown

failed:
- water-flow arrows run from downstream river back into reservoir
- generator is shown submerged inside the penstock
- spillway and penstock labels conflict

required action:
- regenerate with strict gravity-fed flow direction and dry generator placement constraints
```

## Core validation question

```text
Can ConstraintOS preserve a physical process-flow system across cross-section, schematic, cutaway, and classroom graphics while rejecting plausible-looking but hydraulically impossible illustrations?
```
