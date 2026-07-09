from __future__ import annotations

from pathlib import Path
from typing import Any

from constraintos.candidate_intake_manifests import load_candidate_intake_manifest_report


class CandidateIntakeReviewPacketError(ValueError):
    """Raised when a fixture-only candidate intake review packet is unsafe."""


def require_intake_review_is_safe(summary: dict[str, Any]) -> None:
    if summary.get("approval_allowed") is not False:
        raise CandidateIntakeReviewPacketError("Candidate intake review packets must not allow approval")
    if summary.get("image_bytes_loaded") is not False:
        raise CandidateIntakeReviewPacketError("Candidate intake review packets must not load image bytes")
    if summary.get("image_decoded") is not False:
        raise CandidateIntakeReviewPacketError("Candidate intake review packets must not decode images")
    if summary.get("candidate_scoring_ran") is not False:
        raise CandidateIntakeReviewPacketError("Candidate intake review packets must not score candidates")
    if summary.get("source_report_mutation_ran") is not False:
        raise CandidateIntakeReviewPacketError("Candidate intake review packets must not mutate reports")


def build_intake_review_sections(report: dict[str, Any]) -> dict[str, Any]:
    summary = report["summary"]
    manifest = report["candidate_intake_manifest"]
    candidate_reference = manifest.get("candidate_reference", {})
    policy = manifest.get("intake_policy_snapshot", {})
    boundary = manifest.get("intake_boundary", {})
    approval = manifest.get("approval_expectation", {})
    return {
        "candidate_identity": {
            "candidate_intake_manifest_key": summary.get("key"),
            "candidate_intake_manifest_id": summary.get("id"),
            "candidate_id": summary.get("candidate_id"),
            "contract_key": summary.get("contract_key"),
            "source_contract_id": summary.get("source_contract_id"),
            "intake_state": summary.get("intake_state"),
        },
        "reference_metadata": {
            "reference_type": summary.get("reference_type"),
            "reference": summary.get("reference"),
            "reference_status": summary.get("reference_status"),
            "media_type": summary.get("media_type"),
            "image_sha256": summary.get("image_sha256"),
            "expected_byte_count": summary.get("expected_byte_count"),
        },
        "policy_snapshot": {
            "accepted_reference_types": policy.get("accepted_reference_types") if isinstance(policy, dict) else None,
            "accepted_media_types": policy.get("accepted_media_types") if isinstance(policy, dict) else None,
            "forbidden_reference_behaviors": policy.get("forbidden_reference_behaviors") if isinstance(policy, dict) else None,
            "network_fetch_allowed": summary.get("network_fetch_allowed"),
            "successful_intake_can_approve": summary.get("successful_intake_can_approve"),
        },
        "intake_boundaries": {
            "image_bytes_loaded": boundary.get("image_bytes_loaded") if isinstance(boundary, dict) else None,
            "image_decoded": boundary.get("image_decoded") if isinstance(boundary, dict) else None,
            "pixel_inspection_ran": boundary.get("pixel_inspection_ran") if isinstance(boundary, dict) else None,
            "computer_vision_ran": boundary.get("computer_vision_ran") if isinstance(boundary, dict) else None,
            "ocr_ran": boundary.get("ocr_ran") if isinstance(boundary, dict) else None,
            "candidate_scoring_ran": boundary.get("candidate_scoring_ran") if isinstance(boundary, dict) else None,
            "source_report_mutation_ran": boundary.get("source_report_mutation_ran") if isinstance(boundary, dict) else None,
            "approval_automation_ran": boundary.get("approval_automation_ran") if isinstance(boundary, dict) else None,
        },
        "decision_guardrails": {
            "initial_decision": summary.get("initial_decision"),
            "uncertainty_default": summary.get("uncertainty_default"),
            "approval_allowed": summary.get("approval_allowed"),
            "guardrail": approval.get("guardrail") if isinstance(approval, dict) else None,
            "approval_blockers": [
                "intake review packet is fixture-only",
                "image bytes have not been loaded",
                "image decoding has not run",
                "pixel inspection has not run",
                "candidate scoring has not run",
                "approval automation has not run",
            ],
        },
    }


def build_candidate_intake_review_packet_payload(reference: str, candidate_dir: Path) -> dict[str, Any]:
    report = load_candidate_intake_manifest_report(reference, candidate_dir)
    summary = report["summary"]
    require_intake_review_is_safe(summary)
    sections = build_intake_review_sections(report)
    return {
        "candidate_intake_review_packet": {
            "mode": "fixture_only",
            "candidate_dir": str(candidate_dir),
            "selected_intake_manifest": summary.get("key"),
            "image_bytes_loaded": "not_run",
            "image_decoding": "not_run",
            "network_fetch": "not_run",
            "pixel_inspection": "not_run",
            "computer_vision": "not_run",
            "ocr": "not_run",
            "candidate_scoring": "not_run",
            "source_report_mutation": "not_run",
            "approval_automation": "not_run",
        },
        "summary": {
            "candidate_intake_manifest_key": summary.get("key"),
            "candidate_intake_manifest_id": summary.get("id"),
            "candidate_id": summary.get("candidate_id"),
            "contract_key": summary.get("contract_key"),
            "intake_state": summary.get("intake_state"),
            "reference_type": summary.get("reference_type"),
            "reference_status": summary.get("reference_status"),
            "media_type": summary.get("media_type"),
            "network_fetch_allowed": summary.get("network_fetch_allowed"),
            "successful_intake_can_approve": summary.get("successful_intake_can_approve"),
            "initial_decision": summary.get("initial_decision"),
            "uncertainty_default": summary.get("uncertainty_default"),
            "approval_allowed": summary.get("approval_allowed"),
            "intake_review_packet_ready": True,
        },
        "review_sections": sections,
        "candidate_intake_manifest_report": report,
    }
