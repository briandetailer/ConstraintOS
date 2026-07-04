from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class RendererProfile:
    name: str
    version: str
    supported_constraint_types: list[str]
    supports_patch: bool = False
    supports_structured_output: bool = False


@dataclass
class RenderRequest:
    renderer: str
    artifact_id: str
    instruction: str
    metadata: dict[str, Any]


@dataclass
class RenderResponse:
    renderer: str
    artifact_id: str
    status: str
    output_reference: str | None
    messages: list[str]
    metadata: dict[str, Any]


class RendererAdapter(Protocol):
    """Boundary protocol for future renderer integrations.

    Phase 5 intentionally defines the interface without calling live renderers.
    Implementations must not mutate specifications or validate their own output.
    """

    profile: RendererProfile

    def prepare(self, instruction: str, artifact_id: str, metadata: dict[str, Any] | None = None) -> RenderRequest:
        """Prepare a renderer request from compiled instructions."""

    def render(self, request: RenderRequest) -> RenderResponse:
        """Execute a render request and return an output reference.

        Live implementations are intentionally deferred.
        """


class DryRunRendererAdapter:
    """A no-op adapter used to test renderer boundaries without live generation."""

    profile = RendererProfile(
        name="dry-run",
        version="0.1",
        supported_constraint_types=["semantic", "visual", "stylistic", "negative"],
        supports_patch=False,
        supports_structured_output=True,
    )

    def prepare(self, instruction: str, artifact_id: str, metadata: dict[str, Any] | None = None) -> RenderRequest:
        return RenderRequest(
            renderer=self.profile.name,
            artifact_id=artifact_id,
            instruction=instruction,
            metadata=metadata or {},
        )

    def render(self, request: RenderRequest) -> RenderResponse:
        return RenderResponse(
            renderer=self.profile.name,
            artifact_id=request.artifact_id,
            status="dry_run",
            output_reference=None,
            messages=["Dry run only. No live renderer was called."],
            metadata={"instruction_length": len(request.instruction)},
        )
