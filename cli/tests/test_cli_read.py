import json
import pytest
from click.testing import CliRunner
from gtme_linkedin import cli
from gtme_linkedin.errors import GtmeError, EXIT_AUTH


class FakeSession:
    def __init__(self, *a, **k): pass
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def get_person(self, username, sections=None):
        return {"url": f"linkedin.com/in/{username}", "sections": {"main": "..."}}


def test_person_get_single_prints_json_to_stdout(monkeypatch):
    monkeypatch.setattr(cli, "LinkedInSession", FakeSession)
    r = CliRunner().invoke(cli.main, ["person", "get", "williamhgates"])
    assert r.exit_code == 0
    assert json.loads(r.output)["url"] == "linkedin.com/in/williamhgates"


def test_auth_error_writes_stderr_and_exits_4(monkeypatch):
    class AuthFail(FakeSession):
        def __enter__(self):
            raise GtmeError(EXIT_AUTH, "auth_required", suggestion="run `gtme-linkedin auth login`")
    monkeypatch.setattr(cli, "LinkedInSession", AuthFail)
    # Click 8.2+ separates stderr by default; no mix_stderr kwarg needed
    r = CliRunner().invoke(cli.main, ["person", "get", "x"])
    assert r.exit_code == 4
    assert json.loads(r.stderr)["error"] == "auth_required"


class FakeSession2(FakeSession):
    def sidebar(self, username): return {"username": username, "sidebar_profiles": {}}
    def inbox(self, limit=20): return {"threads": [], "limit": limit}
    def search_people(self, keywords, *, location=None, network=None, company=None):
        return {"keywords": keywords, "location": location, "network": network, "company": company}


def test_person_sidebar_single(monkeypatch):
    monkeypatch.setattr(cli, "LinkedInSession", FakeSession2)
    r = CliRunner().invoke(cli.main, ["person", "sidebar", "alice"])
    assert r.exit_code == 0 and json.loads(r.output)["username"] == "alice"


def test_inbox_list(monkeypatch):
    monkeypatch.setattr(cli, "LinkedInSession", FakeSession2)
    r = CliRunner().invoke(cli.main, ["inbox", "list", "--limit", "5"])
    assert r.exit_code == 0 and json.loads(r.output)["limit"] == 5


def test_person_search_splits_network(monkeypatch):
    monkeypatch.setattr(cli, "LinkedInSession", FakeSession2)
    r = CliRunner().invoke(cli.main, ["person", "search", "growth", "--network", "F,S", "--location", "NYC"])
    assert r.exit_code == 0
    body = json.loads(r.output)
    assert body["network"] == ["F", "S"]
    assert body["location"] == "NYC"


# ---------------------------------------------------------------------------
# Auth status unit tests (no network, monkeypatched adapter)
# ---------------------------------------------------------------------------

def test_auth_status_authenticated(monkeypatch):
    monkeypatch.setattr(cli.adapter, "auth_status", lambda: {"authenticated": True})
    r = CliRunner().invoke(cli.main, ["auth", "status"])
    assert r.exit_code == 0
    assert json.loads(r.output) == {"authenticated": True}


def test_auth_status_unauthenticated(monkeypatch):
    monkeypatch.setattr(cli.adapter, "auth_status",
                        lambda: {"authenticated": False, "suggestion": "run `gtme-linkedin auth login`"})
    r = CliRunner().invoke(cli.main, ["auth", "status"])
    assert r.exit_code == 0
    body = json.loads(r.output)
    assert body["authenticated"] is False
    assert "suggestion" in body
