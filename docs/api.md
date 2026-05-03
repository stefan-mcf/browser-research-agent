# API Guide

Browser Research Agent now includes a local FastAPI surface over the same deterministic Playwright research core used by the CLI.

## Status

- Local/private API proof: implemented.
- Cloud deployment: not provisioned; local Docker deployment prep is documented in `docs/deployment.md`.
- Authentication: not implemented; add before any public deployment.
- LLM synthesis: not part of the API path.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev,api]'
python -m playwright install chromium
```

## Run locally

```bash
source .venv/bin/activate
uvicorn browser_research_agent.api:app --host 127.0.0.1 --port 8000
```

Open the interactive API docs locally:

```text
http://127.0.0.1:8000/docs
```

## Health check

```bash
curl -fsS http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

## Research request

Use committed synthetic fixtures for stable local proof:

```bash
curl -fsS -X POST http://127.0.0.1:8000/research \
  -H 'Content-Type: application/json' \
  -d "{
    \"objective\": \"find SOC 2 audit reporting and vendor risk compliance evidence\",
    \"urls\": [
      \"file://$PWD/tests/fixtures/vendor_security.html\",
      \"file://$PWD/tests/fixtures/vendor_blog.html\",
      \"file://$PWD/tests/fixtures/vendor_careers.html\"
    ],
    \"out_dir\": \"artifacts/api-demo\",
    \"include_screenshots\": false,
    \"report\": \"markdown\"
  }" | python -m json.tool
```

Response includes:

- `status`: completed when the synchronous local run finishes.
- `run_id`: generated identifier for the API request.
- `summary_path`: local path to `summary.json`.
- `report_path`: local path to `report.md` when Markdown reporting is enabled.
- `pages`: ranked page summaries with scores, evidence counts, artifact paths, and any structured page error.

A sanitized example response is committed at `examples/api-sample-output/research-response.json`.

## Request fields

| Field | Type | Default | Notes |
|---|---:|---:|---|
| `objective` | string | required | Research objective; minimum 3 characters. |
| `urls` | list[string] | required | URLs to visit; at least one required. |
| `out_dir` | string/path | `artifacts/api-runs/<run_id>` | Local artifact directory. |
| `headless` | boolean | `true` | Run Chromium headless by default. |
| `timeout_ms` | integer | `30000` | Per-page timeout, 1,000 to 120,000 ms. |
| `max_pages` | integer/null | `null` | Optional cap on processed URLs. |
| `include_screenshots` | boolean | `true` | Capture screenshots unless disabled. |
| `user_agent` | string/null | `null` | Optional browser user-agent override. |
| `report` | `markdown` or `none` | `markdown` | Controls Markdown report generation. |

## Safety boundaries

This API is a local proof surface. Before any public/cloud deployment, add explicit decisions for:

- authentication/authorization,
- target-site scope and permission,
- rate limits and abuse prevention,
- storage lifecycle for screenshots/HTML artifacts,
- secrets/environment handling,
- deployment provider and cost posture.

Do not expose this API publicly as-is.
