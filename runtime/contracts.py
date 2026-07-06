from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


CONTRACT_REGISTRY_VERSION = "runtime-contracts/v1"
REQUIRED_CONTRACT_FIELDS = (
    "name",
    "version",
    "contract_type",
    "required_sections",
    "produced_by",
    "consumed_by",
)


@dataclass(frozen=True)
class RuntimeContract:
    name: str
    version: str
    contract_type: str
    required_sections: tuple[str, ...]
    produced_by: str
    consumed_by: tuple[str, ...]
    description: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "contract_type": self.contract_type,
            "required_sections": list(self.required_sections),
            "produced_by": self.produced_by,
            "consumed_by": list(self.consumed_by),
            "description": self.description,
        }


@dataclass(frozen=True)
class RuntimeContractVerification:
    issues: list[str] = field(default_factory=list)

    def successful(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_contract_verification": {
                "successful": self.successful(),
                "issue_count": len(self.issues),
            },
            "issues": self.issues,
        }


def runtime_contracts() -> tuple[RuntimeContract, ...]:
    return (
        RuntimeContract(
            name="runtime_result",
            version="v1",
            contract_type="json_document",
            required_sections=("runtime_result", "summary", "events", "messages"),
            produced_by="RuntimeEngine",
            consumed_by=("runtime_report", "traceability_adapter", "evidence_bundle"),
            description="Canonical serialized runtime orchestration result.",
        ),
        RuntimeContract(
            name="runtime_traceability",
            version="v1",
            contract_type="json_document",
            required_sections=("runtime_traceability", "records"),
            produced_by="runtime_result_to_trace",
            consumed_by=("runtime_trace_report", "evidence_bundle", "external_audit_clients"),
            description="Language-neutral trace records derived from a runtime result.",
        ),
        RuntimeContract(
            name="runtime_trace_report",
            version="v1",
            contract_type="artifact_json",
            required_sections=("runtime_traceability", "records"),
            produced_by="RuntimeTraceReportWriter",
            consumed_by=("evidence_bundle", "external_audit_clients"),
            description="Persisted runtime traceability artifact.",
        ),
        RuntimeContract(
            name="runtime_evidence_manifest",
            version="v1",
            contract_type="artifact_json",
            required_sections=("runtime_evidence", "artifacts"),
            produced_by="RuntimeEvidenceBundleWriter",
            consumed_by=("external_audit_clients", "ci_cd", "enterprise_integrations"),
            description="Manifest linking runtime report and trace report artifacts.",
        ),
    )


def runtime_contract_registry() -> dict[str, Any]:
    contracts = [contract.to_dict() for contract in runtime_contracts()]
    return {
        "runtime_contract_registry": {
            "version": CONTRACT_REGISTRY_VERSION,
            "contract_count": len(contracts),
        },
        "contracts": contracts,
    }


def get_runtime_contract(name: str) -> RuntimeContract | None:
    for contract in runtime_contracts():
        if contract.name == name:
            return contract
    return None


def verify_runtime_contract_registry(registry: dict[str, Any]) -> RuntimeContractVerification:
    issues: list[str] = []
    if not isinstance(registry, dict):
        return RuntimeContractVerification(["Runtime contract registry must be a dictionary."])

    header = _dict_value(registry, "runtime_contract_registry")
    contracts = registry.get("contracts", [])
    if header.get("version") != CONTRACT_REGISTRY_VERSION:
        issues.append(f"Runtime contract registry version must be {CONTRACT_REGISTRY_VERSION}.")
    if not isinstance(header.get("contract_count"), int):
        issues.append("Runtime contract registry contract_count must be an integer.")
    elif isinstance(contracts, list) and header.get("contract_count") != len(contracts):
        issues.append("Runtime contract registry contract_count must match contracts length.")
    if not isinstance(contracts, list):
        issues.append("Runtime contract registry contracts must be a list.")
        return RuntimeContractVerification(issues)

    names: list[str] = []
    for index, contract in enumerate(contracts, start=1):
        if not isinstance(contract, dict):
            issues.append(f"Runtime contract {index} must be a dictionary.")
            continue
        for field_name in REQUIRED_CONTRACT_FIELDS:
            if not contract.get(field_name):
                issues.append(f"Runtime contract {index} requires {field_name}.")
        name = str(contract.get("name", ""))
        if name:
            names.append(name)
        if "required_sections" in contract and not isinstance(contract.get("required_sections"), list):
            issues.append(f"Runtime contract {index} required_sections must be a list.")
        if "consumed_by" in contract and not isinstance(contract.get("consumed_by"), list):
            issues.append(f"Runtime contract {index} consumed_by must be a list.")

    if len(names) != len(set(names)):
        issues.append("Runtime contract names must be unique.")

    return RuntimeContractVerification(issues)


def _dict_value(value: dict[str, Any], key: str) -> dict[str, Any]:
    payload = value.get(key, {}) if isinstance(value, dict) else {}
    return payload if isinstance(payload, dict) else {}
