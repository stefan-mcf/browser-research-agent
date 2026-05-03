from datetime import UTC, datetime
from pathlib import Path

from browser_research_agent.models import (
    EvidenceSnippet,
    PageMetadata,
    PageResearchResult,
    ResearchRun,
    ScoreBreakdown,
)
from browser_research_agent.reporting import render_markdown_report, write_markdown_report


def _page(title: str, total: float, evidence_text: str) -> PageResearchResult:
    return PageResearchResult(
        metadata=PageMetadata(
            url=f"https://example.com/{title.lower().replace(' ', '-')}",
            final_url=f"https://example.com/{title.lower().replace(' ', '-')}",
            title=title,
            fetched_at=datetime(2026, 1, 1, tzinfo=UTC),
            status_code=200,
            elapsed_ms=100,
            content_length=1000,
        ),
        evidence=[
            EvidenceSnippet(text=evidence_text, score=0.9, matched_terms=["security", "audit"])
        ],
        links=["https://docs.example.com"],
        scores=ScoreBreakdown(
            relevance=0.8,
            credibility=0.7,
            freshness=0.6,
            total=total,
            reasons=["Matched objective terms: audit, security", "HTTPS source"],
            weights={"relevance": 0.5, "credibility": 0.35, "freshness": 0.15},
            details={"freshness": {"newest_date": "2026-01-01"}},
        ),
        artifacts={
            "html": Path("pages/page.html"),
            "screenshot": Path("pages/page.png"),
            "json": Path("pages/page.json"),
        },
    )


def test_render_markdown_report_contains_ranked_evidence_and_artifacts() -> None:
    run = ResearchRun(
        objective="Find security audit evidence",
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        pages=[
            _page("Weak Page", 0.3, "weak evidence"),
            _page("Strong Page", 0.9, "strong audit evidence"),
        ],
    )

    markdown = render_markdown_report(run)

    assert markdown.startswith("# Browser Research Report")
    assert "Objective: Find security audit evidence" in markdown
    assert markdown.index("Strong Page") < markdown.index("Weak Page")
    assert "strong audit evidence" in markdown
    assert "pages/page.png" in markdown
    assert "Scoring rubric" in markdown
    assert "Methodology" in markdown
    assert "Limitations" in markdown


def test_write_markdown_report_creates_report_file(tmp_path: Path) -> None:
    run = ResearchRun(
        objective="Find security audit evidence",
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
        pages=[],
    )

    path = write_markdown_report(run, tmp_path)

    assert path == tmp_path / "report.md"
    assert path.exists()
    assert "No pages were captured" in path.read_text()
