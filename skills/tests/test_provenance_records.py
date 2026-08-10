"""Structured provenance: quote bound to source, authenticity enforced, derivation declared.

Every case here is a real failure from a live run, not a hypothetical. The
markdown-only provenance these checks sit beside was well-formed and fully
referenced through all of them.
"""
import json
import pytest

from validate import (
    authenticity_violations,
    derived_unflagged,
    distillation_gaps,
    RESEARCH_FILE,
)


def src(i, **kw):
    base = {
        "id": i,
        "quote": "the backlog never goes to zero",
        "source_url": "https://example.test/thread/1",
        "pulled": "2026-08-08",
        "authenticity": "organic",
    }
    base.update(kw)
    return base


class TestAuthenticity:
    def test_organic_citation_passes(self):
        doc = {"pains": [{"evidence": ["[1]"]}]}
        assert authenticity_violations(doc, [src("[1]")]) == []

    def test_vendor_authored_source_cannot_be_cited(self):
        """The live failure: three vendor-seeded threads from one marketing
        campaign cited as buyer evidence, while the artifact asserted in prose
        that no vendor material had been used."""
        doc = {"pains": [{"evidence": ["[1]"]}]}
        assert authenticity_violations(doc, [src("[1]", authenticity="vendor")]) == ["[1]"]

    def test_astroturf_is_also_refused(self):
        doc = {"awareness": {"default": {"evidence": ["[7]"]}}}
        assert authenticity_violations(doc, [src("[7]", authenticity="astroturf")]) == ["[7]"]

    def test_recorded_but_uncited_vendor_source_is_fine(self):
        """Recording vendor material is legal. Quoting it as buyer voice is not."""
        doc = {"pains": [{"evidence": ["[2]"]}]}
        entries = [src("[1]", authenticity="vendor", unused_reason="vendor-seeded, kept for context"),
                   src("[2]")]
        assert authenticity_violations(doc, entries) == []

    def test_official_and_first_party_are_quotable(self):
        doc = {"pains": [{"evidence": ["[1]", "[2]"]}]}
        entries = [src("[1]", authenticity="official"), src("[2]", authenticity="first_party")]
        assert authenticity_violations(doc, entries) == []

    def test_violations_sort_numerically(self):
        doc = {"e": ["[2]", "[10]"]}
        entries = [src("[10]", authenticity="vendor"), src("[2]", authenticity="vendor")]
        assert authenticity_violations(doc, entries) == ["[2]", "[10]"]


class TestDerived:
    def test_stated_figure_needs_no_flag(self):
        doc = {"constants": [{"name": "cups_per_jug", "value": 12, "source": "[1]"}]}
        assert derived_unflagged(doc) == []

    def test_derived_figure_must_say_what_it_came_from(self):
        """The live failure: 640,000 / 16,000,000 published as a sourced 4%."""
        doc = {"constants": [{"name": "conversion", "value": 4, "source": "[12]", "derived": True}]}
        assert len(derived_unflagged(doc)) == 1

    def test_derived_with_arithmetic_declared_passes(self):
        doc = {"constants": [{"name": "conversion", "value": 4, "source": "[12]",
                              "derived": True, "derived_from": "sars_filed / alerts_reviewed"}]}
        assert derived_unflagged(doc) == []

    def test_finds_derivations_nested_anywhere(self):
        doc = {"pains": [{"gap_math": {"constants": [
            {"name": "x", "value": 1, "source": "[1]", "derived": True}]}}]}
        assert len(derived_unflagged(doc)) == 1


class TestDistillationIsNotCompanyOnly:
    def test_market_stage_has_a_research_contract(self):
        """The asymmetry this closes: one run produced zero citation faults in the
        stage with a distillation contract and four in the stage without."""
        assert "market" in RESEARCH_FILE
        assert "company" in RESEARCH_FILE

    def test_research_file_lives_inside_the_run(self):
        """Not in a scratchpad. A run must be auditable without the session."""
        for stage, rel in RESEARCH_FILE.items():
            assert rel.startswith(("01-", "02-")), rel
            assert "tmp" not in rel and "scratch" not in rel

    def test_unaccounted_market_section_fails(self):
        research = {"reddit_voc": {}, "audio_voc": {},
                    "distillation": {"mapped": [{"section": "reddit_voc"}], "excluded": []}}
        assert distillation_gaps(research) == ["audio_voc"]

    def test_excluded_with_a_reason_is_accounted(self):
        research = {"reddit_voc": {}, "audio_voc": {},
                    "distillation": {"mapped": [{"section": "reddit_voc"}],
                                     "excluded": [{"section": "audio_voc", "reason": "targeting, not pain"}]}}
        assert distillation_gaps(research) == []


class TestExampleIsNotCopyable:
    """The skill's worked example must be impossible to paste into a real artifact
    and still look right. A previous example was a fraud/AML map carried over from
    a live client run; a later run copied a whole pain out of it verbatim, id and
    all, and described it as the best-attested pain in its corpus."""

    def test_market_pain_example_is_obviously_a_toy(self, skills_dir=None):
        import os
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        text = open(os.path.join(here, "gtme-market-pain", "SKILL.md")).read()
        assert "lemonade" in text.lower()
        for leaked in ("pain:unworked_backlog", "crypto-exchange, fintech",
                       "feat:end_to_end_investigation", "cases_per_analyst_day"):
            assert leaked not in text, f"real-domain example content still present: {leaked}"

    def test_example_still_demonstrates_the_hard_fields(self):
        import os
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        text = open(os.path.join(here, "gtme-market-pain", "SKILL.md")).read()
        for shown in ("felt_evidence", "derived", "derived_from", "unanswered_note",
                      "evidence_class", "findable", "complaints"):
            assert shown in text, f"example no longer shows {shown}"
