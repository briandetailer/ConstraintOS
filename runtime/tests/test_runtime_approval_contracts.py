from runtime import (
    get_runtime_contract,
    runtime_contract_registry,
    verify_artifact_writer_contract_coverage,
    verify_runtime_contract_registry,
)


def test_runtime_approval_contracts_are_registered() -> None:
    assert get_runtime_contract("runtime_approval_decision") is not None
    assert get_runtime_contract("runtime_approval_policy") is not None
    assert get_runtime_contract("runtime_approval_report") is not None


def test_runtime_contract_registry_includes_approval_contracts() -> None:
    registry = runtime_contract_registry()
    names = {contract["name"] for contract in registry["contracts"]}

    assert registry["runtime_contract_registry"]["contract_count"] == len(registry["contracts"])
    assert {
        "runtime_approval_decision",
        "runtime_approval_policy",
        "runtime_approval_report",
    }.issubset(names)
    assert verify_runtime_contract_registry(registry).successful()


def test_runtime_approval_report_writer_has_contract_coverage() -> None:
    verification = verify_artifact_writer_contract_coverage(runtime_contract_registry())

    assert verification.successful()
