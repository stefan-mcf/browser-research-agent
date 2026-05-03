# Demo Walkthrough

This walkthrough uses deterministic synthetic fixtures so the project can be reviewed without crawling third-party websites.

## Run

```bash
source .venv/bin/activate
bash examples/demo-command.sh
```

## Inspect

- Open `artifacts/demo/report.md` for the generated Markdown report.
- Review `artifacts/demo/summary.json` for machine-readable ranked results.
- Inspect `artifacts/demo/pages/` for screenshots, HTML, and per-page JSON.

## API proof

Run the local API separately when you want integration-style proof:

```bash
source .venv/bin/activate
uvicorn browser_research_agent.api:app --host 127.0.0.1 --port 8000
```

Then inspect:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`
- `docs/api.md` for a fixture-backed `POST /research` curl example.

## Review positioning

Browser Research Agent is a repeatable research workflow for people who need evidence-backed findings instead of opaque summaries. The included demo niche is SaaS vendor/compliance research: security pages, SOC 2 evidence, audit-reporting language, trust-center signals, and vendor-risk review.

## Proof assets

- `tests/fixtures/*.html`: synthetic compliance/security pages used for stable demos.
- `examples/sample-output/report.md`: curated sample report generated from the fixtures.
- `examples/sample-output/summary.json`: machine-readable ranked result.
- `examples/api-sample-output/research-response.json`: sanitized sample API response.
- `docs/screenshots/`: OpenAPI, report, API response, and quality-gate visuals.

## Safety boundary

The demo is local-first and fixture-backed. Before adapting it to live websites or hosted access, define target-site usage policy, authentication, rate limits, artifact retention, and log redaction.
