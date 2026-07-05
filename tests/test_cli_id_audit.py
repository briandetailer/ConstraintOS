from pathlib import Path

from constraintos.cli import main


def test_id_audit_command_passes_empty_repo(tmp_path: Path) -> None:
    assert main(["id-audit", "--repo-root", str(tmp_path)]) == 0


def test_id_audit_command_fails_duplicates(tmp_path: Path) -> None:
    examples = tmp_path / "examples"
    examples.mkdir()
    (examples / "one.yaml").write_text("thing:\n  id: DUP-0001\n", encoding="utf-8")
    (examples / "two.yaml").write_text("thing:\n  id: DUP-0001\n", encoding="utf-8")
    assert main(["id-audit", "--repo-root", str(tmp_path)]) == 1
