# Screenshot Evidence

These screenshots are generated from deterministic synthetic fixtures and local runs. They do not show a public cloud deployment, credentials, or live customer data.

## Files

- `01-openapi-docs.png` — local FastAPI `/docs` surface for integration review.
- `02-sample-report.png` — generated Markdown research report rendered for visual review.
- `03-api-json-response.png` — sanitized `POST /research` JSON response proof.
- `04-quality-gates.png` — local verification proof for lint, type-check, tests, JSON validation, and Compose config.

## Source helpers

- `source-sample-report.html`
- `source-api-json-response.html`
- `source-quality-gates.html`

These HTML files are committed to make the screenshot evidence reproducible and easy to inspect locally.

## Regeneration

From the repo root:

```bash
source .venv/bin/activate
bash examples/demo-command.sh
uvicorn browser_research_agent.api:app --host 127.0.0.1 --port 8012
python scripts/generate_screenshot_evidence.py
```

Stop the Uvicorn process after capture. The generator expects `/tmp/browser-research-agent-api-response.json` and `/tmp/browser-research-agent-quality-gates.txt` to exist from the verification pass.
