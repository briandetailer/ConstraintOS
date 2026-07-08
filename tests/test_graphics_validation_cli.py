import json
from pathlib import Path

from constraintos.graphics_validation_cli import DEFAULT_RUNTIME_ID, discover_project_root, main


def test_discover_project_root_finds_perseverance_example() -> None:
    root = discover_project_root(Path.cwd())

    assert (root / "examples" / "graphics" / "perseverance" / "spec.json").exists()


def test_graphics_validation_cli_runs_perseverance_plan_only_json(capsys) -> None:
    exit_code = main(["perseverance", "--plan-only"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["graphics_validation"]["example"] == "perseverance"
    assert payload["graphics_validation"]["subject"] == "NASA Perseverance rover"
    assert payload["graphics_validation"]["expected_decision"] == "needs_review"
    assert payload["plan"]["execution_plan"]["source_id"] == "GRAPHICS-PERSEVERANCE-0001"
    assert payload["schedule"]["schedule_result"]["status"] == "scheduled"
    assert payload["schedule"]["unscheduled_nodes"] == []


def test_graphics_validation_cli_runs_perseverance_runtime_text(capsys, tmp_path) -> None:
    exit_code = main([
        "perseverance",
        "--format",
        "text",
        "--artifact-root",
        str(tmp_path / "artifacts"),
    ])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert f"Runtime {DEFAULT_RUNTIME_ID}: completed (success=True)" in output
    assert "Execution GRAPHICS-PERSEVERANCE-RUNTIME-0001-EXEC-RESULT-0001: complete | nodes=6" in output
    assert "Graphics validation perseverance: subject=NASA Perseverance rover | expected_decision=needs_review" in output


def test_graphics_validation_cli_writes_output_file(tmp_path, capsys) -> None:
    output_path = tmp_path / "graphics-validation.json"

    exit_code = main([
        "perseverance",
        "--plan-only",
        "--output",
        str(output_path),
    ])

    assert exit_code == 0
    assert "Wrote graphics validation result" in capsys.readouterr().out
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["graphics_validation"]["mode"] == "fixture_only_no_image_generation"
    policy_path = Path(payload["graphics_validation"]["policy_path"])
    assert policy_path.parts[-4:] == ("examples", "graphics", "perseverance", "policy.json")


def test_graphics_validation_cli_watch_output(capsys, tmp_path) -> None:
    exit_code = main([
        "perseverance",
        "--watch",
        "--artifact-root",
        str(tmp_path / "artifacts"),
    ])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "ConstraintOS Graphics Validation Watch" in output
    assert "example: perseverance" in output
    assert "subject: NASA Perseverance rover" in output
    assert "[1/6] collect_public_reference_requirements" in output
    assert "[6/6] review_graphics_approval_result" in output
    assert "approval expectation: needs_review" in output
    assert "image generation: not run" in output


def test_graphics_validation_cli_returns_error_for_unknown_example(capsys) -> None:
    exit_code = main(["unknown-example", "--plan-only"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Unsupported graphics validation example" in captured.err
