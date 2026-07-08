from __future__ import annotations

from pathlib import Path
from typing import Any

from constraintos.runtime_cli import attach_traceability, plan_runtime
from runtime import ArtifactStore, RuntimeContext, RuntimeEngine

GRAPHICS_RUNTIME_PLUGINS = {
    "reference_collector": "GRAPHICS-WORKER-REFERENCE-0001",
    "constraint_builder": "GRAPHICS-WORKER-CONSTRAINTS-0001",
    "image_prompt_generator": "GRAPHICS-WORKER-PROMPT-0001",
    "image_evaluator": "GRAPHICS-WORKER-EVALUATOR-0001",
    "evidence_manifest_generator": "GRAPHICS-WORKER-EVIDENCE-0001",
    "approval_reviewer": "GRAPHICS-WORKER-APPROVAL-0001",
}


def _contract_meta(contract: dict[str, Any]) -> dict[str, Any]:
    value = contract.get("contract", {})
    return value if isinstance(value, dict) else {}


def _subject(contract: dict[str, Any]) -> dict[str, Any]:
    value = contract.get("subject", {})
    return value if isinstance(value, dict) else {}


def _rendering(contract: dict[str, Any]) -> dict[str, Any]:
    value = contract.get("rendering_requirements", {})
    return value if isinstance(value, dict) else {}


def _constraints(contract: dict[str, Any]) -> dict[str, Any]:
    value = contract.get("constraint_groups", {})
    return value if isinstance(value, dict) else {}


def _decision_policy(contract: dict[str, Any]) -> dict[str, Any]:
    value = contract.get("decision_policy", {})
    return value if isinstance(value, dict) else {}


def _approval_contract(contract: dict[str, Any]) -> dict[str, Any]:
    value = contract.get("approval_contract", {})
    return value if isinstance(value, dict) else {}


def build_runtime_spec_from_contract(contract: dict[str, Any], contract_key: str) -> dict[str, Any]:
    """Create a runtime-ready graphics validation spec from a reusable contract."""
    meta = _contract_meta(contract)
    subject = _subject(contract)
    rendering = _rendering(contract)
    constraints = _constraints(contract)
    decision = _decision_policy(contract)
    approval = _approval_contract(contract)
    contract_id = str(meta.get("id", f"GRAPHICS-CONTRACT-{contract_key.upper()}"))
    source_artifact_id = str(meta.get("source_artifact_id", contract_id))
    subject_name = str(subject.get("name", contract_key))
    required_labels = contract.get("required_labels", []) if isinstance(contract.get("required_labels"), list) else []

    return {
        "artifact": {
            "id": f"{source_artifact_id}-RUNTIME",
            "title": f"{subject_name} Runtime Bridge",
            "domain": "graphics_validation",
            "source_contract_id": contract_id,
            "source_contract_key": contract_key,
            "use_case": meta.get("source_use_case"),
        },
        "graphics_request": {
            "subject": subject_name,
            "target_graphic": rendering.get("target_graphic"),
            "view": rendering.get("view"),
            "style": rendering.get("style"),
            "label_density": rendering.get("label_density"),
            "output_format": rendering.get("output_format"),
            "background_policy": rendering.get("background_policy"),
            "logo_policy": rendering.get("logo_policy"),
        },
        "required_labels": required_labels,
        "subject_identity_constraints": subject.get("identity_constraints", []),
        "geometry_constraints": constraints.get("geometry", []),
        "component_location_constraints": constraints.get("component_location", {}),
        "forbidden_substitutions": subject.get("forbidden_substitutions", []),
        "approval_expectations": {
            "allowed_decisions": decision.get("allowed_decisions", ["approved", "needs_review", "rejected"]),
            "expected_initial_decision": approval.get("expected_initial_decision", "needs_review"),
            "uncertainty_default": decision.get("uncertainty_default", "needs_review"),
            "guardrail": approval.get("guardrail", "Uncertainty must produce needs_review, not approval."),
        },
        "execution_steps": [
            {
                "id": "NODE-0001",
                "plugin": "reference_collector",
                "action": "collect_contract_reference_requirements",
                "inputs": {
                    "subject": subject_name,
                    "source_contract_id": contract_id,
                    "source_use_case": meta.get("source_use_case"),
                    "reference_scope": ["subject identity", "geometry", "component placement", "label vocabulary"],
                },
                "outputs": ["reference_requirements"],
            },
            {
                "id": "NODE-0002",
                "plugin": "constraint_builder",
                "action": "build_contract_graphics_constraints",
                "depends_on": ["NODE-0001"],
                "inputs": {
                    "constraint_groups": ["subject_identity", "geometry", "component_location", "style", "forbidden_substitutions"],
                    "required_label_count": len(required_labels),
                },
                "outputs": ["constraint_checklist"],
            },
            {
                "id": "NODE-0003",
                "plugin": "image_prompt_generator",
                "action": "generate_contract_constrained_prompt",
                "depends_on": ["NODE-0002"],
                "inputs": {
                    "prompt_target": rendering.get("target_graphic"),
                    "view": rendering.get("view"),
                    "style": rendering.get("style"),
                    "negative_prompt_source": "forbidden_substitutions",
                },
                "outputs": ["final_prompt", "negative_prompt"],
            },
            {
                "id": "NODE-0004",
                "plugin": "image_evaluator",
                "action": "evaluate_contract_candidate_against_constraints",
                "depends_on": ["NODE-0003"],
                "inputs": {
                    "candidate_image": f"placeholder://graphics/contracts/{contract_key}/candidate-0001.png",
                    "evaluation_mode": meta.get("mode", "fixture_only_no_image_generation"),
                },
                "outputs": ["constraint_evaluation"],
            },
            {
                "id": "NODE-0005",
                "plugin": "evidence_manifest_generator",
                "action": "build_contract_graphics_evidence_report",
                "depends_on": ["NODE-0004"],
                "inputs": {
                    "evidence_required": True,
                    "trace_required_labels": True,
                },
                "outputs": ["graphics_evidence_report"],
            },
            {
                "id": "NODE-0006",
                "plugin": "approval_reviewer",
                "action": "review_contract_graphics_approval_result",
                "depends_on": ["NODE-0005"],
                "inputs": {
                    "allowed_decisions": decision.get("allowed_decisions", ["approved", "needs_review", "rejected"]),
                    "uncertainty_decision": decision.get("uncertainty_default", "needs_review"),
                    "expected_initial_decision": approval.get("expected_initial_decision", "needs_review"),
                },
                "outputs": ["approval_result"],
            },
        ],
    }


def build_runtime_workers_for_contract() -> list[dict[str, Any]]:
    return [
        {"worker_id": worker_id, "plugins": [plugin], "status": "available"}
        for plugin, worker_id in GRAPHICS_RUNTIME_PLUGINS.items()
    ]


def build_contract_runtime_metadata(contract_key: str, contract: dict[str, Any], runtime_spec: dict[str, Any]) -> dict[str, Any]:
    meta = _contract_meta(contract)
    subject = _subject(contract)
    rendering = _rendering(contract)
    approval = _approval_contract(contract)
    artifact = runtime_spec.get("artifact", {})
    return {
        "contract_key": contract_key,
        "contract_id": meta.get("id"),
        "runtime_artifact_id": artifact.get("id") if isinstance(artifact, dict) else None,
        "subject": subject.get("name"),
        "view": rendering.get("view"),
        "style": rendering.get("style"),
        "mode": meta.get("mode", "fixture_only_no_image_generation"),
        "expected_decision": approval.get("expected_initial_decision", "needs_review"),
        "required_label_count": len(contract.get("required_labels", [])) if isinstance(contract.get("required_labels"), list) else 0,
        "source_use_case": meta.get("source_use_case"),
        "image_generation": "not_run",
    }


def build_contract_runtime_payload(
    contract_key: str,
    contract: dict[str, Any],
    *,
    plan_only: bool = False,
    artifact_root: str | Path = ".constraintos/runtime/artifacts/graphics/contracts",
    workspace: str | Path = ".",
    runtime_id: str | None = None,
) -> tuple[int, dict[str, Any]]:
    runtime_spec = build_runtime_spec_from_contract(contract, contract_key)
    workers = build_runtime_workers_for_contract()
    runtime_id = runtime_id or f"GRAPHICS-CONTRACT-{contract_key.upper()}-RUNTIME-0001"
    if plan_only:
        payload = plan_runtime(runtime_spec, workers)
        exit_code = 0 if not payload["schedule"].get("unscheduled_nodes") else 1
    else:
        result = RuntimeEngine(artifact_store=ArtifactStore(Path(artifact_root))).run(
            runtime_spec,
            workers,
            RuntimeContext(
                workspace=Path(workspace),
                variables={
                    "graphics_contract": contract_key,
                    "source_contract_id": str(_contract_meta(contract).get("id", "unknown")),
                },
            ),
            runtime_id=runtime_id,
        )
        payload = attach_traceability(result.to_dict(), runtime_spec)
        exit_code = 0 if result.success else 1
    payload["graphics_contract_runtime"] = build_contract_runtime_metadata(contract_key, contract, runtime_spec)
    payload["generated_runtime_spec"] = runtime_spec
    payload["generated_workers"] = workers
    return exit_code, payload
