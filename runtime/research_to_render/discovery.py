from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

from .models import ConstraintRequest, ResearchPlan, SourceCandidate

RESPONSES_ENDPOINT = "https://api.openai.com/v1/responses"
ALLOWED_SOURCE_CLASSES = [
    "official_web_3d_geometry",
    "official_web_2d_source_plate",
    "official_web_mechanical_drawing",
    "official_web_technical_documentation",
    "official_web_product_documentation",
    "official_web_component_documentation",
    "verified_secondary_source",
]

DISCOVERY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["sources"],
    "properties": {
        "sources": {
            "type": "array",
            "maxItems": 10,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "source_id",
                    "title",
                    "authority",
                    "url",
                    "download_url",
                    "source_class",
                    "formats",
                    "authoritative",
                    "supports_features",
                    "evidence_claims",
                    "usage_terms_status",
                    "discovery_query",
                    "source_rationale",
                ],
                "properties": {
                    "source_id": {"type": "string"},
                    "title": {"type": "string"},
                    "authority": {"type": "string"},
                    "url": {"type": "string"},
                    "download_url": {"type": "string"},
                    "source_class": {
                        "type": "string",
                        "enum": ALLOWED_SOURCE_CLASSES,
                    },
                    "formats": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "authoritative": {"type": "boolean"},
                    "supports_features": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "evidence_claims": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "usage_terms_status": {
                        "type": "string",
                        "enum": [
                            "review_required_before_distribution",
                            "public_reference_only",
                        ],
                    },
                    "discovery_query": {"type": "string"},
                    "source_rationale": {"type": "string"},
                },
            },
        }
    },
}


class DiscoveryError(RuntimeError):
    pass


def _extract_output_text(response_payload: dict[str, Any]) -> str:
    for item in response_payload.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                return str(content["text"])
    raise DiscoveryError("The web-discovery response did not contain structured output text.")


def _http_error_message(exc: urllib.error.HTTPError) -> str:
    _ = exc.read()
    if exc.code == 401:
        return "OpenAI web discovery failed with HTTP 401: the API key was rejected."
    if exc.code == 429:
        return "OpenAI web discovery failed with HTTP 429: rate limit, quota, or billing availability."
    return f"OpenAI web discovery failed with HTTP {exc.code}."


class OpenAIWebDiscoveryProvider:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        endpoint: str = RESPONSES_ENDPOINT,
        timeout_seconds: int = 180,
    ) -> None:
        self.api_key = (api_key or os.environ.get("OPENAI_API_KEY", "")).strip()
        self.model = (model or os.environ.get("CONSTRAINTOS_RESEARCH_MODEL", "gpt-5")).strip()
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds
        self.last_manifest: dict[str, Any] = {}

    def _require_api_key(self) -> str:
        if not self.api_key:
            raise DiscoveryError(
                "Live web discovery requires OPENAI_API_KEY to be visible to the process."
            )
        return self.api_key

    def build_prompt(
        self,
        request: ConstraintRequest,
        research_plan: ResearchPlan,
    ) -> str:
        required_features = "\n".join(
            f"- {feature}" for feature in request.required_visible_features
        )
        queries = "\n".join(f"- {query}" for query in research_plan.queries)
        return f"""Find authoritative web reference material for a ConstraintOS technical-imagery request.

Subject: {request.subject}
Requested output: {request.output_kind}
Viewpoint: {request.viewpoint}

Required visible features:
{required_features}

Planned searches:
{queries}

Rules:
- Prefer the manufacturer, owner, mission, standards body, or official product portal.
- Search for usable visual evidence, downloadable geometry, mechanical drawings, product documentation, and component documentation.
- Only return URLs that the web-search tool found or opened. Never invent a URL.
- Mark authoritative=true only for an official source controlled by the subject owner or manufacturer.
- In supports_features, copy only exact feature strings from the required-visible-features list and include a feature only when the source supports it.
- A mechanical drawing that warns components are omitted is supporting dimensional evidence, not a component-rich source plate.
- Use an empty string when no direct download URL is available.
- Do not generate or propose imagery. Return source evidence only.
"""

    def build_request_payload(
        self,
        request: ConstraintRequest,
        research_plan: ResearchPlan,
    ) -> dict[str, Any]:
        return {
            "model": self.model,
            "store": False,
            "tools": [{"type": "web_search"}],
            "input": self.build_prompt(request, research_plan),
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "constraintos_web_source_discovery",
                    "description": "Authoritative web sources for source-backed technical imagery.",
                    "strict": True,
                    "schema": DISCOVERY_SCHEMA,
                }
            },
        }

    def discover(
        self,
        request: ConstraintRequest,
        research_plan: ResearchPlan,
    ) -> tuple[SourceCandidate, ...]:
        api_key = self._require_api_key()
        payload = self.build_request_payload(request, research_plan)
        http_request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(  # noqa: S310 - fixed provider endpoint by default
                http_request,
                timeout=self.timeout_seconds,
            ) as response:
                response_payload = json.loads(response.read().decode("utf-8-sig"))
        except urllib.error.HTTPError as exc:
            raise DiscoveryError(_http_error_message(exc)) from exc
        except urllib.error.URLError as exc:
            raise DiscoveryError(f"OpenAI web discovery could not connect: {exc.reason}") from exc

        structured = json.loads(_extract_output_text(response_payload))
        raw_sources = structured.get("sources", [])
        if not isinstance(raw_sources, list):
            raise DiscoveryError("Structured web discovery output did not contain a source list.")
        candidates = tuple(SourceCandidate.from_payload(item) for item in raw_sources)
        self.last_manifest = {
            "provider": "openai_responses_web_search",
            "endpoint": self.endpoint,
            "model": self.model,
            "response_id": response_payload.get("id"),
            "queries": list(research_plan.queries),
            "candidate_count": len(candidates),
            "structured_output_schema": "constraintos_web_source_discovery",
        }
        return candidates
