from browser_research_agent.extractor import extract_evidence, extract_page, normalize_terms


def test_normalize_terms_removes_stop_words() -> None:
    assert "soc" in normalize_terms("Find evidence for SOC 2 compliance automation")
    assert "find" not in normalize_terms("Find evidence for SOC 2 compliance automation")


def test_extract_page_visible_text_and_links() -> None:
    html = """
    <html><head><title>Vendor</title><meta name='description' content='Security platform'></head>
    <body><script>hidden()</script><h1>SOC 2 automation</h1><a href='/security'>Security</a></body></html>
    """
    page = extract_page(html, "https://example.com")
    assert page.title == "Vendor"
    assert page.description == "Security platform"
    assert "SOC 2 automation" in page.text
    assert "hidden" not in page.text
    assert page.links == ["https://example.com/security"]


def test_extract_evidence_scores_matching_sentences() -> None:
    text = "Vendor news. The platform provides SOC 2 compliance automation with audit evidence collection."
    evidence = extract_evidence("SOC 2 compliance automation evidence", text)
    assert evidence
    assert evidence[0].matched_terms
    assert "SOC 2 compliance" in evidence[0].text
