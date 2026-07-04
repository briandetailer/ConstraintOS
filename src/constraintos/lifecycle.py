from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

VALID_STATES = ["draft", "compiled", "rendered", "validated", "approved", "published", "archived", "rejected"]

ALLOWED_TRANSITIONS = {
    "draft": {"compiled", "rejected"},
    "compiled": {"rendered", "draft", "rejected"},
    "rendered": {"validated", "compiled", "rejected"},
    "validated": {"approved", "rejected", "rendered"},
    "approved": {"published", "archived"},
    "published": {"archived"},
    "archived": set(),
    "rejected": {"draft", "archived"},
}


@dataclass
class LifecycleError(Exception):
    message: str


def create_manifest(manifest_id: str, artifact_id: str, artifact_type: str, title: str) -> dict[str, Any]:
    return {
        "manifest": {"id": manifest_id, "version": "0.1", "created": date.today().isoformat()},
        "artifact": {"id": artifact_id, "type": artifact_type, "title": title},
        "state": "draft",
        "history": [{"from": "none", "to": "draft", "date": date.today().isoformat(), "reason": "manifest created"}],
        "outputs": [],
        "approvals": [],
    }


def transition_manifest(manifest: dict[str, Any], target_state: str, reason: str) -> dict[str, Any]:
    current = manifest.get("state")
    if current not in VALID_STATES:
        raise LifecycleError(f"Invalid current state: {current}")
    if target_state not in VALID_STATES:
        raise LifecycleError(f"Invalid target state: {target_state}")
    if target_state not in ALLOWED_TRANSITIONS[current]:
        raise LifecycleError(f"Transition not allowed: {current} -> {target_state}")
    updated = dict(manifest)
    updated["state"] = target_state
    history = list(updated.get("history", []))
    history.append({"from": current, "to": target_state, "date": date.today().isoformat(), "reason": reason})
    updated["history"] = history
    return updated


def create_approval_record(approval_id: str, artifact_id: str, artifact_version: str, compliance_report_id: str, approver: str, status: str, summary: str, notes: list[str] | None = None) -> dict[str, Any]:
    if status not in {"approved", "rejected", "exception"}:
        raise LifecycleError(f"Invalid approval status: {status}")
    return {
        "approval": {"id": approval_id, "created": date.today().isoformat(), "approver": approver, "status": status},
        "artifact": {"id": artifact_id, "version": artifact_version, "compliance_report_id": compliance_report_id},
        "decision": {"summary": summary, "notes": notes or []},
    }
