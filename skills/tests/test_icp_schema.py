"""The ICP contract, tested against a synthetic filter.

Built here rather than read from a run: a live artifact is campaign data that
legitimately changes. test_live_artifact_validates is the one exception - it is
the migration signal and may fail loudly while a run is mid-migration.
"""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA = json.loads((Path(__file__).resolve().parent.parent /
                     "gtme-icp" / "icp.schema.json").read_text())
V = Draft202012Validator(SCHEMA)
RUN = Path(__file__).resolve().parent.parent.parent / "runs" / "mousecat" / "03-icp" / "icp.json"


def errs(d):
    return [f"{list(e.absolute_path)}: {e.message}" for e in V.iter_errors(d)]


ICP = {
    "status": "confirmed", "confirmed_by": "Rahul", "confirmed_at": "2026-08-03",
    "objective": "source every plausible fraud-tooling buyer, exclude provable dead ends, rank by signal",
    "tiers": [{"tier": 1, "allocation": 0.6, "company_type": ["fintech"],
               "employee_count": {"min": 50, "max": 10000},
               "sub_team": {"metric": "fraud_risk_ops", "min": 2},
               "stages": ["series-b"], "geos": ["US"]}],
    "geo_exception": "non-US HQ qualifies if it contracts via a US entity and procures in English",
    "budget_evidence_any_of": ["raised within 48 months", "active fraud hiring", "pays a fraud vendor today"],
    "disqualifiers": [
        {"id": "depository_charter",
         "rule": "any entity licensed to take customer deposits, any jurisdiction",
         "why_impossible": "bank-style model approval and procurement outrun a three-person company's runway",
         "cites": ["[I2]"]}],
    "scoring": {
        "weight_signals_over_firmographics": True,
        "boosts": [{"signal": "job_posting_intent", "weight": "highest",
                    "detail": "live fraud analyst postings", "cites": ["[I5]"]}],
        "demotions": [{"signal": "li_follow_ours", "weight": "low"}],
        "pain_boost": "strong boost when 2+ fraud-role postings in 6 months"},
    "personas": [{"role": "economic_buyer",
                  "identify_by": {
                      "function": "owns the fraud loss number and the budget for the team that works it",
                      "seniority": "director..c_level",
                      "title_examples": ["Chief Risk Officer"],
                      "title_keywords": ["fraud", "fincrime"],
                      "not_keywords": ["credit risk", "information security"]},
                  "cares_about": ["pain:unworked_backlog", "pain:fraud_losses"],
                  "first_touch": True, "cites": ["[I1]"]}],
    "contacts_per_account": {"default": 2, "high_value": 3, "low_value": 1},
    "seed_targets": [{"name": "Mercury", "tier": 1,
                      "qualifying_signal": "job_posting_intent", "cites": ["[I5]"]}],
}


def icp(**over):
    return {**ICP, **over}


def test_a_complete_icp_validates():
    assert errs(ICP) == []


# --- disqualifiers: the shape change ---------------------------------------

def test_disqualifiers_reject_the_old_dict_shape():
    """The dict of bool|string|array could not be validated, could not carry a
    reason, and hid a duplicate bank rule for weeks."""
    assert errs(icp(disqualifiers={"depository_charter": True, "company_type": ["agency"]})) != []


def test_a_disqualifier_must_say_why_a_deal_is_impossible():
    """The skill demands 'impossible, not improbable'. The dict shape had nowhere
    to put that, so it was never written."""
    d = icp(disqualifiers=[{"id": "x", "rule": "y", "cites": ["[I2]"]}])
    assert any("why_impossible" in e for e in errs(d))


def test_a_disqualifier_must_carry_evidence():
    d = icp(disqualifiers=[{"id": "x", "rule": "y", "why_impossible": "z"}])
    assert any("cites" in e for e in errs(d))


def test_duplicate_disqualifier_ids_are_caught_by_the_validator():
    """JSON Schema cannot express unique-by-property, so this is validate.py's
    unique_ids walk - the same check that guards company.json's feat:/prop: ids.
    Recorded here because the live artifact really did state the bank exclusion
    twice, under two different names."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from validate import unique_ids
    d = icp(disqualifiers=[
        {"id": "dup", "rule": "a", "why_impossible": "a", "cites": ["[I2]"]},
        {"id": "dup", "rule": "b", "why_impossible": "b", "cites": ["[I2]"]}])
    assert unique_ids(d) == ["dup"]


# --- cites on empirical claims ---------------------------------------------

def test_a_persona_must_cite_where_its_titles_were_observed():
    """title_examples claims these titles exist in real org charts. That is
    checkable, so it is a claim, not a choice."""
    p = {k: v for k, v in ICP["personas"][0].items() if k != "cites"}
    assert any("cites" in e for e in errs(icp(personas=[p])))


def test_a_boost_may_carry_cites():
    assert errs(icp(scoring={**ICP["scoring"], "boosts": [
        {"signal": "press_mention", "weight": "high",
         "detail": "fine within 6 months, only if fraud org >= 10 people",
         "cites": ["[I6]"]}]})) == []


def test_exactly_one_persona_is_first_touch():
    d = icp(personas=[{**ICP["personas"][0], "first_touch": True},
                      {**ICP["personas"][0], "role": "champion", "first_touch": True}])
    assert errs(d) != []


# --- filter discipline ------------------------------------------------------

def test_an_invented_signal_id_is_rejected():
    """watch_signals come from the taxonomy; a run-invented string breaks scoring."""
    d = icp(scoring={**ICP["scoring"], "boosts": [
        {"signal": "vibes_positive", "weight": "high", "detail": "x"}]})
    assert errs(d) != []


def test_sub_team_takes_a_floor_and_no_cap():
    """A size cap is scoring's job, never the filter's."""
    d = icp(tiers=[{**ICP["tiers"][0], "sub_team": {"metric": "fraud_risk_ops", "min": 2, "max": 50}}])
    assert errs(d) != []


def test_an_unknown_persona_role_is_rejected():
    assert errs(icp(personas=[{**ICP["personas"][0], "role": "procurement"}])) != []


# --- migration signal -------------------------------------------------------

def test_live_artifact_validates():
    assert errs(json.loads(RUN.read_text())) == []


# --- identify_by: state the job, not the list of titles ---------------------

def test_a_persona_must_say_what_the_person_actually_does():
    """A list of titles cannot teach a reader what it is a list OF, so an
    unlisted title is unrecognisable - the way a search for "Software Engineer"
    at Anthropic misses "Member of Technical Staff". gtme-enrich substitutes
    against `function`, and before this field existed it was told to find "the
    closest revenue-owning exec", left over from a different seller."""
    p = {k: v for k, v in ICP["personas"][0]["identify_by"].items() if k != "function"}
    assert any("function" in e for e in errs(icp(personas=[{**ICP["personas"][0], "identify_by": p}])))


def test_a_persona_must_say_which_titles_are_the_wrong_person():
    """"risk" at a lending company returns credit, market, enterprise and
    information-security risk, none of whom hold a fraud queue."""
    p = {k: v for k, v in ICP["personas"][0]["identify_by"].items() if k != "not_keywords"}
    assert any("not_keywords" in e for e in errs(icp(personas=[{**ICP["personas"][0], "identify_by": p}])))


def test_the_old_per_segment_title_table_is_rejected():
    """It implied a completeness it could never have: eight targeted company
    types, titles for three, and nothing reporting the gap."""
    p = {**ICP["personas"][0], "titles_by_segment": {"fintech": ["Chief Risk Officer"]}}
    assert errs(icp(personas=[p])) != []


# --- cares_about points at pains instead of paraphrasing them ---------------

def test_cares_about_must_be_pain_ids():
    """Nine hand-typed phrases restated pains that who_feels already assigns,
    and the two copies had already drifted: "analyst burnout" is a symptom, not
    a pain id, and one persona listed three items where the map yields two."""
    d = icp(personas=[{**ICP["personas"][0], "cares_about": ["review backlog", "analyst burnout"]}])
    assert errs(d) != []


# --- seeds carry the reason they were picked -------------------------------

def test_a_seed_must_carry_its_tier_and_qualifying_signal():
    """Bare names left nothing to check, which is how a chartered bank sat in
    the seed list of an ICP that disqualifies chartered banks."""
    assert errs(icp(seed_targets=["Mercury"])) != []


def test_a_seed_declaring_a_disqualifier_is_caught():
    """JSON Schema cannot cross-reference two arrays, so this is validate.py."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from validate import seeds_pass_disqualifiers
    d = icp(seed_targets=[{"name": "Lead Bank", "tier": 2, "qualifying_signal": "job_posting_intent",
                           "cites": ["[I5]"], "excluded_by": "depository_charter"}])
    assert seeds_pass_disqualifiers(d) != []
