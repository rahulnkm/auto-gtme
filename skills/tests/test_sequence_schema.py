"""The sequence contract, and the library it selects from.

The sequence used to run last, after the messages were already drafted. That put
the campaign's shape downstream of its own copy: `gtme-write` knew a touch
*number* and its formatting limits, and nothing told it what touch 2 was FOR. The
arc existed as one prose sentence inside the sending skill.

Splitting it produced three layers, and most of these tests exist to keep them
apart: a template is a reusable shape, `sequence.json` is that shape bound to one
campaign, and `messages.jsonl` is the bound shape filled in per contact.
"""
import json
import re
from pathlib import Path
from jsonschema import Draft202012Validator

SKILLS = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((SKILLS / "gtme-sequence" / "sequence.schema.json").read_text())
V = Draft202012Validator(SCHEMA)
TEMPLATES = sorted((SKILLS / "gtme-sequence" / "templates").glob("*.json"))


def errs(d):
    return [f"{list(e.absolute_path)}: {e.message}" for e in V.iter_errors(d)]


SEQ = {
    "status": "draft",
    "template_id": "email-3touch", "template_version": "1.0.0",
    "selection_rationale": "Email is the only wired channel and the sending domain is mid-warmup.",
    "channels_verified": [{"channel": "email_cold", "wired": True,
                           "evidence": "channel-plan.json sender_identity has a cold address and SPF/DKIM/DMARC",
                           "daily_cap": 30}],
    "touches": [
        {"n": 1, "channel": "email_cold", "day_offset": 0,
         "intent": "Name the problem in the reader's own words and earn one reply.",
         "leans_on": "pain", "ask": "micro_commitment", "word_max": 175,
         "binds": {"pain_id": "pain:unworked_backlog"}},
        {"n": 2, "channel": "email_cold", "day_offset": 3,
         "intent": "Add an angle touch 1 did not use.",
         "leans_on": "new_angle", "ask": "permission_to_send", "word_max": 120},
        {"n": 3, "channel": "email_cold", "day_offset": 10,
         "intent": "Close the loop and make not-replying easy.",
         "leans_on": "breakup", "ask": "explicit_close", "word_max": 75},
    ],
    "send_window": {"rule": "recipient-local business day, 09:00-11:00",
                    "skip": ["saturday", "sunday"]},
    "volume_ceiling": {"touches_per_contact": 3, "binding_channel": "email_cold",
                       "daily_cap": 30, "max_contacts_in_flight": 100,
                       "derivation": "30/day x 10 sequence days / 3 touches per contact"},
    "branches": [{"on": "reply_any", "action": "stop_cold"},
                 {"on": "no_reply", "action": "advance"}],
}


def seq(**over):
    return {**SEQ, **over}


def test_a_complete_sequence_validates():
    assert errs(SEQ) == []


# --- the binding: ids, not prose ---------------------------------------------

def test_a_touch_leaning_on_a_pain_must_name_which_pain():
    """The template says touch 1 opens on pain. Which pain is a campaign
    decision, and leaving it to the writer turns a designed arc back into five
    variations of touch 1."""
    t = [{k: v for k, v in SEQ["touches"][0].items() if k != "binds"}] + SEQ["touches"][1:]
    assert any("binds" in e for e in errs(seq(touches=t)))


def test_a_touch_leaning_on_an_objection_must_name_which_objection():
    t = [{**SEQ["touches"][0], "leans_on": "objection", "binds": None}]
    assert errs(seq(touches=t)) != []


def test_a_binding_is_an_id_never_a_paraphrase():
    """Prose here would be a second copy of the pain map, and the copy drifts."""
    t = [{**SEQ["touches"][0], "binds": {"pain_id": "the unworked backlog"}}]
    assert errs(seq(touches=t)) != []


def test_a_new_angle_touch_needs_no_binding():
    """It exists to NOT reuse what came before, so there is nothing to bind."""
    assert errs(seq(touches=[SEQ["touches"][1]])) == []


# --- what makes the library compound -----------------------------------------

def test_the_template_version_is_pinned():
    """gtme-measure attributes outcomes to template_id + version. Without the
    version an outcome cannot be compared to anything."""
    assert any("template_version" in e for e in
               errs({k: v for k, v in SEQ.items() if k != "template_version"}))
    assert errs(seq(template_version="1.0")) != []


def test_an_adaptation_must_say_why():
    """A silent template edit breaks attribution: the run reports against a
    version whose shape it no longer used."""
    d = seq(adaptations=[{"field": "touches[1].day_offset", "from": 3, "to": 5}])
    assert any("why" in e for e in errs(d))


# --- channels must be real ----------------------------------------------------

def test_every_required_channel_carries_evidence_it_is_wired():
    """A multichannel template selected while LinkedIn is unwired does not make a
    7-touch campaign. It makes a 4-touch campaign with three holes, and nothing
    downstream says so."""
    d = seq(channels_verified=[{"channel": "linkedin_dm", "wired": True}])
    assert any("evidence" in e for e in errs(d))


# --- the ceiling that bounds the list ----------------------------------------

def test_the_volume_ceiling_must_be_derived_not_asserted():
    """It exists to constrain gtme-list, and an underived number constrains
    nothing. Touches x contacts against the daily cap is the real ceiling, and
    list was sizing volume from offer_tier alone."""
    v = {k: x for k, x in SEQ["volume_ceiling"].items() if k != "derivation"}
    assert errs(seq(volume_ceiling=v)) != []


def test_the_ceiling_names_the_channel_that_runs_out_first():
    v = {k: x for k, x in SEQ["volume_ceiling"].items() if k != "binding_channel"}
    assert any("binding_channel" in e for e in errs(seq(volume_ceiling=v)))


def test_a_confirmed_sequence_records_who_confirmed_it():
    assert errs(seq(status="confirmed")) != []


# --- the template library -----------------------------------------------------

def test_templates_exist():
    assert {p.stem for p in TEMPLATES} >= {"email-3touch", "multichannel-7touch",
                                           "nurture-10touch", "signal-triggered"}


def test_every_template_is_seller_agnostic():
    """A template carrying one client's pain ids, prices or product claims is not
    a template. This is the discipline that lets the library be reused, and the
    same rule that keeps campaign data out of a public repo.
    """
    banned = re.compile(r"pain:[a-z_]+|\bf\d+\b|\bobj\d+\b|\$\d|MouseCat|mousecat", re.I)
    for p in TEMPLATES:
        hits = banned.findall(p.read_text())
        assert not hits, f"{p.name} carries campaign-specific content: {hits}"


def test_every_template_cites_where_its_cadence_came_from():
    """These are not invented cadences. An uncited template is someone's
    intuition wearing the word 'proven'."""
    for p in TEMPLATES:
        d = json.loads(p.read_text())
        assert d.get("cites"), f"{p.name} has no cites"
        assert all("research/" in c or "skills/" in c for c in d["cites"]), p.name


def test_every_template_is_versioned_and_says_when_to_use_it():
    for p in TEMPLATES:
        d = json.loads(p.read_text())
        assert re.fullmatch(r"\d+\.\d+\.\d+", d["version"]), p.name
        assert len(d.get("when_to_use", "")) > 40, p.name
        assert d["id"] == p.stem, p.name


def test_every_cold_template_stops_on_any_reply():
    """A scheduled follow-up landing after a human answered is the clearest
    possible tell that nobody is reading."""
    for p in TEMPLATES:
        d = json.loads(p.read_text())
        if d.get("track") == "warm":
            continue
        actions = {b["on"]: b["action"] for b in d["branches"]}
        assert actions.get("reply_any") in ("stop_cold", "stop_all"), p.name
        assert actions.get("reply_negative") == "stop_all", p.name


def test_first_touch_never_asks_for_a_meeting():
    """research/04 §5.3: never ask for a 30-60 minute meeting on first touch. The
    graduated ask is the whole mechanism - an interest question outperforms any
    calendar ask on touch 1."""
    for p in TEMPLATES:
        d = json.loads(p.read_text())
        first = next((t for t in d.get("touches", []) if t["n"] == 1), None)
        if first:
            assert first["ask"] in ("micro_commitment", "connect"), f"{p.name}: {first['ask']}"


def test_no_cold_first_touch_exceeds_the_word_ceiling():
    """research/04 §5.3: never exceed 175 words on a first touch."""
    for p in TEMPLATES:
        d = json.loads(p.read_text())
        first = next((t for t in d.get("touches", []) if t["n"] == 1), None)
        if first:
            assert first["word_max"] <= 175, p.name


def test_touch_numbers_are_contiguous_and_days_never_go_backwards():
    for p in TEMPLATES:
        d = json.loads(p.read_text())
        ts = d.get("touches")
        if not ts:
            continue
        assert [t["n"] for t in ts] == list(range(1, len(ts) + 1)), p.name
        offsets = [t["day_offset"] for t in ts]
        assert offsets == sorted(offsets), p.name


def test_a_route_to_target_names_a_template_that_exists():
    """A dangling route sends an interested reply nowhere."""
    ids = {p.stem for p in TEMPLATES}
    for p in TEMPLATES:
        for b in json.loads(p.read_text())["branches"]:
            if b.get("route_to"):
                assert b["route_to"] in ids, f"{p.name} -> {b['route_to']}"


# --- example data must not name real people ----------------------------------

def test_no_real_person_is_named_in_skill_examples():
    """A schema example showed a real person, by name and by their actual
    LinkedIn slug, depicted in a public repo as an outbound target. Companies in
    examples are public entities and stay; a private individual does not, and the
    example teaches exactly as well with a placeholder.

    The allowlist is the point: a new name in an example has to be added here
    deliberately, which is the same escape-hatch-with-a-reason shape as
    `UNUSED:` in provenance.md and `UNREAD_OK` in validate.py.
    """
    ALLOWED = {"John Smith"}
    ALLOWED_SLUGS = {"john-smith", "clay-hq"}          # clay-hq is a company page
    ALLOWED_EMAIL_LOCALS = {"john.smith", "jane.doe", "x"}
    name_field = re.compile(r'"(?:name|prospect|contact|full_name)":\s*"([^"]+)"')
    slug_field = re.compile(r'"linkedin":\s*"([^"]+)"')
    bad = []
    for p in sorted(SKILLS.glob("gtme-*/SKILL.md")):
        text = p.read_text()
        for n in name_field.findall(text):
            if " " in n and n not in ALLOWED:
                bad.append(f"{p.parent.name}: name {n!r}")
        for s in slug_field.findall(text):
            if s not in ALLOWED_SLUGS:
                bad.append(f"{p.parent.name}: linkedin slug {s!r}")
        # The name and the slug were replaced while the address survived, which
        # is the same partial fix that keeps showing up: change what you looked
        # at, miss the copy one line down.
        for e in re.findall(r'"email":\s*"([^"@]+)@', text):
            if e not in ALLOWED_EMAIL_LOCALS:
                bad.append(f"{p.parent.name}: email local-part {e!r}")
    assert not bad, "real people in public example data: " + "; ".join(bad)
