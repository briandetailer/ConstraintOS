from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEEDBACK_CARD = ROOT / "docs" / "800_Demos" / "Validated_Output_POC_Demo_Feedback_Card.md"


def test_validated_output_poc_demo_feedback_card_exists() -> None:
    content = FEEDBACK_CARD.read_text(encoding="utf-8")

    expected = [
        "# Validated Output POC Demo Feedback Card",
        "status: ready-for-use",
        "scenario_key: supra_2jz_gte_twin_turbo",
        "primary_use_case: Toyota Supra A80 2JZ-GTE Twin-Turbo Technical Graphic",
        "launcher_script: scripts/run-validated-output-poc-demo.ps1",
        "implementation_authority: deterministic-fixture-safe-validated-demo-launcher-only",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_feedback_card_records_entry_point_and_context() -> None:
    content = FEEDBACK_CARD.read_text(encoding="utf-8")

    expected = [
        ".\\scripts\\run-validated-output-poc-demo.ps1",
        "final decision remains `needs_review`",
        "`approval_allowed` remains `false`",
        "input constraints produce controlled output permutations",
        "deterministic SVG graphics",
        "structural validation evidence",
        "This is not final production artwork",
        "does not authorize automatic approval",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_feedback_card_lists_feedback_prompts() -> None:
    content = FEEDBACK_CARD.read_text(encoding="utf-8")

    expected = [
        "Product clarity",
        "Evidence confidence",
        "Browser usability",
        "Approval safety",
        "Product gap",
        "Did the one-command demo clearly show that constraints define controlled output permutations?",
        "Did the validation report, review packet, browser summary, and launcher summary make the demo feel auditable?",
        "Could you understand the generated browser page without opening JSON files first?",
        "Was it clear that the system preserved needs_review and approval_allowed: false?",
        "What is the most important missing capability before this feels like a complete product demo?",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_feedback_card_lists_classification_and_tags() -> None:
    content = FEEDBACK_CARD.read_text(encoding="utf-8")

    expected = [
        "strong_product_signal",
        "mixed_product_signal",
        "weak_product_signal",
        "browser_clarity",
        "artifact_traceability",
        "validation_trust",
        "workflow_simplicity",
        "business_story",
        "visual_specificity_gap",
        "scope_confusion",
        "approval_safety",
    ]
    for item in expected:
        assert item in content


def test_validated_output_poc_demo_feedback_card_preserves_decision_rules_and_blocked_scope() -> None:
    content = FEEDBACK_CARD.read_text(encoding="utf-8")

    expected = [
        "Continue improving the validated demo path and browser-facing evidence.",
        "Preserve deterministic fixture-safe scope.",
        "Do not add real image generation yet.",
        "Improve the reviewer handoff, browser copy, and artifact traceability before adding capability.",
        "Keep the one-command launcher as the entry point.",
        "Pause feature expansion.",
        "Rework the story around constraints, evidence, review blocking, and output expectations.",
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
    for item in expected:
        assert item in content
