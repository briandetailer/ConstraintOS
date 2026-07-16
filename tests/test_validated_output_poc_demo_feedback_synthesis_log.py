from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "docs" / "800_Demos" / "Validated_Output_POC_Demo_Feedback_Synthesis_Log.md"


def test_validated_output_poc_demo_feedback_synthesis_log_exists() -> None:
    content = LOG.read_text(encoding="utf-8")

    expected = [
        "# Validated Output POC Demo Feedback Synthesis Log",
        "status: ready-for-use",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "source_feedback_card: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md",
        "reviewer_handoff: docs/800_Demos/Validated_Output_POC_Demo_Reviewer_Handoff.md",
        "launcher_script: scripts/run-validated-output-poc-demo.ps1",
        "implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_feedback_synthesis_log_defines_inputs_and_template() -> None:
    content = LOG.read_text(encoding="utf-8")

    expected = [
        "reviewer feedback -> signal classification -> accepted next steps -> deferred ideas -> blocked scope preserved",
        "docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md",
        "validated-output-poc-demo-summary.json",
        "svg-structural-validation.json",
        "graphic-output-review-packet.json",
        "primary_signal: strong_product_signal | mixed_product_signal | weak_product_signal",
        "browser_clarity",
        "artifact_traceability",
        "validation_trust",
        "workflow_simplicity",
        "visual_specificity_gap",
        "approval_safety",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_feedback_synthesis_log_defines_decision_rules() -> None:
    content = LOG.read_text(encoding="utf-8")

    expected = [
        "If strong_product_signal dominates:",
        "Continue improving the validated one-command demo path.",
        "Do not add real image generation yet.",
        "If mixed_product_signal dominates:",
        "Improve reviewer handoff, browser copy, and artifact traceability first.",
        "Avoid expanding runtime capability until the story is clearer.",
        "If weak_product_signal dominates:",
        "Pause feature expansion.",
        "Do not add new processing capabilities.",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_feedback_synthesis_log_defines_follow_up_boundaries() -> None:
    content = LOG.read_text(encoding="utf-8")

    accepted = [
        "Browser copy refinement for the validated output POC page.",
        "Better traceability between constraints, SVG graphics, validation report, review packet, and launcher summary.",
        "Reviewer-facing explanation of needs_review and approval_allowed: false.",
        "Cleaner product story for input constraints -> controlled output permutations -> evidence -> manual review.",
    ]
    for item in accepted:
        assert item in content

    deferred = [
        "Real generated final graphics.",
        "Real local image input.",
        "Pixel-level validation.",
        "CV/OCR provider integration.",
        "Candidate image comparison.",
        "Automatic approval.",
    ]
    for item in deferred:
        assert item in content


def test_validated_output_poc_demo_feedback_synthesis_log_preserves_blocked_scope() -> None:
    content = LOG.read_text(encoding="utf-8")

    blocked = [
        "Production artwork generation.",
        "local_file_path loading.",
        "file_uri loading.",
        "Artifact download.",
        "Network fetch.",
        "Image decoding.",
        "Pixel inspection.",
        "CV/OCR provider integration.",
        "Automatic approval.",
        "status: pending-real-reviewer-feedback",
        "assistant_ran_review: false",
    ]
    for item in blocked:
        assert item in content
