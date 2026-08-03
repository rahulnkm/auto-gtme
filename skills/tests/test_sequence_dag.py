"""Graph invariants for `spec: dag/1` sequence templates.

A sequence template is executed by gtme-send as a state machine, so a malformed graph is not
a style problem - it is a contact that never gets a message, or one that never stops getting
them. Schema validation cannot catch either, because both are well-formed JSON. These are the
checks that need the whole graph in hand at once.
"""
import json
from conftest import seller_names
import pathlib

import pytest

TEMPLATES = pathlib.Path(__file__).resolve().parents[1] / "gtme-sequence" / "templates"
DAGS = sorted(p for p in TEMPLATES.glob("*.json") if json.loads(p.read_text()).get("spec") == "dag/1")

# Events a human resolves at a gate, versus events an adapter observes. The split is the
# architecture's central claim: the engine never decides one of the first kind.
JUDGMENT_EVENTS = {
    "classified_interested", "classified_not_now", "classified_negative",
    "classified_wrong_person", "classified_unsubscribe_request",
}
MACHINE_EVENTS = {
    "timeout", "reply_human", "bounce_hard", "bounce_soft", "unsubscribe", "auto_reply_ooo",
    "link_clicked", "connection_accepted", "connection_withdrawn", "meeting_booked",
    "signal_expired",
}


def load(p):
    return json.loads(p.read_text())


def ids(t):
    return {n["id"]: n for n in t["nodes"]}


@pytest.fixture(params=DAGS, ids=lambda p: p.stem)
def tpl(request):
    return load(request.param)


def test_at_least_one_dag_template_exists():
    assert DAGS, "no spec: dag/1 templates found"


def test_node_ids_unique(tpl):
    seen = [n["id"] for n in tpl["nodes"]]
    assert len(seen) == len(set(seen)), f"duplicate node ids: {seen}"


def test_every_edge_endpoint_exists(tpl):
    known = ids(tpl)
    for e in tpl["edges"]:
        assert e["from"] in known, f"edge from unknown node {e['from']}"
        assert e["to"] in known, f"edge to unknown node {e['to']}"


def test_entry_exists_and_is_a_message(tpl):
    n = ids(tpl)[tpl["entry"]]
    assert n["kind"] == "message", "entry must be a message node"


def test_every_node_reachable_from_entry(tpl):
    adj = {}
    for e in tpl["edges"]:
        adj.setdefault(e["from"], []).append(e["to"])
    seen, stack = set(), [tpl["entry"]]
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(adj.get(cur, []))
    orphans = set(ids(tpl)) - seen
    assert not orphans, f"unreachable nodes (a contact can never arrive): {sorted(orphans)}"


def test_non_terminal_nodes_can_be_left(tpl):
    outgoing = {e["from"] for e in tpl["edges"]}
    for n in tpl["nodes"]:
        if n["kind"] == "terminal":
            continue
        assert n["id"] in outgoing, f"{n['id']} has no exit - a contact entering it is stuck forever"


def test_terminals_are_terminal(tpl):
    term = {n["id"] for n in tpl["nodes"] if n["kind"] == "terminal"}
    for e in tpl["edges"]:
        assert e["from"] not in term, f"terminal {e['from']} has an outgoing edge"


def test_terminals_declare_an_outcome(tpl):
    """gtme-measure attributes against these; an unnamed ending is an unattributable contact."""
    allowed = {"booked", "replied_positive", "replied_negative", "disqualified", "bounced",
               "unsubscribed", "exhausted_no_reply", "stopped_by_human"}
    for n in tpl["nodes"]:
        if n["kind"] == "terminal":
            assert n.get("outcome") in allowed, f"{n['id']} has no valid outcome"


def test_every_cold_path_can_reach_a_terminal(tpl):
    adj = {}
    for e in tpl["edges"]:
        adj.setdefault(e["from"], []).append(e["to"])
    term = {n["id"] for n in tpl["nodes"] if n["kind"] == "terminal"}
    for n in tpl["nodes"]:
        seen, stack, ok = set(), [n["id"]], False
        while stack:
            cur = stack.pop()
            if cur in term:
                ok = True
                break
            if cur in seen:
                continue
            seen.add(cur)
            stack.extend(adj.get(cur, []))
        assert ok, f"{n['id']} cannot reach any terminal - the contact never finishes"


def test_exactly_one_final_cold_touch(tpl):
    fin = [n for n in tpl["nodes"] if n.get("is_final_cold")]
    assert len(fin) == 1, f"expected exactly one is_final_cold node, got {[n['id'] for n in fin]}"


def test_no_cold_node_follows_the_final_cold_touch(tpl):
    """The copy says 'this is the last time'. This makes that true."""
    node = ids(tpl)
    fin = next(n["id"] for n in tpl["nodes"] if n.get("is_final_cold"))
    adj = {}
    for e in tpl["edges"]:
        adj.setdefault(e["from"], []).append(e["to"])
    seen, stack = set(), list(adj.get(fin, []))
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(adj.get(cur, []))
    after_cold = [n for n in seen if node[n].get("stage") == "cold"]
    assert not after_cold, f"cold nodes reachable after the breakup: {sorted(after_cold)}"


def test_four_cold_touches(tpl):
    cold = [n for n in tpl["nodes"] if n["kind"] == "message" and n.get("stage") == "cold"]
    assert len(cold) == 4, f"expected 4 cold touches, got {len(cold)}"


def test_event_edges_outrank_timeout_on_the_same_node(tpl):
    """If a reply and a scheduled send land on the same tick, the reply must win."""
    for n in tpl["nodes"]:
        out = [e for e in tpl["edges"] if e["from"] == n["id"]]
        timeouts = [e for e in out if e["when"] == "timeout"]
        events = [e for e in out if e["when"] != "timeout"]
        if not timeouts or not events:
            continue
        assert max(e.get("priority", 100) for e in events) < min(e.get("priority", 100) for e in timeouts), \
            f"{n['id']}: a timeout edge outranks an event edge"


def test_timeout_edges_carry_a_duration(tpl):
    for e in tpl["edges"]:
        if e["when"] == "timeout":
            assert e.get("after", "").startswith("P"), f"{e['from']}->{e['to']} timeout without ISO duration"


def test_judgment_events_only_leave_a_human_gate(tpl):
    """The whole point: the engine never classifies a human reply."""
    node = ids(tpl)
    for e in tpl["edges"]:
        if e["when"] in JUDGMENT_EVENTS:
            assert node[e["from"]]["kind"] == "human_gate", \
                f"{e['from']} emits {e['when']} but is not a human_gate - that automates judgment"


def test_all_events_are_known(tpl):
    for e in tpl["edges"]:
        assert e["when"] in MACHINE_EVENTS | JUDGMENT_EVENTS, f"unknown event {e['when']}"


def test_any_reply_leaves_every_cold_node(tpl):
    """A follow-up landing after a human replied is the clearest tell nobody is reading."""
    for n in tpl["nodes"]:
        if n["kind"] == "message" and n.get("stage") == "cold":
            outs = {e["when"] for e in tpl["edges"] if e["from"] == n["id"]}
            assert "reply_human" in outs, f"{n['id']} has no reply_human exit"


def test_hard_stops_exist_on_every_cold_node(tpl):
    for n in tpl["nodes"]:
        if n["kind"] == "message" and n.get("stage") == "cold":
            outs = {e["when"] for e in tpl["edges"] if e["from"] == n["id"]}
            assert {"bounce_hard", "unsubscribe"} <= outs, f"{n['id']} missing a hard-stop exit"


def test_message_nodes_carry_a_writing_brief(tpl):
    """gtme-write reads these. A node without them is a message nobody briefed."""
    for n in tpl["nodes"]:
        if n["kind"] != "message":
            continue
        for f in ("intent", "leans_on", "ask", "word_max", "channel"):
            assert n.get(f) not in (None, ""), f"{n['id']} missing {f}"
        assert len(n["intent"]) >= 15, f"{n['id']} intent too thin to brief from"


def test_only_warm_nodes_may_carry_a_product_link(tpl):
    """Cold touches earn attention by naming a problem, not by linking a product."""
    for n in tpl["nodes"]:
        if n["kind"] == "message" and n.get("stage") == "cold":
            joined = " ".join(n.get("constraints", []))
            assert "product page" not in joined.lower(), f"{n['id']} is cold but references a product page"


def test_templates_carry_no_seller_specifics(tpl):
    """A template that only works for one seller is not a template."""
    blob = json.dumps(tpl).lower()
    for bad in [n.lower() for n in seller_names()] + ["$", "pricing page", "our product is"]:
        assert bad not in blob, f"seller-specific content leaked into the template: {bad!r}"


def test_structural_claims_are_cited(tpl):
    assert tpl.get("cites"), "timing and structure claims must cite research/"


# --- schema conformance ------------------------------------------------------
#
# The graph checks above need the whole graph in hand. These are the per-object rules
# JSON Schema can carry, plus the negative cases that prove it actually rejects them - a
# schema nobody has tried to break is a schema that accepts anything.

from jsonschema import Draft202012Validator  # noqa: E402

DAG_SCHEMA = json.loads((TEMPLATES.parent / "sequence.dag.schema.json").read_text())
DV = Draft202012Validator(DAG_SCHEMA)


def errs(d):
    return [f"{list(e.absolute_path)}: {e.message}" for e in DV.iter_errors(d)]


def test_the_schema_is_itself_valid():
    Draft202012Validator.check_schema(DAG_SCHEMA)


def test_every_dag_template_validates(tpl):
    assert errs(tpl) == []


def bound(**over):
    """A minimal VALID bound sequence, used as the base for negative cases."""
    d = {
        "spec": "dag/1", "id": "email-4touch-dag", "version": "2.0.0",
        "status": "draft",
        "template_id": "email-4touch-dag", "template_version": "2.0.0",
        "selection_rationale": "Email is the only wired channel and the domain is still warming, so extra channels would add holes rather than touches.",
        "channels_verified": [{"channel": "email_cold", "wired": True, "evidence": "channel-plan.json: smartlead, 30/day, warmup complete"}],
        "volume_ceiling": {"binding_channel": "email_cold", "daily_cap": 30, "sequence_days": 19,
                           "touches_per_contact": 4, "max_contacts_in_flight": 142,
                           "derivation": "30 x 19 / 4 = 142 contacts in flight"},
        "entry": "t1",
        "nodes": [
            {"id": "t1", "kind": "message", "stage": "cold", "channel": "email_cold",
             "intent": "Name the problem in their own words and earn one reply.",
             "leans_on": "pain", "ask": "micro_commitment", "word_max": 125,
             "binds": {"pain_id": "pain:unworked_backlog"}},
            {"id": "end_exhausted", "kind": "terminal", "outcome": "exhausted_no_reply"},
        ],
        "edges": [{"from": "t1", "to": "end_exhausted", "when": "timeout", "after": "P7D", "priority": 10}],
    }
    d.update(over)
    return d


def test_the_bound_example_is_valid():
    assert errs(bound()) == []


def test_bound_sequence_must_bind_a_pain_it_leans_on():
    d = bound()
    del d["nodes"][0]["binds"]
    assert errs(d), "a bound sequence leaning on a pain with no pain_id must be rejected"


def test_a_template_may_omit_binds():
    """The difference between a template and a bound sequence."""
    d = bound()
    for k in ("status", "template_id", "template_version", "selection_rationale",
              "channels_verified", "volume_ceiling"):
        d.pop(k)
    d.update(when_to_use="Email is the only wired channel, or deliverability is fragile.",
             channels_required=["email_cold"],
             rationale="One opener plus three follow-ups is the documented ceiling before marginal replies stop paying for domain reputation.",
             cites=["research/04 §5.2"])
    del d["nodes"][0]["binds"]
    assert errs(d) == []


def test_bound_sequence_requires_a_derived_volume_ceiling():
    d = bound()
    del d["volume_ceiling"]
    assert errs(d), "gtme-list reads this; an absent ceiling constrains nothing"


def test_confirmed_requires_who_and_when():
    assert errs(bound(status="confirmed")), "gate 2.5 must record who confirmed and when"


def test_timeout_edge_without_a_duration_is_rejected():
    d = bound()
    del d["edges"][0]["after"]
    assert errs(d), "a timeout with no duration never fires"


def test_unknown_event_is_rejected():
    d = bound()
    d["edges"][0]["when"] = "vibes"
    assert errs(d)


def test_bad_duration_is_rejected():
    d = bound()
    d["edges"][0]["after"] = "7 days"
    assert errs(d), "durations are ISO-8601"


def test_final_cold_must_be_a_cold_breakup():
    d = bound()
    d["nodes"][0]["is_final_cold"] = True
    d["nodes"][0]["stage"] = "warm"
    assert errs(d), "only a cold node can be the final cold node"


def test_terminal_needs_a_known_outcome():
    d = bound()
    d["nodes"][1]["outcome"] = "fizzled"
    assert errs(d)


def test_unknown_channel_is_rejected():
    d = bound()
    d["nodes"][0]["channel"] = "carrier_pigeon"
    assert errs(d), "a channel with no adapter is a hole in the plan"


def test_prose_instead_of_an_id_is_rejected():
    """A paraphrase here is a second copy of the pain map, and the copy drifts."""
    d = bound()
    d["nodes"][0]["binds"] = {"pain_id": "the backlog never goes to zero"}
    assert errs(d)


def test_unknown_field_is_rejected():
    assert errs(bound(mystery_field="x")), "additionalProperties must stay closed"
