from constraintos.approval import ApprovalEngine
from constraintos.validation import ValidationEvidence, ValidationGate, ValidationKernel


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
