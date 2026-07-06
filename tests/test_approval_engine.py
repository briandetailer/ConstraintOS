from constraintos.approval import ApprovalEngine
from constraintos.validation import ValidationEvidence, ValidationGate, ValidationKernel


CONSTRAINT_PACK_REFERENCE = {"id": "CPACK-0001", "version": "0.1", "title": "LF4 Engineering Atlas Constraint Pack"}


def test_approval_engine_approves_passing_validation_report() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[ValidationEvidence("GATE-0001", "passed")],
        subject_id="LF4-ENGINE",
    )

    decision = ApprovalEngine().decide(report, artifact_id="ARTIFACT-0001")

    assert decision.approved() is True
    assert decision.status == "approved"
    assert decision.to_dict()["decision"]["summary"] == "Approved because all validation gates passed."


def test_approval_engine_rejects_required_validation_issue() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[],
        subject_id="LF4-ENGINE",
    )

    decision = ApprovalEngine().decide(report, artifact_id="ARTIFACT-0001")

    assert decision.approved() is False
    assert decision.status == "rejected"
    assert decision.reasons == ["VAL-0001: No evidence was supplied for this gate."]


def test_approval_engine_approves_optional_issue_with_warnings() -> None:
    report = ValidationKernel().evaluate(
        gates=[{"id": "GATE-0001", "name": "Optional Gate", "required_pass": False}],
        evidence=[{"gate_id": "GATE-0001", "status": "failed", "message": "Optional warning."}],
    )

    decision = ApprovalEngine().decide(report, artifact_id="ARTIFACT-0001")

    assert decision.approved() is True
    assert decision.status == "approved_with_warnings"
    assert decision.reasons == ["VAL-0002: Optional warning."]


def test_approval_engine_accepts_validation_report_dict() -> None:
    decision = ApprovalEngine().decide(
        {
            "validation_report": {"id": "VALIDATION-REPORT-0001", "status": "passed"},
            "results": [{"gate_id": "GATE-0001", "name": "Gate", "status": "passed", "required_pass": True}],
        },
        artifact_id="ARTIFACT-0001",
    )

    assert decision.status == "approved"
    assert decision.validation_report_id == "VALIDATION-REPORT-0001"


def test_approval_engine_preserves_constraint_pack_references() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[ValidationEvidence("GATE-0001", "passed")],
        subject_id="LF4-ENGINE",
        constraint_packs=[CONSTRAINT_PACK_REFERENCE],
    )

    decision = ApprovalEngine().decide(report, artifact_id="ARTIFACT-0001")

    assert decision.constraint_packs == [CONSTRAINT_PACK_REFERENCE]
    assert decision.to_dict()["approval"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]


def test_approval_engine_accepts_constraint_pack_references_from_dictionary() -> None:
    decision = ApprovalEngine().decide(
        {
            "validation_report": {
                "id": "VALIDATION-REPORT-0001",
                "status": "passed",
                "constraint_packs": [CONSTRAINT_PACK_REFERENCE],
            },
            "results": [{"gate_id": "GATE-0001", "name": "Gate", "status": "passed", "required_pass": True}],
        },
        artifact_id="ARTIFACT-0001",
    )

    assert decision.to_dict()["approval"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
