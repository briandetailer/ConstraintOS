from __future__ import annotations

from pathlib import Path
from typing import Any

from constraintos.candidate_image_byte_loading_records import load_candidate_image_byte_loading_record_report


class CandidateImageByteLoadingReviewPacketError(ValueError):
    """Raised when a fixture-only candidate image byte-loading review packet is unsafe."""


def require_byte_loading_review_is_safe(summary: dict[str, Any]) -> None:
    unsafe_expectations = {
        "image_bytes_loaded": False,
        "local_file_opened": False,
        "artifact_downloaded": False,
        "network_fetch_ran": False,
        "image_decoded": False,
        "candidate_scoring_ran": False,
        "source_report_mutation_ran": False,
        "approval_automation_ran": False,
        "approval_allowed": False,
    }
    for field, expected in unsafe_expectations.items():
        if summary.get(field) is not expected:
            raise CandidateImageByteLoadingReviewPacketError(
                f"Candidate image byte-loading review packets require {field} to be {expected!r}"
            )
    if summary.get("byte_loading_success_can_approve") is not False:
        raise CandidateImageByteLoadingReviewPacketError("Byte-loading success must not allow approval")


def build_byte_loading_review_sections(report: dict[str, Any]) -> dict[str, Any]:
    summary = report["summary"]
    record = report["candidate_image_byte_loading_record"]
    result = record.get("byte_loading_result", {})
    boundary = record.get("post_load_boundary", {})
    approval = record.get("approval_expectation", {})
    return {
        "byte_loading_record_identity": {
            "record_key": summary.get("key"),
            "record_id": summary.get("id"),
            "candidate_id": summary.get("candidate_id"),
            "status": summary.get("status"),
            "byte_loading_state": summary.get("byte_loading_state"),
        },
        "intake_manifest_binding": {
            "contract_key": summary.get("contract_key"),
            "source_contract_id": summary.get("source_contract_id"),
            "candidate_intake_manifest_id": summary.get("candidate_intake_manifest_id"),
        },
        "reference_metadata": {
            "reference_type": summary.get("reference_type"),
            "reference": summary.get("reference"),
            "media_type": summary.get("media_type"),
            "image_sha256": summary.get("image_sha256"),
            "expected_byte_count": summary.get("expected_byte_count"),
        },
        "byte_loading_policy_snapshot": {
            "max_candidate_image_bytes": summary.get("max_candidate_image_bytes"),
            "network_fetch_allowed": summary.get("network_fetch_allowed"),
            "implicit_cloud_download_allowed": summary.get("implicit_cloud_download_allowed"),
            "byte_loading_success_can_approve": summary.get("byte_loading_success_can_approve"),
        },
        "byte_loading_result": {
            "image_bytes_loaded": result.get("image_bytes_loaded") if isinstance(result, dict) else None,
            "local_file_opened": result.get("local_file_opened") if isinstance(result, dict) else None,
            "artifact_downloaded": result.get("artifact_downloaded") if isinstance(result, dict) else None,
            "network_fetch_ran": result.get("network_fetch_ran") if isinstance(result, dict) else None,
            "actual_loaded_byte_count": result.get("actual_loaded_byte_count") if isinstance(result, dict) else None,
            "computed_sha256": result.get("computed_sha256") if isinstance(result, dict) else None,
            "sniffed_media_type": result.get("sniffed_media_type") if isinstance(result, dict) else None,
            "checksum_matches": result.get("checksum_matches") if isinstance(result, dict) else None,
            "media_type_matches": result.get("media_type_matches") if isinstance(result, dict) else None,
        },
        "post_load_boundaries": {
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
                "byte-loading review packet is fixture-only",
                "image bytes have not been loaded",
                "local files have not been opened",
                "artifacts have not been downloaded",
                "network fetch has not run",
                "image decoding has not run",
                "candidate scoring has not run",
                "approval automation has not run",
            ],
        },
    }


def build_candidate_image_byte_loading_review_packet_payload(reference: str, candidate_dir: Path) -> dict[str, Any]:
    report = load_candidate_image_byte_loading_record_report(reference, candidate_dir)
    summary = report["summary"]
    require_byte_loading_review_is_safe(summary)
    sections = build_byte_loading_review_sections(report)
    return {
        "candidate_image_byte_loading_review_packet": {
            "mode": "fixture_only",
            "candidate_dir": str(candidate_dir),
            "selected_byte_loading_record": summary.get("key"),
            "image_bytes_loaded": "not_run",
            "local_file_opening": "not_run",
            "artifact_download": "not_run",
            "network_fetch": "not_run",
            "image_decoding": "not_run",
            "pixel_inspection": "not_run",
            "computer_vision": "not_run",
            "ocr": "not_run",
            "candidate_scoring": "not_run",
            "source_report_mutation": "not_run",
            "approval_automation": "not_run",
        },
        "summary": {
            "byte_loading_record_key": summary.get("key"),
            "byte_loading_record_id": summary.get("id"),
            "candidate_id": summary.get("candidate_id"),
            "contract_key": summary.get("contract_key"),
            "candidate_intake_manifest_id": summary.get("candidate_intake_manifest_id"),
            "byte_loading_state": summary.get("byte_loading_state"),
            "reference_type": summary.get("reference_type"),
            "media_type": summary.get("media_type"),
            "image_bytes_loaded": summary.get("image_bytes_loaded"),
            "local_file_opened": summary.get("local_file_opened"),
            "artifact_downloaded": summary.get("artifact_downloaded"),
            "network_fetch_ran": summary.get("network_fetch_ran"),
            "image_decoded": summary.get("image_decoded"),
            "candidate_scoring_ran": summary.get("candidate_scoring_ran"),
            "initial_decision": summary.get("initial_decision"),
            "uncertainty_default": summary.get("uncertainty_default"),
            "approval_allowed": summary.get("approval_allowed"),
            "byte_loading_review_packet_ready": True,
        },
        "review_sections": sections,
        "candidate_image_byte_loading_record_report": report,
    }
