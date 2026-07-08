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
CONTRACT_FILES = [
    "perseverance.contract.json",
    "wind_turbine_nacelle.contract.json",
    "hydroelectric_dam_powerhouse.contract.json",
    "supra_2jz_gte_twin_turbo.contract.json",
]


def contract(name: str) -> dict:
    return load_json(CONTRACT_DIR / name)


@pytest.mark.parametrize("contract_file", CONTRACT_FILES)
def test_graphics_contract_satisfies_reusable_schema(contract_file: str) -> None:
    schema = load_json(CONTRACT_DIR / "graphics_validation_contract.schema.json")

    validate_contract_schema(contract(contract_file), schema)


@pytest.mark.parametrize("contract_file", CONTRACT_FILES)
def test_graphics_contract_declares_reusable_fixture_only_fields(contract_file: str) -> None:
    subject_contract = contract(contract_file)

    assert subject_contract["contract"]["domain"] == "graphics_validation"
    assert subject_contract["contract"]["mode"] == "fixture_only_no_image_generation"
    assert subject_contract["decision_policy"]["allowed_decisions"] == ["approved", "needs_review", "rejected"]
    assert subject_contract["decision_policy"]["uncertainty_default"] == "needs_review"
    assert subject_contract["approval_contract"]["expected_initial_decision"] == "needs_review"
    assert subject_contract["approval_contract"]["guardrail"] == "Uncertainty must produce needs_review, not approval."


@pytest.mark.parametrize("contract_file", CONTRACT_FILES)
def test_graphics_contract_required_labels_have_label_trace(contract_file: str) -> None:
    subject_contract = contract(contract_file)

    required_labels = set(subject_contract["required_labels"])
    label_trace = set(subject_contract["evidence_contract"]["required_label_trace"].keys())
    assert required_labels == label_trace


def test_perseverance_contract_preserves_required_labels_and_forbidden_substitutions() -> None:
    subject_contract = contract("perseverance.contract.json")

    required_labels = set(subject_contract["required_labels"])
    forbidden_substitutions = set(subject_contract["subject"]["forbidden_substitutions"])

    assert {"Mastcam-Z", "SuperCam", "MEDA", "MOXIE", "PIXL", "RIMFAX", "SHERLOC"}.issubset(required_labels)
    assert {"robotic arm", "wheels", "mast", "chassis"}.issubset(required_labels)
    assert {"Curiosity rover", "generic Mars rover", "lunar rover", "tank tracks", "solar panels"}.issubset(forbidden_substitutions)


def test_wind_turbine_contract_preserves_drivetrain_guardrails() -> None:
    subject_contract = contract("wind_turbine_nacelle.contract.json")

    required_labels = set(subject_contract["required_labels"])
    forbidden_substitutions = set(subject_contract["subject"]["forbidden_substitutions"])
    geometry = "\n".join(subject_contract["constraint_groups"]["geometry"])

    assert {"rotor", "hub", "low-speed shaft", "gearbox", "high-speed shaft", "generator", "yaw system"}.issubset(required_labels)
    assert {"vertical-axis wind turbine", "small residential turbine", "solar panels", "combustion engine"}.issubset(forbidden_substitutions)
    assert "Blade count must remain three" in geometry
    assert "Gearbox must sit between low-speed shaft and generator" in geometry


def test_hydroelectric_contract_preserves_process_flow_guardrails() -> None:
    subject_contract = contract("hydroelectric_dam_powerhouse.contract.json")

    required_labels = set(subject_contract["required_labels"])
    forbidden_substitutions = set(subject_contract["subject"]["forbidden_substitutions"])
    geometry = "\n".join(subject_contract["constraint_groups"]["geometry"])

    assert {"reservoir", "dam wall", "intake", "penstock", "turbine", "generator", "spillway", "tailrace", "water-flow arrows"}.issubset(required_labels)
    assert {"coal power plant", "nuclear power plant", "combustion engine", "smokestack"}.issubset(forbidden_substitutions)
    assert "Reservoir must be upstream and higher" in geometry
    assert "Spillway must be distinct from the penstock/turbine path" in geometry


def test_supra_contract_preserves_engine_and_turbo_guardrails() -> None:
    subject_contract = contract("supra_2jz_gte_twin_turbo.contract.json")

    required_labels = set(subject_contract["required_labels"])
    forbidden_substitutions = set(subject_contract["subject"]["forbidden_substitutions"])
    geometry = "\n".join(subject_contract["constraint_groups"]["geometry"])

    assert {"2JZ-GTE inline-six", "primary turbocharger", "secondary turbocharger", "intercooler", "intake charge path", "exhaust flow path"}.issubset(required_labels)
    assert {"Nissan Skyline GT-R", "Mazda RX-7", "newer GR Supra", "RB26DETT", "B58", "single-turbo swap"}.issubset(forbidden_substitutions)
    assert "The engine must be an inline-six layout" in geometry
    assert "The system must distinguish primary and secondary turbocharger function" in geometry


def test_perseverance_contract_preserves_evidence_and_approval_guardrails() -> None:
    subject_contract = contract("perseverance.contract.json")

    label_trace = subject_contract["evidence_contract"]["required_label_trace"]
    assert label_trace["MOXIE"] == "internal/body-mounted technology payload"
    assert label_trace["RIMFAX"] == "lower/rear underside antenna region"
    assert "verify_uncertainty_marked_needs_review" in subject_contract["evidence_contract"]["required_checks"]
    assert subject_contract["approval_contract"]["guardrail"] == "Uncertainty must produce needs_review, not approval."


def test_perseverance_contract_is_consistent_with_existing_fixtures() -> None:
    subject_contract = contract("perseverance.contract.json")
    spec = load_json(PERSEVERANCE_DIR / "spec.json")
    policy = load_json(PERSEVERANCE_DIR / "policy.json")
    expected_evidence = load_json(PERSEVERANCE_DIR / "expected_evidence.json")
    expected_approval = load_json(PERSEVERANCE_DIR / "expected_approval.json")

    validate_perseverance_contract_consistency(subject_contract, spec, policy, expected_evidence, expected_approval)


def test_perseverance_contract_consistency_rejects_label_drift() -> None:
    subject_contract = contract("perseverance.contract.json")
    spec = load_json(PERSEVERANCE_DIR / "spec.json")
    policy = load_json(PERSEVERANCE_DIR / "policy.json")
    expected_evidence = load_json(PERSEVERANCE_DIR / "expected_evidence.json")
    expected_approval = load_json(PERSEVERANCE_DIR / "expected_approval.json")
    subject_contract["required_labels"] = [label for label in subject_contract["required_labels"] if label != "RIMFAX"]

    with pytest.raises(GraphicsContractError, match="required_labels mismatch"):
        validate_perseverance_contract_consistency(subject_contract, spec, policy, expected_evidence, expected_approval)
