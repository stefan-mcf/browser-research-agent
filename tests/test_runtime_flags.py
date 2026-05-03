from browser_research_agent.agent import _truthy_env


def test_truthy_env_accepts_common_enabled_values(monkeypatch):
    for value in ["1", "true", "yes", "on", "TRUE"]:
        monkeypatch.setenv("BROWSER_RESEARCH_AGENT_NO_SANDBOX", value)
        assert _truthy_env("BROWSER_RESEARCH_AGENT_NO_SANDBOX") is True


def test_truthy_env_rejects_disabled_or_missing_values(monkeypatch):
    for value in ["0", "false", "no", "off", ""]:
        monkeypatch.setenv("BROWSER_RESEARCH_AGENT_NO_SANDBOX", value)
        assert _truthy_env("BROWSER_RESEARCH_AGENT_NO_SANDBOX") is False

    monkeypatch.delenv("BROWSER_RESEARCH_AGENT_NO_SANDBOX", raising=False)
    assert _truthy_env("BROWSER_RESEARCH_AGENT_NO_SANDBOX") is False
