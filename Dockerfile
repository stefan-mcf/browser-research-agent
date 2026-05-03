FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    BROWSER_RESEARCH_AGENT_NO_SANDBOX=1 \
    PORT=8000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN pip install --upgrade pip \
    && pip install -e '.[api]' \
    && python -m playwright install --with-deps chromium

COPY docs ./docs
COPY examples ./examples
COPY tests/fixtures ./tests/fixtures

RUN useradd --create-home --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/artifacts \
    && chown -R appuser:appuser /app /ms-playwright

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS "http://127.0.0.1:${PORT}/health" || exit 1

CMD ["sh", "-c", "uvicorn browser_research_agent.api:app --host 0.0.0.0 --port ${PORT:-8000}"]
