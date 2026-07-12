from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "800_Demos" / "Constraint_Driven_Graphic_Output_Permutation_POC_Contract.md"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Constraint_Driven_Graphic_Output_Permutation_POC_v1.md"


def test_output_permutation_contract_exists_and_is_fixture_safe() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "# Constraint-Driven Graphic Output Permutation POC Contract",
        "status: contract-defined",
        "phase: Phase 1 - contract and data model",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: fixture-safe-output-specifications-only",
        "The POC may define output specifications.",
        "The POC must not generate production artwork.",
        "The POC must not inspect or decode real images.",
        "The POC must not approve candidates automatically.",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_contract_defines_allowed_artifact_set() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "graphic-output-manifest.json",
        "graphic-output-permutations.json",
        "graphic-output-validation.json",
        "graphic-output-review-packet.json",
        "index.html",
        "run-metadata.json",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_contract_defines_required_shapes() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "Required top-level fields:",
        "permutation_id",
        "variant_name",
        "business_intent",
        "visual_strategy",
        "required_constraints",
        "emphasized_constraints",
        "known_risks",
        "explicit_non_goals",
        "placeholder_artifact",
        "expected_review_state",
        "permutation_results",
        "satisfied_constraints",
        "missing_constraints",
        "uncertain_constraints",
        "blocked_claims",
        "review_decision",
        "why_approval_is_blocked",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_contract_defines_toyota_baseline_constraints_and_variants() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

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
        "turbo_system_focus",
        "inline_six_engine_identity_focus",
        "technical_label_density_focus",
        "reviewer_safe_minimal_focus",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_contract_defines_decision_and_approval_semantics() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "pass:",
        "needs_review:",
        "fail:",
        "approval_allowed: false",
        "A fixture-safe output specification leaves a constraint uncertain.",
        "A fixture-safe output specification contradicts a required constraint.",
        "The POC may compare permutations, but approval must remain blocked",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_contract_blocks_real_image_and_auto_approval_fields() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "Forbidden field names:",
        "local_file_path",
        "file_uri",
        "source_image_path",
        "generated_image_path",
        "production_artwork_path",
        "pixel_data",
        "ocr_text",
        "cv_provider",
        "auto_approved",
        "No unrestricted image generation.",
        "No production artwork generation.",
        "No real local image input.",
        "No image decoding.",
        "No pixel inspection.",
        "No CV/OCR provider integration.",
        "No automatic approval.",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_milestone_records_kickoff_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "kickoff_status: complete",
        "latest_user_reported_constraint_driven_graphic_output_permutation_poc_test_result: 4 passed",
        "source: user-reported local test run",
        "command: pytest tests/test_constraint_driven_graphic_output_permutation_poc.py",
        "result: 4 passed",
        "[x] Verification test result recorded.",
    ]
    for item in expected:
        assert item in content
