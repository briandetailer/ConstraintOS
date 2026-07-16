from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "docs" / "800_Demos" / "Validated_Output_POC_Demo_Readiness_Checklist.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_validated_output_poc_demo_readiness_checklist_exists() -> None:
    content = CHECKLIST.read_text(encoding="utf-8")

    expected = [
        "# Validated Output POC Demo Readiness Checklist",
        "status: ready-for-use",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "launcher_script: scripts/run-validated-output-poc-demo.ps1",
        "reviewer_handoff: docs/800_Demos/Validated_Output_POC_Demo_Reviewer_Handoff.md",
        "feedback_card: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md",
        "feedback_synthesis_log: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Synthesis_Log.md",
        "implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_readiness_checklist_defines_local_verification() -> None:
    content = CHECKLIST.read_text(encoding="utf-8")

    expected = [
        "pytest tests/test_validated_output_poc_demo_launcher_milestone.py",
        "pytest tests/test_run_validated_output_poc_demo_script.py",
        "pytest tests/test_validated_output_poc_demo_reviewer_handoff.py",
        "pytest tests/test_validated_output_poc_demo_feedback_card.py",
        "pytest tests/test_validated_output_poc_demo_feedback_synthesis_log.py",
        ".\\scripts\\run-validated-output-poc-demo.ps1",
        "Validated ConstraintOS output POC demo complete.",
        "Browser summary updated:",
        "Final decision remains: needs_review",
        "Approval allowed remains: false",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_readiness_checklist_defines_browser_and_artifacts() -> None:
    content = CHECKLIST.read_text(encoding="utf-8")

    expected = [
        "Deterministic SVG graphics",
        "SVG structural validation",
        "Validated demo launcher",
        "validated-output-poc-demo-summary.json",
        "svg-structural-validation.json",
        "graphic-output-review-packet.json",
        "index.html",
        "run-metadata.json",
        "graphic-output-manifest.json",
        "graphic-output-permutations.json",
        "graphic-output-validation.json",
        "graphics/turbo_system_focus.svg",
        "graphics/inline_six_engine_identity_focus.svg",
        "graphics/technical_label_density_focus.svg",
        "graphics/reviewer_safe_minimal_focus.svg",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_readiness_checklist_defines_ready_and_not_ready_rules() -> None:
    content = CHECKLIST.read_text(encoding="utf-8")

    ready = [
        "ready_to_show = true only when:",
        "all listed tests pass locally;",
        "the launcher runs successfully;",
        "the browser opens the latest generated output POC page;",
        "the browser contains SVG structural validation evidence;",
        "the browser contains validated launcher summary evidence;",
        "the run folder contains the expected JSON and SVG artifacts;",
        "the terminal preserves needs_review and approval_allowed: false;",
        "reviewer handoff, feedback card, and synthesis log are available.",
    ]
    for item in ready:
        assert item in content

    not_ready = [
        "Do not mark ready-to-show if:",
        "any listed test fails;",
        "the launcher does not complete;",
        "the browser does not open;",
        "validated-output-poc-demo-summary.json is missing;",
        "svg-structural-validation.json is missing;",
        "graphic-output-review-packet.json is missing;",
        "final decision is anything other than needs_review;",
        "approval_allowed is anything other than false.",
    ]
    for item in not_ready:
        assert item in content


def test_validated_output_poc_demo_readiness_checklist_preserves_blocked_scope_and_pending_state() -> None:
    content = CHECKLIST.read_text(encoding="utf-8")

    expected = [
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
        "readiness_state: pending-local-verification",
        "ready_to_show: false",
        "assistant_ran_tests: false",
        "assistant_ran_demo: false",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_readiness_checklist_is_in_command_reference() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    expected = [
        "pytest tests/test_validated_output_poc_demo_readiness_checklist.py",
        "Readiness checklist:",
        "docs/800_Demos/Validated_Output_POC_Demo_Readiness_Checklist.md",
        "local verification gate",
        "not-ready conditions",
        "ready-to-show decision rule",
    ]
    for item in expected:
        assert item in content
