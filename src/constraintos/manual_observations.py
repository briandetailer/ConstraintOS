from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from constraintos.candidate_manifests import load_candidate_manifest_report, load_json

MANUAL_OBSERVATION_SCHEMA_NAME = "manual_observation.schema.json"
MANUAL_OBSERVATION_SUFFIX = "_manual_observation.fixture.json"


class ManualObservationError(ValueError):
    """Raised when a manual observation fixture is invalid or unsafe."""


def manual_observation_key(path: Path) -> str:
    name = path.name
    if name.endswith(MANUAL_OBSERVATION_SUFFIX):
        return name[: -len(MANUAL_OBSERVATION_SUFFIX)]
    return path.stem


def iter_manual_observation_paths(candidate_dir: Path) -> list[Path]:
    if not candidate_dir.exists():
        raise ManualObservationError(f"Candidate evaluation directory does not exist: {candidate_dir}")
    return sorted(path for path in candidate_dir.glob(f"*{MANUAL_OBSERVATION_SUFFIX}") if path.is_file())


def load_manual_observation_schema(candidate_dir: Path) -> dict[str, Any]:
    return load_json(candidate_dir / MANUAL_OBSERVATION_SCHEMA_NAME)


def validate_manual_observation_schema(observation: dict[str, Any], schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(observation), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise ManualObservationError(f"Manual observation schema error at {location}: {first.message}")


def load_validated_manual_observation(path: Path, schema: dict[str, Any]) -> dict[str, Any]:
    observation = load_json(path)
    validate_manual_observation_schema(observation, schema)
    return observation


def summarize_manual_observation(path: Path, observation: dict[str, Any]) -> dict[str, Any]:
    fixture = observation.get("manual_observation_fixture", {})
    binding = observation.get("candidate_binding", {})
    boundary = observation.get("observation_boundary", {})
    summary = observation.get("observation_summary", {})
    recommendation = observation.get("recommendation", {})
    return {
        "key": manual_observation_key(path),
        "file": str(path),
        "id": fixture.get("id") if isinstance(fixture, dict) else None,
        "status": fixture.get("status") if isinstance(fixture, dict) else None,
        "observation_mode": fixture.get("observation_mode") if isinstance(fixture, dict) else None,
        "candidate_manifest_id": binding.get("candidate_manifest_id") if isinstance(binding, dict) else None,
        "candidate_id": binding.get("candidate_id") if isinstance(binding, dict) else None,
        "candidate_manifest_key": binding.get("candidate_manifest_key") if isinstance(binding, dict) else None,
        "contract_key": binding.get("contract_key") if isinstance(binding, dict) else None,
        "candidate_reference_status": binding.get("candidate_reference_status") if isinstance(binding, dict) else None,
        "source_type": boundary.get("source_type") if isinstance(boundary, dict) else None,
        "real_image_ingestion_ran": boundary.get("real_image_ingestion_ran") if isinstance(boundary, dict) else None,
        "computer_vision_ran": boundary.get("computer_vision_ran") if isinstance(boundary, dict) else None,
        "ocr_ran": boundary.get("ocr_ran") if isinstance(boundary, dict) else None,
        "image_generation_ran": boundary.get("image_generation_ran") if isinstance(boundary, dict) else None,
        "image_editing_ran": boundary.get("image_editing_ran") if isinstance(boundary, dict) else None,
        "approval_automation_ran": boundary.get("approval_automation_ran") if isinstance(boundary, dict) else None,
        "total_observations": summary.get("total_observations") if isinstance(summary, dict) else None,
        "not_observed_count": summary.get("not_observed_count") if isinstance(summary, dict) else None,
        "lowest_confidence": summary.get("lowest_confidence") if isinstance(summary, dict) else None,
        "overall_observation_status": summary.get("overall_observation_status") if isinstance(summary, dict) else None,
        "recommended_decision": recommendation.get("recommended_decision") if isinstance(recommendation, dict) else None,
        "approval_allowed": recommendation.get("approval_allowed") if isinstance(recommendation, dict) else None,
        "uncertainty_default": recommendation.get("uncertainty_default") if isinstance(recommendation, dict) else None,
        "manual_observations_can_approve_alone": recommendation.get("manual_observations_can_approve_alone") if isinstance(recommendation, dict) else None,
    }


def find_manual_observation_for_manifest(manifest_summary: dict[str, Any], candidate_dir: Path) -> Path:
    schema = load_manual_observation_schema(candidate_dir)
    expected = {
        manifest_summary.get("key"),
        manifest_summary.get("contract_key"),
        manifest_summary.get("candidate_id"),
        manifest_summary.get("id"),
    }
    matches: list[Path] = []
    for path in iter_manual_observation_paths(candidate_dir):
        observation = load_validated_manual_observation(path, schema)
        summary = summarize_manual_observation(path, observation)
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
        raise ManualObservationError(f"Ambiguous manual observation fixture for manifest {manifest_summary.get('key')}: {available}")
    available = ", ".join(manual_observation_key(path) for path in iter_manual_observation_paths(candidate_dir))
    raise ManualObservationError(f"No manual observation fixture found for manifest {manifest_summary.get('key')}. Available observations: {available}")


def require_observation_matches_manifest(observation_summary: dict[str, Any], manifest_summary: dict[str, Any]) -> None:
    checks = [
        ("candidate_manifest_id", manifest_summary.get("id")),
        ("candidate_id", manifest_summary.get("candidate_id")),
        ("contract_key", manifest_summary.get("contract_key")),
        ("candidate_reference_status", manifest_summary.get("reference_status")),
    ]
    for observation_field, expected in checks:
        actual = observation_summary.get(observation_field)
        if actual != expected:
            raise ManualObservationError(f"Manual observation binding mismatch for {observation_field}: expected={expected!r}; actual={actual!r}")


def build_manual_observation_payload(reference: str, candidate_dir: Path) -> dict[str, Any]:
    manifest_report = load_candidate_manifest_report(reference, candidate_dir)
    manifest_summary = manifest_report["summary"]
    observation_path = find_manual_observation_for_manifest(manifest_summary, candidate_dir)
    schema = load_manual_observation_schema(candidate_dir)
    observation = load_validated_manual_observation(observation_path, schema)
    observation_summary = summarize_manual_observation(observation_path, observation)
    require_observation_matches_manifest(observation_summary, manifest_summary)
    if observation_summary.get("recommended_decision") != "needs_review":
        raise ManualObservationError("Manual observation fixtures must recommend needs_review")
    if observation_summary.get("approval_allowed") is not False:
        raise ManualObservationError("Manual observation fixtures must not allow approval")
    return {
        "manual_observation": {
            "mode": "fixture_only",
            "candidate_dir": str(candidate_dir),
            "selected_manifest": manifest_summary.get("key"),
            "selected_observation": observation_summary.get("key"),
            "real_image_ingestion": "not_run",
            "computer_vision": "not_run",
            "ocr": "not_run",
            "image_generation": "not_run",
            "approval_automation": "not_run",
        },
        "summary": {
            "candidate_manifest_key": manifest_summary.get("key"),
            "candidate_id": manifest_summary.get("candidate_id"),
            "contract_key": manifest_summary.get("contract_key"),
            "candidate_reference_status": manifest_summary.get("reference_status"),
            "observation_key": observation_summary.get("key"),
            "observation_mode": observation_summary.get("observation_mode"),
            "source_type": observation_summary.get("source_type"),
            "total_observations": observation_summary.get("total_observations"),
            "not_observed_count": observation_summary.get("not_observed_count"),
            "lowest_confidence": observation_summary.get("lowest_confidence"),
            "overall_observation_status": observation_summary.get("overall_observation_status"),
            "recommended_decision": observation_summary.get("recommended_decision"),
            "uncertainty_default": observation_summary.get("uncertainty_default"),
            "approval_allowed": observation_summary.get("approval_allowed"),
        },
        "candidate_manifest": manifest_report["candidate_manifest"],
        "manual_observation_fixture": observation,
    }
