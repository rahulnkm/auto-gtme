#!/usr/bin/env python3
"""Validate a run's artifacts against the stage schemas.

Usage:  python3 skills/validate.py runs/<slug> [stage ...]

With no stage names it checks every artifact present in the run and skips the
ones that have no schema yet. Exit code 1 if anything failed, so a stage can
refuse to hand off. Requires `jsonschema` (pip install jsonschema).

Registry maps stage -> (artifact path in the run, schema path in skills/, mode).
Mode is "document" for a whole-file JSON artifact, "lines" for a line-delimited
one whose schema describes a single record.
Add a line here when a stage gets a schema; nothing else needs to change.
"""
import json, os, sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("needs jsonschema:  pip install jsonschema")

SKILLS = os.path.dirname(os.path.abspath(__file__))

REGISTRY = {
    "company": ("company/company.json",   "gtme-company/company.schema.json",  "document"),
    "enrich":  ("enrich/prospects.jsonl", "gtme-enrich/prospects.schema.json", "lines"),
}

def unique_ids(doc):
    """Duplicate ids are legal JSON and silently break every downstream
    reference that resolves by id, so they get their own check."""
    seen, dupes = set(), []
    def walk(node):
        if isinstance(node, dict):
            i = node.get("id")
            if isinstance(i, str):
                (dupes.append(i) if i in seen else seen.add(i))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(doc)
    return dupes

def where(e):
    return "".join(f"[{p!r}]" if isinstance(p, str) else f"[{p}]"
                   for p in e.absolute_path) or "<root>"

def check(run, stage):
    rel, schema_rel, mode = REGISTRY[stage]
    path = os.path.join(run, rel)
    if not os.path.exists(path):
        return None                       # stage has not run yet
    schema = json.load(open(os.path.join(SKILLS, schema_rel)))
    validator = Draft202012Validator(schema)
    return (_check_lines if mode == "lines" else _check_document)(rel, path, validator)


def _check_document(rel, path, validator):
    try:
        doc = json.load(open(path))
    except json.JSONDecodeError as e:
        print(f"FAIL {rel}\n  not valid JSON: {e}")
        return False
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
    dupes = unique_ids(doc)
    for i in dupes:
        print(f"FAIL {rel}\n  duplicate id {i!r} - downstream refs to it are ambiguous")
    if not errors and not dupes:
        print(f"ok   {rel}")
        return True
    print(f"FAIL {rel}  ({len(errors)} schema error{'s' if len(errors) != 1 else ''})")
    for e in errors:
        print(f"  {where(e)}: {e.message}")
    return False


def _check_lines(rel, path, validator):
    """Line-delimited artifacts are validated per record. unique_ids is NOT run:
    it tests uniqueness within one document, and per-record invocation would ask
    a meaningless question. Cross-record uniqueness is a different property.

    Counts failing RECORDS, not error messages. One record routinely trips
    several rules at once, and a count of messages reads as a larger problem
    than exists.
    """
    bad, total = 0, 0
    for n, line in enumerate(open(path), 1):
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"FAIL {rel}:{n}  not valid JSON: {e}")
            bad += 1
            continue
        errors = sorted(validator.iter_errors(rec), key=lambda e: list(e.absolute_path))
        for e in errors:
            print(f"FAIL {rel}:{n}  {where(e)}: {e.message}")
        if errors:
            bad += 1
    if bad:
        print(f"FAIL {rel}  ({bad} of {total} records invalid)")
        return False
    print(f"ok   {rel}  ({total} records)")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    run, stages = sys.argv[1], sys.argv[2:] or list(REGISTRY)
    unknown = [s for s in stages if s not in REGISTRY]
    if unknown:
        sys.exit(f"no schema registered for: {', '.join(unknown)}")

    results = [check(run, s) for s in stages]
    ran = [r for r in results if r is not None]
    if not ran:
        print("nothing to validate - no artifacts found with a registered schema")
    sys.exit(1 if False in ran else 0)
