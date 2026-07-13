from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Fixture_Safe_Placeholder_Browser_Implementation_v1.md"


def test_fixture_safe_placeholder_browser_implementation_milestone_exists() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "# Fixture-Safe Placeholder Browser Implementation v1",
        "status: active",
        "kickoff_status: complete",
        "phase_1_browser_placeholder_contract_activation_status: complete",
        "phase_2_watch_script_browser_update_status: ready-for-verification",
        "track: Business Demo Visibility Track",
        "previous_milestone: docs/500_Milestones/Fixture_Safe_Visual_Placeholder_Refinement_v1.md",
        "previous_contract: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Refinement_Contract.md",
        "previous_panel_design: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Panel_Design.md",
        "previous_evidence_summary_cards: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Evidence_Summary_Cards.md",
        "previous_reviewer_handoff: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Reviewer_Handoff.md",
        "previous_closeout: docs/800_Demos/Fixture_Safe_Visual_Placeholder_Closeout.md",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: deterministic-browser-placeholders-only",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_browser_implementation_product_target_is_recorded() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "output permutations -> deterministic placeholder panels -> evidence summary cards -> needs_review",
        "Add browser-visible placeholder panels for the four Toyota Supra permutations.",
        "Add evidence summary cards beside or inside each placeholder panel.",
        "Preserve the existing generated run artifact structure.",
        "Preserve needs_review for every variant.",
        "Preserve approval_allowed: false.",
        "Keep every visual element deterministic and fixture-defined.",
        "Update tests and command reference when the watch script behavior changes.",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_browser_implementation_targets_script_and_artifacts() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "script: scripts/watch-constraintos-output-poc.ps1",
        "browser_artifact: runs/output-poc/<scenario>/<timestamp>/index.html",
        "graphic-output-manifest.json",
        "graphic-output-permutations.json",
        "graphic-output-validation.json",
        "graphic-output-review-packet.json",
        "run-metadata.json",
        "command_reference: docs/700_Use_Cases/Graphics_Validation_Command_Reference.md",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_browser_implementation_scopes_required_browser_additions() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "Placeholder panel section",
        "one panel for each permutation_id",
        "fixture-safe visual tokens only",
        "visible statement that panel is not final artwork",
        "Evidence summary card section",
        "satisfied constraints",
        "visible uncertainty",
        "blocked claims",
        "Traceability labels",
        "engine_identity",
        "vehicle_identity",
        "turbo_identity",
        "wrong_engine_exclusion",
        "review_safety",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_browser_implementation_records_script_update() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "## Implementation changes now under verification",
        "script_update: scripts/watch-constraintos-output-poc.ps1",
        "command_reference_update: docs/700_Use_Cases/Graphics_Validation_Command_Reference.md",
        "verification: pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py",
        "status: ready-for-verification",
        "browser-visible deterministic placeholder panels and evidence summary cards",
        "placeholder/evidence metadata in `run-metadata.json`",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_browser_implementation_preserves_guardrails() -> None:
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


def test_fixture_safe_placeholder_browser_implementation_defines_phases_and_kickoff_done_criteria() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "Phase 1: browser placeholder contract activation",
        "Phase 2: watch script browser update",
        "Phase 3: artifact metadata update",
        "Phase 4: command reference update",
        "Phase 5: verification and closeout",
        "latest_user_reported_fixture_safe_placeholder_browser_implementation_milestone_test_result: 6 passed",
        "source: user-reported local test run",
        "command: pytest tests/test_fixture_safe_placeholder_browser_implementation_milestone.py",
        "result: 6 passed",
        "assistant_ran_tests: false",
        "[x] Milestone exists.",
        "[x] Previous fixture-safe refinement milestone is referenced.",
        "[x] Browser implementation target is defined.",
        "[x] Existing run artifact structure is preserved.",
        "[x] Command reference maintenance is called out.",
        "[x] Blocked scope is preserved.",
        "[x] Verification test result recorded.",
        "pytest tests/test_fixture_safe_placeholder_browser_implementation_milestone.py",
        "pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py",
    ]
    for item in expected:
        assert item in content
