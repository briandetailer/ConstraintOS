from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from constraintos.graphics_contracts import discover_project_root

DEFAULT_CANDIDATE_MANIFESTS_DIR = Path("examples") / "graphics" / "candidate_evaluation"
DEFAULT_CANDIDATE_MANIFEST_SCHEMA_NAME = "candidate_manifest.schema.json"
CANDIDATE_MANIFEST_SUFFIX = "_candidate_manifest.fixture.json"


class CandidateManifestError(ValueError):
    """Raised when a candidate manifest fixture is invalid or cannot be found."""


def load_json(path: Path | str) -> dict[str, Any]:
    target = Path(path)
    value = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CandidateManifestError(f"Expected JSON object in {target}")
    return value


def validate_candidate_manifest_schema(manifest: dict[str, Any], schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(manifest), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise CandidateManifestError(f"Candidate manifest schema error at {location}: {first.message}")


def resolve_candidate_manifests_dir(project_root: Path, explicit_candidate_dir: str | None = None) -> Path:
    if explicit_candidate_dir:
        candidate_dir = Path(explicit_candidate_dir)
        return candidate_dir if candidate_dir.is_absolute() else project_root / candidate_dir
    return project_root / DEFAULT_CANDIDATE_MANIFESTS_DIR


def candidate_manifest_key(path: Path) -> str:
    name = path.name
    if name.endswith(CANDIDATE_MANIFEST_SUFFIX):
        return name[: -len(CANDIDATE_MANIFEST_SUFFIX)]
    return path.stem


def iter_candidate_manifest_paths(candidate_dir: Path) -> list[Path]:
    if not candidate_dir.exists():
        raise CandidateManifestError(f"Candidate manifests directory does not exist: {candidate_dir}")
    return sorted(path for path in candidate_dir.glob(f"*{CANDIDATE_MANIFEST_SUFFIX}") if path.is_file())


def load_candidate_manifest_schema(candidate_dir: Path) -> dict[str, Any]:
    return load_json(candidate_dir / DEFAULT_CANDIDATE_MANIFEST_SCHEMA_NAME)


def load_validated_candidate_manifest(path: Path, schema: dict[str, Any]) -> dict[str, Any]:
    manifest = load_json(path)
    validate_candidate_manifest_schema(manifest, schema)
    return manifest


def summarize_candidate_manifest(path: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    candidate_manifest = manifest.get("candidate_manifest", {})
    contract_binding = manifest.get("contract_binding", {})
    candidate_reference = manifest.get("candidate_reference", {})
    candidate_source = manifest.get("candidate_source", {})
    evaluation_boundary = manifest.get("evaluation_boundary", {})
    approval_expectation = manifest.get("approval_expectation", {})
    return {
        "key": candidate_manifest_key(path),
        "file": str(path),
        "id": candidate_manifest.get("id") if isinstance(candidate_manifest, dict) else None,
        "candidate_id": candidate_manifest.get("candidate_id") if isinstance(candidate_manifest, dict) else None,
        "status": candidate_manifest.get("status") if isinstance(candidate_manifest, dict) else None,
        "contract_key": contract_binding.get("contract_key") if isinstance(contract_binding, dict) else None,
        "source_contract_id": contract_binding.get("source_contract_id") if isinstance(contract_binding, dict) else None,
        "reference_type": candidate_reference.get("reference_type") if isinstance(candidate_reference, dict) else None,
        "reference_status": candidate_reference.get("reference_status") if isinstance(candidate_reference, dict) else None,
        "media_type": candidate_reference.get("media_type") if isinstance(candidate_reference, dict) else None,
        "candidate_source_type": candidate_source.get("candidate_source_type") if isinstance(candidate_source, dict) else None,
        "generated_by_constraintos": candidate_source.get("generated_by_constraintos") if isinstance(candidate_source, dict) else None,
        "producer": candidate_source.get("producer") if isinstance(candidate_source, dict) else None,
        "evaluation_status": evaluation_boundary.get("evaluation_status") if isinstance(evaluation_boundary, dict) else None,
        "image_generation_allowed": evaluation_boundary.get("image_generation_allowed") if isinstance(evaluation_boundary, dict) else None,
        "image_editing_allowed": evaluation_boundary.get("image_editing_allowed") if isinstance(evaluation_boundary, dict) else None,
        "real_image_ingestion_allowed": evaluation_boundary.get("real_image_ingestion_allowed") if isinstance(evaluation_boundary, dict) else None,
        "computer_vision_integration_allowed": evaluation_boundary.get("computer_vision_integration_allowed") if isinstance(evaluation_boundary, dict) else None,
        "initial_decision": approval_expectation.get("initial_decision") if isinstance(approval_expectation, dict) else None,
        "uncertainty_default": approval_expectation.get("uncertainty_default") if isinstance(approval_expectation, dict) else None,
    }


def list_candidate_manifest_summaries(candidate_dir: Path) -> list[dict[str, Any]]:
    schema = load_candidate_manifest_schema(candidate_dir)
    summaries: list[dict[str, Any]] = []
    for path in iter_candidate_manifest_paths(candidate_dir):
        summaries.append(summarize_candidate_manifest(path, load_validated_candidate_manifest(path, schema)))
    return summaries


def resolve_candidate_manifest_path(reference: str, candidate_dir: Path) -> Path:
    candidate = Path(reference)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    if candidate.suffix == ".json":
        relative = candidate_dir / candidate
        if relative.exists():
            return relative
    direct = candidate_dir / f"{reference}{CANDIDATE_MANIFEST_SUFFIX}"
    if direct.exists():
        return direct

    schema = load_candidate_manifest_schema(candidate_dir)
    matches: list[Path] = []
    for path in iter_candidate_manifest_paths(candidate_dir):
        manifest = load_validated_candidate_manifest(path, schema)
        summary = summarize_candidate_manifest(path, manifest)
        if reference in {summary.get("key"), summary.get("contract_key"), summary.get("candidate_id"), summary.get("id")}:
            matches.append(path)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        available = ", ".join(str(path.name) for path in matches)
        raise CandidateManifestError(f"Ambiguous candidate manifest reference: {reference}. Matches: {available}")

    available = ", ".join(candidate_manifest_key(path) for path in iter_candidate_manifest_paths(candidate_dir))
    raise CandidateManifestError(f"Unknown candidate manifest: {reference}. Available manifests: {available}")


def load_candidate_manifest_report(reference: str, candidate_dir: Path) -> dict[str, Any]:
    schema = load_candidate_manifest_schema(candidate_dir)
    path = resolve_candidate_manifest_path(reference, candidate_dir)
    manifest = load_validated_candidate_manifest(path, schema)
    return {
        "summary": summarize_candidate_manifest(path, manifest),
        "candidate_manifest": manifest,
    }
