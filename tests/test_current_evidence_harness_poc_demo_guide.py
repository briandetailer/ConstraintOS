from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "800_Demos" / "Current_Evidence_Harness_POC_Demo_Guide.md"


def test_current_evidence_harness_poc_demo_guide_exists_and_names_current_script() -> None:
    content = GUIDE.read_text(encoding="utf-8")

    assert "demo: Current Evidence-Harness POC Demo" in content
    assert "current_script: scripts/watch-constraintos-poc.ps1" in content
    assert "future_target_bank: Constraint-Driven Graphic Output Permutation POC v1" in content
    assert ".\\scripts\\watch-constraintos-poc.ps1 -Scenario perseverance" in content


def test_current_evidence_harness_poc_demo_guide_separates_current_and_future_output_targets() -> None:
    content = GUIDE.read_text(encoding="utf-8")

    assert "It does not yet generate a series of new graphics." in content
    assert "later output-permutation goal is intentionally banked" in content
    assert "It does not derive graphic-output permutations from constraints yet." in content
    assert "The next product-shaped demo will add the missing output layer" in content


def test_current_evidence_harness_poc_demo_guide_lists_auditable_outputs_and_guardrails() -> None:
    content = GUIDE.read_text(encoding="utf-8")

    expected = [
        "runs/poc-demo/<scenario>/<timestamp>/",
        "watch-output.txt",
        "demo-summary.json",
        "final-review-packet.json",
        "run-metadata.json",
        "final_decision: needs_review",
        "approval_allowed: false",
        "It does not accept arbitrary local image files.",
        "It does not fetch network resources.",
        "It does not decode images.",
        "It does not automatically approve candidates.",
    ]
    for item in expected:
        assert item in content


def test_current_evidence_harness_poc_demo_guide_includes_local_verification() -> None:
    content = GUIDE.read_text(encoding="utf-8")

    assert "git pull --rebase origin phase-1-cli-tooling" in content
    assert "pytest tests/test_end_to_end_fixture_poc_demo.py" in content
    assert ".\\scripts\\watch-constraintos-poc.ps1 -Scenario perseverance" in content
