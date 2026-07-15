from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Validated_Output_POC_Demo_Launcher_v1.md"


def test_validated_output_poc_demo_launcher_milestone_exists() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "# Validated Output POC Demo Launcher v1",
        "status: active",
        "phase_1_validated_demo_launcher_status: ready-for-verification",
        "phase_2_validated_demo_summary_status: ready-for-verification",
        "previous_milestone: docs/500_Milestones/Deterministic_SVG_Structural_Validation_v1.md",
        "launcher_script: scripts/run-validated-output-poc-demo.ps1",
        "generator_script: scripts/watch-constraintos-output-poc.ps1",
        "validator_script: scripts/validate-output-poc-svg-graphics.ps1",
        "browser_helper_script: scripts/open-latest-output-poc-browser.ps1",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_records_product_target() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "one command -> generate output POC -> validate SVG evidence -> write launcher summary -> update browser evidence -> open latest browser UI",
        "Run the fixture-safe output POC generator.",
        "Run the deterministic SVG structural validator.",
        "Write validated-output-poc-demo-summary.json for the latest run.",
        "Open the latest output POC browser UI by default.",
        "Allow a NoOpenBrowser mode for terminal-only verification.",
        "Preserve needs_review and approval_allowed: false.",
        "Preserve deterministic fixture-safe scope.",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_lists_commands() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        ".\\scripts\\run-validated-output-poc-demo.ps1",
        ".\\scripts\\run-validated-output-poc-demo.ps1 -NoOpenBrowser",
        "pytest tests/test_validated_output_poc_demo_launcher_milestone.py",
        "pytest tests/test_run_validated_output_poc_demo_script.py",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_defines_summary_artifact() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "## Launcher summary artifact",
        "runs/output-poc/<scenario>/<timestamp>/validated-output-poc-demo-summary.json",
        "launcher",
        "scenario_key",
        "run_dir",
        "browser_ui",
        "validation_report",
        "review_packet",
        "generated_at_local",
        "generator_script",
        "validator_script",
        "browser_helper_script",
        "final_decision: needs_review",
        "approval_allowed: false",
        "blocked_scope_preserved",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_records_implementation_under_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "## Implementation under verification",
        "script: scripts/run-validated-output-poc-demo.ps1",
        "test: tests/test_run_validated_output_poc_demo_script.py",
        "command_reference_update: docs/700_Use_Cases/Graphics_Validation_Command_Reference.md",
        "summary_artifact: validated-output-poc-demo-summary.json",
        "status: ready-for-verification",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_preserves_blocked_scope() -> None:
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


def test_validated_output_poc_demo_launcher_done_criteria() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "[x] Milestone exists.",
        "[x] Previous deterministic SVG structural validation milestone is referenced.",
        "[x] Launcher command is defined.",
        "[x] Generator script dependency is defined.",
        "[x] Validator script dependency is defined.",
        "[x] Browser helper script dependency is defined.",
        "[x] NoOpenBrowser mode is defined.",
        "[x] Launcher summary artifact is defined.",
        "[x] Blocked scope is preserved.",
        "[x] Launcher script exists.",
        "[ ] Verification result recorded.",
    ]
    for item in expected:
        assert item in content
