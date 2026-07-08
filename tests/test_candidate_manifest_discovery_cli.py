import json
from pathlib import Path

from constraintos.candidate_manifests import (
    candidate_manifest_key,
    list_candidate_manifest_summaries,
    load_candidate_manifest_report,
)
from constraintos.candidate_manifests_cli import main

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_DIR = ROOT / "examples" / "graphics" / "candidate_evaluation"
COMMAND_REFERENCE = ROOT / "docs" / "700_Use_Cases" / "Graphics_Validation_Command_Reference.md"
PYPROJECT = ROOT / "pyproject.toml"


def test_candidate_manifest_key_removes_fixture_suffix() -> None:
    path = CANDIDATE_DIR / "perseverance_candidate_manifest.fixture.json"

    assert candidate_manifest_key(path) == "perseverance"


def test_candidate_manifest_discovery_lists_static_fixtures() -> None:
    summaries = list_candidate_manifest_summaries(CANDIDATE_DIR)
    keys = {summary["key"] for summary in summaries}
    contract_keys = {summary["contract_key"] for summary in summaries}

    assert keys == {"perseverance", "supra_2jz_gte"}
    assert contract_keys == {"perseverance", "supra_2jz_gte_twin_turbo"}
    assert all(summary["status"] == "static_fixture_only" for summary in summaries)
    assert all(summary["evaluation_status"] == "not_evaluated" for summary in summaries)
    assert all(summary["initial_decision"] == "needs_review" for summary in summaries)


def test_candidate_manifest_report_can_resolve_by_contract_key() -> None:
    report = load_candidate_manifest_report("supra_2jz_gte_twin_turbo", CANDIDATE_DIR)

    assert report["summary"]["key"] == "supra_2jz_gte"
    assert report["summary"]["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert report["summary"]["reference_status"] == "reference_only_not_loaded"
    assert report["summary"]["evaluation_status"] == "not_evaluated"


def test_candidate_manifest_cli_lists_manifests_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "list"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Candidate manifests: 2" in output
    assert "perseverance | contract=perseverance" in output
    assert "supra_2jz_gte | contract=supra_2jz_gte_twin_turbo" in output
    assert "evaluation=not_evaluated" in output
    assert "image_generation: not run" in output
    assert "candidate_evaluation: not run" in output


def test_candidate_manifest_cli_shows_manifest_text(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "show", "supra_2jz_gte_twin_turbo"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Candidate manifest: supra_2jz_gte" in output
    assert "contract_key: supra_2jz_gte_twin_turbo" in output
    assert "reference_status: reference_only_not_loaded" in output
    assert "evaluation_status: not_evaluated" in output
    assert "initial_decision: needs_review" in output
    assert "image_generation: not run" in output
    assert "candidate_evaluation: not run" in output


def test_candidate_manifest_cli_supports_json_output(capsys) -> None:
    exit_code = main(["--project-root", str(ROOT), "--format", "json", "list"])
    output = capsys.readouterr().out
    payload = json.loads(output)

    assert exit_code == 0
    assert payload["candidate_manifests"]["count"] == 2
    assert payload["candidate_manifests"]["read_only"] is True
    assert payload["candidate_manifests"]["image_generation"] == "not_run"
    assert payload["candidate_manifests"]["candidate_evaluation"] == "not_run"


def test_pyproject_exposes_candidate_manifest_cli_entry_point() -> None:
    content = PYPROJECT.read_text(encoding="utf-8")

    assert 'cos-graphics-candidates = "constraintos.candidate_manifests_cli:main"' in content


def test_command_reference_includes_candidate_manifest_discovery_commands() -> None:
    content = COMMAND_REFERENCE.read_text(encoding="utf-8")

    assert "Candidate manifest discovery" in content
    assert "cos-graphics-candidates list" in content
    assert "cos-graphics-candidates show perseverance" in content
    assert "pytest tests/test_candidate_manifest_discovery_cli.py" in content
