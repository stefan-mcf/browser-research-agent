# Product Brief: Browser Research Agent

## Concept

Browser Research Agent is a domain-agnostic research automation engine for gathering verifiable web evidence from any set of URLs. It opens web pages in a real browser, captures durable artifacts, extracts objective-relevant snippets, and scores sources with transparent heuristics.

The project is designed for repeatable research workflows across any domain — vendor due diligence, market research, competitor analysis, real estate intelligence, job market scanning, academic literature review, or any task where reviewers need an evidence trail rather than unsupported summaries. The engine is domain-agnostic; use cases are defined by the objective and URLs you provide.

## Value

- Reduces repetitive web research work.
- Produces evidence trails instead of generic summaries.
- Ranks sources so reviewers can focus on the strongest findings first.
- Creates reusable artifacts: JSON, screenshots, captured HTML, and Markdown reports.
- Keeps the core repeatable and auditable before optional AI-generated synthesis is added.

## Core loop

1. Receive a research objective and candidate URLs.
2. Open each URL in an automated browser.
3. Capture page HTML and optional screenshot for auditability.
4. Extract visible text, title, metadata, canonical URL, headings, and outgoing links.
5. Identify objective-relevant evidence snippets with context.
6. Score each page on:
   - Relevance: objective-term overlap and evidence density.
   - Credibility: HTTPS, domain heuristics, about/contact/legal/security signals, and outbound references.
   - Freshness: detected dates and recency signals.
7. Produce ranked JSON and Markdown reports with evidence references.

## Best-fit use cases

The engine is domain-agnostic. Use cases are defined by the objective and URLs you provide. Common domains include:

- SaaS vendor due diligence and security/compliance page review.
- Market research and competitive landscape analysis.
- Real estate intelligence and property listing analysis.
- Job market scanning and opportunity qualification.
- Competitor product and pricing research.
- Procurement shortlist scoring.
- Lead qualification with evidence trails.
- Academic literature and citation review.
- Any research workflow where source quality must be transparent and auditable.

## Current implementation

The repository includes:

- a CLI for fixture-backed and live-URL research runs,
- a local FastAPI service over the same research core,
- a Dockerfile and Compose service for local container smoke tests,
- simulated fixtures and sample outputs,
- a screenshot evidence package under `docs/screenshots/`,
- transparent scoring and output-schema documentation.

## Non-goals for the current version

- No login/session automation.
- No stealth scraping or CAPTCHA bypass.
- No paywall bypass.
- No hidden data exfiltration.
- No required LLM dependency in the core path.
- No unauthenticated public API deployment by default.

## Extension points

- Search-provider URL discovery.
- LLM synthesis constrained to captured evidence.
- Entity extraction and claim normalization.
- Hosted API deployment after authentication, rate limits, scope, and artifact-storage policy are defined.
- Lightweight review UI for screenshots and snippets.
