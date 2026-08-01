import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA = json.loads(
    (Path(__file__).resolve().parent.parent / "gtme-company" / "company.schema.json").read_text())
V = Draft202012Validator(SCHEMA)
RUN = Path(__file__).resolve().parent.parent.parent / "runs" / "mousecat" / "company" / "company.json"


def errs(doc):
    return [f"{list(e.absolute_path)}: {e.message}" for e in V.iter_errors(doc)]


def doc(**over):
    """The live fingerprint is the fixture: if a schema change breaks a real
    artifact, the test says so before the run does."""
    return {**json.loads(RUN.read_text()), **over}


def test_live_artifact_validates():
    assert errs(doc()) == []


# --- positioning_history ---------------------------------------------------

def test_positioning_history_accepts_current_prior_and_removals():
    assert errs(doc(positioning_history={
        "current": {"text": "Agentic AI Infrastructure for Risk Operations", "cites": ["[1]"]},
        "prior": [{"as_of": "2026-03", "text": "AI that investigates like your best analyst",
                   "cites": ["[21]"]}],
        "removed_claims": [{"claim": "'Works with' logo wall including Alloy",
                            "removed_between": "2026-03/2026-07", "cites": ["[21]"]}],
    })) == []


def test_positioning_history_rejects_removal_without_cites():
    bad = errs(doc(positioning_history={
        "current": {"text": "x", "cites": ["[1]"]}, "prior": [],
        "removed_claims": [{"claim": "no citation on this one",
                            "removed_between": "2026-03/2026-07"}],
    }))
    assert any("cites" in e for e in bad)


# --- go_to_market ----------------------------------------------------------

def test_go_to_market_accepts_a_sales_led_shape():
    assert errs(doc(go_to_market={
        "motion": "sales_led", "pricing_public": False, "docs_public": False,
        "entry_point": "book-a-demo form to founder inbox", "cites": ["[1]"],
    })) == []


def test_go_to_market_rejects_an_invented_motion():
    bad = errs(doc(go_to_market={
        "motion": "viral", "pricing_public": False, "docs_public": False,
        "entry_point": "x", "cites": ["[1]"],
    }))
    assert any("motion" in e or "viral" in e for e in bad)


# --- stage.compliance ------------------------------------------------------

def test_compliance_accepts_certifications_and_vocabulary():
    d = doc()
    d["stage"] = {**d["stage"], "compliance": {
        "certifications": [{"name": "SOC 2", "status": "in_progress",
                            "via": "Oneleet", "cites": ["[14]"]}],
        "regulatory_vocabulary": "absent",
    }}
    assert errs(d) == []


def test_compliance_rejects_a_bare_string():
    d = doc()
    d["stage"] = {**d["stage"], "compliance": "SOC 2 in progress via Oneleet"}
    assert errs(d) != []


# --- credibility verification ----------------------------------------------

def test_credibility_accepts_disproven():
    d = doc()
    d["credibility"] = d["credibility"] + [{
        "marker": "press", "claim": "Aggregator listed 9 customer logos",
        "cites": ["[22]"], "verification": "disproven",
    }]
    assert errs(d) == []
