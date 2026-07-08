import json
from pathlib import Path
from typing import Any

from runtime.engine import RuntimeEngine


ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_DIR = ROOT / "examples" / "graphics" / "perseverance"


REQUIRED_LABELS = {
    "Mastcam-Z",
    "SuperCam",
    "MEDA",
    "MOXIE",
    "PIXL",
    "RIMFAX",
    "SHERLOC",
    "robotic arm",
    "wheels",
    "mast",
    "chassis",
}


FORBIDDEN_SUBSTITUTIONS = {
    "Curiosity rover",
    "Opportunity rover",
    "Spirit rover",
    "generic Mars rover",
    "lunar rover",
    "fictional rover",
    "crewed rover",
    "tank tracks",
    "solar panels",
    "cockpit glass",
    "human seats",
    "animal-like legs",
}


def read_json(name: str) -> dict[str, Any]:
    value = json.loads((EXAMPLE_DIR / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_perseverance_spec_captures_required_graphics_constraints() -> None:
    spec = read_json("spec.json")

    assert spec["artifact"]["id"] == "GRAPHICS-PERSEVERANCE-0001"
    assert spec["graphics_request"]["subject"] == "NASA Perseverance rover"
    assert spec["graphics_request"]["view"] == "front-left three-quarter view"
    assert spec["graphics_request"]["style"] == "clean engineering-manual technical infographic"
    assert set(spec["required_labels"]) == REQUIRED_LABELS
    assert set(spec["forbidden_substitutions"]) == FORBIDDEN_SUBSTITUTIONS
    assert spec["approval_expectations"]["needs_review"] == "required subsystem placement is missing, ambiguous, or uncertain"


def test_perseverance_workers_cover_all_runtime_plugins() -> None:
    spec = read_json("spec.json")
    workers = read_json("workers.json")["workers"]

    planned_plugins = {step["plugin"] for step in spec["execution_steps"]}
    worker_plugins = {plugin for worker in workers for plugin in worker["plugins"] if worker["status"] == "available"}

    assert planned_plugins <= worker_plugins


def test_perseverance_expected_outputs_preserve_needs_review_guardrail() -> None:
    prompt = read_json("expected_prompt.json")
    evidence = read_json("expected_evidence.json")
    approval = read_json("expected_approval.json")

    assert prompt["graphics_prompt_result"]["status"] == "ready_for_candidate_generation"
    assert evidence["graphics_evidence_report"]["status"] == "needs_review"
    assert approval["graphics_approval_result"]["decision"] == "needs_review"
    assert "Uncertainty must produce needs_review, not approval." == approval["guardrail"]
    assert any("RIMFAX" in item for item in approval["needs_review"])
    assert any("MOXIE" in item for item in approval["needs_review"])


def test_perseverance_example_runs_through_current_dry_run_runtime() -> None:
    spec = read_json("spec.json")
    workers = read_json("workers.json")["workers"]

    result = RuntimeEngine().run(spec, workers)
    data = result.to_dict()

    assert data["runtime_result"]["successful"] is True
    assert data["summary"]["plan_nodes"] == 6
    assert data["summary"]["plan_stages"] == 6
    assert data["summary"]["scheduled_assignments"] == 6
    assert data["summary"]["unscheduled_nodes"] == 0
    assert data["summary"]["node_results"] == 6
    assert data["plan"]["execution_plan"]["source_id"] == "GRAPHICS-PERSEVERANCE-0001"
    assert data["schedule"]["schedule_result"]["status"] == "scheduled"
    assert data["execution"]["execution_result"]["status"] == "complete"
