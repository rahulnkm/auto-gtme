#!/usr/bin/env python3
"""One-off: make unproven identity claims in an existing prospects.jsonl visible.

Usage:  python3 skills/backfill_identity.py runs/<slug>

Sets record_status to "unchecked" on every record that either lacks the field or
claims "verified" without the identity evidence prospects.schema.json requires.

It writes no identity. A pull date copied off enriched_at is not a record of a
visit, and marking it as reconstructed would create a schema-legal path to
"ready" with no captured evidence - the original defect under a new name.

Takes an explicit run path rather than globbing runs/*, so abandoned directories
(runs/adin/_investor-abandoned/) are migrated only if named.

DELETE THIS once every active run is migrated. It is a broom, not a stage.
"""
import json, os, sys


def unproven(record):
    status = record.get("record_status")
    if status is None:
        return True                                   # never checked
    return status == "verified" and "identity" not in record   # claimed, not evidenced


def main(run):
    path = os.path.join(run, "enrich", "prospects.jsonl")
    rows = [json.loads(l) for l in open(path) if l.strip()]
    changed = 0
    for r in rows:
        if unproven(r):
            r["record_status"] = "unchecked"
            changed += 1
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{changed} of {len(rows)} records set to unchecked")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
