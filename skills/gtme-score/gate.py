#!/usr/bin/env python3
"""The send gate, extracted from score.py so it can be tested in isolation.

This is the SECOND of two defenses against an unverified identity reaching
outreach; the first is prospects.schema.json. It therefore must behave correctly
on records the schema would have rejected - a record written by a tool that
skipped validation is exactly the case it exists to catch. Do not assume the
input is schema-valid.
"""
import datetime

BLOCKED = ("not_found", "wrong_person", "stale")
VERIFIED = "verified"
MIN_CONFIDENCE = 0.7
DEFAULT_MAX_AGE_DAYS = 30


def max_age_from_icp(icp):
    """Recency tolerance is a per-campaign judgment, not part of the fixed
    formula, so it lives in icp.scoring rather than in score.py's constants.

    Extracted here rather than inlined in score.py because score.py executes its
    whole pipeline at import time and cannot be unit tested.
    """
    return (icp.get("scoring") or {}).get("identity_max_age_days", DEFAULT_MAX_AGE_DAYS)


def send_gate(record, as_of, max_age_days=DEFAULT_MAX_AGE_DAYS):
    """ready | verify_first | do_not_send.

    An identity nobody checked is not a ranking problem, it is a send problem.

    "ready" is an ALLOWLIST of exactly one status. Enumerating the bad values and
    letting the rest through is the original defect in miniature: it makes the
    set of things that pass depend on the set someone remembered to name. A
    typo'd "verifed", a capitalised "Verified", or a status a future change adds
    to the schema's enum would all sail through a denylist, and the schema's enum
    would be the only thing stopping them - which would make these two defenses
    one defense wearing two hats.
    """
    status = record.get("record_status")
    if status in BLOCKED:
        return "do_not_send"
    if status != VERIFIED or (record.get("confidence") or 0.0) < MIN_CONFIDENCE:
        return "verify_first"
    if _stale(record, as_of, max_age_days):
        return "verify_first"
    return "ready"


def _stale(record, as_of, max_age_days):
    """A verified identity is a claim about a moment; people change jobs.

    Anything that is not a readable date in the window counts as stale: absent,
    wrong type, malformed, or in the future. The schema forbids `verified`
    without a well-formed `pulled`, so most of these mean validation was
    bypassed - but "2026-02-31" matches the schema's pattern and is still not a
    date, so this is not purely a bypass guard. The safe reading of anything
    unreadable is "we do not know when", and a run must not die on one bad row.
    """
    try:
        age = (as_of - datetime.date.fromisoformat(record["identity"]["pulled"])).days
    except (KeyError, TypeError, ValueError):
        return True
    return not 0 <= age <= max_age_days
