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
    "offer":   ("offer/offer.json",       "gtme-offer/offer.schema.json",       "document"),
    "enrich":  ("enrich/prospects.jsonl", "gtme-enrich/prospects.schema.json", "lines"),
}

# Run order. A reader must come after the producer, so this is what makes
# "downstream" in the admission test mean something checkable.
PIPELINE = [
    "gtme-why", "gtme-research", "gtme-company", "gtme-market-pain", "gtme-icp",
    "gtme-offer", "gtme-list", "gtme-signals", "gtme-enrich", "gtme-score",
    "gtme-write", "gtme-sequence", "gtme-publish", "gtme-measure", "gtme-handoff",
]

# The skill that PRODUCES each artifact. unread_fields excludes it when looking
# for readers: a stage naming its own output field proves nothing.
STAGE_SKILL = {
    "company": "gtme-company",
    "market":  "gtme-market-pain",
    "icp":     "gtme-icp",
    "offer":   "gtme-offer",
    "enrich":  "gtme-enrich",
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


# Fields that legitimately have no downstream reader, each with the reason on the
# record. The escape hatch is a decision in a diff, not silence - same bar as
# `UNUSED:` in provenance.md.
UNREAD_OK = {
    "offer.status":        "gate state; gtme-list refuses an unconfirmed offer by reading the file, not this field",
    "offer.confirmed_by":  "gate provenance",
    "offer.confirmed_at":  "gate provenance",
    "offer.gate_answers":  "the human judgment surface; the gate is human by design",
    "offer.cut_list":      "the human judgment surface - what was traded away",
    "offer.rationale":     "the human judgment surface",
    "icp.status":          "gate state; the ★1 confirmation is read by humans, not a stage",
    "icp.confirmed_by":    "gate provenance",
    "icp.confirmed_at":    "gate provenance",
    "icp.objective":       "states the filter's intent for the human at the gate",
    "market.status":       "gate state; the pain map is confirmed by a human, not consumed",
    "market.harvested_at": "freshness stamp read by humans deciding to re-sweep",
    "market.sources_swept": "method record - what was searched and what blocked",
    "market.market_verdict": "the go/no-go judgment surface for the human",
}


def unread_fields(doc, stage):
    """Top-level fields of an artifact that no OTHER skill names.

    `artifact-design.md` states the admission test, rule 2: "A named downstream
    stage reads it. Every field holds its seat by a consumer. No consumer, no
    seat." That rule was written and never enforced, so eight fields accumulated
    across four artifacts - objections, market statistics, the practitioner
    keyword list, the offer's proof levers - each researched, written, and read
    by nothing.

    Readers are discovered by scanning SKILL.md rather than declared in a table
    here: a hand-kept registry drifts from the skills it describes, and the
    drift is exactly what this check exists to catch. A skill that merely
    mentions a field counts as reading it. That is deliberately generous - this
    check answers "does anything downstream know this exists", which is the
    weakest form of the rule and still catches every live violation.
    """
    producer = STAGE_SKILL.get(stage)
    # Only skills that run AFTER the producer can be readers. gtme-company
    # mentions `pain_keywords` and runs three stages earlier, which made a dead
    # field look consumed - the check has to respect pipeline order or it
    # launders exactly the drift it exists to catch.
    after = PIPELINE[PIPELINE.index(producer) + 1:] if producer in PIPELINE else []
    named = set()
    for d in after:
        path = os.path.join(SKILLS, d, "SKILL.md")
        if os.path.exists(path):
            text = open(path).read()
            named |= {f for f in doc if f in text}
    return sorted(f for f in doc
                  if f not in named and f"{stage}.{f}" not in UNREAD_OK)


def numbers_agree(run):
    """Quantities stated in two files that must match, asserted in one place.

    Two live disagreements paid for this: the in-VPC audit capacity appears as
    both 2 and 3 inside offer.json, and it gates the whole delivery plan; and
    the ICP's niche-slap guard sets a 500-account bar without anything checking
    that 500 accounts pass the filter. The second cleared by luck (774), which
    is the point - nothing would have said otherwise.
    """
    out = []
    o = _load(run, "offer/offer.json")
    i = _load(run, "icp/icp.json")

    if o:
        # Two distinct quantities that prose collapses into one. offer/provenance.md
        # [O4] states both: "2 concurrent in-VPC slots, ~3/quarter". Written as
        # "2 concurrent slots per quarter" they read as one number stated twice,
        # which is how the file appeared to say 2 and 3 for the same thing.
        econ = o.get("economics") or {}
        prose = json.dumps({k: v for k, v in o.items() if k != "economics"})
        for pattern, field, label in (
                (r"(\d+)\s+concurrent",            "vpc_concurrent_slots",           "concurrent in-VPC slots"),
                (r"(\d+)\s+(?:completed\s+)?per\s+quarter", "vpc_audit_capacity_per_quarter", "in-VPC audits per quarter")):
            stated = {int(n) for n in re.findall(pattern, prose)}
            truth = econ.get(field)
            if truth is not None and stated and stated != {truth}:
                out.append(f"{label}: prose says {sorted(stated)}, economics.{field} says {truth}")

    if i:
        g = i.get("niche_slap_guard") or {}
        per = (i.get("contacts_per_account") or {}).get("default")
        bar = g.get("min_contacts_before_icp_edit")
        tam = os.path.join(run, "list", "tam.jsonl")
        if bar and per and os.path.exists(tam):
            need = bar // per
            have = sum(1 for line in open(tam) if line.strip())
            if have < need:
                out.append(f"niche_slap_guard needs {need} accounts "
                           f"({bar} contacts / {per} per account); tam.jsonl has {have} - "
                           f"the guard can never be cleared, so the ICP can never be questioned")
    return out


def seeds_pass_disqualifiers(icp):
    """A hand-picked seed that the filter itself excludes.

    icp.seed_targets carried `Lead Bank` while icp.disqualifiers excluded any
    entity licensed to take deposits. Nothing caught it because seeds were bare
    strings with no tier, signal, or reason attached - there was nothing to
    check. Structured seeds make the contradiction visible.
    """
    dq = {d["id"] for d in icp.get("disqualifiers", []) if isinstance(d, dict)}
    return [f"{s['name']}: declares disqualifier {s['excluded_by']!r}"
            for s in icp.get("seed_targets", [])
            if isinstance(s, dict) and s.get("excluded_by") in dq]


def check_contracts(run, stage, doc):
    """Cross-cutting checks that schemas cannot express."""
    ok = True
    unread = unread_fields(doc, stage)
    if unread:
        ok = False
        print(f"FAIL {stage}  ({len(unread)} field{'s' if len(unread) != 1 else ''} "
              f"no other skill reads - admission test rule 2)")
        for f in unread:
            print(f"  {f!r}: name it in a downstream SKILL.md, delete it, "
                  f"or add it to UNREAD_OK with a reason")
    if stage == "icp":
        for bad in seeds_pass_disqualifiers(doc):
            ok = False
            print(f"FAIL {stage}  seed target excluded by this ICP's own filter\n  {bad}")
    return ok


def check_numbers(run):
    bad = numbers_agree(run)
    if not bad:
        print("ok   cross-file numbers agree")
        return True
    print(f"FAIL cross-file numbers  ({len(bad)} disagreement{'s' if len(bad) != 1 else ''})")
    for b in bad:
        print(f"  {b}")
    return False


def _load(run, rel):
    path = os.path.join(run, rel)
    if not os.path.exists(path):
        return None
    try:
        return json.load(open(path))
    except json.JSONDecodeError:
        return None


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
    for s in stages:
        rel, _, mode = REGISTRY[s]
        doc = _load(run, rel) if mode == "document" else None
        if doc is not None:
            results.append(check_contracts(run, s, doc))
    results.append(check_numbers(run))
    if "company" in stages:
        results.append(check_distillation(run))
    ran = [r for r in results if r is not None]
    if not ran:
        print("nothing to validate - no artifacts found with a registered schema")
    sys.exit(1 if False in ran else 0)
