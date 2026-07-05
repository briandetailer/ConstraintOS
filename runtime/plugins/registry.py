from __future__ import annotations

from runtime.plugins.base import RuntimePlugin
from runtime.plugins.exceptions import PluginNotFoundError, PluginRegistrationError


class PluginRegistry:
    """In-memory registry for runtime plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, RuntimePlugin] = {}

    def register(self, plugin: RuntimePlugin) -> None:
        name = getattr(plugin, "name", "")
        if not name:
            raise PluginRegistrationError("Plugin must define a name")
        if name in self._plugins:
            raise PluginRegistrationError(f"Plugin {name} is already registered")
        self._plugins[name] = plugin

    def get(self, name: str) -> RuntimePlugin:
        try:
            return self._plugins[name]
        except KeyError as error:
            raise PluginNotFoundError(f"Plugin {name} is not registered") from error

    def names(self) -> list[str]:
        return sorted(self._plugins)

    def supports(self, name: str, capability: str) -> bool:
        plugin = self.get(name)
        return capability in plugin.capabilities
