#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

browser-research-agent research \
  --objective "find SOC 2 audit reporting and vendor risk compliance evidence" \
  --url "file://${REPO_ROOT}/tests/fixtures/vendor_security.html" \
  --url "file://${REPO_ROOT}/tests/fixtures/vendor_blog.html" \
  --url "file://${REPO_ROOT}/tests/fixtures/vendor_careers.html" \
  --out artifacts/demo \
  --report markdown

printf '\nReport written to artifacts/demo/report.md\n'
