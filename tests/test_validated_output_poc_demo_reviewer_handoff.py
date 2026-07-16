from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "800_Demos" / "Validated_Output_POC_Demo_Reviewer_Handoff.md"


def test_validated_output_poc_demo_reviewer_handoff_exists() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "# Validated Output POC Demo Reviewer Handoff",
        "status: ready-for-use",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic",
        "launcher_script: scripts/run-validated-output-poc-demo.ps1",
        "implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_reviewer_handoff_lists_entry_commands() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        ".\\scripts\\run-validated-output-poc-demo.ps1",
        ".\\scripts\\run-validated-output-poc-demo.ps1 -NoOpenBrowser",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_reviewer_handoff_describes_launcher_flow() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "Runs the fixture-safe output POC generator.",
        "Runs deterministic SVG structural validation.",
        "Writes svg-structural-validation.json.",
        "Updates graphic-output-review-packet.json with svg_structural_validation.",
        "Writes validated-output-poc-demo-summary.json.",
        "Adds SVG structural validation evidence to index.html.",
        "Adds validated demo launcher evidence to index.html.",
        "Opens the latest generated browser UI by default.",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_reviewer_handoff_lists_expected_terminal_and_browser_evidence() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "Validated ConstraintOS output POC demo complete.",
        "Run directory:",
        "Browser UI:",
        "Validation report:",
        "Review packet:",
        "Launcher summary:",
        "Browser summary updated:",
        "Final decision remains: needs_review",
        "Approval allowed remains: false",
        "Deterministic SVG graphics",
        "SVG structural validation",
        "Validated demo launcher",
        "One-command validated output POC complete",
        "validated-output-poc-demo-summary.json",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_reviewer_handoff_lists_expected_artifacts() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "runs/output-poc/supra_2jz_gte_twin_turbo/<timestamp>/",
        "index.html",
        "run-metadata.json",
        "graphic-output-manifest.json",
        "graphic-output-permutations.json",
        "graphic-output-validation.json",
        "graphic-output-review-packet.json",
        "svg-structural-validation.json",
        "validated-output-poc-demo-summary.json",
        "graphics/turbo_system_focus.svg",
        "graphics/inline_six_engine_identity_focus.svg",
        "graphics/technical_label_density_focus.svg",
        "graphics/reviewer_safe_minimal_focus.svg",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_reviewer_handoff_preserves_decision_rule_and_blocked_scope() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    expected = [
        "ready to show as a fixture-safe product demonstration",
        "needs_review",
        "approval_allowed: false",
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


def test_validated_output_poc_demo_reviewer_handoff_lists_verification_command() -> None:
    content = HANDOFF.read_text(encoding="utf-8")

    assert "pytest tests/test_validated_output_poc_demo_reviewer_handoff.py" in content
