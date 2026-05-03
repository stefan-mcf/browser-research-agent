# Browser Research Report

Objective: find SOC 2 audit reporting and vendor risk compliance evidence
Created at: 2026-05-03T04:47:30.510367+00:00

## Executive summary

Captured pages: 3
Strong candidates: 1
Review candidates: 1
Weak candidates: 1

## Ranked findings

### 1. Acme TrustHub Security and Compliance

- URL: file://tests/fixtures/vendor_security.html
- Total score: 0.7550
- Relevance: 1.0000
- Credibility: 0.3000
- Freshness: 1.0000
- Artifacts:
  - html: `examples/sample-output/pages/01-vendor-security-117298b5.html`
  - json: `examples/sample-output/pages/01-vendor-security-117298b5.json`
  - screenshot: `examples/sample-output/pages/01-vendor-security-117298b5.png`
- Scoring rationale:
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

- URL: file://tests/fixtures/vendor_blog.html
- Total score: 0.6117
- Relevance: 0.9083
- Credibility: 0.3000
- Freshness: 0.3500
- Artifacts:
  - html: `examples/sample-output/pages/02-vendor-blog-0da05732.html`
  - json: `examples/sample-output/pages/02-vendor-blog-0da05732.json`
  - screenshot: `examples/sample-output/pages/02-vendor-blog-0da05732.png`
- Scoring rationale:
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

- URL: file://tests/fixtures/vendor_careers.html
- Total score: 0.0735
- Relevance: 0.0000
- Credibility: 0.0600
- Freshness: 0.3500
- Artifacts:
  - html: `examples/sample-output/pages/03-vendor-careers-b45230f2.html`
  - json: `examples/sample-output/pages/03-vendor-careers-b45230f2.json`
  - screenshot: `examples/sample-output/pages/03-vendor-careers-b45230f2.png`
- Scoring rationale:
  - Credibility signals: report
  - No explicit freshness date found

Evidence: none extracted.

## How this report was generated

This report was generated using data captured from web pages, including HTML, optional screenshots, extracted metadata, links, and snippets matching the research objective.
Each page is scored with a consistent system so users can examine the evidence directly rather than relying on a generic summary.

## Limitations

Scores help prioritize research review; they are not final judgments. Review screenshots, HTML, and extracted snippets before making business decisions.
The system does not perform login automation, CAPTCHA bypass, paywall bypass, search discovery, or AI-generated synthesis by default.

## Scoring rubric

Total score = 50% relevance + 35% credibility + 15% freshness.
Scores indicate the relevance of captured evidence and should be reviewed alongside screenshots and captured HTML.
See `docs/scoring-rubric.md` for the full scoring explanation.
