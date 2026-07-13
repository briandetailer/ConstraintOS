from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "800_Demos" / "Fixture_Safe_Visual_Placeholder_Reviewer_Handoff.md"


def test_fixture_safe_placeholder_reviewer_handoff_exists_and_targets_phase_4() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "# Fixture-Safe Visual Placeholder Reviewer Handoff",
        "status: reviewer-handoff-defined",
        "phase: Phase 4 - reviewer handoff update",
        "phase_status: complete",
        "milestone: docs/500_Milestones/Fixture_Safe_Visual_Placeholder_Refinement_v1.md",
        "contract: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Refinement_Contract.md",
        "panel_design: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Panel_Design.md",
        "evidence_summary_cards: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Evidence_Summary_Cards.md",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: fixture-safe-visual-placeholders-only",
        "latest_user_reported_fixture_safe_visual_placeholder_reviewer_handoff_test_result: 7 passed",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_reviewer_handoff_defines_reviewer_story() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "same constraints -> distinct placeholder panels -> evidence summaries -> needs_review",
        "These panels are not generated final artwork.",
        "deterministic, fixture-safe placeholders",
        "The evidence cards summarize fixture evidence only.",
        "Every variant remains needs_review.",
        "approval_allowed remains false.",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_reviewer_handoff_defines_inspection_path() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "turbo_system_focus",
        "Is the sequential twin-turbo intent clear without implying final artwork?",
        "inline_six_engine_identity_focus",
        "Is the 2JZ-GTE inline-six identity clear, including wrong-engine exclusions?",
        "technical_label_density_focus",
        "Does the denser callout comparison help explain how variants can differ?",
        "reviewer_safe_minimal_focus",
        "Is the conservative placeholder useful for showing only validated claims?",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_reviewer_handoff_defines_evidence_interpretation() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "satisfied fixture constraints:",
        "Claims that the fixture can safely surface for review.",
        "visible uncertainty:",
        "must stay needs_review",
        "blocked claims:",
        "Claims that must not be made by placeholder refinement.",
        "review_decision: needs_review",
        "approval_allowed: false",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_reviewer_handoff_defines_signal_capture() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "clarity_signal:",
        "strong: reviewer can describe why each placeholder differs.",
        "mixed: reviewer sees visual differences but still expects final artwork.",
        "weak: reviewer interprets placeholders as failed generated images.",
        "trust_signal:",
        "strong: reviewer understands why evidence cards block approval.",
        "next_step_signal:",
        "browser polish",
        "evidence card simplification",
        "stronger traceability labels",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_reviewer_handoff_preserves_cautions_and_guardrails() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "Do not evaluate these panels as final generated graphics.",
        "Do not treat evidence cards as scoring cards.",
        "Do not approve any variant.",
        "Do not request real image input as part of this milestone.",
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


def test_fixture_safe_placeholder_reviewer_handoff_done_criteria_and_command() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "source: user-reported local test run",
        "command: pytest tests/test_fixture_safe_visual_placeholder_reviewer_handoff.py",
        "result: 7 passed",
        "reported_on: 2026-07-13",
        "assistant_ran_tests: false",
        "[x] Reviewer handoff document exists.",
        "[x] Placeholder reviewer framing is defined.",
        "[x] Review path covers all four placeholder panels.",
        "[x] Evidence card interpretation is defined.",
        "[x] Reviewer signal capture is defined.",
        "[x] Reviewer cautions preserve fixture-safe scope.",
        "[x] Guardrails are preserved.",
        "[x] Verification test result recorded.",
        "pytest tests/test_fixture_safe_visual_placeholder_reviewer_handoff.py",
    ]
    for item in expected:
        assert item in content
