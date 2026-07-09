from __future__ import annotations

from pathlib import Path
from typing import Any

from constraintos.candidate_evaluation import build_fixture_only_candidate_evaluation
from constraintos.manual_observations import build_manual_observation_payload


class ObservationReportBindingError(ValueError):
    """Raised when fixture-only observation/report binding is unsafe."""


def require_same_value(field: str, left: Any, right: Any, *, left_name: str, right_name: str) -> None:
    if left != right:
        raise ObservationReportBindingError(
            f"Observation/report binding mismatch for {field}: {left_name}={left!r}; {right_name}={right!r}"
        )


def build_observation_report_binding_payload(reference: str, candidate_dir: Path) -> dict[str, Any]:
    observation_payload = build_manual_observation_payload(reference, candidate_dir)
    evaluation_payload = build_fixture_only_candidate_evaluation(reference, candidate_dir)
    observation_summary = observation_payload["summary"]
    evaluation_summary = evaluation_payload["summary"]

    for field in ["candidate_manifest_key", "candidate_id", "contract_key", "candidate_reference_status"]:
        require_same_value(
            field,
            observation_summary.get(field),
            evaluation_summary.get(field),
            left_name="manual_observation",
            right_name="candidate_evaluation_report",
        )

    require_same_value(
        "recommended_decision",
        observation_summary.get("recommended_decision"),
        evaluation_summary.get("recommended_decision"),
        left_name="manual_observation",
        right_name="candidate_evaluation_report",
    )
    require_same_value(
        "approval_allowed",
        observation_summary.get("approval_allowed"),
        evaluation_summary.get("approval_allowed"),
        left_name="manual_observation",
        right_name="candidate_evaluation_report",
    )

    if observation_summary.get("recommended_decision") != "needs_review":
        raise ObservationReportBindingError("Observation/report binding must recommend needs_review")
    if observation_summary.get("approval_allowed") is not False:
        raise ObservationReportBindingError("Observation/report binding must not allow approval")

    return {
        "observation_report_binding": {
            "mode": "fixture_only",
            "candidate_dir": str(candidate_dir),
            "selected_manifest": observation_summary.get("candidate_manifest_key"),
            "selected_observation": observation_summary.get("observation_key"),
            "selected_report": evaluation_summary.get("report_key"),
            "real_image_ingestion": "not_run",
            "computer_vision": "not_run",
            "ocr": "not_run",
            "image_generation": "not_run",
            "approval_automation": "not_run",
            "candidate_scoring": "not_run",
        },
        "summary": {
            "candidate_manifest_key": observation_summary.get("candidate_manifest_key"),
            "candidate_id": observation_summary.get("candidate_id"),
            "contract_key": observation_summary.get("contract_key"),
            "candidate_reference_status": observation_summary.get("candidate_reference_status"),
            "observation_key": observation_summary.get("observation_key"),
            "observation_mode": observation_summary.get("observation_mode"),
            "observation_source_type": observation_summary.get("source_type"),
            "overall_observation_status": observation_summary.get("overall_observation_status"),
            "observation_not_observed_count": observation_summary.get("not_observed_count"),
            "report_key": evaluation_summary.get("report_key"),
            "report_mode": evaluation_summary.get("report_mode"),
            "overall_evidence_status": evaluation_summary.get("overall_evidence_status"),
            "report_not_observed_count": evaluation_summary.get("not_observed_count"),
            "recommended_decision": observation_summary.get("recommended_decision"),
            "uncertainty_default": observation_summary.get("uncertainty_default"),
            "approval_allowed": observation_summary.get("approval_allowed"),
        },
        "manual_observation": observation_payload,
        "candidate_evaluation": evaluation_payload,
    }
