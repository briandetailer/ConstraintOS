from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "docs" / "500_Milestones" / "Foundation_Readiness_Review_v1.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


REQUIRED_FOUNDATION_LAYERS = [
    "Runtime Package Artifact Handoff",
    "NASA Perseverance graphics-validation fixture",
    "Reusable Graphics Validation Contracts v1",
    "Additional Graphics Contract Instances v1",
    "Graphics Contract CLI Discovery v1",
    "Graphics Contract Runtime Bridge v1",
    "Graphics Contract Runtime Watch v1",
    "Graphics Contract Watch Capture v1",
    "Candidate Evaluation Adapter Design v1",
    "Candidate Manifest Schema v1",
    "Candidate Manifest Discovery v1",
    "Candidate Evaluation Report Contract v1",
    "Fixture-only Candidate Evaluation v1",
]


def review_content() -> str:
    return REVIEW.read_text(encoding="utf-8")


def test_foundation_readiness_review_exists_and_is_pending_verification() -> None:
    content = review_content()

    assert "milestone: Foundation Readiness Review v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "previous_gate: Fixture-only Candidate Evaluation v1 complete" in content
    assert "track: Foundation Completion Track" in content


def test_foundation_readiness_review_lists_completed_layers() -> None:
    content = review_content()

    for layer in REQUIRED_FOUNDATION_LAYERS:
        assert f"[x] {layer}" in content


def test_foundation_readiness_review_blocks_premature_real_image_work() -> None:
    content = review_content()

    assert "real_image_ingestion_status: not_ready" in content
    assert "computer_vision_integration_status: not_ready" in content
    assert "image_generation_integration_status: not_ready" in content
    assert "approval_automation_status: not_ready" in content
    assert "No real image loading or decoding." in content
    assert "No computer-vision integration." in content
    assert "No image generation integration." in content
    assert "No automatic approval of generated candidates." in content


def test_foundation_readiness_review_allows_only_observation_adapter_design_next() -> None:
    content = review_content()

    assert "next_allowed_milestone: Observation Adapter Design v1" in content
    assert "decision: proceed_to_observation_adapter_design_only" in content
    assert "Before real candidate image ingestion, the project must define an observation adapter boundary." in content
    assert "Explicit non-approval default for low-confidence observations" in content


def test_command_reference_includes_foundation_readiness_review_verification() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Foundation readiness review" in content
    assert "pytest tests/test_foundation_readiness_review.py" in content
