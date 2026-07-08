from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

DEFAULT_CONTRACTS_DIR = Path("examples") / "graphics" / "contracts"
DEFAULT_SCHEMA_NAME = "graphics_validation_contract.schema.json"
CONTRACT_SUFFIX = ".contract.json"


class GraphicsContractError(ValueError):
    """Raised when a graphics validation contract is invalid or inconsistent."""


def load_json(path: Path | str) -> dict[str, Any]:
    target = Path(path)
    value = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GraphicsContractError(f"Expected JSON object in {target}")
    return value


def validate_contract_schema(contract: dict[str, Any], schema: dict[str, Any]) -> None:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(contract), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.path) or "<root>"
        raise GraphicsContractError(f"Graphics contract schema error at {location}: {first.message}")


def require_same_set(name: str, left: list[str], right: list[str]) -> None:
    left_set = set(left)
    right_set = set(right)
    if left_set != right_set:
        missing = sorted(left_set - right_set)
        unexpected = sorted(right_set - left_set)
        raise GraphicsContractError(f"{name} mismatch; missing={missing}; unexpected={unexpected}")


def discover_project_root(start: Path | None = None) -> Path:
    """Find the repository root for graphics contract discovery."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / DEFAULT_CONTRACTS_DIR / DEFAULT_SCHEMA_NAME).exists():
            return candidate
    return current


def resolve_contracts_dir(project_root: Path, explicit_contracts_dir: str | None = None) -> Path:
    if explicit_contracts_dir:
        contracts_dir = Path(explicit_contracts_dir)
        return contracts_dir if contracts_dir.is_absolute() else project_root / contracts_dir
    return project_root / DEFAULT_CONTRACTS_DIR


def contract_key(path: Path) -> str:
    name = path.name
    if name.endswith(CONTRACT_SUFFIX):
        return name[: -len(CONTRACT_SUFFIX)]
    return path.stem


def iter_contract_paths(contracts_dir: Path) -> list[Path]:
    if not contracts_dir.exists():
        raise GraphicsContractError(f"Graphics contracts directory does not exist: {contracts_dir}")
    return sorted(path for path in contracts_dir.glob(f"*{CONTRACT_SUFFIX}") if path.is_file())


def load_contract_schema(contracts_dir: Path) -> dict[str, Any]:
    return load_json(contracts_dir / DEFAULT_SCHEMA_NAME)


def load_validated_contract(path: Path, schema: dict[str, Any]) -> dict[str, Any]:
    contract = load_json(path)
    validate_contract_schema(contract, schema)
    return contract


def summarize_contract(path: Path, contract: dict[str, Any]) -> dict[str, Any]:
    contract_meta = contract.get("contract", {})
    subject = contract.get("subject", {})
    rendering = contract.get("rendering_requirements", {})
    decision = contract.get("decision_policy", {})
    approval = contract.get("approval_contract", {})
    required_labels = contract.get("required_labels", [])
    forbidden = subject.get("forbidden_substitutions", {}) if isinstance(subject, dict) else []
    return {
        "key": contract_key(path),
        "file": str(path),
        "id": contract_meta.get("id") if isinstance(contract_meta, dict) else None,
        "subject": subject.get("name") if isinstance(subject, dict) else None,
        "category": subject.get("category") if isinstance(subject, dict) else None,
        "mode": contract_meta.get("mode") if isinstance(contract_meta, dict) else None,
        "view": rendering.get("view") if isinstance(rendering, dict) else None,
        "style": rendering.get("style") if isinstance(rendering, dict) else None,
        "allowed_decisions": decision.get("allowed_decisions") if isinstance(decision, dict) else [],
        "expected_initial_decision": approval.get("expected_initial_decision") if isinstance(approval, dict) else None,
        "required_label_count": len(required_labels) if isinstance(required_labels, list) else 0,
        "forbidden_substitution_count": len(forbidden) if isinstance(forbidden, list) else 0,
        "source_use_case": contract_meta.get("source_use_case") if isinstance(contract_meta, dict) else None,
        "guardrail": approval.get("guardrail") if isinstance(approval, dict) else None,
    }


def list_contract_summaries(contracts_dir: Path) -> list[dict[str, Any]]:
    schema = load_contract_schema(contracts_dir)
    summaries: list[dict[str, Any]] = []
    for path in iter_contract_paths(contracts_dir):
        summaries.append(summarize_contract(path, load_validated_contract(path, schema)))
    return summaries


def resolve_contract_path(reference: str, contracts_dir: Path) -> Path:
    candidate = Path(reference)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    if candidate.suffix == ".json":
        relative = contracts_dir / candidate
        if relative.exists():
            return relative
    key = reference[:-len(CONTRACT_SUFFIX)] if reference.endswith(CONTRACT_SUFFIX) else reference
    relative = contracts_dir / f"{key}{CONTRACT_SUFFIX}"
    if relative.exists():
        return relative
    available = ", ".join(contract_key(path) for path in iter_contract_paths(contracts_dir))
    raise GraphicsContractError(f"Unknown graphics contract: {reference}. Available contracts: {available}")


def load_contract_report(reference: str, contracts_dir: Path) -> dict[str, Any]:
    schema = load_contract_schema(contracts_dir)
    path = resolve_contract_path(reference, contracts_dir)
    contract = load_validated_contract(path, schema)
    return {
        "summary": summarize_contract(path, contract),
        "contract": contract,
    }


def validate_perseverance_contract_consistency(
    contract: dict[str, Any],
    spec: dict[str, Any],
    policy: dict[str, Any],
    expected_evidence: dict[str, Any],
    expected_approval: dict[str, Any],
) -> None:
    request = spec.get("graphics_request", {})
    artifact = spec.get("artifact", {})
    if not isinstance(request, dict) or not isinstance(artifact, dict):
        raise GraphicsContractError("Perseverance spec must include artifact and graphics_request objects")

    contract_meta = contract.get("contract", {})
    subject = contract.get("subject", {})
    rendering = contract.get("rendering_requirements", {})
    constraints = contract.get("constraint_groups", {})
    decision_policy = contract.get("decision_policy", {})
    evidence_contract = contract.get("evidence_contract", {})
    approval_contract = contract.get("approval_contract", {})
    policy_header = policy.get("graphics_approval_policy", {})
    decision_rules = policy.get("decision_rules", {})
    evidence_report = expected_evidence.get("graphics_evidence_report", {})
    approval_result = expected_approval.get("graphics_approval_result", {})

    if contract_meta.get("source_artifact_id") != artifact.get("id"):
        raise GraphicsContractError("contract source_artifact_id must match spec artifact id")
    if subject.get("name") != request.get("subject"):
        raise GraphicsContractError("contract subject name must match spec subject")
    for field in ["target_graphic", "view", "style", "label_density", "output_format", "background_policy", "logo_policy"]:
        if rendering.get(field) != request.get(field):
            raise GraphicsContractError(f"rendering requirement mismatch: {field}")

    require_same_set("required_labels", contract.get("required_labels", []), spec.get("required_labels", []))
    require_same_set("forbidden_substitutions", subject.get("forbidden_substitutions", []), spec.get("forbidden_substitutions", []))
    require_same_set("policy required_labels", contract.get("required_labels", []), policy.get("required_labels", []))
    require_same_set("policy forbidden_substitutions", subject.get("forbidden_substitutions", []), policy.get("forbidden_substitutions", []))
    require_same_set("identity_constraints", subject.get("identity_constraints", []), spec.get("subject_identity_constraints", []))
    require_same_set("geometry_constraints", constraints.get("geometry", []), spec.get("geometry_constraints", []))

    if constraints.get("component_location") != spec.get("instrument_constraints"):
        raise GraphicsContractError("component location constraints must match spec instrument constraints")
    if decision_policy.get("allowed_decisions") != policy.get("allowed_decisions"):
        raise GraphicsContractError("allowed decisions must match policy")
    if decision_policy.get("approved_requires") != decision_rules.get("approved", {}).get("requires"):
        raise GraphicsContractError("approved requirements must match policy")
    if decision_policy.get("needs_review_when_any") != decision_rules.get("needs_review", {}).get("when_any"):
        raise GraphicsContractError("needs_review triggers must match policy")
    if decision_policy.get("rejected_when_any") != decision_rules.get("rejected", {}).get("when_any"):
        raise GraphicsContractError("rejection triggers must match policy")
    if decision_policy.get("uncertainty_default") != policy.get("uncertainty_handling", {}).get("default_decision"):
        raise GraphicsContractError("uncertainty default must match policy")

    require_same_set("required_checks", evidence_contract.get("required_checks", []), policy.get("required_checks", []))
    evidence_trace = expected_evidence.get("required_label_trace", {})
    if evidence_contract.get("required_label_trace") != evidence_trace:
        raise GraphicsContractError("required label trace must match expected evidence")
    if contract_meta.get("mode") != policy_header.get("mode") or contract_meta.get("mode") != evidence_report.get("mode") or contract_meta.get("mode") != approval_result.get("mode"):
        raise GraphicsContractError("contract mode must match policy, evidence, and approval fixtures")
    if approval_contract.get("expected_initial_decision") != approval_result.get("decision"):
        raise GraphicsContractError("expected approval decision must match expected approval fixture")
    if approval_contract.get("guardrail") != expected_approval.get("guardrail"):
        raise GraphicsContractError("approval guardrail must match expected approval fixture")
