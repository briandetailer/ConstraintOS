import json
from pathlib import Path

from constraintos.runtime_cli import load_runtime_specification, main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
CONSTRAINT_PACK = "examples/constraint_packs/lf4_engine_constraint_pack.yaml"
RUNTIME_SPECIFICATION = "examples/runtime/echo_pipeline.yaml"
CONSTRAINT_PACK_REFERENCE = {"id": "CPACK-0001", "version": "0.1", "title": "LF4 Engineering Atlas Constraint Pack"}


def test_runtime_cli_render_contract_accepts_constraint_pack(capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--render-contract",
        "--constraint-pack",
        CONSTRAINT_PACK,
        "--plan-only",
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["plan"]["required_plugins"] == ["render_contract"]
    assert len(payload["plan"]["nodes"]) == 4


def test_runtime_cli_plan_only_json_preserves_constraint_pack_traceability(capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--render-contract",
        "--constraint-pack",
        CONSTRAINT_PACK,
        "--plan-only",
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["artifact"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["render_contract"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]


def test_runtime_cli_plan_only_text_reports_constraint_pack_count(capsys) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--render-contract",
        "--constraint-pack",
        CONSTRAINT_PACK,
        "--plan-only",
        "--format",
        "text",
    ])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Plan PLAN-0001: planned | nodes=4 | stages=4 | plugins=render_contract" in output
    assert "Constraint packs: 1" in output


def test_runtime_cli_execution_json_preserves_constraint_pack_traceability(capsys, tmp_path) -> None:
    exit_code = main([
        RENDER_SPECIFICATION,
        "--render-contract",
        "--constraint-pack",
        CONSTRAINT_PACK,
        "--plugin-executor",
        "--artifact-root",
        str(tmp_path / "artifacts"),
    ])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["artifact"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["render_contract"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert payload["runtime_result"]["success"] is True


def test_runtime_cli_rejects_constraint_pack_without_render_contract(capsys) -> None:
    exit_code = main([
        RUNTIME_SPECIFICATION,
        "--constraint-pack",
        CONSTRAINT_PACK,
        "--plan-only",
    ])

    assert exit_code == 2
    assert "--constraint-pack requires --render-contract" in capsys.readouterr().err


def test_load_runtime_specification_applies_constraint_pack_before_compiling() -> None:
    runtime_specification = load_runtime_specification(
        path=Path(RENDER_SPECIFICATION),
        render_contract=True,
        constraint_pack_paths=[CONSTRAINT_PACK],
    )

    assert runtime_specification["artifact"]["id"] == "RSPEC-0001"
    assert [step["plugin"] for step in runtime_specification["execution_steps"]] == ["render_contract"] * 4


def test_load_runtime_specification_preserves_constraint_pack_traceability() -> None:
    runtime_specification = load_runtime_specification(
        path=Path(RENDER_SPECIFICATION),
        render_contract=True,
        constraint_pack_paths=[CONSTRAINT_PACK, CONSTRAINT_PACK],
    )

    assert runtime_specification["artifact"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
    assert runtime_specification["render_contract"]["constraint_packs"] == [CONSTRAINT_PACK_REFERENCE]
