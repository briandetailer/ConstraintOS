from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MILESTONE = ROOT / "docs" / "500_Milestones" / "Public_Demo_Reviewer_Entry_Point_v1.md"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"


def test_root_readme_explains_current_public_poc_status() -> None:
    content = README.read_text(encoding="utf-8")

    assert "# ConstraintOS" in content
    assert "Current POC status" in content
    assert "public POC mode" in content
    assert "evidence-harness POC" in content
    assert "does not generate final graphics yet" in content
    assert "validation and traceability layer" in content


def test_root_readme_exposes_current_demo_commands() -> None:
    content = README.read_text(encoding="utf-8")

    expected = [
        ".\\scripts\\watch-constraintos-poc.ps1 -Scenario perseverance",
        ".\\scripts\\watch-constraintos-poc.ps1 -Scenario supra_2jz_gte_twin_turbo",
        ".\\scripts\\watch-constraintos-poc.ps1 -Scenario perseverance -OpenRunFolder",
        "runs/poc-demo/<scenario>/<timestamp>/",
    ]
    for item in expected:
        assert item in content


def test_root_readme_links_reviewer_docs_and_inspection_files() -> None:
    content = README.read_text(encoding="utf-8")

    expected = [
        "docs/800_Demos/Current_Evidence_Harness_POC_Demo_Readiness_Packet.md",
        "docs/800_Demos/Current_Evidence_Harness_POC_Demo_Guide.md",
        "docs/800_Demos/End_to_End_Fixture_POC_Demo_Outline.md",
        "watch-output.txt",
        "demo-summary.json",
        "final-review-packet.json",
        "run-metadata.json",
    ]
    for item in expected:
        assert item in content


def test_root_readme_preserves_limitations_and_future_target() -> None:
    content = README.read_text(encoding="utf-8")

    expected = [
        "No generated series of final graphics yet.",
        "No constraint-derived graphic output permutations yet.",
        "No arbitrary local image file input.",
        "No artifact download.",
        "No network fetch.",
        "No image decoding.",
        "No CV/OCR provider integration.",
        "No unrestricted image generation or editing.",
        "No automatic candidate approval.",
        "Constraint-Driven Graphic Output Permutation POC v1",
        "input constraints + scenario instructions",
        "controlled graphic-output permutations",
    ]
    for item in expected:
        assert item in content


def test_root_readme_records_local_verification_path() -> None:
    content = README.read_text(encoding="utf-8")

    expected = [
        "git pull --rebase origin phase-1-cli-tooling",
        "pytest tests/test_public_demo_reviewer_entry_point.py",
        "pytest tests/test_current_evidence_harness_poc_demo_readiness_packet.py",
        "pytest tests/test_current_evidence_harness_poc_demo_guide.py",
        "pytest tests/test_end_to_end_fixture_poc_demo.py",
    ]
    for item in expected:
        assert item in content


def test_public_demo_reviewer_entry_point_milestone_records_scope() -> None:
    content = MILESTONE.read_text(encoding="utf-8")

    assert "milestone: Public Demo Reviewer Entry Point v1" in content
    assert "status: implementation-complete-pending-test" in content
    assert "current_demo_type: evidence-harness POC demo" in content
    assert "future_target_bank: Constraint-Driven Graphic Output Permutation POC v1" in content
    assert "pytest tests/test_public_demo_reviewer_entry_point.py" in content
    assert "No image decoding." in content
    assert "No automatic candidate approval." in content


def test_command_reference_includes_public_demo_reviewer_entry_point() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Public demo reviewer entry point" in content
    assert "pytest tests/test_public_demo_reviewer_entry_point.py" in content
    assert "README.md" in content
