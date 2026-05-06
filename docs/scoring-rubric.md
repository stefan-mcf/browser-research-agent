# Scoring Rubric

Browser Research Agent uses a clear scoring system so users can understand how sources are ranked.

## Weights

- Relevance: `0.50`
  - Coverage of key terms in the title, description, and visible page text.
  - Quantity and quality of extracted evidence snippets.
- Credibility: `0.35`
  - HTTPS availability.
  - High-trust public-interest TLDs such as `.gov` and `.edu`.
  - Indicators of trustworthiness, such as security, compliance, privacy, terms of service, documentation, reports, citations, customer references, and case studies.
  - Distinct outbound reference domains.
- Freshness: `0.15`
  - Newest detected year or date in the first captured page text.
  - If no explicit date is found, a neutral-low score is assigned instead of zero.

## Interpretation bands

- Strong candidate: `>= 0.72`
- Review candidate: `>= 0.45` and `< 0.72`
- Weak candidate: `< 0.45`

## Important limitations

- The score reflects the relevance and credibility of captured evidence; it does not guarantee that a claim is true.
- Domain and text analysis methods are designed to be conservative and verifiable.
- Any AI-generated synthesis should cite captured evidence rather than replace this scoring system.
