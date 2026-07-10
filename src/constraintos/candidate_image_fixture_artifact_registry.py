from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from constraintos.candidate_image_byte_loader import (
    InMemoryArtifactRegistry,
    SUPPORTED_MEDIA_TYPES,
    sniff_candidate_image_media_type,
)
from constraintos.candidate_manifests import CandidateManifestError


DEFAULT_FIXTURE_ARTIFACT_REGISTRY = "candidate_image_fixture_artifact_registry.fixture.json"


class CandidateImageFixtureArtifactRegistryError(CandidateManifestError):
    """Raised when fixture artifact registry data is unsafe or invalid."""


def immutable_mapping(value: dict[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(deepcopy(value))


def parse_hex_bytes(value: str) -> bytes:
    normalized = "".join(value.split()).lower()
    if not normalized:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact data_hex must not be empty")
    try:
        return bytes.fromhex(normalized)
    except ValueError as error:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact data_hex must be valid hexadecimal bytes") from error


def validate_fixture_artifact_descriptor(descriptor: Mapping[str, Any]) -> tuple[str, bytes, Mapping[str, Any]]:
    artifact_id = descriptor.get("artifact_id")
    artifact_uri = descriptor.get("artifact_uri")
    reference_type = descriptor.get("reference_type")
    media_type = descriptor.get("media_type")
    expected_sha256 = descriptor.get("sha256")
    expected_byte_count = descriptor.get("byte_count")
    data_encoding = descriptor.get("data_encoding")
    data_hex = descriptor.get("data_hex")

    if not isinstance(artifact_id, str) or not artifact_id:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor requires artifact_id")
    if not isinstance(artifact_uri, str) or not artifact_uri.startswith("artifact://"):
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor requires artifact:// artifact_uri")
    if reference_type != "artifact_uri":
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor reference_type must be artifact_uri")
    if media_type not in SUPPORTED_MEDIA_TYPES:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor media_type is unsupported")
    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor requires 64-character sha256")
    if not isinstance(expected_byte_count, int) or expected_byte_count <= 0:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor requires positive byte_count")
    if data_encoding != "hex":
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor data_encoding must be hex")
    if not isinstance(data_hex, str):
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor requires data_hex")
    if descriptor.get("descriptor_immutable") is not True:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor must be immutable")
    if descriptor.get("local_file_opened") is not False:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor must not open local files")
    if descriptor.get("artifact_downloaded") is not False:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor must not download artifacts")
    if descriptor.get("network_fetch_ran") is not False:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor must not fetch network resources")
    if descriptor.get("image_decoded") is not False:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor must not decode images")
    if descriptor.get("approval_allowed") is not False:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact descriptor cannot approve candidates")

    data = parse_hex_bytes(data_hex)
    if len(data) != expected_byte_count:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact byte_count does not match data_hex length")
    computed_sha256 = hashlib.sha256(data).hexdigest()
    if computed_sha256 != expected_sha256:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact sha256 does not match data_hex")
    sniffed_media_type = sniff_candidate_image_media_type(data)
    if sniffed_media_type != media_type:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact media_type does not match data signature")

    safe_descriptor = {
        "artifact_id": artifact_id,
        "candidate_key": descriptor.get("candidate_key"),
        "artifact_uri": artifact_uri,
        "reference_type": reference_type,
        "media_type": media_type,
        "sha256": expected_sha256,
        "byte_count": expected_byte_count,
        "data_encoding": data_encoding,
        "descriptor_immutable": True,
        "local_file_opened": False,
        "artifact_downloaded": False,
        "network_fetch_ran": False,
        "image_decoded": False,
        "approval_allowed": False,
    }
    return artifact_uri, data, immutable_mapping(safe_descriptor)


def validate_fixture_artifact_registry(registry: Mapping[str, Any]) -> Mapping[str, Any]:
    header = registry.get("candidate_image_fixture_artifact_registry")
    artifacts = registry.get("artifacts")
    guardrails = registry.get("guardrails")
    if not isinstance(header, Mapping):
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact registry requires header")
    if not isinstance(artifacts, list) or not artifacts:
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact registry requires artifacts")
    if not isinstance(guardrails, Mapping):
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact registry requires guardrails")
    if header.get("status") != "fixture_only":
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact registry status must be fixture_only")
    if header.get("registry_state") != "deterministic_fixture_bytes":
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact registry must use deterministic_fixture_bytes")
    if header.get("artifact_count") != len(artifacts):
        raise CandidateImageFixtureArtifactRegistryError("Fixture artifact registry artifact_count must match artifacts")
    for flag in [
        "local_file_opening_allowed",
        "artifact_download_allowed",
        "network_fetch_allowed",
        "image_decoding_allowed",
        "approval_allowed",
    ]:
        if header.get(flag) is not False:
            raise CandidateImageFixtureArtifactRegistryError(f"Fixture artifact registry header must keep {flag} false")
    for flag in [
        "expected_sha256_required_before_byte_exposure",
        "expected_byte_count_required_before_byte_exposure",
        "declared_media_type_required_before_byte_exposure",
    ]:
        if guardrails.get(flag) is not True:
            raise CandidateImageFixtureArtifactRegistryError(f"Fixture artifact registry guardrail must keep {flag} true")
    for flag in [
        "local_file_opening_allowed",
        "artifact_download_allowed",
        "network_fetch_allowed",
        "image_decoding_allowed",
        "byte_loading_success_can_approve",
    ]:
        if guardrails.get(flag) is not False:
            raise CandidateImageFixtureArtifactRegistryError(f"Fixture artifact registry guardrail must keep {flag} false")

    descriptors = []
    artifact_bytes: dict[str, bytes] = {}
    seen_ids: set[str] = set()
    seen_uris: set[str] = set()
    for descriptor in artifacts:
        if not isinstance(descriptor, Mapping):
            raise CandidateImageFixtureArtifactRegistryError("Fixture artifact registry artifacts must be objects")
        artifact_uri, data, safe_descriptor = validate_fixture_artifact_descriptor(descriptor)
        artifact_id = str(safe_descriptor["artifact_id"])
        if artifact_id in seen_ids:
            raise CandidateImageFixtureArtifactRegistryError("Fixture artifact registry artifact_id values must be unique")
        if artifact_uri in seen_uris:
            raise CandidateImageFixtureArtifactRegistryError("Fixture artifact registry artifact_uri values must be unique")
        seen_ids.add(artifact_id)
        seen_uris.add(artifact_uri)
        artifact_bytes[artifact_uri] = data
        descriptors.append(dict(safe_descriptor))

    return immutable_mapping(
        {
            "candidate_image_fixture_artifact_registry": dict(header),
            "artifacts": descriptors,
            "guardrails": dict(guardrails),
            "_artifact_bytes": artifact_bytes,
        }
    )


def load_fixture_artifact_registry(path: Path) -> Mapping[str, Any]:
    return validate_fixture_artifact_registry(json.loads(path.read_text(encoding="utf-8")))


def resolve_fixture_artifact_registry_path(candidate_dir: Path, fixture_registry: str | None = None) -> Path:
    if fixture_registry:
        return Path(fixture_registry).resolve()
    return candidate_dir / DEFAULT_FIXTURE_ARTIFACT_REGISTRY


def build_in_memory_artifact_registry_from_fixture(registry: Mapping[str, Any]) -> InMemoryArtifactRegistry:
    artifact_bytes = registry.get("_artifact_bytes")
    if not isinstance(artifact_bytes, Mapping):
        raise CandidateImageFixtureArtifactRegistryError("Validated fixture artifact registry missing byte map")
    return InMemoryArtifactRegistry({str(uri): bytes(data) for uri, data in artifact_bytes.items()})


def build_fixture_artifact_registry_report(registry: Mapping[str, Any], registry_path: Path | None = None) -> Mapping[str, Any]:
    header = registry.get("candidate_image_fixture_artifact_registry", {})
    artifacts = registry.get("artifacts", [])
    return immutable_mapping(
        {
            "candidate_image_fixture_artifact_registry": {
                "mode": "fixture_only",
                "registry_path": str(registry_path) if registry_path else None,
                "artifact_count": header.get("artifact_count") if isinstance(header, Mapping) else None,
                "local_file_opening": "not_run",
                "artifact_download": "not_run",
                "network_fetch": "not_run",
                "image_decoding": "not_run",
                "approval_allowed": False,
            },
            "artifacts": artifacts if isinstance(artifacts, list) else [],
        }
    )
