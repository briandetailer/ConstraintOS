import json

import pytest

from constraintos.runtime_cli import load_workers_file, main, normalize_plugins, workers_from_args


def test_load_workers_file_reads_json_worker_definitions(tmp_path) -> None:
    source = tmp_path / "workers.json"
    source.write_text(json.dumps({"workers": [{"worker_id": "WORKER-0003", "plugins": ["echo"]}]}), encoding="utf-8")

    workers = load_workers_file(source)

    assert workers[0].worker_id == "WORKER-0003"
    assert workers[0].plugins == ["echo"]


def test_normalize_plugins_rejects_non_string_entries() -> None:
    with pytest.raises(ValueError, match="plugins must be non-empty strings"):
        normalize_plugins(["echo", 123], "workers.json worker 1")


def test_load_workers_file_rejects_empty_plugins(tmp_path) -> None:
    source = tmp_path / "workers.json"
    source.write_text(json.dumps({"workers": [{"worker_id": "WORKER-0003", "plugins": []}]}), encoding="utf-8")

    with pytest.raises(ValueError, match="must declare plugins"):
        load_workers_file(source)


def test_workers_from_args_combines_file_and_inline_workers(tmp_path) -> None:
    source = tmp_path / "workers.json"
    source.write_text(json.dumps({"workers": [{"worker_id": "WORKER-0003", "plugins": ["echo"]}]}), encoding="utf-8")

    workers = workers_from_args(["WORKER-0004:generic"], str(source))

    assert [worker.worker_id for worker in workers] == ["WORKER-0003", "WORKER-0004"]


def test_runtime_cli_plan_only_uses_workers_file(tmp_path, capsys) -> None:
    spec = tmp_path / "runtime.json"
    workers = tmp_path / "workers.json"
    spec.write_text(json.dumps({"artifact": {"id": "SPEC-0001"}, "execution_steps": [{"id": "NODE-0001", "plugin": "echo", "action": "prepare"}]}), encoding="utf-8")
    workers.write_text(json.dumps({"workers": [{"worker_id": "WORKER-0003", "plugins": ["echo"]}]}), encoding="utf-8")

    exit_code = main([str(spec), "--plan-only", "--workers-file", str(workers)])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["schedule"]["assignments"][0]["worker_id"] == "WORKER-0003"
