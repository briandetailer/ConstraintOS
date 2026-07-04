from pathlib import Path

import yaml

from constraintos.cli import main
from constraintos.patching import build_patch_instruction, create_patch_package, create_regression_baseline


def sample_report() -> dict:
    return {
        "report": {"id": "VAL-0001", "version": "0.1", "created": "2026-07-04", "validator_version": "test"},
        "artifact": {"id": "PLATE-0001", "version": "0.1", "specification_id": "PLATE-0001"},
        "summary": {"blocker_failures": 0, "major_failures": 0, "minor_failures": 0, "uncertain_results": 1},
        "constraint_results": [
            {"constraint_id": "C-0001", "severity": "blocker", "result": "pass", "confidence": 0.9},
            {"constraint_id": "C-0002", "severity": "blocker", "result": "uncertain", "confidence": 0.4, "evidence": "Needs review", "recommended_fix": "Make turbo visible"},
        ],
        "recommendation": "escalate",
    }


def test_patch_instruction_only_includes_failed_or_uncertain() -> None:
    instruction = build_patch_instruction(sample_report())
    assert "C-0002" in instruction
    assert "C-0001" not in instruction
    assert "Do not alter passing constraints" in instruction


def test_create_patch_package() -> None:
    package = create_patch_package(sample_report(), "PATCH-0001")
    data = package.to_dict()
    assert data["patch"]["id"] == "PATCH-0001"
    assert data["failed_constraints"][0]["constraint_id"] == "C-0002"


def test_create_regression_baseline() -> None:
    baseline = create_regression_baseline("PLATE-0001", "0.1", "VAL-0001", ["C-0001"])
    assert baseline["baseline"]["artifact_id"] == "PLATE-0001"
    assert baseline["approved_constraints"] == ["C-0001"]


def test_cli_new_patch(tmp_path: Path) -> None:
    report = tmp_path / "report.yaml"
    output = tmp_path / "patch.yaml"
    report.write_text(yaml.safe_dump(sample_report()))
    rc = main(["new-patch", "PATCH-0001", str(report), "--output", str(output)])
    assert rc == 0
    data = yaml.safe_load(output.read_text())
    assert data["patch"]["id"] == "PATCH-0001"


def test_cli_new_baseline(tmp_path: Path) -> None:
    output = tmp_path / "baseline.yaml"
    rc = main(["new-baseline", "PLATE-0001", "0.1", "VAL-0001", "--constraints", "C-0001,C-0002", "--output", str(output)])
    assert rc == 0
    data = yaml.safe_load(output.read_text())
    assert data["approved_constraints"] == ["C-0001", "C-0002"]
