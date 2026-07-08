import json

from constraintos.graphics_contracts_cli import main


def test_graphics_contracts_cli_lists_contracts_text(capsys) -> None:
    exit_code = main(["list"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Graphics contracts: 4" in output
    assert "perseverance" in output
    assert "wind_turbine_nacelle" in output
    assert "hydroelectric_dam_powerhouse" in output
    assert "supra_2jz_gte_twin_turbo" in output
    assert "mode=fixture_only_no_image_generation" in output
    assert "image_generation: not run" not in output


def test_graphics_contracts_cli_lists_contracts_json(capsys) -> None:
    exit_code = main(["--format", "json", "list"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["graphics_contracts"]["count"] == 4
    keys = {contract["key"] for contract in payload["contracts"]}
    assert keys == {
        "perseverance",
        "wind_turbine_nacelle",
        "hydroelectric_dam_powerhouse",
        "supra_2jz_gte_twin_turbo",
    }


def test_graphics_contracts_cli_shows_contract_text(capsys) -> None:
    exit_code = main(["show", "wind_turbine_nacelle"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Graphics contract: wind_turbine_nacelle" in output
    assert "subject: NREL offshore 5-MW baseline wind turbine nacelle / drivetrain" in output
    assert "expected_initial_decision: needs_review" in output
    assert "image_generation: not run" in output


def test_graphics_contracts_cli_shows_contract_json(capsys) -> None:
    exit_code = main(["--format", "json", "show", "supra_2jz_gte_twin_turbo"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert payload["summary"]["key"] == "supra_2jz_gte_twin_turbo"
    assert payload["summary"]["expected_initial_decision"] == "needs_review"
    assert payload["contract"]["subject"]["name"] == "Toyota Supra Mk IV / A80 Turbo 2JZ-GTE sequential twin-turbo system"
    assert "B58" in payload["contract"]["subject"]["forbidden_substitutions"]


def test_graphics_contracts_cli_writes_output_file(tmp_path, capsys) -> None:
    output_path = tmp_path / "contracts.json"

    exit_code = main(["--format", "json", "--output", str(output_path), "list"])

    assert exit_code == 0
    assert "Wrote graphics contract report" in capsys.readouterr().out
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["graphics_contracts"]["count"] == 4


def test_graphics_contracts_cli_rejects_unknown_contract(capsys) -> None:
    exit_code = main(["show", "missing_contract"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Unknown graphics contract" in captured.err
    assert "perseverance" in captured.err
