from pathlib import Path


def test_constraint_pack_cli_entry_point_is_registered() -> None:
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")

    assert 'cos-apply-constraints = "constraintos.constraint_pack_cli:main"' in pyproject
