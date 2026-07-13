from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Constraint_Driven_Graphic_Output_Permutation_POC_v1.md"


def test_constraint_driven_output_permutation_poc_milestone_exists() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "# Constraint-Driven Graphic Output Permutation POC v1" in content
    assert "status: complete" in content
    assert "kickoff_status: complete" in content
    assert "phase_4_browser_demo_status: ready-to-show" in content
    assert "phase_5_feedback_loop_status: complete" in content
    assert "completed_on: 2026-07-13" in content
    assert "Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic" in content
    assert "scenario_key: supra_2jz_gte_twin_turbo" in content


def test_constraint_driven_output_permutation_product_target_is_recorded() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    for item in [
        "input constraints + scenario instructions -> graphic output permutations -> validation evidence -> reviewable result",
        "Produce fixture-safe graphic output permutations or output specifications",
        "Show how each permutation differs",
        "Validate each permutation against explicit requirements",
        "final_decision: needs_review",
        "approval_allowed: false",
    ]:
        assert item in content


def test_constraint_driven_output_permutation_has_toyota_fixture_variants() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    for item in [
        "turbo_system_focus",
        "inline_six_engine_identity_focus",
        "technical_label_density_focus",
        "reviewer_safe_minimal_focus",
        "sequential twin-turbo 2JZ-GTE",
        "not drift into V6, V8, rotary, RB26, LF4, or B58 geometry",
    ]:
        assert item in content


def test_constraint_driven_output_permutation_records_artifacts_and_command() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    for item in [
        ".\\scripts\\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-manifest.json",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-permutations.json",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-validation.json",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-review-packet.json",
        "runs/output-poc/<scenario>/<timestamp>/index.html",
        "runs/output-poc/<scenario>/<timestamp>/run-metadata.json",
    ]:
        assert item in content


def test_constraint_driven_output_permutation_guardrails_are_preserved() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    for item in [
        "No unrestricted image generation",
        "No production artwork generation",
        "No real local image input",
        "No image decoding",
        "No pixel inspection",
        "No automatic approval",
        "requirements are source of truth",
        "uncertainty defaults to needs_review",
        "approval_allowed remains false",
    ]:
        assert item in content


def test_constraint_driven_output_permutation_done_criteria_are_complete() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    for item in [
        "[x] Milestone exists.",
        "[x] Toyota Supra use case is selected.",
        "[x] Corrected product-shaped POC target is recorded.",
        "[x] Demo command is recorded.",
        "[x] Run-folder outputs are recorded.",
        "[x] Implementation phases are complete.",
        "[x] Browser demo is ready to show.",
        "[x] Feedback loop is complete.",
        "[x] Final verification result recorded.",
    ]:
        assert item in content


def test_constraint_driven_output_permutation_records_user_reported_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    for item in [
        "latest_user_reported_constraint_driven_graphic_output_permutation_poc_test_result: 11 passed",
        "command: pytest tests/test_constraint_driven_graphic_output_permutation_poc.py",
        "result: 11 passed",
        "reported_on: 2026-07-13",
        "assistant_ran_tests: false",
    ]:
        assert item in content


def test_constraint_driven_output_permutation_records_phase_status_summary() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    for item in [
        "phase_1_contract_and_data_model: complete",
        "phase_2_deterministic_toyota_fixture_data: complete",
        "phase_3_watch_script: complete",
        "phase_4_browser_business_demo: ready-to-show",
        "phase_5_feedback_loop: complete",
    ]:
        assert item in content


def test_constraint_driven_output_permutation_records_watch_script_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    for item in [
        "latest_user_reported_constraint_driven_graphic_output_permutation_watch_script_test_result: 9 passed",
        "command: pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py",
        "result: 9 passed",
        "reported_on: 2026-07-13",
        "assistant_ran_tests: false",
    ]:
        assert item in content


def test_constraint_driven_output_permutation_records_latest_browser_demo_run() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    for item in [
        "latest_user_reported_constraint_driven_graphic_output_permutation_browser_demo_run_created: true",
        "run_dir: D:\\Code\\ConstraintOS\\runs\\output-poc\\supra_2jz_gte_twin_turbo\\20260712-151228",
        "index_html: D:\\Code\\ConstraintOS\\runs\\output-poc\\supra_2jz_gte_twin_turbo\\20260712-151228\\index.html",
        "final_decision: needs_review",
        "approval_allowed: false",
        "assistant_ran_demo: false",
    ]:
        assert item in content


def test_constraint_driven_output_permutation_records_feedback_loop_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    for item in [
        "feedback_loop: docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Feedback_Loop.md",
        "latest_user_reported_constraint_driven_graphic_output_permutation_feedback_loop_test_result: 6 passed",
        "command: pytest tests/test_constraint_driven_graphic_output_permutation_feedback_loop.py",
        "result: 6 passed",
        "reported_on: 2026-07-13",
        "phase_5_feedback_loop: complete",
        "assistant_ran_tests: false",
    ]:
        assert item in content