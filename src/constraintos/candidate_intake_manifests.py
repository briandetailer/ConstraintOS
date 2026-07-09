from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from constraintos.candidate_manifests import CandidateManifestError, load_json

CANDIDATE_INTAKE_MANIFEST_SCHEMA_NAME = "candidate_intake_manifest.schema.json"
CANDIDATE_INTAKE_MANIFEST_SUFFIX = "_candidate_intake_manifest.fixture.json"


class CandidateIntakeManifestError(CandidateManifestError):
    """Raised when a candidate intake manifest fixture is invalid or cannot be found."""


def validate_candidate_intake_manifest_schema(manifest: dict[str, Any], schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(manifest), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise CandidateIntakeManifestError(f"Candidate intake manifest schema error at {location}: {first.message}")


def candidate_intake_manifest_key(path: Path) -> str:
    name = path.name
    if name.endswith(CANDIDATE_INTAKE_MANIFEST_SUFFIX):
        return name[: -len(CANDIDATE_INTAKE_MANIFEST_SUFFIX)]
    return path.stem


def iter_candidate_intake_manifest_paths(candidate_dir: Path) -> list[Path]:
    if not candidate_dir.exists():
        raise CandidateIntakeManifestError(f"Candidate manifests directory does not exist: {candidate_dir}")
    return sorted(path for path in candidate_dir.glob(f"*{CANDIDATE_INTAKE_MANIFEST_SUFFIX}") if path.is_file())


def load_candidate_intake_manifest_schema(candidate_dir: Path) -> dict[str, Any]:
    return load_json(candidate_dir / CANDIDATE_INTAKE_MANIFEST_SCHEMA_NAME)


def load_validated_candidate_intake_manifest(path: Path, schema: dict[str, Any]) -> dict[str, Any]:
    manifest = load_json(path)
    validate_candidate_intake_manifest_schema(manifest, schema)
    return manifest


def summarize_candidate_intake_manifest(path: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    intake_manifest = manifest.get("candidate_intake_manifest", {})
    contract_binding = manifest.get("contract_binding", {})
    candidate_reference = manifest.get("candidate_reference", {})
    candidate_source = manifest.get("candidate_source", {})
    policy = manifest.get("intake_policy_snapshot", {})
    boundary = manifest.get("intake_boundary", {})
    approval = manifest.get("approval_expectation", {})
    return {
        "key": candidate_intake_manifest_key(path),
        "file": str(path),
        "id": intake_manifest.get("id") if isinstance(intake_manifest, dict) else None,
        "candidate_id": intake_manifest.get("candidate_id") if isinstance(intake_manifest, dict) else None,
        "status": intake_manifest.get("status") if isinstance(intake_manifest, dict) else None,
        "intake_state": intake_manifest.get("intake_state") if isinstance(intake_manifest, dict) else None,
        "contract_key": contract_binding.get("contract_key") if isinstance(contract_binding, dict) else None,
        "source_contract_id": contract_binding.get("source_contract_id") if isinstance(contract_binding, dict) else None,
        "reference_type": candidate_reference.get("reference_type") if isinstance(candidate_reference, dict) else None,
        "reference": candidate_reference.get("reference") if isinstance(candidate_reference, dict) else None,
        "reference_status": candidate_reference.get("reference_status") if isinstance(candidate_reference, dict) else None,
        "media_type": candidate_reference.get("media_type") if isinstance(candidate_reference, dict) else None,
        "image_sha256": candidate_reference.get("image_sha256") if isinstance(candidate_reference, dict) else None,
        "expected_byte_count": candidate_reference.get("expected_byte_count") if isinstance(candidate_reference, dict) else None,
        "candidate_source_type": candidate_source.get("candidate_source_type") if isinstance(candidate_source, dict) else None,
        "generated_by_constraintos": candidate_source.get("generated_by_constraintos") if isinstance(candidate_source, dict) else None,
        "producer": candidate_source.get("producer") if isinstance(candidate_source, dict) else None,
        "network_fetch_allowed": policy.get("network_fetch_allowed") if isinstance(policy, dict) else None,
        "successful_intake_can_approve": policy.get("successful_intake_can_approve") if isinstance(policy, dict) else None,
        "image_bytes_loaded": boundary.get("image_bytes_loaded") if isinstance(boundary, dict) else None,
        "image_decoded": boundary.get("image_decoded") if isinstance(boundary, dict) else None,
        "pixel_inspection_ran": boundary.get("pixel_inspection_ran") if isinstance(boundary, dict) else None,
        "candidate_scoring_ran": boundary.get("candidate_scoring_ran") if isinstance(boundary, dict) else None,
        "source_report_mutation_ran": boundary.get("source_report_mutation_ran") if isinstance(boundary, dict) else None,
        "initial_decision": approval.get("initial_decision") if isinstance(approval, dict) else None,
        "uncertainty_default": approval.get("uncertainty_default") if isinstance(approval, dict) else None,
        "approval_allowed": approval.get("approval_allowed") if isinstance(approval, dict) else None,
    }


def list_candidate_intake_manifest_summaries(candidate_dir: Path) -> list[dict[str, Any]]:
    schema = load_candidate_intake_manifest_schema(candidate_dir)
    summaries: list[dict[str, Any]] = []
    for path in iter_candidate_intake_manifest_paths(candidate_dir):
        summaries.append(summarize_candidate_intake_manifest(path, load_validated_candidate_intake_manifest(path, schema)))
    return summaries


def resolve_candidate_intake_manifest_path(reference: str, candidate_dir: Path) -> Path:
    candidate = Path(reference)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    if candidate.suffix == ".json":
        relative = candidate_dir / candidate
        if relative.exists():
            return relative
    direct = candidate_dir / f"{reference}{CANDIDATE_INTAKE_MANIFEST_SUFFIX}"
    if direct.exists():
        return direct

    schema = load_candidate_intake_manifest_schema(candidate_dir)
    matches: list[Path] = []
    for path in iter_candidate_intake_manifest_paths(candidate_dir):
        manifest = load_validated_candidate_intake_manifest(path, schema)
        summary = summarize_candidate_intake_manifest(path, manifest)
        if reference in {summary.get("key"), summary.get("contract_key"), summary.get("candidate_id"), summary.get("id")}:
            matches.append(path)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        available = ", ".join(str(path.name) for path in matches)
        raise CandidateIntakeManifestError(f"Ambiguous candidate intake manifest reference: {reference}. Matches: {available}")

    available = ", ".join(candidate_intake_manifest_key(path) for path in iter_candidate_intake_manifest_paths(candidate_dir))
    raise CandidateIntakeManifestError(f"Unknown candidate intake manifest: {reference}. Available manifests: {available}")


def load_candidate_intake_manifest_report(reference: str, candidate_dir: Path) -> dict[str, Any]:
    schema = load_candidate_intake_manifest_schema(candidate_dir)
    path = resolve_candidate_intake_manifest_path(reference, candidate_dir)
    manifest = load_validated_candidate_intake_manifest(path, schema)
    return {
        "summary": summarize_candidate_intake_manifest(path, manifest),
        "candidate_intake_manifest": manifest,
    }
