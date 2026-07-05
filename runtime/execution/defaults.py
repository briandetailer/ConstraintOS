from __future__ import annotations

from runtime.execution.plugin_executor import PluginExecutor
from runtime.plugins import DryRunPlugin, EchoPlugin, PluginDispatcher, PluginRegistry


def create_default_plugin_registry() -> PluginRegistry:
    """Create the built-in plugin registry for local runtime execution."""
    registry = PluginRegistry()
    registry.register(EchoPlugin())
    registry.register(DryRunPlugin())
    return registry


def create_default_plugin_executor() -> PluginExecutor:
    """Create a plugin executor wired to the built-in plugin registry."""
    return PluginExecutor(PluginDispatcher(create_default_plugin_registry()))
