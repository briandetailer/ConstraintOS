from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYNTHESIS_LOG = ROOT / "docs" / "800_Demos" / "Current_Evidence_Harness_POC_Demo_Feedback_Synthesis_Log.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_feedback_synthesis_log_exists_and_frames_purpose() -> None:
    content = SYNTHESIS_LOG.read_text(encoding="utf-8")

    assert "# Current Evidence-Harness POC Demo Feedback Synthesis Log" in content
    assert "status: synthesis-log" in content
    assert "triage_guide: docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Triage_Guide.md" in content
    assert "future_target_bank: Constraint-Driven Graphic Output Permutation POC v1" in content
    assert "turns triaged reviewer feedback into prioritized action decisions" in content


def test_feedback_synthesis_log_has_actionable_table_and_decisions() -> None:
    content = SYNTHESIS_LOG.read_text(encoding="utf-8")

    expected = [
        "| ID | Source | Feedback theme | Primary category | Severity | Current-demo or later track | Decision | Follow-up | Status |",
        "FDBK-001",
        "accept_now",
        "bank_for_later",
        "needs_more_signal",
        "reject_or_close",
    ]
    for item in expected:
        assert item in content


def test_feedback_synthesis_log_preserves_current_vs_later_boundaries() -> None:
    content = SYNTHESIS_LOG.read_text(encoding="utf-8")

    expected = [
        "README clarity",
        "demo narration clarity",
        "inspection order clarity",
        "needs_review explanation",
        "generated final graphics",
        "constraint-derived graphic output permutations",
        "real local image input",
        "image decoding",
        "CV/OCR provider integration",
        "automatic approval",
    ]
    for item in expected:
        assert item in content


def test_feedback_synthesis_log_has_prioritization_and_guardrails() -> None:
    content = SYNTHESIS_LOG.read_text(encoding="utf-8")

    expected = [
        "Fix blocking current-demo comprehension issues first.",
        "Improve reviewer trust and clarity second.",
        "Bank output-generation requests for the output-permutation track.",
        "This log is documentation-only.",
        "This log does not authorize local image loading.",
        "This log does not authorize network fetch.",
        "This log does not authorize image decoding.",
        "This log does not authorize CV/OCR provider integration.",
        "This log does not authorize automatic approval.",
    ]
    for item in expected:
        assert item in content


def test_command_reference_includes_feedback_synthesis_log() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Current evidence-harness POC demo feedback synthesis log" in content
    assert "docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Synthesis_Log.md" in content
    assert "pytest tests/test_current_evidence_harness_poc_demo_feedback_synthesis_log.py" in content
