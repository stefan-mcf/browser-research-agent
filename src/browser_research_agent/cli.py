from __future__ import annotations

import asyncio
import json
from pathlib import Path

import click
from rich.console import Console

from browser_research_agent.agent import research_urls

console = Console()


@click.group()
def main() -> None:
    """Browser Research Agent CLI."""


@main.command()
@click.option("--objective", required=True, help="Research objective or buying criterion.")
@click.option(
    "--url", "urls", multiple=True, required=True, help="URL to research. Can be repeated."
)
@click.option(
    "--out",
    "out_dir",
    default="artifacts/run",
    type=click.Path(path_type=Path),
    help="Artifact output directory.",
)
@click.option("--headless/--headed", default=True, help="Run Chromium headless or visibly.")
@click.option(
    "--timeout-ms", default=30_000, show_default=True, help="Per-page navigation timeout."
)
@click.option(
    "--max-pages",
    default=None,
    type=int,
    help="Maximum number of URLs to process from the request.",
)
@click.option(
    "--include-screenshots/--no-screenshots", default=True, help="Capture full-page screenshots."
)
@click.option("--user-agent", default=None, help="Optional browser user-agent override.")
@click.option(
    "--report",
    type=click.Choice(["markdown", "none"]),
    default="markdown",
    show_default=True,
    help="Report output mode.",
)
def research(
    objective: str,
    urls: tuple[str, ...],
    out_dir: Path,
    headless: bool,
    timeout_ms: int,
    max_pages: int | None,
    include_screenshots: bool,
    user_agent: str | None,
    report: str,
) -> None:
    """Research URLs and produce evidence/scoring artifacts."""
    run = asyncio.run(
        research_urls(
            objective=objective,
            urls=list(urls),
            out_dir=out_dir,
            headless=headless,
            timeout_ms=timeout_ms,
            max_pages=max_pages,
            include_screenshots=include_screenshots,
            user_agent=user_agent,
            report=report,
        )
    )
    console.print_json(json.dumps(run.to_summary()))
    console.print(f"[green]Wrote artifacts to {out_dir.resolve()}[/green]")


if __name__ == "__main__":
    main()
