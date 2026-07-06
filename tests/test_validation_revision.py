from constraintos.validation.failure_report import ValidationFailureReporter
from constraintos.validation.kernel import ValidationKernel
from constraintos.validation.models import ValidationGate
from constraintos.validation.remediation import ValidationRemediationPlanner
from constraintos.validation.revision import ValidationRevisionPlanner


CONSTRAINT_PACK_REFERENCE = {"id": "CPACK-0001", "version": "0.1", "title": "LF4 Engineering Atlas Constraint Pack"}


def test_revision_request_is_not_required_when_remediation_plan_is_clear() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[{"gate_id": "GATE-0001", "status": "passed"}],
    )
    failure_report = ValidationFailureReporter().build(report)
    remediation_plan = ValidationRemediationPlanner().build(failure_report)

    request = ValidationRevisionPlanner().build(remediation_plan, artifact_id="ARTIFACT-0001")

    assert request.required() is False
    assert request.status == "not_required"
    assert request.steps == []


def test_revision_request_creates_step_from_remediation_action() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[],
    )
    failure_report = ValidationFailureReporter().build(report)
    remediation_plan = ValidationRemediationPlanner().build(failure_report)

    request = ValidationRevisionPlanner().build(remediation_plan, artifact_id="ARTIFACT-0001")

    step = request.steps[0]
    assert request.required() is True
    assert request.status == "revision_required"
    assert step["id"] == "REVISION-STEP-0001"
    assert step["remediation_action_id"] == "REMEDIATION-0001"
    assert step["gate_id"] == "GATE-0001"
    assert step["issue_code"] == "VAL-0001"


def test_revision_request_accepts_remediation_plan_dictionary() -> None:
    request = ValidationRevisionPlanner().build(
        {
            "remediation_plan": {"id": "REMEDIATION-PLAN-0007", "status": "required"},
            "actions": [
                {
                    "id": "REMEDIATION-0001",
                    "gate_id": "GATE-0001",
                    "issue_code": "VAL-0002",
                    "severity": "blocker",
                    "instruction": "Revise artifact.",
                    "source_reason": "Gate did not pass.",
                }
            ],
        },
        artifact_id="ARTIFACT-0007",
        revision_request_id="REVISION-REQUEST-0007",
    )

    payload = request.to_dict()
    assert payload["revision_request"]["id"] == "REVISION-REQUEST-0007"
    assert payload["revision_request"]["artifact_id"] == "ARTIFACT-0007"
    assert payload["revision_request"]["remediation_plan_id"] == "REMEDIATION-PLAN-0007"
    assert payload["steps"][0]["instruction"] == "Revise artifact."


def test_revision_request_preserves_constraint_pack_references() -> None:
    report = ValidationKernel().evaluate(
        gates=[ValidationGate("GATE-0001", "LF4 Specificity Gate")],
        evidence=[],
        constraint_packs=[CONSTRAINT_PACK_REFERENCE],
    )
    failure_report = ValidationFailureReporter().build(report)
    remediation_plan = ValidationRemediationPlanner().build(failure_report)

    request = ValidationRevisionPlanner().build(remediation_plan, artifact_id="ARTIFACT-0001")

    assert request.constraint_packs == [CONSTRAINT_PACK_REFERENCE]
    assert request.to_dict()["revision_request"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]


def test_revision_request_accepts_constraint_pack_references_from_dictionary() -> None:
    request = ValidationRevisionPlanner().build(
        {
            "remediation_plan": {
                "id": "REMEDIATION-PLAN-0007",
                "status": "required",
                "constraint_packs": [CONSTRAINT_PACK_REFERENCE],
            },
            "actions": [],
        },
        artifact_id="ARTIFACT-0007",
        revision_request_id="REVISION-REQUEST-0007",
    )

    assert request.to_dict()["revision_request"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
