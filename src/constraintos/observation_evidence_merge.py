from __future__ import annotations

from pathlib import Path
from typing import Any

from constraintos.observation_report_binding import build_observation_report_binding_payload


class ObservationEvidenceMergeError(ValueError):
    """Raised when fixture-only observation/evidence merge is unsafe."""


def index_by_constraint_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for item in items:
        constraint_id = item.get("constraint_id")
        if not isinstance(constraint_id, str) or not constraint_id:
            raise ObservationEvidenceMergeError("Every merge item must include a non-empty constraint_id")
        if constraint_id in indexed:
            raise ObservationEvidenceMergeError(f"Duplicate constraint_id in merge inputs: {constraint_id}")
        indexed[constraint_id] = item
    return indexed


def merge_status(manual_status: str | None, report_status: str | None) -> str:
    statuses = {manual_status, report_status}
    if "contradicted" in statuses:
        return "contradicted"
    if "missing" in statuses:
        return "missing"
    if "ambiguous" in statuses:
        return "ambiguous"
    if statuses == {"satisfied"}:
        return "satisfied"
    return "not_observed"


def build_merged_evidence_items(manual_items: list[dict[str, Any]], report_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    manual_by_constraint = index_by_constraint_id(manual_items)
    report_by_constraint = index_by_constraint_id(report_items)
    constraint_ids = sorted(set(manual_by_constraint) | set(report_by_constraint))
    merged: list[dict[str, Any]] = []
    for constraint_id in constraint_ids:
        manual = manual_by_constraint.get(constraint_id)
        report = report_by_constraint.get(constraint_id)
        manual_status = manual.get("observed_status") if isinstance(manual, dict) else None
        report_status = report.get("observed_status") if isinstance(report, dict) else None
        merged.append({
            "constraint_id": constraint_id,
            "constraint_group": (
                (manual or {}).get("constraint_group")
                or (report or {}).get("constraint_group")
                or "unknown"
            ),
            "manual_observation_status": manual_status or "not_present",
            "report_evidence_status": report_status or "not_present",
            "merged_status": merge_status(manual_status, report_status),
            "manual_observation_present": manual is not None,
            "report_evidence_present": report is not None,
            "manual_observation_id": (manual or {}).get("observation_id"),
            "report_claim": (report or {}).get("claim"),
            "manual_claim": (manual or {}).get("claim"),
            "merge_source": "fixture_only_manual_observation_and_report_evidence",
        })
    return merged


def summarize_merged_evidence(merged_items: list[dict[str, Any]], manual_count: int, report_count: int) -> dict[str, Any]:
    matched_count = sum(1 for item in merged_items if item["manual_observation_present"] and item["report_evidence_present"])
    manual_only_count = sum(1 for item in merged_items if item["manual_observation_present"] and not item["report_evidence_present"])
    report_only_count = sum(1 for item in merged_items if item["report_evidence_present"] and not item["manual_observation_present"])
    not_observed_count = sum(1 for item in merged_items if item["merged_status"] == "not_observed")
    return {
        "manual_observation_count": manual_count,
        "report_evidence_count": report_count,
        "merged_evidence_count": len(merged_items),
        "matched_constraint_count": matched_count,
        "manual_only_constraint_count": manual_only_count,
        "report_only_constraint_count": report_only_count,
        "not_observed_count": not_observed_count,
        "overall_merged_evidence_status": "not_observed" if not_observed_count else "needs_review",
        "recommended_decision": "needs_review",
        "approval_allowed": False,
    }


def build_observation_evidence_merge_payload(reference: str, candidate_dir: Path) -> dict[str, Any]:
    binding_payload = build_observation_report_binding_payload(reference, candidate_dir)
    manual_fixture = binding_payload["manual_observation"]["manual_observation_fixture"]
    evaluation_report = binding_payload["candidate_evaluation"]["evaluation_report"]
    manual_items = manual_fixture.get("observations", [])
    report_items = evaluation_report.get("evidence_items", [])
    if not isinstance(manual_items, list) or not isinstance(report_items, list):
        raise ObservationEvidenceMergeError("Manual observations and report evidence must both be lists")
    merged_items = build_merged_evidence_items(manual_items, report_items)
    merge_summary = summarize_merged_evidence(merged_items, len(manual_items), len(report_items))
    if merge_summary["recommended_decision"] != "needs_review":
        raise ObservationEvidenceMergeError("Merged evidence must recommend needs_review")
    if merge_summary["approval_allowed"] is not False:
        raise ObservationEvidenceMergeError("Merged evidence must not allow approval")
    binding_summary = binding_payload["summary"]
    return {
        "observation_evidence_merge": {
            "mode": "fixture_only",
            "candidate_dir": str(candidate_dir),
            "selected_manifest": binding_summary.get("candidate_manifest_key"),
            "selected_observation": binding_summary.get("observation_key"),
            "selected_report": binding_summary.get("report_key"),
            "real_image_ingestion": "not_run",
            "computer_vision": "not_run",
            "ocr": "not_run",
            "image_generation": "not_run",
            "approval_automation": "not_run",
            "candidate_scoring": "not_run",
            "source_report_mutation": "not_run",
        },
        "summary": {
            "candidate_manifest_key": binding_summary.get("candidate_manifest_key"),
            "candidate_id": binding_summary.get("candidate_id"),
            "contract_key": binding_summary.get("contract_key"),
            "candidate_reference_status": binding_summary.get("candidate_reference_status"),
            "observation_key": binding_summary.get("observation_key"),
            "report_key": binding_summary.get("report_key"),
            **merge_summary,
        },
        "merged_evidence_items": merged_items,
        "observation_report_binding": binding_payload,
    }
