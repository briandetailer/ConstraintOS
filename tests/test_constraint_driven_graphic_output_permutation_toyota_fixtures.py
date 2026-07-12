from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "docs" / "800_Demos" / "Constraint_Driven_Graphic_Output_Permutation_POC_Toyota_Fixtures.md"
CONTRACT = ROOT / "docs" / "800_Demos" / "Constraint_Driven_Graphic_Output_Permutation_POC_Contract.md"


def test_toyota_output_permutation_fixture_doc_exists() -> None:
    content = FIXTURES.read_text(encoding="utf-8")

    expected = [
        "# Constraint-Driven Graphic Output Permutation POC Toyota Fixtures",
        "status: fixture-data-defined",
        "phase: Phase 2 - deterministic Toyota fixture data",
        "phase_status: complete",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: deterministic-fixture-data-only",
    ]
    for item in expected:
        assert item in content


def test_toyota_output_permutation_fixture_records_all_four_variants() -> None:
    content = FIXTURES.read_text(encoding="utf-8")

    expected = [
        "permutation_id: turbo_system_focus",
        "permutation_id: inline_six_engine_identity_focus",
        "permutation_id: technical_label_density_focus",
        "permutation_id: reviewer_safe_minimal_focus",
        "Sequential twin-turbo system focus",
        "2JZ-GTE inline-six identity focus",
        "Technical label-density focus",
        "Reviewer-safe minimal focus",
        "permutation_count: 4",
    ]
    for item in expected:
        assert item in content


def test_toyota_output_permutation_fixtures_reference_required_constraints() -> None:
    content = FIXTURES.read_text(encoding="utf-8")

    expected = [
        "Toyota Supra Mk IV / A80 identity",
        "2JZ-GTE inline-six identity",
        "sequential twin-turbo system",
        "not generic engine",
        "not V6",
        "not V8",
        "not rotary",
        "not RB26",
        "not LF4",
        "not B58",
        "technical graphic / publishing context",
        "uncertainty defaults to needs_review",
        "approval_allowed remains false",
    ]
    for item in expected:
        assert item in content


def test_toyota_output_permutation_fixtures_include_business_intent_and_risk_fields() -> None:
    content = FIXTURES.read_text(encoding="utf-8")

    expected = [
        "business_intent:",
        "visual_strategy:",
        "known_risks:",
        "explicit_non_goals:",
        "placeholder_artifact:",
        "expected_review_state: needs_review",
        "review_decision: needs_review",
        "approval_allowed: false",
    ]
    for item in expected:
        assert item in content


def test_toyota_output_permutation_fixtures_use_placeholder_identifiers_not_real_artwork_paths() -> None:
    content = FIXTURES.read_text(encoding="utf-8")

    expected = [
        "fixture-placeholder://output-poc/supra/turbo-system-focus",
        "fixture-placeholder://output-poc/supra/inline-six-identity-focus",
        "fixture-placeholder://output-poc/supra/technical-label-density-focus",
        "fixture-placeholder://output-poc/supra/reviewer-safe-minimal-focus",
    ]
    for item in expected:
        assert item in content

    forbidden_runtime_authority = [
        "source_image_path:",
        "generated_image_path:",
        "production_artwork_path:",
        "pixel_data:",
        "ocr_text:",
        "cv_provider:",
        "auto_approved:",
    ]
    for item in forbidden_runtime_authority:
        assert item not in content


def test_toyota_output_permutation_fixtures_preserve_guardrails() -> None:
    content = FIXTURES.read_text(encoding="utf-8")

    expected = [
        "Fixture data only.",
        "No generated final graphics.",
        "No production artwork generation.",
        "No real local image input.",
        "No artifact download.",
        "No network fetch.",
        "No image decoding.",
        "No pixel inspection.",
        "No CV/OCR provider integration.",
        "No automatic approval.",
    ]
    for item in expected:
        assert item in content


def test_toyota_output_permutation_phase_2_done_criteria_are_defined() -> None:
    content = FIXTURES.read_text(encoding="utf-8")

    expected = [
        "[x] Toyota fixture data document exists.",
        "[x] Four permutation records are defined.",
        "[x] Each permutation includes business intent.",
        "[x] Each permutation includes visual strategy.",
        "[x] Each permutation references Toyota Supra / 2JZ-GTE constraints.",
        "[x] Each permutation includes known risks.",
        "[x] Each permutation includes explicit non-goals.",
        "[x] Each permutation uses a placeholder artifact identifier.",
        "[x] Each permutation defaults to needs_review.",
        "[x] approval_allowed remains false.",
        "[x] Guardrails are preserved.",
        "[x] Verification test result recorded.",
    ]
    for item in expected:
        assert item in content


def test_toyota_output_permutation_fixture_data_records_verification() -> None:
    content = FIXTURES.read_text(encoding="utf-8")

    expected = [
        "latest_user_reported_constraint_driven_graphic_output_permutation_toyota_fixtures_test_result: 8 passed",
        "source: user-reported local test run",
        "command: pytest tests/test_constraint_driven_graphic_output_permutation_toyota_fixtures.py",
        "result: 8 passed",
        "assistant_ran_tests: false",
    ]
    for item in expected:
        assert item in content


def test_toyota_output_permutation_fixture_data_follows_phase_1_contract() -> None:
    fixture_content = FIXTURES.read_text(encoding="utf-8")
    contract_content = CONTRACT.read_text(encoding="utf-8")

    for item in [
        "turbo_system_focus",
        "inline_six_engine_identity_focus",
        "technical_label_density_focus",
        "reviewer_safe_minimal_focus",
        "placeholder_artifact",
        "expected_review_state",
    ]:
        assert item in fixture_content
        assert item in contract_content
