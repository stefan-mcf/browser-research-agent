from __future__ import annotations

import asyncio
import html
import json
import re
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "screenshots"
REPORT = ROOT / "examples" / "sample-output" / "report.md"
API_JSON = Path("/tmp/browser-research-agent-api-response.json")
QUALITY = Path("/tmp/browser-research-agent-quality-gates.txt")


def sanitize(text: str) -> str:
    text = text.replace(str(ROOT), "<repo>")
    text = re.sub(r"/Users/[^/\s]+/", "/Users/<user>/", text)
    return text


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    body: list[str] = []
    in_list = False
    for raw in lines:
        line = raw.rstrip()
        if not line:
            if in_list:
                body.append("</ul>")
                in_list = False
            body.append("<br>")
            continue
        if line.startswith("#"):
            if in_list:
                body.append("</ul>")
                in_list = False
            level = min(len(line) - len(line.lstrip("#")), 3)
            text = html.escape(line[level:].strip())
            body.append(f"<h{level}>{text}</h{level}>")
        elif line.startswith("- "):
            if not in_list:
                body.append("<ul>")
                in_list = True
            body.append(f"<li>{html.escape(line[2:])}</li>")
        else:
            if in_list:
                body.append("</ul>")
                in_list = False
            body.append(f"<p>{html.escape(line)}</p>")
    if in_list:
        body.append("</ul>")
    return "\n".join(body)


def write_html(path: Path, title: str, body: str, *, mono: bool = False) -> None:
    font = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" if mono else "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    path.write_text(
        f"""<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{ margin: 0; background: #0b1020; color: #e5ecff; font-family: {font}; }}
    .frame {{ max-width: 1120px; margin: 0 auto; padding: 42px; }}
    .card {{ background: linear-gradient(180deg, #111936 0%, #0f172a 100%); border: 1px solid #263456; border-radius: 22px; padding: 34px; box-shadow: 0 24px 80px rgba(0,0,0,.35); }}
    .eyebrow {{ color: #8bd5ff; text-transform: uppercase; letter-spacing: .15em; font-size: 12px; font-weight: 700; margin-bottom: 10px; }}
    h1 {{ margin: 0 0 18px; font-size: 34px; line-height: 1.1; }}
    h2 {{ color: #c7d2fe; margin-top: 30px; }}
    h3 {{ color: #bae6fd; margin-top: 22px; }}
    p, li {{ color: #d8e1ff; font-size: 16px; line-height: 1.55; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; color: #d9f99d; background: #050816; border: 1px solid #22304f; border-radius: 16px; padding: 22px; font-size: 14px; line-height: 1.45; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }}
    .shot {{ background: #080d1d; border: 1px solid #263456; border-radius: 16px; padding: 14px; }}
    .shot img {{ width: 100%; border-radius: 10px; border: 1px solid #334155; display: block; }}
    .shot h3 {{ margin: 12px 0 4px; font-size: 16px; }}
    .muted {{ color: #94a3b8; font-size: 14px; }}
  </style>
</head>
<body><main class=\"frame\"><section class=\"card\"><div class=\"eyebrow\">Browser Research Agent evidence</div>{body}</section></main></body>
</html>
""",
        encoding="utf-8",
    )


async def screenshot_file(page, html_path: Path, png_path: Path, *, full_page: bool = True) -> None:
    await page.goto(html_path.as_uri(), wait_until="networkidle")
    await page.screenshot(path=str(png_path), full_page=full_page)


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    api_data = json.loads(API_JSON.read_text(encoding="utf-8"))
    sanitized_api = sanitize(json.dumps(api_data, indent=2))
    quality = sanitize(QUALITY.read_text(encoding="utf-8"))
    report_html = markdown_to_html(sanitize(REPORT.read_text(encoding="utf-8")))

    report_page = OUT / "source-sample-report.html"
    api_page = OUT / "source-api-json-response.html"
    quality_page = OUT / "source-quality-gates.html"

    write_html(report_page, "Sample Markdown report", f"<h1>Sample generated research report</h1>{report_html}")
    write_html(api_page, "API JSON response", "<h1>Local FastAPI response proof</h1><pre>" + html.escape(sanitized_api) + "</pre>", mono=True)
    write_html(quality_page, "Quality gates", "<h1>Quality gates passed locally</h1><pre>" + html.escape(quality) + "</pre>", mono=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 1050}, device_scale_factor=1)

        await page.goto("http://127.0.0.1:8012/docs", wait_until="networkidle")
        await page.screenshot(path=str(OUT / "01-openapi-docs.png"), full_page=True)

        await screenshot_file(page, report_page, OUT / "02-sample-report.png")
        await screenshot_file(page, api_page, OUT / "03-api-json-response.png")
        await screenshot_file(page, quality_page, OUT / "04-quality-gates.png")

        await browser.close()

    print(f"wrote screenshots to {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
