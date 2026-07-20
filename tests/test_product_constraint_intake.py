from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from runtime.product import intake


class FakeResponse:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def compiled_intake_payload() -> dict[str, Any]:
    return {
        "subject": "Previously Unknown Hydraulic Test Stand",
        "output_kind": "technical_component_plate",
        "viewpoint": "locked_front_oblique_view",
        "required_visible_features": [
            "hydraulic reservoir",
            "pressure gauge",
            "control valve manifold",
        ],
        "forbidden_features": [
            "invented hoses",
            "generated labels inside the raster",
            "automatic approval",
        ],
        "visual_output": {
            "illustration_style": "publication-ready technical ink illustration",
            "composition": "complete isolated assembly with annotation space",
            "palette": "neutral grayscale with restrained amber fluid-path accents",
            "background": "plain white background",
            "surface_treatment": "precise machined surfaces and controlled line weight",
            "label_strategy": "no generated text; labels added deterministically after review",
            "output_size": "1536x1024",
            "quality": "high",
            "candidate_count": 2,
        },
        "repeatability_required": True,
        "authoritative_sources_required": True,
        "labels_required": True,
        "novel_view_requested": True,
        "allow_exploratory_generation": False,
        "manual_review_required": True,
        "assumptions": ["The assembly should be isolated from its workshop environment."],
        "unresolved_questions": [],
    }


def test_intake_request_uses_strict_structured_output_contract() -> None:
    provider = intake.OpenAIConstraintIntakeProvider(api_key="test-key")

    payload = provider.build_request_payload(
        "Create a technical image of a previously unknown hydraulic test stand."
    )

    assert payload["model"] == "gpt-5"
    assert payload["store"] is False
    assert payload["text"]["format"]["type"] == "json_schema"
    assert payload["text"]["format"]["strict"] is True
    assert payload["text"]["format"]["schema"] == intake.INTAKE_SCHEMA
    prompt = payload["input"]
    assert "do not invent factual component details" in prompt
    assert "required_visible_features" in prompt
    assert "unresolved_questions" in prompt
    assert "manual_review_required must remain true" in prompt


def test_openai_intake_compiles_unknown_request_into_full_request_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    structured = compiled_intake_payload()
    response_payload = {
        "id": "resp_intake_001",
        "output": [
            {
                "type": "message",
                "content": [
                    {
                        "type": "output_text",
                        "text": json.dumps(structured),
                    }
                ],
            }
        ],
    }
    captured: dict[str, Any] = {}

    def fake_urlopen(request: Any, timeout: int) -> FakeResponse:
        captured["request"] = request
        captured["timeout"] = timeout
        return FakeResponse(response_payload)

    monkeypatch.setattr(intake.urllib.request, "urlopen", fake_urlopen)
    provider = intake.OpenAIConstraintIntakeProvider(
        api_key="test-key",
        endpoint="https://example.invalid/v1/responses",
    )

    result = provider.compile(
        "hydraulic-test-job-001",
        "Create a publication-ready technical plate of a hydraulic test stand.",
    )

    assert captured["timeout"] == 180
    assert result["request_id"] == "hydraulic-test-job-001"
    assert result["subject"] == structured["subject"]
    assert result["constraints"]["required_visible_features"] == (
        structured["required_visible_features"]
    )
    assert result["constraints"]["visual_output"] == structured["visual_output"]
    assert result["constraints"]["novel_view_requested"] is True
    assert result["constraints"]["manual_review_required"] is True
    assert result["intake"]["provider"] == "openai_responses_structured_intake"
    assert result["intake"]["response_id"] == "resp_intake_001"
    assert result["intake"]["assumptions"] == structured["assumptions"]
    assert result["intake"]["unresolved_questions"] == []
    assert provider.last_manifest == result["intake"]


def test_explicit_nested_constraint_payload_uses_defaults_without_provider() -> None:
    result = intake.normalize_explicit_request(
        "explicit-job-001",
        "Create a top-view technical plate.",
        {
            "subject": "Unknown Sensor Board",
            "output_kind": "technical_component_plate",
            "viewpoint": "locked_top_view",
            "constraints": {
                "required_visible_features": ["sensor array", "power connector"],
                "forbidden_features": ["invented components"],
                "visual_output": {
                    "background": "transparent background",
                    "candidate_count": 3,
                },
                "labels_required": False,
            },
        },
    )

    constraints = result["constraints"]
    assert constraints["required_visible_features"] == [
        "sensor array",
        "power connector",
    ]
    assert constraints["forbidden_features"] == ["invented components"]
    assert constraints["visual_output"]["background"] == "transparent background"
    assert constraints["visual_output"]["candidate_count"] == 3
    assert constraints["visual_output"]["quality"] == "high"
    assert constraints["labels_required"] is False
    assert result["intake"]["provider"] == "explicit_structured_request"


def test_natural_language_intake_requires_process_credential() -> None:
    provider = intake.OpenAIConstraintIntakeProvider(api_key="")

    with pytest.raises(intake.IntakeError, match="requires OPENAI_API_KEY"):
        provider.compile("job-001", "Create a technical image.")
