from pathlib import Path
import shutil

from fastapi.testclient import TestClient

from browser_research_agent.api import app


client = TestClient(app)


def fixture_url(name: str) -> str:
    return f"file://{(Path(__file__).parent / 'fixtures' / name).resolve()}"


def test_health_endpoint_reports_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_research_endpoint_rejects_empty_url_list() -> None:
    response = client.post(
        "/research",
        json={"objective": "find SOC 2 compliance evidence", "urls": []},
    )

    assert response.status_code == 422


def test_research_endpoint_runs_fixture_backed_research() -> None:
    out_dir = Path("artifacts/test-api-relative")
    shutil.rmtree(out_dir, ignore_errors=True)
    response = client.post(
        "/research",
        json={
            "objective": "find SOC 2 audit reporting and vendor risk compliance evidence",
            "urls": [fixture_url("vendor_security.html"), fixture_url("vendor_blog.html")],
            "out_dir": str(out_dir),
            "include_screenshots": False,
            "timeout_ms": 10_000,
            "report": "markdown",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["objective"] == "find SOC 2 audit reporting and vendor risk compliance evidence"
    assert body["page_count"] == 2
    assert body["strong_candidates"] == 1
    assert body["summary_path"].endswith("summary.json")
    assert body["report_path"].endswith("report.md")
    assert Path(body["summary_path"]).exists()
    assert Path(body["report_path"]).exists()
    assert Path(body["pages"][0]["artifact_paths"]["html"]).is_absolute()
    assert Path(body["pages"][0]["artifact_paths"]["html"]).exists()
    assert body["pages"][0]["title"] == "Acme TrustHub Security and Compliance"
    assert body["pages"][0]["total_score"] > body["pages"][1]["total_score"]
