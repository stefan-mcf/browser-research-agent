# Browser Research Agent

Domain-agnostic browser automation research engine. Provide an objective and URLs — the agent handles browser automation, evidence extraction, and transparent source scoring for any research domain: vendor due diligence, market research, competitor analysis, real estate intelligence, job market scanning, academic literature review, or any repeatable web research workflow.

## Features

- Drives a real browser with Playwright.
- Visits supplied research URLs and captures auditable artifacts.
- Extracts metadata, headings, visible text, links, and objective-matching evidence snippets.
- Scores each page for relevance, credibility, and freshness with an inspectable rubric.
- Writes ranked JSON and Markdown reports for downstream review.
- Exposes the same research core through a CLI and a local FastAPI service.
- Keeps failures visible as structured page errors instead of failing an entire run.
- Domain-agnostic core — swap fixtures, objectives, and URLs to target any research domain.

## Use cases

The same engine powers research across many domains. Examples:

| Domain | Sample objective |
|--------|------------------|
| Vendor due diligence | "Find SOC 2 audit evidence, security certifications, and data-residency commitments" |
| Market research | "Identify pricing tiers, target segments, and competitive positioning across these SaaS landing pages" |
| Real estate intelligence | "Extract property details, agent contact information, and listing history for these 15 properties" |
| Job market scanning | "Find AI automation roles with Python, FastAPI, and multi-agent requirements posted this week" |
| Competitor analysis | "Map feature claims, integrations listed, and customer logos from these competitor homepages" |
| Academic literature review | "Extract methodology sections, dataset references, and author affiliations from these paper pages" |

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev,api]'
python -m playwright install chromium
bash examples/demo-command.sh
```

The demo uses simulated local fixtures and writes outputs under `artifacts/demo`.

## CLI

Run a research job against one or more URLs:

```bash
# Vendor due diligence example
browser-research-agent research \
  --objective "find SOC 2 audit reporting and vendor risk compliance evidence" \
  --url https://vendor-a.example/security \
  --url https://vendor-b.example/trust \
  --out artifacts/run-001 \
  --headless

# Job market intelligence example (same engine, different domain)
browser-research-agent research \
  --objective "identify AI automation roles requiring Python, FastAPI, and multi-agent experience" \
  --url https://example-job-board.example/search?q=ai+automation \
  --out artifacts/run-002 \
  --headless
```

Output includes:

- `report.md`: reviewer-readable ranked research report.
- `summary.json`: ranked pages and aggregate run metadata.
- `pages/*.json`: extracted evidence and scores per page.
- `pages/*.html`: captured page HTML.
- `pages/*.png`: screenshot evidence when screenshots are enabled.

## API

Run the local FastAPI service over the same repeatable research core:

```bash
source .venv/bin/activate
uvicorn browser_research_agent.api:app --host 127.0.0.1 --port 8000
```

Useful local endpoints:

- `GET /health`: health check.
- `POST /research`: run a browser research job and return ranked page summaries plus report and evidence paths.
- `GET /docs`: interactive OpenAPI docs served by FastAPI.

See `docs/api.md` for request examples and safety boundaries. Add authentication, rate limits, storage policy, and deployment review before exposing the API beyond trusted local environments.

## Demo package

The bundled demo uses SaaS vendor compliance fixtures as one example domain. The core engine is domain-agnostic — swap the fixtures and objective to target any research domain.

- `examples/request.json`: sample request shape.
- `examples/demo-command.sh`: repeatable local demo command (vendor compliance domain).
- `examples/sample-output/`: curated sample report and summary JSON generated from simulated pages.
- `examples/api-sample-output/research-response.json`: sanitized sample `POST /research` response.
- `docs/demo-walkthrough.md`: short demo walkthrough.
- `tests/fixtures/*.html`: simulated pages used for stable demos and tests.
- `docs/product-brief.md`: broader product concept and extension points.
- `docs/architecture.md`: implementation architecture and data flow.
- `docs/output-schema.md`: JSON output contract.
- `docs/scoring-rubric.md`: transparent scoring explanation.
- `docs/api.md`: local FastAPI request/response guide and safety notes.
- `docs/screenshots/`: curated visual evidence set: OpenAPI docs, sample report, API response, and quality gates.

## Running tests

```bash
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
ruff check src tests
```

## Local Docker smoke test

```bash
docker build -t browser-research-agent .
docker run --rm browser-research-agent research \
  --objective "verify the health endpoint and fixture processing" \
  --url "file:///app/tests/fixtures/vendor_security.html" \
  --out /tmp/docker-smoke \
  --report markdown
```

## Design constraints

- No login/session automation.
- No stealth scraping or CAPTCHA bypass.
- No paywall bypass.
- No hidden data exfiltration.
- No required LLM dependency in the core path — scoring is heuristic and inspectable.
- Domain-agnostic engine stays separate from domain-specific logic (parsing, heuristics, proposal templates).

## Extension points

- Search-provider URL discovery.
- LLM synthesis constrained to captured evidence.
- Entity extraction and claim normalization.
- Hosted API deployment after authentication, rate limits, scope, and artifact-storage policy are defined.
- Domain-specific layers (Upwork intelligence, real estate analysis, vendor assessment) that use this engine as foundation.
- Lightweight review UI for screenshots and snippets.
