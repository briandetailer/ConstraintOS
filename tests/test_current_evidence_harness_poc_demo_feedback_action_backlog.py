from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "docs" / "800_Demos" / "Current_Evidence_Harness_POC_Demo_Feedback_Action_Backlog.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_current_evidence_harness_feedback_action_backlog_exists_and_frames_scope() -> None:
    content = BACKLOG.read_text(encoding="utf-8")

    assert "# Current Evidence-Harness POC Demo Feedback Action Backlog" in content
    assert "status: action-backlog" in content
    assert "synthesis_log: docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Synthesis_Log.md" in content
    assert "triage_guide: docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Triage_Guide.md" in content
    assert "future_target_bank: Constraint-Driven Graphic Output Permutation POC v1" in content
    assert "Do not add raw reviewer comments directly." in content


def test_current_evidence_harness_feedback_action_backlog_has_current_and_later_lanes() -> None:
    content = BACKLOG.read_text(encoding="utf-8")

    expected = [
        "## Current-demo polish backlog",
        "## Banked later-work backlog",
        "ACT-001",
        "BANK-001",
        "Constraint-driven graphic output permutations",
        "Requires explicit output-generation milestone",
        "banked",
    ]
    for item in expected:
        assert item in content


def test_current_evidence_harness_feedback_action_backlog_defines_status_and_priorities() -> None:
    content = BACKLOG.read_text(encoding="utf-8")

    expected = [
        "open: not started",
        "accepted: ready for a scoped current-demo polish slice",
        "in_progress: actively being worked",
        "complete: implemented and verified",
        "banked: intentionally held for later gated milestone",
        "closed: not actionable, duplicate, or outside current direction",
        "Resolve blocking current-demo comprehension issues first.",
        "Bank output-generation and real-input requests instead of implementing them here.",
    ]
    for item in expected:
        assert item in content


def test_current_evidence_harness_feedback_action_backlog_preserves_guardrails() -> None:
    content = BACKLOG.read_text(encoding="utf-8")

    expected = [
        "This backlog is documentation-only.",
        "This backlog does not authorize new processing capability.",
        "This backlog does not authorize local image loading.",
        "This backlog does not authorize artifact download.",
        "This backlog does not authorize network fetch.",
        "This backlog does not authorize image decoding.",
        "This backlog does not authorize CV/OCR provider integration.",
        "This backlog does not authorize unrestricted image generation or editing.",
        "This backlog does not authorize automatic approval.",
    ]
    for item in expected:
        assert item in content


def test_command_reference_includes_current_evidence_harness_feedback_action_backlog() -> None:
    command_reference = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Current evidence-harness POC demo feedback action backlog" in command_reference
    assert "docs/800_Demos/Current_Evidence_Harness_POC_Demo_Feedback_Action_Backlog.md" in command_reference
    assert "pytest tests/test_current_evidence_harness_poc_demo_feedback_action_backlog.py" in command_reference
