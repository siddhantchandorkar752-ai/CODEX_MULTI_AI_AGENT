from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalCandidate:
    document_id: str
    chunk_id: str
    text: str
    bm25_score: float
    vector_score: float
    authority_score: float
    freshness_score: float
    source_diversity_bonus: float = 0.0
    duplication_penalty: float = 0.0

    @property
    def hybrid_score(self) -> float:
        return (
            self.bm25_score * 0.20
            + self.vector_score * 0.20
            + self.authority_score * 0.25
            + self.freshness_score * 0.15
            + self.source_diversity_bonus * 0.10
            - self.duplication_penalty
        )


class HybridRetriever:
    def rank(self, candidates: list[RetrievalCandidate], limit: int = 20) -> list[RetrievalCandidate]:
        return sorted(candidates, key=lambda candidate: candidate.hybrid_score, reverse=True)[:limit]
