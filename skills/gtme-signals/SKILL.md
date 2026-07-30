---
name: gtme-signals
description: Use after a TAM map exists (tam.jsonl), when you need to find which accounts are showing buying intent right now — before scoring or outreach. Triggers include "detect signals", "who's in-market", "check for intent", or the signals step of an auto-gtme run.
---

# gtme-signals

## Overview

Fire buying signals **onto** the TAM map. A signal is noise until it lands on an account you already wanted (doctrine Part 1) — so this runs *over* `tam.jsonl`, never as a free-floating "find intent" search. Practitioners state the same doctrine independently: intent signals are noise without a base map — the map turns "someone got funded" into "tier-1 account got funded, route it now" (codyschneider). Output: `signals.jsonl`, one event per detection, which `gtme-score` ranks.

**Signals multiply effort on the map — they never filter it** (Copeland, Vercel). A no-signal account is *held this cycle*, not deleted; it stays on the TAM for the next pass. Signals decide where effort concentrates, the ICP decides who's on the map.

You already detect well. This skill locks the **contract** (event schema), the **gate** (why-you-why-now), the **decay** model, and the **false-positive discipline** — and points to `detectors.md` for the per-signal method for all 34 signals.

## When to Use

- After `gtme-list`, before `gtme-score`. Input: `runs/<slug>/list/tam.jsonl` + the ICP's `icp.scoring.boosts[].signal` (formerly watch_signals). Output: `runs/<slug>/signals/signals.jsonl` (+ the standard folder companions `provenance.md` and `decisions.md`)
- Re-run on a cadence (daily/weekly) — signals are time-sensitive; the map is durable

## The why-you-why-now gate (Jordan Crawford)

**An account with zero qualifying signals is NOT advanced to outreach this cycle.** Before any account is reached, there must be a *current public signal* that it has the problem today. No signal → hold, don't reach. Emit weak and counter events too (so `gtme-score` can decide and de-rank), but the gate is hard: qualifying signal or hold.

## signal_event schema (fixed — gtme-score reads these keys)

```json
{"account_id": "domain:baseten.co", "signal_type": "funding_raised",
 "event_date": "2026-06-22", "detected_at": "<iso8601>",
 "strength": "strong", "direction": "acquire", "confidence": 0.95,
 "detection": {"source": "company blog + LinkedIn post", "method": "WebSearch cross-confirm", "query": "Baseten Series F 2026"},
 "evidence": {"summary": "$1.5B Series F, names eng headcount as use of funds", "quote": "increase headcount in engineering teams"},
 "sources": ["https://..."]}
```

- `signal_type` — exact ID from the 34-signal taxonomy (see `detectors.md`). No invented strings.
- `strength` — `strong | medium | weak | counter | unknown`. This is the **raw** strength at `event_date` — do NOT pre-decay it (see Decay below). `counter` = evidence *against* reaching (e.g. they already use the seller's product); emit it, `gtme-score` subtracts. `unknown` = you checked a source and genuinely can't tell. If you did **not** detect a signal at all, **omit the event entirely** — never emit a fabricated `none`.
- `direction` — `acquire` (new logo) vs `expansion` (already a customer, sell more). Changes the message entirely.
- `event_date` vs `detected_at` — the decay inputs (below). Always both.
- `detection` — source + method + query so the detection is **reproducible and auditable**. Never emit a signal you can't cite.

## Freshness windows — harvest inside the window, not "recently"

*(Sourcing: `research/14-practitioner-signals-enrichment.md`.)*

Two signals carry **hard harvest windows**; outside them the event is history, not intent. Cody Schneider's build pulls *"job changes last 30 days, new postings last 14 days"* ([x.com/codyschneider/status/2028606359617388794](https://x.com/codyschneider/status/2028606359617388794)), and his reasoning is the mechanism, not the number: *"someone just started as vp of marketing 2 weeks ago? they're evaluating every tool in their stack. company just posted 'revenue operations analyst'? they have a problem they need solved before that person even starts."*

| Signal | Harvest window | Why the window, not just decay |
|---|---|---|
| `li_job_change` / `new_exec_hire` | **30 days** | The stack-evaluation window closes once they've chosen. Past ~90d they own the decisions they inherited. |
| `job_posting_intent` | **14 days** | The pain is live *before* the hire lands. Once filled, the buying reason is staffed, not automated. |

Beyond the window the event still emits (it's true, and `gtme-score` decays it), but it may **not** be the `top_signal` driving a why-now claim in copy — a message whose entire hook is a five-month-old job posting is a message that got the timing wrong.

**Verify at the source, not at an aggregator.** Postings must be confirmed live at the ATS (Greenhouse/Lever/Ashby JSON endpoints), never on builtin/Indeed/startup.jobs mirrors — mirrors stay up for months after a req closes. Store the machine-checkable id (`greenhouse:goatgroup:4701901005`) so re-verification is a scripted diff. Re-verify within **48h of any send** that references a posting. This is not theoretical: the 2026-07-21 run "verified" two postings that had been dead since February and April because the checks read mirrors — assume **only ~1 in 3 hiring signals is still live** by the time outreach fires.

**A closed req is a downgrade, not a zero.** `live` (confirmed at ATS ≤48h) → full weight, posting may be cited. `recently_closed` (was live within ~60d, now gone) → one notch down, reframe to "you just staffed up fraud ops," never cite the posting. `unverifiable` (aggregator-only) → treat as no hiring signal at all.

## Decay — recency is part of the signal

**Decay ownership is one-sided: you emit raw strength + honest `event_date`; `gtme-score` owns the decay math.** Do not pre-decay — a funding round from last week and one from last year both emit at their raw strength with their true date, and `gtme-score` applies the curve (roughly: `strong` <30d, `medium` ~6mo, `weak` past 12mo). If both this skill and score decayed, the signal would be double-penalized. Your one job here: date every event by `event_date` (when it happened), not `detected_at`.

## Calibration anchors (Voje)

- Conversion-indicative vs noise: pricing page visited 5× in 4 days = signal; an exec liking LinkedIn posts = not. Behavior must indicate a buying decision, not attention.
- Timing: a $2–5M round converts best ~3 months post-close — emit `funding_raised` at raw strength with its true `event_date`; `gtme-score`'s decay finds the window.

## False-positive discipline (traps that fabricate intent)

| Trap | Rule |
|---|---|
| Vendor marketing read as `li_problem_post` | A problem-post counts only if the author **works at a TAM account**. Competitors' Jira-complaint ads are not intent. |
| LinkedIn `search_jobs` keyword counts | Junk (returns unrelated roles). Use the company's ATS board (Ashby/Greenhouse API) or Jobs tab for company-scoped counts. |
| Detection gap read as absence | If you couldn't detect a signal, mark it **unknown/omit** — never emit `strength: none` as if confirmed-clear. A gap is not a fact. |
| Unverified `incumbent_tech` used as `tech_stack_change` | The TAM's incumbent field may be seeded; confirm live before firing a stack-switch signal. |

## Detection methods

**REQUIRED REFERENCE:** `detectors.md` — the per-signal method for all 34 signals (source, tool, exact query, false-positive trap). Detect only the ICP's `icp.scoring.boosts[].signal` (formerly watch_signals) subset per run; the full 34 are there for coverage.

## Common Mistakes

- Free-floating intent search not bound to `tam.jsonl` → route signals onto known accounts only.
- Advancing no-signal accounts → the gate is hard: no qualifying signal, hold.
- Omitting counter-signals → `gtme-score` mis-ranks. Emit them.
- Undated events → decay can't run. `event_date` always.
- Uncitable signal → not a signal. `detection` block mandatory.

## Next

`gtme-score` reads `signals/signals.jsonl` + `list/tam.jsonl` → fit × signal × recency → tier 1/2/3 routing.
