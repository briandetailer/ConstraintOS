from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Deterministic_SVG_Structural_Validation_v1.md"


def test_deterministic_svg_structural_validation_milestone_exists() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "# Deterministic SVG Structural Validation v1",
        "status: complete",
        "phase_1_svg_structural_validator_status: complete",
        "phase_1_svg_runtime_validation_status: complete",
        "phase_2_svg_validation_report_status: complete",
        "phase_3_review_packet_surfacing_status: complete",
        "post_closeout_browser_evidence_surfacing_status: static-test-complete",
        "completed_on: 2026-07-14",
        "previous_milestone: docs/500_Milestones/Deterministic_SVG_Graphics_Renderer_v1.md",
        "renderer_script: scripts/watch-constraintos-output-poc.ps1",
        "validator_script: scripts/validate-output-poc-svg-graphics.ps1",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: deterministic-svg-structural-validation-only",
        "latest_user_reported_svg_validator_static_test_result: 8 passed",
        "latest_user_reported_svg_runtime_validator_result: success message received",
        "latest_user_reported_svg_validation_report_and_review_packet_test_result: 10 passed",
        "latest_user_reported_svg_validation_report_and_review_packet_runtime_result: success message received with validation report and review packet paths",
        "latest_user_reported_svg_browser_evidence_surfacing_static_test_result: 10 passed",
    ]
    for item in expected:
        assert item in content


def test_deterministic_svg_structural_validation_records_product_target() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "output permutations -> deterministic SVG graphics -> structural SVG validation -> needs_review",
        "Validate the latest generated output-poc run.",
        "Confirm the graphics directory exists.",
        "Confirm all four SVG graphics exist.",
        "Confirm each SVG contains required structural metadata.",
        "Confirm each SVG is referenced in run-metadata.json.",
        "Confirm each SVG is linked from index.html.",
        "Confirm forbidden external image references are absent.",
        "Write svg-structural-validation.json as a durable validation report.",
        "Surface svg_structural_validation in graphic-output-review-packet.json.",
        "Preserve needs_review and approval_allowed: false.",
    ]
    for item in expected:
        assert item in content


def test_deterministic_svg_structural_validation_lists_commands_and_artifacts() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        ".\\scripts\\validate-output-poc-svg-graphics.ps1",
        "graphics/turbo_system_focus.svg",
        "graphics/inline_six_engine_identity_focus.svg",
        "graphics/technical_label_density_focus.svg",
        "graphics/reviewer_safe_minimal_focus.svg",
    ]
    for item in expected:
        assert item in content


def test_deterministic_svg_structural_validation_lists_required_and_forbidden_markers() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    required = [
        "<svg xmlns=\"http://www.w3.org/2000/svg\"",
        "permutation_id",
        "svg_artifact",
        "review_decision: needs_review",
        "approval_allowed: false",
        "renderer: deterministic-svg-output-only",
        "id=\"deterministic-graphic-core\"",
        "id=\"traceability-labels\"",
        "id=\"evidence-summary\"",
        "Toyota Supra A80",
        "2JZ-GTE",
    ]
    for item in required:
        assert item in content

    forbidden = [
        "<image",
        "href=\"http",
        "href=\"file:",
        "xlink:href=\"http",
        "xlink:href=\"file:",
        "auto_approved",
        "production approval",
        "final production artwork approved",
    ]
    for item in forbidden:
        assert item in content


def test_deterministic_svg_structural_validation_records_verification_results() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "## Static validator test record",
        "source: user-reported local test run",
        "command: pytest tests/test_validate_output_poc_svg_graphics_script.py",
        "result: 8 passed",
        "reported_on: 2026-07-14",
        "assistant_ran_tests: false",
        "## Runtime validator record",
        "source: user-reported local runtime validation",
        "command: .\\scripts\\validate-output-poc-svg-graphics.ps1",
        "result: success message received",
        "assistant_ran_demo: false",
        "## Validation report and review packet surfacing record",
        "test_validate_output_poc_svg_graphics_script: 10 passed",
        "runtime_validator: success message received with Validation report and Review packet paths",
        "validation_report: runs/output-poc/supra_2jz_gte_twin_turbo/20260714-100414/svg-structural-validation.json",
        "review_packet: runs/output-poc/supra_2jz_gte_twin_turbo/20260714-100414/graphic-output-review-packet.json",
        "## Post-closeout browser evidence surfacing record",
        "result: 10 passed",
        "browser_summary_target: svg-structural-validation-summary in index.html",
        "runtime_browser_summary_status: pending user-reported runtime output",
    ]
    for item in expected:
        assert item in content


def test_deterministic_svg_structural_validation_preserves_blocked_scope() -> None:
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


def test_deterministic_svg_structural_validation_done_criteria_and_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "[x] Milestone exists.",
        "[x] Previous deterministic SVG renderer milestone is referenced.",
        "[x] Validator command is defined.",
        "[x] Expected SVG artifacts are listed.",
        "[x] Required SVG markers are listed.",
        "[x] Forbidden SVG markers are listed.",
        "[x] Validator script exists.",
        "[x] Static validator test result recorded.",
        "[x] Runtime validator result recorded.",
        "[x] Validation report artifact implemented.",
        "[x] Review packet surfacing implemented.",
        "[x] Validation report and review packet verification recorded.",
        "pytest tests/test_deterministic_svg_structural_validation_milestone.py",
        "pytest tests/test_validate_output_poc_svg_graphics_script.py",
        ".\\scripts\\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser",
        ".\\scripts\\validate-output-poc-svg-graphics.ps1",
    ]
    for item in expected:
        assert item in content
