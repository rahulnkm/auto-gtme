---
name: gtme-score
description: Use after signals are detected, when you need to rank and route accounts for outreach — decide who to reach first and how. Triggers include "score the accounts", "rank the prospects", "prioritize", or the scoring step of an auto-gtme run.
---

# gtme-score

## Overview

Rank accounts by **fit × decayed-signal**, then route them. This is the single owner of the decay math (`gtme-signals` emits raw strength + dates; you apply the curve — do not expect it pre-decayed). Output: `scored.jsonl`, ranked, with a routing decision per account.

The formula is **fixed** — scores must be comparable across runs and re-runs, so don't reinvent constants each time.

## When to Use

- After `gtme-signals` (+ `gtme-enrich` for contacts), before `gtme-write`/`gtme-sequence`
- Input: `tam.jsonl` (fit_tier) + `signals.jsonl` (raw signals) + ICP `score_hint`. Output: `runs/<slug>/scored.jsonl`

## The formula (fixed constants)

```
raw points:      strong=10  medium=5  weak=2  counter=-8   unknown=0
signal prior:    prior[type]  — from measure.json signal_priors; DEFAULT 1.0 if absent
decay:           decayed = raw × prior[type] × 0.5^(age_days / 90)   # 90-day half-life, age from event_date
signal_score:    Σ decayed  (across an account's events)
tier multiplier: score_hint.weight_signals_over_firmographics == true → {1:1.15, 2:1.0, 3:0.9}
                 else (firmographics matter more)            → {1:1.5, 2:1.0, 3:0.6}
final_score:     signal_score × tier_multiplier
```

`prior[type]` is the only tunable that changes between cycles — `gtme-measure` retunes it from book-rate. The raw points, half-life, and tier multipliers are **frozen** so scores stay comparable across runs; all cross-cycle learning flows through `signal_priors` (and the ICP's `watch_signals` membership). First cycle / no measurement → every prior is 1.0, so this reduces to the base formula.

- Trust the signal's emitted `strength` and `counter` label — **do not re-interpret what a signal means.** If `tech_stack_change` fired as `counter`, score it negative; its sign was decided at detection. (A "ripped out the incumbent" event should have been emitted `strong/acquire`, a "adopted a competitor" event `counter` — that call belongs to `gtme-signals`.)
- Counter-signals are **negative, not zero.** Zero lets a stale positive drag a bad-timing account back into the queue — the classic mis-fire.

## Routing — three independent axes

Don't collapse these into one label. Each account gets all three:

| Axis | Set by | Values |
|---|---|---|
| `effort_mode` | **fit_tier** | tier 1 → `human_assisted` (bespoke, human approves send) · tier 2 → `semi_auto` · tier 3 → `fully_auto` |
| `priority` | **final_score** | `high` ≥12 · `medium` 5 ≤ x < 12 · `low` 0 ≤ x < 5 · suppressed accounts → `n/a` |
| `route` | **suppress gate** | `signal_score < 0` (net counter) → `hold_human_review`; else `send` |

- `has_active_counter` — `true` when the account has any `counter` event whose decayed value still contributes materially negative (i.e. it's pulling `signal_score` down). This is what trips the suppress gate.
- `top_signal` — the **highest positive `acquire`** decayed signal; this is the hook `gtme-write` opens with. Never a `counter` (a counter is a reason to hold, not a hook). If an account has no positive signal, `top_signal` is `null` — and it's suppressed anyway, so `gtme-write` won't run on it.

Why separate: a high-fit tier-1 account still deserves a *human-assisted* touch (codyschneider: spend human effort where fit is best), but an active counter-signal must be able to **suppress it regardless of tier** — the trap a firmographics-led model falls into (blasting a tier-1 that just tooled up). `effort_mode` says *how much craft*, `route` says *whether to send at all*.

## scored.jsonl schema (fixed)

```json
{"account_id": "domain:mercury.com", "company": "Mercury", "fit_tier": 1,
 "signal_score": 16.37, "final_score": 18.83, "has_active_counter": false,
 "effort_mode": "human_assisted", "priority": "high", "route": "send",
 "top_signal": {"type": "job_posting_intent", "decayed": 9.40, "direction": "acquire"},
 "message_angle": "fresh hiring intent on top of a recent raise — team scaling, CRM pain imminent",
 "scored_at": "<iso8601>"}
```

`top_signal` (+ its `direction`) is what `gtme-write` leads the message with. `message_angle` is a one-line hook, not the message.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Re-inventing decay/points per run | Constants are fixed; scores must compare across runs. |
| Expecting pre-decayed signals | You own decay; signals arrive raw + dated. |
| Counter-signal scored as 0 | Negative (−8). Zero re-admits bad-timing accounts. |
| Re-interpreting a signal's meaning | Trust emitted `strength`/`counter`; the sign was set at detection. |
| Collapsing routing to one flag | Three axes: `effort_mode` (tier), `priority` (score), `route` (counter gate). |
| Auto-sending a tier-1 with a live counter | Suppress gate fires regardless of tier → `hold_human_review`. |

## Next

`gtme-write` reads `scored.jsonl` (order + `top_signal` + `effort_mode`) → drafts the message; tier-1 `human_assisted` accounts get a bespoke draft for approval, tier-3 `fully_auto` flow straight to `gtme-sequence`.
