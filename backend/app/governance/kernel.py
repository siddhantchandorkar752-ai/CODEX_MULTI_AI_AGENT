from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from app.schemas.messages import AgentName


class PolicyDecision(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    DEGRADE = "DEGRADE"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class Budget:
    max_input_tokens: int
    max_output_tokens: int
    max_usd: float
    max_wall_seconds: int
    max_recursion_depth: int


@dataclass(frozen=True)
class ToolRequest:
    run_id: UUID
    agent: AgentName
    tool_name: str
    estimated_input_tokens: int = 0
    estimated_output_tokens: int = 0
    estimated_usd: float = 0.0
    recursion_depth: int = 0


class GovernanceKernel:
    """Central policy supervisor for agent execution."""

    def __init__(self, budget: Budget, tool_allowlist: dict[AgentName, set[str]]) -> None:
        self._budget = budget
        self._tool_allowlist = tool_allowlist

    def evaluate_tool_request(self, request: ToolRequest) -> tuple[PolicyDecision, str]:
        allowed_tools = self._tool_allowlist.get(request.agent, set())
        if request.tool_name not in allowed_tools:
            return PolicyDecision.DENY, "tool_not_allowed_for_agent"
        if request.recursion_depth > self._budget.max_recursion_depth:
            return PolicyDecision.ESCALATE, "recursion_depth_exceeded"
        if request.estimated_usd > self._budget.max_usd:
            return PolicyDecision.DEGRADE, "estimated_cost_exceeds_budget"
        if request.estimated_input_tokens > self._budget.max_input_tokens:
            return PolicyDecision.DEGRADE, "input_token_budget_exceeded"
        if request.estimated_output_tokens > self._budget.max_output_tokens:
            return PolicyDecision.DEGRADE, "output_token_budget_exceeded"
        return PolicyDecision.ALLOW, "policy_passed"
