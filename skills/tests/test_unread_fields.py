"""The admission test, rule 2, made checkable.

`artifact-design.md` states it: "A named downstream stage reads it. Every field
holds its seat by a consumer. No consumer, no seat." The rule was written and
never enforced, so eight fields accumulated across four artifacts - the buyer's
predicted objections, the sourced market statistics, the practitioner keyword
list, the offer's proof levers, the seed accounts - each researched, written,
and read by nothing.

This is the third check of its family. `distillation_gaps` exists because schema
validation catches an invented field and is blind to a dropped one.
`orphaned_citations` exists because a third of one stage's evidence was gathered
and silently unused. Both make an unexplained drop impossible to do quietly;
neither can see a field that has no reader at all.
"""
import sys
from pathlib import Path

import pytest

SKILLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILLS))
from conftest import live_runs  # noqa: E402
from validate import (unread_fields, numbers_agree, PIPELINE, STAGE_SKILL,  # noqa: E402
                      UNREAD_OK, WAVES, FOLDER, ROOT_FILE, stage_path)


def test_a_field_no_downstream_skill_names_is_reported():
    assert unread_fields({"zzz_invented_field": 1}, "market") == ["zzz_invented_field"]


def test_a_field_a_downstream_skill_names_is_accepted():
    """gtme-write reads the pain map, so `pains` has a consumer."""
    assert unread_fields({"pains": []}, "market") == []


def test_a_reader_must_run_AFTER_the_producer():
    """gtme-company mentions `pain_keywords` and runs two stages before
    gtme-market-pain, which made a dead field look consumed. A check that
    ignores run order launders exactly the drift it exists to catch."""
    assert PIPELINE.index("gtme-company") < PIPELINE.index("gtme-market-pain")
    company_only = {f for f in ["pain_keywords"]
                    if f in (SKILLS / "gtme-company" / "SKILL.md").read_text()}
    assert company_only, "fixture assumes gtme-company still mentions pain_keywords"
    # Named by a LATER skill now, so it passes - but not on the strength of the
    # earlier mention.
    assert PIPELINE.index("gtme-signals") > PIPELINE.index("gtme-market-pain")


def test_the_producer_naming_its_own_field_proves_nothing():
    """Otherwise every field trivially passes."""
    producer = STAGE_SKILL["market"]
    assert producer not in PIPELINE[PIPELINE.index(producer) + 1:]


def test_the_escape_hatch_is_a_reason_on_the_record():
    """A field may legitimately have no downstream reader - gate state, the
    human judgment surface - but the exemption is a line in a diff, not
    silence. Same bar as `UNUSED:` in provenance.md."""
    assert unread_fields({"gate_answers": {}}, "offer") == []
    assert "offer.gate_answers" in UNREAD_OK
    assert UNREAD_OK["offer.gate_answers"].strip(), "an exemption must state why"


def test_every_exemption_states_a_reason():
    for key, reason in UNREAD_OK.items():
        assert "." in key, f"{key} should be <stage>.<field>"
        assert len(reason) > 10, f"{key} exempted without a real reason"


# --- numbers that must agree across files ------------------------------------

def _run(tmp_path, offer=None, icp=None, tam_lines=None):
    if offer is not None:
        (tmp_path / FOLDER["gtme-offer"]).mkdir(exist_ok=True)
        (tmp_path / FOLDER["gtme-offer"] / "offer.json").write_text(__import__("json").dumps(offer))
    if icp is not None:
        (tmp_path / FOLDER["gtme-icp"]).mkdir(exist_ok=True)
        (tmp_path / FOLDER["gtme-icp"] / "icp.json").write_text(__import__("json").dumps(icp))
    if tam_lines is not None:
        (tmp_path / FOLDER["gtme-list"]).mkdir(exist_ok=True)
        (tmp_path / FOLDER["gtme-list"] / "tam.jsonl").write_text("{}\n" * tam_lines)
    return str(tmp_path)


def test_concurrency_and_throughput_are_different_quantities(tmp_path):
    """04-offer/provenance.md [O4] states both: "2 concurrent in-VPC slots,
    ~3/quarter". Collapsed into "2 concurrent slots per quarter" they read as
    one number stated twice, which is how the file appeared to say 2 and 3 for
    the same thing. Stated correctly, both must pass."""
    o = {"scarcity_facts": ["in-VPC audits run 2 concurrent slots, about 3 completed per quarter"],
         "economics": {"vpc_concurrent_slots": 2, "vpc_audit_capacity_per_quarter": 3}}
    assert numbers_agree(_run(tmp_path, offer=o)) == []


def test_prose_contradicting_economics_is_caught(tmp_path):
    o = {"scarcity_facts": ["in-VPC audits run 5 concurrent slots"],
         "economics": {"vpc_concurrent_slots": 2, "vpc_audit_capacity_per_quarter": 3}}
    assert any("concurrent" in x for x in numbers_agree(_run(tmp_path, offer=o)))


def test_a_guard_larger_than_its_own_universe_is_caught(tmp_path):
    """niche_slap_guard blocks ICP edits until a contact bar is cleared. Nothing
    checked the bar was reachable: a threshold larger than the filter's universe
    makes the ICP permanently unfalsifiable, turning a safety catch into a wall."""
    icp = {"niche_slap_guard": {"min_contacts_before_icp_edit": 500, "min_cycles": 2},
           "contacts_per_account": {"default": 2}}
    assert any("guard" in x for x in numbers_agree(_run(tmp_path, icp=icp, tam_lines=100)))


def test_a_reachable_guard_passes(tmp_path):
    icp = {"niche_slap_guard": {"min_contacts_before_icp_edit": 500, "min_cycles": 2},
           "contacts_per_account": {"default": 2}}
    assert numbers_agree(_run(tmp_path, icp=icp, tam_lines=774)) == []


def test_every_real_run_on_this_machine_is_green():
    """The migration signal for the checks themselves.

    The example run proves the check accepts a well-formed artifact; only a real
    one proves a change has not broken work already done. Real runs are
    gitignored, so on a fresh clone there are none and this skips - it is an
    extra signal for whoever has the data, never a gate the suite depends on.
    Discovered by shape rather than named, so no client name is written here.
    """
    runs = live_runs()
    if not runs:
        pytest.skip("no real runs on this machine - the example run covers the rest")
    for run in runs:
        assert numbers_agree(str(run)) == [], f"{run.name} is not green"


# --- folder numbering ---------------------------------------------------------

def test_concurrent_stages_share_a_number():
    """gtme-signals and gtme-enrich both consume the TAM and neither reads the
    other. A letter suffix (08a, 08b) would assert a sequence that does not
    exist; a shared bare number says peers, and lets the filesystem break the
    tie arbitrarily - which is correct, because their order is arbitrary."""
    assert FOLDER["gtme-signals"][:2] == FOLDER["gtme-enrich"][:2]
    assert FOLDER["gtme-signals"] != FOLDER["gtme-enrich"]


def test_pipeline_is_derived_from_waves_not_hand_kept():
    """Two lists of the same order drift, and the drift is what these checks
    exist to catch. The only hand-placed entries are the two cross-cutting
    gates, which bracket the waves instead of sitting in one."""
    assert PIPELINE == ["gtme-why"] + [s for w in WAVES for s in w] + ["gtme-handoff"]


def test_numbers_are_contiguous_and_ordered():
    nums = [int(FOLDER[wave[0]][:2]) for wave in WAVES]
    assert nums == list(range(1, len(WAVES) + 1))


def test_every_stage_has_a_folder_or_a_root_file_but_not_both():
    """gtme-why writes 00-why.md and gtme-handoff writes 99-handoff.md at the run
    root. Giving them wave folders would have invented two stages that produce no
    artifact directory."""
    assert set(FOLDER) | set(ROOT_FILE) == set(PIPELINE)
    assert not (set(FOLDER) & set(ROOT_FILE))
    assert len(set(FOLDER.values())) == len(FOLDER)


def test_the_run_starts_at_01_company():
    """A run begins from a URL at gtme-company. Numbering from a stage that may
    never run left the live run starting at 02 with no 01 anywhere."""
    assert FOLDER["gtme-company"] == "01-company"
    assert [f for f in ROOT_FILE.values() if f.startswith("00")] == ["00-why.md"]


def test_a_parallel_branch_is_numbered_by_its_earliest_start():
    """gtme-publish runs independently from the moment company.json exists and
    reads offer.json opportunistically, so it spans most of the run. Its number
    says when it CAN start, not when it ends."""
    assert FOLDER["gtme-publish"][:2] == FOLDER["gtme-market-pain"][:2] == "02"


def test_research_runs_late_not_early():
    """gtme-research is deep research on tier-1 accounts and barriers on score.
    Reading the name as "background reading" put it second in an earlier draft,
    six waves from the truth."""
    assert PIPELINE.index("gtme-research") > PIPELINE.index("gtme-score")


def test_stage_path_is_never_hand_typed():
    """A hand-written "company/seller-research.json" survived the renumbering
    and made the distillation check silently stop running: a wrong path and an
    absent file are indistinguishable to a silent skip."""
    assert stage_path("gtme-company", "seller-research.json") == "01-company/seller-research.json"
