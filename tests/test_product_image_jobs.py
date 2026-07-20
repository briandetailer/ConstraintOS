from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from runtime.product import api as product_api
from runtime.product.intake import normalize_explicit_request
from runtime.product.service import ConstraintOSProductService, ProductServiceError
from runtime.product.store import FileJobStore
from runtime.research_to_render.models import SourceCandidate

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
START_SCRIPT = ROOT / "scripts" / "start-constraintos-product.ps1"


def explicit_payload() -> dict[str, Any]:
    return {
        "request_text": (
            "Create a publication-ready orthographic technical illustration of a fictionalized "
            "test fixture, showing connector alpha and connector beta without labels in the raster."
        ),
        "title": "Unknown-subject product test",
        "subject": "Example Test Fixture X1",
        "output_kind": "technical_component_plate",
        "viewpoint": "locked_top_view",
        "required_visible_features": ["connector alpha", "connector beta"],
        "forbidden_features": ["invented connectors", "generated text"],
        "visual_output": {
            "illustration_style": "publication-ready technical line illustration",
            "palette": "neutral grayscale with restrained blue accents",
        },
    }


def official_sources(*, cover_beta: bool = True) -> tuple[SourceCandidate, ...]:
    visual_features = ["connector alpha"]
    if cover_beta:
        visual_features.append("connector beta")
    return (
        SourceCandidate.from_payload(
            {
                "source_id": "official-x1-top-view",
                "title": "Example Test Fixture X1 official top view",
                "authority": "Example Manufacturer",
                "url": "https://example.invalid/x1/top-view",
                "download_url": "https://example.invalid/x1/top-view.png",
                "source_class": "official_web_2d_source_plate",
                "formats": ["png"],
                "authoritative": True,
                "supports_features": visual_features,
                "evidence_claims": ["official subject identity and component layout"],
                "usage_terms_status": "review_required_before_distribution",
            }
        ),
        SourceCandidate.from_payload(
            {
                "source_id": "official-x1-documentation",
                "title": "Example Test Fixture X1 documentation",
                "authority": "Example Manufacturer",
                "url": "https://example.invalid/x1/docs",
                "download_url": "",
                "source_class": "official_web_product_documentation",
                "formats": ["html"],
                "authoritative": True,
                "supports_features": ["connector alpha", "connector beta"],
                "evidence_claims": ["official component terminology"],
                "usage_terms_status": "review_required_before_distribution",
            }
        ),
    )


class FakeIntakeProvider:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def compile(self, job_id: str, request_text: str) -> dict[str, Any]:
        self.calls.append((job_id, request_text))
        return normalize_explicit_request(
            job_id,
            request_text,
            {
                "subject": "Novel Subject Never Previously Registered",
                "output_kind": "technical_illustration",
                "viewpoint": "locked_side_view",
                "required_visible_features": ["primary housing", "service connector"],
                "forbidden_features": ["invented geometry"],
                "assumptions": ["Use the standard publication-safe background."],
            },
        )


class FakeDiscoveryProvider:
    def __init__(self, sources: tuple[SourceCandidate, ...]) -> None:
        self.sources = sources
        self.last_manifest = {
            "provider": "fake_live_discovery",
            "response_id": "discovery-test-001",
            "candidate_count": len(sources),
        }

    def discover(self, _request: Any, _plan: Any) -> tuple[SourceCandidate, ...]:
        return self.sources


def test_file_job_store_persists_job_and_event_history(tmp_path: Path) -> None:
    store = FileJobStore(tmp_path / "jobs")
    job = store.create(request_text="Create a technical illustration.", title="Test job")
    store.append_event(
        job.job_id,
        stage="test_stage",
        event_type="test_event",
        message="A durable test event.",
        data={"value": 1},
    )
    updated = store.update(job.job_id, status="constraints_ready", subject="Test Subject")

    reloaded = FileJobStore(tmp_path / "jobs").load(job.job_id)
    events = store.read_events(job.job_id)

    assert reloaded == updated
    assert reloaded.subject == "Test Subject"
    assert reloaded.workspace == str((tmp_path / "jobs" / job.job_id).resolve())
    assert [event.event_type for event in events] == ["job_created", "test_event"]
    assert json.loads((tmp_path / "jobs" / job.job_id / "job.json").read_text())[
        "approval_allowed"
    ] is False


def test_structured_unknown_subject_creates_research_ready_product_job(tmp_path: Path) -> None:
    service = ConstraintOSProductService(FileJobStore(tmp_path / "jobs"))

    job = service.create_job(explicit_payload())
    detail = service.get_job(job.job_id, include_events=True)

    assert job.status == "research_ready"
    assert job.current_stage == "source_discovery"
    assert job.subject == "Example Test Fixture X1"
    assert set(job.artifacts) == {
        "submitted_request",
        "normalized_request",
        "research_plan",
    }
    request = json.loads(Path(job.artifacts["normalized_request"]).read_text())
    assert request["request_id"] == job.job_id
    assert request["constraints"]["required_visible_features"] == [
        "connector alpha",
        "connector beta",
    ]
    assert request["constraints"]["visual_output"]["palette"] == (
        "neutral grayscale with restrained blue accents"
    )
    assert any(event["event_type"] == "stage_completed" for event in detail["events"])


def test_natural_language_intake_is_compiled_without_a_registered_scenario(tmp_path: Path) -> None:
    intake = FakeIntakeProvider()
    service = ConstraintOSProductService(
        FileJobStore(tmp_path / "jobs"),
        intake_provider=intake,
    )

    job = service.create_job(
        {"request_text": "Draw a side-view technical image of a completely new device."}
    )

    assert job.status == "research_ready"
    assert job.subject == "Novel Subject Never Previously Registered"
    assert len(intake.calls) == 1
    normalized = json.loads(Path(job.artifacts["normalized_request"]).read_text())
    assert normalized["request_id"] == job.job_id
    assert normalized["intake"]["provider"] == "explicit_structured_request"
    assert normalized["constraints"]["required_visible_features"] == [
        "primary housing",
        "service connector",
    ]


def test_live_research_selects_reference_conditioned_generation_for_unknown_subject(
    tmp_path: Path,
) -> None:
    provider = FakeDiscoveryProvider(official_sources())
    service = ConstraintOSProductService(
        FileJobStore(tmp_path / "jobs"),
        discovery_provider_factory=lambda: provider,
    )
    job = service.create_job(explicit_payload())

    researched = service.run_research(job.job_id)
    orchestration = json.loads(Path(researched.artifacts["orchestration"]).read_text())

    assert researched.status == "reference_preparation_required"
    assert researched.current_stage == "reference_preparation"
    assert orchestration["render_plan"]["production_mode"] == (
        "reference_conditioned_generation"
    )
    assert orchestration["render_plan"]["canonical_source_ids"] == [
        "official-x1-top-view"
    ]
    assert orchestration["discovery"]["provider"] == "fake_live_discovery"
    assert "source_plate_not_materialized_or_digest_verified" in researched.blockers
    assert researched.approval_allowed is False


def test_research_blocks_when_required_feature_has_no_authoritative_evidence(
    tmp_path: Path,
) -> None:
    provider = FakeDiscoveryProvider(official_sources(cover_beta=False)[:1])
    service = ConstraintOSProductService(
        FileJobStore(tmp_path / "jobs"),
        discovery_provider_factory=lambda: provider,
    )
    job = service.create_job(explicit_payload())

    researched = service.run_research(job.job_id)

    assert researched.status == "blocked"
    assert "unsupported_feature:connector beta" in researched.blockers
    assert researched.production_ready is False
    assert researched.approval_allowed is False


def test_service_records_research_failure_and_event(tmp_path: Path) -> None:
    class FailingDiscovery:
        last_manifest: dict[str, Any] = {}

        def discover(self, _request: Any, _plan: Any) -> tuple[SourceCandidate, ...]:
            raise RuntimeError("simulated discovery failure")

    service = ConstraintOSProductService(
        FileJobStore(tmp_path / "jobs"),
        discovery_provider_factory=FailingDiscovery,
    )
    job = service.create_job(explicit_payload())

    with pytest.raises(ProductServiceError, match="simulated discovery failure"):
        service.run_research(job.job_id)

    failed = service.get_job(job.job_id, include_events=True)
    assert failed["status"] == "research_failed"
    assert failed["error"] == "simulated discovery failure"
    assert failed["events"][-1]["event_type"] == "stage_failed"


def test_product_api_creates_and_reads_structured_job(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("CONSTRAINTOS_JOB_ROOT", str(tmp_path / "api-jobs"))
    body = product_api.CreateJobBody(**explicit_payload())

    created = product_api.create_job(body)
    loaded = product_api.get_job(created["job_id"], include_events=True)
    listing = product_api.list_jobs(limit=20)

    assert created["status"] == "research_ready"
    assert loaded["job_id"] == created["job_id"]
    assert loaded["subject"] == "Example Test Fixture X1"
    assert listing[0]["job_id"] == created["job_id"]
    assert product_api.health()["job_root"] == str((tmp_path / "api-jobs").resolve())


def test_product_cli_and_windows_launcher_are_registered() -> None:
    pyproject = PYPROJECT.read_text(encoding="utf-8")
    launcher = START_SCRIPT.read_text(encoding="utf-8")

    assert 'cos-image-job = "runtime.product.cli:main"' in pyproject
    assert '"uvicorn>=0.30"' in pyproject
    assert "runtime.product.api:app" in launcher
    assert r"runs\product-jobs" in launcher
    assert "Ensure-ConstraintOSOpenAIKey" in launcher
    assert "CONSTRAINTOS_JOB_ROOT" in launcher
    assert "Start-Process $Url" in launcher
