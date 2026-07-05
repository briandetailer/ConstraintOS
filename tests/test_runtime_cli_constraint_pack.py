import json

from constraintos.runtime_cli import load_runtime_specification, main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
CONSTRAINT_PACK = "examples/constraint_packs/lf4_engine_constraint_pack.yaml"
RUNTIME_SPECIFICATION = "examples/runtime/echo_pipeline.yaml"


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
        path=__import__("pathlib").Path(RENDER_SPECIFICATION),
        render_contract=True,
        constraint_pack_paths=[CONSTRAINT_PACK],
    )

    assert runtime_specification["artifact"]["id"] == "RSPEC-0001"
    assert [step["plugin"] for step in runtime_specification["execution_steps"]] == ["render_contract"] * 4
