import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate

from runtime import (
    ArtifactStore,
    RuntimeApprovalReportWriter,
    verify_runtime_approval_decision,
    verify_runtime_approval_policy,
)


SCHEMA_ROOT = Path("schemas/runtime/v1")


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


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


def _approval_policy() -> dict:
    return {
        "runtime_approval_policy": {
            "name": "default-runtime-approval/v1",
            "version": "v1",
            "contract_registry_version": "runtime-contracts/v1",
        },
        "required_evidence_artifacts": [
            "runtime_report",
            "runtime_trace_report",
            "runtime_contract_registry",
            "runtime_evidence_manifest",
        ],
        "required_checks": ["verify_runtime_evidence_manifest"],
        "allowed_decisions": ["approved", "rejected", "needs_review", "waived"],
        "allowed_check_statuses": ["passed", "failed", "waived", "needs_review"],
        "approvers": ["policy-owner"],
        "waiver_rules": {"requires_note_or_waived_check": True},
        "rejection_rules": {"requires_note_or_failed_check": True},
    }


def _approval_report_artifact(tmp_path: Path) -> dict:
    return RuntimeApprovalReportWriter(ArtifactStore(tmp_path)).write_approval(_approval_decision()).to_dict()


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


def test_runtime_approval_decision_matches_json_schema() -> None:
    schema = _schema("runtime-approval-decision.schema.json")

    validate(instance=_approval_decision(), schema=schema)


def test_runtime_approval_decision_schema_rejects_unknown_decision() -> None:
    schema = _schema("runtime-approval-decision.schema.json")
    decision = _approval_decision()
    decision["runtime_approval"]["decision"] = "maybe"

    with pytest.raises(ValidationError):
        validate(instance=decision, schema=schema)


def test_runtime_approval_decision_schema_rejects_unknown_check_status() -> None:
    schema = _schema("runtime-approval-decision.schema.json")
    decision = _approval_decision()
    decision["checks"][0]["status"] = "unknown"

    with pytest.raises(ValidationError):
        validate(instance=decision, schema=schema)


def test_runtime_approval_decision_schema_rejects_non_object_metadata() -> None:
    schema = _schema("runtime-approval-decision.schema.json")
    decision = _approval_decision()
    decision["checks"][0]["metadata"] = []

    with pytest.raises(ValidationError):
        validate(instance=decision, schema=schema)


def test_runtime_approval_report_writer_writes_approval_artifact(tmp_path) -> None:
    artifact = RuntimeApprovalReportWriter(ArtifactStore(tmp_path)).write_approval(_approval_decision())

    assert artifact.to_dict() == {
        "id": "ARTIFACT-0001",
        "uri": (tmp_path / "approvals" / "RUNTIME-0001.json").resolve().as_uri(),
        "kind": "file",
        "producer": "policy-owner",
        "metadata": {
            "path": str((tmp_path / "approvals" / "RUNTIME-0001.json").resolve()),
            "artifact_role": "runtime_approval_report",
            "content_type": "application/json",
            "runtime_id": "RUNTIME-0001",
            "evidence_manifest_artifact_id": "ARTIFACT-0004",
            "decision": "approved",
            "approval_policy": "default-runtime-approval/v1",
            "decided_by": "policy-owner",
            "decided_at": "2026-07-06T00:00:00Z",
        },
    }


def test_runtime_approval_report_writer_persists_approval_payload(tmp_path) -> None:
    decision = _approval_decision()
    artifact = RuntimeApprovalReportWriter(ArtifactStore(tmp_path)).write_approval(decision)

    assert json.loads(Path(artifact.metadata["path"]).read_text(encoding="utf-8")) == decision


def test_runtime_approval_report_writer_rejects_invalid_decision(tmp_path) -> None:
    decision = _approval_decision()
    decision["runtime_approval"]["decision"] = "rejected"

    with pytest.raises(ValueError, match="Runtime approval report requires a valid approval decision"):
        RuntimeApprovalReportWriter(ArtifactStore(tmp_path)).write_approval(decision)


def test_runtime_approval_report_artifact_matches_json_schema(tmp_path) -> None:
    schema = _schema("runtime-approval-report.schema.json")

    validate(instance=_approval_report_artifact(tmp_path), schema=schema)


def test_runtime_approval_report_artifact_schema_rejects_wrong_role(tmp_path) -> None:
    schema = _schema("runtime-approval-report.schema.json")
    artifact = _approval_report_artifact(tmp_path)
    artifact["metadata"]["artifact_role"] = "runtime_report"

    with pytest.raises(ValidationError):
        validate(instance=artifact, schema=schema)


def test_runtime_approval_report_artifact_schema_rejects_unknown_decision(tmp_path) -> None:
    schema = _schema("runtime-approval-report.schema.json")
    artifact = _approval_report_artifact(tmp_path)
    artifact["metadata"]["decision"] = "unknown"

    with pytest.raises(ValidationError):
        validate(instance=artifact, schema=schema)


def test_runtime_approval_policy_verifier_accepts_valid_policy() -> None:
    verification = verify_runtime_approval_policy(_approval_policy())

    assert verification.successful()


def test_runtime_approval_policy_requires_header_fields() -> None:
    policy = _approval_policy()
    policy["runtime_approval_policy"].pop("name")
    policy["runtime_approval_policy"].pop("version")

    verification = verify_runtime_approval_policy(policy)

    assert not verification.successful()
    assert "Runtime approval policy requires name." in verification.issues
    assert "Runtime approval policy requires version." in verification.issues


def test_runtime_approval_policy_requires_all_evidence_artifact_roles() -> None:
    policy = _approval_policy()
    policy["required_evidence_artifacts"].remove("runtime_trace_report")

    verification = verify_runtime_approval_policy(policy)

    assert not verification.successful()
    assert "Runtime approval policy must require all Runtime evidence artifact roles." in verification.issues


def test_runtime_approval_policy_rejects_unknown_allowed_decision() -> None:
    policy = _approval_policy()
    policy["allowed_decisions"].append("unknown")

    verification = verify_runtime_approval_policy(policy)

    assert not verification.successful()
    assert "Runtime approval policy allowed_decisions must contain only supported decisions." in verification.issues


def test_runtime_approval_policy_rejects_unknown_check_status() -> None:
    policy = _approval_policy()
    policy["allowed_check_statuses"].append("unknown")

    verification = verify_runtime_approval_policy(policy)

    assert not verification.successful()
    assert "Runtime approval policy allowed_check_statuses must contain only supported check statuses." in verification.issues


def test_runtime_approval_policy_requires_rule_booleans() -> None:
    policy = _approval_policy()
    policy["waiver_rules"]["requires_note_or_waived_check"] = False
    policy["rejection_rules"].pop("requires_note_or_failed_check")

    verification = verify_runtime_approval_policy(policy)

    assert not verification.successful()
    assert "Runtime approval policy waiver_rules.requires_note_or_waived_check must be true." in verification.issues
    assert "Runtime approval policy rejection_rules.requires_note_or_failed_check must be true." in verification.issues


def test_runtime_approval_policy_verifier_does_not_mutate_payload() -> None:
    policy = _approval_policy()
    original = deepcopy(policy)

    verify_runtime_approval_policy(policy)

    assert policy == original


def test_runtime_approval_policy_matches_json_schema() -> None:
    schema = _schema("runtime-approval-policy.schema.json")

    validate(instance=_approval_policy(), schema=schema)


def test_runtime_approval_policy_schema_rejects_missing_evidence_artifact_role() -> None:
    schema = _schema("runtime-approval-policy.schema.json")
    policy = _approval_policy()
    policy["required_evidence_artifacts"].remove("runtime_trace_report")

    with pytest.raises(ValidationError):
        validate(instance=policy, schema=schema)


def test_runtime_approval_policy_schema_rejects_unknown_allowed_decision() -> None:
    schema = _schema("runtime-approval-policy.schema.json")
    policy = _approval_policy()
    policy["allowed_decisions"].append("unknown")

    with pytest.raises(ValidationError):
        validate(instance=policy, schema=schema)


def test_runtime_approval_policy_schema_rejects_false_waiver_rule() -> None:
    schema = _schema("runtime-approval-policy.schema.json")
    policy = _approval_policy()
    policy["waiver_rules"]["requires_note_or_waived_check"] = False

    with pytest.raises(ValidationError):
        validate(instance=policy, schema=schema)
