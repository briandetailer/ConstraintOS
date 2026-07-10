import json
from copy import deepcopy
from pathlib import Path

import pytest

from constraintos.candidate_image_fixture_artifact_registry import (
    CandidateImageFixtureArtifactRegistryError,
    build_in_memory_artifact_registry_from_fixture,
    load_fixture_artifact_registry,
    validate_fixture_artifact_registry,
)

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
BASE_REGISTRY = CANDIDATE_DIR / "candidate_image_fixture_artifact_registry.fixture.json"
FAILURE_MATRIX = CANDIDATE_DIR / "candidate_image_fixture_artifact_registry_failure_matrix.fixture.json"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Candidate_Image_Byte_Loading_Fixture_Registry_Failure_Matrix_v1.md"
README = CANDIDATE_DIR / "README.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_path(value: dict, dotted_path: str):
    current = value
    for part in dotted_path.split("."):
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def write_path(value: dict, dotted_path: str, replacement) -> None:
    parts = dotted_path.split(".")
    current = value
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    last = parts[-1]
    if isinstance(current, list):
        current[int(last)] = replacement
    else:
        current[last] = replacement


def mutated_registry_for_case(base_registry: dict, case: dict) -> dict:
    registry = deepcopy(base_registry)
    if "mutation_value_from_path" in case:
        replacement = read_path(registry, case["mutation_value_from_path"])
    else:
        replacement = case["mutation_value"]
    write_path(registry, case["mutation_path"], replacement)
    return registry


def test_failure_matrix_fixture_records_cases_and_guardrails() -> None:
    matrix = load_json(FAILURE_MATRIX)
    header = matrix["candidate_image_fixture_artifact_registry_failure_matrix"]
    guardrails = matrix["guardrails"]
    case_ids = {case["case_id"] for case in matrix["failure_cases"]}

    assert header["status"] == "fixture_only"
    assert header["matrix_state"] == "in_memory_mutation_cases"
    assert header["case_count"] == len(matrix["failure_cases"])
    assert case_ids == {
        "invalid_sha256",
        "invalid_byte_count",
        "invalid_media_type",
        "invalid_artifact_uri",
        "duplicate_artifact_id",
        "duplicate_artifact_uri",
        "descriptor_mutability_violation",
        "local_file_opening_guardrail_violation",
        "network_fetch_guardrail_violation",
        "image_decoding_guardrail_violation",
        "approval_guardrail_violation",
    }
    assert guardrails["failure_cases_are_in_memory_mutations_only"] is True
    assert guardrails["local_file_opening_allowed"] is False
    assert guardrails["artifact_download_allowed"] is False
    assert guardrails["network_fetch_allowed"] is False
    assert guardrails["image_decoding_allowed"] is False
    assert guardrails["failure_can_approve"] is False


@pytest.mark.parametrize("case", load_json(FAILURE_MATRIX)["failure_cases"], ids=lambda case: case["case_id"])
def test_fixture_registry_failure_matrix_cases_fail_closed(case: dict) -> None:
    base_registry = load_json(BASE_REGISTRY)
    registry = mutated_registry_for_case(base_registry, case)

    with pytest.raises(CandidateImageFixtureArtifactRegistryError) as error:
        validate_fixture_artifact_registry(registry)

    assert case["expected_error_contains"] in str(error.value)
    assert case["bytes_exposed_on_failure"] is False


def test_failure_matrix_does_not_build_adapter_for_invalid_cases() -> None:
    base_registry = load_json(BASE_REGISTRY)
    matrix = load_json(FAILURE_MATRIX)

    for case in matrix["failure_cases"]:
        registry = mutated_registry_for_case(base_registry, case)
        with pytest.raises(CandidateImageFixtureArtifactRegistryError):
            validated = validate_fixture_artifact_registry(registry)
            build_in_memory_artifact_registry_from_fixture(validated)


def test_valid_registry_success_case_still_cannot_approve() -> None:
    registry = load_fixture_artifact_registry(BASE_REGISTRY)
    adapter = build_in_memory_artifact_registry_from_fixture(registry)
    header = registry["candidate_image_fixture_artifact_registry"]
    guardrails = registry["guardrails"]

    assert header["approval_allowed"] is False
    assert guardrails["byte_loading_success_can_approve"] is False
    assert adapter.read_artifact_bytes("artifact://external-candidates/perseverance/candidate-0001.png") == bytes.fromhex("89504e470d0a1a0a")


def test_failure_matrix_milestone_records_scope_and_guardrails() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Candidate Image Byte Loading Fixture Registry Failure Matrix v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "matrix_source: fixture-only JSON case list" in content
    assert "bytes_exposed_on_failure: false" in content
    assert "invalid sha256 fixture case" in content
    assert "invalid byte count fixture case" in content
    assert "invalid media type fixture case" in content
    assert "invalid artifact URI fixture case" in content
    assert "duplicate artifact ID fixture case" in content
    assert "duplicate artifact URI fixture case" in content
    assert "descriptor mutability violation fixture case" in content
    assert "No local image file opening." in content
    assert "No network fetch." in content
    assert "No image decoding." in content
    assert "No candidate scoring." in content
    assert "pytest tests/test_candidate_image_byte_loading_fixture_registry_failure_matrix.py" in content


def test_readme_and_command_reference_include_failure_matrix() -> None:
    readme = README.read_text(encoding="utf-8")
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "candidate_image_fixture_artifact_registry_failure_matrix.fixture.json" in readme
    assert "candidate_image_byte_loading_fixture_registry_failure_matrix_status: fixture_only" in readme
    assert "Candidate image byte loading fixture registry failure matrix" in command_reference
    assert "pytest tests/test_candidate_image_byte_loading_fixture_registry_failure_matrix.py" in command_reference
