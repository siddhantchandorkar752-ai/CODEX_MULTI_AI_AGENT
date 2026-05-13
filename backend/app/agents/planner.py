from __future__ import annotations

from uuid import uuid4

from app.agents.base import BaseAgent
from app.schemas.messages import AgentMessage, AgentName, ConfidenceEnvelope, EventType


class PlannerAgent(BaseAgent):
    name = AgentName.PLANNER

    async def handle(self, message: AgentMessage) -> AgentMessage:
        objective = str(message.payload.get("objective", "")).strip()
        if not objective:
            confidence = ConfidenceEnvelope(score=0.0, uncertainty=["missing_objective"])
            payload = {"error": "objective is required"}
            event_type = EventType.TASK_FAILED
        else:
            confidence = ConfidenceEnvelope(score=0.78, rationale="initial deterministic decomposition")
            payload = {
                "dag": [
                    {"task_id": str(uuid4()), "agent": "search", "depends_on": [], "goal": "discover sources"},
                    {"task_id": str(uuid4()), "agent": "reader", "depends_on": ["search"], "goal": "extract claims"},
                    {"task_id": str(uuid4()), "agent": "writer", "depends_on": ["reader"], "goal": "draft report"},
                    {"task_id": str(uuid4()), "agent": "critic", "depends_on": ["writer"], "goal": "critique report"},
                    {"task_id": str(uuid4()), "agent": "verification", "depends_on": ["critic"], "goal": "verify claims"},
                ],
                "budgets": {"max_usd": 5.0, "max_wall_seconds": 900, "max_recursion_depth": 3},
            }
            event_type = EventType.TASK_RESULT
        return AgentMessage(
            trace_id=message.trace_id,
            run_id=message.run_id,
            parent_message_id=message.message_id,
            event_type=event_type,
            sender=self.name,
            recipient=AgentName.ORCHESTRATOR,
            task_id=message.task_id,
            state="PLANNING",
            confidence=confidence,
            payload=payload,
        )
