import json
from pathlib import Path

from runtime.research_to_render.cli import main

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "config" / "research-to-render-examples" / "raspberry-pi-5-io-plate-request.json"
SOURCES = ROOT / "config" / "research-to-render-examples" / "raspberry-pi-5-discovered-sources.json"
SCRIPT = ROOT / "scripts" / "exercise-research-to-render.ps1"
GENERATION_SCRIPT = ROOT / "scripts" / "generate-raspberry-pi-5-candidates.ps1"
REPAIR_SCRIPT = ROOT / "scripts" / "repair-constraintos-candidate-run.ps1"
PYPROJECT = ROOT / "pyproject.toml"


def test_research_to_render_cli_writes_a_planned_artifact(tmp_path: Path) -> None:
    output = tmp_path / "research-to-render-plan.json"

    exit_code = main(
        [
            "--request",
            str(REQUEST),
            "--sources",
            str(SOURCES),
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["status"] == "planned"
    assert payload["request"]["subject"] == "Raspberry Pi 5"
    assert payload["render_plan"]["production_mode"] == (
        "reference_conditioned_generation"
    )
    assert payload["render_plan"]["mode_selection_reason"].startswith(
        "authoritative_fixed_view_reference"
    )
    assert payload["render_plan"]["canonical_source_ids"] == [
        "rpi5-official-top-view-source-plate-2026"
    ]
    assert payload["render_plan"]["production_ready"] is False
    assert payload["source_evaluation"]["unsupported_required_features"] == []
    assert payload["discovery"]["provider"] == "recorded_source_fixture"


def test_windows_exercise_runs_request_research_and_render_planning() -> None:
    content = SCRIPT.read_text(encoding="utf-8")

    assert "raspberry-pi-5-io-plate-request.json" in content
    assert "raspberry-pi-5-discovered-sources.json" in content
    assert "runtime.research_to_render.cli" in content
    assert "research-to-render-plan.json" in content
    assert r"runs\research-to-render\raspberry-pi-5-io-plate" in content
    assert "LiveWebSearch" in content
    assert r"lib\openai-credential.ps1" in content
    assert "Ensure-ConstraintOSOpenAIKey" in content
    assert "--live-web-search" in content


def test_windows_generation_exercise_generates_validates_and_auto_repairs() -> None:
    content = GENERATION_SCRIPT.read_text(encoding="utf-8")

    assert "runtime.research_to_render.candidate_generation" in content
    assert "runtime.research_to_render.candidate_validation" in content
    assert "runtime.research_to_render.candidate_repair" in content
    assert "generation-package.json" in content
    assert "generated-candidate-manifest.json" in content
    assert "candidate-validation-manifest.json" in content
    assert "candidate-repair-loop-manifest.json" in content
    assert "MaxRepairAttempts = 2" in content
    assert "DisableAutoRepair" in content
    assert "--max-attempts $MaxRepairAttempts" in content
    assert "-Validate requires -Generate" in content
    assert 'Arguments += "--generate"' in content
    assert r"lib\openai-credential.ps1" in content
    assert "Ensure-ConstraintOSOpenAIKey" in content
    assert "No persisted OpenAI API key was found" not in content


def test_windows_repair_exercise_resumes_an_existing_rejected_run() -> None:
    content = REPAIR_SCRIPT.read_text(encoding="utf-8")

    assert "[Parameter(Mandatory = $true)]" in content
    assert "[string]$RunRoot" in content
    assert "runtime.research_to_render.candidate_repair" in content
    assert "generation-package.json" in content
    assert "generated-candidate-manifest.json" in content
    assert "candidate-validation-manifest.json" in content
    assert "candidate-repair-loop-manifest.json" in content
    assert "Ensure-ConstraintOSOpenAIKey" in content
    assert "Overall machine decision" in content


def test_installed_cli_entry_points_are_declared() -> None:
    content = PYPROJECT.read_text(encoding="utf-8")
    assert 'cos-research-render = "runtime.research_to_render.cli:main"' in content
    assert (
        'cos-generate-candidates = "runtime.research_to_render.candidate_generation:main"'
        in content
    )
    assert (
        'cos-validate-generated-candidates = "runtime.research_to_render.candidate_validation:main"'
        in content
    )
    assert (
        'cos-repair-generated-candidates = "runtime.research_to_render.candidate_repair:main"'
        in content
    )
