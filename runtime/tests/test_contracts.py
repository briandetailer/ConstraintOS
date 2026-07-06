from runtime import get_runtime_contract, runtime_contract_registry, verify_runtime_contract_registry


def test_runtime_contract_registry_declares_enterprise_boundary_contracts() -> None:
    registry = runtime_contract_registry()

    assert registry["runtime_contract_registry"] == {
        "version": "runtime-contracts/v1",
        "contract_count": 4,
    }
    assert [contract["name"] for contract in registry["contracts"]] == [
        "runtime_result",
        "runtime_traceability",
        "runtime_trace_report",
        "runtime_evidence_manifest",
    ]
    assert registry["contracts"][0]["required_sections"] == [
        "runtime_result",
        "summary",
        "events",
        "messages",
    ]
    assert registry["contracts"][3]["consumed_by"] == [
        "external_audit_clients",
        "ci_cd",
        "enterprise_integrations",
    ]


def test_get_runtime_contract_returns_named_contract() -> None:
    contract = get_runtime_contract("runtime_evidence_manifest")

    assert contract is not None
    assert contract.name == "runtime_evidence_manifest"
    assert contract.produced_by == "RuntimeEvidenceBundleWriter"
    assert contract.required_sections == ("runtime_evidence", "artifacts")
    assert get_runtime_contract("missing") is None


def test_runtime_contract_registry_verifier_accepts_current_registry() -> None:
    verification = verify_runtime_contract_registry(runtime_contract_registry())

    assert verification.successful() is True
    assert verification.to_dict() == {
        "runtime_contract_verification": {"successful": True, "issue_count": 0},
        "issues": [],
    }


def test_runtime_contract_registry_verifier_reports_mismatches() -> None:
    verification = verify_runtime_contract_registry(
        {
            "runtime_contract_registry": {"version": "old", "contract_count": 1},
            "contracts": [
                {
                    "name": "runtime_result",
                    "version": "v1",
                    "contract_type": "json_document",
                    "required_sections": "runtime_result",
                    "produced_by": "RuntimeEngine",
                    "consumed_by": ["runtime_report"],
                },
                {
                    "name": "runtime_result",
                    "version": "v1",
                    "contract_type": "json_document",
                    "required_sections": ["runtime_result"],
                    "produced_by": "RuntimeEngine",
                    "consumed_by": "runtime_report",
                },
            ],
        }
    )

    assert verification.successful() is False
    assert verification.issues == [
        "Runtime contract registry version must be runtime-contracts/v1.",
        "Runtime contract registry contract_count must match contracts length.",
        "Runtime contract 1 required_sections must be a list.",
        "Runtime contract 2 consumed_by must be a list.",
        "Runtime contract names must be unique.",
    ]
