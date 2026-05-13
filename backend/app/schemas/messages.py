from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class AgentName(StrEnum):
    PLANNER = "planner"
    SEARCH = "search"
    READER = "reader"
    MEMORY = "memory"
    WRITER = "writer"
    CRITIC = "critic"
    VERIFICATION = "verification"
    COST = "cost"
    GOVERNANCE = "governance"
    ORCHESTRATOR = "orchestrator"


class EventType(StrEnum):
    TASK_ASSIGNED = "TASK_ASSIGNED"
    TASK_STARTED = "TASK_STARTED"
    TASK_RESULT = "TASK_RESULT"
    TASK_FAILED = "TASK_FAILED"
    CLAIM_EXTRACTED = "CLAIM_EXTRACTED"
    EVIDENCE_VERIFIED = "EVIDENCE_VERIFIED"
    POLICY_DECISION = "POLICY_DECISION"
    POLICY_VIOLATION = "POLICY_VIOLATION"
    COST_RECORDED = "COST_RECORDED"
    MEMORY_READ = "MEMORY_READ"
    MEMORY_WRITE = "MEMORY_WRITE"
    STATE_TRANSITION = "STATE_TRANSITION"


class CostEnvelope(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    usd: float = 0.0
    provider: str | None = None
    model: str | None = None


class ConfidenceEnvelope(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    rationale: str | None = None
    uncertainty: list[str] = Field(default_factory=list)


class AgentMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message_id: UUID = Field(default_factory=uuid4)
    trace_id: UUID
    run_id: UUID
    parent_message_id: UUID | None = None
    event_type: EventType
    sender: AgentName
    recipient: AgentName
    task_id: UUID | None = None
    state: str
    confidence: ConfidenceEnvelope | None = None
    cost: CostEnvelope = Field(default_factory=CostEnvelope)
    memory_refs: list[str] = Field(default_factory=list)
    dependencies: list[UUID] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SourceRecord(BaseModel):
    url: str
    canonical_url: str | None = None
    title: str | None = None
    publisher: str | None = None
    published_at: datetime | None = None
    authority_score: float = Field(default=0.0, ge=0.0, le=1.0)
    freshness_score: float = Field(default=0.0, ge=0.0, le=1.0)
    trust_score: float = Field(default=0.0, ge=0.0, le=1.0)


class ClaimRecord(BaseModel):
    claim_id: UUID = Field(default_factory=uuid4)
    text: str
    source_urls: list[str]
    confidence: ConfidenceEnvelope
    evidence_refs: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
