from pathlib import Path

import yaml

from constraintos.render_contract import compile_render_contract_to_runtime
from runtime.planner import RuntimePlanner
from runtime.scheduler import RuntimeScheduler, WorkerCapability


def load_lf4_specification() -> dict:
    source = Path("examples/render/lf4_engine_render_specification.yaml")
    return yaml.safe_load(source.read_text(encoding="utf-8"))


def test_compile_render_contract_to_runtime_creates_gate_pipeline() -> None:
    runtime_specification = compile_render_contract_to_runtime(load_lf4_specification())

    assert runtime_specification["artifact"]["id"] == "RSPEC-0001"
    assert runtime_specification["artifact"]["type"] == "render_contract_runtime"
    assert [step["action"] for step in runtime_specification["execution_steps"]] == [
        "load_subject",
        "check_requirements",
        "check_negative_constraints",
        "check_validation_gates",
    ]
    assert runtime_specification["execution_steps"][3]["depends_on"] == ["NODE-0003"]


def test_compiled_render_contract_can_be_planned_and_scheduled() -> None:
    runtime_specification = compile_render_contract_to_runtime(load_lf4_specification())
    plan = RuntimePlanner().build(runtime_specification)
    schedule = RuntimeScheduler().schedule(plan, [WorkerCapability(worker_id="WORKER-0001", plugins=["render_contract"])])

    assert plan.required_plugins == ["render_contract"]
    assert len(plan.stages) == 4
    assert schedule.status == "scheduled"
    assert schedule.unscheduled_nodes == []
