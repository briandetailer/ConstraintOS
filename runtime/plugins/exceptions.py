from __future__ import annotations


class PluginRuntimeError(ValueError):
    """Base error for runtime plugin operations."""


class PluginRegistrationError(PluginRuntimeError):
    """Raised when a plugin cannot be registered."""


class PluginNotFoundError(PluginRuntimeError):
    """Raised when a requested plugin is not registered."""


class PluginDispatchError(PluginRuntimeError):
    """Raised when an assignment cannot be dispatched to a plugin."""
