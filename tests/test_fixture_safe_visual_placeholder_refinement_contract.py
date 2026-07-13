from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "800_Demos" / "Fixture_Safe_Visual_Placeholder_Refinement_Contract.md"


def test_fixture_safe_placeholder_refinement_contract_exists_and_targets_phase_1() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "# Fixture-Safe Visual Placeholder Refinement Contract",
        "status: contract-defined",
        "phase: Phase 1 - placeholder refinement contract",
        "phase_status: complete",
        "milestone: docs/500_Milestones/Fixture_Safe_Visual_Placeholder_Refinement_v1.md",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: fixture-safe-visual-placeholders-only",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_refinement_contract_defines_core_rule() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "constraints -> fixture-safe placeholder visuals -> evidence summary -> needs_review",
        "Fixture-safe placeholders may make output specifications easier to compare",
        "must not become generated artwork, inspected images, or approval automation",
        "deterministic",
        "fixture-defined",
        "non-image-derived",
        "traceable to loaded constraints",
        "explicitly marked needs_review",
        "blocked from approval",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_refinement_contract_defines_placeholder_schema() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "placeholder_id:",
        "permutation_id:",
        "scenario_key:",
        "business_intent:",
        "visual_placeholder_type:",
        "fixture_components:",
        "constraint_trace:",
        "evidence_summary:",
        "uncertainty_notes:",
        "review_decision: needs_review",
        "approval_allowed: false",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_refinement_contract_scopes_allowed_types_and_components() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "schematic_block_panel",
        "text_first_panel",
        "label_density_panel",
        "constraint_trace_panel",
        "evidence_summary_card",
        "reviewer_safe_minimal_panel",
        "deterministic rectangles, bands, and containers",
        "deterministic labels and captions",
        "deterministic callout placeholders",
        "deterministic component tokens",
        "deterministic traceability rows",
        "deterministic evidence chips",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_refinement_contract_blocks_image_authority_fields() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    blocked_fields = [
        "image_path",
        "local_file_path",
        "file_uri",
        "source_image_uri",
        "source_image_bytes",
        "pixel_data",
        "ocr_text",
        "cv_provider_result",
        "generated_image_uri",
        "approval_result",
    ]
    for item in blocked_fields:
        assert item in content


def test_fixture_safe_placeholder_refinement_contract_preserves_toyota_constraints() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "Toyota Supra A80 / Mk IV identity",
        "2JZ-GTE inline-six identity",
        "sequential twin-turbo identity",
        "not V6",
        "not V8",
        "not rotary",
        "not RB26",
        "not LF4",
        "not B58",
        "technical graphic context",
        "uncertainty defaults to needs_review",
        "approval_allowed remains false",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_refinement_contract_defines_required_placeholder_set() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "turbo_system_focus",
        "visual_placeholder_type: schematic_block_panel",
        "required emphasis: sequential twin-turbo identity",
        "inline_six_engine_identity_focus",
        "visual_placeholder_type: text_first_panel",
        "required emphasis: 2JZ-GTE inline-six identity and wrong-engine exclusions",
        "technical_label_density_focus",
        "visual_placeholder_type: label_density_panel",
        "required emphasis: denser technical callout comparison",
        "reviewer_safe_minimal_focus",
        "visual_placeholder_type: reviewer_safe_minimal_panel",
        "required emphasis: only validated claims and visible uncertainty",
    ]
    for item in expected:
        assert item in content


def test_fixture_safe_placeholder_refinement_contract_preserves_review_semantics_and_guardrails() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "Default decision for every fixture-safe placeholder.",
        "not final artwork",
        "approval_allowed: false",
        "Required for every placeholder.",
        "Cannot be changed by placeholder refinement.",
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


def test_fixture_safe_placeholder_refinement_contract_done_criteria_and_command() -> None:
    content = CONTRACT.read_text(encoding="utf-8")

    expected = [
        "latest_user_reported_fixture_safe_visual_placeholder_refinement_contract_test_result: 9 passed",
        "source: user-reported local test run",
        "command: pytest tests/test_fixture_safe_visual_placeholder_refinement_contract.py",
        "result: 9 passed",
        "reported_on: 2026-07-13",
        "assistant_ran_tests: false",
        "[x] Contract document exists.",
        "[x] Placeholder record schema is defined.",
        "[x] Allowed placeholder types are defined.",
        "[x] Allowed fixture components are defined.",
        "[x] Blocked placeholder fields are listed.",
        "[x] Toyota Supra placeholder requirements are defined.",
        "[x] Required placeholder set is defined.",
        "[x] Review semantics preserve needs_review.",
        "[x] approval_allowed remains false.",
        "[x] Blocked scope is preserved.",
        "[x] Verification test result recorded.",
        "pytest tests/test_fixture_safe_visual_placeholder_refinement_contract.py",
    ]
    for item in expected:
        assert item in content
