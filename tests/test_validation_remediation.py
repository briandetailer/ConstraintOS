from constraintos.validation.failure_report import ValidationFailureReporter
from constraintos.validation.kernel import ValidationKernel
from constraintos.validation.models import ValidationGate
from constraintos.validation.remediation import ValidationRemediationPlanner


CONSTRAINT_PACK_REFERENCE = {"id": "CPACK-0001", "version": "0.1", "title": "LF4 Engineering Atlas Constraint Pack"}


def test_remediation_plan_is_not_required_when_failure_report_is_clear() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[{"gate_id": "GATE-0001", "status": "passed"}],
    )
    failure_report = ValidationFailureReporter().build(report)

    plan = ValidationRemediationPlanner().build(failure_report)

    assert plan.required() is False
    assert plan.status == "not_required"
    assert plan.actions == []


def test_remediation_plan_creates_action_for_missing_evidence() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[],
    )
    failure_report = ValidationFailureReporter().build(report)

    plan = ValidationRemediationPlanner().build(failure_report)

    action = plan.actions[0]
    assert plan.required() is True
    assert action["id"] == "REMEDIATION-0001"
    assert action["gate_id"] == "GATE-0001"
    assert action["issue_code"] == "VAL-0001"
    assert action["instruction"] == "Supply evidence for the required validation gate."


def test_remediation_plan_accepts_failure_report_dictionary() -> None:
    plan = ValidationRemediationPlanner().build(
        {
            "failure_report": {"id": "FAILURE-REPORT-0007", "status": "failed"},
            "failures": [
                {
                    "gate_id": "GATE-0001",
                    "gate_name": "LF4 Specificity Gate",
                    "issue_code": "VAL-0002",
                    "severity": "blocker",
                    "reason": "Gate did not pass.",
                    "remediation": "Revise artifact.",
                }
            ],
        },
        remediation_plan_id="REMEDIATION-PLAN-0007",
    )

    payload = plan.to_dict()
    assert payload["remediation_plan"]["id"] == "REMEDIATION-PLAN-0007"
    assert payload["remediation_plan"]["failure_report_id"] == "FAILURE-REPORT-0007"
    assert payload["actions"][0]["instruction"] == "Revise artifact."


def test_remediation_plan_preserves_constraint_pack_references() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[],
        constraint_packs=[CONSTRAINT_PACK_REFERENCE],
    )
    failure_report = ValidationFailureReporter().build(report)

    plan = ValidationRemediationPlanner().build(failure_report)

    assert plan.constraint_packs == [CONSTRAINT_PACK_REFERENCE]
    assert plan.to_dict()["remediation_plan"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]


def test_remediation_plan_accepts_constraint_pack_references_from_dictionary() -> None:
    plan = ValidationRemediationPlanner().build(
        {
            "failure_report": {
                "id": "FAILURE-REPORT-0007",
                "status": "failed",
                "constraint_packs": [CONSTRAINT_PACK_REFERENCE],
            },
            "failures": [],
        },
        remediation_plan_id="REMEDIATION-PLAN-0007",
    )

    assert plan.to_dict()["remediation_plan"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
