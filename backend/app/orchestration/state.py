from __future__ import annotations

from enum import StrEnum
from typing import Final


class RunState(StrEnum):
    IDLE = "IDLE"
    PLANNING = "PLANNING"
    SEARCHING = "SEARCHING"
    READING = "READING"
    RETRIEVING = "RETRIEVING"
    WRITING = "WRITING"
    CRITIQUING = "CRITIQUING"
    VERIFYING = "VERIFYING"
    REVISING = "REVISING"
    FINALIZING = "FINALIZING"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    ESCALATED = "ESCALATED"


ALLOWED_TRANSITIONS: Final[dict[RunState, set[RunState]]] = {
    RunState.IDLE: {RunState.PLANNING},
    RunState.PLANNING: {RunState.SEARCHING, RunState.FAILED},
    RunState.SEARCHING: {RunState.READING, RunState.RETRYING, RunState.FAILED},
    RunState.READING: {RunState.RETRIEVING, RunState.RETRYING, RunState.FAILED},
    RunState.RETRIEVING: {RunState.WRITING, RunState.RETRYING, RunState.FAILED},
    RunState.WRITING: {RunState.CRITIQUING, RunState.RETRYING, RunState.FAILED},
    RunState.CRITIQUING: {RunState.VERIFYING, RunState.REVISING, RunState.ESCALATED, RunState.FAILED},
    RunState.VERIFYING: {RunState.REVISING, RunState.FINALIZING, RunState.ESCALATED, RunState.FAILED},
    RunState.REVISING: {RunState.CRITIQUING, RunState.FAILED},
    RunState.RETRYING: {
        RunState.SEARCHING,
        RunState.READING,
        RunState.RETRIEVING,
        RunState.WRITING,
        RunState.FAILED,
    },
    RunState.ESCALATED: {RunState.FINALIZING, RunState.FAILED},
    RunState.FINALIZING: set(),
    RunState.FAILED: set(),
}


class InvalidStateTransition(ValueError):
    pass


def assert_transition(current: RunState, target: RunState) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise InvalidStateTransition(f"{current} cannot transition to {target}")
