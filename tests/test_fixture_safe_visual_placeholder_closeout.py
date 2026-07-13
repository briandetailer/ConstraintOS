from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOSEOUT = ROOT / "docs" / "800_Demos" / "Fixture_Safe_Visual_Placeholder_Closeout.md"


def test_fixture_safe_placeholder_closeout_exists_and_targets_phase_5() -> None:
    content = CLOSEOUT.read_text(encoding="utf-8")

    expected = [
        "# Fixture-Safe Visual Placeholder Closeout",
        "status: closeout-defined",
        "phase: Phase 5 - verification and closeout",
        "phase_status: ready-for-verification",
        "milestone: docs/500_Milestones/Fixture_Safe_Visual_Placeholder_Refinement_v1.md",
        "contract: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Refinement_Contract.md",
        "panel_design: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Panel_Design.md",
        "evidence_summary_cards: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Evidence_Summary_Cards.md",
        "reviewer_handoff: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Reviewer_Handoff.md",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: fixture-safe-visual-placeholders-only",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_closeout_records_completion_inventory() -> None:
    content = CLOSEOUT.read_text(encoding="utf-8")

    expected = [
        "Phase 1 contract:",
        "Defines placeholder schema, allowed types, blocked fields, Toyota requirements, and review semantics.",
        "Phase 2 panel design:",
        "Defines browser-visible placeholder panel structure for the four Toyota Supra permutations.",
        "Phase 3 evidence summary cards:",
        "Defines evidence cards that summarize fixture evidence without scoring or approving output.",
        "Phase 4 reviewer handoff:",
        "Defines reviewer framing, inspection path, evidence interpretation, and signal capture.",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_closeout_defines_final_product_state() -> None:
    content = CLOSEOUT.read_text(encoding="utf-8")

    expected = [
        "The milestone remains fixture-safe.",
        "Placeholders are deterministic and non-image-derived.",
        "Evidence cards summarize fixture evidence only.",
        "Reviewers can compare all four output permutation intents.",
        "Every variant remains needs_review.",
        "approval_allowed remains false.",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_closeout_lists_final_verification_suite() -> None:
    content = CLOSEOUT.read_text(encoding="utf-8")

    expected = [
        "pytest tests/test_fixture_safe_visual_placeholder_refinement_milestone.py",
        "pytest tests/test_fixture_safe_visual_placeholder_refinement_contract.py",
        "pytest tests/test_fixture_safe_visual_placeholder_panel_design.py",
        "pytest tests/test_fixture_safe_visual_placeholder_evidence_summary_cards.py",
        "pytest tests/test_fixture_safe_visual_placeholder_reviewer_handoff.py",
        "pytest tests/test_fixture_safe_visual_placeholder_closeout.py",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_closeout_preserves_blocked_scope() -> None:
    content = CLOSEOUT.read_text(encoding="utf-8")

    expected = [
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
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_closeout_done_criteria_and_command() -> None:
    content = CLOSEOUT.read_text(encoding="utf-8")

    expected = [
        "This milestone may be marked complete only after the final verification suite is user-reported as passing.",
        "[x] Closeout document exists.",
        "[x] Completion inventory is listed.",
        "[x] Final product state is defined.",
        "[x] Final verification suite is listed.",
        "[x] Blocked scope is preserved.",
        "[ ] Final verification result recorded.",
        "pytest tests/test_fixture_safe_visual_placeholder_closeout.py",
    ]
    for item in expected:
        assert item in content
