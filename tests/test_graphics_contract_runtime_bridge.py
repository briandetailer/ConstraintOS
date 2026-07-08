import json

from constraintos.graphics_contract_runtime import (
    build_contract_runtime_payload,
    build_runtime_spec_from_contract,
    build_runtime_workers_for_contract,
)
from constraintos.graphics_contracts import load_json
from constraintos.graphics_contracts_cli import main

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = ROOT / "examples" / "graphics" / "contracts"


def load_contract(name: str) -> dict:
    return load_json(CONTRACT_DIR / name)


def test_contract_runtime_spec_from_supra_contract_preserves_subject_and_steps() -> None:
    contract = load_contract("supra_2jz_gte_twin_turbo.contract.json")

    spec = build_runtime_spec_from_contract(contract, "supra_2jz_gte_twin_turbo")

    assert spec["artifact"]["domain"] == "graphics_validation"
    assert spec["artifact"]["source_contract_key"] == "supra_2jz_gte_twin_turbo"
    assert spec["graphics_request"]["subject"] == "Toyota Supra Mk IV / A80 Turbo 2JZ-GTE sequential twin-turbo system"
    assert "2JZ-GTE inline-six" in spec["required_labels"]
    assert "B58" in spec["forbidden_substitutions"]
    assert len(spec["execution_steps"]) == 6
    assert spec["execution_steps"][3]["inputs"]["evaluation_mode"] == "fixture_only_no_image_generation"


def test_contract_runtime_workers_cover_graphics_plugins() -> None:
    workers = build_runtime_workers_for_contract()
    plugins = {plugin for worker in workers for plugin in worker["plugins"]}

    assert plugins == {
        "reference_collector",
        "constraint_builder",
        "image_prompt_generator",
        "image_evaluator",
        "evidence_manifest_generator",
        "approval_reviewer",
    }


def test_contract_runtime_payload_plan_only_schedules_all_nodes() -> None:
    contract = load_contract("wind_turbine_nacelle.contract.json")

    exit_code, payload = build_contract_runtime_payload("wind_turbine_nacelle", contract, plan_only=True)

    assert exit_code == 0
    assert payload["graphics_contract_runtime"]["contract_key"] == "wind_turbine_nacelle"
    assert payload["graphics_contract_runtime"]["image_generation"] == "not_run"
    assert len(payload["plan"]["nodes"]) == 6
    assert len(payload["schedule"]["assignments"]) == 6
    assert payload["schedule"]["unscheduled_nodes"] == []
    assert payload["generated_runtime_spec"]["artifact"]["source_contract_key"] == "wind_turbine_nacelle"


def test_contract_runtime_payload_dry_run_executes_all_nodes(tmp_path) -> None:
    contract = load_contract("hydroelectric_dam_powerhouse.contract.json")

    exit_code, payload = build_contract_runtime_payload(
        "hydroelectric_dam_powerhouse",
        contract,
        artifact_root=tmp_path / "artifacts",
        workspace=tmp_path,
    )

    assert exit_code == 0
    assert payload["runtime_result"]["status"] == "completed"
    assert payload["summary"]["plan_nodes"] == 6
    assert payload["summary"]["scheduled_assignments"] == 6
    assert payload["summary"]["node_results"] == 6
    assert payload["graphics_contract_runtime"]["expected_decision"] == "needs_review"
    assert payload["graphics_contract_runtime"]["image_generation"] == "not_run"


def test_graphics_contracts_cli_runs_contract_bridge_plan_only_text(capsys) -> None:
    exit_code = main(["run", "perseverance", "--plan-only"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Graphics contract runtime: perseverance" in output
    assert "plan_nodes: 6" in output
    assert "unscheduled_nodes: 0" in output
    assert "execution: not_run_plan_only" in output
    assert "image_generation: not run" in output


def test_graphics_contracts_cli_runs_contract_bridge_json(tmp_path, capsys) -> None:
    exit_code = main([
        "--format",
        "json",
        "run",
        "supra_2jz_gte_twin_turbo",
        "--artifact-root",
        str(tmp_path / "artifacts"),
        "--workspace",
        str(tmp_path),
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["graphics_contract_runtime"]["contract_key"] == "supra_2jz_gte_twin_turbo"
    assert payload["graphics_contract_runtime"]["image_generation"] == "not_run"
    assert payload["runtime_result"]["status"] == "completed"
    assert payload["summary"]["node_results"] == 6
