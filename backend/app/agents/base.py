from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.messages import AgentMessage, AgentName


class AgentExecutionError(RuntimeError):
    pass


class BaseAgent(ABC):
    name: AgentName

    @abstractmethod
    async def handle(self, message: AgentMessage) -> AgentMessage:
        """Process a typed task message and return a typed result event."""
