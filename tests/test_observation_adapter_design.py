import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN_DOC = ROOT / "docs" / "500_Milestones" / "Observation_Adapter_Design_v1.md"
DESIGN_FIXTURE = ROOT / "examples" / "graphics" / "candidate_evaluation" / "observation_adapter.design.json"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def load_design_fixture() -> dict:
    value = json.loads(DESIGN_FIXTURE.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_observation_adapter_design_fixture_is_design_only() -> None:
    fixture = load_design_fixture()

    assert fixture["design"]["domain"] == "graphics_validation"
    assert fixture["design"]["status"] == "design_only"
    assert fixture["design"]["implementation_status"] == "not_started"


def test_observation_adapter_design_blocks_premature_runtime_work() -> None:
    guardrails = load_design_fixture()["guardrails"]

    assert guardrails["real_candidate_image_loading_allowed"] is False
    assert guardrails["computer_vision_provider_allowed"] is False
    assert guardrails["ocr_provider_allowed"] is False
    assert guardrails["image_generation_allowed"] is False
    assert guardrails["image_editing_allowed"] is False
    assert guardrails["approval_automation_change_allowed"] is False


def test_observation_adapter_design_defines_source_taxonomy() -> None:
    sources = {item["source_type"]: item for item in load_design_fixture()["source_taxonomy"]}

    assert set(sources) == {
        "manual_human_review",
        "metadata_only",
        "machine_assisted_placeholder",
        "external_claim",
    }
    assert sources["manual_human_review"]["availability"] == "allowed_first"
    assert sources["machine_assisted_placeholder"]["availability"] == "design_only_not_implemented"
    assert all(item["approval_capability"] == "cannot_approve_alone" for item in sources.values())


def test_observation_adapter_design_defines_normalized_item_shape() -> None:
    item = load_design_fixture()["normalized_observation_item"]

    assert "observation_id" in item["required_fields"]
    assert "constraint_id" in item["required_fields"]
    assert "source_type" in item["required_fields"]
    assert "observed_status" in item["required_fields"]
    assert "confidence" in item["required_fields"]
    assert item["observed_status_values"] == [
        "satisfied",
        "missing",
        "ambiguous",
        "contradicted",
        "not_observed",
    ]
    assert item["confidence_range"] == {"minimum": 0, "maximum": 1}


def test_observation_adapter_design_preserves_non_approval_defaults() -> None:
    fixture = load_design_fixture()
    rules = fixture["decision_safety_rules"]

    assert fixture["guardrails"]["uncertainty_default"] == "needs_review"
    assert fixture["guardrails"]["low_confidence_default"] == "needs_review"
    assert rules["low_confidence_satisfied_observations_allow_approval"] is False
    assert rules["ambiguous_observations_decision"] == "needs_review"
    assert rules["missing_required_evidence_decision"] == "needs_review"
    assert rules["manual_observations_can_approve_alone"] is False
    assert rules["machine_assisted_observations_can_approve_alone"] is False
    assert rules["metadata_only_observations_can_approve_alone"] is False
    assert rules["external_claims_can_approve_alone"] is False


def test_observation_adapter_design_sets_next_gate() -> None:
    gate = load_design_fixture()["future_gate"]

    assert gate["recommended_next_milestone"] == "Manual Observation Fixture Adapter v1"
    assert "real_image_ingestion" in gate["blocked_until_later"]
    assert "computer_vision_provider_integration" in gate["blocked_until_later"]
    assert "approval_automation_change" in gate["blocked_until_later"]


def test_observation_adapter_design_doc_matches_gate_and_guardrails() -> None:
    content = DESIGN_DOC.read_text(encoding="utf-8")

    assert "milestone: Observation Adapter Design v1" in content
    assert "previous_gate: Foundation Readiness Review v1 complete" in content
    assert "recommended_next_milestone: Manual Observation Fixture Adapter v1" in content
    assert "No real image loading or decoding." in content
    assert "Low-confidence or incomplete observations default to needs_review." in content


def test_command_reference_includes_observation_adapter_design_verification() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Observation adapter design" in content
    assert "pytest tests/test_observation_adapter_design.py" in content
