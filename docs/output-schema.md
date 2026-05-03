# Output Schema

The Browser Research Agent writes a run-level `summary.json` plus one JSON file per researched page.

## `summary.json`

- `objective` (`string`): user-supplied research objective.
- `created_at` (`datetime`): UTC timestamp for the completed run.
- `pages` (`array<PageResearchResult>`): researched pages sorted by descending total score.

## `PageResearchResult`

- `metadata` (`PageMetadata`): source URL, final URL, HTTP/status metadata, title, description, canonical URL, and timing fields.
- `evidence` (`array<EvidenceSnippet>`): ranked snippets matched to the objective.
- `links` (`array<string>`): normalized links discovered on the page, capped for output size.
- `scores` (`ScoreBreakdown`): relevance, credibility, freshness, confidence, total score, and reasons.
- `artifacts` (`object`): paths for captured `html`, optional `screenshot`, and per-page `json`.
- `error` (`PageError | null`): structured failure data when navigation or capture partially failed.

## `PageMetadata`

- `url`: requested URL.
- `final_url`: URL after redirects.
- `title`: page title when available.
- `description`: meta description when available.
- `canonical_url`: canonical URL when declared.
- `fetched_at`: UTC timestamp for capture start.
- `status_code`: HTTP status when Playwright receives a response.
- `elapsed_ms`: elapsed capture time.
- `content_length`: captured HTML length in characters.

## `EvidenceSnippet`

- `text`: concise evidence text.
- `score`: snippet-level objective match from `0.0` to `1.0`.
- `matched_terms`: normalized objective terms found in the snippet.
- `source`: evidence origin such as `title`, `heading`, `meta`, or `body`.
- `context_before` / `context_after`: neighboring text for reviewer context.

## `ScoreBreakdown`

- `relevance`: objective/evidence match from `0.0` to `1.0`.
- `credibility`: source trust signals from `0.0` to `1.0`.
- `freshness`: recency signal from `0.0` to `1.0`.
- `confidence`: confidence in scoring completeness from `0.0` to `1.0`.
- `total`: weighted score from `0.0` to `1.0`.
- `reasons`: backward-compatible flat reason list.
- `relevance_reasons`, `credibility_reasons`, `freshness_reasons`: category-specific explanations.

## `PageError`

- `message`: human-readable error.
- `kind`: short category such as `timeout`, `navigation`, `capture`, or `unknown`.
- `recoverable`: whether the run could continue and retry may help.
