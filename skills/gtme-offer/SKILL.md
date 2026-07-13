---
name: gtme-offer
description: Use after gtme-icp confirms, when the campaign's offer must be constructed and human-approved before any list is pulled — the WHAT the whole run pitches. Triggers include "design the offer", "what are we offering", or the third step of an auto-gtme run.
---

# gtme-offer

## Overview

Turn `context.json` + confirmed `icp.json` into a **human-gated grand-slam offer**: the full offer stack (for the close) plus the front-end slice (for touch-1 copy), as machine-readable data downstream skills consume. Expected conversion is conditioned on offer quality before any copy is written — a commodity offer needs 1,000–10,000 contacts per lead; an incredible one needs 25–200 — so a wrong offer wastes every downstream row exactly like a wrong ICP.

The one failure this skill exists to prevent: **designing a plausible offer in prose and rolling straight into list building** — no gate, no artifact, no tier, no record of what was considered and cut. A good offer that only you reviewed is an unreviewed offer.

## When to Use

- After `gtme-icp` confirms (and after `gtme-why` if a why exists — read its `goal`), before `gtme-list`
- Input: `runs/<slug>/context.json` + `icp.json`. Output: `runs/<slug>/offer.md` (editable — gate ★2) → `offer.json` (machine)
- Re-run when: icp.json is re-confirmed (**an ICP change invalidates the offer** — never keep an offer built on an old ICP), or `gtme-measure` returns `offer_verdict: primary_problem`

## Construction (research/12 §2 — do all five, keep the record)

1. **Dream outcome** per persona, from `icp.json personas[].cares_about`.
2. **Exhaustive problem list** — everything before/during/after the outcome; probe each on the four value-equation axes (worth it? faster? easier? believable?). Gate each problem with **PURE**: Painful, Urgent, Recognized, Expensive. Problems failing PURE don't earn offer components.
3. **One solution per problem** — each must trace to a `context.json` capability or proof point. **Never invent a capability.** No capability → the problem stays unsolved in this offer (say so), or the offer narrows.
4. **Delivery + trim & stack** — pick delivery shapes, score value × cost, cut everything not-high-value, keep a handful of high-cost-high-value. Record the cut list in offer.md prose — the human judges what you discarded, not just what you kept.
5. **Assemble:** core offer (value-equation levers explicit) + guarantee (from the research/12 §3 menu; conditional terms = real activation points) + honest scarcity (only if it maps to a verifiable operational fact — no cap ⇒ no scarcity line) + name (MAGIC — body/asset surfaces only, never email subjects) + **front-end slice**: the stack's cheapest high-value-low-cost component detached as a touch-1 deliverable (`[Type] deliverable (timeframe)` shape).

## The review gate ★2 (non-negotiable — same mechanics as gtme-icp)

1. Generate `offer.md` — prose rationale (including the §6 gate answers and the trim cut-list) + a single fenced ```yaml block holding all machine fields.
2. **STOP. Tell the user to review against the 10-question gate** (below). The campaign shipping today is not a reason to skip — the gate exists precisely for that pressure.
3. On `confirm`, parse the yaml → `offer.json`, set `status: confirmed`. Never pull a list off an unconfirmed offer.

**The 10-question gate** (research/12 §6 — answer each in offer.md; any NO blocks):
PURE problem · incomparability (can they get a like-for-like quote?) · all four value levers addressed · every named problem has a component · trim check · **guarantee ops can cash** (worst case survivable?) · **scarcity true** · premium price held (bonuses, not discounts) · named + front-end slice cut · honest tier. Questions on competitors, fulfillment capacity, operational truth, and tier taste are why the gate is human — the agent prepares the judgment surface, it doesn't judge.

## offer.md yaml block (fixed schema — downstream reads these exact keys)

```yaml
name: "The Snowflake Cost Sprint"        # MAGIC-named; never used as an email subject
status: draft                            # compile sets: confirmed
offer_tier: 2          # 1 incredible / 2 good / 3 decent / 4 commodity (research/11 §3.1)
                       # contacts-per-lead is DERIVED from tier, not stored. tier 4 → fix the offer, don't scale volume
core_offer:
  dream_outcome: "..."
  likelihood_levers: ["case study: 38% in 6 wks", "conditional guarantee"]
  time_to_value: "first findings in 48h"
  effort_asked: "read-only role grant, 10 min"
  guarantee: {type: conditional, terms: "no 15% found -> keep the report, no sprint pitch",
              activation_points: ["access granted wk 1"], worst_case_cost: "8h founder time"}
scarcity_facts: ["2 concurrent client slots (founder-fulfilled)"]   # empty list ⇒ no scarcity in copy
problems:
  - {id: p1, problem: "warehouse spend scrutiny post-raise", persona: economic_buyer,
     solution: "cost sprint", proof: "38% case study", signals: [funding_raised, x_problem_post]}
front_end_offers:
  - {id: f1, name: "[Teardown] Snowflake cost teardown (48 hrs)", reveals: p1,
     signals: [funding_raised], direction: acquire, deliverable_exists: true, sampleable: true}
```

| Rule | Why |
|---|---|
| `signals` use taxonomy IDs (gtme-icp vocabulary); `persona` uses the icp role enum | `gtme-write` matches them against `top_signal.type` and prospect role — invented strings fail silently. Unknown ID → refuse to compile |
| `deliverable_exists` false → the row doesn't ship | Integrity guard: no offer without a real deliverable behind it |
| `sampleable` false → permission CTA only | A Loom teardown exists but can't be excerpted in plaintext |
| `direction` on every front-end offer | Expansion prospects never get a cold acquire offer; no expansion row → gtme-write falls back to its rule-6 reframe |
| `worst_case_cost` always filled | The ops-can-cash check needs a number to judge |

## Blocked states

- `context.json` has no capabilities/proof → `offer.status.json` `blocked_thin_context`, name what's missing. Never invent capabilities to proceed.
- No confirmed why → proceed without a goal; `gtme-list` will skip its volume check with a warning (it doesn't block, it doesn't invent).

## Common Mistakes

- Designing the offer and proceeding to gtme-list in the same breath → ★2 is a hard stop, deadline or not.
- Offer lives in prose only → downstream can't read it. The yaml block is the offer.
- Solution without a capability behind it → check `context.json` first; the check is step 3, not the gate's job.
- Vibes-based volume plan → tier drives contacts-per-lead; the tier is assigned at the gate, not implied.
- Fake scarcity ("spots filling fast") → only `scarcity_facts` entries reach copy.
- Skipping the cut-list → the human can't judge an offer without seeing what was traded away.

## Next

`gtme-list` reads confirmed `offer.json` (`offer_tier` × goal → volume plan) → builds the TAM. `gtme-write` consumes `problems` + `front_end_offers` as its WHAT layer. `gtme-measure` grades the cycle against `offer_tier` and may return `offer_verdict: primary_problem` → re-open this gate.

**REFERENCE:** `research/12-offer-construction.md` (value equation, trim & stack, guarantee menu, gate rationale) · `research/11-x-primary-sources.md` §3.1 (tiers), §3.7 (front-end starters).
