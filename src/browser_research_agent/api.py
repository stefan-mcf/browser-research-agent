from __future__ import annotations

from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

from browser_research_agent.agent import research_urls
from browser_research_agent.models import PageResearchResult


def _public_path(path: Path) -> str:
    """Return a repo-relative artifact path without exposing host filesystem details."""
    resolved = path.resolve()
    try:
        return resolved.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return resolved.name


class ResearchRequest(BaseModel):
    objective: str = Field(min_length=3)
    urls: list[str] = Field(min_length=1)
    out_dir: Path | None = None
    headless: bool = True
    timeout_ms: int = Field(default=30_000, ge=1_000, le=120_000)
    max_pages: int | None = Field(default=None, ge=1)
    include_screenshots: bool = True
    user_agent: str | None = None
    report: Literal["markdown", "none"] = "markdown"


class ResearchPageSummary(BaseModel):
    title: str | None
    url: str
    final_url: str
    total_score: float
    relevance: float
    credibility: float
    freshness: float
    evidence_count: int
    artifact_paths: dict[str, str]
    error: dict[str, object] | None = None


class ResearchResponse(BaseModel):
    status: Literal["completed"]
    run_id: str
    objective: str
    page_count: int
    strong_candidates: int
    review_candidates: int
    weak_candidates: int
    summary_path: str
    report_path: str | None
    pages: list[ResearchPageSummary]


app = FastAPI(
    title="Browser Research Agent API",
    description="Local-first API for evidence-backed browser research runs.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest) -> ResearchResponse:
    run_id = uuid4().hex[:12]
    out_dir = request.out_dir or Path("artifacts") / "api-runs" / run_id
    run = await research_urls(
        objective=request.objective,
        urls=request.urls,
        out_dir=out_dir,
        headless=request.headless,
        timeout_ms=request.timeout_ms,
        max_pages=request.max_pages,
        include_screenshots=request.include_screenshots,
        user_agent=request.user_agent,
        report=request.report,
    )
    ranked_pages = run.ranked_pages
    return ResearchResponse(
        status="completed",
        run_id=run_id,
        objective=run.objective,
        page_count=len(run.pages),
        strong_candidates=sum(1 for page in run.pages if page.scores.total >= 0.72),
        review_candidates=sum(1 for page in run.pages if 0.45 <= page.scores.total < 0.72),
        weak_candidates=sum(1 for page in run.pages if page.scores.total < 0.45),
        summary_path=_public_path(out_dir / "summary.json"),
        report_path=_public_path(out_dir / "report.md") if request.report == "markdown" else None,
        pages=[_page_summary(page) for page in ranked_pages],
    )


def _page_summary(page: PageResearchResult) -> ResearchPageSummary:
    return ResearchPageSummary(
        title=page.metadata.title,
        url=page.metadata.url,
        final_url=page.metadata.final_url,
        total_score=page.scores.total,
        relevance=page.scores.relevance,
        credibility=page.scores.credibility,
        freshness=page.scores.freshness,
        evidence_count=len(page.evidence),
        artifact_paths={name: _public_path(path) for name, path in page.artifacts.items()},
        error=page.error.model_dump(mode="json") if page.error else None,
    )
