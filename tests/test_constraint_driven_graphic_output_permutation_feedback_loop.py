from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_LOOP = ROOT / "docs" / "800_Demos" / "Constraint_Driven_Graphic_Output_Permutation_POC_Feedback_Loop.md"


def test_output_permutation_feedback_loop_exists_and_targets_phase_5() -> None:
    content = FEEDBACK_LOOP.read_text(encoding="utf-8")

    expected = [
        "# Constraint-Driven Graphic Output Permutation POC Feedback Loop",
        "status: feedback-loop-defined",
        "phase_status: complete",
        "phase: Phase 5 - feedback loop",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: documentation-only-feedback-loop",
        "loaded constraints -> controlled output permutations -> deterministic validation -> needs_review",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_feedback_loop_points_to_reviewer_facing_index_html() -> None:
    content = FEEDBACK_LOOP.read_text(encoding="utf-8")

    expected = [
        "runs/output-poc/supra_2jz_gte_twin_turbo/<timestamp>/index.html",
        "D:\\Code\\ConstraintOS\\runs\\output-poc\\supra_2jz_gte_twin_turbo\\20260712-151228\\index.html",
        "The generated `index.html` is the business-facing artifact.",
        "The JSON files are supporting evidence for technical reviewers.",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_feedback_loop_defines_reviewer_questions() -> None:
    content = FEEDBACK_LOOP.read_text(encoding="utf-8")

    expected = [
        "Did the four-step flow make sense?",
        "Was it clear that ConstraintOS is defining controlled output specifications from requirements?",
        "Was it clear why every variant remains needs_review?",
        "Was it clear why approval_allowed remains false?",
        "Which output permutation was easiest to understand?",
        "Which output permutation felt most product-relevant?",
        "What did the reviewer expect to see next?",
        "Did the guardrails feel like a strength, a limitation, or both?",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_feedback_loop_defines_signal_classification_and_decisions() -> None:
    content = FEEDBACK_LOOP.read_text(encoding="utf-8")

    expected = [
        "strong_product_signal",
        "mixed_product_signal",
        "weak_product_signal",
        "If strong_product_signal dominates:",
        "If mixed_product_signal dominates:",
        "If weak_product_signal dominates:",
        "Move to a fixture-safe visual placeholder refinement milestone.",
        "Improve the browser story and reviewer handoff first.",
        "Pause feature expansion.",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_feedback_loop_scopes_allowed_and_blocked_next_steps() -> None:
    content = FEEDBACK_LOOP.read_text(encoding="utf-8")

    allowed = [
        "Fixture-safe visual placeholder refinement.",
        "Browser walkthrough polish.",
        "Reviewer copy simplification.",
        "Better evidence summary cards.",
        "Stronger traceability between constraints, permutations, and validation evidence.",
    ]
    for item in allowed:
        assert item in content

    blocked = [
        "Real generated final graphics.",
        "Production artwork generation.",
        "Real local image input.",
        "local_file_path loading.",
        "file_uri loading.",
        "Artifact download.",
        "Network fetch.",
        "Image decoding.",
        "Pixel inspection.",
        "CV/OCR provider integration.",
        "Automatic approval.",
    ]
    for item in blocked:
        assert item in content


def test_output_permutation_feedback_loop_defines_synthesis_format_and_done_criteria() -> None:
    content = FEEDBACK_LOOP.read_text(encoding="utf-8")

    expected = [
        "reviewer_count:",
        "strong_product_signal_count:",
        "mixed_product_signal_count:",
        "weak_product_signal_count:",
        "recommended_decision:",
        "recommended_next_milestone:",
        "approval_allowed: false",
        "latest_user_reported_constraint_driven_graphic_output_permutation_feedback_loop_test_result: 6 passed",
        "source: user-reported local test run",
        "command: pytest tests/test_constraint_driven_graphic_output_permutation_feedback_loop.py",
        "result: 6 passed",
        "reported_on: 2026-07-13",
        "assistant_ran_tests: false",
        "[x] Feedback loop document exists.",
        "[x] Reviewer feedback questions are defined.",
        "[x] Feedback classification labels are defined.",
        "[x] Decision rules are defined.",
        "[x] Guardrails are preserved.",
        "[x] Verification test result recorded.",
        "pytest tests/test_constraint_driven_graphic_output_permutation_feedback_loop.py",
    ]
    for item in expected:
        assert item in content
