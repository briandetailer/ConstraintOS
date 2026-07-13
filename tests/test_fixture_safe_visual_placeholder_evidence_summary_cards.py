from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_CARDS = ROOT / "docs" / "800_Demos" / "Fixture_Safe_Visual_Placeholder_Evidence_Summary_Cards.md"


def test_fixture_safe_placeholder_evidence_summary_cards_exist_and_target_phase_3() -> None:
    content = EVIDENCE_CARDS.read_text(encoding="utf-8")

    expected = [
        "# Fixture-Safe Visual Placeholder Evidence Summary Cards",
        "status: evidence-summary-cards-defined",
        "phase: Phase 3 - evidence summary cards",
        "phase_status: complete",
        "milestone: docs/500_Milestones/Fixture_Safe_Visual_Placeholder_Refinement_v1.md",
        "contract: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Refinement_Contract.md",
        "panel_design: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Panel_Design.md",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: fixture-safe-visual-placeholders-only",
        "latest_user_reported_fixture_safe_visual_placeholder_evidence_summary_cards_test_result: 7 passed",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_evidence_summary_cards_define_review_goal() -> None:
    content = EVIDENCE_CARDS.read_text(encoding="utf-8")

    expected = [
        "placeholder panel -> evidence summary card -> needs_review explanation -> approval_allowed false",
        "Evidence summary cards may summarize fixture evidence",
        "must not score artwork, inspect pixels, or approve output",
        "satisfied fixture constraints",
        "visible uncertainty",
        "blocked claims",
        "review_decision: needs_review",
        "approval_allowed: false",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_evidence_summary_cards_define_shared_card_layout() -> None:
    content = EVIDENCE_CARDS.read_text(encoding="utf-8")

    expected = [
        "evidence_summary_card:",
        "card title",
        "constraint coverage chips",
        "visible uncertainty note",
        "blocked claim list",
        "reviewer interpretation note",
        "review state footer",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_evidence_summary_cards_define_four_required_cards() -> None:
    content = EVIDENCE_CARDS.read_text(encoding="utf-8")

    expected = [
        "turbo_system_focus",
        "evidence_card_title: Turbo System Evidence",
        "satisfied_constraints: Toyota Supra A80, 2JZ-GTE, sequential twin-turbo",
        "inline_six_engine_identity_focus",
        "evidence_card_title: Inline-Six Identity Evidence",
        "satisfied_constraints: Toyota Supra A80, 2JZ-GTE inline-six, wrong-engine exclusions",
        "technical_label_density_focus",
        "evidence_card_title: Label Density Evidence",
        "visible_uncertainty: label density requires reviewer judgment",
        "reviewer_safe_minimal_focus",
        "evidence_card_title: Reviewer-Safe Evidence",
        "blocked_claims: final artwork, automatic approval, unstated mechanical claims",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_evidence_summary_cards_scope_allowed_and_blocked_tokens() -> None:
    content = EVIDENCE_CARDS.read_text(encoding="utf-8")

    allowed = [
        "evidence_summary_card",
        "constraint_coverage_chip",
        "visible_uncertainty_note",
        "blocked_claim_item",
        "reviewer_interpretation_note",
        "review_state_footer",
    ]
    for item in allowed:
        assert item in content

    blocked = [
        "numeric_quality_score",
        "visual_similarity_score",
        "pixel_confidence",
        "ocr_confidence",
        "cv_detection_confidence",
        "approval_score",
        "pass_fail_artwork_grade",
        "generated_asset_reference",
    ]
    for item in blocked:
        assert item in content


def test_fixture_safe_placeholder_evidence_summary_cards_preserve_copy_and_traceability() -> None:
    content = EVIDENCE_CARDS.read_text(encoding="utf-8")

    expected = [
        "This card summarizes fixture evidence only.",
        "This card does not inspect or grade final artwork.",
        "Uncertainty remains needs_review.",
        "approval_allowed remains false.",
        "engine_identity -> 2JZ-GTE inline-six identity",
        "vehicle_identity -> Toyota Supra A80 / Mk IV identity",
        "turbo_identity -> sequential twin-turbo identity",
        "wrong_engine_exclusion -> not V6 / not V8 / not rotary / not RB26 / not LF4 / not B58",
        "review_safety -> uncertainty defaults to needs_review and approval_allowed remains false",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_evidence_summary_cards_preserve_guardrails_and_done_criteria() -> None:
    content = EVIDENCE_CARDS.read_text(encoding="utf-8")

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
        "source: user-reported local test run",
        "command: pytest tests/test_fixture_safe_visual_placeholder_evidence_summary_cards.py",
        "result: 7 passed",
        "reported_on: 2026-07-13",
        "assistant_ran_tests: false",
        "[x] Evidence summary card document exists.",
        "[x] Four required evidence cards are defined.",
        "[x] Reviewer copy requirements preserve fixture-safe scope.",
        "[x] Traceability requirements are defined.",
        "[x] Verification test result recorded.",
        "pytest tests/test_fixture_safe_visual_placeholder_evidence_summary_cards.py",
    ]
    for item in expected:
        assert item in content
