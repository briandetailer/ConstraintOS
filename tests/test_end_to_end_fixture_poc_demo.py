from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "watch-constraintos-poc.ps1"
MILESTONE = ROOT / "docs" / "500_Milestones" / "End_to_End_Fixture_POC_Demo_v1.md"
DEMO_OUTLINE = ROOT / "docs" / "800_Demos" / "End_to_End_Fixture_POC_Demo_Outline.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_end_to_end_fixture_poc_demo_script_exists_and_has_defaults() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert "param(" in content
    assert '[string]$Scenario = "perseverance"' in content
    assert '[int]$WatchDelayMs = 500' in content
    assert "runs\\poc-demo\\$Scenario\\$Timestamp" in content
    assert "ConstraintOS end-to-end fixture POC demo" in content
    assert "Demo principle: structured specifications, validation, and traceability are the source of truth." in content
    assert "fixture-based POC only" in content


def test_end_to_end_fixture_poc_demo_script_runs_visible_ten_stage_pipeline() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "Load scenario",
        "Load contract/specification",
        "Load candidate manifest and intake evidence",
        "Validate intake boundaries through review packet evidence",
        "Load deterministic fixture bytes",
        "Generate byte-loading and registry evidence",
        "Review fixture registry failure matrix",
        "Load and bind observation evidence",
        "Merge evidence and evaluate candidate fixture report",
        "Produce final review packet and demo summary",
        'Invoke-DemoStage "1/10"',
        'Invoke-DemoStage "10/10"',
    ]
    for item in expected:
        assert item in content


def test_end_to_end_fixture_poc_demo_script_calls_existing_product_clis() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "cos-graphics-contracts show $Scenario",
        "cos-graphics-candidates show $Scenario",
        "cos-graphics-candidates intake-show $Scenario",
        "cos-graphics-candidates intake-review-packet $Scenario",
        "cos-graphics-byte-loader minimal $Scenario",
        "cos-graphics-byte-loader review-packet $Scenario",
        "cos-graphics-byte-loader registry-review-packet",
        "cos-graphics-byte-loader failure-review-packet",
        "cos-graphics-candidates observe $Scenario",
        "cos-graphics-candidates bind-observations $Scenario",
        "cos-graphics-candidates merge-evidence $Scenario",
        "cos-graphics-candidates evaluate $Scenario",
        "cos-graphics-candidates review-packet $Scenario",
    ]
    for item in expected:
        assert item in content


def test_end_to_end_fixture_poc_demo_script_captures_expected_evidence_files() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "terminal-transcript.txt",
        "watch-output.txt",
        "contract.json",
        "candidate-manifest.json",
        "candidate-intake.json",
        "candidate-intake-review-packet.json",
        "byte-loading.json",
        "byte-loading-review-packet.json",
        "fixture-registry-review-packet.json",
        "fixture-registry-failure-review-packet.json",
        "manual-observations.json",
        "observation-binding.json",
        "merged-evidence.json",
        "evaluation-report.json",
        "final-review-packet.json",
        "demo-summary.json",
        "run-metadata.json",
        "Tee-Object -FilePath $WatchOutputPath",
        "ConvertTo-Json -Depth 6",
    ]
    for item in expected:
        assert item in content


def test_end_to_end_fixture_poc_demo_script_preserves_public_poc_guardrails() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    expected = [
        "no local image file opening, download, network fetch, image decoding, CV/OCR, image generation/editing, automatic approval, or private data",
        'local_image_file_opening = "not_run"',
        'artifact_download = "not_run"',
        'network_fetch = "not_run"',
        'image_decoding = "not_run"',
        'candidate_scoring_automation = "not_run"',
        'source_report_mutation = "not_run"',
        'approval_automation = "not_run"',
        'approval_allowed = $false',
        'final_decision = "needs_review"',
    ]
    for item in expected:
        assert item in content


def test_end_to_end_fixture_poc_demo_milestone_records_scope_and_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: End-to-End Fixture POC Demo v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "Business Demo Visibility Track" in content
    assert "watch-constraintos-poc.ps1" in content
    assert "Load the graphics validation contract/specification." in content
    assert "Generate final candidate review packet." in content
    assert "runs/poc-demo/<scenario>/<timestamp>/demo-summary.json" in content
    assert "pytest tests/test_end_to_end_fixture_poc_demo.py" in content
    assert "Product correction recorded" in content
    assert "Constraint-Driven Graphic Output Permutation POC v1" in content
    assert "No local image file opening." in content
    assert "No network fetch." in content
    assert "No image decoding." in content
    assert "No automatic candidate approval." in content


def test_demo_outline_points_to_corrected_graphic_output_poc_demo() -> None:
    content = DEMO_OUTLINE.read_text(encoding="utf-8")

    assert "recommended_next_milestone: Constraint-Driven Graphic Output Permutation POC v1" in content
    assert "primary_output: scripts/watch-constraintos-output-poc.ps1" in content
    assert "verification: pytest tests/test_constraint_driven_graphic_output_permutation_poc.py" in content
    assert "graphic output permutations" in content
    assert "input_constraints + scenario instructions -> graphic output permutations -> validation evidence -> reviewable result" in content


def test_command_reference_includes_end_to_end_fixture_poc_demo() -> None:
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "End-to-end fixture POC demo" in command_reference
    assert ".\\scripts\\watch-constraintos-poc.ps1" in command_reference
    assert "pytest tests/test_end_to_end_fixture_poc_demo.py" in command_reference
