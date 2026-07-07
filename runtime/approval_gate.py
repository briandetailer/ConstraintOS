from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime.approval import verify_runtime_approval_decision, verify_runtime_approval_policy
from runtime.artifacts.evidence import verify_runtime_evidence_manifest


def create_runtime_approval_decision(
    evidence_manifest_artifact: dict[str, Any],
    policy: dict[str, Any],
    decided_by: str,
    decided_at: str,
) -> dict[str, Any]:
    """Create an approval decision from evidence and policy without mutating either input."""
    if not isinstance(evidence_manifest_artifact, dict):
        raise ValueError("Runtime approval requires an evidence manifest artifact dictionary.")
    if not decided_by:
        raise ValueError("Runtime approval requires decided_by.")
    if not decided_at:
        raise ValueError("Runtime approval requires decided_at.")

    evidence_manifest_artifact_id = str(evidence_manifest_artifact.get("id", ""))
    if not evidence_manifest_artifact_id:
        raise ValueError("Runtime approval requires evidence manifest artifact id.")

    manifest_payload = _manifest_payload(evidence_manifest_artifact)
    runtime_id = _runtime_id(manifest_payload)
    policy_name = _policy_name(policy)

    evidence_verification = verify_runtime_evidence_manifest(evidence_manifest_artifact)
    policy_verification = verify_runtime_approval_policy(policy)
    evidence_successful = evidence_verification.successful()
    policy_successful = policy_verification.successful()

    checks = [
        {
            "id": "APPROVAL-CHECK-0001",
            "name": "runtime evidence manifest verified",
            "status": "passed" if evidence_successful else "failed",
            "source": "verify_runtime_evidence_manifest",
            "message": "Evidence manifest verification passed."
            if evidence_successful
            else "Evidence manifest verification failed.",
            "metadata": {"issue_count": len(evidence_verification.issues)},
        },
        {
            "id": "APPROVAL-CHECK-0002",
            "name": "runtime approval policy verified",
            "status": "passed" if policy_successful else "failed",
            "source": "verify_runtime_approval_policy",
            "message": "Approval policy verification passed."
            if policy_successful
            else "Approval policy verification failed.",
            "metadata": {"issue_count": len(policy_verification.issues)},
        },
    ]
    issues = [*evidence_verification.issues, *policy_verification.issues]
    decision = {
        "runtime_approval": {
            "runtime_id": runtime_id,
            "evidence_manifest_artifact_id": evidence_manifest_artifact_id,
            "decision": "approved" if evidence_successful and policy_successful else "rejected",
            "decided_by": decided_by,
            "decided_at": decided_at,
            "approval_policy": policy_name,
        },
        "checks": checks,
        "notes": issues,
    }
    approval_verification = verify_runtime_approval_decision(decision)
    if not approval_verification.successful():
        raise ValueError("Generated runtime approval decision is invalid.")
    return decision


def _manifest_payload(evidence_manifest_artifact: dict[str, Any]) -> dict[str, Any]:
    if "runtime_evidence" in evidence_manifest_artifact:
        return evidence_manifest_artifact
    metadata = _dict_value(evidence_manifest_artifact, "metadata")
    path = metadata.get("path")
    if isinstance(path, str) and path:
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
        return payload if isinstance(payload, dict) else {}
    return {}


def _runtime_id(manifest_payload: dict[str, Any]) -> str:
    evidence = _dict_value(manifest_payload, "runtime_evidence")
    runtime_id = evidence.get("runtime_id")
    return str(runtime_id) if runtime_id else "RUNTIME-UNKNOWN"


def _policy_name(policy: dict[str, Any]) -> str:
    header = _dict_value(policy, "runtime_approval_policy")
    name = header.get("name")
    return str(name) if name else "unknown-runtime-approval-policy"


def _dict_value(value: dict[str, Any], key: str) -> dict[str, Any]:
    payload = value.get(key, {}) if isinstance(value, dict) else {}
    return payload if isinstance(payload, dict) else {}
