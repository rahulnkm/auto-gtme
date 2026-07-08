import json
from click.testing import CliRunner
from gtme_linkedin import cli


class SpySession:
    connected = []
    messaged = []
    def __init__(self, *a, **k): pass
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def connect(self, username, note=None):
        SpySession.connected.append((username, note))
        return {"status": "pending", "url": username}
    def send_message(self, username, body, *, confirm_send=False):
        SpySession.messaged.append((username, body, confirm_send))
        return {"status": "sent", "url": username}


def test_connect_dry_run_does_not_call_adapter(monkeypatch):
    SpySession.connected = []
    monkeypatch.setattr(cli, "LinkedInSession", SpySession)
    r = CliRunner().invoke(cli.main, ["person", "connect", "alice", "--note", "hi"])
    assert r.exit_code == 0
    body = json.loads(r.output)
    assert body == {"action": "connect", "target": "alice", "note": "hi", "would_send": True}
    assert SpySession.connected == []  # nothing sent


def test_connect_send_calls_adapter(monkeypatch):
    SpySession.connected = []
    monkeypatch.setattr(cli, "LinkedInSession", SpySession)
    r = CliRunner().invoke(cli.main, ["person", "connect", "alice", "--note", "hi", "--send"])
    assert r.exit_code == 0
    assert SpySession.connected == [("alice", "hi")]
    assert json.loads(r.output)["status"] == "pending"


def test_message_dry_run_does_not_call_adapter(monkeypatch):
    SpySession.messaged = []
    monkeypatch.setattr(cli, "LinkedInSession", SpySession)
    r = CliRunner().invoke(cli.main, ["message", "send", "alice", "--body", "yo"])
    assert r.exit_code == 0
    body = json.loads(r.output)
    assert body == {"action": "send_message", "target": "alice", "body": "yo", "would_send": True}
    assert SpySession.messaged == []  # nothing sent


def test_message_send_passes_confirm_true(monkeypatch):
    SpySession.messaged = []
    monkeypatch.setattr(cli, "LinkedInSession", SpySession)
    r = CliRunner().invoke(cli.main, ["message", "send", "alice", "--body", "yo", "--send"])
    assert r.exit_code == 0
    assert SpySession.messaged == [("alice", "yo", True)]   # confirm_send MUST be True
    assert json.loads(r.output)["status"] == "sent"
