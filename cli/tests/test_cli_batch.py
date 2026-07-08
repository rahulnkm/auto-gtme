import json
from pathlib import Path
from click.testing import CliRunner
from gtme_linkedin import cli


class FakeSession:
    def __init__(self, *a, **k): pass
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def get_person(self, username, sections=None):
        return {"url": username}


def test_batch_writes_jsonl_file_and_pointer(monkeypatch, tmp_path):
    monkeypatch.setattr(cli, "LinkedInSession", FakeSession)
    out = tmp_path / "p.jsonl"
    r = CliRunner().invoke(
        cli.main, ["person", "get", "--batch", "-", "--out", str(out)],
        input="alice\nbob\n",
    )
    assert r.exit_code == 0
    pointer = json.loads(r.output)
    assert pointer == {"written": str(out), "count": 2}
    lines = [json.loads(x) for x in Path(out).read_text().splitlines()]
    assert [d["url"] for d in lines] == ["alice", "bob"]


def test_batch_stdout_flag_inlines_jsonl(monkeypatch):
    monkeypatch.setattr(cli, "LinkedInSession", FakeSession)
    r = CliRunner().invoke(
        cli.main, ["person", "get", "--batch", "-", "--stdout"], input="alice\nbob\n",
    )
    assert r.exit_code == 0
    urls = [json.loads(x)["url"] for x in r.output.splitlines()]
    assert urls == ["alice", "bob"]
