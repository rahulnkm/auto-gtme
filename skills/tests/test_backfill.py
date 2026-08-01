import json, shutil, subprocess, sys
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO / "skills" / "backfill_identity.py"

@pytest.fixture
def run_dir(tmp_path):
    src = REPO / "runs" / "mousecat" / "enrich" / "prospects.jsonl"
    dst = tmp_path / "enrich"
    dst.mkdir()
    shutil.copy(src, dst / "prospects.jsonl")
    return tmp_path

def load(run_dir):
    return [json.loads(l) for l in (run_dir / "enrich" / "prospects.jsonl").open() if l.strip()]

def backfill(run_dir):
    return subprocess.run([sys.executable, str(SCRIPT), str(run_dir)],
                          capture_output=True, text=True, check=True)

def test_status_counts_after_migration(run_dir):
    backfill(run_dir)
    counts = {}
    for r in load(run_dir):
        counts[r["record_status"]] = counts.get(r["record_status"], 0) + 1
    assert counts == {"unchecked": 299, "ambiguous": 11, "stale": 3, "wrong_person": 1}

def test_only_record_status_changes(run_dir):
    before = load(run_dir)
    backfill(run_dir)
    after = load(run_dir)
    assert len(before) == len(after)
    for b, a in zip(before, after):
        assert {k: v for k, v in a.items() if k != "record_status"} == \
               {k: v for k, v in b.items() if k != "record_status"}

def test_no_identity_is_invented(run_dir):
    backfill(run_dir)
    assert not any("identity" in r for r in load(run_dir))

def test_is_idempotent(run_dir):
    backfill(run_dir)
    once = load(run_dir)
    second = backfill(run_dir)
    assert load(run_dir) == once
    assert "0 of 314" in second.stdout
