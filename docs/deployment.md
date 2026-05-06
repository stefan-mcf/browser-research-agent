# Deployment Preparation

Browser Research Agent includes a local FastAPI service and container contract that can be used for local smoke testing or adapted for a hosted deployment. The default project state is local-first: no cloud resources, public URLs, paid provider services, or release tags are created by the repository itself.

## Current deployment posture

- Runtime surface: local FastAPI API over the Playwright research core.
- Container status: local Docker image and Compose service are defined.
- Authentication: not implemented; keep the service local or otherwise access-controlled until an auth boundary is added.
- Secrets: none required for the local fixture-backed example.
- Public exposure: possible only after authentication, rate limits, storage policy, and target-site usage review are implemented.

## Local prerequisites

- Docker Desktop or Docker Engine.
- Network access during image build to install Python packages and Playwright Chromium dependencies.
- No provider credentials are required for the fixture-backed example.

## Build the image

Run from the repo root:

```bash
docker build -t browser-research-agent:local .
```

The Dockerfile:

- installs the package with the `api` extra,
- installs Playwright Chromium and system dependencies,
- exposes port `8000`,
- honors `PORT` at runtime via the container command,
- stores Playwright browser binaries under `/ms-playwright` so the non-root runtime user can launch Chromium,
- sets `BROWSER_RESEARCH_AGENT_NO_SANDBOX=1` in the container so Chromium can run reliably under Docker's container boundary,
- runs the app as a non-root `appuser`,
- defines a `/health` healthcheck.

## Run locally with Docker

```bash
docker rm -f browser-research-agent-smoke >/dev/null 2>&1 || true
docker run --name browser-research-agent-smoke \
  --shm-size=2g \
  -p 8010:8000 \
  -e PORT=8000 \
  -e BROWSER_RESEARCH_AGENT_NO_SANDBOX=1 \
  browser-research-agent:local
```

In another shell:

```bash
curl -fsS http://127.0.0.1:8010/health
```

Expected response:

```json
{"status":"ok"}
```

## Representative API smoke request

Use the included simulated pages so the smoke test is repeatable and does not crawl third-party sites:

```bash
ROOT="file:///app/tests/fixtures"
curl -fsS -X POST http://127.0.0.1:8010/research \
  -H 'Content-Type: application/json' \
  -d "{
    \"objective\": \"find SOC 2 audit reporting and vendor risk compliance evidence\",
    \"urls\": [
      \"${ROOT}/vendor_security.html\",
      \"${ROOT}/vendor_blog.html\",
      \"${ROOT}/vendor_careers.html\"
    ],
    \"out_dir\": \"artifacts/container-smoke\",
    \"headless\": true,
    \"include_screenshots\": true,
    \"report\": \"markdown\"
  }" | python -m json.tool
```

Expected result:

- `status` is `completed`.
- `page_count` is `3`.
- `summary_path` points to `artifacts/container-smoke/summary.json`.
- `report_path` points to `artifacts/container-smoke/report.md`.
- page artifacts are written under `artifacts/container-smoke/pages/`.

Stop and clean up:

```bash
docker rm -f browser-research-agent-smoke
```

## Run with Docker Compose

```bash
mkdir -p artifacts
docker compose up --build
```

The compose file maps:

- host `8000` to container `8000`,
- `./artifacts` to `/app/artifacts`,
- `/health` as the service healthcheck.

The `artifacts` directory is bind-mounted into the container for local output review. On Linux hosts, fix ownership or permissions if the non-root container user cannot write to the bind mount.

Stop it with:

```bash
docker compose down
```

## Environment variables

| Variable | Default | Required | Notes |
| --- | --- | --- | --- |
| `PORT` | `8000` | No | Used by the Docker command to bind Uvicorn inside the container. |
| `BROWSER_RESEARCH_AGENT_NO_SANDBOX` | `0` locally, `1` in Docker | No | Adds Chromium `--no-sandbox` for containerized runs. Keep disabled for normal local browser runs unless your environment requires it. |

`.env.example` is included for local runtime notes. The current local example does not require API keys or credentials.

## Secrets policy

- Do not commit `.env`, API keys, cookies, browser profiles, account exports, or customer data.
- Keep example inputs simulated unless a live-target review explicitly approves otherwise.
- If a LLM/search provider is added, document required variables in `.env.example` with empty values only.
- If a public deployment is added, add authentication and rate limiting before exposing `/research`.

## Candidate cloud targets

The container contract should be portable to:

- Render web service,
- Fly.io app,
- Railway service,
- Google Cloud Run,
- AWS ECS/Fargate.

Browser automation hosts may need Chromium `--no-sandbox`, larger shared memory, or provider-specific browser dependency settings. The local Docker path sets `BROWSER_RESEARCH_AGENT_NO_SANDBOX=1` and uses `--shm-size=2g` / Compose `shm_size: "2gb"`; verify equivalent settings before deploying elsewhere.

Before choosing any target, confirm:

1. provider/account to use,
2. cost limits,
3. public versus restricted access,
4. auth requirements,
5. artifact retention policy,
6. whether browser automation is allowed by the provider/runtime.

## Pre-deployment checklist

Do not deploy publicly until these are implemented for the target environment:

- [ ] Authentication or private network boundary.
- [ ] Rate limiting / request size limits suitable for public access.
- [ ] Storage retention policy for captured HTML/screenshots.
- [ ] Target-site usage policy and robots/legal review for live crawling.
- [ ] Secret management for any provider credentials.
- [ ] Observability/log redaction plan.
- [ ] Cloud provider, region, cost ceiling, and teardown policy.

## Verification checklist

- [ ] `ruff check .`
- [ ] `mypy src`
- [ ] `pytest -q`
- [ ] `bash examples/run-example.sh`
- [ ] `docker build -t browser-research-agent:local .`
- [ ] container `/health` smoke test with `--shm-size=2g`
- [ ] container `POST /research` smoke test against simulated pages
- [ ] non-root container user verified
- [ ] Docker health status verified
- [ ] `docker compose config` validates the Compose service
- [ ] local container removed after smoke test

## What is intentionally not included yet

- No hosted URL by default.
- No cloud resources or credentials.
- No paid provider integration.
- No public unauthenticated API exposure.
- No review UI.
