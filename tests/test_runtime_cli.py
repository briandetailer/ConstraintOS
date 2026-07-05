import argparse
import json

import pytest

from constraintos.runtime_cli import main, parse_worker, summarize_payload, workers_from_args


def test_parse_worker_declares_capabilities() -> None:
    worker = parse_worker("WORKER-0001:generic,echo")

    assert worker.worker_id == "WORKER-0001"
    assert worker.plugins == ["generic", "echo"]


def test_parse_worker_rejects_missing_capabilities() -> None:
    with pytest.raises(argparse.ArgumentTypeError, match="at least one plugin"):
        parse_worker("WORKER-0001:")


def test_workers_from_args_uses_default_only_when_none_are_supplied() -> None:
    default_workers = workers_from_args(None)
    explicit_workers = workers_from_args(["WORKER-0002:echo"])

    assert [worker.worker_id for worker in default_workers] == ["WORKER-0001"]
    assert default_workers[0].plugins == ["generic", "echo", "dry_run"]
    assert [worker.worker_id for worker in explicit_workers] == ["WORKER-0002"]
    assert explicit_workers[0].plugins == ["echo"]


def test_runtime_cli_plan_only_prints_plan_and_schedule(tmp_path, capsys) -> None:
    spec = tmp_path / "runtime.yaml"
    spec.write_text(
        """
artifact:
  id: SPEC-0001
execution_steps:
  - id: NODE-0001
    plugin: echo
    action: prepare
""".strip(),
        encoding="utf-8",
    )

    exit_code = main([str(spec), "--plan-only", "--worker", "WORKER-0001:echo"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["plan"]["execution_plan"]["status"] == "planned"
    assert payload["schedule"]["schedule_result"]["status"] == "scheduled"
    assert payload["schedule"]["assignments"][0]["node_id"] == "NODE-0001"
    assert "execution" not in payload


def test_runtime_cli_plan_only_returns_failure_when_unscheduled(tmp_path, capsys) -> None:
    spec = tmp_path / "runtime.yaml"
    spec.write_text(
        """
artifact:
  id: SPEC-0001
execution_steps:
  - id: NODE-0001
    plugin: missing
    action: prepare
""".strip(),
        encoding="utf-8",
    )

    exit_code = main([str(spec), "--plan-only", "--worker", "WORKER-0001:echo"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 1
    assert payload["schedule"]["schedule_result"]["status"] == "partial"
    assert payload["schedule"]["unscheduled_nodes"] == ["NODE-0001"]


def test_runtime_cli_plan_only_can_print_text_summary(tmp_path, capsys) -> None:
    spec = tmp_path / "runtime.yaml"
    spec.write_text(
        """
artifact:
  id: SPEC-0001
execution_steps:
  - id: NODE-0001
    plugin: echo
    action: prepare
""".strip(),
        encoding="utf-8",
    )

    exit_code = main([str(spec), "--plan-only", "--format", "text", "--worker", "WORKER-0001:echo"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Plan PLAN-0001: planned | nodes=1 | stages=1 | plugins=echo" in output
    assert "Schedule SCHEDULE-0001: scheduled | assignments=1 | unscheduled=0" in output


def test_runtime_cli_runs_dry_run_specification(tmp_path, capsys) -> None:
    spec = tmp_path / "runtime.yaml"
    spec.write_text(
        """
artifact:
  id: SPEC-0001
execution_steps:
  - id: NODE-0001
    plugin: generic
    action: prepare
""".strip(),
        encoding="utf-8",
    )

    exit_code = main([str(spec), "--worker", "WORKER-0001:generic", "--artifact-root", str(tmp_path / "artifacts")])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["runtime_result"]["status"] == "completed"
    assert payload["execution"]["node_results"][0]["outputs"] == ["dry-run://NODE-0001"]


def test_runtime_cli_runs_dry_run_specification_with_text_summary(tmp_path, capsys) -> None:
    spec = tmp_path / "runtime.yaml"
    spec.write_text(
        """
artifact:
  id: SPEC-0001
execution_steps:
  - id: NODE-0001
    plugin: generic
    action: prepare
""".strip(),
        encoding="utf-8",
    )

    exit_code = main([str(spec), "--format", "text", "--worker", "WORKER-0001:generic", "--artifact-root", str(tmp_path / "artifacts")])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Runtime RUNTIME-0001: completed (success=True)" in output
    assert "Execution EXEC-RESULT-0001: complete | nodes=1" in output


def test_runtime_cli_writes_output_file(tmp_path, capsys) -> None:
    spec = tmp_path / "runtime.json"
    output = tmp_path / "result.json"
    spec.write_text(
        json.dumps({"artifact": {"id": "SPEC-0001"}, "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}]}),
        encoding="utf-8",
    )

    exit_code = main([str(spec), "--worker", "WORKER-0001:generic", "--artifact-root", str(tmp_path / "artifacts"), "--output", str(output)])

    assert exit_code == 0
    assert "Wrote runtime result" in capsys.readouterr().out
    assert json.loads(output.read_text(encoding="utf-8"))["runtime_result"]["success"] is True


def test_runtime_cli_writes_text_output_file(tmp_path, capsys) -> None:
    spec = tmp_path / "runtime.json"
    output = tmp_path / "result.txt"
    spec.write_text(
        json.dumps({"artifact": {"id": "SPEC-0001"}, "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}]}),
        encoding="utf-8",
    )

    exit_code = main([str(spec), "--format", "text", "--worker", "WORKER-0001:generic", "--artifact-root", str(tmp_path / "artifacts"), "--output", str(output)])

    assert exit_code == 0
    assert "Wrote runtime result" in capsys.readouterr().out
    assert "Runtime RUNTIME-0001: completed" in output.read_text(encoding="utf-8")


def test_runtime_cli_writes_plan_only_output_file(tmp_path, capsys) -> None:
    spec = tmp_path / "runtime.json"
    output = tmp_path / "plan.json"
    spec.write_text(
        json.dumps({"artifact": {"id": "SPEC-0001"}, "execution_steps": [{"id": "NODE-0001", "plugin": "echo", "action": "prepare"}]}),
        encoding="utf-8",
    )

    exit_code = main([str(spec), "--plan-only", "--worker", "WORKER-0001:echo", "--output", str(output)])

    assert exit_code == 0
    assert "Wrote runtime plan" in capsys.readouterr().out
    assert json.loads(output.read_text(encoding="utf-8"))["plan"]["execution_plan"]["status"] == "planned"


def test_summarize_payload_includes_artifact_count() -> None:
    summary = summarize_payload({"artifacts": {"artifact_store": {"count": 3}}})

    assert summary == "Artifacts: 3\n"


def test_runtime_cli_returns_error_code_for_invalid_worker(capsys) -> None:
    exit_code = main(["missing.yaml", "--worker", "WORKER-0001:"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "ERROR: workers must declare at least one plugin" in captured.err


def test_runtime_cli_returns_error_code_for_missing_specification(capsys) -> None:
    exit_code = main(["missing.yaml"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "ERROR:" in captured.err
    assert "missing.yaml" in captured.err


def test_runtime_cli_runs_plugin_executor_and_report(tmp_path) -> None:
    spec = tmp_path / "runtime.yaml"
    artifact_root = tmp_path / "artifacts"
    spec.write_text(
        """
artifact:
  id: SPEC-0001
execution_steps:
  - id: NODE-0001
    plugin: echo
    action: package
""".strip(),
        encoding="utf-8",
    )

    exit_code = main([
        str(spec),
        "--plugin-executor",
        "--worker",
        "WORKER-0001:echo",
        "--artifact-root",
        str(artifact_root),
        "--report",
    ])

    report = artifact_root / "reports" / "RUNTIME-0001.json"
    assert exit_code == 0
    assert report.exists()
    assert json.loads(report.read_text(encoding="utf-8"))["runtime_result"]["status"] == "completed"
