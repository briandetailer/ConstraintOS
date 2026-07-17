import json
from pathlib import Path

from runtime.research_to_render.cli import main

ROOT = Path(__file__).resolve().parents[1]
REQUEST = ROOT / "config" / "research-to-render-examples" / "raspberry-pi-5-io-plate-request.json"
SOURCES = ROOT / "config" / "research-to-render-examples" / "raspberry-pi-5-discovered-sources.json"
SCRIPT = ROOT / "scripts" / "exercise-research-to-render.ps1"
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
    assert payload["render_plan"]["production_mode"] == "source_plate_annotation"
    assert payload["render_plan"]["mode_selection_reason"].startswith(
        "authoritative_fixed_view_source_plate"
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
    assert "runs\\research-to-render\\raspberry-pi-5-io-plate" in content
    assert "LiveWebSearch" in content
    assert "OPENAI_API_KEY" in content
    assert "--live-web-search" in content


def test_installed_cli_entry_point_is_declared() -> None:
    content = PYPROJECT.read_text(encoding="utf-8")
    assert 'cos-research-render = "runtime.research_to_render.cli:main"' in content
