# Architecture

Browser Research Agent is a local-first research automation tool. It uses a real browser to capture pages, extracts objective-matched evidence, scores each source, and writes auditable artifacts for review.

## Module map

- `config.py`: validated run configuration shared by CLI, browser runner, and future adapters.
- `agent.py`: Playwright orchestration, page capture, artifact writing, and run summary persistence.
- `extractor.py`: HTML parsing, visible-text extraction, metadata extraction, link normalization, and evidence snippet selection.
- `scoring.py`: repeatable relevance, credibility, freshness, and confidence scoring.
- `models.py`: Pydantic contracts for configs, page metadata, evidence, scoring, errors, and run summaries.
- `reporting.py`: Markdown report rendering.
- `cli.py`: command-line product surface.

## Data flow

1. A user provides an objective and URLs through the CLI.
2. The CLI builds a `ResearchConfig`.
3. `agent.py` opens each URL in Chromium using Playwright.
4. For every page, the runner captures HTML and optional screenshots.
5. `extractor.py` turns HTML into structured text, headings, links, and evidence snippets.
6. `scoring.py` assigns transparent scores and reasons.
7. `agent.py` writes per-page JSON plus `summary.json`.
8. `reporting.py` writes `report.md` for client review.

## Artifact lifecycle

Generated crawl artifacts are written under `artifacts/` and ignored by git. The repo should commit only source code, tests, docs, and stable fixtures. Live crawl outputs should be regenerated during demos rather than versioned.

## Safety boundaries

The current system intentionally does not perform login automation, CAPTCHA bypass, stealth scraping, paywall bypass, or hidden data extraction. Failed pages are represented as structured errors rather than fatal exceptions so users can inspect partial evidence and retry intentionally.
