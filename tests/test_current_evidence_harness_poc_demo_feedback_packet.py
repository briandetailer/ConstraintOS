from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_PACKET = ROOT / "docs" / "800_Demos" / "Current_Evidence_Harness_POC_Demo_Feedback_Packet.md"


def test_current_evidence_harness_demo_feedback_packet_exists_and_frames_context() -> None:
    content = FEEDBACK_PACKET.read_text(encoding="utf-8")

    assert "# Current Evidence-Harness POC Demo Feedback Packet" in content
    assert "current_script: scripts/watch-constraintos-poc.ps1" in content
    assert "future_target_bank: Constraint-Driven Graphic Output Permutation POC v1" in content
    assert "not the final graphics-output demo yet" in content
    assert "expected result is needs_review" in content


def test_current_evidence_harness_demo_feedback_packet_records_review_focus() -> None:
    content = FEEDBACK_PACKET.read_text(encoding="utf-8")

    expected = [
        "Can you tell what the system is trying to do?",
        "Can you follow the staged terminal output?",
        "Does the run folder make the result feel auditable?",
        "Does final_decision: needs_review make sense?",
        "Does the future output-permutation direction make sense?",
    ]
    for item in expected:
        assert item in content


def test_current_evidence_harness_demo_feedback_packet_lists_evidence_files() -> None:
    content = FEEDBACK_PACKET.read_text(encoding="utf-8")

    expected = [
        "watch-output.txt",
        "demo-summary.json",
        "final-review-packet.json",
        "run-metadata.json",
        "contract.json",
        "candidate-manifest.json",
        "candidate-intake-review-packet.json",
        "byte-loading.json",
        "fixture-registry-failure-review-packet.json",
        "manual-observations.json",
        "observation-binding.json",
        "merged-evidence.json",
        "evaluation-report.json",
    ]
    for item in expected:
        assert item in content


def test_current_evidence_harness_demo_feedback_packet_contains_copyable_form() -> None:
    content = FEEDBACK_PACKET.read_text(encoding="utf-8")

    expected = [
        "Reviewer name:",
        "Scenario reviewed:",
        "Run folder reviewed:",
        "In one sentence, what do you think ConstraintOS does?",
        "Did the demo feel like a real workflow?",
        "Which evidence file was most useful?",
        "What would you expect the future generated graphic-output permutations to look like?",
        "What should be built next?",
    ]
    for item in expected:
        assert item in content


def test_current_evidence_harness_demo_feedback_packet_records_classification_labels() -> None:
    content = FEEDBACK_PACKET.read_text(encoding="utf-8")

    expected = [
        "product_clarity",
        "demo_flow",
        "evidence_quality",
        "technical_trust",
        "future_output_expectations",
        "ux_readability",
        "risk_or_gap",
        "next_step",
    ]
    for item in expected:
        assert item in content


def test_current_evidence_harness_demo_feedback_packet_preserves_guardrails() -> None:
    content = FEEDBACK_PACKET.read_text(encoding="utf-8")

    expected = [
        "No generated series of final graphics yet.",
        "No constraint-derived graphic output permutations yet.",
        "No arbitrary local image file input.",
        "No artifact download.",
        "No network fetch.",
        "No image decoding.",
        "No CV/OCR provider integration.",
        "No unrestricted image generation.",
        "No automatic candidate approval.",
    ]
    for item in expected:
        assert item in content


def test_current_evidence_harness_demo_feedback_packet_records_local_verification() -> None:
    content = FEEDBACK_PACKET.read_text(encoding="utf-8")

    assert "git pull --rebase origin phase-1-cli-tooling" in content
    assert "pytest tests/test_current_evidence_harness_poc_demo_feedback_packet.py" in content
