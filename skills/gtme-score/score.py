#!/usr/bin/env python3
"""Reference implementation of the gtme-score formula (see SKILL.md).

Usage:  python3 score.py runs/<slug> [--write]
Without --write it dry-runs and prints the distribution report.
The constants here ARE the fixed formula - change them only by changing SKILL.md.
"""
import json, math, sys, collections, datetime, os
from gate import send_gate, max_age_from_icp

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
RUN = ARGS[0] if ARGS else "."
AS_OF = datetime.date.today()
for a in sys.argv[1:]:
    if a.startswith("--as-of="):
        AS_OF = datetime.date.fromisoformat(a.split("=", 1)[1])
DRY = "--write" not in sys.argv

def jl(p):
    out = []
    for l in open(os.path.join(RUN, p)):
        l = l.strip()
        if l:
            out.append(json.loads(l))
    return out

tam = jl("06-list/tam.jsonl")
signals = jl("07-signals/signals.jsonl")
prospects = jl("07-enrich/prospects.jsonl")
icp = json.load(open(os.path.join(RUN, "03-icp/icp.json")))
# Recency tolerance is a per-campaign judgment, not part of the fixed formula,
# so it lives in icp.scoring rather than in the constants below. This is the
# first code that reads icp.scoring - score.py previously read only icp["tiers"].
MAX_IDENTITY_AGE_DAYS = max_age_from_icp(icp)
try:
    old = {d["account_id"]: d for d in jl("08-score/scored.jsonl")}
except FileNotFoundError:
    old = {}

allowed_stages = {t["tier"]: set(t.get("stages", [])) for t in icp["tiers"]}
GOOD_GEO = {"US", "CA", "UK", "EU"}
# Whose LinkedIn account produced connection_degree. NOT necessarily the sender.
NETWORK_OWNER = "rahul_nandakumar"
PTS = {"strong": 10.0, "medium": 5.0, "weak": 2.0, "counter": -8.0, "unknown": 0.0}

# ---------- account layer ----------
by_acct = collections.defaultdict(list)
for s in signals:
    by_acct[s["account_id"]].append(s)

def parse_date(s):
    """event_date may be YYYY-MM-DD, YYYY-MM (month precision) or YYYY."""
    p = s.split("-")
    if len(p) >= 3:
        return datetime.date(int(p[0]), int(p[1]), int(p[2][:2]))
    if len(p) == 2:
        return datetime.date(int(p[0]), int(p[1]), 15)   # midpoint, unbiased
    return datetime.date(int(p[0]), 7, 1)

def decayed(s):
    ev = parse_date(s["event_date"])
    age = max(0, (AS_OF - ev).days)
    return PTS.get(s.get("strength"), 0.0) * (0.5 ** (age / 90.0))

def value_mult(a):
    """Deal-size proxy from fraud/T&S team size, shrunk toward 1.0 when the
    size is imputed rather than researched (directory rows are employee_est x 0.03)."""
    st = a.get("sub_team_est")
    if not st or st <= 0:
        return 1.0
    raw = max(0.6, min(1.4, 0.6 + 0.5 * math.log10(st / 3.0)))
    shrink = 1.0 if a.get("firmographic_source") == "researched" else 0.5
    return 1.0 + shrink * (raw - 1.0)

def fit_mult(a):
    base = {1: 1.0, 2: 0.75, 3: 0.5}.get(a.get("tier"), 0.5)
    geo = 1.0 if a.get("geo") in GOOD_GEO else 0.9
    stage = 1.0 if a.get("stage") in allowed_stages.get(a.get("tier"), set()) else 0.9
    inc = 1.1 if a.get("incumbent_tech") else 1.0
    return base * geo * stage * inc

# contact coverage
contacts_by_acct = collections.defaultdict(list)
for p in prospects:
    contacts_by_acct[p["account_id"]].append(p)

def coverage_state(aid):
    cs = contacts_by_acct.get(aid, [])
    if not cs:
        return "whitespace"
    if any(c.get("connection_degree") in ("1st", "2nd") for c in cs):
        return "covered"
    return "thin"

scored = []
for a in tam:
    aid = a["account_id"]
    evs = by_acct.get(aid, [])
    dec = [(e, decayed(e)) for e in evs]
    signal_score = round(sum(d for _, d in dec), 2)
    has_counter = any(e.get("strength") == "counter" and d < -0.5 for e, d in dec)
    pos = [(e, d) for e, d in dec if d > 0]
    top = max(pos, key=lambda x: x[1]) if pos else None

    v = round(value_mult(a), 3)
    f = round(fit_mult(a), 3)
    sm = round(max(0.1, 1 + signal_score / 10.0), 3)
    # need_mult = the account's PROPENSITY (does it have the problem, right now),
    # held separate from value so the two questions stay separable. final_score is
    # the expected value: how big the deal is x how likely they need it.
    need = round(f * sm, 3)
    final = round(10 * v * need, 2)

    # A disqualifier set at list time must survive into routing. gtme-list can flag
    # an account a competitor or out-of-ICP; if scoring ignores that flag the account
    # walks straight back into the send/enrich queue with a good score attached.
    dq = a.get("disqualifier_check", "pass")
    if dq.startswith("drop"):
        route = "excluded"
    elif signal_score < 0:
        route = "hold_human_review"
    else:
        route = "send"
    if route != "send":
        priority = "n/a"
    elif final >= 18:
        priority = "high"
    elif final >= 11:
        priority = "medium"
    else:
        priority = "low"

    scored.append({
        "account_id": aid, "company": a["company"], "fit_tier": a["tier"],
        "value_mult": v, "fit_mult": f, "signal_score": signal_score,
        "signal_mult": sm, "need_mult": need, "final_score": final,
        "coverage_state": coverage_state(aid),
        "has_active_counter": has_counter,
        "effort_mode": {1: "human_assisted", 2: "semi_auto", 3: "fully_auto"}.get(a["tier"]),
        "priority": priority, "route": route, "disqualifier_check": dq,
        "top_signal": ({"type": top[0]["signal_type"], "decayed": round(top[1], 2),
                        "direction": top[0].get("direction", "acquire")} if top else None),
        "evidence_layer": old.get(aid, {}).get("evidence_layer", "directory"),
        "geo": a.get("geo"), "sub_team_est": a.get("sub_team_est"),
        "size_source": a.get("firmographic_source"),
        "scored_at": AS_OF.isoformat() + "T00:00:00Z",
    })

scored.sort(key=lambda d: -d["final_score"])
acct_score = {d["account_id"]: d for d in scored}

# ---------- contact layer ----------
# contact_score = account_ev x reach_mult. A PRODUCT, not a sum.
#
# Why a product: the old form was account_final/2 + orbit + degree + role + seniority,
# which let additive constants decide the account/person trade-off row by row - the
# account's share of the total swung 41%-94% across the top 8, an accident rather
# than a decision. A product fixes that ratio by construction.
#
# Why reach_mult is centred on 1.0 (never 0): a cold 3rd-degree contact is the
# BASELINE, not an impossibility - 261 of 314 contacts here have no warmth at all.
# A raw product would zero them out and the queue would only ever contain the warm
# 8%. Same shape signal_mult already uses at the account layer: 1 + pts/10.
#
# Two warmth surfaces, kept separate because they belong to different people:
#   founder_orbit  - the SENDER's surface (shared employer/school with the seller's
#                    founders), read from the target's work history + education.
#   network_degree - measures whoever ran the enrichment, NOT the sender. Real, but
#                    it is the operator's network; owner is stamped on every row.
#
# What deliberately does NOT score here: role (champion vs economic buyer) and
# seniority. Those are ROUTING, not probability of reach - the champion is likelier
# to reply, the buyer is likelier to decide, and collapsing that into one number
# destroys the distinction the sequencer needs. Both are emitted as fields instead.
ORBIT_EMPLOYER = 6.0
ORBIT_SCHOOL = 3.0
DEGREE_PTS = {"1st": 5.0, "2nd": 3.0, "3rd+": 0.0}
DEGREE_UNKNOWN = 0.5
REACH_DIVISOR = 10.0   # warmth points -> multiplier: 1 + pts/10 (max ~1.9)
SENIOR = ("chief", "vp ", "vp,", "head of", "director", "president", "founder")

# Seller-specific, so it is DATA not code: read from company.json's
# warm_universe.founder_orbit. Absent = no orbit boost, which is the correct
# default - a hardcoded list would silently score another seller's run against
# this seller's network.
# ONLY places a founder actually worked. Investor/backer names do not belong here:
# "we took an angel check from X" is not a relationship with everyone who ever
# worked at X, and treating it as one manufactures warmth that does not exist.
_orbit = (json.load(open(os.path.join(RUN, "01-company/company.json")))
          .get("warm_universe", {}).get("founder_orbit", {}))
ORBIT_EMPLOYERS = tuple(e.lower() for e in _orbit.get("employers", ()))
ORBIT_SCHOOLS = tuple(s.lower() for s in _orbit.get("schools", ()))
if not ORBIT_EMPLOYERS and not ORBIT_SCHOOLS:
    print("  note: no warm_universe.founder_orbit in company.json - founder_orbit scores 0 for every contact")

sc = []
for p in prospects:
    a = acct_score.get(p["account_id"])
    if not a:
        continue
    base = round(a["final_score"] / 2.0, 2)
    deg = p.get("connection_degree")
    conn = DEGREE_PTS.get(deg, DEGREE_UNKNOWN)
    title = (p.get("title") or "").lower()
    # founder_orbit reads WORK HISTORY, not the headline - a headline never says
    # where someone used to work, which is the whole point of the signal.
    emps = p.get("employer_history") or []
    schools_l = p.get("education") or []
    # emps[0] is the CURRENT employer (= the target account). A match there means
    # "works where a founder used to work" - still warm, but a different claim from
    # "ex-colleague", so label which it is instead of silently merging them.
    ev = []
    for i, e in enumerate(emps):
        if any(o in e.lower() for o in ORBIT_EMPLOYERS):
            ev.append({"kind": "employer_current" if i == 0 else "employer_past", "value": e})
    for sch in schools_l:
        if any(x in sch.lower() for x in ORBIT_SCHOOLS):
            ev.append({"kind": "school", "value": sch})
    orbit = 0.0
    if any(x["kind"].startswith("employer") for x in ev):
        orbit += ORBIT_EMPLOYER
    if any(x["kind"] == "school" for x in ev):
        orbit += ORBIT_SCHOOL
    # warmth -> reach multiplier, floored at 1.0 (cold is baseline, not zero)
    warmth = orbit + conn
    reach = round(max(1.0, 1 + warmth / REACH_DIVISOR), 3)
    total = round(a["final_score"] * reach, 2)
    parts = {"account_ev": a["final_score"], "reach_mult": reach,
             "founder_orbit": orbit, "network_degree": conn, "warmth_pts": warmth}
    # routing metadata - deliberately NOT scored (see header note)
    is_champion = p.get("role") == "champion"
    sen = 1.0 if any(s in title for s in SENIOR) else 0.0
    conf = p.get("confidence") or 0.0
    # A record that failed identity verification is not a ranking problem, it is
    # a send problem. Gate it; do not quietly leave it in the queue.
    status = p.get("record_status")
    gate = send_gate(p, AS_OF, MAX_IDENTITY_AGE_DAYS)
    cand = {k: parts[k] for k in ("founder_orbit", "network_degree") if parts[k] >= 3.0}
    dom = max(cand, key=lambda k: cand[k]) if cand else "account_fit"
    sc.append({
        "account_id": p["account_id"], "company": p["company"], "role": p["role"],
        "name": p["name"], "title": p["title"], "linkedin": p.get("linkedin"),
        "network_degree": deg, "network_owner": NETWORK_OWNER,
        "orbit_evidence": ev, "record_status": status, "confidence": conf,
        "mutual_connection": p.get("mutual_connection"),
        "mutual_connections": p.get("mutual_connections"),
        "mutual_status": p.get("mutual_status"),
        "send_gate": gate, "email_status": p.get("email_status"),
        "fit_tier": p.get("tier"), "account_score": a["final_score"],
        "account_route": a["route"], "coverage_state": a["coverage_state"],
        "top_signal": (a["top_signal"] or {}).get("type"),
        "contact_score": total, "reach_mult": reach, "warmth_pts": warmth,
        "score_parts": parts, "dominant_reason": dom,
        "is_champion": is_champion, "is_senior": bool(sen),
        "touch_order": ("champion_first" if is_champion else "buyer"),
    })

# A gated row must not hold a rank. Leaving a do-not-send contact at #3 in the
# queue is an invitation to step over the gate; rank only what is sendable.
#
# Ties are common by design now: two contacts at one account with equal warmth get
# an identical score, because the score no longer contains role or seniority. Those
# break the tie instead - champion first (the ICP's first_touch), then seniority,
# then name for determinism. Routing decides order within a score; it never moves
# the score itself.
sc.sort(key=lambda d: (-d["contact_score"], not d["is_champion"],
                       not d["is_senior"], d["name"]))
rank = 0
for c in sc:
    if c["send_gate"] == "do_not_send":
        c["send_rank"] = None
        continue
    rank += 1
    c["send_rank"] = rank

# ---------- report ----------
def hist(vals, label):
    c = collections.Counter(vals)
    print(f"  {label}: " + ", ".join(f"{k}={v}" for k, v in c.most_common()))

print("=== ACCOUNTS (773 live; tam has %d) ===" % len(tam))
hist([d["priority"] for d in scored], "priority")
hist([d["route"] for d in scored], "route")
hist([d["coverage_state"] for d in scored], "coverage")
fs = [d["final_score"] for d in scored]
print(f"  final_score: min={min(fs)} med={sorted(fs)[len(fs)//2]} max={max(fs)} distinct={len(set(fs))}")
oldfs = [d["final_score"] for d in old.values()]
print(f"  OLD final_score: distinct={len(set(oldfs))}, zeros={sum(1 for x in oldfs if x==0)}")
print(f"  NEW zeros={sum(1 for x in fs if x==0)}")
print("\n  TOP 15 NEW:")
for d in scored[:15]:
    o = old.get(d["account_id"], {})
    orank = None
    print(f"    {d['final_score']:6.2f}  {d['company'][:26]:26s} t{d['fit_tier']} "
          f"v{d['value_mult']:.2f} f{d['fit_mult']:.2f} s{d['signal_mult']:.2f} "
          f"{d['coverage_state']:10s} (old {o.get('final_score','-')})")

# biggest movers: accounts that were 0 before
zero_before = [d for d in scored if old.get(d["account_id"], {}).get("final_score", 0) == 0]
zero_before.sort(key=lambda d: -d["final_score"])
if zero_before:
    print(f"\n  {len(zero_before)} accounts scored 0.0 before; now spread {zero_before[-1]['final_score']}–{zero_before[0]['final_score']}. Top 8:")
for d in zero_before[:8]:
    print(f"    {d['final_score']:6.2f}  {d['company'][:26]:26s} t{d['fit_tier']} sub_team={d['sub_team_est']} {d['coverage_state']}")

print("\n=== CONTACTS (%d) ===" % len(sc))
hist([c["dominant_reason"] for c in sc], "dominant_reason")
hist([c["send_gate"] for c in sc], "send_gate")
hist([c["record_status"] for c in sc if c["record_status"]], "record_status(backfilled only)")
print("  orbit hits: %d contacts" % sum(1 for c in sc if c["score_parts"]["founder_orbit"] > 0))
hist([c["reach_mult"] for c in sc], "reach_mult")
cscores = [c["contact_score"] for c in sc]
print(f"  contact_score distinct={len(set(cscores))}  range={min(cscores)}-{max(cscores)}")
oldc = {}
try:
    for c in jl("08-score/scored_contacts.jsonl.pre-v3.bak"):
        oldc[(c["account_id"], c["name"])] = c
except FileNotFoundError:
    pass
print("  TOP 15  (acct_ev x reach = contact_ev):")
for c in [x for x in sc if x["send_rank"]][:15]:
    o = oldc.get((c["account_id"], c["name"]), {})
    orank = o.get("send_rank")
    mv = f"was #{orank}" if orank else "new"
    print(f"    #{c['send_rank']:3d} {c['account_score']:6.2f} x{c['reach_mult']:.2f} = {c['contact_score']:6.2f}  "
          f"{c['name'][:22]:22s} {c['company'][:16]:16s} {str(c['network_degree']):6s} "
          f"{c['dominant_reason']:14s} {mv}")
# biggest rank movers
if oldc:
    mv = []
    for c in sc:
        o = oldc.get((c["account_id"], c["name"]))
        if o and o.get("send_rank") and c.get("send_rank"):
            mv.append((o["send_rank"] - c["send_rank"], c, o))
    mv.sort(key=lambda x: -x[0])
    print("\n  BIGGEST RISERS:")
    for d, c, o in mv[:6]:
        print(f"    +{d:3d}  #{o['send_rank']:3d} -> #{c['send_rank']:3d}  {c['name'][:22]:22s} {c['company'][:16]:16s} acct={c['account_score']:.2f} reach={c['reach_mult']:.2f}")
    print("  BIGGEST FALLERS:")
    for d, c, o in mv[-6:]:
        print(f"    {d:4d}  #{o['send_rank']:3d} -> #{c['send_rank']:3d}  {c['name'][:22]:22s} {c['company'][:16]:16s} acct={c['account_score']:.2f} reach={c['reach_mult']:.2f}")

if not DRY:
    with open(os.path.join(RUN, "08-score/scored.jsonl"), "w") as f:
        for d in scored:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    with open(os.path.join(RUN, "08-score/scored_contacts.jsonl"), "w") as f:
        for c in sc:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print("\nWROTE 08-score/scored.jsonl + 08-score/scored_contacts.jsonl")
else:
    print("\n(dry run — pass --write to persist)")
