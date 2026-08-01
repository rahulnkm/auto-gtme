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
import json, os, re, sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("needs jsonschema:  pip install jsonschema")

SKILLS = os.path.dirname(os.path.abspath(__file__))

REGISTRY = {
    "company": ("company/company.json",   "gtme-company/company.schema.json",  "document"),
    "market":  ("market/market-pain.json", "gtme-market-pain/market-pain.schema.json", "document"),
    "icp":     ("icp/icp.json",           "gtme-icp/icp.schema.json",           "document"),
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


# Sections describing the research process itself, not findings about the company.
DISTILLATION_META = {"subject", "distillation"}

def distillation_gaps(research):
    """Research sections neither mapped into company.json nor excluded with a reason.

    Schema validation catches an agent INVENTING a field. It cannot catch an agent
    holding a fact, finding no home for it, and dropping it - nothing was added, so
    nothing fails. That is the failure this check exists for: a diff of a real run
    found four classes of company-shape fact sitting in the research file and
    silently absent from the fingerprint.

    It does not verify a mapping is truthful. It makes an unexplained drop
    impossible to do silently, which is the same bar the competitor identity check
    sets for not-looking."""
    d = research.get("distillation") or {}
    accounted = {e.get("section") for e in d.get("mapped", [])} | \
                {e.get("section") for e in d.get("excluded", [])}
    return sorted(set(research) - DISTILLATION_META - accounted)


# Citation ids may carry a stage prefix ([O1] in offer/), so they are strings, not ints.
CITE = re.compile(r"\[([A-Za-z]*\d+)\]")
# An entry starts a block: preceded by a blank line or the start of file. Without
# that anchor, a prose paragraph that happens to wrap onto "[4] Nick's post" reads
# as a definition - which it is not, and which offer/provenance.md actually does.
PROV_ENTRY = re.compile(r"(?:\A\s*|\n[ \t]*\n)\[([A-Za-z]*\d+)\](.*?)(?=\n[ \t]*\n\[[A-Za-z]*\d+\]|\Z)", re.S)

def _defined(provenance):
    return {n: body for n, body in PROV_ENTRY.findall(provenance)}

def _key(n):
    """Sort [2] before [10], and letter-prefixed ids after plain ones."""
    pre = n.rstrip("0123456789")
    return (pre, int(n[len(pre):]))

def orphaned_citations(artifact_text, provenance_text):
    """Citations researched, written into provenance.md, and never referenced.

    Evidence gathered and then dropped is invisible to every other check: the
    artifact is well-formed, every claim it does make is cited, and nothing
    errors. A measured sweep found a third of one stage's citations orphaned -
    including the only direct proof of a claim the artifact went on to assert
    bare, and five verbatim named-vendor complaints flattened into one sentence.

    An orphan is legal when its provenance entry says why, so the escape hatch is
    a decision on the record instead of silence: mark the entry UNUSED: <reason>.
    """
    used = set(CITE.findall(artifact_text))
    return sorted((n for n, body in _defined(provenance_text).items()
                   if n not in used and "UNUSED:" not in body), key=_key)

def dangling_citations(artifact_text, provenance_text):
    """The opposite failure: the artifact cites [n] that provenance never defines."""
    defined = set(_defined(provenance_text))
    return sorted(set(CITE.findall(artifact_text)) - defined, key=_key)


def check_citations(run, stage):
    """Citation hygiene for one stage folder. Silent when there is no provenance.md."""
    rel_art, _, mode = REGISTRY[stage]
    if mode != "document":
        return None
    art_p = os.path.join(run, rel_art)
    prov_p = os.path.join(run, os.path.dirname(rel_art), "provenance.md")
    if not (os.path.exists(art_p) and os.path.exists(prov_p)):
        return None
    art, prov = open(art_p).read(), open(prov_p).read()
    orph, dang = orphaned_citations(art, prov), dangling_citations(art, prov)
    rel = os.path.join(os.path.dirname(rel_art), "provenance.md")
    if not orph and not dang:
        print(f"ok   {rel}  (citations accounted)")
        return True
    for n in dang:
        print(f"FAIL {rel}\n  [{n}] cited by the artifact but never defined here")
    if orph:
        print(f"FAIL {rel}  ({len(orph)} citation{'s' if len(orph) != 1 else ''} researched and never used)")
        for n in orph:
            print(f"  [{n}]: reference it from the artifact, or mark the entry 'UNUSED: <reason>'")
    return False


def check_distillation(run):
    """Company-stage companion to check(). Silent when the research file is absent."""
    path = os.path.join(run, "company", "seller-research.json")
    rel = "company/seller-research.json"
    if not os.path.exists(path):
        return None
    try:
        research = json.load(open(path))
    except json.JSONDecodeError as e:
        print(f"FAIL {rel}\n  not valid JSON: {e}")
        return False
    gaps = distillation_gaps(research)
    if not gaps:
        print(f"ok   {rel}  (distillation accounted)")
        return True
    print(f"FAIL {rel}  ({len(gaps)} section{'s' if len(gaps) != 1 else ''} unaccounted for)")
    for g in gaps:
        print(f"  {g!r}: neither mapped into company.json nor excluded with a reason")
    return False

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
    results += [check_citations(run, s) for s in stages]
    if "company" in stages:
        results.append(check_distillation(run))
    ran = [r for r in results if r is not None]
    if not ran:
        print("nothing to validate - no artifacts found with a registered schema")
    sys.exit(1 if False in ran else 0)
