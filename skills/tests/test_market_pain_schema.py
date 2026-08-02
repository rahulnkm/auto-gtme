"""The market-pain contract, tested against a synthetic map.

The fixture is built here rather than read from a run: a live artifact is
campaign data that legitimately changes, and pinning assertions to it turns a
data edit into a code failure. test_live_artifact_validates is the one
deliberate exception - it is the migration signal, and it is allowed to fail
loudly while a run is mid-migration.
"""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA = json.loads((Path(__file__).resolve().parent.parent /
                     "gtme-market-pain" / "market-pain.schema.json").read_text())
V = Draft202012Validator(SCHEMA)
RUN = Path(__file__).resolve().parent.parent.parent / "runs" / "mousecat" / "04-market" / "market-pain.json"


def errs(d):
    return [f"{list(e.absolute_path)}: {e.message}" for e in V.iter_errors(d)]


PAIN = {
    "id": "pain:unworked_backlog",
    "statement": "we only work a fraction of the queue and hope the rest is noise",
    "shape": {
        "surface": "the backlog never goes to zero",
        "operational": "sampled-out cases are unmeasured loss",
        "personal": "the miss with my name on it",
    },
    "workflow": "alerts land in Unit21, worked oldest-first against a per-analyst quota",
    "confidence": "high",
    "type": "felt",
    "felt_evidence": "26 of 61 mapped accounts have live fraud-investigator postings",
    "who_feels": ["champion", "economic_buyer"],
    "segments": ["crypto-exchange", "fintech"],
    "evidence": ["[3]", "[7]"],
    "dream_outcome": {"champion": "queue at zero by Friday"},
    "feature_ref": "feat:end_to_end_investigation",
    "gap_math": {
        "observables": [{"name": "analyst_count", "findable": "public", "how": "LinkedIn title count"},
                        {"name": "alert_volume", "findable": "must_ask"}],
        "constants": [{"name": "cases_per_analyst_day", "value": 30, "unit": "cases",
                       "source": "[15]", "evidence_class": "vendor_consensus"}],
    },
}

MAP = {
    "status": "draft",
    "harvested_at": "2026-08-02",
    "sources_swept": ["review sites", "practitioner communities"],
    "pains": [PAIN],
    "tried_and_failed": [{"approach": "rules engines", "disappointment": "still manual casework",
                          "evidence": ["[4]"]}],
    "predicted_objections": [{"id": "obj1", "answered_by": "problems:p1", "persona": "technical_evaluator",
                              "objection": "our risk-eng team will build this", "evidence": ["[9]"]}],
    "awareness": {"fintech": {"level": "solution_aware", "evidence": ["[44]"]},
                  "default": {"level": "problem_aware",
                              "rationale": "segments enter the ICP faster than awareness is researched, and the two registers produce opposite emails"}},
    "pain_keywords": ["alert backlog"],
    "market_pain_stats": [{"stat": ">90% of alerts are false positives", "source": "vendor-cluster consensus",
                           "scope": "rules-based transaction monitoring", "citation": "[32]"}],
    "market_verdict": {"pain": 9, "pain_evidence": "hiring against it",
                       "purchasing_power": 9, "purchasing_power_evidence": "incumbent ACV ~$160K",
                       "targetability": 8, "targetability_evidence": "public postings",
                       "growth": "growing", "growth_evidence": "category leader rebuilt around agents",
                       "verdict": "proceed"},
}


def pain(**over):
    return {**MAP, "pains": [{**PAIN, **over}]}


def mp(**over):
    return {**MAP, **over}


def test_a_complete_map_validates():
    assert errs(MAP) == []


# --- the fields gtme-write and gtme-icp actually read -----------------------

def test_statement_and_shape_are_required():
    """gtme-write reads statement/shape as the reader's own language. The artifact
    shipped with 'pain' and 'their_words' instead, so the contract was broken in
    production and nothing caught it."""
    d = pain()
    d["pains"][0].pop("statement"); d["pains"][0].pop("shape")
    assert len(errs(d)) >= 2


def test_the_personal_rung_is_mandatory():
    """Emotional-layer copy is written against it, and it is the hardest evidence
    class to find - which is exactly why it gets dropped without a rule."""
    d = pain(shape={"surface": "s", "operational": "o"})
    assert any("personal" in e for e in errs(d))


def test_segments_are_required_because_icp_derives_tiers_from_them():
    d = pain()
    d["pains"][0].pop("segments")
    assert any("segments" in e for e in errs(d))


# --- felt vs latent ---------------------------------------------------------

def test_a_felt_pain_needs_two_independent_citations():
    """One quote is an anecdote."""
    assert errs(pain(evidence=["[3]"])) != []


def test_a_felt_pain_needs_felt_evidence():
    d = pain()
    d["pains"][0].pop("felt_evidence")
    assert any("felt_evidence" in e for e in errs(d))


def test_a_latent_pain_may_carry_one_citation():
    """felt needs two independent citations; latent is the gap the seller reveals,
    so one is enough and felt_evidence does not apply."""
    d = pain(type="latent", evidence=["[3]"])
    d["pains"][0].pop("felt_evidence")
    assert errs(d) == []


def test_a_latent_pain_must_name_what_reveals_it():
    """A latent pain with no revealing capability is a guess, not a wedge."""
    d = pain(type="latent", feature_ref=None)
    d["pains"][0].pop("felt_evidence")
    assert any("feature_ref" in e or "null" in e.lower() for e in errs(d))


# --- feature_ref ------------------------------------------------------------

def test_feature_ref_accepts_a_platform_property_id():
    assert errs(pain(feature_ref="prop:vpc_deploy")) == []


def test_feature_ref_rejects_a_free_text_feature_name():
    assert errs(pain(feature_ref="the investigation agent")) != []


def test_feature_ref_may_be_null_for_a_felt_pain_no_capability_kills():
    """Legal, and a finding: the pain is content-only or disqualifying."""
    assert errs(pain(feature_ref=None)) == []


# --- gap_math ---------------------------------------------------------------

def test_gap_math_is_a_computable_model_not_a_sentence():
    """A prose figure cannot produce 'your 12 analysts x 30 cases/day'."""
    assert errs(pain(gap_math={"text": "analysts cost about $85K/yr", "cites": ["[33]"]})) != []


def test_a_gap_math_constant_must_cite_its_source():
    d = pain(gap_math={"observables": [{"name": "analyst_count", "findable": "public", "how": "LinkedIn title count"}],
                       "constants": [{"name": "cases_per_analyst_day", "value": 30}]})
    assert any("source" in e for e in errs(d))


def test_a_constant_must_declare_how_much_weight_it_carries():
    """Two authoritative-sounding minutes-per-alert benchmarks in circulation both
    trace to one vendor blog with no findable paper. A number that reaches copy
    wearing a citation, when it is really a guess, is the failure this prevents."""
    d = pain(gap_math={"observables": [{"name": "analyst_count", "findable": "public", "how": "LinkedIn title count"}],
                       "constants": [{"name": "minutes_per_alert", "value": 30, "source": "[31]"}]})
    assert any("evidence_class" in e for e in errs(d))


def test_an_assumption_is_a_legal_evidence_class():
    """Declaring the guess is allowed; disguising it is not."""
    d = pain(gap_math={"observables": [{"name": "analyst_count", "findable": "public", "how": "LinkedIn title count"}],
                       "constants": [{"name": "minutes_per_alert", "value": 30,
                                      "source": "[31]", "evidence_class": "assumption"}]})
    assert errs(d) == []


def test_an_unknown_persona_is_rejected():
    assert errs(pain(who_feels=["procurement"])) != []


def test_a_stat_without_scope_is_rejected():
    d = {**MAP, "market_pain_stats": [{"stat": "x", "source": "y", "citation": "[1]"}]}
    assert any("scope" in e for e in errs(d))


# --- migration signal -------------------------------------------------------

def test_live_artifact_validates():
    assert errs(json.loads(RUN.read_text())) == []


# --- the audit findings, as rules -------------------------------------------

def test_an_observable_must_say_whether_a_stranger_can_get_it():
    """constants[] carried source and evidence_class while observables[] was three
    bare words - and two of the three only exist inside the account. Unmarked, a
    writer invents them or drops the math."""
    d = pain(gap_math={"observables": [{"name": "alert_volume_monthly"}], "constants": []})
    assert any("findable" in e for e in errs(d))


def test_a_public_observable_must_say_where_it_is_found():
    d = pain(gap_math={"observables": [{"name": "analyst_count", "findable": "public"}], "constants": []})
    assert any("how" in e for e in errs(d))


def test_a_must_ask_observable_needs_no_how():
    d = pain(gap_math={"observables": [{"name": "backlog_age_days", "findable": "must_ask"}], "constants": []})
    assert errs(d) == []


def test_an_objection_must_name_what_answers_it_or_admit_nothing_does():
    """Five evidenced objections sat in this artifact and nothing read them.
    answered_by is what gives gtme-write something to resolve against."""
    o = {k: v for k, v in MAP["predicted_objections"][0].items() if k != "answered_by"}
    assert any("answered_by" in e for e in errs(mp(predicted_objections=[o])))


def test_an_unanswered_objection_must_say_so_out_loud():
    """Null is legal - the champion's job-security objection genuinely has no
    answer - but it has to be stated, because gtme-write must then avoid writing
    copy that walks into it."""
    o = {**MAP["predicted_objections"][0], "answered_by": None}
    assert any("unanswered_note" in e for e in errs(mp(predicted_objections=[o])))
    o["unanswered_note"] = "no offer element addresses this; do not raise it and do not write efficiency copy"
    assert errs(mp(predicted_objections=[o])) == []


def test_awareness_must_carry_a_default():
    """Four of eight targeted segments had no awareness level and no fallback,
    so the writer guessed between two opposite registers."""
    assert any("default" in e for e in errs(mp(awareness={"fintech": MAP["awareness"]["fintech"]})))
