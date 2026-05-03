# Browser Research Report

Objective: find SOC 2 audit reporting and vendor risk compliance evidence
Created at: 2026-05-03T01:41:39.253947+00:00

## Executive summary

Captured pages: 3
Strong candidates: 1
Review candidates: 1
Weak candidates: 1

## Ranked findings

### 1. Acme TrustHub Security and Compliance

- URL: demo://acme-trusthub/security
- Total score: 0.7550
- Relevance: 1.0000
- Credibility: 0.3000
- Freshness: 1.0000
- Artifacts:
  - html: `examples/sample-output/pages/01-unknown-url-98e34481.html`
  - json: `examples/sample-output/pages/01-unknown-url-98e34481.json`
  - screenshot: `examples/sample-output/pages/01-unknown-url-98e34481.png`
- Why it scored this way:
  - Matched objective terms: audit, compliance, report, risk, soc, vendor
  - Extracted 8 evidence snippets
  - Credibility signals: about, compliance, documentation, report, security
  - Newest detected date: 2026-05-03

Evidence:
- (1.00; audit, report, risk, soc, vendor) SOC 2, ISO 27001, vendor risk, and audit reporting evidence for enterprise buyers.
- (0.99; audit, report, risk, soc, vendor) Acme TrustHub publishes SOC 2 Type II controls, ISO 27001 policy coverage, and vendor risk documentation for procurement teams. The trust center includes audit reports, encryption details, uptime history, subprocessors, and data processing commitments updated in 2026.
- (0.82; audit, compliance, report, vendor) The trust center includes audit reports, encryption details, uptime history, subprocessors, and data processing commitments updated in 2026. Security reviewers can export compliance evidence for board reporting, customer questionnaires, and vendor due diligence workflows.
- (0.76; risk, soc, vendor) Acme TrustHub publishes SOC 2 Type II controls, ISO 27001 policy coverage, and vendor risk documentation for procurement teams.
- (0.76; compliance, report, vendor) Security reviewers can export compliance evidence for board reporting, customer questionnaires, and vendor due diligence workflows.

### 2. Acme TrustHub Product Blog

- URL: demo://acme-trusthub/blog/product-update
- Total score: 0.6117
- Relevance: 0.9083
- Credibility: 0.3000
- Freshness: 0.3500
- Artifacts:
  - html: `examples/sample-output/pages/02-unknown-url-b1add7b5.html`
  - json: `examples/sample-output/pages/02-unknown-url-b1add7b5.json`
  - screenshot: `examples/sample-output/pages/02-unknown-url-b1add7b5.png`
- Why it scored this way:
  - Matched objective terms: audit, compliance, report, soc, vendor
  - Extracted 5 evidence snippets
  - Credibility signals: compliance, customers, documentation, report, security
  - No explicit freshness date found

Evidence:
- (1.00; audit, compliance, report, soc, vendor) Acme TrustHub added onboarding checklists for procurement teams and a dashboard for vendor documentation requests. The update mentions compliance workflows, customer questionnaires, and report exports, but it does not provide SOC 2 audit evidence.
- (0.95; audit, compliance, report, soc) The update mentions compliance workflows, customer questionnaires, and report exports, but it does not provide SOC 2 audit evidence.
- (0.83; audit, compliance, report, soc) The update mentions compliance workflows, customer questionnaires, and report exports, but it does not provide SOC 2 audit evidence. Customers can use the checklist to prepare security review materials before sending them to enterprise buyers.
- (0.38; compliance) A product update mentioning compliance workflows and customer onboarding improvements.
- (0.36; vendor) Acme TrustHub added onboarding checklists for procurement teams and a dashboard for vendor documentation requests.

### 3. Acme TrustHub Careers

- URL: demo://acme-trusthub/careers
- Total score: 0.0735
- Relevance: 0.0000
- Credibility: 0.0600
- Freshness: 0.3500
- Artifacts:
  - html: `examples/sample-output/pages/03-unknown-url-a25f56ca.html`
  - json: `examples/sample-output/pages/03-unknown-url-a25f56ca.json`
  - screenshot: `examples/sample-output/pages/03-unknown-url-a25f56ca.png`
- Why it scored this way:
  - Credibility signals: report
  - No explicit freshness date found

Evidence: none extracted.

## Methodology

This report was generated from captured browser artifacts: page HTML, optional screenshot evidence, extracted metadata, links, and objective-matching snippets.
Each page is scored deterministically so reviewers can inspect the evidence instead of trusting an opaque summary.

## Limitations

Scores are research triage signals, not final judgments. Review screenshots, HTML, and snippets before making business decisions.
The MVP does not perform login automation, CAPTCHA bypass, paywall bypass, search discovery, or LLM synthesis by default.

## Scoring rubric

Total score = 50% relevance + 35% credibility + 15% freshness.
Scores rank captured evidence and should be reviewed alongside screenshots and HTML artifacts.
See `docs/scoring-rubric.md` for the full scoring explanation.
