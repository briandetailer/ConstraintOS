from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass
class RepositoryInventory:
    root: str
    schemas: list[str]
    examples: list[str]
    tests: list[str]
    docs: list[str]
    source_files: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "repository_inventory": {
                "root": self.root,
                "created": date.today().isoformat(),
                "schema_count": len(self.schemas),
                "example_count": len(self.examples),
                "test_count": len(self.tests),
                "doc_count": len(self.docs),
                "source_count": len(self.source_files),
            },
            "schemas": self.schemas,
            "examples": self.examples,
            "tests": self.tests,
            "docs": self.docs,
            "source_files": self.source_files,
        }


def _relative_files(root: Path, pattern: str) -> list[str]:
    return sorted(str(path.relative_to(root)) for path in root.rglob(pattern) if path.is_file())


def create_repository_inventory(repo_root: str | Path = ".") -> RepositoryInventory:
    root = Path(repo_root)
    return RepositoryInventory(
        root=str(root),
        schemas=_relative_files(root, "schemas/*.json"),
        examples=_relative_files(root, "examples/**/*.yaml"),
        tests=_relative_files(root, "tests/test_*.py"),
        docs=_relative_files(root, "docs/**/*.md"),
        source_files=_relative_files(root, "src/**/*.py"),
    )


def create_repository_health_summary(inventory: RepositoryInventory) -> dict[str, Any]:
    warnings: list[str] = []
    if not inventory.schemas:
        warnings.append("No schemas found.")
    if not inventory.examples:
        warnings.append("No examples found.")
    if not inventory.tests:
        warnings.append("No tests found.")
    if not inventory.docs:
        warnings.append("No documentation found.")
    return {
        "repository_health_summary": {
            "status": "pass" if not warnings else "review",
            "created": date.today().isoformat(),
            "schema_count": len(inventory.schemas),
            "example_count": len(inventory.examples),
            "test_count": len(inventory.tests),
            "doc_count": len(inventory.docs),
            "source_count": len(inventory.source_files),
        },
        "warnings": warnings,
    }
