import json

from constraintos.runtime_cli import load_workers_file


def test_load_workers_file_reads_json_worker_definitions(tmp_path) -> None:
    source = tmp_path / "workers.json"
    source.write_text(json.dumps({"workers": [{"worker_id": "WORKER-0003", "plugins": ["echo"]}]}), encoding="utf-8")

    workers = load_workers_file(source)

    assert workers[0].worker_id == "WORKER-0003"
    assert workers[0].plugins == ["echo"]
