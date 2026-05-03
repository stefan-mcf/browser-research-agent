# Screenshot Evidence

These screenshots are generated from simulated data and local test runs. They do not show a public cloud deployment, sensitive credentials, or live customer data.

## Files

- `01-openapi-docs.png` — local API documentation for understanding integration points.
- `02-sample-report.png` — visual example of a generated Markdown research report.
- `03-api-json-response.png` — sanitized JSON response from the `POST /research` endpoint.
- `04-quality-gates.png` — local verification checks, including linting, type-checking, tests, JSON validation, and Docker Compose configuration.

## Supporting HTML files

- `source-sample-report.html`
- `source-api-json-response.html`
- `source-quality-gates.html`

These HTML files are included so the screenshot evidence is reproducible and easy to inspect locally.

## Regeneration

From the repo root:

```bash
source .venv/bin/activate
bash examples/demo-command.sh
uvicorn browser_research_agent.api:app --host 127.0.0.1 --port 8012
python scripts/generate_screenshot_evidence.py
```

Stop the Uvicorn process after capture. The generator reads API-response and quality-gate inputs from environment variables or repo-relative defaults; see `scripts/generate_screenshot_evidence.py` for the exact paths.
