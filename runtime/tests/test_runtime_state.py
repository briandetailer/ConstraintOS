from runtime import RuntimeState


def test_runtime_state_terminal_helper() -> None:
    assert RuntimeState.COMPLETED.terminal() is True
    assert RuntimeState.PARTIAL.terminal() is True
    assert RuntimeState.FAILED.terminal() is True
    assert RuntimeState.CANCELLED.terminal() is True
    assert RuntimeState.SKIPPED.terminal() is True
    assert RuntimeState.RUNNING.terminal() is False


def test_runtime_state_successful_helper() -> None:
    assert RuntimeState.COMPLETED.successful() is True
    assert RuntimeState.PARTIAL.successful() is False
    assert RuntimeState.FAILED.successful() is False
