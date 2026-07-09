from __future__ import annotations

from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from constraintos.candidate_manifests import CandidateManifestError, load_json

CANDIDATE_IMAGE_BYTE_LOADING_RECORD_SCHEMA_NAME = "candidate_image_byte_loading_record.schema.json"
CANDIDATE_IMAGE_BYTE_LOADING_RECORD_SUFFIX = "_candidate_image_byte_loading_record.fixture.json"


class CandidateImageByteLoadingRecordError(CandidateManifestError):
    """Raised when a candidate image byte-loading record fixture is invalid or cannot be found."""


def validate_candidate_image_byte_loading_record_schema(record: dict[str, Any], schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise CandidateImageByteLoadingRecordError(f"Candidate image byte-loading record schema error at {location}: {first.message}")


def candidate_image_byte_loading_record_key(path: Path) -> str:
    name = path.name
    if name.endswith(CANDIDATE_IMAGE_BYTE_LOADING_RECORD_SUFFIX):
        return name[: -len(CANDIDATE_IMAGE_BYTE_LOADING_RECORD_SUFFIX)]
    return path.stem


def iter_candidate_image_byte_loading_record_paths(candidate_dir: Path) -> list[Path]:
    if not candidate_dir.exists():
        raise CandidateImageByteLoadingRecordError(f"Candidate records directory does not exist: {candidate_dir}")
    return sorted(path for path in candidate_dir.glob(f"*{CANDIDATE_IMAGE_BYTE_LOADING_RECORD_SUFFIX}") if path.is_file())


def load_candidate_image_byte_loading_record_schema(candidate_dir: Path) -> dict[str, Any]:
    return load_json(candidate_dir / CANDIDATE_IMAGE_BYTE_LOADING_RECORD_SCHEMA_NAME)


def load_validated_candidate_image_byte_loading_record(path: Path, schema: dict[str, Any]) -> dict[str, Any]:
    record = load_json(path)
    validate_candidate_image_byte_loading_record_schema(record, schema)
    return record


def summarize_candidate_image_byte_loading_record(path: Path, record: dict[str, Any]) -> dict[str, Any]:
    loading_record = record.get("candidate_image_byte_loading_record", {})
    binding = record.get("contract_binding", {})
    reference = record.get("reference_snapshot", {})
    policy = record.get("byte_loading_policy_snapshot", {})
    result = record.get("byte_loading_result", {})
    boundary = record.get("post_load_boundary", {})
    approval = record.get("approval_expectation", {})
    return {
        "key": candidate_image_byte_loading_record_key(path),
        "file": str(path),
        "id": loading_record.get("id") if isinstance(loading_record, dict) else None,
        "candidate_id": loading_record.get("candidate_id") if isinstance(loading_record, dict) else None,
        "status": loading_record.get("status") if isinstance(loading_record, dict) else None,
        "byte_loading_state": loading_record.get("byte_loading_state") if isinstance(loading_record, dict) else None,
        "contract_key": binding.get("contract_key") if isinstance(binding, dict) else None,
        "source_contract_id": binding.get("source_contract_id") if isinstance(binding, dict) else None,
        "candidate_intake_manifest_id": binding.get("candidate_intake_manifest_id") if isinstance(binding, dict) else None,
        "reference_type": reference.get("reference_type") if isinstance(reference, dict) else None,
        "reference": reference.get("reference") if isinstance(reference, dict) else None,
        "media_type": reference.get("media_type") if isinstance(reference, dict) else None,
        "image_sha256": reference.get("image_sha256") if isinstance(reference, dict) else None,
        "expected_byte_count": reference.get("expected_byte_count") if isinstance(reference, dict) else None,
        "max_candidate_image_bytes": policy.get("max_candidate_image_bytes") if isinstance(policy, dict) else None,
        "network_fetch_allowed": policy.get("network_fetch_allowed") if isinstance(policy, dict) else None,
        "implicit_cloud_download_allowed": policy.get("implicit_cloud_download_allowed") if isinstance(policy, dict) else None,
        "byte_loading_success_can_approve": policy.get("byte_loading_success_can_approve") if isinstance(policy, dict) else None,
        "image_bytes_loaded": result.get("image_bytes_loaded") if isinstance(result, dict) else None,
        "local_file_opened": result.get("local_file_opened") if isinstance(result, dict) else None,
        "artifact_downloaded": result.get("artifact_downloaded") if isinstance(result, dict) else None,
        "network_fetch_ran": result.get("network_fetch_ran") if isinstance(result, dict) else None,
        "actual_loaded_byte_count": result.get("actual_loaded_byte_count") if isinstance(result, dict) else None,
        "computed_sha256": result.get("computed_sha256") if isinstance(result, dict) else None,
        "sniffed_media_type": result.get("sniffed_media_type") if isinstance(result, dict) else None,
        "checksum_matches": result.get("checksum_matches") if isinstance(result, dict) else None,
        "media_type_matches": result.get("media_type_matches") if isinstance(result, dict) else None,
        "image_decoded": boundary.get("image_decoded") if isinstance(boundary, dict) else None,
        "pixel_inspection_ran": boundary.get("pixel_inspection_ran") if isinstance(boundary, dict) else None,
        "computer_vision_ran": boundary.get("computer_vision_ran") if isinstance(boundary, dict) else None,
        "ocr_ran": boundary.get("ocr_ran") if isinstance(boundary, dict) else None,
        "candidate_scoring_ran": boundary.get("candidate_scoring_ran") if isinstance(boundary, dict) else None,
        "source_report_mutation_ran": boundary.get("source_report_mutation_ran") if isinstance(boundary, dict) else None,
        "approval_automation_ran": boundary.get("approval_automation_ran") if isinstance(boundary, dict) else None,
        "initial_decision": approval.get("initial_decision") if isinstance(approval, dict) else None,
        "uncertainty_default": approval.get("uncertainty_default") if isinstance(approval, dict) else None,
        "approval_allowed": approval.get("approval_allowed") if isinstance(approval, dict) else None,
    }


def list_candidate_image_byte_loading_record_summaries(candidate_dir: Path) -> list[dict[str, Any]]:
    schema = load_candidate_image_byte_loading_record_schema(candidate_dir)
    summaries: list[dict[str, Any]] = []
    for path in iter_candidate_image_byte_loading_record_paths(candidate_dir):
        summaries.append(summarize_candidate_image_byte_loading_record(path, load_validated_candidate_image_byte_loading_record(path, schema)))
    return summaries


def resolve_candidate_image_byte_loading_record_path(reference: str, candidate_dir: Path) -> Path:
    candidate = Path(reference)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    if candidate.suffix == ".json":
        relative = candidate_dir / candidate
        if relative.exists():
            return relative
    direct = candidate_dir / f"{reference}{CANDIDATE_IMAGE_BYTE_LOADING_RECORD_SUFFIX}"
    if direct.exists():
        return direct

    schema = load_candidate_image_byte_loading_record_schema(candidate_dir)
    matches: list[Path] = []
    for path in iter_candidate_image_byte_loading_record_paths(candidate_dir):
        record = load_validated_candidate_image_byte_loading_record(path, schema)
        summary = summarize_candidate_image_byte_loading_record(path, record)
        if reference in {summary.get("key"), summary.get("contract_key"), summary.get("candidate_id"), summary.get("id"), summary.get("candidate_intake_manifest_id")}:
            matches.append(path)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        available = ", ".join(str(path.name) for path in matches)
        raise CandidateImageByteLoadingRecordError(f"Ambiguous candidate image byte-loading record reference: {reference}. Matches: {available}")

    available = ", ".join(candidate_image_byte_loading_record_key(path) for path in iter_candidate_image_byte_loading_record_paths(candidate_dir))
    raise CandidateImageByteLoadingRecordError(f"Unknown candidate image byte-loading record: {reference}. Available records: {available}")


def load_candidate_image_byte_loading_record_report(reference: str, candidate_dir: Path) -> dict[str, Any]:
    schema = load_candidate_image_byte_loading_record_schema(candidate_dir)
    path = resolve_candidate_image_byte_loading_record_path(reference, candidate_dir)
    record = load_validated_candidate_image_byte_loading_record(path, schema)
    return {
        "summary": summarize_candidate_image_byte_loading_record(path, record),
        "candidate_image_byte_loading_record": record,
    }
