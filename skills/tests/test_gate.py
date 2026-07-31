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
