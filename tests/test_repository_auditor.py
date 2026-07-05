from pathlib import Path

from constraintos.repository_auditor import audit_to_markdown, create_artifact_coverage_report, create_schema_coverage_report, create_technical_debt_report, run_repository_audit


def test_schema_coverage_report_detects_missing_registered_schemas(tmp_path: Path) -> None:
    (tmp_path / "schemas").mkdir()
    report = create_schema_coverage_report(tmp_path)
    assert report["schema_coverage_report"]["status"] == "fail"
    assert report["schema_coverage_report"]["missing_registered_count"] > 0


def test_artifact_coverage_report_detects_example(tmp_path: Path) -> None:
    examples = tmp_path / "examples"
    examples.mkdir()
    (examples / "failure.yaml").write_text("failure:\n  id: FR-0001\n  title: Test\n  status: draft\n", encoding="utf-8")
    report = create_artifact_coverage_report(tmp_path)
    assert report["artifact_coverage_report"]["example_count"] == 1
    assert report["artifact_coverage_report"]["undetected_count"] == 0


def test_technical_debt_report_detects_todo(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    (src / "example.py").write_text("# TODO: fix later\n", encoding="utf-8")
    report = create_technical_debt_report(tmp_path)
    assert report["technical_debt_report"]["todo_file_count"] == 1


def test_run_repository_audit_returns_report(tmp_path: Path) -> None:
    (tmp_path / "schemas").mkdir()
    (tmp_path / "examples").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "docs").mkdir()
    (tmp_path / "src").mkdir()
    audit = run_repository_audit(tmp_path)
    data = audit.to_dict()
    assert data["repository_audit"]["id"] == "REPO-AUDIT-0001"
    assert "schema_coverage" in data


def test_audit_to_markdown() -> None:
    audit = run_repository_audit(".")
    markdown = audit_to_markdown(audit)
    assert "# ConstraintOS Repository Audit" in markdown
    assert "## Inventory" in markdown
