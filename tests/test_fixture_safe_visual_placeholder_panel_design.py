from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL_DESIGN = ROOT / "docs" / "800_Demos" / "Fixture_Safe_Visual_Placeholder_Panel_Design.md"


def test_fixture_safe_placeholder_panel_design_exists_and_targets_phase_2() -> None:
    content = PANEL_DESIGN.read_text(encoding="utf-8")

    expected = [
        "# Fixture-Safe Visual Placeholder Panel Design",
        "status: panel-design-defined",
        "phase: Phase 2 - browser placeholder panel design",
        "phase_status: complete",
        "milestone: docs/500_Milestones/Fixture_Safe_Visual_Placeholder_Refinement_v1.md",
        "contract: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Refinement_Contract.md",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: fixture-safe-visual-placeholders-only",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_panel_design_defines_reviewer_clarity_goal() -> None:
    content = PANEL_DESIGN.read_text(encoding="utf-8")

    expected = [
        "same constraints -> visibly different fixture-safe placeholder panels -> same needs_review decision",
        "Panels may improve visual comparison",
        "deterministic",
        "fixture-defined",
        "non-image-derived",
        "blocked from approval",
        "review_decision: needs_review",
        "approval_allowed: false",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_panel_design_defines_shared_browser_layout() -> None:
    content = PANEL_DESIGN.read_text(encoding="utf-8")

    expected = [
        "panel_shell:",
        "permutation title",
        "one-line business intent",
        "deterministic schematic or text-first placeholder area",
        "constraint trace chips",
        "evidence summary card",
        "uncertainty banner",
        "review state footer",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_panel_design_defines_four_required_panels() -> None:
    content = PANEL_DESIGN.read_text(encoding="utf-8")

    expected = [
        "turbo_system_focus",
        "visual_placeholder_type: schematic_block_panel",
        "engine core, twin turbo A, twin turbo B, charge path, exhaust path",
        "inline_six_engine_identity_focus",
        "visual_placeholder_type: text_first_panel",
        "not V6, not V8, not rotary, not RB26, not LF4, not B58",
        "technical_label_density_focus",
        "visual_placeholder_type: label_density_panel",
        "density indicator: high label density for review comparison",
        "reviewer_safe_minimal_focus",
        "visual_placeholder_type: reviewer_safe_minimal_panel",
        "conservative placeholder only, not final artwork",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_panel_design_scopes_allowed_and_blocked_tokens() -> None:
    content = PANEL_DESIGN.read_text(encoding="utf-8")

    allowed = [
        "panel_shell",
        "title_band",
        "schematic_block",
        "identity_block",
        "exclusion_chip",
        "constraint_chip",
        "evidence_chip",
        "density_indicator",
        "uncertainty_banner",
        "review_footer",
    ]
    for item in allowed:
        assert item in content

    blocked = [
        "raster_image",
        "generated_artwork",
        "source_image",
        "decoded_pixels",
        "ocr_overlay",
        "cv_detection_box",
        "external_asset",
        "downloaded_asset",
        "approval_badge",
    ]
    for item in blocked:
        assert item in content


def test_fixture_safe_placeholder_panel_design_preserves_copy_and_traceability_requirements() -> None:
    content = PANEL_DESIGN.read_text(encoding="utf-8")

    expected = [
        "This is a deterministic placeholder, not final artwork.",
        "This panel is derived from fixture constraints, not image inspection.",
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


def test_fixture_safe_placeholder_panel_design_preserves_guardrails_done_criteria_and_verification() -> None:
    content = PANEL_DESIGN.read_text(encoding="utf-8")

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
        "latest_user_reported_fixture_safe_visual_placeholder_panel_design_test_result: 7 passed",
        "source: user-reported local test run",
        "command: pytest tests/test_fixture_safe_visual_placeholder_panel_design.py",
        "result: 7 passed",
        "reported_on: 2026-07-13",
        "assistant_ran_tests: false",
        "[x] Panel design document exists.",
        "[x] Four required placeholder panels are defined.",
        "[x] Browser copy requirements preserve fixture-safe scope.",
        "[x] Traceability requirements are defined.",
        "[x] Verification test result recorded.",
        "pytest tests/test_fixture_safe_visual_placeholder_panel_design.py",
    ]
    for item in expected:
        assert item in content
