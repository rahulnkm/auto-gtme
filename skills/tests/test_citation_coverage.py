import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILLS))
from validate import orphaned_citations, dangling_citations  # noqa: E402

PROV = """
[1] "quoted thing", Source (https://a.example), pulled 2026-08-02.

[2] "another", Source (https://b.example), pulled 2026-08-02.

[3] "unused on purpose", Source (https://c.example), pulled 2026-08-02. UNUSED: superseded by [1], same claim better sourced.
"""


def test_referenced_and_marked_citations_are_clean():
    assert orphaned_citations('{"a": ["[1]", "[2]"]}', PROV) == []


def test_an_unreferenced_unmarked_citation_is_reported():
    assert orphaned_citations('{"a": ["[1]"]}', PROV) == ["2"]


def test_a_marked_citation_stays_clean_even_when_unreferenced():
    """UNUSED is the escape hatch: a decision on the record, not silence."""
    assert "3" not in orphaned_citations('{"a": []}', PROV)


def test_a_citation_used_but_never_defined_is_reported_separately():
    assert dangling_citations('{"a": ["[9]"]}', PROV) == ["9"]


def test_no_provenance_means_nothing_to_check():
    assert orphaned_citations('{"a": 1}', "") == []
    assert dangling_citations('{"a": 1}', "") == []


def test_a_reference_inside_the_provenance_reason_does_not_count_as_use():
    """[3]'s reason mentions [1]. That is bookkeeping, not the artifact using [1]."""
    assert orphaned_citations('{"a": ["[2]"]}', PROV) == ["1"]


PREFIXED = """
[O1] "offer-specific claim", Vendr (https://v.example), pulled 2026-08-02.

[O2] "another", Vendr (https://w.example), pulled 2026-08-02.
"""


def test_stage_prefixed_ids_are_parsed():
    """06-offer/provenance.md numbers its entries [O1], [O2]. A digits-only parser
    silently sees zero entries there and reports a clean file."""
    assert orphaned_citations('{"a": ["[O1]"]}', PREFIXED) == ["O2"]


WRAPPED_PROSE = """
Company metrics resolve in ../company/provenance.md ([2] site metric,
[4] a post, [5] another post). Entries below cover the rest.

[O1] "the only real entry", Source (https://a.example), pulled 2026-08-02.
"""


def test_a_prose_line_wrapping_onto_a_bracket_is_not_an_entry():
    """Real case: a header paragraph wrapped so a line began '[4] a post', which a
    line-start parser counted as a definition and then reported as orphaned."""
    assert orphaned_citations('{"a": ["[O1]"]}', WRAPPED_PROSE) == []
