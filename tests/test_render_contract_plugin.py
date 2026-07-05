from pathlib import Path

import pytest
import yaml

from constraintos.render_contract import compile_render_contract_to_runtime
from runtime import RuntimeContext, RuntimeEngine
from runtime.execution import create_default_plugin_executor, create_default_plugin_registry
from runtime.plugins import RenderContractPlugin
from runtime.scheduler import WorkerCapability


def load_lf4_specification() -> dict:
    source = Path("examples/render/lf4_engine_render_specification.yaml")
    return yaml.safe_load(source.read_text(encoding="utf-8"))


def test_render_contract_plugin_validates_required_inputs() -> None:
    result = RenderContractPlugin().execute(
        {
            "node_id": "NODE-0001",
            "worker_id": "WORKER-0001",
            "action": "load_subject",
            "inputs": {"subject": {"id": "LF4-ENGINE"}},
        }
    )

    assert result.status == "complete"
    assert result.outputs == ["render-contract://NODE-0001/load_subject"]
    assert result.metrics["required_input"] == "subject"


def test_render_contract_plugin_rejects_missing_required_input() -> None:
    with pytest.raises(ValueError, match="missing required input"):
        RenderContractPlugin().execute({"node_id": "NODE-0001", "action": "load_subject", "inputs": {}})


def test_default_plugin_registry_includes_render_contract_plugin() -> None:
    registry = create_default_plugin_registry()

    assert registry.supports("render_contract", "load_subject") is True


def test_runtime_engine_executes_compiled_render_contract_with_plugin_executor() -> None:
    runtime_specification = compile_render_contract_to_runtime(load_lf4_specification())
    engine = RuntimeEngine(executor=create_default_plugin_executor())
    result = engine.run(
        runtime_specification,
        [WorkerCapability(worker_id="WORKER-0001", plugins=["render_contract"])],
        RuntimeContext(workspace=Path(".")),
    )

    payload = result.to_dict()
    assert result.success is True
    assert payload["execution"]["node_results"][0]["plugin"] == "render_contract"
    assert payload["execution"]["node_results"][0]["outputs"] == ["render-contract://NODE-0001/load_subject"]
    assert payload["artifacts"]["artifact_store"]["count"] == 4
