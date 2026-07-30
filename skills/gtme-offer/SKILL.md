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
- Input: `runs/<slug>/context/context.json` + `icp/icp.json` + `market/market-pain.json` (+ `seller-research.json` evidence). Output: `runs/<slug>/offer/offer.json` (`status: draft` — gate ★2 → `status: confirmed`)
- Re-run when: icp.json is re-confirmed (**an ICP change invalidates the offer** — never keep an offer built on an old ICP), `gtme-measure` returns `offer_verdict: primary_problem`, or **`proof_inventory` gains a named case study/testimonial → mandatory re-tier** (new proof moves the Likelihood lever; an offer still priced at its no-proof tier is under-claiming)

## Construction (research/12 §2 — do all five, keep the record)

1. **Dream outcome** per persona, from `market-pain.json pains[].dream_outcome` (evidence-backed buyer desire, role-keyed) — `icp.json personas[].cares_about` is the fallback only when the pain map lacks the role.
2. **Problem list from the pain map** — start from `market-pain.json pains[]` (each already evidenced and PURE-testable: felt = Recognized, gap_math = Expensive), then extend with anything before/during/after the outcome the map missed; probe each on the four value-equation axes (worth it? faster? easier? believable?). Gate each problem with **PURE**: Painful, Urgent, Recognized, Expensive. Problems failing PURE don't earn offer components. Carry the source `pain_id` on each `problems[]` row — write and measure attribute against it.
3. **One solution per problem** — each must trace to a `context.json` capability or proof point. **Never invent a capability.** No capability → the problem stays unsolved in this offer (say so), or the offer narrows.
4. **Delivery + trim & stack** — pick delivery shapes, score value × cost, cut everything not-high-value, keep a handful of high-cost-high-value. Record the cut list in offer.md prose — the human judges what you discarded, not just what you kept.
5. **Assemble:** core offer (value-equation levers explicit) + guarantee (from the research/12 §3 menu; conditional terms = real activation points) + honest scarcity (only if it maps to a verifiable operational fact — no cap ⇒ no scarcity line) + name (MAGIC — body/asset surfaces only, never email subjects) + **front-end slice**: a **complete solution to a narrow problem whose solving reveals the problem the core offer solves** (the Problem→Solution cycle). Selected by *revelation*, never by cost — a cheap detached component is a discount, not a lead magnet. Quality bar: so good a stranger would feel obligated to pay for it standalone. Shape stays `[Type] deliverable (timeframe)`.

## Validation pass (before the human gate)

**The review question every lens serves — the Hormozi razor: "Is this offer something the target would be STUPID to say no to?"** Not "is it good," not "is it fair" — would a rational buyer in the ICP, seeing this cold, feel that declining costs them more than accepting? Every reviewer answers the razor first, then their lens-specific findings explain why the answer isn't yes: value too low, risk not reversed, effort too high, proof too thin, ask mis-sized. An offer where reviewers answer "reasonable to decline" is not done.

Dispatch **8 review subagents** (pipeline-wide standard — see auto-gtme skill): buyer simulations per segment, grand-slam gate re-audit, operational feasibility, evidence-trace, competitive incomparability, economics, front-end/AI-smell, downstream contract.

**Belief-weak is not coverage-weak (Hormozi doctrine, learned in run 1).** When reviewers answer "reasonable to decline" because proof is thin (anonymized, founder-claimed), re-running problem-solution stacking fixes nothing — the weak term is Likelihood, and its only fix is PROOF: execute `warm_first_plan` to mint a named logo, then the mandatory re-tier fires. Meanwhile apply obstacle-resolution ONE LEVEL DOWN, to the yes-path itself, not the dream outcome: (1) shrink the first yes (a preview so small the proof arrives before belief is required), (2) pre-resolve the data/legal gate (one-page handling term: retention, deletion, no-training; plus a zero-export synthetic-data fallback), (3) make the champion the hero of the findings (named-recipient, recovered-dollars framing — money they discovered, never errors they made). Then SHIP at the honest tier: a good offer into a verified starving crowd beats holding everything for a logo you don't have. Incredible is earned, then the construction catches up.

## The review gate ★2 (non-negotiable — same mechanics as gtme-icp)

1. Generate `offer.json` directly with `status: "draft"`. The prose judgment surface lives INSIDE the JSON: `rationale`, `gate_answers` (all 11), and `cut_list` string fields — no .md companion (design decision: the JSON is the reviewable artifact).
2. **STOP. Tell the user to review against the 11-question gate** (below). The campaign shipping today is not a reason to skip — the gate exists precisely for that pressure.
3. On `confirm`, set `status: "confirmed"` + `confirmed_by`/`confirmed_at`. Never pull a list off an unconfirmed offer.

**The 11-question gate** (research/12 §6 — answer each in offer.md; any NO blocks):
PURE problem · incomparability (can they get a like-for-like quote?) · all four value levers addressed · every named problem has a component · trim check · **guarantee ops can cash** (worst case survivable?) · **scarcity true** · premium price held (bonuses, not discounts) · named + front-end slice cut · honest tier · **standalone price** (what would a stranger pay for the front-end deliverable as delivered? no number ⇒ NO — it's a flyer, not a magnet). Questions on competitors, fulfillment capacity, operational truth, and tier taste are why the gate is human — the agent prepares the judgment surface, it doesn't judge.

## offer.json machine fields (fixed schema — downstream reads these exact keys; shown as yaml for readability)

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
  - {id: p1, pain_id: "pain:unworked_backlog", problem: "warehouse spend scrutiny post-raise", persona: economic_buyer,
     solution: "cost sprint", proof: "38% case study", signals: [funding_raised, x_problem_post]}
front_end_offers:
  - {id: f1, name: "[Teardown] Snowflake cost teardown (48 hrs)", reveals: p1,   # required, never null
     magnet_type: reveal_problem,        # reveal_problem | sample_trial | one_step
     narrow_problem_solved: "which of your warehouse queries burn the spend",
     standalone_price: "$2k as a consulting deliverable",   # gate q11 needs a number; none ⇒ not a magnet
     signals: [funding_raised], direction: acquire, deliverable_exists: true, sampleable: true}
proof_inventory: {case_studies: 1, testimonials: 0}   # counted from context.json, never asserted
warm_first_plan: null    # required (not null) when proof_inventory is all zeros — see Blocked states
engaged_definition: [reply, connect_accept, sample_requested]   # what counts as an ENGAGED lead; gtme-measure grades engaged per 100 contacts, tier math means THIS, not sends
```

| Rule | Why |
|---|---|
| `signals` use taxonomy IDs (gtme-icp vocabulary); `persona` uses the icp role enum | `gtme-write` matches them against `top_signal.type` and prospect role — invented strings fail silently. Unknown ID → refuse to compile |
| `deliverable_exists` false → the row doesn't ship | Integrity guard: no offer without a real deliverable behind it |
| `sampleable` false → permission CTA only | A Loom teardown exists but can't be excerpted in plaintext |
| `direction` on every front-end offer | Expansion prospects never get a cold acquire offer; no expansion row → gtme-write falls back to its rule-6 reframe |
| `worst_case_cost` always filled | The ops-can-cash check needs a number to judge |
| `magnet_type` + `narrow_problem_solved` + non-null `reveals` on every front-end row | A magnet is picked by revelation, not cost; these fields force the selection logic into the artifact |
| `engaged_definition` always present | "Contacts per lead" means engaged leads — people who took an action — or the campaign gets graded on activity, which is how agencies lie to clients |
| `proof_inventory` counted, not asserted | Zeros trigger the warm-first gate; an invented "1" skips the one motion that mints real proof |

## Blocked states

- `context.json` has no capabilities/proof → `offer.status.json` `blocked_thin_context`, name what's missing. Never invent capabilities to proceed.
- **`proof_inventory` all zeros → warm-first gate.** offer.json must carry a `warm_first_plan`: `{count: 3-5, source: context.json warm_universe, term: "named logo + case study + referral on success — in writing", status: proposed|running|done|waived}`. `gtme-list` is blocked for cold tiers until the plan is attempted or the human waives it at ★2 with a logged reason. Rationale: proof-of-work copy treats the symptom; the disease is skipping warm. No volume of cold email fixes a proof problem that 3-5 free warm deliveries solve — the circular dependency (no logos → weak proof → commodity tier → weak cold conversion → no logos) only breaks here.
- No confirmed why → proceed without a goal; `gtme-list` will skip its volume check with a warning (it doesn't block, it doesn't invent).

## Common Mistakes

- Designing the offer and proceeding to gtme-list in the same breath → ★2 is a hard stop, deadline or not.
- Offer lives in prose only → downstream can't read it. The machine fields are the offer; rationale/gate_answers/cut_list ride along inside the same JSON.
- Solution without a capability behind it → check `context.json` first; the check is step 3, not the gate's job.
- Vibes-based volume plan → tier drives contacts-per-lead; the tier is assigned at the gate, not implied.
- Fake scarcity ("spots filling fast") → only `scarcity_facts` entries reach copy.
- Skipping the cut-list → the human can't judge an offer without seeing what was traded away.
- Front-end slice picked because it's cheap → wrong axis. Pick the component whose delivery *reveals* the core-offer problem; then check you'd charge for it standalone (gate q11).
- Zero proof + straight to cold list → the warm-first gate exists precisely here. Free-for-named-logo against `warm_universe` first, or a logged human waiver.

## Next

`gtme-list` reads confirmed `offer.json` (`offer_tier` × goal → volume plan) → builds the TAM. `gtme-write` consumes `problems` + `front_end_offers` as its WHAT layer. `gtme-measure` grades the cycle against `offer_tier` and may return `offer_verdict: primary_problem` → re-open this gate.

**REFERENCE:** `research/12-offer-construction.md` (value equation, trim & stack, guarantee menu, gate rationale) · `research/11-x-primary-sources.md` §3.1 (tiers), §3.7 (front-end starters).
