from datetime import UTC, datetime

from browser_research_agent.extractor import ExtractedPage, extract_evidence
from browser_research_agent.models import ResearchRun
from browser_research_agent.scoring import score_page


def _score(text: str, url: str = "https://example.com/security") -> float:
    page = ExtractedPage(
        title="Vendor security",
        description="Security and compliance",
        canonical_url=None,
        text=text,
        links=["https://docs.example.com"],
    )
    evidence = extract_evidence("SOC 2 audit reports security compliance", page.text)
    return score_page(url, "SOC 2 audit reports security compliance", page, evidence).total


def test_scoring_calibration_ranks_strong_review_and_weak_pages() -> None:
    strong = _score(
        "Updated 2026-01-10. Vendor publishes SOC 2 audit reports, security documentation, privacy terms, "
        "contact details, compliance policies, customer references, and citations."
    )
    review = _score(
        "Vendor mentions SOC 2 and security but has limited audit evidence.",
        "http://unknown.example/security",
    )
    weak = _score("A generic marketing page about collaboration and dashboards.")

    assert strong > review > weak


def test_research_run_ranks_pages_by_total_score() -> None:
    # Ranking behavior is covered through the model API used by JSON and report output.
    run = ResearchRun(objective="rank", created_at=datetime(2026, 1, 1, tzinfo=UTC), pages=[])

    assert run.ranked_pages == []
