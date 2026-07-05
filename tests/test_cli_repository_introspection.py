from pathlib import Path

from constraintos.cli import main


def make_repo(root: Path) -> None:
    (root / "schemas").mkdir()
    (root / "schemas" / "example.schema.json").write_text("{}", encoding="utf-8")
    (root / "examples").mkdir()
    (root / "examples" / "EXAMPLE-0001.yaml").write_text("example: true", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests" / "test_example.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs" / "README.md").write_text("# Docs", encoding="utf-8")


def test_repo_inventory_command(tmp_path: Path) -> None:
    make_repo(tmp_path)
    assert main(["repo-inventory", "--repo-root", str(tmp_path)]) == 0


def test_repo_health_command(tmp_path: Path) -> None:
    make_repo(tmp_path)
    assert main(["repo-health", "--repo-root", str(tmp_path)]) == 0


def test_repo_health_command_reviews_empty_repo(tmp_path: Path) -> None:
    assert main(["repo-health", "--repo-root", str(tmp_path)]) == 1
