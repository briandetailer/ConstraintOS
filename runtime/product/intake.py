from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Mapping

from runtime.research_to_render.models import ConstraintRequest

RESPONSES_ENDPOINT = "https://api.openai.com/v1/responses"

INTAKE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "subject",
        "output_kind",
        "viewpoint",
        "required_visible_features",
        "forbidden_features",
        "visual_output",
        "repeatability_required",
        "authoritative_sources_required",
        "labels_required",
        "novel_view_requested",
        "allow_exploratory_generation",
        "manual_review_required",
        "assumptions",
        "unresolved_questions",
    ],
    "properties": {
        "subject": {"type": "string", "minLength": 1},
        "output_kind": {"type": "string", "minLength": 1},
        "viewpoint": {"type": "string", "minLength": 1},
        "required_visible_features": {
            "type": "array",
            "minItems": 1,
            "items": {"type": "string", "minLength": 1},
        },
        "forbidden_features": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "visual_output": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "illustration_style",
                "composition",
                "palette",
                "background",
                "surface_treatment",
                "label_strategy",
                "output_size",
                "quality",
                "candidate_count",
            ],
            "properties": {
                "illustration_style": {"type": "string", "minLength": 1},
                "composition": {"type": "string", "minLength": 1},
                "palette": {"type": "string", "minLength": 1},
                "background": {"type": "string", "minLength": 1},
                "surface_treatment": {"type": "string", "minLength": 1},
                "label_strategy": {"type": "string", "minLength": 1},
                "output_size": {
                    "type": "string",
                    "enum": ["1024x1024", "1536x1024", "1024x1536", "auto"],
                },
                "quality": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "auto"],
                },
                "candidate_count": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 4,
                },
            },
        },
        "repeatability_required": {"type": "boolean"},
        "authoritative_sources_required": {"type": "boolean"},
        "labels_required": {"type": "boolean"},
        "novel_view_requested": {"type": "boolean"},
        "allow_exploratory_generation": {"type": "boolean"},
        "manual_review_required": {"type": "boolean"},
        "assumptions": {
            "type": "array",
            "items": {"type": "string"},
        },
        "unresolved_questions": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
}


class IntakeError(RuntimeError):
    pass


def _extract_output_text(response_payload: Mapping[str, Any]) -> str:
    for item in response_payload.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                return str(content["text"])
    raise IntakeError("Constraint intake response did not contain structured output text.")


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    raise IntakeError("Expected a string or list of strings in request intake.")


def default_visual_output() -> dict[str, Any]:
    return {
        "illustration_style": (
            "publication-ready technical illustration with controlled linework and precise component separation"
        ),
        "composition": (
            "single complete subject, centered, uncropped, with clean surrounding annotation space"
        ),
        "palette": "neutral technical palette with restrained functional accents",
        "background": "plain white background",
        "surface_treatment": "clean engineered surfaces without decorative texture or sketchiness",
        "label_strategy": (
            "generate no text or callouts in the raster; add deterministic labels after candidate validation"
        ),
        "output_size": "1024x1024",
        "quality": "high",
        "candidate_count": 1,
    }


def normalize_explicit_request(
    job_id: str,
    request_text: str,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    subject = str(payload.get("subject", "")).strip()
    required_features = _string_list(
        payload.get("required_visible_features")
        or payload.get("constraints", {}).get("required_visible_features")
        if isinstance(payload.get("constraints", {}), Mapping)
        else payload.get("required_visible_features")
    )
    if not subject or not required_features:
        raise IntakeError(
            "Explicit intake requires subject and at least one required_visible_feature."
        )
    constraints_payload = payload.get("constraints", {})
    constraints = dict(constraints_payload) if isinstance(constraints_payload, Mapping) else {}
    visual = default_visual_output()
    raw_visual = payload.get("visual_output") or constraints.get("visual_output")
    if isinstance(raw_visual, Mapping):
        visual.update({key: value for key, value in raw_visual.items() if value is not None})
    forbidden = _string_list(
        payload.get("forbidden_features", constraints.get("forbidden_features"))
    )
    normalized = {
        "request_id": job_id,
        "request_text": request_text,
        "subject": subject,
        "output_kind": str(payload.get("output_kind", "technical_illustration")).strip(),
        "viewpoint": str(payload.get("viewpoint", "unspecified")).strip(),
        "constraints": {
            "required_visible_features": required_features,
            "forbidden_features": forbidden,
            "visual_output": visual,
            "repeatability_required": bool(
                payload.get(
                    "repeatability_required",
                    constraints.get("repeatability_required", True),
                )
            ),
            "authoritative_sources_required": bool(
                payload.get(
                    "authoritative_sources_required",
                    constraints.get("authoritative_sources_required", True),
                )
            ),
            "labels_required": bool(
                payload.get("labels_required", constraints.get("labels_required", True))
            ),
            "novel_view_requested": bool(
                payload.get(
                    "novel_view_requested",
                    constraints.get("novel_view_requested", False),
                )
            ),
            "allow_exploratory_generation": bool(
                payload.get(
                    "allow_exploratory_generation",
                    constraints.get("allow_exploratory_generation", False),
                )
            ),
            "manual_review_required": bool(
                payload.get(
                    "manual_review_required",
                    constraints.get("manual_review_required", True),
                )
            ),
        },
        "intake": {
            "provider": "explicit_structured_request",
            "assumptions": _string_list(payload.get("assumptions")),
            "unresolved_questions": _string_list(payload.get("unresolved_questions")),
        },
    }
    ConstraintRequest.from_payload(normalized)
    return normalized


class OpenAIConstraintIntakeProvider:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
        endpoint: str = RESPONSES_ENDPOINT,
        timeout_seconds: int = 180,
    ) -> None:
        self.api_key = (api_key or os.environ.get("OPENAI_API_KEY", "")).strip()
        self.model = (model or os.environ.get("CONSTRAINTOS_INTAKE_MODEL", "gpt-5")).strip()
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds
        self.last_manifest: dict[str, Any] = {}

    def build_prompt(self, request_text: str) -> str:
        return f"""Compile the following natural-language request into an executable ConstraintOS technical-image specification.

USER REQUEST
{request_text}

RULES
- Preserve the user's explicit subject, requested view, visible components, style, composition, palette, and prohibitions.
- Do not research the subject in this step and do not invent factual component details not present in the request.
- Translate explicitly named components into concise required_visible_features.
- When the user asks for a general complete view but names no components, use the subject itself as the minimum required visible feature and record that assumption.
- Use forbidden_features to prevent generic substitution, invented geometry, cropped required features, generated text, and automatic approval when those restrictions are implied by technical publication work.
- Use publication-safe defaults only when the request is silent. Record every default or interpretation in assumptions.
- unresolved_questions should contain only issues that make execution unsafe or materially ambiguous; do not create unnecessary questions.
- labels_required means the final publication image needs labels, even though labels should not be generated inside the raster.
- novel_view_requested is true only when the requested viewpoint is not already available from likely fixed reference imagery or the user explicitly asks for a custom, exploded, sectional, or oblique view.
- manual_review_required must remain true.
- Return structured data only."""

    def build_request_payload(self, request_text: str) -> dict[str, Any]:
        return {
            "model": self.model,
            "store": False,
            "input": self.build_prompt(request_text),
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "constraintos_image_request_intake",
                    "description": "Normalized constraints for a technical image job.",
                    "strict": True,
                    "schema": INTAKE_SCHEMA,
                }
            },
        }

    def compile(self, job_id: str, request_text: str) -> dict[str, Any]:
        if not self.api_key:
            raise IntakeError(
                "Natural-language constraint intake requires OPENAI_API_KEY to be visible to the process."
            )
        payload = self.build_request_payload(request_text)
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:  # noqa: S310
                response_payload = json.loads(response.read().decode("utf-8-sig"))
        except urllib.error.HTTPError as exc:
            _ = exc.read()
            if exc.code == 401:
                message = "OpenAI constraint intake failed with HTTP 401: the API key was rejected."
            elif exc.code == 429:
                message = (
                    "OpenAI constraint intake failed with HTTP 429: rate limit, quota, or billing availability."
                )
            else:
                message = f"OpenAI constraint intake failed with HTTP {exc.code}."
            raise IntakeError(message) from exc
        except urllib.error.URLError as exc:
            raise IntakeError(f"OpenAI constraint intake could not connect: {exc.reason}") from exc

        structured = json.loads(_extract_output_text(response_payload))
        normalized = normalize_explicit_request(job_id, request_text, structured)
        normalized["intake"] = {
            "provider": "openai_responses_structured_intake",
            "model": self.model,
            "response_id": response_payload.get("id"),
            "assumptions": _string_list(structured.get("assumptions")),
            "unresolved_questions": _string_list(structured.get("unresolved_questions")),
            "structured_output_schema": "constraintos_image_request_intake",
        }
        self.last_manifest = dict(normalized["intake"])
        return normalized
