from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID, uuid4


class MemoryKind(StrEnum):
    WORKING = "working"
    SESSION = "session"
    SEMANTIC = "semantic"
    EPISODIC = "episodic"


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: UUID
    kind: MemoryKind
    tenant_id: UUID
    run_id: UUID | None
    text: str
    metadata: dict[str, str]
    confidence: float


class MemoryStore:
    def __init__(self) -> None:
        self._records: dict[UUID, MemoryRecord] = {}

    async def write(
        self,
        *,
        kind: MemoryKind,
        tenant_id: UUID,
        text: str,
        metadata: dict[str, str],
        confidence: float,
        run_id: UUID | None = None,
    ) -> MemoryRecord:
        record = MemoryRecord(uuid4(), kind, tenant_id, run_id, text, metadata, confidence)
        self._records[record.memory_id] = record
        return record

    async def recall(self, *, tenant_id: UUID, query: str, limit: int = 10) -> list[MemoryRecord]:
        query_terms = set(query.lower().split())
        scoped = [record for record in self._records.values() if record.tenant_id == tenant_id]
        scored = sorted(
            scoped,
            key=lambda record: len(query_terms.intersection(record.text.lower().split())) + record.confidence,
            reverse=True,
        )
        return scored[:limit]
