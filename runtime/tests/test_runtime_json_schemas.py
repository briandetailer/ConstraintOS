import json
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate

from runtime import RuntimeEngine, runtime_contract_registry, runtime_result_to_trace
from runtime.scheduler import WorkerCapability


SCHEMA_ROOT = Path("schemas/runtime/v1")


def _schema(name: str) -> dict:
    return json.loads((SCHEMA_ROOT / name).read_text(encoding="utf-8"))


def _completed_runtime_result() -> dict:
    specification = {
        "artifact": {"id": "SPEC-0001"},
        "execution_steps": [{"id": "NODE-0001", "plugin": "generic", "action": "prepare"}],
    }
    result = RuntimeEngine().run(specification, [WorkerCapability("WORKER-0001", ["generic"])])
    return result.to_dict()


def _completed_runtime_trace() -> dict:
    return runtime_result_to_trace(_completed_runtime_result()).to_dict()


def test_runtime_contract_registry_matches_json_schema() -> None:
    schema = _schema("runtime-contract-registry.schema.json")

    validate(instance=runtime_contract_registry(), schema=schema)


def test_runtime_contract_registry_schema_rejects_missing_required_contract_fields() -> None:
    schema = _schema("runtime-contract-registry.schema.json")
    registry = runtime_contract_registry()
    registry["contracts"][0].pop("produced_by")

    with pytest.raises(ValidationError):
        validate(instance=registry, schema=schema)


def test_runtime_contract_registry_schema_rejects_unknown_contract_type() -> None:
    schema = _schema("runtime-contract-registry.schema.json")
    registry = runtime_contract_registry()
    registry["contracts"][0]["contract_type"] = "unknown"

    with pytest.raises(ValidationError):
        validate(instance=registry, schema=schema)


def test_runtime_result_matches_json_schema() -> None:
    schema = _schema("runtime-result.schema.json")

    validate(instance=_completed_runtime_result(), schema=schema)


def test_runtime_result_schema_rejects_unknown_status() -> None:
    schema = _schema("runtime-result.schema.json")
    result = _completed_runtime_result()
    result["runtime_result"]["status"] = "unknown"

    with pytest.raises(ValidationError):
        validate(instance=result, schema=schema)


def test_runtime_result_schema_rejects_negative_summary_counts() -> None:
    schema = _schema("runtime-result.schema.json")
    result = _completed_runtime_result()
    result["summary"]["events"] = -1

    with pytest.raises(ValidationError):
        validate(instance=result, schema=schema)


def test_runtime_traceability_matches_json_schema() -> None:
    schema = _schema("runtime-traceability.schema.json")

    validate(instance=_completed_runtime_trace(), schema=schema)


def test_runtime_traceability_schema_rejects_unknown_record_type() -> None:
    schema = _schema("runtime-traceability.schema.json")
    trace = _completed_runtime_trace()
    trace["records"][0]["type"] = "unknown"

    with pytest.raises(ValidationError):
        validate(instance=trace, schema=schema)


def test_runtime_traceability_schema_rejects_non_object_metadata() -> None:
    schema = _schema("runtime-traceability.schema.json")
    trace = _completed_runtime_trace()
    trace["records"][0]["metadata"] = []

    with pytest.raises(ValidationError):
        validate(instance=trace, schema=schema)
