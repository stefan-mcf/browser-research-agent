from pathlib import Path

from browser_research_agent.extractor import extract_evidence, extract_page, normalize_terms


HTML = (Path(__file__).parent / "fixtures" / "vendor_security.html").read_text(encoding="utf-8")


def test_extract_page_includes_structured_sections_and_absolute_links() -> None:
    page = extract_page(HTML, "https://example.com/vendor")

    assert page.title == "Acme TrustHub Security and Compliance"
    assert page.description == "SOC 2, ISO 27001, vendor risk, and audit reporting evidence for enterprise buyers."
    assert page.canonical_url == "https://example.com/security"
    assert "Security and Compliance" in page.headings
    assert "https://example.com/trust" in page.links
    assert "Pricing Blog Careers" not in page.text


def test_normalize_terms_removes_duplicates_and_stems_simple_plurals() -> None:
    terms = normalize_terms("Find audit reports, auditing controls, and reports for vendors")

    assert terms == ["audit", "report", "control", "vendor"]


def test_evidence_prefers_dense_objective_matches_with_context_and_dedupes() -> None:
    page = extract_page(HTML, "https://example.com/vendor")
    evidence = extract_evidence("SOC 2 audit reports vendor risk compliance", page.text, limit=3)

    assert evidence[0].score > 0.65
    assert {"audit", "report", "vendor", "risk"}.issubset(set(evidence[0].matched_terms))
    assert any("SOC 2 Type II controls" in item.text for item in evidence)
    assert evidence[0].source is not None
    assert evidence[0].context_before is not None or evidence[0].context_after is not None
    assert len({item.text for item in evidence}) == len(evidence)
    assert all(len(item.text) <= 700 for item in evidence)
