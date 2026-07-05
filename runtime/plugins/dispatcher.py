from __future__ import annotations

from typing import Any

from runtime.context import RuntimeContext
from runtime.plugins.base import PluginResult
from runtime.plugins.exceptions import PluginDispatchError
from runtime.plugins.registry import PluginRegistry


class PluginDispatcher:
    """Routes scheduled assignments to registered runtime plugins."""

    def __init__(self, registry: PluginRegistry) -> None:
        self.registry = registry

    def dispatch(self, assignment: dict[str, Any], context: RuntimeContext | None = None) -> PluginResult:
        if not isinstance(assignment, dict):
            raise PluginDispatchError("assignment must be a dictionary")
        plugin_name = assignment.get("plugin")
        if not plugin_name:
            raise PluginDispatchError("assignment must include a plugin")
        plugin = self.registry.get(str(plugin_name))
        return plugin.execute(assignment, context)
