from pathlib import Path

from constraintos.cli import main, record_from_data


def test_cli_record_from_registry_artifact() -> None:
    record = record_from_data(Path("examples/local_runtime/LOCAL-0001.yaml"), {"local_runtime_profile": {"id": "LOCAL-0001", "name": "local-development"}})
    assert record is not None
    assert record["id"] == "LOCAL-0001"
    assert record["type"] == "local_runtime_profile"


def test_cli_record_from_special_rule() -> None:
    record = record_from_data(Path("health.yaml"), {"status": "ok", "service": "constraintos-api", "version": "1.0"})
    assert record is not None
    assert record["type"] == "api_health_response"


def test_registry_report_command_runs() -> None:
    assert main(["registry-report"]) == 0


def test_registry_check_command_accepts_missing_root(tmp_path: Path) -> None:
    assert main(["registry-check", "--repo-root", str(tmp_path)]) == 1
