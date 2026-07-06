# Deterministic Provenance IDs

## Status

Implemented in the validation approval pipeline.

## Guarantees

- A provenance manifest id is derived from the validation report id when no explicit provenance id is supplied.
- `VALIDATION-REPORT-0007` derives `PROVENANCE-0007`.
- `VALIDATION-0008` derives `PROVENANCE-0008`.
- Missing validation report ids fall back to `PROVENANCE-0001`.
- Explicit provenance manifest ids still override derived ids.

## Notes

The first implementation slice is in the core validation approval pipeline. CLI default derivation remains deferred because the connector blocked the validation CLI edit during this session.
