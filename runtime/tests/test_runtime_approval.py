from copy import deepcopy

from runtime import verify_runtime_approval_decision


def _approval_decision() -> dict:
    return {
        "runtime_approval": {
            "runtime_id": "RUNTIME-0001",
            "evidence_manifest_artifact_id": "ARTIFACT-0004",
            "decision": "approved",
            "decided_by": "policy-owner",
            "decided_at": "2026-07-06T00:00:00Z",
            "approval_policy": "default-runtime-approval/v1",
        },
        "checks": [
            {
                "id": "APPROVAL-CHECK-0001",
                "name": "runtime evidence manifest verified",
                "status": "passed",
                "source": "verify_runtime_evidence_manifest",
                "message": "Evidence manifest verification passed.",
                "metadata": {"runtime_id": "RUNTIME-0001"},
            }
        ],
        "notes": [],
    }


def test_runtime_approval_decision_verifier_accepts_valid_approval() -> None:
    verification = verify_runtime_approval_decision(_approval_decision())

    assert verification.successful()
    assert verification.to_dict() == {
        "runtime_approval_verification": {"successful": True, "issue_count": 0},
        "issues": [],
    }


def test_runtime_approval_decision_requires_runtime_id_and_manifest_reference() -> None:
    decision = _approval_decision()
    decision["runtime_approval"].pop("runtime_id")
    decision["runtime_approval"].pop("evidence_manifest_artifact_id")

    verification = verify_runtime_approval_decision(decision)

    assert not verification.successful()
    assert "Runtime approval requires runtime_id." in verification.issues
    assert "Runtime approval requires evidence_manifest_artifact_id." in verification.issues


def test_runtime_approval_decision_rejects_unknown_decision_value() -> None:
    decision = _approval_decision()
    decision["runtime_approval"]["decision"] = "maybe"

    verification = verify_runtime_approval_decision(decision)

    assert not verification.successful()
    assert "Runtime approval decision must be approved, rejected, needs_review, or waived." in verification.issues


def test_rejected_runtime_approval_requires_note_or_failed_check() -> None:
    decision = _approval_decision()
    decision["runtime_approval"]["decision"] = "rejected"

    verification = verify_runtime_approval_decision(decision)

    assert not verification.successful()
    assert "Rejected runtime approval decisions require a failed check or explanatory note." in verification.issues


def test_rejected_runtime_approval_allows_failed_check() -> None:
    decision = _approval_decision()
    decision["runtime_approval"]["decision"] = "rejected"
    decision["checks"][0]["status"] = "failed"

    verification = verify_runtime_approval_decision(decision)

    assert verification.successful()


def test_waived_runtime_approval_requires_note_or_waived_check() -> None:
    decision = _approval_decision()
    decision["runtime_approval"]["decision"] = "waived"

    verification = verify_runtime_approval_decision(decision)

    assert not verification.successful()
    assert "Waived runtime approval decisions require a waived check or explanatory note." in verification.issues


def test_runtime_approval_check_metadata_must_be_dictionary() -> None:
    decision = _approval_decision()
    decision["checks"][0]["metadata"] = []

    verification = verify_runtime_approval_decision(decision)

    assert not verification.successful()
    assert "Runtime approval check 1 metadata must be a dictionary." in verification.issues


def test_runtime_approval_verifier_does_not_mutate_payload() -> None:
    decision = _approval_decision()
    original = deepcopy(decision)

    verify_runtime_approval_decision(decision)

    assert decision == original
