import json

from constraintos.runtime_cli import default_workers_for_mode, main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"


def test_render_contract_mode_uses_render_contract_default_worker() -> None:
    assert default_workers_for_mode(render_contract=True) == ["WORKER-0001:render_contract"]
    assert default_workers_for_mode(render_contract=False) == ["WORKER-0001:generic,echo,dry_run"]


def test_runtime_cli_plan_only_can_compile_render_contract(capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--render-contract",
        "--plan-only",
        "--worker",
        "WORKER-0001:render_contract",
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["plan"]["required_plugins"] == ["render_contract"]
    assert len(payload["plan"]["nodes"]) == 4
    assert payload["schedule"]["schedule_result"]["status"] == "scheduled"


def test_runtime_cli_render_contract_plan_only_works_without_explicit_worker(capsys) -> None:
    exit_code = main([RENDER_SPECIFICATION, "--render-contract", "--plan-only"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["schedule"]["assignments"][0]["worker_id"] == "WORKER-0001"
    assert payload["schedule"]["assignments"][0]["plugin"] == "render_contract"


def test_runtime_cli_can_execute_render_contract_with_plugin_executor(tmp_path, capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--render-contract",
        "--plugin-executor",
        "--worker",
        "WORKER-0001:render_contract",
        "--artifact-root",
        str(tmp_path / "artifacts"),
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["runtime_result"]["success"] is True
    assert payload["execution"]["node_results"][0]["plugin"] == "render_contract"
    assert payload["artifacts"]["artifact_store"]["count"] == 4
