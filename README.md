# Browser Research Agent

Browser automation research agent with evidence extraction, deterministic artifacts, and transparent source scoring for repeatable web research workflows.

## Features

- Drives a real browser with Playwright.
- Visits supplied research URLs and captures auditable artifacts.
- Extracts metadata, headings, visible text, links, and objective-matching evidence snippets.
- Scores each page for relevance, credibility, and freshness with an inspectable rubric.
- Writes ranked JSON and Markdown reports for downstream review.
- Exposes the same research core through a CLI and a local FastAPI service.
- Keeps failures visible as structured page errors instead of failing an entire run.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev,api]'
python -m playwright install chromium
bash examples/demo-command.sh
```

The deterministic demo uses synthetic local fixtures and writes outputs under `artifacts/demo`.

## CLI

Run a research job against one or more URLs:

```bash
browser-research-agent research \
  --objective "research question or buying criterion" \
  --url https://vendor-a.example \
  --url https://vendor-b.example/security \
  --out artifacts/run-001 \
  --headless
```

Output includes:

- `report.md`: reviewer-readable ranked research report.
- `summary.json`: ranked pages and aggregate run metadata.
- `pages/*.json`: extracted evidence and scores per page.
- `pages/*.html`: captured page HTML.
- `pages/*.png`: screenshot evidence when screenshots are enabled.

## API

Run the local FastAPI surface over the same deterministic research core:

```bash
source .venv/bin/activate
uvicorn browser_research_agent.api:app --host 127.0.0.1 --port 8000
```

Useful local endpoints:

- `GET /health`: health check.
- `POST /research`: run a browser research job and return ranked page summaries, local artifact paths, and report/summary paths.
- `GET /docs`: interactive OpenAPI docs served by FastAPI.

See `docs/api.md` for request examples and safety boundaries. Add authentication, rate limits, storage policy, and deployment review before exposing the API beyond trusted local/private environments.

## Demo package

- `examples/request.json`: sample request shape.
- `examples/demo-command.sh`: repeatable deterministic local demo command.
- `examples/sample-output/`: curated sample report and summary JSON generated from synthetic fixtures.
- `examples/api-sample-output/research-response.json`: sanitized sample `POST /research` response.
- `docs/demo-walkthrough.md`: short demo walkthrough.
- `docs/product-brief.md`: product overview and extension points.
- `docs/architecture.md`: implementation architecture.
- `docs/output-schema.md`: JSON output contract.
- `docs/scoring-rubric.md`: transparent scoring explanation.
- `docs/api.md`: local FastAPI request/response guide.
- `docs/deployment.md`: Docker/container deployment-prep runbook.
- `docs/screenshots/`: visual evidence set.
- `tests/fixtures/*.html`: synthetic SaaS compliance pages used for stable demos and tests.
- `Dockerfile`, `docker-compose.yml`, `.env.example`: local container contract; no cloud resources are provisioned by default.

## Intended use cases

- SaaS vendor and compliance research.
- Vendor due diligence.
- Market and competitor research.
- Procurement shortlist scoring.
- Lead qualification with evidence trails.

## Visual evidence

The screenshot evidence set is available as full-size image links:

- [OpenAPI docs screenshot](docs/screenshots/01-openapi-docs.png)
- [Sample report screenshot](docs/screenshots/02-sample-report.png)
- [API JSON response screenshot](docs/screenshots/03-api-json-response.png)
- [Quality gates screenshot](docs/screenshots/04-quality-gates.png)

The screenshots are generated from deterministic synthetic fixtures and local-only runs. They do not show a public cloud deployment, credentials, or live customer data.

## Limitations

- Manually supplied URLs only; search discovery is a planned adapter.
- Local CLI, local FastAPI API, and local Docker/container smoke surfaces are implemented; hosted deployment is intentionally left to project-specific review.
- No login automation, CAPTCHA bypass, paywall bypass, stealth scraping, authentication layer, or LLM synthesis by default.
- Scores are triage signals and should be reviewed alongside captured artifacts.
- Live web research must respect target-site terms, robots/legal constraints, and data retention requirements.

## License

MIT License. See `LICENSE`.
