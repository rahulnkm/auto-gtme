---
name: gtme-signals
description: Use after a TAM map exists (tam.jsonl), when you need to find which accounts are showing buying intent right now — before scoring or outreach. Triggers include "detect signals", "who's in-market", "check for intent", or the signals step of an auto-gtme run.
---

# gtme-signals

## Overview

Fire buying signals **onto** the TAM map. A signal is noise until it lands on an account you already wanted (doctrine Part 1) — so this runs *over* `tam.jsonl`, never as a free-floating "find intent" search. Output: `signals.jsonl`, one event per detection, which `gtme-score` ranks.

You already detect well. This skill locks the **contract** (event schema), the **gate** (why-you-why-now), the **decay** model, and the **false-positive discipline** — and points to `detectors.md` for the per-signal method for all 30 signals.

## When to Use

- After `gtme-list`, before `gtme-score`. Input: `runs/<slug>/tam.jsonl` + the ICP's `watch_signals`. Output: `runs/<slug>/signals.jsonl`
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

- `signal_type` — exact ID from the 30-signal taxonomy (see `detectors.md`). No invented strings.
- `strength` — `strong | medium | weak | counter | unknown`. This is the **raw** strength at `event_date` — do NOT pre-decay it (see Decay below). `counter` = evidence *against* reaching (e.g. they already use the seller's product); emit it, `gtme-score` subtracts. `unknown` = you checked a source and genuinely can't tell. If you did **not** detect a signal at all, **omit the event entirely** — never emit a fabricated `none`.
- `direction` — `acquire` (new logo) vs `expansion` (already a customer, sell more). Changes the message entirely.
- `event_date` vs `detected_at` — the decay inputs (below). Always both.
- `detection` — source + method + query so the detection is **reproducible and auditable**. Never emit a signal you can't cite.

## Decay — recency is part of the signal

**Decay ownership is one-sided: you emit raw strength + honest `event_date`; `gtme-score` owns the decay math.** Do not pre-decay — a funding round from last week and one from last year both emit at their raw strength with their true date, and `gtme-score` applies the curve (roughly: `strong` <30d, `medium` ~6mo, `weak` past 12mo). If both this skill and score decayed, the signal would be double-penalized. Your one job here: date every event by `event_date` (when it happened), not `detected_at`.

## False-positive discipline (traps that fabricate intent)

| Trap | Rule |
|---|---|
| Vendor marketing read as `li_problem_post` | A problem-post counts only if the author **works at a TAM account**. Competitors' Jira-complaint ads are not intent. |
| LinkedIn `search_jobs` keyword counts | Junk (returns unrelated roles). Use the company's ATS board (Ashby/Greenhouse API) or Jobs tab for company-scoped counts. |
| Detection gap read as absence | If you couldn't detect a signal, mark it **unknown/omit** — never emit `strength: none` as if confirmed-clear. A gap is not a fact. |
| Unverified `incumbent_tech` used as `tech_stack_change` | The TAM's incumbent field may be seeded; confirm live before firing a stack-switch signal. |

## Detection methods

**REQUIRED REFERENCE:** `detectors.md` — the per-signal method for all 30 signals (source, tool, exact query, false-positive trap). Detect only the ICP's `watch_signals` subset per run; the full 30 are there for coverage.

## Common Mistakes

- Free-floating intent search not bound to `tam.jsonl` → route signals onto known accounts only.
- Advancing no-signal accounts → the gate is hard: no qualifying signal, hold.
- Omitting counter-signals → `gtme-score` mis-ranks. Emit them.
- Undated events → decay can't run. `event_date` always.
- Uncitable signal → not a signal. `detection` block mandatory.

## Next

`gtme-score` reads `signals.jsonl` + `tam.jsonl` → fit × signal × recency → tier 1/2/3 routing.
