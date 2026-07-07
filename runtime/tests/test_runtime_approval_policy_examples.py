import json
from pathlib import Path

from jsonschema import validate

from runtime import verify_runtime_approval_policy


EXAMPLE_POLICY_ROOT = Path("examples/runtime/approval-policies")
SCHEMA_PATH = Path("schemas/runtime/v1/runtime-approval-policy.schema.json")


def _example_policy_paths() -> list[Path]:
    return sorted(EXAMPLE_POLICY_ROOT.glob("*.json"))


def test_runtime_approval_policy_examples_exist() -> None:
    assert [path.name for path in _example_policy_paths()] == [
        "default-runtime-approval-v1.json",
        "manual-review-runtime-approval-v1.json",
    ]


def test_runtime_approval_policy_examples_pass_python_verifier() -> None:
    for policy_path in _example_policy_paths():
        policy = json.loads(policy_path.read_text(encoding="utf-8"))

        verification = verify_runtime_approval_policy(policy)

        assert verification.successful(), policy_path.name


def test_runtime_approval_policy_examples_match_json_schema() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    for policy_path in _example_policy_paths():
        policy = json.loads(policy_path.read_text(encoding="utf-8"))

        validate(instance=policy, schema=schema)
