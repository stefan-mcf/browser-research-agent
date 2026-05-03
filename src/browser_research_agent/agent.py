from __future__ import annotations

import json
import os
import time
from datetime import UTC, datetime
from pathlib import Path

from playwright.async_api import (
    BrowserContext,
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)

from browser_research_agent.artifacts import safe_slug
from browser_research_agent.config import ResearchConfig
from browser_research_agent.extractor import extract_evidence, extract_page
from browser_research_agent.models import (
    PageError,
    PageMetadata,
    PageResearchResult,
    ResearchRun,
    ScoreBreakdown,
)
from browser_research_agent.scoring import score_page
from browser_research_agent.reporting import write_markdown_report


async def research_urls(
    *,
    objective: str,
    urls: list[str],
    out_dir: Path,
    headless: bool = True,
    timeout_ms: int = 30_000,
    max_pages: int | None = None,
    include_screenshots: bool = True,
    user_agent: str | None = None,
    report: str = "markdown",
) -> ResearchRun:
    config = ResearchConfig(
        objective=objective,
        urls=urls,
        out_dir=out_dir,
        headless=headless,
        timeout_ms=timeout_ms,
        max_pages=max_pages,
        include_screenshots=include_screenshots,
        user_agent=user_agent,
        report=report,
    )
    return await research_with_config(config)


async def research_with_config(config: ResearchConfig) -> ResearchRun:
    config.out_dir.mkdir(parents=True, exist_ok=True)
    pages_dir = config.out_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    results: list[PageResearchResult] = []
    async with async_playwright() as p:
        launch_args = ["--no-sandbox"] if _truthy_env("BROWSER_RESEARCH_AGENT_NO_SANDBOX") else []
        browser = await p.chromium.launch(headless=config.headless, args=launch_args)
        if config.user_agent:
            context = await browser.new_context(
                viewport={"width": 1440, "height": 1200},
                user_agent=config.user_agent,
            )
        else:
            context = await browser.new_context(viewport={"width": 1440, "height": 1200})
        try:
            for index, url in enumerate(config.urls, start=1):
                result = await _research_single_url(
                    context=context,
                    objective=config.objective,
                    url=url,
                    pages_dir=pages_dir,
                    index=index,
                    timeout_ms=config.timeout_ms,
                    include_screenshots=config.include_screenshots,
                )
                results.append(result)
        finally:
            await context.close()
            await browser.close()

    run = ResearchRun(objective=config.objective, created_at=datetime.now(tz=UTC), pages=results)
    (config.out_dir / "summary.json").write_text(
        json.dumps(run.to_summary(), indent=2), encoding="utf-8"
    )
    if config.report == "markdown":
        write_markdown_report(run, config.out_dir)
    return run


def _truthy_env(name: str) -> bool:
    return os.getenv(name, "").lower() in {"1", "true", "yes", "on"}


async def _research_single_url(
    context: BrowserContext,
    objective: str,
    url: str,
    pages_dir: Path,
    index: int,
    timeout_ms: int,
    include_screenshots: bool,
) -> PageResearchResult:
    page = await context.new_page()
    response = None
    fetched_at = datetime.now(tz=UTC)
    started = time.perf_counter()
    error: PageError | None = None
    html = ""
    final_url = url

    try:
        response = await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        try:
            await page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 10_000))
        except PlaywrightTimeoutError:
            # Network idle is useful but many modern sites keep connections open; keep capture.
            pass
    except PlaywrightTimeoutError as exc:
        error = PageError(message=_error_message(exc), kind="timeout", recoverable=True)
    except PlaywrightError as exc:
        error = PageError(message=_error_message(exc), kind="navigation", recoverable=True)
    except Exception as exc:  # noqa: BLE001 - preserve unexpected failures as data artifacts.
        error = PageError(message=str(exc), kind="unknown", recoverable=True)

    try:
        final_url = page.url or url
        html = await page.content()
    except Exception as exc:  # noqa: BLE001
        error = PageError(message=str(exc), kind="capture", recoverable=False)
        html = ""

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    slug = safe_slug(final_url, index)
    html_path = pages_dir / f"{slug}.html"
    json_path = pages_dir / f"{slug}.json"
    artifacts: dict[str, Path] = {"html": html_path, "json": json_path}

    html_path.write_text(html, encoding="utf-8")
    if include_screenshots:
        png_path = pages_dir / f"{slug}.png"
        try:
            await page.screenshot(path=str(png_path), full_page=True)
            artifacts["screenshot"] = png_path
        except Exception as exc:  # noqa: BLE001
            error = error or PageError(message=str(exc), kind="screenshot", recoverable=True)

    if html:
        try:
            extracted = extract_page(html, final_url)
            evidence = extract_evidence(objective, extracted.text)
            scores = score_page(final_url, objective, extracted, evidence)
            links = extracted.links[:250]
            title = extracted.title
            description = extracted.description
            canonical_url = extracted.canonical_url
        except Exception as exc:  # noqa: BLE001 - keep multi-page runs resilient.
            error = PageError(message=_error_message(exc), kind="extraction", recoverable=True)
            evidence = []
            scores = ScoreBreakdown(relevance=0, credibility=0, freshness=0, total=0, reasons=[])
            links = []
            title = description = canonical_url = None
    else:
        evidence = []
        scores = ScoreBreakdown(relevance=0, credibility=0, freshness=0, total=0, reasons=[])
        links = []
        title = description = canonical_url = None

    result = PageResearchResult(
        metadata=PageMetadata(
            url=url,
            final_url=final_url,
            title=title,
            description=description,
            canonical_url=canonical_url,
            fetched_at=fetched_at,
            status_code=response.status if response else None,
            elapsed_ms=elapsed_ms,
            content_length=len(html),
        ),
        evidence=evidence,
        links=links,
        scores=scores,
        artifacts=artifacts,
        error=error,
    )
    json_path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    await page.close()
    return result


def _error_message(exc: BaseException) -> str:
    return next((line for line in str(exc).splitlines() if line.strip()), exc.__class__.__name__)
