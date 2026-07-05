from pathlib import Path

from constraintos.repository_introspection import create_repository_health_summary, create_repository_inventory


def make_repo(root: Path) -> None:
    (root / "schemas").mkdir()
    (root / "schemas" / "example.schema.json").write_text("{}")
    (root / "examples").mkdir()
    (root / "examples" / "EXAMPLE-0001.yaml").write_text("example: true")
    (root / "tests").mkdir()
    (root / "tests" / "test_example.py").write_text("def test_ok():\n    assert True\n")
    (root / "docs").mkdir()
    (root / "docs" / "README.md").write_text("# Docs")
    (root / "src").mkdir()
    (root / "src" / "module.py").write_text("x = 1")


def test_create_repository_inventory(tmp_path: Path) -> None:
    make_repo(tmp_path)
    inventory = create_repository_inventory(tmp_path)
    assert len(inventory.schemas) == 1
    assert len(inventory.examples) == 1
    assert len(inventory.tests) == 1
    assert len(inventory.docs) == 1
    assert len(inventory.source_files) == 1


def test_repository_health_summary(tmp_path: Path) -> None:
    make_repo(tmp_path)
    summary = create_repository_health_summary(create_repository_inventory(tmp_path))
    assert summary["repository_health_summary"]["schema_count"] == 1
    assert summary["warnings"] == []
