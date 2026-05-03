import re

from browser_research_agent.artifacts import safe_slug
from browser_research_agent.models import (
    PageError,
    PageMetadata,
    PageResearchResult,
    ScoreBreakdown,
)


def test_safe_slug_contains_index_domain_and_hash() -> None:
    slug = safe_slug("https://Example.com/security/compliance?x=1", 3)

    assert slug.startswith("03-example-com-")
    assert re.fullmatch(r"03-example-com-[a-f0-9]{8}", slug)


def test_safe_slug_is_collision_resistant_for_same_domain() -> None:
    first = safe_slug("https://example.com/a", 1)
    second = safe_slug("https://example.com/b", 1)

    assert first != second


def test_failed_page_result_keeps_error_and_empty_artifacts() -> None:
    result = PageResearchResult(
        metadata=PageMetadata(
            url="https://bad.invalid",
            final_url="https://bad.invalid",
            fetched_at="2026-01-01T00:00:00Z",
            elapsed_ms=42,
            content_length=0,
        ),
        evidence=[],
        links=[],
        scores=ScoreBreakdown(relevance=0, credibility=0, freshness=0, total=0, reasons=[]),
        artifacts={},
        error=PageError(message="failed", kind="navigation", recoverable=True),
    )

    dumped = result.model_dump(mode="json")
    assert dumped["metadata"]["elapsed_ms"] == 42
    assert dumped["metadata"]["content_length"] == 0
    assert dumped["error"]["kind"] == "navigation"
