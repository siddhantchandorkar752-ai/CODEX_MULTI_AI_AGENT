from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QualityScores:
    factuality: float
    coherence: float
    depth: float
    rigor: float
    source_quality: float
    reasoning_quality: float
    citation_accuracy: float

    @property
    def passes_production_gate(self) -> bool:
        return (
            self.factuality >= 0.88
            and self.citation_accuracy >= 0.95
            and self.source_quality >= 0.80
            and self.reasoning_quality >= 0.85
        )
