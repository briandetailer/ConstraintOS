from constraintos.validation_cli import main

RENDER_SPECIFICATION = "examples/render/lf4_engine_render_specification.yaml"
CONSTRAINT_PACK = "examples/constraint_packs/lf4_engine_constraint_pack.yaml"


def test_validation_cli_type_check_one(capsys) -> None:
    exit_code = main([CONSTRAINT_PACK])

    assert exit_code == 2
    assert capsys.readouterr().err


def test_validation_cli_type_check_two(capsys) -> None:
    exit_code = main([RENDER_SPECIFICATION, "--constraint-pack", RENDER_SPECIFICATION])

    assert exit_code == 2
    assert capsys.readouterr().err
