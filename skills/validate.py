#!/usr/bin/env python3
"""Validate a run's artifacts against the stage schemas.

Usage:  python3 skills/validate.py runs/<slug> [stage ...]

With no stage names it checks every artifact present in the run and skips the
ones that have no schema yet. Exit code 1 if anything failed, so a stage can
refuse to hand off. Requires `jsonschema` (pip install jsonschema).

Registry maps stage -> (artifact path in the run, schema path in skills/).
Add a line here when a stage gets a schema; nothing else needs to change.
"""
import json, os, sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("needs jsonschema:  pip install jsonschema")

SKILLS = os.path.dirname(os.path.abspath(__file__))

REGISTRY = {
    "company": ("company/company.json", "gtme-company/company.schema.json"),
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

def check(run, stage):
    rel, schema_rel = REGISTRY[stage]
    path = os.path.join(run, rel)
    if not os.path.exists(path):
        return None                       # stage has not run yet
    schema = json.load(open(os.path.join(SKILLS, schema_rel)))
    try:
        doc = json.load(open(path))
    except json.JSONDecodeError as e:
        print(f"FAIL {rel}\n  not valid JSON: {e}")
        return False

    errors = sorted(Draft202012Validator(schema).iter_errors(doc),
                    key=lambda e: list(e.absolute_path))
    for i in unique_ids(doc):
        print(f"FAIL {rel}\n  duplicate id {i!r} - downstream refs to it are ambiguous")
    if not errors and not unique_ids(doc):
        print(f"ok   {rel}")
        return True

    print(f"FAIL {rel}  ({len(errors)} schema error{'s' if len(errors) != 1 else ''})")
    for e in errors:
        where = "".join(f"[{p!r}]" if isinstance(p, str) else f"[{p}]"
                        for p in e.absolute_path) or "<root>"
        print(f"  {where}: {e.message}")
    return False

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
