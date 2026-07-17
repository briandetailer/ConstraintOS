import io
import json
import urllib.error
from pathlib import Path

import pytest

from runtime.research_to_render import ConstraintRequest, ResearchToRenderOrchestrator
from runtime.research_to_render.discovery import (
    DiscoveryError,
    OpenAIWebDiscoveryProvider,
)
import runtime.research_to_render.discovery as discovery_module

ROOT = Path(__file__).resolve().parents[1]
REQUEST_PATH = (
    ROOT
    / "config"
    / "research-to-render-examples"
    / "raspberry-pi-5-io-plate-request.json"
)


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def read(self) -> bytes:
        return self.payload


def request_and_plan() -> tuple[ConstraintRequest, object]:
    request = ConstraintRequest.from_payload(
        json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    )
    plan = ResearchToRenderOrchestrator().build_research_plan(request)
    return request, plan


def test_live_discovery_request_uses_web_search_and_strict_structured_output() -> None:
    request, plan = request_and_plan()
    provider = OpenAIWebDiscoveryProvider(api_key="test-key", model="gpt-5")

    payload = provider.build_request_payload(request, plan)

    assert payload["model"] == "gpt-5"
    assert payload["store"] is False
    assert payload["tools"] == [{"type": "web_search"}]
    assert payload["text"]["format"]["type"] == "json_schema"
    assert payload["text"]["format"]["strict"] is True
    schema = payload["text"]["format"]["schema"]
    assert schema["additionalProperties"] is False
    assert schema["properties"]["sources"]["items"]["additionalProperties"] is False
    assert "official_web_3d_geometry" in schema["properties"]["sources"]["items"]["properties"]["source_class"]["enum"]


def test_live_discovery_prompt_preserves_constraints_and_source_limits() -> None:
    request, plan = request_and_plan()
    provider = OpenAIWebDiscoveryProvider(api_key="test-key")

    prompt = provider.build_prompt(request, plan)

    assert "Raspberry Pi 5" in prompt
    assert "40-pin GPIO header" in prompt
    assert "PWM fan connector" in prompt
    assert "Never invent a URL" in prompt
    assert "mechanical drawing" in prompt
    assert "not a component-rich source plate" in prompt
    assert "Return source evidence only" in prompt


def test_live_discovery_parses_structured_web_sources(monkeypatch: pytest.MonkeyPatch) -> None:
    request, plan = request_and_plan()
    provider = OpenAIWebDiscoveryProvider(api_key="test-key", model="gpt-5")
    structured = {
        "sources": [
            {
                "source_id": "rpi5-official-step-live",
                "title": "Official Raspberry Pi 5 STEP",
                "authority": "Raspberry Pi Ltd",
                "url": "https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5",
                "download_url": "https://pip-assets.raspberrypi.com/example.zip",
                "source_class": "official_web_3d_geometry",
                "formats": ["zip", "step"],
                "authoritative": True,
                "supports_features": [
                    "40-pin GPIO header",
                    "PWM fan connector",
                ],
                "evidence_claims": ["official connector geometry"],
                "usage_terms_status": "review_required_before_distribution",
                "discovery_query": "Raspberry Pi 5 official STEP CAD 3D model",
                "source_rationale": "Official product portal design file.",
            }
        ]
    }
    response_payload = {
        "id": "resp_test_123",
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
    captured: dict = {}

    def fake_urlopen(request_object, timeout):
        captured["payload"] = json.loads(request_object.data.decode("utf-8"))
        captured["authorization"] = request_object.headers["Authorization"]
        captured["timeout"] = timeout
        return FakeResponse(response_payload)

    monkeypatch.setattr(discovery_module.urllib.request, "urlopen", fake_urlopen)

    candidates = provider.discover(request, plan)

    assert len(candidates) == 1
    assert candidates[0].source_id == "rpi5-official-step-live"
    assert candidates[0].authoritative is True
    assert candidates[0].source_class == "official_web_3d_geometry"
    assert captured["payload"]["tools"] == [{"type": "web_search"}]
    assert captured["authorization"] == "Bearer test-key"
    assert provider.last_manifest["response_id"] == "resp_test_123"
    assert provider.last_manifest["candidate_count"] == 1


def test_live_discovery_requires_api_key() -> None:
    request, plan = request_and_plan()
    provider = OpenAIWebDiscoveryProvider(api_key="")
    provider.api_key = ""

    with pytest.raises(DiscoveryError, match="OPENAI_API_KEY"):
        provider.discover(request, plan)


def test_live_discovery_discards_provider_error_body(monkeypatch: pytest.MonkeyPatch) -> None:
    request, plan = request_and_plan()
    provider = OpenAIWebDiscoveryProvider(api_key="secret-key")

    def fake_urlopen(request_object, timeout):
        raise urllib.error.HTTPError(
            request_object.full_url,
            401,
            "Unauthorized",
            hdrs=None,
            fp=io.BytesIO(b'{"error":{"message":"secret-key-fragment"}}'),
        )

    monkeypatch.setattr(discovery_module.urllib.request, "urlopen", fake_urlopen)

    with pytest.raises(DiscoveryError) as exc_info:
        provider.discover(request, plan)

    message = str(exc_info.value)
    assert "HTTP 401" in message
    assert "secret-key-fragment" not in message
