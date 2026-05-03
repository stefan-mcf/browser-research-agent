# Scoring Rubric

Browser Research Agent uses a transparent deterministic rubric so clients can inspect why a source ranked highly.

## Weights

- Relevance: `0.50`
  - Objective term coverage across title, description, and visible page text.
  - Density and quality of extracted evidence snippets.
- Credibility: `0.35`
  - HTTPS availability.
  - High-trust public-interest TLDs such as `.gov` and `.edu`.
  - Trust signals such as security, compliance, privacy, terms, documentation, reports, citations, customers, and case studies.
  - Distinct outbound reference domains.
- Freshness: `0.15`
  - Newest detected year or date in the first captured page text.
  - No explicit date receives a neutral-low score rather than a hard zero.

## Interpretation bands

- Strong candidate: `>= 0.72`
- Review candidate: `>= 0.45` and `< 0.72`
- Weak candidate: `< 0.45`

## Important limitations

- The score ranks captured evidence; it is not a guarantee that a claim is true.
- Domain and text heuristics are intentionally conservative and auditable.
- LLM synthesis, if added later, should cite captured evidence rather than replace the rubric.
