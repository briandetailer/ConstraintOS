from constraintos.local_runtime import create_api_run_command, create_local_deployment_checklist, create_local_runtime_profile, create_worker_run_command


def test_create_local_runtime_profile() -> None:
    profile = create_local_runtime_profile()
    assert profile["local_runtime_profile"]["id"] == "LOCAL-0001"
    assert profile["local_runtime_profile"]["api_port"] == 8000


def test_create_api_run_command() -> None:
    command = create_api_run_command()
    assert command["runtime_command"]["id"] == "COMMAND-0001"
    assert "uvicorn" in command["runtime_command"]["command"]


def test_create_worker_run_command() -> None:
    command = create_worker_run_command()
    assert command["runtime_command"]["id"] == "COMMAND-0002"
    assert "constraintos.worker" in command["runtime_command"]["command"]


def test_create_local_deployment_checklist() -> None:
    checklist = create_local_deployment_checklist()
    assert checklist["local_deployment_checklist"]["id"] == "DEPLOY-0001"
    assert len(checklist["items"]) >= 5
