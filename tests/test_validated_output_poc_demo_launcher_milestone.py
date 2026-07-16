from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MILESTONE = ROOT / "docs" / "500_Milestones" / "Validated_Output_POC_Demo_Launcher_v1.md"


def test_validated_output_poc_demo_launcher_milestone_exists() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "# Validated Output POC Demo Launcher v1",
        "status: active",
        "phase_1_validated_demo_launcher_status: ready-for-verification",
        "phase_2_validated_demo_summary_status: ready-for-verification",
        "phase_3_validated_demo_browser_summary_status: ready-for-verification",
        "phase_4_validated_demo_reviewer_handoff_status: ready-for-verification",
        "phase_5_validated_demo_feedback_card_status: ready-for-use",
        "phase_6_validated_demo_feedback_synthesis_status: ready-for-use",
        "previous_milestone: docs/500_Milestones/Deterministic_SVG_Structural_Validation_v1.md",
        "launcher_script: scripts/run-validated-output-poc-demo.ps1",
        "generator_script: scripts/watch-constraintos-output-poc.ps1",
        "validator_script: scripts/validate-output-poc-svg-graphics.ps1",
        "browser_helper_script: scripts/open-latest-output-poc-browser.ps1",
        "reviewer_handoff: docs/800_Demos/Validated_Output_POC_Demo_Reviewer_Handoff.md",
        "feedback_card: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md",
        "feedback_synthesis_log: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Synthesis_Log.md",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_records_product_target() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "one command -> generate output POC -> validate SVG evidence -> write launcher summary -> update browser evidence -> reviewer handoff -> feedback card -> feedback synthesis -> open latest browser UI",
        "Run the fixture-safe output POC generator.",
        "Run the deterministic SVG structural validator.",
        "Write validated-output-poc-demo-summary.json for the latest run.",
        "Add validated-output-poc-demo-summary to the latest browser UI.",
        "Provide a reviewer handoff for the validated one-command demo path.",
        "Provide a reviewer feedback card for structured product signal.",
        "Provide a feedback synthesis log for scoped follow-up decisions.",
        "Open the latest output POC browser UI by default.",
        "Allow a NoOpenBrowser mode for terminal-only verification.",
        "Preserve needs_review and approval_allowed: false.",
        "Preserve deterministic fixture-safe scope.",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_lists_commands() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        ".\\scripts\\run-validated-output-poc-demo.ps1",
        ".\\scripts\\run-validated-output-poc-demo.ps1 -NoOpenBrowser",
        "pytest tests/test_validated_output_poc_demo_launcher_milestone.py",
        "pytest tests/test_run_validated_output_poc_demo_script.py",
        "pytest tests/test_validated_output_poc_demo_reviewer_handoff.py",
        "pytest tests/test_validated_output_poc_demo_feedback_card.py",
        "pytest tests/test_validated_output_poc_demo_feedback_synthesis_log.py",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_defines_summary_artifact() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "## Launcher summary artifact",
        "runs/output-poc/<scenario>/<timestamp>/validated-output-poc-demo-summary.json",
        "launcher",
        "scenario_key",
        "run_dir",
        "browser_ui",
        "validation_report",
        "review_packet",
        "generated_at_local",
        "generator_script",
        "validator_script",
        "browser_helper_script",
        "final_decision: needs_review",
        "approval_allowed: false",
        "blocked_scope_preserved",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_defines_browser_summary_target() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "## Browser summary target",
        "id=\"validated-output-poc-demo-summary\"",
        "validated-output-poc-demo-summary.json",
        "svg-structural-validation.json",
        "graphic-output-review-packet.json",
        "final_decision: needs_review",
        "approval_allowed: false",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_defines_reviewer_handoff() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "## Reviewer handoff",
        "docs/800_Demos/Validated_Output_POC_Demo_Reviewer_Handoff.md",
        "expected terminal evidence",
        "expected browser evidence",
        "expected run artifacts",
        "ready-to-show decision rule",
        "blocked scope",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_defines_feedback_card() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "## Reviewer feedback card",
        "docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md",
        "product clarity",
        "evidence confidence",
        "browser usability",
        "approval safety",
        "product gaps",
        "without authorizing real image generation, real image input, or automatic approval",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_defines_feedback_synthesis_log() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "## Feedback synthesis log",
        "docs/800_Demos/Validated_Output_POC_Demo_Feedback_Synthesis_Log.md",
        "strong, mixed, or weak product signal",
        "accepted follow-up candidates",
        "deferred items",
        "blocked-scope preservation",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_records_implementation_under_verification() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "## Implementation under verification",
        "script: scripts/run-validated-output-poc-demo.ps1",
        "test: tests/test_run_validated_output_poc_demo_script.py",
        "command_reference_update: docs/700_Use_Cases/Graphics_Validation_Command_Reference.md",
        "summary_artifact: validated-output-poc-demo-summary.json",
        "browser_summary_target: validated-output-poc-demo-summary in index.html",
        "reviewer_handoff: docs/800_Demos/Validated_Output_POC_Demo_Reviewer_Handoff.md",
        "reviewer_handoff_test: tests/test_validated_output_poc_demo_reviewer_handoff.py",
        "feedback_card: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Card.md",
        "feedback_card_test: tests/test_validated_output_poc_demo_feedback_card.py",
        "feedback_synthesis_log: docs/800_Demos/Validated_Output_POC_Demo_Feedback_Synthesis_Log.md",
        "feedback_synthesis_log_test: tests/test_validated_output_poc_demo_feedback_synthesis_log.py",
        "status: ready-for-verification",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_launcher_preserves_blocked_scope() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    blocked = [
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
    ]
    for item in blocked:
        assert item in content


def test_validated_output_poc_demo_launcher_done_criteria() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    expected = [
        "[x] Milestone exists.",
        "[x] Previous deterministic SVG structural validation milestone is referenced.",
        "[x] Launcher command is defined.",
        "[x] Generator script dependency is defined.",
        "[x] Validator script dependency is defined.",
        "[x] Browser helper script dependency is defined.",
        "[x] NoOpenBrowser mode is defined.",
        "[x] Launcher summary artifact is defined.",
        "[x] Browser summary target is defined.",
        "[x] Reviewer handoff is defined.",
        "[x] Reviewer feedback card is defined.",
        "[x] Feedback synthesis log is defined.",
        "[x] Blocked scope is preserved.",
        "[x] Launcher script exists.",
        "[ ] Verification result recorded.",
    ]
    for item in expected:
        assert item in content
