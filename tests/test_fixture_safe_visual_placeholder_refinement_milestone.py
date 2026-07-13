from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Fixture_Safe_Visual_Placeholder_Refinement_v1.md"


def test_fixture_safe_visual_placeholder_refinement_milestone_exists() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "# Fixture-Safe Visual Placeholder Refinement v1",
        "status: kickoff-ready",
        "kickoff_status: complete",
        "track: Business Demo Visibility Track",
        "previous_milestone: docs/500_Milestones/Constraint_Driven_Graphic_Output_Permutation_POC_v1.md",
        "previous_feedback_loop: docs/800_Demos/Constraint_Driven_Graphic_Output_Permutation_POC_Feedback_Loop.md",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: fixture-safe-visual-placeholders-only",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_visual_placeholder_refinement_product_target_is_recorded() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "constraints -> fixture-safe placeholder visuals -> evidence summary -> needs_review",
        "Improve the browser-visible distinction between the four Toyota Supra output permutations.",
        "Add fixture-safe visual placeholder cards or schematic panels.",
        "Keep every placeholder deterministic and non-image-derived.",
        "Keep every variant in needs_review.",
        "Preserve approval_allowed: false.",
        "Improve traceability from constraint -> placeholder -> validation evidence.",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_visual_placeholder_refinement_targets_four_permutations() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "turbo_system_focus",
        "inline_six_engine_identity_focus",
        "technical_label_density_focus",
        "reviewer_safe_minimal_focus",
        "visually emphasize sequential twin-turbo identity using deterministic schematic blocks",
        "visually emphasize inline-six identity and wrong-engine exclusions using deterministic label panels",
        "compare denser callout layout against the same loaded constraints",
        "show the conservative output style that exposes only validated claims and keeps uncertainty visible",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_visual_placeholder_refinement_scopes_allowed_outputs() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "Static HTML placeholder cards.",
        "Deterministic schematic blocks.",
        "Text-first visual panels.",
        "Constraint-to-placeholder traceability tables.",
        "Evidence summary cards.",
        "Reviewer-friendly labels and captions.",
        "Fixture placeholder identifiers.",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_visual_placeholder_refinement_preserves_blocked_scope() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

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


def test_fixture_safe_visual_placeholder_refinement_defines_phases_and_kickoff_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "Phase 1: placeholder refinement contract",
        "Phase 2: browser placeholder panel design",
        "Phase 3: evidence summary cards",
        "Phase 4: reviewer handoff update",
        "Phase 5: verification and closeout",
        "latest_user_reported_fixture_safe_visual_placeholder_refinement_milestone_test_result: 6 passed",
        "latest_user_reported_fixture_safe_visual_placeholder_refinement_milestone_rerun_test_result: 6 passed",
        "source: user-reported local test run",
        "source: user-reported local test rerun",
        "command: pytest tests/test_fixture_safe_visual_placeholder_refinement_milestone.py",
        "result: 6 passed",
        "reported_on: 2026-07-13",
        "assistant_ran_tests: false",
        "[x] Milestone exists.",
        "[x] Previous output-permutation POC is referenced.",
        "[x] Feedback-loop authority is referenced.",
        "[x] Fixture-safe visual placeholder scope is defined.",
        "[x] Blocked outputs are preserved.",
        "[x] Verification test result recorded.",
        "pytest tests/test_fixture_safe_visual_placeholder_refinement_milestone.py",
    ]
    for item in expected:
        assert item in content
