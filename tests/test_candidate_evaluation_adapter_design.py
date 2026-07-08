import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN_DOC = ROOT / "docs" / "700_Use_Cases" / "Candidate_Evaluation_Adapter_Design.md"
DESIGN_FIXTURE = ROOT / "examples" / "graphics" / "candidate_evaluation" / "candidate_evaluation_adapter.design.json"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def load_design() -> dict:
    return json.loads(DESIGN_FIXTURE.read_text(encoding="utf-8"))


def test_candidate_evaluation_design_fixture_exists_and_is_design_only() -> None:
    payload = load_design()

    assert payload["design"]["status"] == "design_only"
    assert payload["design"]["implementation_status"] == "not_started"
    assert payload["design"]["domain"] == "graphics_validation"


def test_candidate_evaluation_design_disallows_image_generation_and_real_ingestion() -> None:
    guardrails = load_design()["guardrails"]

    assert guardrails["image_generation_allowed"] is False
    assert guardrails["image_editing_allowed"] is False
    assert guardrails["real_candidate_image_ingestion_allowed"] is False
    assert guardrails["computer_vision_integration_allowed"] is False
    assert guardrails["approval_automation_change_allowed"] is False
    assert guardrails["candidate_images_are_external_inputs"] is True


def test_candidate_evaluation_design_preserves_uncertainty_and_decisions() -> None:
    payload = load_design()
    guardrails = payload["guardrails"]
    decision = payload["decision_contract"]

    assert guardrails["uncertainty_default"] == "needs_review"
    assert decision["allowed_decisions"] == ["approved", "needs_review", "rejected"]
    assert decision["missing_evidence_decision"] == "needs_review"
    assert decision["ambiguous_evidence_decision"] == "needs_review"
    assert decision["contradicted_required_constraint_decision"] == "rejected"


def test_candidate_evaluation_design_defines_manifest_and_evidence_boundaries() -> None:
    payload = load_design()

    assert payload["candidate_manifest_contract"]["required_fields"] == [
        "candidate_id",
        "contract_key",
        "candidate_reference",
        "candidate_source",
        "submitted_at",
    ]
    assert "image_sha256" in payload["candidate_manifest_contract"]["recommended_fields"]
    assert payload["evidence_item_contract"]["allowed_observed_statuses"] == [
        "satisfied",
        "missing",
        "ambiguous",
        "contradicted",
        "not_observed",
    ]


def test_candidate_evaluation_design_stages_are_ordered() -> None:
    stages = load_design()["adapter_stages"]

    assert stages[0] == "ingest_candidate_manifest"
    assert stages[1] == "validate_candidate_manifest"
    assert stages[-1] == "recommend_approval_decision"
    assert "request_observation_evidence" in stages
    assert "build_evidence_report" in stages


def test_candidate_evaluation_design_doc_marks_future_command_as_unavailable() -> None:
    content = DESIGN_DOC.read_text(encoding="utf-8")

    assert "status: design_only" in content
    assert "image_generation: not_allowed" in content
    assert "cos-graphics-candidate evaluate <candidate-manifest>" in content
    assert "That command is not available in this milestone." in content


def test_future_command_proposal_requires_command_reference_update() -> None:
    proposals = load_design()["future_command_proposals"]

    assert proposals == [
        {
            "command": "cos-graphics-candidate evaluate <candidate-manifest>",
            "status": "proposed_not_available",
            "requires_command_reference_update_before_implementation": True,
        }
    ]


def test_command_reference_includes_candidate_evaluation_design_verification() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Candidate evaluation adapter design" in content
    assert "pytest tests/test_candidate_evaluation_adapter_design.py" in content
