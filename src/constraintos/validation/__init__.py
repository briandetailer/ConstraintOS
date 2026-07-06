from constraintos.validation.kernel import GATE_EVIDENCE_FAILED, MISSING_EVIDENCE, ValidationKernel
from constraintos.validation.models import ValidationEvidence, ValidationGate, ValidationIssueCode, ValidationReport, ValidationResult
from constraintos.validation.provenance import ValidationProvenanceManifest, ValidationProvenanceManifestBuilder

__all__ = [
    "GATE_EVIDENCE_FAILED",
    "MISSING_EVIDENCE",
    "ValidationApprovalPipeline",
    "ValidationApprovalResult",
    "ValidationEvidence",
    "ValidationGate",
    "ValidationIssueCode",
    "ValidationKernel",
    "ValidationProvenanceManifest",
    "ValidationProvenanceManifestBuilder",
    "ValidationReport",
    "ValidationResult",
]


def __getattr__(name: str):
    if name in {"ValidationApprovalPipeline", "ValidationApprovalResult"}:
        from constraintos.validation.pipeline import ValidationApprovalPipeline, ValidationApprovalResult

        exports = {
            "ValidationApprovalPipeline": ValidationApprovalPipeline,
            "ValidationApprovalResult": ValidationApprovalResult,
        }
        return exports[name]
    raise AttributeError(f"module 'constraintos.validation' has no attribute {name!r}")
