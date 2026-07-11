from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "docs" / "800_Demos" / "Current_Evidence_Harness_POC_Demo_Progress_Snapshot.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_current_evidence_harness_progress_snapshot_records_total_progress_figure() -> None:
    content = SNAPSHOT.read_text(encoding="utf-8")

    assert "# Current Evidence-Harness POC Demo Progress Snapshot" in content
    assert "current_public_evidence_harness_demo_package_progress: 92%" in content
    assert "reviewer_feedback_operating_loop_progress: 100%" in content
    assert "core_evidence_harness_verification_progress: 85%" in content
    assert "11 / 12 = 91.7%, rounded to 92%" in content


def test_current_evidence_harness_progress_snapshot_defines_scope_and_open_item() -> None:
    content = SNAPSHOT.read_text(encoding="utf-8")

    expected = [
        "public README demo entry point",
        "current evidence-harness demo guide",
        "current evidence-harness demo readiness packet",
        "current evidence-harness demo feedback packet",
        "GitHub demo feedback issue template",
        "feedback triage guide",
        "feedback synthesis log",
        "feedback action backlog",
        "command-reference discoverability",
        "recorded demo-reviewer verification results",
        "banked future output-permutation target",
        "core end-to-end evidence harness verification closure",
        "pytest tests/test_end_to_end_fixture_poc_demo.py",
    ]
    for item in expected:
        assert item in content


def test_current_evidence_harness_progress_snapshot_preserves_scope_guardrails() -> None:
    content = SNAPSHOT.read_text(encoding="utf-8")

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
        "later gated milestones",
    ]
    for item in expected:
        assert item in content


def test_command_reference_includes_current_evidence_harness_progress_snapshot() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Current evidence-harness POC demo progress snapshot" in content
    assert "docs/800_Demos/Current_Evidence_Harness_POC_Demo_Progress_Snapshot.md" in content
    assert "pytest tests/test_current_evidence_harness_poc_demo_progress_snapshot.py" in content
