from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "docs" / "800_Demos" / "Current_Evidence_Harness_POC_Demo_Final_Verification_Gate.md"


def test_final_verification_gate_records_remaining_progress_gap() -> None:
    content = GATE.read_text(encoding="utf-8")

    assert "# Current Evidence-Harness POC Demo Final Verification Gate" in content
    assert "current_public_evidence_harness_demo_package_progress: 92%" in content
    assert "reviewer_feedback_operating_loop_progress: 100%" in content
    assert "remaining_completion_gap: 8%" in content


def test_final_verification_gate_records_exact_final_command() -> None:
    content = GATE.read_text(encoding="utf-8")

    assert "git pull --rebase origin phase-1-cli-tooling" in content
    assert "pytest tests/test_end_to_end_fixture_poc_demo.py" in content


def test_final_verification_gate_records_completion_rule() -> None:
    content = GATE.read_text(encoding="utf-8")

    expected = [
        "docs/500_Milestones/End_to_End_Fixture_POC_Demo_v1.md",
        "docs/800_Demos/Current_Evidence_Harness_POC_Demo_Progress_Snapshot.md",
        "update the progress snapshot from 92% to 100%",
        "current_public_evidence_harness_demo_package_progress: 100%",
        "core_evidence_harness_verification_progress: 100%",
        "final_current_demo_status: complete",
        "Constraint-Driven Graphic Output Permutation POC v1",
    ]
    for item in expected:
        assert item in content


def test_final_verification_gate_preserves_guardrails() -> None:
    content = GATE.read_text(encoding="utf-8")

    expected = [
        "generated final graphics",
        "constraint-derived graphic output permutations",
        "real local image input",
        "local_file_path loading",
        "file_uri loading",
        "artifact download",
        "network fetch",
        "image decoding",
        "pixel inspection",
        "CV/OCR provider integration",
        "unrestricted image generation",
        "automatic approval",
    ]
    for item in expected:
        assert item in content
