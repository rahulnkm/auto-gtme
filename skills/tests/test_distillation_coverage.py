import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILLS))
from validate import distillation_gaps  # noqa: E402


def research(**over):
    return {"subject": "x", "team": {}, "funding": {}, "founder_hooks": {}, **over}


def test_every_section_mapped_or_excluded_is_clean():
    assert distillation_gaps(research(distillation={
        "mapped":   [{"section": "team", "to": "team"},
                     {"section": "funding", "to": "stage.rounds"}],
        "excluded": [{"section": "founder_hooks", "reason": "raw material for gtme-write"}],
    })) == []


def test_an_unaccounted_section_is_reported():
    gaps = distillation_gaps(research(distillation={
        "mapped":   [{"section": "team", "to": "team"}],
        "excluded": [{"section": "founder_hooks", "reason": "raw material"}],
    }))
    assert gaps == ["funding"]


def test_missing_distillation_block_reports_every_section():
    assert distillation_gaps(research()) == ["founder_hooks", "funding", "team"]


def test_the_live_research_file_is_fully_accounted():
    import json
    path = SKILLS.parent / "runs" / "mousecat" / "company" / "seller-research.json"
    assert distillation_gaps(json.loads(path.read_text())) == []
