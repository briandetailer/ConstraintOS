from pathlib import Path

import pytest

from constraintos.graphics_contracts import (
    GraphicsContractError,
    load_json,
    validate_contract_schema,
    validate_perseverance_contract_consistency,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "examples" / "graphics" / "contracts"
PERSEVERANCE_DIR = ROOT / "examples" / "graphics" / "perseverance"


def test_perseverance_contract_satisfies_reusable_schema() -> None:
    schema = load_json(CONTRACT_DIR / "graphics_validation_contract.schema.json")
    contract = load_json(CONTRACT_DIR / "perseverance.contract.json")

    validate_contract_schema(contract, schema)


def test_perseverance_contract_declares_reusable_graphics_contract_fields() -> None:
    contract = load_json(CONTRACT_DIR / "perseverance.contract.json")

    assert contract["contract"]["domain"] == "graphics_validation"
    assert contract["contract"]["mode"] == "fixture_only_no_image_generation"
    assert contract["subject"]["name"] == "NASA Perseverance rover"
    assert contract["rendering_requirements"]["view"] == "front-left three-quarter view"
    assert contract["decision_policy"]["allowed_decisions"] == ["approved", "needs_review", "rejected"]
    assert contract["decision_policy"]["uncertainty_default"] == "needs_review"
    assert contract["approval_contract"]["expected_initial_decision"] == "needs_review"


def test_perseverance_contract_preserves_required_labels_and_forbidden_substitutions() -> None:
    contract = load_json(CONTRACT_DIR / "perseverance.contract.json")

    required_labels = set(contract["required_labels"])
    forbidden_substitutions = set(contract["subject"]["forbidden_substitutions"])

    assert {"Mastcam-Z", "SuperCam", "MEDA", "MOXIE", "PIXL", "RIMFAX", "SHERLOC"}.issubset(required_labels)
    assert {"robotic arm", "wheels", "mast", "chassis"}.issubset(required_labels)
    assert {"Curiosity rover", "generic Mars rover", "lunar rover", "tank tracks", "solar panels"}.issubset(forbidden_substitutions)


def test_perseverance_contract_preserves_evidence_and_approval_guardrails() -> None:
    contract = load_json(CONTRACT_DIR / "perseverance.contract.json")

    label_trace = contract["evidence_contract"]["required_label_trace"]
    assert label_trace["MOXIE"] == "internal/body-mounted technology payload"
    assert label_trace["RIMFAX"] == "lower/rear underside antenna region"
    assert "verify_uncertainty_marked_needs_review" in contract["evidence_contract"]["required_checks"]
    assert contract["approval_contract"]["guardrail"] == "Uncertainty must produce needs_review, not approval."


def test_perseverance_contract_is_consistent_with_existing_fixtures() -> None:
    contract = load_json(CONTRACT_DIR / "perseverance.contract.json")
    spec = load_json(PERSEVERANCE_DIR / "spec.json")
    policy = load_json(PERSEVERANCE_DIR / "policy.json")
    expected_evidence = load_json(PERSEVERANCE_DIR / "expected_evidence.json")
    expected_approval = load_json(PERSEVERANCE_DIR / "expected_approval.json")

    validate_perseverance_contract_consistency(contract, spec, policy, expected_evidence, expected_approval)


def test_perseverance_contract_consistency_rejects_label_drift() -> None:
    contract = load_json(CONTRACT_DIR / "perseverance.contract.json")
    spec = load_json(PERSEVERANCE_DIR / "spec.json")
    policy = load_json(PERSEVERANCE_DIR / "policy.json")
    expected_evidence = load_json(PERSEVERANCE_DIR / "expected_evidence.json")
    expected_approval = load_json(PERSEVERANCE_DIR / "expected_approval.json")
    contract["required_labels"] = [label for label in contract["required_labels"] if label != "RIMFAX"]

    with pytest.raises(GraphicsContractError, match="required_labels mismatch"):
        validate_perseverance_contract_consistency(contract, spec, policy, expected_evidence, expected_approval)
