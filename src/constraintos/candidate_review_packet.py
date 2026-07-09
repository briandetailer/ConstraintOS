from __future__ import annotations

from pathlib import Path
from typing import Any

from constraintos.observation_evidence_merge import build_observation_evidence_merge_payload


class CandidateReviewPacketError(ValueError):
    """Raised when a fixture-only candidate review packet is unsafe."""


def require_needs_review(summary: dict[str, Any]) -> None:
    if summary.get("recommended_decision") != "needs_review":
        raise CandidateReviewPacketError("Candidate review packets must recommend needs_review")
    if summary.get("approval_allowed") is not False:
        raise CandidateReviewPacketError("Candidate review packets must not allow approval")


def build_candidate_review_sections(merge_payload: dict[str, Any]) -> dict[str, Any]:
    merge_summary = merge_payload["summary"]
    binding_payload = merge_payload["observation_report_binding"]
    manual_summary = binding_payload["manual_observation"]["summary"]
    evaluation_summary = binding_payload["candidate_evaluation"]["summary"]
    candidate_manifest = binding_payload["candidate_evaluation"]["candidate_manifest"]
    manifest = candidate_manifest.get("candidate_manifest", {})
    subject = candidate_manifest.get("subject", {})
    candidate = candidate_manifest.get("candidate", {})
    return {
        "candidate_identity": {
            "candidate_manifest_key": merge_summary.get("candidate_manifest_key"),
            "candidate_manifest_id": manifest.get("id"),
            "candidate_id": merge_summary.get("candidate_id"),
            "contract_key": merge_summary.get("contract_key"),
            "subject_name": subject.get("name"),
            "candidate_reference_status": merge_summary.get("candidate_reference_status"),
            "candidate_source_type": candidate.get("source_type"),
            "generated_by_constraintos": candidate.get("generated_by_constraintos"),
        },
        "manual_observations": {
            "observation_key": merge_summary.get("observation_key"),
            "observation_source_type": manual_summary.get("source_type"),
            "total_observations": manual_summary.get("total_observations"),
            "not_observed_count": manual_summary.get("not_observed_count"),
            "overall_observation_status": manual_summary.get("overall_observation_status"),
        },
        "candidate_evaluation_report": {
            "report_key": merge_summary.get("report_key"),
            "report_mode": evaluation_summary.get("report_mode"),
            "overall_evidence_status": evaluation_summary.get("overall_evidence_status"),
            "not_observed_count": evaluation_summary.get("not_observed_count"),
            "recommended_decision": evaluation_summary.get("recommended_decision"),
        },
        "merged_evidence": {
            "merged_evidence_count": merge_summary.get("merged_evidence_count"),
            "matched_constraint_count": merge_summary.get("matched_constraint_count"),
            "manual_only_constraint_count": merge_summary.get("manual_only_constraint_count"),
            "report_only_constraint_count": merge_summary.get("report_only_constraint_count"),
            "overall_merged_evidence_status": merge_summary.get("overall_merged_evidence_status"),
        },
        "decision_guardrails": {
            "recommended_decision": merge_summary.get("recommended_decision"),
            "approval_allowed": merge_summary.get("approval_allowed"),
            "approval_blockers": [
                "candidate_reference_status is reference_only_not_loaded",
                "real image ingestion has not run",
                "computer vision has not run",
                "manual observations cannot approve alone",
                "merged evidence cannot approve candidates",
                "candidate scoring has not run",
            ],
        },
    }


def build_candidate_review_packet_payload(reference: str, candidate_dir: Path) -> dict[str, Any]:
    merge_payload = build_observation_evidence_merge_payload(reference, candidate_dir)
    merge_summary = merge_payload["summary"]
    require_needs_review(merge_summary)
    sections = build_candidate_review_sections(merge_payload)
    return {
        "candidate_review_packet": {
            "mode": "fixture_only",
            "candidate_dir": str(candidate_dir),
            "selected_manifest": merge_summary.get("candidate_manifest_key"),
            "selected_observation": merge_summary.get("observation_key"),
            "selected_report": merge_summary.get("report_key"),
            "real_image_ingestion": "not_run",
            "computer_vision": "not_run",
            "ocr": "not_run",
            "image_generation": "not_run",
            "approval_automation": "not_run",
            "candidate_scoring": "not_run",
            "source_report_mutation": "not_run",
        },
        "summary": {
            "candidate_manifest_key": merge_summary.get("candidate_manifest_key"),
            "candidate_id": merge_summary.get("candidate_id"),
            "contract_key": merge_summary.get("contract_key"),
            "candidate_reference_status": merge_summary.get("candidate_reference_status"),
            "merged_evidence_count": merge_summary.get("merged_evidence_count"),
            "matched_constraint_count": merge_summary.get("matched_constraint_count"),
            "report_only_constraint_count": merge_summary.get("report_only_constraint_count"),
            "manual_only_constraint_count": merge_summary.get("manual_only_constraint_count"),
            "overall_merged_evidence_status": merge_summary.get("overall_merged_evidence_status"),
            "recommended_decision": merge_summary.get("recommended_decision"),
            "approval_allowed": merge_summary.get("approval_allowed"),
            "review_packet_ready": True,
        },
        "review_sections": sections,
        "observation_evidence_merge": merge_payload,
    }
