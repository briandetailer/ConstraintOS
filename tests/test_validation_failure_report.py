from constraintos.validation.failure_report import ValidationFailureReporter
from constraintos.validation.kernel import ValidationKernel
from constraintos.validation.models import ValidationGate


CONSTRAINT_PACK_REFERENCE = {"id": "CPACK-0001", "version": "0.1", "title": "LF4 Engineering Atlas Constraint Pack"}


def test_failure_report_is_clear_when_validation_passes() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[{"gate_id": "GATE-0001", "status": "passed", "message": "Passed."}],
    )

    failure_report = ValidationFailureReporter().build(report)

    assert failure_report.has_failures() is False
    assert failure_report.status == "passed"
    assert failure_report.to_dict()["failure_report"]["failure_count"] == 0


def test_failure_report_extracts_missing_evidence_issue() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[],
    )

    failure_report = ValidationFailureReporter().build(report)

    item = failure_report.failures[0]
    assert failure_report.status == "failed"
    assert item["gate_id"] == "GATE-0001"
    assert item["issue_code"] == "VAL-0001"
    assert item["severity"] == "blocker"


def test_failure_report_accepts_report_dictionary() -> None:
    failure_report = ValidationFailureReporter().build(
        {
            "validation_report": {"id": "VALIDATION-REPORT-0009", "status": "failed"},
            "results": [
                {
                    "gate_id": "GATE-0001",
                    "name": "LF4 Specificity Gate",
                    "status": "failed",
                    "required_pass": True,
                    "reason": "Gate did not pass.",
                    "issue_code": {"code": "VAL-0002", "severity": "blocker", "remediation": "Revise artifact."},
                }
            ],
        },
        failure_report_id="FAILURE-REPORT-0009",
    )

    payload = failure_report.to_dict()
    assert payload["failure_report"]["id"] == "FAILURE-REPORT-0009"
    assert payload["failure_report"]["validation_report_id"] == "VALIDATION-REPORT-0009"
    assert payload["failures"][0]["reason"] == "Gate did not pass."


def test_failure_report_preserves_constraint_pack_references() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[],
        constraint_packs=[CONSTRAINT_PACK_REFERENCE],
    )

    failure_report = ValidationFailureReporter().build(report)

    assert failure_report.constraint_packs == [CONSTRAINT_PACK_REFERENCE]
    assert failure_report.to_dict()["failure_report"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]


def test_failure_report_accepts_constraint_pack_references_from_dictionary() -> None:
    failure_report = ValidationFailureReporter().build(
        {
            "validation_report": {
                "id": "VALIDATION-REPORT-0009",
                "status": "failed",
                "constraint_packs": [CONSTRAINT_PACK_REFERENCE],
            },
            "results": [],
        },
        failure_report_id="FAILURE-REPORT-0009",
    )

    assert failure_report.to_dict()["failure_report"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
