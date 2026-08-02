---
name: gtme-sequence
description: Use after the offer is confirmed, when the campaign's outbound sequence must be selected and bound before any list is pulled or any message is written. Triggers include "pick the sequence", "design the cadence", "how many touches", or the sequence step of an auto-gtme run.
---

# gtme-sequence

## Overview

Select a sequence template from the library and **bind it to this campaign**: which pain touch 1 opens on, which objection touch 5 answers, which front-end offer is the ask, and how many contacts the daily cap actually allows in flight.

Output: `runs/<slug>/05-sequence/sequence.json` (`status: draft` — gate ★2.5 → `confirmed`).

The one failure this skill exists to prevent: **messages drafted with no idea what each touch is for.** Before this stage existed, `gtme-write` produced one row per (prospect × channel × touch) knowing only the touch *number* and its formatting limits. The arc — what touch 2 does that touch 1 did not — lived as a single prose sentence inside the sending skill, downstream of the writing. A writer cannot hit a beat nobody has told them about.

## Three layers, kept apart

```
templates/*.json     the shape        reusable across clients, versioned in this repo
05-sequence/         the shape        which pain touch 2 leans on, which offer is
  sequence.json      bound to this    the ask, resolved windows, volume ceiling
                     campaign
10-write/            the bound        one row per contact per touch
  messages.jsonl     shape filled
```

Collapsing any two is the failure. A template carrying a client's pain ids stops being reusable. A campaign that edits a template silently stops being measurable, because `gtme-measure` can no longer attribute an outcome to a known shape.

## When to Use

- After `gtme-offer` confirms, **before `gtme-list`**. Input: `04-offer/offer.json` (front-end offers, the ask per touch), `02-market/market-pain.json` (pains, `predicted_objections`, `awareness`), `03-icp/icp.json` (personas, geos), `channel-plan.json` (which channels are wired, daily caps, warmup state), and `templates/`.
- Re-run when the offer is re-confirmed, or when `gtme-measure` returns a sequence verdict.

**Why before the list, not merely before write.** Touches × contacts against the daily cap is the real ceiling on list size, and nothing computed it before — `gtme-list` was sizing volume from `offer_tier` alone. Five touches at 30 sends/day is a very different campaign from two.

## Selecting

`templates/README.md` carries the selection table. The decision is made against what is actually wired, never against what would be nice.

**Verify every required channel first.** `channels_verified[]` records each with evidence. A template requiring LinkedIn, selected while LinkedIn is unwired, does not produce a 7-touch campaign — it produces a 4-touch campaign with three holes in it, and nothing downstream will say so.

**Awareness constrains the opener.** `market-pain.json awareness` decides the register: a `problem_aware` segment needs the problem named on touch 1; a `solution_aware` one is already comparing vendors and will resent being taught. Both cold templates open on pain, but what "pain" means differs, and the binding is where that gets settled.

**Signal density gates `signal-triggered`.** It fires on a dated trigger. Selecting it when most contacts carry none produces a sequence whose first touch waits on an event that never arrives.

## Binding

Every touch the template marks `leans_on: pain` or `leans_on: objection` must name **which one**, by id, in `binds`. Ids, never prose — a paraphrase here is a second copy of the pain map, and the copy drifts.

The binding is where campaign judgment lives. The template says touch 5 answers an objection; you decide it answers `obj2`, because this ICP's technical evaluator raises it and the offer has an element that handles it. **An objection whose `answered_by` is null must never be bound** — `gtme-write` is instructed not to raise it, and binding it here would override that.

## The volume ceiling

Compute it, do not assert it:

```
max_contacts_in_flight = daily_cap(binding_channel) × sequence_days ÷ touches_per_contact
```

The **binding channel** is whichever runs out first. On `multichannel-7touch` that is usually LinkedIn at ≤20 connects/day, not email. Record the derivation; `gtme-list` reads the ceiling and `gtme-send` enforces the caps.

## Adaptations

Deviating from a template is allowed, and must be recorded in `adaptations[]` with a reason. An unrecorded edit is what breaks the library: `gtme-measure` attributes outcomes to `template_id` + `template_version`, so a run that quietly changed touch 4 makes every comparison against that version wrong.

An adaptation that proves out across runs becomes a new template version here — not a habit repeated per campaign.

## The gate ★2.5

1. Generate `sequence.json` with `status: "draft"`.
2. **STOP.** Present: the template chosen and why, the bound touches in order with their intents, the channels verified, the volume ceiling and what it implies for list size, and every adaptation.
3. On confirm, set `status: "confirmed"` + `confirmed_by`/`confirmed_at`.

The human judges two things an agent should not decide alone: whether the cadence suits people who investigate suspicious email for a living, and whether the volume ceiling is one the seller can actually fulfil.

## Common Mistakes

- Selecting a multichannel template because it looks more thorough while a required channel is unwired → the plan gains holes, not touches.
- Binding a pain to every touch → touches 2 and 3 exist to add angles, not restate touch 1 (`research/04` §5.2).
- Editing a template inline instead of recording an adaptation → the library stops compounding.
- Treating the send window as a timestamp → it is a rule; `gtme-send` resolves it per contact against their location.
- Asserting a volume ceiling without deriving it → the number exists to constrain `gtme-list`, and an underived one constrains nothing.

## Next

`gtme-list` reads `volume_ceiling` for its volume plan. `gtme-write` reads `touches[]` — each touch's `intent`, `leans_on`, `ask`, `word_max` and `binds` are the brief for that message. `gtme-send` reads `send_window` and `branches` to materialize the plan.

**REFERENCE:** `templates/README.md` (selection) · `research/01-discipline-and-pipeline.md` (multichannel cadence, LinkedIn limits, signal-triggered pattern) · `research/04-psychology-nepq-persuasion.md` §5.2–5.3 (per-touch asks, follow-up doctrine, the DON'T list)
