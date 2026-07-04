from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass
class ReviewItem:
    constraint_id: str
    statement: str
    severity: str
    acceptance: str
    validation_method: str
    reviewer_result: str = "unreviewed"
    reviewer_confidence: float = 0.0
    evidence: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


def create_review_checklist(spec: dict[str, Any], checklist_id: str) -> dict[str, Any]:
    artifact = spec.get("artifact", {})
    items: list[ReviewItem] = []
    for constraint in spec.get("constraints", []) or []:
        items.append(
            ReviewItem(
                constraint_id=str(constraint.get("id", "UNKNOWN")),
                statement=str(constraint.get("statement", "")),
                severity=str(constraint.get("severity", "major")),
                acceptance=str(constraint.get("acceptance", "")),
                validation_method=str(constraint.get("validation_method", "review")),
            )
        )
    return {
        "review_checklist": {
            "id": checklist_id,
            "artifact_id": artifact.get("id", "UNKNOWN"),
            "artifact_version": artifact.get("version", "0.1"),
            "created": date.today().isoformat(),
            "status": "open",
        },
        "items": [item.to_dict() for item in items],
        "summary": {
            "total": len(items),
            "reviewed": 0,
            "pass": 0,
            "fail": 0,
            "uncertain": 0,
        },
    }


def summarize_review(checklist: dict[str, Any]) -> dict[str, Any]:
    items = checklist.get("items", []) or []
    reviewed = [item for item in items if item.get("reviewer_result") != "unreviewed"]
    summary = {
        "total": len(items),
        "reviewed": len(reviewed),
        "pass": sum(1 for item in items if item.get("reviewer_result") == "pass"),
        "fail": sum(1 for item in items if item.get("reviewer_result") == "fail"),
        "uncertain": sum(1 for item in items if item.get("reviewer_result") == "uncertain"),
    }
    updated = dict(checklist)
    updated["summary"] = summary
    if summary["reviewed"] == summary["total"] and summary["fail"] == 0 and summary["uncertain"] == 0:
        updated["review_checklist"] = dict(updated.get("review_checklist", {}), status="complete")
    return updated


def review_gate_status(checklist: dict[str, Any]) -> dict[str, Any]:
    summary = summarize_review(checklist).get("summary", {})
    blockers = [item for item in checklist.get("items", []) or [] if item.get("severity") == "blocker" and item.get("reviewer_result") in {"fail", "uncertain", "unreviewed"}]
    if blockers:
        return {"gate": "blocked", "reason": "blocker constraints are failed, uncertain, or unreviewed", "blocked_items": [item.get("constraint_id") for item in blockers]}
    if summary.get("reviewed") != summary.get("total"):
        return {"gate": "blocked", "reason": "review incomplete", "blocked_items": []}
    if summary.get("fail", 0) > 0 or summary.get("uncertain", 0) > 0:
        return {"gate": "escalate", "reason": "review contains failures or uncertainty", "blocked_items": []}
    return {"gate": "pass", "reason": "review complete with no failed or uncertain results", "blocked_items": []}
