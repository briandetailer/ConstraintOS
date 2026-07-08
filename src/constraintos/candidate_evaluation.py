from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from constraintos.candidate_manifests import (
    CandidateManifestError,
    candidate_manifest_key,
    load_candidate_manifest_report,
    load_json,
)

CANDIDATE_EVALUATION_REPORT_SCHEMA_NAME = "candidate_evaluation_report.schema.json"
CANDIDATE_EVALUATION_REPORT_SUFFIX = "_candidate_evaluation_report.fixture.json"


class CandidateEvaluationError(ValueError):
    """Raised when fixture-only candidate evaluation cannot be produced safely."""


def validate_candidate_evaluation_report_schema(report: dict[str, Any], schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(report), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise CandidateEvaluationError(f"Candidate evaluation report schema error at {location}: {first.message}")


def candidate_evaluation_report_key(path: Path) -> str:
    name = path.name
    if name.endswith(CANDIDATE_EVALUATION_REPORT_SUFFIX):
        return name[: -len(CANDIDATE_EVALUATION_REPORT_SUFFIX)]
    return path.stem


def iter_candidate_evaluation_report_paths(candidate_dir: Path) -> list[Path]:
    if not candidate_dir.exists():
        raise CandidateEvaluationError(f"Candidate evaluation directory does not exist: {candidate_dir}")
    return sorted(path for path in candidate_dir.glob(f"*{CANDIDATE_EVALUATION_REPORT_SUFFIX}") if path.is_file())


def load_candidate_evaluation_report_schema(candidate_dir: Path) -> dict[str, Any]:
    return load_json(candidate_dir / CANDIDATE_EVALUATION_REPORT_SCHEMA_NAME)


def load_validated_candidate_evaluation_report(path: Path, schema: dict[str, Any]) -> dict[str, Any]:
    report = load_json(path)
    validate_candidate_evaluation_report_schema(report, schema)
    return report


def summarize_candidate_evaluation_report(path: Path, report: dict[str, Any]) -> dict[str, Any]:
    evaluation_report = report.get("evaluation_report", {})
    binding = report.get("candidate_binding", {})
    summary = report.get("evidence_summary", {})
    recommendation = report.get("recommendation", {})
    boundary = report.get("evaluation_boundary", {})
    return {
        "key": candidate_evaluation_report_key(path),
        "file": str(path),
        "id": evaluation_report.get("id") if isinstance(evaluation_report, dict) else None,
        "status": evaluation_report.get("status") if isinstance(evaluation_report, dict) else None,
        "report_mode": evaluation_report.get("report_mode") if isinstance(evaluation_report, dict) else None,
        "candidate_manifest_id": binding.get("candidate_manifest_id") if isinstance(binding, dict) else None,
        "candidate_id": binding.get("candidate_id") if isinstance(binding, dict) else None,
        "candidate_manifest_key": binding.get("candidate_manifest_key") if isinstance(binding, dict) else None,
        "contract_key": binding.get("contract_key") if isinstance(binding, dict) else None,
        "candidate_reference_status": binding.get("candidate_reference_status") if isinstance(binding, dict) else None,
        "overall_evidence_status": summary.get("overall_evidence_status") if isinstance(summary, dict) else None,
        "not_observed_count": summary.get("not_observed_count") if isinstance(summary, dict) else None,
        "recommended_decision": recommendation.get("recommended_decision") if isinstance(recommendation, dict) else None,
        "uncertainty_default": recommendation.get("uncertainty_default") if isinstance(recommendation, dict) else None,
        "approval_allowed": recommendation.get("approval_allowed") if isinstance(recommendation, dict) else None,
        "image_generation_ran": boundary.get("image_generation_ran") if isinstance(boundary, dict) else None,
        "real_image_ingestion_ran": boundary.get("real_image_ingestion_ran") if isinstance(boundary, dict) else None,
        "computer_vision_integration_ran": boundary.get("computer_vision_integration_ran") if isinstance(boundary, dict) else None,
        "candidate_evaluation_ran": boundary.get("candidate_evaluation_ran") if isinstance(boundary, dict) else None,
    }


def find_candidate_evaluation_report_for_manifest(manifest_summary: dict[str, Any], candidate_dir: Path) -> Path:
    schema = load_candidate_evaluation_report_schema(candidate_dir)
    matches: list[Path] = []
    expected = {
        manifest_summary.get("key"),
        manifest_summary.get("contract_key"),
        manifest_summary.get("candidate_id"),
        manifest_summary.get("id"),
    }
    for path in iter_candidate_evaluation_report_paths(candidate_dir):
        report = load_validated_candidate_evaluation_report(path, schema)
        summary = summarize_candidate_evaluation_report(path, report)
        actual = {
            summary.get("key"),
            summary.get("candidate_manifest_key"),
            summary.get("contract_key"),
            summary.get("candidate_id"),
            summary.get("candidate_manifest_id"),
        }
        if expected & actual:
            matches.append(path)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        available = ", ".join(path.name for path in matches)
        raise CandidateEvaluationError(f"Ambiguous candidate evaluation report for manifest {manifest_summary.get('key')}: {available}")
    available = ", ".join(candidate_evaluation_report_key(path) for path in iter_candidate_evaluation_report_paths(candidate_dir))
    raise CandidateEvaluationError(f"No candidate evaluation report fixture found for manifest {manifest_summary.get('key')}. Available reports: {available}")


def require_report_matches_manifest(report_summary: dict[str, Any], manifest_summary: dict[str, Any]) -> None:
    checks = [
        ("candidate_manifest_id", manifest_summary.get("id")),
        ("candidate_id", manifest_summary.get("candidate_id")),
        ("contract_key", manifest_summary.get("contract_key")),
        ("candidate_reference_status", manifest_summary.get("reference_status")),
    ]
    for report_field, expected in checks:
        actual = report_summary.get(report_field)
        if actual != expected:
            raise CandidateEvaluationError(f"Candidate evaluation report binding mismatch for {report_field}: expected={expected!r}; actual={actual!r}")


def build_fixture_only_candidate_evaluation(reference: str, candidate_dir: Path) -> dict[str, Any]:
    manifest_report = load_candidate_manifest_report(reference, candidate_dir)
    manifest_summary = manifest_report["summary"]
    report_path = find_candidate_evaluation_report_for_manifest(manifest_summary, candidate_dir)
    report_schema = load_candidate_evaluation_report_schema(candidate_dir)
    evaluation_report = load_validated_candidate_evaluation_report(report_path, report_schema)
    evaluation_summary = summarize_candidate_evaluation_report(report_path, evaluation_report)
    require_report_matches_manifest(evaluation_summary, manifest_summary)
    if evaluation_summary.get("recommended_decision") != "needs_review":
        raise CandidateEvaluationError("Fixture-only candidate evaluation must recommend needs_review")
    if evaluation_summary.get("approval_allowed") is not False:
        raise CandidateEvaluationError("Fixture-only candidate evaluation must not allow approval")
    return {
        "candidate_evaluation": {
            "mode": "fixture_only",
            "candidate_dir": str(candidate_dir),
            "selected_manifest": manifest_summary.get("key"),
            "selected_report": evaluation_summary.get("key"),
            "image_generation": "not_run",
            "real_image_ingestion": "not_run",
            "computer_vision": "not_run",
            "approval_automation": "not_run",
        },
        "summary": {
            "candidate_manifest_key": manifest_summary.get("key"),
            "candidate_id": manifest_summary.get("candidate_id"),
            "contract_key": manifest_summary.get("contract_key"),
            "candidate_reference_status": manifest_summary.get("reference_status"),
            "report_key": evaluation_summary.get("key"),
            "report_mode": evaluation_summary.get("report_mode"),
            "overall_evidence_status": evaluation_summary.get("overall_evidence_status"),
            "not_observed_count": evaluation_summary.get("not_observed_count"),
            "recommended_decision": evaluation_summary.get("recommended_decision"),
            "uncertainty_default": evaluation_summary.get("uncertainty_default"),
            "approval_allowed": evaluation_summary.get("approval_allowed"),
        },
        "candidate_manifest": manifest_report["candidate_manifest"],
        "evaluation_report": evaluation_report,
    }
