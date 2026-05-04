#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Demo: vendor compliance research (one of many possible domains)
browser-research-agent research \
  --objective "find SOC 2 audit reporting and vendor risk compliance evidence" \
  --url "file://${REPO_ROOT}/tests/fixtures/vendor_security.html" \
  --url "file://${REPO_ROOT}/tests/fixtures/vendor_blog.html" \
  --url "file://${REPO_ROOT}/tests/fixtures/vendor_careers.html" \
  --out artifacts/example \
  --report markdown

printf '\nReport written to artifacts/example/report.md\n'

# Other example objectives (swap fixtures to match):
#   "identify pricing tiers, target segments, and competitive positioning across these SaaS pages"
#   "extract property details, agent contact info, and listing history for these 15 properties"
#   "find AI automation roles requiring Python, FastAPI, and multi-agent experience"
