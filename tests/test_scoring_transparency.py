from browser_research_agent.extractor import ExtractedPage, extract_evidence
from browser_research_agent.scoring import SCORE_RUBRIC, score_page


def test_score_breakdown_exposes_weights_and_component_details() -> None:
    page = ExtractedPage(
        title="Vendor SOC 2 Security",
        description="Audit reports and compliance evidence",
        canonical_url=None,
        text=(
            "Updated 2026-02-01. Vendor publishes SOC 2 audit reports, security documentation, "
            "privacy terms, contact details, customer references, and compliance policies."
        ),
        links=["https://trust.example.com/report", "https://docs.example.com/security"],
    )
    evidence = extract_evidence("vendor SOC 2 audit report compliance security", page.text)

    score = score_page(
        "https://example.com/security",
        "vendor SOC 2 audit report compliance security",
        page,
        evidence,
    )

    assert score.weights == SCORE_RUBRIC.weights
    assert set(score.details) == {"relevance", "credibility", "freshness", "confidence"}
    assert score.confidence > 0
    assert score.relevance_reasons
    assert score.credibility_reasons
    assert score.freshness_reasons
    assert score.details["relevance"]["matched_terms"]
    assert score.details["credibility"]["https"] is True
    assert score.details["freshness"]["newest_date"] == "2026-02-01"
    expected_total = round(
        score.weights["relevance"] * score.relevance
        + score.weights["credibility"] * score.credibility
        + score.weights["freshness"] * score.freshness,
        4,
    )
    assert score.total == expected_total


def test_score_rubric_documents_client_safe_interpretation() -> None:
    assert "transparent" in SCORE_RUBRIC.description.lower()
    assert SCORE_RUBRIC.interpretation["strong"] > SCORE_RUBRIC.interpretation["review"]
    assert SCORE_RUBRIC.weights == {"relevance": 0.5, "credibility": 0.35, "freshness": 0.15}
