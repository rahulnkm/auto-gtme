---
name: gtme-measure
description: Use after an outreach cycle has outcomes (replies, meetings, bounces), when you need to measure what worked and improve targeting for the next cycle. Triggers include "measure the results", "what worked", "tune the targeting", or the learning-loop step of an auto-gtme run.
---

# gtme-measure

**The ICP is not editable on a hunch.** `icp.json niche_slap_guard` sets the volume bar (`min_contacts_before_icp_edit` x `min_cycles`) below which zero replies is the expected output of a WORKING filter, not evidence against it. Under the bar, only `edits_allowed_below_bar` may be proposed. Over it, WHO changes may be proposed and still need a human gate. `hard_falsifiers_bypass_bar` are facts about the filter rather than noise about the response rate, and they act immediately. Before trusting the bar, confirm it is reachable: compare it against `list/tam.jsonl` — a threshold larger than the filter's own universe can never be cleared, which would make the ICP permanently unfalsifiable.

## Overview

Close the loop: measure the cycle's outcomes, attribute conversion to signals/segments, and emit a feedback patch that tightens the next cycle's ICP and scoring. This is the "learns every week" engine — the difference between a one-shot blast and a compounding system.

Output: `measure.json` (the machine `icp_patch`) + `measure.md` (the reasoning).

## When to Use

- After a cycle's `gtme-sequence` sends have outcomes. Input: send outcomes (replies, meetings, bounces) + the cycle's `signals/signals.jsonl` / `icp/icp.json` / `write/messages.jsonl` (`pain_id` tags) / `market/market-pain.json`. Output: `runs/<slug>/measure/measure.json` + `measure/measure.md`
- Feeds `gtme-icp` (next confirm), `gtme-score` (signal priors), and `gtme-market-pain` (pain verdicts)

## Pre-register the test

**Decide the success metric and the kill criterion before the sends go out** — one variable per test, explicit kill threshold, always something running (Copeland, Vercel). Post-hoc metric picking turns every cycle into a "win" and the patch into noise.

## Book-rate is the objective (not reply-rate)

**Measure meetings-booked / reached. A reply is curiosity; a booked meeting is the revenue event.** Reply-rate is a diagnostic, never the target.

**Where reply-rate and book-rate disagree, book-rate is the truth.** The classic trap: a signal earns lots of polite replies but few meetings (`funding_raised` — "congrats on the raise" gets a nod and no calendar). Optimizing reply-rate would weight it up; book-rate demotes it correctly.

## The metric ladder (research/15)

Reply → book → close → **retain** is a ladder; each rung is the objective only until the next rung has data. Book-rate is the terminal metric *only while the seller has zero customers*. Once any customer exists, also grade cohorts against the LIR in `icp.json success_criteria` (emit `retention_performance[]`). **An account that matched the filter but missed the LIR is evidence against the filter — same weight as a hard falsifier**, because "who bought" inherits the survivorship bias of your own outreach; "who succeeded" is the only unbiased grade of the ICP (Roberge: retention issues originate in who marketing targeted). A loop graded on engagement alone optimizes toward who replies, forever.

## Offer-tier baseline

Set the expectation **before** judging the cycle — read `offer_tier` from confirmed `offer.json` (assigned by the human at gate ★2; never guess it here). Contacts-per-lead scales with offer quality (coldemailchris): incredible/unique offer ≈ 1 lead per 25–200 contacts; good ≈ 200–500; decent ≈ 500–1,000; weak/commodity category (SEO, cybersecurity, recruiting) ≈ 1,000–10,000. Treat the bands as single-source priors to recalibrate from own campaign data — no independent benchmark measures the offer axis (research/12 §5). A "bad" cycle judged at tier-1 expectations may be the **offer**, not the copy or the targeting — the offer is the third attribution branch alongside channel and upstream step. Emit `offer_verdict: sound | suspect | primary_problem` in measure.json; `primary_problem` recommends re-opening gate ★2 (gtme-offer) on the next cycle.

## The clock lens

Signals that convert carry a **decision window** — a new hire onboarding, a stack mid-migration, a contract renewal. Signals without a clock (a funding round is lagging + crowded; a vent-post has no budget cycle) reply but don't book. When a signal over-performs on book-rate, check whether it carries a clock; that's usually why.

## Attribution discipline

Don't blame a channel for an upstream miss:
- **Bounces → a `gtme-enrich` validation miss**, not an email-channel weakness. (3/10 bounced = enrich let unvalidated addresses through.)
- **Low LinkedIn accept-rate → a targeting/message leak**, not "LinkedIn doesn't work."
- **Deliverability vs copy split** (the weekly check, @dimitarangg): bounces + spam placement + open-rate collapse = infrastructure problem; healthy opens with no replies = copy/offer problem.
- Attribute each outcome to the step that owns it, or the patch fixes the wrong thing.

## icp_patch schema (measure.json — gtme-icp + gtme-score consume it)

```json
{"cycle": "<id>", "objective": "book_rate",
 "signal_performance": [
   {"signal": "job_posting_intent", "reached": 15, "replied": 6, "booked": 4, "book_rate": 0.27, "verdict": "up", "low_n": false},
   {"signal": "li_problem_post", "reached": 8, "replied": 1, "booked": 0, "book_rate": 0.0, "verdict": "drop", "low_n": false}
 ],
 "icp_patch": {
   "watch_signals_add": ["li_hiring_spike"],
   "watch_signals_drop": ["li_problem_post"],
   "verticals_add": ["fintech"],
   "tier_multiplier": {"1": 1.3, "2": 1.0, "3": 0.9},
   "signal_priors": {"job_posting_intent": 1.3, "tech_stack_change": 1.4, "funding_raised": 0.8, "li_problem_post": 0.0}
 },
 "pain_performance": [
   {"pain_id": "pain:unworked_backlog", "reached": 12, "replied": 5, "booked": 3, "verdict": "confirmed", "low_n": false},
   {"pain_id": "pain:rules_lag", "reached": 9, "replied": 0, "booked": 0, "verdict": "suspect", "low_n": true}
 ],
 "channel_notes": ["email_cold books 43%/deliverable — promote to co-primary; bounces = enrich miss"],
 "segment_economics": [
   {"segment": "tier1-crypto", "avg_days_to_close": null, "discount_pressure": "none|asked|required", "n": 0}
 ],
 "retention_performance": [
   {"account_id": "domain:example.com", "matched_tier": 1, "lir_hit": true, "days_to_value": 41}
 ],
 "caveats": ["tech_stack_change n=5 — prior is directional, will regress; self-corrects next cycle"],
 "measured_at": "<iso8601>"}
```

- `segment_economics` — Murphy's Acquisition Efficiency / Dunford's "buy quickly, rarely discount" made measurable: per-segment close speed + discount pressure replace static guesses (`heavy_procurement`). Emit from first closed deal onward; null until then.
- `retention_performance` — one row per customer per cycle, graded against `icp.json success_criteria.lir`. Omit the block entirely while customers = 0. An ICP-matched account with `lir_hit: false` feeds the next ★1 gate as filter-evidence, not as churn ops.

- `cycle` — `<run-slug>-c<n>` (e.g. `linear-c1`). Outputs live under `runs/<slug>/`, the same slug as the rest of the run.
- `verdict` per signal is one of: `up` (raise its prior), `down` (lower its prior but keep it in `watch_signals` — a real audience that books poorly), `drop` (remove from `watch_signals` entirely — 0 book on adequate n). Distinct: `down` demotes, `drop` removes.
- `signal_priors` — the sanctioned re-weighting path. A per-signal-type multiplier retuned from **book-rate** each cycle, **kept separate from `gtme-score`'s frozen decay/strength constants** so cross-run scores stay comparable. `gtme-score` reads it as an optional layer (default 1.0). This is how the loop feeds scoring without breaking the fixed formula.
- `watch_signals_add/drop` + `verticals_add` → applied on the next `gtme-icp` confirm. **These arrays may be empty** — a cycle where everything performs adjusts only priors, adds/drops nothing.
- The patch is a **diff to apply on next `gtme-icp` confirm**, not an in-place edit of a live ICP.
- `pain_performance` — every message carries a `pain_id` hypothesis tag; group outcomes by it. Verdicts: `confirmed` (books — the evidenced pain converts), `suspect` (reached but silent on adequate n — the pain may be real but unfelt by this segment, or mis-worded), `killed` (0 across cycles at adequate n → demote the row in market-pain.json or re-evidence it). Objections quoted in replies attach to their pain row as *new VoC* — a reply is the highest-grade evidence the map will ever get. This is what makes reply data interpretable: without the tag, a cycle teaches you a rate; with it, a cycle edits a specific evidenced claim.

## Small-sample humility

Flag any signal with `reached < 10` as `low_n: true`. A `0` book-rate on n=8 is a safe kill; an exact prior (1.4) on n=5 is directional and will regress — say so in `caveats`. The design self-corrects because priors are retuned from fresh book-rate every cycle.

**Volume math:** P(≥1 booking) = 1 − (1−p)^N. From the measured book-rate `p`, compute the minimum N the next cycle needs — this turns the `icp_patch` into a concrete volume plan, and shows when a 0-book cycle was simply under-powered rather than mis-targeted.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Optimizing reply-rate / open-rate | Book-rate is the objective; replies are a diagnostic. |
| Weighting up a high-reply low-book signal | Where they disagree, book wins. |
| Blaming the channel for bounces | Bounce = enrich miss; attribute to the owning step. |
| Blaming copy for a weak offer | Set the offer-tier baseline first; offer is the third attribution branch. |
| Picking the metric after the sends | Pre-register metric + kill criterion before launch. |
| Baking priors into frozen constants | `signal_priors` is a separate optional layer; constants stay fixed. |
| Killing a signal on n=3 | Flag `low_n`; kill on 0-book, keep directional priors humble. |
| Editing the live ICP in place | Emit a patch; apply on next confirm. |

## Next

The loop restarts: `gtme-icp` applies the patch on next confirm → `gtme-score` reads `signal_priors` → the next cycle targets sharper.
