"""The offer contract, tested against a synthetic offer.

Written from gtme-offer/SKILL.md, not from a live artifact: the market-pain
schema was once built from its own artifact and reproduced the exact drift it
existed to catch. test_live_artifact_validates is the one exception - it is the
migration signal and may fail loudly while a run is mid-migration.

The offer was the last of the four artifacts with no schema, and it held nine of
the twenty-four defects the audit found. That is not a coincidence, and most of
the rules below name the specific failure that bought them.
"""
import json
from conftest import EXAMPLE_RUN
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA = json.loads((Path(__file__).resolve().parent.parent /
                     "gtme-offer" / "offer.schema.json").read_text())
V = Draft202012Validator(SCHEMA)
RUN = EXAMPLE_RUN / "04-offer" / "offer.json"


def errs(d):
    return [f"{list(e.absolute_path)}: {e.message}" for e in V.iter_errors(d)]


OFFER = {
    "name": "The Closed-Case Audit", "status": "draft", "offer_tier": 2,
    "rationale": "Tier 2: the offer is good, not incredible, and the weak term is Likelihood.",
    "cut_list": "Dropped the standing retainer and the dashboard; neither reveals the core problem.",
    "core_offer": {
        "dream_outcome": "the queue stops being a source of unmeasured loss",
        "time_to_value": "first findings in 48h",
        "effort_asked": "a CSV of 100 closed cases",
        "likelihood_levers": [
            {"claim": "81% precision at a $50B+ marketplace", "evidence_class": "anonymized_customer",
             "cites": ["[O6]"], "measured": "private beta, single account, post-tuning"},
            {"claim": "white-box: prompts and evals inspectable by the buyer's team",
             "evidence_class": "structural"},
        ],
        "guarantee": {"type": "conditional",
                      "terms": "no missed fraud found above the agreed floor and you keep the memo",
                      "activation_points": ["corpus and dollar floor agreed in writing"],
                      "worst_case_cost": "2-3 engineer-days"},
    },
    "scarcity_facts": ["in-VPC shadow audits run 2 concurrent slots"],
    "problems": [{"id": "p1", "pain_id": "pain:unworked_backlog",
                  "problem": "review volume outgrows the analyst team",
                  "personas": ["champion", "economic_buyer"],
                  "solution": "queue rerank", "proof": "the audit's own findings",
                  "signals": ["job_posting_intent"]}],
    "front_end_offers": [{"id": "f1", "name": "[Desk Audit] 100 closed cases (2 weeks)",
                          "reveals": "p1", "magnet_type": "reveal_problem",
                          "narrow_problem_solved": "which closed cases were called wrong",
                          "standalone_price": "$5-10k", "direction": "acquire",
                          "deliverable_exists": True, "sampleable": True,
                          "acceptance_path": ["data-handling one-pager attached to the ask"]}],
    "proof_inventory": {"case_studies": 1, "testimonials": 0},
    "engaged_definition": ["reply", "sample_requested"],
    "economics": {"vpc_audit_capacity_per_quarter": 3, "vpc_concurrent_slots": 2},
    "gate_answers": {f"q{n}_{k}": "answered at the gate with reasons" for n, k in enumerate(
        ["pure", "incomparability", "four_levers", "component_per_problem", "trim",
         "guarantee_cashable", "scarcity_true", "premium_price", "named_and_front_end",
         "honest_tier", "standalone_price", "acceptance_obstacles"], 1)},
}


def offer(**over):
    return {**OFFER, **over}


def core(**over):
    return offer(core_offer={**OFFER["core_offer"], **over})


def test_a_complete_offer_validates():
    assert errs(OFFER) == []


# --- likelihood_levers: the most dangerous field, previously the least ruled --

def test_a_lever_may_not_be_a_bare_string():
    """These were four bare strings carrying "81% precision" and "$1.5M/month
    prevented" - founder-claimed figures from two unnamed betas - published to
    fraud teams whose job is catching unsupported claims."""
    assert errs(core(likelihood_levers=["81% precision at a $50B+ marketplace"])) != []


def test_a_lever_must_say_how_the_buyer_can_check_it():
    assert any("evidence_class" in e for e in
               errs(core(likelihood_levers=[{"claim": "81% precision on transaction review"}])))


def test_an_empirical_lever_must_cite():
    d = core(likelihood_levers=[{"claim": "81% precision on review", "evidence_class": "anonymized_customer"}])
    assert any("cites" in e for e in errs(d))


def test_a_structural_lever_needs_no_citation():
    """A property of how the product works is verified by inspection, not by a
    source. Conflating it with an unaudited performance number is what left 81%
    precision sitting next to a proof_inventory of zero."""
    d = core(likelihood_levers=[{"claim": "white-box: prompts inspectable", "evidence_class": "structural"}])
    assert errs(d) == []


# --- grain: the offer must not narrow what the pain map widened --------------

def test_a_problem_serves_every_persona_who_feels_it():
    """pains[].who_feels is plural; problems[].persona was singular, which made
    two of five problems unsellable to half the people who have them."""
    p = {**OFFER["problems"][0]}
    del p["personas"]
    p["persona"] = "champion"
    assert errs(offer(problems=[p])) != []


def test_an_unknown_persona_role_is_rejected():
    assert errs(offer(problems=[{**OFFER["problems"][0], "personas": ["procurement"]}])) != []


def test_a_problem_must_name_the_pain_it_sells():
    p = {k: v for k, v in OFFER["problems"][0].items() if k != "pain_id"}
    assert any("pain_id" in e for e in errs(offer(problems=[p])))


# --- front-end rows -----------------------------------------------------------

def test_every_front_end_offer_needs_a_path_to_yes():
    """The $5-10k desk audit had one. The $10-25k in-VPC audit, which needs a
    security review, did not - the higher-friction ask shipped with no route
    through its own friction, and the cut list named it as the touch-1 ask."""
    f = {k: v for k, v in OFFER["front_end_offers"][0].items() if k != "acceptance_path"}
    assert any("acceptance_path" in e for e in errs(offer(front_end_offers=[f])))


def test_a_front_end_offer_may_not_restate_the_problem_signals():
    """Both arrays held the same six values. The row reaches its signals through
    `reveals`; two copies drift."""
    f = {**OFFER["front_end_offers"][0], "signals": ["job_posting_intent"]}
    assert errs(offer(front_end_offers=[f])) != []


def test_a_front_end_offer_must_reveal_a_problem():
    f = {k: v for k, v in OFFER["front_end_offers"][0].items() if k != "reveals"}
    assert any("reveals" in e for e in errs(offer(front_end_offers=[f])))


def test_standalone_price_is_required_because_gate_q11_needs_a_number():
    f = {k: v for k, v in OFFER["front_end_offers"][0].items() if k != "standalone_price"}
    assert any("standalone_price" in e for e in errs(offer(front_end_offers=[f])))


# --- capacity has one home ----------------------------------------------------

def test_economics_must_separate_concurrency_from_throughput():
    """provenance [O4] states both: "2 concurrent in-VPC slots, ~3/quarter".
    Written as "2 concurrent slots per quarter" they read as one number stated
    twice, which is how the file appeared to say 2 and 3 for the same thing."""
    e = {k: v for k, v in OFFER["economics"].items() if k != "vpc_concurrent_slots"}
    assert any("vpc_concurrent_slots" in x for x in errs(offer(economics=e)))


def test_the_capacity_number_is_checked_across_the_file():
    """JSON Schema cannot compare prose to a field, so this is validate.py."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from validate import numbers_agree
    import tempfile, os
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "04-offer"))
        bad = offer(scarcity_facts=["in-VPC shadow audits run 5 concurrent slots"])
        json.dump(bad, open(os.path.join(d, "04-offer", "offer.json"), "w"))
        assert any("concurrent" in x for x in numbers_agree(d))


# --- the warm-first gate ------------------------------------------------------

def test_zero_proof_requires_a_warm_first_plan():
    """No volume of cold email fixes a proof problem that 3-5 free warm
    deliveries solve."""
    d = offer(proof_inventory={"case_studies": 0, "testimonials": 0})
    assert any("warm_first_plan" in e for e in errs(d))


def test_a_warm_plan_carries_named_paths_not_a_count():
    """The artifact carried `count: 5` beside four named paths. A number next to
    a list it can contradict is the same defect as every other duplicated fact,
    so the count is now the length of the list."""
    d = offer(proof_inventory={"case_studies": 0, "testimonials": 0},
              warm_first_plan={"count": 5, "source": "warm_universe",
                               "term": "free audit for a named logo, agreed in writing",
                               "status": "approved"})
    assert errs(d) != []


def test_a_complete_warm_plan_validates():
    paths = [{"who": f"path {n}", "path": "traceable to company.json warm_universe", "state": "untried"}
             for n in range(3)]
    d = offer(proof_inventory={"case_studies": 0, "testimonials": 0},
              warm_first_plan={"source": "company.json warm_universe",
                               "term": "free audit for a named logo plus case study, agreed in writing",
                               "status": "approved", "named_paths": paths})
    assert errs(d) == []


# --- the judgment surface -----------------------------------------------------

def test_all_twelve_gate_questions_are_required():
    """The skill listed 11 while the artifact answered 12; the twelfth
    (acceptance obstacles) comes from the belief-weak doctrine and is real."""
    g = {k: v for k, v in OFFER["gate_answers"].items() if k != "q12_acceptance_obstacles"}
    assert any("q12" in e for e in errs(offer(gate_answers=g)))


def test_rationale_and_cut_list_are_required():
    """The JSON is the reviewable artifact - there is no .md companion - so the
    human cannot judge an offer whose reasoning and discards are absent."""
    assert any("rationale" in e for e in errs({k: v for k, v in OFFER.items() if k != "rationale"}))
    assert any("cut_list" in e for e in errs({k: v for k, v in OFFER.items() if k != "cut_list"}))


def test_a_confirmed_offer_records_who_confirmed_it():
    assert errs(offer(status="confirmed")) != []


def test_an_invented_signal_id_is_rejected():
    assert errs(offer(problems=[{**OFFER["problems"][0], "signals": ["vibes_positive"]}])) != []


def test_the_signal_taxonomy_matches_the_icp_exactly():
    """Two copies of an enum is how the offer's list silently gained three
    invented signals and lost six real ones while nothing failed."""
    icp = json.loads((Path(__file__).resolve().parent.parent /
                      "gtme-icp" / "icp.schema.json").read_text())
    assert SCHEMA["$defs"]["signalId"]["enum"] == icp["$defs"]["signalId"]["enum"]


# --- migration signal ---------------------------------------------------------

def test_live_artifact_validates():
    assert errs(json.loads(RUN.read_text())) == []
