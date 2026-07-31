import json
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator

SCHEMA = json.loads(
    (Path(__file__).resolve().parent.parent / "gtme-enrich" / "prospects.schema.json").read_text())
V = Draft202012Validator(SCHEMA)

def errs(record):
    return [e.message for e in V.iter_errors(record)]

# Built from the real record that turned out to be the wrong human.
CURRAN = {
    "account_id": "domain:upgrade.com", "company": "Upgrade",
    "name": "Thomas Curran", "title": "Chief Risk Officer",
    "linkedin": "thomas-curran", "confidence": 0.85,
    "sources": ["https://www.upgrade.com/team/"],
}

def rec(**over):
    return {**CURRAN, **over}

GOOD_IDENTITY = {"pulled": "2026-07-31", "says": "Chief Risk Officer at Upgrade"}


def test_fully_evidenced_verified_record_passes():
    assert errs(rec(record_status="verified", identity=GOOD_IDENTITY,
                    employer_history=["Upgrade"], education=["Boston College"])) == []

def test_absent_record_status_is_rejected():
    assert errs(CURRAN)

def test_verified_without_identity_is_rejected():
    assert errs(rec(record_status="verified",
                    employer_history=["Upgrade"], education=["Boston College"]))

def test_verified_without_employer_history_is_rejected():
    assert errs(rec(record_status="verified", identity=GOOD_IDENTITY,
                    education=["Boston College"]))

def test_verified_with_null_says_is_rejected():
    assert errs(rec(record_status="verified",
                    identity={"pulled": "2026-07-31", "says": None},
                    employer_history=["Upgrade"], education=["Boston College"]))

def test_verified_with_says_shorter_than_a_role_line_is_rejected():
    """A 20-char floor so the person's name alone cannot satisfy it."""
    assert errs(rec(record_status="verified",
                    identity={"pulled": "2026-07-31", "says": "Thomas Curran"},
                    employer_history=["Upgrade"], education=["Boston College"]))

def test_unchecked_carrying_an_identity_is_rejected():
    """A pull date on a profile nobody opened is the ambiguity being removed."""
    assert errs(rec(record_status="unchecked", identity=GOOD_IDENTITY))

def test_unchecked_without_identity_passes():
    assert errs(rec(record_status="unchecked")) == []

def test_empty_byproduct_arrays_pass():
    """Some profiles genuinely list neither. Presence is the check, not content."""
    assert errs(rec(record_status="verified", identity=GOOD_IDENTITY,
                    employer_history=[], education=[])) == []

def test_not_found_with_a_non_null_says_is_rejected():
    assert errs(rec(record_status="not_found", identity=GOOD_IDENTITY))

def test_failure_statuses_may_omit_identity():
    for s in ("wrong_person", "stale", "ambiguous", "not_found"):
        assert errs(rec(record_status=s)) == [], s

def test_wrong_person_may_carry_the_quote_that_proves_the_collision():
    assert errs(rec(record_status="wrong_person", identity=GOOD_IDENTITY)) == []

def test_a_present_identity_may_not_have_a_null_says_except_at_not_found():
    """If a profile loaded, the quote is what makes the status checkable."""
    null_says = {"pulled": "2026-07-31", "says": None}
    for s in ("stale", "wrong_person", "ambiguous"):
        assert errs(rec(record_status=s, identity=null_says)), s
    assert errs(rec(record_status="not_found", identity=null_says)) == []

def test_any_legacy_key_is_rejected():
    """No grandfather clause. An exemption that lets verified skip its evidence
    is the original defect renamed."""
    assert errs(rec(record_status="unchecked", legacy=True))

def test_bad_pull_date_format_is_rejected():
    assert errs(rec(record_status="verified",
                    identity={"pulled": "Jul 2026", "says": "Chief Risk Officer at Upgrade"},
                    employer_history=[], education=[]))

def test_impossible_dates_are_rejected():
    """A bare [0-9]{2} month accepts 2026-99-99, which then reaches gate.py."""
    for bad in ("2026-99-99", "2026-13-01", "2026-00-15", "2026-07-32", "2026-07-00"):
        assert errs(rec(record_status="verified",
                        identity={"pulled": bad, "says": "Chief Risk Officer at Upgrade"},
                        employer_history=[], education=[])), bad

def test_real_dates_still_pass():
    for good in ("2026-01-01", "2026-12-31", "2026-07-15"):
        assert errs(rec(record_status="verified",
                        identity={"pulled": good, "says": "Chief Risk Officer at Upgrade"},
                        employer_history=[], education=[])) == [], good

def test_dates_the_pattern_cannot_disprove_are_left_to_the_gate():
    """2026 is not a leap year, so 2026-02-29 is not a date - but no regex can
    know that. The schema accepts it and gate.py's parse guard catches it. This
    is the case that makes the two date checks non-redundant."""
    assert errs(rec(record_status="verified",
                    identity={"pulled": "2026-02-29", "says": "Chief Risk Officer at Upgrade"},
                    employer_history=[], education=[])) == []
