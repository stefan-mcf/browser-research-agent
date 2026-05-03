from browser_research_agent.extractor import ExtractedPage, extract_evidence
from browser_research_agent.scoring import score_page


def test_score_page_rewards_relevance_and_https() -> None:
    page = ExtractedPage(
        title="SOC 2 Compliance Automation",
        description="Security automation for audit evidence",
        canonical_url=None,
        text=(
            "Updated 2026-01-10. SOC 2 compliance automation gathers audit evidence. "
            "Security documentation, privacy terms, contact, and customers are available."
        ),
        links=["https://docs.example.com", "https://trust.example.com"],
    )
    evidence = extract_evidence("SOC 2 compliance automation evidence", page.text)
    scores = score_page(
        "https://example.com/security", "SOC 2 compliance automation evidence", page, evidence
    )
    assert scores.relevance > 0.5
    assert scores.credibility > 0.3
    assert scores.total > 0.45
    assert scores.reasons


def test_score_page_handles_no_dates() -> None:
    page = ExtractedPage(
        title=None, description=None, canonical_url=None, text="plain page", links=[]
    )
    scores = score_page("http://example.com", "unmatched objective", page, [])
    assert scores.freshness == 0.35
    assert scores.total >= 0
