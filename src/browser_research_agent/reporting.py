from __future__ import annotations

from pathlib import Path

from browser_research_agent.models import PageResearchResult, ResearchRun


def render_markdown_report(run: ResearchRun) -> str:
    lines: list[str] = [
        "# Browser Research Report",
        "",
        f"Objective: {run.objective}",
        f"Created at: {run.created_at.isoformat()}",
        "",
        "## Executive summary",
        "",
    ]
    if not run.pages:
        lines.extend(["No pages were captured.", ""])
    else:
        lines.extend(
            [
                f"Captured pages: {len(run.pages)}",
                f"Strong candidates: {sum(1 for page in run.pages if page.scores.total >= 0.72)}",
                f"Review candidates: {sum(1 for page in run.pages if 0.45 <= page.scores.total < 0.72)}",
                f"Weak candidates: {sum(1 for page in run.pages if page.scores.total < 0.45)}",
                "",
                "## Ranked findings",
                "",
            ]
        )
        for rank, page in enumerate(run.ranked_pages, start=1):
            lines.extend(_render_page(rank, page))

    lines.extend(
        [
            "## How this report was generated",
            "",
            "This report was generated using data captured from web pages, including HTML, optional screenshots, extracted metadata, links, and snippets matching the research objective.",
            "Each page is scored with a consistent system so users can examine the evidence directly rather than relying on a generic summary.",
            "",
            "## Limitations",
            "",
            "Scores help prioritize research review; they are not final judgments. Review screenshots, HTML, and extracted snippets before making business decisions.",
            "The system does not perform login automation, CAPTCHA bypass, paywall bypass, search discovery, or AI-generated synthesis by default.",
            "",
            "## Scoring rubric",
            "",
            "Total score = 50% relevance + 35% credibility + 15% freshness.",
            "Scores indicate the relevance of captured evidence and should be reviewed alongside screenshots and captured HTML.",
            "See `docs/scoring-rubric.md` for the full scoring explanation.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_markdown_report(run: ResearchRun, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "report.md"
    path.write_text(render_markdown_report(run), encoding="utf-8")
    return path


def _render_page(rank: int, page: PageResearchResult) -> list[str]:
    title = page.metadata.title or page.metadata.final_url
    lines = [
        f"### {rank}. {title}",
        "",
        f"- URL: {page.metadata.final_url}",
        f"- Total score: {page.scores.total:.4f}",
        f"- Relevance: {page.scores.relevance:.4f}",
        f"- Credibility: {page.scores.credibility:.4f}",
        f"- Freshness: {page.scores.freshness:.4f}",
    ]
    if page.error:
        lines.append(f"- Capture error: {page.error.kind} — {page.error.message}")
    if page.artifacts:
        lines.append("- Artifacts:")
        for name, path in sorted(page.artifacts.items()):
            lines.append(f"  - {name}: `{path}`")
    if page.scores.reasons:
        lines.append("- Scoring rationale:")
        for reason in page.scores.reasons[:8]:
            lines.append(f"  - {reason}")
    if page.evidence:
        lines.extend(["", "Evidence:"])
        for item in page.evidence[:5]:
            matched = ", ".join(item.matched_terms)
            lines.append(f"- ({item.score:.2f}; {matched}) {item.text}")
    else:
        lines.extend(["", "Evidence: none extracted."])
    lines.append("")
    return lines
