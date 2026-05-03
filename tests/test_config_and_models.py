from pathlib import Path

import pytest
from pydantic import ValidationError

from browser_research_agent.config import ResearchConfig
from browser_research_agent.models import (
    PageError,
    PageMetadata,
    PageResearchResult,
    ScoreBreakdown,
)


def test_research_config_limits_urls_and_normalizes_output_dir() -> None:
    config = ResearchConfig(
        objective="Find SOC 2 automation evidence",
        urls=["https://example.com/1", "https://example.com/2"],
        out_dir=Path("artifacts/test"),
        max_pages=1,
    )

    assert config.urls == ["https://example.com/1"]
    assert config.out_dir == Path("artifacts/test")
    assert config.include_screenshots is True


def test_research_config_requires_objective_and_urls() -> None:
    with pytest.raises(ValidationError):
        ResearchConfig(objective="", urls=["https://example.com"], out_dir=Path("artifacts/test"))

    with pytest.raises(ValidationError):
        ResearchConfig(objective="Research", urls=[], out_dir=Path("artifacts/test"))


def test_page_error_serializes_with_research_result() -> None:
    result = PageResearchResult(
        metadata=PageMetadata(
            url="https://example.com",
            final_url="https://example.com",
            fetched_at="2026-01-01T00:00:00Z",
            status_code=None,
        ),
        evidence=[],
        links=[],
        scores=ScoreBreakdown(relevance=0, credibility=0, freshness=0, total=0, reasons=[]),
        artifacts={},
        error=PageError(message="navigation timed out", kind="timeout", recoverable=True),
    )

    data = result.model_dump(mode="json")
    assert data["error"] == {
        "message": "navigation timed out",
        "kind": "timeout",
        "recoverable": True,
    }
