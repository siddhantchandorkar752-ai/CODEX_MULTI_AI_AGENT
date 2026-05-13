import pytest

from app.orchestration.state import InvalidStateTransition, RunState, assert_transition


def test_valid_transition() -> None:
    assert_transition(RunState.IDLE, RunState.PLANNING)


def test_invalid_transition() -> None:
    with pytest.raises(InvalidStateTransition):
        assert_transition(RunState.IDLE, RunState.FINALIZING)
