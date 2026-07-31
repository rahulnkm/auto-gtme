import datetime
import pytest
from gate import send_gate

AS_OF = datetime.date(2026, 7, 31)
FRESH = {"pulled": "2026-07-25", "says": "Chief Risk Officer at Upgrade"}


def test_absent_status_with_high_confidence_does_not_reach_ready():
    """The regression this whole change exists to prevent. A record nobody
    checked must never be indistinguishable from one that passed."""
    record = {"confidence": 0.85, "identity": FRESH}
    assert send_gate(record, AS_OF) == "verify_first"


STALE_PULL = {"pulled": "2026-06-01", "says": "Chief Risk Officer at Upgrade"}
BOUNDARY = {"pulled": "2026-07-01", "says": "Chief Risk Officer at Upgrade"}  # exactly 30 days

@pytest.mark.parametrize("status,conf,expected", [
    # blocked outright, confidence irrelevant
    ("not_found",    0.9, "do_not_send"),
    ("wrong_person", 0.9, "do_not_send"),
    ("stale",        0.9, "do_not_send"),
    # unproven, confidence irrelevant
    ("ambiguous",    0.9, "verify_first"),
    ("unchecked",    0.9, "verify_first"),
    (None,           0.9, "verify_first"),
    # the only path to ready
    ("verified",     0.9, "ready"),
    # confidence floor still applies to a verified record
    ("verified",     0.6, "verify_first"),
])
def test_truth_table(status, conf, expected):
    record = {"confidence": conf, "identity": FRESH}
    if status is not None:
        record["record_status"] = status
    assert send_gate(record, AS_OF) == expected


def test_stale_verified_downgrades_but_never_blocks():
    """Age is weaker evidence, not counter-evidence."""
    record = {"record_status": "verified", "confidence": 0.9, "identity": STALE_PULL}
    assert send_gate(record, AS_OF) == "verify_first"


def test_threshold_boundary_day_is_inside():
    """Exactly max_age_days old is still fresh; one day more is not."""
    record = {"record_status": "verified", "confidence": 0.9, "identity": BOUNDARY}
    assert send_gate(record, AS_OF, max_age_days=30) == "ready"
    assert send_gate(record, AS_OF, max_age_days=29) == "verify_first"


def test_custom_threshold_is_honored():
    record = {"record_status": "verified", "confidence": 0.9, "identity": STALE_PULL}
    assert send_gate(record, AS_OF, max_age_days=90) == "ready"


# --- inputs the schema forbids, which the gate must still survive ---

def test_verified_without_identity_does_not_reach_ready():
    """Schema-illegal. Only reachable if something bypassed validation, which is
    precisely what a second defense is for."""
    record = {"record_status": "verified", "confidence": 0.9}
    assert send_gate(record, AS_OF) == "verify_first"


def test_unchecked_carrying_an_identity_is_handled():
    """Schema-illegal in the other direction. Must not crash, must not pass."""
    record = {"record_status": "unchecked", "confidence": 0.9, "identity": FRESH}
    assert send_gate(record, AS_OF) == "verify_first"


def test_missing_confidence_is_treated_as_zero():
    record = {"record_status": "verified", "identity": FRESH}
    assert send_gate(record, AS_OF) == "verify_first"


# --- threshold resolution from icp.scoring ---
# This is the first code that reads icp.scoring at all, so nothing else covers it.

def test_threshold_defaults_when_icp_omits_the_key():
    from gate import max_age_from_icp, DEFAULT_MAX_AGE_DAYS
    assert max_age_from_icp({"scoring": {"weight_signals_over_firmographics": True}}) \
        == DEFAULT_MAX_AGE_DAYS

def test_threshold_defaults_when_icp_has_no_scoring_block():
    from gate import max_age_from_icp, DEFAULT_MAX_AGE_DAYS
    assert max_age_from_icp({}) == DEFAULT_MAX_AGE_DAYS
    assert max_age_from_icp({"scoring": None}) == DEFAULT_MAX_AGE_DAYS

def test_threshold_is_read_from_icp_when_set():
    from gate import max_age_from_icp
    assert max_age_from_icp({"scoring": {"identity_max_age_days": 90}}) == 90


# --- the gate is an allowlist, not a denylist ---
# Enumerating bad values and letting the rest through is the original defect in
# miniature. These would all have reached "ready" before the allowlist fix.

@pytest.mark.parametrize("status", [
    "Verified", "VERIFIED", "verifed", "confirmed", "", True, 1, ["verified"],
])
def test_unrecognized_status_never_reaches_ready(status):
    record = {"record_status": status, "confidence": 0.9, "identity": FRESH}
    assert send_gate(record, AS_OF) == "verify_first"


# --- unreadable pull dates degrade instead of crashing ---
# "2026-02-31" matches the schema pattern and is still not a date, so a run can
# meet the schema and still hit this. One bad row must not kill the campaign.

@pytest.mark.parametrize("pulled", [
    "2026-99-99", "2026-02-31", "2026-13-01", "0000-00-00", "", 20260731, None, [],
])
def test_unreadable_pull_date_is_stale_not_an_exception(pulled):
    record = {"record_status": "verified", "confidence": 0.9,
              "identity": {"pulled": pulled, "says": "Chief Risk Officer at Upgrade"}}
    assert send_gate(record, AS_OF) == "verify_first"


def test_a_future_pull_date_is_stale():
    """A date we cannot have pulled yet is not fresher than one we did."""
    record = {"record_status": "verified", "confidence": 0.9,
              "identity": {"pulled": "2030-01-01", "says": "Chief Risk Officer at Upgrade"}}
    assert send_gate(record, AS_OF) == "verify_first"


def test_a_malformed_identity_does_not_crash():
    """Schema-illegal shapes. The gate's job is surviving unvalidated input."""
    for identity in ("2026-07-31", ["2026-07-31"], 7, None):
        record = {"record_status": "verified", "confidence": 0.9, "identity": identity}
        assert send_gate(record, AS_OF) == "verify_first", identity
