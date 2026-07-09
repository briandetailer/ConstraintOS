from __future__ import annotations

import hashlib
from copy import deepcopy
from types import MappingProxyType
from typing import Any, Mapping

from constraintos.candidate_image_byte_loading_records import CandidateImageByteLoadingRecordError


class CandidateImageByteLoaderError(CandidateImageByteLoadingRecordError):
    """Raised when minimal candidate image byte loading cannot evaluate a request safely."""


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"
WEBP_RIFF_SIGNATURE = b"RIFF"
WEBP_FORMAT_SIGNATURE = b"WEBP"


SUPPORTED_MEDIA_TYPES = {"image/png", "image/jpeg", "image/webp"}
NETWORK_REFERENCE_PREFIXES = ("http://", "https://")


class InMemoryArtifactRegistry:
    """Explicit fixture-controlled artifact registry for minimal byte-loading tests."""

    def __init__(self, artifacts: Mapping[str, bytes]):
        self._artifacts = MappingProxyType(dict(artifacts))

    def read_artifact_bytes(self, artifact_uri: str) -> bytes | None:
        artifact = self._artifacts.get(artifact_uri)
        if artifact is None:
            return None
        return bytes(artifact)


def sniff_candidate_image_media_type(data: bytes) -> str | None:
    if data.startswith(PNG_SIGNATURE):
        return "image/png"
    if data.startswith(JPEG_SIGNATURE):
        return "image/jpeg"
    if len(data) >= 12 and data.startswith(WEBP_RIFF_SIGNATURE) and data[8:12] == WEBP_FORMAT_SIGNATURE:
        return "image/webp"
    return None


def immutable_result(result: dict[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(deepcopy(result))


def reference_snapshot(record: dict[str, Any]) -> dict[str, Any]:
    snapshot = record.get("reference_snapshot")
    if not isinstance(snapshot, dict):
        raise CandidateImageByteLoaderError("Byte-loading record must include reference_snapshot")
    return snapshot


def policy_snapshot(record: dict[str, Any]) -> dict[str, Any]:
    policy = record.get("byte_loading_policy_snapshot")
    if not isinstance(policy, dict):
        raise CandidateImageByteLoaderError("Byte-loading record must include byte_loading_policy_snapshot")
    return policy


def loading_record_identity(record: dict[str, Any]) -> tuple[str | None, str | None]:
    loading_record = record.get("candidate_image_byte_loading_record", {})
    binding = record.get("contract_binding", {})
    candidate_id = loading_record.get("candidate_id") if isinstance(loading_record, dict) else None
    contract_key = binding.get("contract_key") if isinstance(binding, dict) else None
    return candidate_id, contract_key


def safe_failure_result(record: dict[str, Any], failure_code: str, failure_reason: str) -> Mapping[str, Any]:
    snapshot = reference_snapshot(record)
    candidate_id, contract_key = loading_record_identity(record)
    return immutable_result(
        {
            "status": "intake_failed",
            "failure_code": failure_code,
            "failure_reason": failure_reason,
            "candidate_id": candidate_id,
            "contract_key": contract_key,
            "reference_type": snapshot.get("reference_type"),
            "reference": snapshot.get("reference"),
            "declared_media_type": snapshot.get("media_type"),
            "expected_byte_count": snapshot.get("expected_byte_count"),
            "image_bytes_loaded": False,
            "local_file_opened": False,
            "artifact_downloaded": False,
            "network_fetch_ran": False,
            "actual_loaded_byte_count": None,
            "computed_sha256": None,
            "sniffed_media_type": None,
            "byte_count_within_limit": None,
            "checksum_matches": None,
            "media_type_matches": None,
            "image_decoded": False,
            "pixel_inspection_ran": False,
            "computer_vision_ran": False,
            "ocr_ran": False,
            "candidate_scoring_ran": False,
            "source_report_mutation_ran": False,
            "approval_automation_ran": False,
            "initial_decision": "intake_failed",
            "approval_allowed": False,
        }
    )


def successful_byte_loading_result(record: dict[str, Any], data: bytes, computed_sha256: str, sniffed_media_type: str) -> Mapping[str, Any]:
    snapshot = reference_snapshot(record)
    candidate_id, contract_key = loading_record_identity(record)
    return immutable_result(
        {
            "status": "bytes_loaded",
            "failure_code": None,
            "failure_reason": None,
            "candidate_id": candidate_id,
            "contract_key": contract_key,
            "reference_type": snapshot.get("reference_type"),
            "reference": snapshot.get("reference"),
            "declared_media_type": snapshot.get("media_type"),
            "expected_byte_count": snapshot.get("expected_byte_count"),
            "image_bytes_loaded": True,
            "local_file_opened": False,
            "artifact_downloaded": False,
            "network_fetch_ran": False,
            "actual_loaded_byte_count": len(data),
            "computed_sha256": computed_sha256,
            "sniffed_media_type": sniffed_media_type,
            "byte_count_within_limit": True,
            "checksum_matches": True,
            "media_type_matches": True,
            "image_decoded": False,
            "pixel_inspection_ran": False,
            "computer_vision_ran": False,
            "ocr_ran": False,
            "candidate_scoring_ran": False,
            "source_report_mutation_ran": False,
            "approval_automation_ran": False,
            "initial_decision": "needs_review",
            "approval_allowed": False,
        }
    )


def load_candidate_image_bytes_minimal(record: dict[str, Any], artifact_registry: InMemoryArtifactRegistry) -> Mapping[str, Any]:
    snapshot = reference_snapshot(record)
    policy = policy_snapshot(record)
    reference_type = snapshot.get("reference_type")
    reference = snapshot.get("reference")
    declared_media_type = snapshot.get("media_type")
    expected_sha256 = snapshot.get("image_sha256")
    expected_byte_count = snapshot.get("expected_byte_count")
    max_bytes = policy.get("max_candidate_image_bytes")

    if not isinstance(reference, str) or not reference:
        return safe_failure_result(record, "missing_reference", "Reference must be a non-empty string")
    if reference.startswith(NETWORK_REFERENCE_PREFIXES):
        return safe_failure_result(record, "network_reference_rejected", "HTTP and HTTPS references are not allowed")
    if reference_type != "artifact_uri":
        return safe_failure_result(record, "unsupported_reference_type", "Minimal byte loading accepts artifact_uri only")
    if not reference.startswith("artifact://"):
        return safe_failure_result(record, "unsupported_reference_type", "artifact_uri references must use artifact://")
    if declared_media_type not in SUPPORTED_MEDIA_TYPES:
        return safe_failure_result(record, "unsupported_or_unknown_media_type", "Declared media type is not supported")
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        return safe_failure_result(record, "invalid_expected_checksum", "Expected sha256 must be a 64-character string")
    if not isinstance(expected_byte_count, int) or expected_byte_count < 0:
        return safe_failure_result(record, "invalid_expected_byte_count", "Expected byte count must be a non-negative integer")
    if not isinstance(max_bytes, int) or max_bytes <= 0:
        return safe_failure_result(record, "invalid_max_bytes", "max_candidate_image_bytes must be a positive integer")
    if expected_byte_count > max_bytes:
        return safe_failure_result(record, "expected_byte_count_exceeds_limit", "Expected byte count exceeds max_candidate_image_bytes")

    data = artifact_registry.read_artifact_bytes(reference)
    if data is None:
        return safe_failure_result(record, "artifact_not_found", "Artifact registry did not contain the requested artifact")
    if len(data) != expected_byte_count:
        return safe_failure_result(record, "loaded_byte_count_mismatch", "Loaded byte count did not match expected_byte_count")
    if len(data) > max_bytes:
        return safe_failure_result(record, "loaded_byte_count_exceeds_limit", "Loaded byte count exceeds max_candidate_image_bytes")

    computed_sha256 = hashlib.sha256(data).hexdigest()
    if computed_sha256 != expected_sha256:
        result = dict(safe_failure_result(record, "checksum_mismatch", "Loaded bytes did not match expected sha256"))
        result["actual_loaded_byte_count"] = len(data)
        result["computed_sha256"] = computed_sha256
        result["byte_count_within_limit"] = True
        result["checksum_matches"] = False
        return immutable_result(result)

    sniffed_media_type = sniff_candidate_image_media_type(data)
    if sniffed_media_type not in SUPPORTED_MEDIA_TYPES:
        result = dict(safe_failure_result(record, "unsupported_or_unknown_media_type", "Loaded bytes did not match a supported image signature"))
        result["actual_loaded_byte_count"] = len(data)
        result["computed_sha256"] = computed_sha256
        result["sniffed_media_type"] = sniffed_media_type
        result["byte_count_within_limit"] = True
        result["checksum_matches"] = True
        result["media_type_matches"] = False
        return immutable_result(result)
    if sniffed_media_type != declared_media_type:
        result = dict(safe_failure_result(record, "media_type_mismatch", "Declared media type did not match sniffed media type"))
        result["actual_loaded_byte_count"] = len(data)
        result["computed_sha256"] = computed_sha256
        result["sniffed_media_type"] = sniffed_media_type
        result["byte_count_within_limit"] = True
        result["checksum_matches"] = True
        result["media_type_matches"] = False
        return immutable_result(result)

    return successful_byte_loading_result(record, data, computed_sha256, sniffed_media_type)
