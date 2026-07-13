from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "800_Demos" / "Constraint_Driven_Graphic_Output_Permutation_POC_Reviewer_Handoff.md"


def test_output_permutation_reviewer_handoff_identifies_generated_index_html() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "# Constraint-Driven Graphic Output Permutation POC Reviewer Handoff",
        "status: ready-to-show",
        "scripts/watch-constraintos-output-poc.ps1",
        "runs/output-poc/supra_2jz_gte_twin_turbo/<timestamp>/index.html",
        "D:\\Code\\ConstraintOS\\runs\\output-poc\\supra_2jz_gte_twin_turbo\\20260712-151228\\index.html",
        "The `-OpenBrowser` flag opens the generated `index.html` automatically.",
        "Do not point a non-technical reviewer directly at the PowerShell script, JSON files, or source documents",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_reviewer_handoff_lists_viewer_expectations() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "Toyota Supra A80 / 2JZ-GTE twin-turbo use case",
        "A visible four-step walkthrough:",
        "1. Constraints loaded",
        "2. Output permutations",
        "3. Deterministic validation",
        "4. needs_review",
        "turbo_system_focus",
        "inline_six_engine_identity_focus",
        "technical_label_density_focus",
        "reviewer_safe_minimal_focus",
        "final_decision: needs_review",
        "approval_allowed: false",
        "does not generate final graphics or inspect real images",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_reviewer_handoff_keeps_json_as_supporting_evidence() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "graphic-output-manifest.json",
        "graphic-output-permutations.json",
        "graphic-output-validation.json",
        "graphic-output-review-packet.json",
        "run-metadata.json",
        "The `index.html` is the business-viewable page.",
        "The JSON files are supporting evidence artifacts for technical reviewers.",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_reviewer_handoff_records_watch_script_verification() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "latest_user_reported_constraint_driven_graphic_output_permutation_watch_script_test_result: 9 passed",
        "source: user-reported local test run",
        "command: pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py",
        "result: 9 passed",
        "latest_user_reported_constraint_driven_graphic_output_permutation_reviewer_handoff_test_result: 5 passed",
        "latest_user_reported_constraint_driven_graphic_output_permutation_reviewer_handoff_rerun_test_result: 5 passed",
        "latest_user_reported_constraint_driven_graphic_output_permutation_reviewer_handoff_rerun_test_result_on: 2026-07-13",
        "command: pytest tests/test_constraint_driven_graphic_output_permutation_reviewer_handoff.py",
        "result: 5 passed",
        "Latest reviewer handoff rerun verification record",
        "reported_on: 2026-07-13",
        "latest_user_reported_constraint_driven_graphic_output_permutation_browser_demo_run_created: true",
        "source: user-reported local script run",
        "result: browser run created",
        "assistant_ran_tests: false",
        "assistant_ran_demo: false",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_reviewer_handoff_preserves_guardrails() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "Fixture-safe output specifications only.",
        "No generated final graphics.",
        "No production artwork generation.",
        "No real local image input.",
        "No local_file_path loading.",
        "No file_uri loading.",
        "No artifact download.",
        "No network fetch.",
        "No image decoding.",
        "No pixel inspection.",
        "No CV/OCR provider integration.",
        "No automatic approval.",
    ]
    for item in expected:
        assert item in content
