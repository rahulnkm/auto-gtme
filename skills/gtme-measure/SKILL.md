---
name: gtme-measure
description: Use after an outreach cycle has outcomes (replies, meetings, bounces), when you need to measure what worked and improve targeting for the next cycle. Triggers include "measure the results", "what worked", "tune the targeting", or the learning-loop step of an auto-gtme run.
---

# gtme-measure

## Overview

Close the loop: measure the cycle's outcomes, attribute conversion to signals/segments, and emit a feedback patch that tightens the next cycle's ICP and scoring. This is the "learns every week" engine — the difference between a one-shot blast and a compounding system.

Output: `measure.json` (the machine `icp_patch`) + `measure.md` (the reasoning).

## When to Use

- After a cycle's `gtme-sequence` sends have outcomes. Input: send outcomes (replies, meetings, bounces) + the cycle's `signals.jsonl` / `icp.json`. Output: `runs/<slug>/measure.json` + `measure.md`
- Feeds `gtme-icp` (next confirm) and `gtme-score` (signal priors)

## Pre-register the test

**Decide the success metric and the kill criterion before the sends go out** — one variable per test, explicit kill threshold, always something running (Copeland, Vercel). Post-hoc metric picking turns every cycle into a "win" and the patch into noise.

## Book-rate is the objective (not reply-rate)

**Measure meetings-booked / reached. A reply is curiosity; a booked meeting is the revenue event.** Reply-rate is a diagnostic, never the target.

**Where reply-rate and book-rate disagree, book-rate is the truth.** The classic trap: a signal earns lots of polite replies but few meetings (`funding_raised` — "congrats on the raise" gets a nod and no calendar). Optimizing reply-rate would weight it up; book-rate demotes it correctly.

## Offer-tier baseline

Set the expectation **before** judging the cycle — contacts-per-lead scales with offer quality (coldemailchris): incredible/unique offer ≈ 1 lead per 25–200 contacts; good ≈ 200–500; decent ≈ 500–1,000; weak/commodity category (SEO, cybersecurity, recruiting) ≈ 1,000–10,000. A "bad" cycle judged at tier-1 expectations may be the **offer**, not the copy or the targeting — the offer is the third attribution branch alongside channel and upstream step.

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
 "channel_notes": ["email_cold books 43%/deliverable — promote to co-primary; bounces = enrich miss"],
 "caveats": ["tech_stack_change n=5 — prior is directional, will regress; self-corrects next cycle"],
 "measured_at": "<iso8601>"}
```

- `cycle` — `<run-slug>-c<n>` (e.g. `linear-c1`). Outputs live under `runs/<slug>/`, the same slug as the rest of the run.
- `verdict` per signal is one of: `up` (raise its prior), `down` (lower its prior but keep it in `watch_signals` — a real audience that books poorly), `drop` (remove from `watch_signals` entirely — 0 book on adequate n). Distinct: `down` demotes, `drop` removes.
- `signal_priors` — the sanctioned re-weighting path. A per-signal-type multiplier retuned from **book-rate** each cycle, **kept separate from `gtme-score`'s frozen decay/strength constants** so cross-run scores stay comparable. `gtme-score` reads it as an optional layer (default 1.0). This is how the loop feeds scoring without breaking the fixed formula.
- `watch_signals_add/drop` + `verticals_add` → applied on the next `gtme-icp` confirm. **These arrays may be empty** — a cycle where everything performs adjusts only priors, adds/drops nothing.
- The patch is a **diff to apply on next `gtme-icp` confirm**, not an in-place edit of a live ICP.

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
