# Demo Walkthrough

This walkthrough uses simulated pages so the project can be reviewed without crawling third-party websites.

## Run

```bash
source .venv/bin/activate
bash examples/demo-command.sh
```

## Inspect

- Open `artifacts/demo/report.md` for the generated Markdown report.
- Review `artifacts/demo/summary.json` for machine-readable ranked results.
- Inspect `artifacts/demo/pages/` for screenshots, HTML, and per-page JSON.

## API example

Run the local API separately when you want an integration-style example:

```bash
source .venv/bin/activate
uvicorn browser_research_agent.api:app --host 127.0.0.1 --port 8000
```

Then inspect:

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`
- `docs/api.md` for a fixture-backed `POST /research` curl example.

## Review positioning

Browser Research Agent is a domain-agnostic research engine for evidence-backed findings instead of generic summaries. The included demo uses SaaS vendor compliance fixtures as one example domain: security pages, SOC 2 evidence, audit-reporting language, trust-center signals, and vendor-risk review. Swap the fixtures and objective — the same engine handles real estate research, job market scanning, competitor analysis, or any repeatable web research workflow.

## Proof assets

- `tests/fixtures/*.html`: simulated compliance/security pages used for stable demos.
- `examples/sample-output/report.md`: curated sample report generated from the fixtures.
- `examples/sample-output/summary.json`: machine-readable ranked result.
- `examples/api-sample-output/research-response.json`: sanitized sample API response.
- `docs/screenshots/`: OpenAPI, report, API response, and quality-gate visuals.

## Safety boundary

The demo is local-first and fixture-backed. Before adapting it to live websites or hosted access, define target-site usage policy, authentication, rate limits, artifact retention, and log redaction.
