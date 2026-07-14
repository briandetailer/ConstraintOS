from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Deterministic_SVG_Graphics_Renderer_v1.md"


def test_deterministic_svg_graphics_renderer_milestone_exists() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "# Deterministic SVG Graphics Renderer v1",
        "status: active",
        "phase_1_svg_renderer_status: ready-for-verification",
        "phase_1_graphics_helper_status: ready-for-verification",
        "previous_milestone: docs/500_Milestones/Fixture_Safe_Placeholder_Browser_Implementation_v1.md",
        "script: scripts/watch-constraintos-output-poc.ps1",
        "helper_script: scripts/open-latest-output-poc-graphics.ps1",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: deterministic-svg-output-only",
    ]
    for item in expected:
        assert item in content


def test_deterministic_svg_graphics_renderer_records_product_target() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "output permutations -> deterministic SVG graphics -> browser display -> structural evidence -> needs_review",
        "Write one SVG file for each Toyota Supra output permutation.",
        "Store SVG files under runs/output-poc/<scenario>/<timestamp>/graphics/.",
        "Link generated SVG files from index.html.",
        "Record generated SVG artifact paths in run-metadata.json.",
        "Provide a helper command that opens the latest generated graphics folder.",
        "Preserve approval_allowed: false.",
    ]
    for item in expected:
        assert item in content


def test_deterministic_svg_graphics_renderer_lists_target_artifacts() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "graphics/turbo_system_focus.svg",
        "graphics/inline_six_engine_identity_focus.svg",
        "graphics/technical_label_density_focus.svg",
        "graphics/reviewer_safe_minimal_focus.svg",
    ]
    for item in expected:
        assert item in content


def test_deterministic_svg_graphics_renderer_defines_boundary_and_validation_target() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "SVG markup generated from deterministic fixture data",
        "rectangles",
        "lines",
        "text labels",
        "callout groups",
        "each SVG file is listed in metadata",
        "each SVG file is linked from index.html",
        "each SVG preserves permutation_id",
        "each SVG preserves review_decision: needs_review",
        "each SVG preserves approval_allowed: false",
    ]
    for item in expected:
        assert item in content


def test_deterministic_svg_graphics_renderer_records_implementation_under_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "script_update: scripts/watch-constraintos-output-poc.ps1",
        "helper_script: scripts/open-latest-output-poc-graphics.ps1",
        "command_reference_update: docs/700_Use_Cases/Graphics_Validation_Command_Reference.md",
        "pytest tests/test_deterministic_svg_graphics_renderer_milestone.py",
        "pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py",
        "pytest tests/test_open_latest_output_poc_graphics_script.py",
        "status: ready-for-verification",
        "creates a `graphics/` directory",
        "writes four deterministic SVG graphics",
        "records them in `svg_graphics` metadata",
        "links them from the generated browser page",
        "opens the latest generated deterministic SVG graphics folder",
        "prints the full path to each expected SVG artifact",
    ]
    for item in expected:
        assert item in content


def test_deterministic_svg_graphics_renderer_preserves_blocked_scope() -> None:
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


def test_deterministic_svg_graphics_renderer_done_criteria_and_commands() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "[x] Milestone exists.",
        "[x] Previous browser implementation milestone is referenced.",
        "[x] Deterministic SVG output target is defined.",
        "[x] Required SVG artifact paths are listed.",
        "[x] Renderer boundary is defined.",
        "[x] Structural validation target is defined.",
        "[x] SVG output implemented.",
        "[x] Latest graphics helper implemented.",
        "[ ] Verification result recorded.",
        "pytest tests/test_deterministic_svg_graphics_renderer_milestone.py",
        "pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py",
        "pytest tests/test_open_latest_output_poc_graphics_script.py",
        ".\\scripts\\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser",
        ".\\scripts\\open-latest-output-poc-graphics.ps1",
    ]
    for item in expected:
        assert item in content
