from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "watch-constraintos-output-poc.ps1"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_output_permutation_watch_script_exists_and_defaults_to_toyota_supra() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "param(",
        "[string]$Scenario = \"supra_2jz_gte_twin_turbo\"",
        "Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic",
        "constraint-driven-graphic-output-permutation-poc",
        "Unsupported scenario",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_watch_script_writes_expected_run_artifacts() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "runs",
        "output-poc",
        "graphic-output-manifest.json",
        "graphic-output-permutations.json",
        "graphic-output-validation.json",
        "graphic-output-review-packet.json",
        "index.html",
        "run-metadata.json",
        "Set-Content -Path $ManifestPath -Encoding UTF8",
        "Set-Content -Path $PermutationsPath -Encoding UTF8",
        "Set-Content -Path $ValidationPath -Encoding UTF8",
        "Set-Content -Path $ReviewPacketPath -Encoding UTF8",
        "Set-Content -Path $IndexPath -Encoding UTF8",
        "Set-Content -Path $MetadataPath -Encoding UTF8",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_watch_script_defines_four_fixture_permutations() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "turbo_system_focus",
        "inline_six_engine_identity_focus",
        "technical_label_density_focus",
        "reviewer_safe_minimal_focus",
        "fixture-placeholder://output-poc/supra/turbo-system-focus",
        "fixture-placeholder://output-poc/supra/inline-six-identity-focus",
        "fixture-placeholder://output-poc/supra/technical-label-density-focus",
        "fixture-placeholder://output-poc/supra/reviewer-safe-minimal-focus",
        "permutation_count = $Permutations.Count",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_watch_script_preserves_decision_and_approval_semantics() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "$FinalDecision = \"needs_review\"",
        "$ApprovalAllowed = $false",
        "final_decision = $FinalDecision",
        "approval_allowed = $ApprovalAllowed",
        "review_decision = \"needs_review\"",
        "approval_allowed = $false",
        "why_approval_is_blocked",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_watch_script_references_toyota_constraints() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "Toyota Supra Mk IV / A80 identity",
        "2JZ-GTE inline-six identity",
        "sequential twin-turbo system",
        "not generic engine",
        "not V6",
        "not V8",
        "not rotary",
        "not RB26",
        "not LF4",
        "not B58",
        "technical graphic / publishing context",
        "uncertainty defaults to needs_review",
        "approval_allowed remains false",
    ]
    for item in expected:
        assert item in content


def test_output_permutation_watch_script_preserves_guardrails() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "No generated final graphics",
        "No production artwork generation",
        "No real local image input",
        "No artifact download",
        "No network fetch",
        "No image decoding",
        "No pixel inspection",
        "No CV/OCR provider integration",
        "No automatic approval",
    ]
    for item in expected:
        assert item in content

    forbidden_runtime_authority = [
        "source_image_path =",
        "generated_image_path =",
        "production_artwork_path =",
        "pixel_data =",
        "ocr_text =",
        "cv_provider =",
        "auto_approved =",
    ]
    for item in forbidden_runtime_authority:
        assert item not in content


def test_output_permutation_watch_script_can_open_browser_when_requested() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert "[switch]$OpenBrowser" in content
    assert "if ($OpenBrowser)" in content
    assert "Start-Process $IndexPath" in content


def test_output_permutation_watch_script_is_in_command_reference() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    expected = [
        "Constraint-driven output permutation POC - Toyota Supra",
        ".\\scripts\\watch-constraintos-output-poc.ps1",
        ".\\scripts\\watch-constraintos-output-poc.ps1 -Scenario supra_2jz_gte_twin_turbo -OpenBrowser",
        "pytest tests/test_constraint_driven_graphic_output_permutation_watch_script.py",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-manifest.json",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-permutations.json",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-validation.json",
        "runs/output-poc/<scenario>/<timestamp>/graphic-output-review-packet.json",
    ]
    for item in expected:
        assert item in content
