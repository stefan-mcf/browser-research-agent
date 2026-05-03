from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class EvidenceSnippet(BaseModel):
    text: str
    score: float = Field(ge=0.0, le=1.0)
    matched_terms: list[str]
    source: str | None = None
    context_before: str | None = None
    context_after: str | None = None


class PageError(BaseModel):
    message: str
    kind: str
    recoverable: bool


class PageMetadata(BaseModel):
    url: str
    final_url: str
    title: str | None = None
    description: str | None = None
    canonical_url: str | None = None
    fetched_at: datetime
    status_code: int | None = None
    elapsed_ms: int | None = None
    content_length: int | None = None


class ScoreBreakdown(BaseModel):
    relevance: float = Field(ge=0.0, le=1.0)
    credibility: float = Field(ge=0.0, le=1.0)
    freshness: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    total: float = Field(ge=0.0, le=1.0)
    reasons: list[str]
    relevance_reasons: list[str] = Field(default_factory=list)
    credibility_reasons: list[str] = Field(default_factory=list)
    freshness_reasons: list[str] = Field(default_factory=list)
    weights: dict[str, float] = Field(default_factory=dict)
    details: dict[str, Any] = Field(default_factory=dict)


class PageResearchResult(BaseModel):
    metadata: PageMetadata
    evidence: list[EvidenceSnippet]
    links: list[str]
    scores: ScoreBreakdown
    artifacts: dict[str, Path]
    error: PageError | None = None


class ResearchRun(BaseModel):
    objective: str
    created_at: datetime
    pages: list[PageResearchResult]

    @property
    def ranked_pages(self) -> list[PageResearchResult]:
        return sorted(self.pages, key=lambda page: page.scores.total, reverse=True)

    def to_summary(self) -> dict[str, Any]:
        return {
            "objective": self.objective,
            "created_at": self.created_at.isoformat(),
            "pages": [page.model_dump(mode="json") for page in self.ranked_pages],
        }
