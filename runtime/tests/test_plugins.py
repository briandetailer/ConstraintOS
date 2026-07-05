import pytest

from runtime.context import RuntimeContext
from runtime.plugins import (
    DryRunPlugin,
    EchoPlugin,
    PluginDispatchError,
    PluginDispatcher,
    PluginNotFoundError,
    PluginRegistrationError,
    PluginRegistry,
)


def test_plugin_registry_registers_and_retrieves_plugin() -> None:
    registry = PluginRegistry()
    plugin = EchoPlugin()

    registry.register(plugin)

    assert registry.get("echo") is plugin
    assert registry.names() == ["echo"]
    assert registry.supports("echo", "echo") is True


def test_plugin_registry_rejects_duplicate_plugin_names() -> None:
    registry = PluginRegistry()
    registry.register(EchoPlugin())

    with pytest.raises(PluginRegistrationError, match="Plugin echo is already registered"):
        registry.register(EchoPlugin())


def test_plugin_registry_rejects_unknown_plugin_lookup() -> None:
    with pytest.raises(PluginNotFoundError, match="Plugin missing is not registered"):
        PluginRegistry().get("missing")


def test_plugin_dispatcher_routes_assignment_to_plugin() -> None:
    registry = PluginRegistry()
    registry.register(EchoPlugin())
    dispatcher = PluginDispatcher(registry)

    result = dispatcher.dispatch(
        {"node_id": "NODE-0001", "plugin": "echo", "action": "package"},
        RuntimeContext(variables={"test": True}),
    )

    assert result.status == "complete"
    assert result.outputs == ["echo://NODE-0001"]
    assert result.logs == ["Executed package for NODE-0001."]


def test_plugin_dispatcher_rejects_assignment_without_plugin() -> None:
    dispatcher = PluginDispatcher(PluginRegistry())

    with pytest.raises(PluginDispatchError, match="assignment must include a plugin"):
        dispatcher.dispatch({"node_id": "NODE-0001", "action": "package"})


def test_dry_run_plugin_returns_standard_result() -> None:
    result = DryRunPlugin().execute({"node_id": "NODE-0001", "action": "render"})
    data = result.to_dict()

    assert data["plugin"] == "dry_run"
    assert data["node_id"] == "NODE-0001"
    assert data["status"] == "dry_run_complete"
    assert data["outputs"] == ["dry-run://NODE-0001"]
    assert data["metrics"] == {"side_effects": 0}


def test_echo_plugin_returns_standard_result() -> None:
    result = EchoPlugin().execute({"node_id": "NODE-0002", "action": "compile"})

    assert result.plugin == "echo"
    assert result.node_id == "NODE-0002"
    assert result.action == "compile"
    assert result.status == "complete"
    assert result.outputs == ["echo://NODE-0002"]
