# Provenance Contract Hardening

## Status

Deferred for code implementation in this session.

## Reason

The current branch is green at 335 passed. The next intended slice is to add runtime consistency checks for provenance manifests, including node ordering, status consistency, result counts, and duplicate gate detection.

The GitHub connector blocked attempted code and schema writes for this slice, so no runtime behavior was changed.

## Intended checks

- The traceability node list should remain deterministic.
- Manifest status should match the approval decision node.
- Validation status should match the validation report node.
- Validation result count should match the number of gate traces.
- Gate trace entries should not repeat gate ids.

## Safe baseline

The safe baseline remains the deterministic provenance id slice at 335 passing tests.
