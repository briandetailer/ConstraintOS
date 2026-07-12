from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Constraint_Driven_Graphic_Output_Permutation_POC_v1.md"


def test_constraint_driven_output_permutation_poc_milestone_exists() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "# Constraint-Driven Graphic Output Permutation POC v1" in content
    assert "status: kickoff-ready" in content
    assert "kickoff_status: complete" in content
    assert "phase_3_watch_script_status: complete" in content
    assert "phase_4_browser_demo_status: active" in content
    assert "Business Demo UI Toyota Supra" in content
    assert "Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic" in content
    assert "scenario_key: supra_2jz_gte_twin_turbo" in content


def test_constraint_driven_output_permutation_product_target_is_recorded() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "input constraints + scenario instructions -> graphic output permutations -> validation evidence -> reviewable result",
        "Produce fixture-safe graphic output permutations or output specifications",
        "Show how each permutation differs",
        "Validate each permutation against explicit requirements",
        "Preserve traceability from requirement -> permutation -> evidence -> review decision",
        "final_decision: needs_review",
        "approval_allowed: false",
    ]
    for item in expected:
        assert item in content


def test_constraint_driven_output_permutation_has_toyota_fixture_variants() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "turbo_system_focus",
        "inline_six_engine_identity_focus",
        "technical_label_density_focus",
        "reviewer_safe_minimal_focus",
        "sequential twin-turbo 2JZ-GTE",
        "not drift into V6, V8, rotary, RB26, LF4, or B58 geometry",
    ]
    for item in expected:
        assert item in content


def test_constraint_driven_output_permutation_records_proposed_artifacts_and_command() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        ".\\scripts\\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-manifest.json",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-permutations.json",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-validation.json",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-review-packet.json",
        "runs/output-poc/<scenario>/<timestamp>/index.html",
        "runs/output-poc/<scenario>/<timestamp>/run-metadata.json",
    ]
    for item in expected:
        assert item in content


def test_constraint_driven_output_permutation_guardrails_are_preserved() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "No unrestricted image generation",
        "No production artwork generation",
        "No real local image input",
        "No local_file_path loading",
        "No file_uri loading",
        "No artifact download",
        "No network fetch",
        "No image decoding",
        "No pixel inspection",
        "No CV/OCR provider integration",
        "No automatic scoring beyond deterministic fixture-safe validation",
        "No automatic approval",
        "requirements are source of truth",
        "uncertainty defaults to needs_review",
        "approval_allowed remains false",
    ]
    for item in expected:
        assert item in content


def test_constraint_driven_output_permutation_kickoff_done_criteria_are_defined() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "[x] Milestone exists.",
        "[x] Toyota Supra use case is selected.",
        "[x] Corrected product-shaped POC target is recorded.",
        "[x] Fixture-safe output permutations are explicitly allowed.",
        "[x] Production generated graphics remain out of scope.",
        "[x] Proposed command is recorded.",
        "[x] Proposed run-folder outputs are recorded.",
        "[x] Implementation phases are defined.",
        "[x] Guardrails are preserved.",
        "[x] Verification test result recorded.",
    ]
    for item in expected:
        assert item in content


def test_constraint_driven_output_permutation_records_user_reported_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "source: user-reported local test run",
        "command: pytest tests/test_constraint_driven_graphic_output_permutation_poc.py",
        "result: 4 passed",
        "assistant_ran_tests: false",
    ]
    for item in expected:
        assert item in content


def test_constraint_driven_output_permutation_records_phase_status_summary() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "phase_1_contract_and_data_model: complete",
        "phase_2_deterministic_toyota_fixture_data: complete",
        "phase_3_watch_script: complete",
        "phase_4_browser_business_demo: active",
        "phase_5_feedback_loop: pending",
    ]
    for item in expected:
        assert item in content


def test_constraint_driven_output_permutation_records_watch_script_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "latest_user_reported_constraint_driven_graphic_output_permutation_watch_script_test_result: 8 passed",
        "command: pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py",
        "result: 8 passed",
        "reported_on: 2026-07-10",
        "assistant_ran_tests: false",
    ]
    for item in expected:
        assert item in content
