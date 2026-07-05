import json
from pathlib import Path

from constraintos.runtime_cli import main


def test_echo_pipeline_example_runs_with_plugin_executor(tmp_path, capsys) -> None:
    source = Path("examples/runtime/echo_pipeline.yaml")
    artifact_root = tmp_path / "artifacts"

    exit_code = main([
        str(source),
        "--plugin-executor",
        "--worker",
        "WORKER-0001:echo",
        "--artifact-root",
        str(artifact_root),
        "--report",
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["runtime_result"]["status"] == "completed"
    assert payload["artifacts"]["artifact_store"]["count"] == 3
    assert [node["status"] for node in payload["execution"]["node_results"]] == ["complete", "complete"]
    assert (artifact_root / "reports" / "RUNTIME-0001.json").exists()
