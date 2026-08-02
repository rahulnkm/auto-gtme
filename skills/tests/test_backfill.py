"""The backfill's contract, tested against a synthetic file.

An earlier version of these tests copied runs/mousecat/06-enrich/prospects.jsonl
and asserted its exact status counts. That file is live campaign data: once it
was migrated and contacts started getting verified, the assertions broke without
anything being wrong with the code. Tests that read mutable data are flaky by
construction, so the fixture is built here and covers every case by name.
"""
import json, subprocess, sys
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO / "skills" / "backfill_identity.py"

EVIDENCE = {"pulled": "2026-08-02", "says": "Head of Fraud at Acme, Jan 2024 - Present"}

# One row per case the backfill has to distinguish.
ROWS = [
    # no status at all - never checked
    {"name": "No Status", "linkedin": "no-status", "confidence": 0.9},
    # claims verified, carries no evidence - unprovable
    {"name": "Bare Claim", "linkedin": "bare-claim", "record_status": "verified"},
    # claims verified with byproducts but still no identity - still unprovable
    {"name": "Byproducts Only", "linkedin": "byproducts", "record_status": "verified",
     "employer_history": ["Acme"], "education": ["Somewhere"]},
    # genuinely evidenced - must survive untouched
    {"name": "Evidenced", "linkedin": "evidenced", "record_status": "verified",
     "identity": EVIDENCE, "employer_history": ["Acme"], "education": []},
    # already-known failures - untouched, identity optional at these statuses
    {"name": "Ambiguous", "linkedin": "amb", "record_status": "ambiguous"},
    {"name": "Stale", "linkedin": "stale", "record_status": "stale"},
    {"name": "Wrong", "linkedin": "wrong", "record_status": "wrong_person"},
    # already migrated - the idempotence case
    {"name": "Already", "linkedin": "already", "record_status": "unchecked"},
    # non-ASCII must survive the rewrite as itself
    {"name": "Aistė Stakauskaitė", "linkedin": "aiste", "confidence": 0.8},
]


@pytest.fixture
def run_dir(tmp_path):
    d = tmp_path / "enrich"
    d.mkdir()
    with (d / "prospects.jsonl").open("w") as f:
        for r in ROWS:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return tmp_path


def load(run_dir):
    return [json.loads(l) for l in (run_dir / "enrich" / "prospects.jsonl").open() if l.strip()]


def backfill(run_dir):
    return subprocess.run([sys.executable, str(SCRIPT), str(run_dir)],
                          capture_output=True, text=True, check=True)


def by_slug(rows):
    return {r["linkedin"]: r for r in rows}


def test_downgrades_exactly_what_cannot_be_proven(run_dir):
    backfill(run_dir)
    got = {k: v["record_status"] for k, v in by_slug(load(run_dir)).items()}
    assert got == {
        "no-status":  "unchecked",     # never had a status
        "bare-claim": "unchecked",     # claimed verified, no evidence
        "byproducts": "unchecked",     # byproducts are not proof of a visit
        "evidenced":  "verified",      # the only survivor
        "amb":        "ambiguous",     # failure statuses are left alone
        "stale":      "stale",
        "wrong":      "wrong_person",
        "already":    "unchecked",
        "aiste":      "unchecked",
    }


def test_only_record_status_changes(run_dir):
    before = load(run_dir)
    backfill(run_dir)
    after = load(run_dir)
    assert len(before) == len(after)
    for b, a in zip(before, after):
        assert {k: v for k, v in a.items() if k != "record_status"} == \
               {k: v for k, v in b.items() if k != "record_status"}


def test_no_identity_is_invented(run_dir):
    """A pull date copied off another field is not a record of a visit. The only
    identity in the output must be the one that was already there."""
    backfill(run_dir)
    carriers = {r["linkedin"] for r in load(run_dir) if "identity" in r}
    assert carriers == {"evidenced"}


def test_evidenced_records_survive_untouched(run_dir):
    backfill(run_dir)
    kept = by_slug(load(run_dir))["evidenced"]
    assert kept["record_status"] == "verified"
    assert kept["identity"] == EVIDENCE


def test_is_idempotent(run_dir):
    backfill(run_dir)
    once = load(run_dir)
    second = backfill(run_dir)
    assert load(run_dir) == once
    assert "0 of 9" in second.stdout


def test_non_ascii_names_survive_the_rewrite(run_dir):
    backfill(run_dir)
    assert by_slug(load(run_dir))["aiste"]["name"] == "Aistė Stakauskaitė"
    raw = (run_dir / "enrich" / "prospects.jsonl").read_text()
    assert "Aistė" in raw          # written as itself, not \\u escapes
