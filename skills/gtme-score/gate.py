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
UNPROVEN = ("ambiguous", "unchecked", None)
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
    Absence fails closed: an unknown status can never produce "ready".
    """
    status = record.get("record_status")
    if status in BLOCKED:
        return "do_not_send"
    if status in UNPROVEN or (record.get("confidence") or 0.0) < MIN_CONFIDENCE:
        return "verify_first"
    if _stale(record, as_of, max_age_days):
        return "verify_first"
    return "ready"


def _stale(record, as_of, max_age_days):
    """A verified identity is a claim about a moment; people change jobs.

    No pull date counts as stale rather than fresh. The schema forbids
    `verified` without one, so reaching here means validation was bypassed, and
    the safe reading of a missing date is "we do not know when".
    """
    pulled = (record.get("identity") or {}).get("pulled")
    if not pulled:
        return True
    return (as_of - datetime.date.fromisoformat(pulled)).days > max_age_days
