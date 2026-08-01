import json
from pathlib import Path
from jsonschema import Draft202012Validator

SCHEMA = json.loads((Path(__file__).resolve().parent.parent /
                     "gtme-market-pain" / "market-pain.schema.json").read_text())
V = Draft202012Validator(SCHEMA)
RUN = Path(__file__).resolve().parent.parent.parent / "runs" / "mousecat" / "market" / "market-pain.json"


def errs(d):
    return [f"{list(e.absolute_path)}: {e.message}" for e in V.iter_errors(d)]


def doc(**over):
    return {**json.loads(RUN.read_text()), **over}


def test_live_artifact_validates():
    assert errs(doc()) == []


def test_a_pain_without_evidence_is_rejected():
    d = doc()
    d["pains"] = [{k: v for k, v in d["pains"][0].items() if k != "evidence"}]
    assert errs(d) != []


def test_gap_math_must_carry_its_own_cites():
    """The dollar figure that makes a pain 'expensive' is exactly the number a
    buyer pushes back on, so it cannot be a bare string."""
    d = doc()
    d["pains"] = [{**d["pains"][0], "gap_math": "analysts cost about $85K/yr"}]
    assert errs(d) != []


def test_awareness_requires_evidence_for_its_label():
    assert errs(doc(awareness={"fintech": {"level": "solution_aware"}})) != []


def test_awareness_with_evidence_passes():
    assert errs(doc(awareness={"fintech": {"level": "solution_aware", "evidence": ["[44]"]}})) == []


def test_an_invented_awareness_level_is_rejected():
    assert errs(doc(awareness={"fintech": {"level": "very_aware", "evidence": ["[44]"]}})) != []


def test_named_vendor_complaints_are_accepted_on_a_tried_and_failed_row():
    d = doc()
    d["tried_and_failed"] = [{**d["tried_and_failed"][0], "complaints": [
        {"vendor": "Forter", "verbatim": "Merchants do not have much control over the decisioning logic.",
         "cites": ["[13]"]}]}]
    assert errs(d) == []


def test_a_complaint_without_a_vendor_is_rejected():
    d = doc()
    d["tried_and_failed"] = [{**d["tried_and_failed"][0], "complaints": [
        {"verbatim": "some gripe", "cites": ["[13]"]}]}]
    assert errs(d) != []


def test_an_unknown_persona_is_rejected():
    d = doc()
    d["pains"] = [{**d["pains"][0], "who_feels": ["procurement"]}]
    assert errs(d) != []


def test_a_stat_without_scope_is_rejected():
    """A stat quoted outside its scope is how a defensible number becomes an
    indefensible one."""
    d = doc()
    d["market_pain_stats"] = [{k: v for k, v in d["market_pain_stats"][0].items() if k != "scope"}]
    assert errs(d) != []
