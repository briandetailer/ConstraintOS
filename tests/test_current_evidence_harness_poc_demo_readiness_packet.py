from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS_PACKET = ROOT / "docs" / "800_Demos" / "Current_Evidence_Harness_POC_Demo_Readiness_Packet.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_current_evidence_harness_demo_readiness_packet_exists_and_frames_current_demo() -> None:
    content = READINESS_PACKET.read_text(encoding="utf-8")

    assert "# Current Evidence-Harness POC Demo Readiness Packet" in content
    assert "current_script: scripts/watch-constraintos-poc.ps1" in content
    assert "current_guide: docs/800_Demos/Current_Evidence_Harness_POC_Demo_Guide.md" in content
    assert "future_target_bank: Constraint-Driven Graphic Output Permutation POC v1" in content
    assert "evidence pipeline" in content
    assert "not the final product-shaped graphics-output demo" in content


def test_current_evidence_harness_demo_readiness_packet_records_run_commands() -> None:
    content = READINESS_PACKET.read_text(encoding="utf-8")

    expected = [
        "git pull --rebase origin phase-1-cli-tooling",
        "pytest tests/test_current_evidence_harness_poc_demo_guide.py",
        "pytest tests/test_end_to_end_fixture_poc_demo.py",
        ".\\scripts\\watch-constraintos-poc.ps1 -Scenario perseverance",
        ".\\scripts\\watch-constraintos-poc.ps1 -Scenario supra_2jz_gte_twin_turbo",
        ".\\scripts\\watch-constraintos-poc.ps1 -Scenario perseverance -OpenRunFolder",
    ]
    for item in expected:
        assert item in content


def test_current_evidence_harness_demo_readiness_packet_records_expected_outputs_and_inspection_order() -> None:
    content = READINESS_PACKET.read_text(encoding="utf-8")

    expected_outputs = [
        "runs/poc-demo/<scenario>/<timestamp>/",
        "terminal-transcript.txt",
        "watch-output.txt",
        "contract.json",
        "candidate-manifest.json",
        "candidate-intake-review-packet.json",
        "byte-loading.json",
        "fixture-registry-failure-review-packet.json",
        "manual-observations.json",
        "observation-binding.json",
        "merged-evidence.json",
        "evaluation-report.json",
        "final-review-packet.json",
        "demo-summary.json",
        "run-metadata.json",
    ]
    for item in expected_outputs:
        assert item in content

    assert "1. watch-output.txt" in content
    assert "2. demo-summary.json" in content
    assert "3. final-review-packet.json" in content
    assert "4. run-metadata.json" in content


def test_current_evidence_harness_demo_readiness_packet_preserves_current_limitations_and_future_target() -> None:
    content = READINESS_PACKET.read_text(encoding="utf-8")

    expected = [
        "final_decision: needs_review",
        "approval_allowed: false",
        "No generated series of final graphics yet.",
        "No constraint-derived graphic output permutations yet.",
        "No arbitrary local image file input.",
        "No artifact download.",
        "No network fetch.",
        "No image decoding.",
        "No unrestricted image generation.",
        "No automatic candidate approval.",
        "Constraint-Driven Graphic Output Permutation POC v1",
    ]
    for item in expected:
        assert item in content


def test_command_reference_includes_current_evidence_harness_demo_readiness_packet() -> None:
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Current evidence-harness POC demo readiness packet" in command_reference
    assert "docs/800_Demos/Current_Evidence_Harness_POC_Demo_Readiness_Packet.md" in command_reference
    assert "pytest tests/test_current_evidence_harness_poc_demo_readiness_packet.py" in command_reference
