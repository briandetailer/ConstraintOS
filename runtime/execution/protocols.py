from __future__ import annotations

from typing import Any, Protocol

from runtime.context import RuntimeContext
from runtime.execution.models import ExecutionRequest, ExecutionResult


class RuntimeExecutor(Protocol):
    """Common interface for runtime execution backends."""

    def execute(
        self,
        request: ExecutionRequest | dict[str, Any],
        result_id: str = "EXEC-RESULT-0001",
        context: RuntimeContext | None = None,
    ) -> ExecutionResult:
        """Execute a runtime execution request."""
