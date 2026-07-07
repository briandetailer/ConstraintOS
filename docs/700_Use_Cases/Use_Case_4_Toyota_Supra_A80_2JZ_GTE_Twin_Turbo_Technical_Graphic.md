# Use Case 4 - Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic

## Purpose

Use this case to validate ConstraintOS against an enthusiast-car technical graphic where subject identity, engine identity, turbo-system layout, component placement, and audience scrutiny all matter.

This is the replacement automotive test case for the Cadillac ATS-V / LF4 challenge. The Toyota Supra Mk IV / A80 Turbo is a better early validation candidate because it has a much larger enthusiast footprint and far more publicly discussed technical reference material.

## Selection rules

```text
1. Has to be an enthusiast car.
2. Has to be twin turbo charged.
3. Has to have a cult following.
4. Must have readily available precise graphics available online to work from.
```

## Selected subject

```text
Toyota Supra Mk IV / A80 Turbo
Engine: Toyota 2JZ-GTE
Induction: sequential twin turbochargers
Target graphic: technical engine-bay / sequential twin-turbo system illustration
```

## Why this is a strong graphics-validation case

```text
It is one of the most recognized enthusiast cars of the 1990s.
It has a cult following and an unusually high level of enthusiast scrutiny.
It has a factory twin-turbo inline-six engine.
The 2JZ-GTE sequential turbo system has a specific layout and operating sequence.
There are many public technical discussions, repair-manual references, parts diagrams, and engine-bay photos.
Mistakes are easy for the target audience to detect.
```

## Reference basis

```text
Reference facts to verify before production use:
- A80 Supra Turbo used the Toyota 2JZ-GTE inline-six.
- The 2JZ-GTE is twin turbocharged.
- The Supra turbo system operates sequentially, not as a simple parallel twin-turbo layout.
- The turbo model used larger brakes and distinctive A80 body features.
- The 2JZ-GTE differs from the naturally aspirated 2JZ-GE in forced-induction hardware and supporting components.
```

Before using any specific repair-manual page, parts diagram, or photo in a production image workflow, confirm that the source is legitimate and that reuse is allowed. For ConstraintOS validation, the system can still use the reference list to test constraints without redistributing source artwork.

## Target graphic

```text
A clean technical infographic / engineering atlas plate of the Toyota Supra A80 Turbo 2JZ-GTE engine bay,
showing the inline-six engine, sequential twin-turbo system, intake path, intercooler path,
exhaust/turbine path, major turbo-control valves, and key engine-bay landmarks.
```

This is not just “make a Supra picture.” The system must preserve the A80 Supra identity and the 2JZ-GTE sequential twin-turbo architecture while varying view, style, label density, and publishing format.

## Required permutations

```text
Subject:
Toyota Supra Mk IV / A80 Turbo 2JZ-GTE

Views:
1. engine-bay top/front three-quarter view
2. 2JZ-GTE side cutaway
3. sequential twin-turbo flow schematic
4. front-mounted intercooler routing diagram
5. full car exterior with engine-bay inset

Styles:
1. clean engineering manual
2. enthusiast magazine technical spread
3. grayscale patent-style line art
4. simplified flat-vector classroom diagram
5. exploded subsystem callout plate

Label density:
1. no labels
2. major subsystem labels only
3. full turbo-system labels
4. full labels plus short function descriptions

Output formats:
1. landscape poster
2. book-page illustration
3. square social preview
4. transparent-background engine cutout
5. printable black-and-white worksheet
```

## Subject identity constraints

```text
- The subject must be a Toyota Supra Mk IV / A80 Turbo.
- It must not become a Nissan Skyline GT-R, Mazda RX-7, Mitsubishi 3000GT, BMW Z4, newer GR Supra, generic tuner car, or fictional sports car.
- The engine must be represented as a Toyota 2JZ-GTE inline-six, not a V6, V8, rotary, boxer, or electric drivetrain.
- The turbo system must be twin-turbocharged.
- The turbo system must be represented as sequential unless a variant explicitly asks for a simplified high-level twin-turbo diagram.
- The car must remain front-engine, rear-wheel-drive in whole-car views.
```

## Geometry constraints

```text
- The engine must be an inline-six layout.
- Turbochargers must be on the exhaust side of the engine, not randomly placed on top of the valve cover.
- Intake manifold/plenum must be distinguishable from exhaust/turbo hardware.
- Intercooler path must route compressed air through an intercooler before entering the intake path.
- Exhaust path must feed turbine housings before exiting through downpipe/exhaust.
- The engine bay must not gain an impossible second engine, V-bank, rotary housing, or electric motor pack.
- Whole-car views must preserve A80 Supra proportions: long hood, hatchback/liftback rear, rounded 1990s body, optional large rear wing.
```

## Sequential twin-turbo constraints

```text
- The system must distinguish primary and secondary turbocharger function.
- Low-RPM operation should emphasize the first/primary turbo.
- Transition/pre-spool operation may show exhaust routing to bring the second turbo up to speed.
- High-RPM operation should show both turbochargers contributing.
- Turbo-control valves, actuators, or VSV-style controls may be simplified but must not be replaced with unrelated parts.
- The diagram must not claim the system is a simple symmetrical parallel twin-turbo layout unless specifically presenting a simplified comparison.
```

## Required component labels

```text
- 2JZ-GTE inline-six
- valve cover / cam cover
- intake manifold / plenum
- exhaust manifold
- primary turbocharger
- secondary turbocharger
- intercooler
- intake charge path
- exhaust flow path
- throttle body
- wastegate / boost-control path
- sequential turbo control valves / actuators
- downpipe / exhaust outlet
```

## Labeling constraints

```text
- Labels must not point to empty space.
- Labels must not swap intake and exhaust paths.
- Labels must not duplicate a single turbocharger and call it twin turbo.
- Labels must not call the engine an RB26DETT, VR38DETT, LF4, 13B, LS, B58, or generic inline-six.
- Labels must not invent non-existent factory systems.
- If a component is uncertain or hidden in the selected view, mark it hidden/needs_review rather than fabricating a visible part.
```

## Style constraints

```text
- Style may change, but engine and car identity may not.
- Enthusiast-magazine styling is allowed.
- Fictionalization is not allowed.
- Decorative smoke, flames, racing graphics, or cinematic backgrounds are allowed only if they do not obscure technical components.
- Toyota logos, Supra badges, and exact OEM diagrams should be handled carefully and only used when source/reuse policy allows.
```

## Evidence constraints

```text
- Every required subsystem must be traceable to the reference list.
- Any generated output must produce a pass/fail checklist.
- Any incorrect engine family, wrong turbo count, non-sequential turbo logic, impossible flow direction, or mislabeled component must mark the image as needs_review or rejected.
```

## User-facing request

```text
Create a technical infographic of the Toyota Supra Mk IV / A80 Turbo 2JZ-GTE sequential twin-turbo system in a clean engineering-manual style.
Show the engine from an engine-bay top/front three-quarter view.
Label the 2JZ-GTE inline-six, intake manifold, exhaust manifold, primary turbocharger, secondary turbocharger, intercooler, intake charge path, exhaust flow path, throttle body, wastegate/boost-control path, sequential turbo control valves, and downpipe.
Do not turn it into a Skyline GT-R, RX-7, newer GR Supra, generic tuner car, V-engine, or single-turbo swap.
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
- sequential turbo flow requirements
- output format

workers.json:
- reference collector
- constraint builder
- image prompt generator
- technical-flow evaluator
- image evaluator
- evidence manifest generator
- approval reviewer

policy.json:
- must preserve A80 Supra / 2JZ-GTE identity
- must preserve inline-six geometry
- must preserve twin-turbo count
- must preserve sequential turbo logic
- must preserve intake/exhaust flow direction
- must include required labels
- must reject wrong-car or wrong-engine substitutions
- must mark uncertainty as needs_review
```

## Expected run outputs

```text
1. Final image prompt
2. Negative prompt / forbidden elements
3. Generated image candidate
4. Subject-identity checklist
5. Turbo-system flow checklist
6. Label-placement checklist
7. Evidence report
8. Approval result
```

## Example approval result

```text
decision: rejected

passed:
- A80 Supra body reference present
- inline-six engine represented
- two turbochargers visible
- technical infographic style preserved

failed:
- turbochargers shown as a simple parallel V-engine layout
- intake and exhaust paths are swapped
- engine label says RB26DETT instead of 2JZ-GTE
- intercooler is omitted despite being required

required action:
- regenerate with stricter 2JZ-GTE identity, sequential-turbo flow, and intake/exhaust path constraints
```

## Core validation question

```text
Can ConstraintOS preserve a highly scrutinized enthusiast-car engine subject across style, view, label-density, and format permutations while rejecting good-looking but mechanically wrong graphics?
```
