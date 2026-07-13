---
name: auto-gtme
description: Use to start or run the full GTM pipeline from a company website — the orchestrator entry point. Triggers include "get me started", "here's my site", "run auto-gtme", "run the whole pipeline", or `auto-gtme init --website`.
---

# auto-gtme

## Overview

The orchestrator. From one website URL, chain the 14 `gtme-*` skills into a full inbound + outbound GTM pipeline — an open-source, agent-native, self-hosted Gojiberry. Each skill reads the prior artifact and writes the next; the run directory *is* the state. Four human gates, dry-run-safe sends.

## Entry — from just a website

```
auto-gtme init --website https://linear.app
```
Derive the run slug from the domain (`linear.app` → `linear`). All artifacts live under `runs/<slug>/`. Then run `gtme-context` on the URL and proceed down the DAG.

## Run-state model

- **`runs/<slug>/` is the state.** Each stage's output artifact is its completion marker.
- **Skip-if-exists:** a stage whose output already exists is skipped unless the user asks to refresh.
- **Resumable:** stop and restart anytime; the directory says what's done.
- `run.log` records what ran when.

## The DAG (order + parallelism)

```
URL
 └ gtme-context → context.json
    └ gtme-icp → icp.md ★1 → icp.json
       └ gtme-offer → offer.md ★2 → offer.json   (the campaign's WHAT — grand-slam gate)
          └ gtme-list → tam.jsonl                 (volume plan: offer_tier × goal)
             ├ gtme-signals → signals.jsonl   ┐ (parallel — no mutual dependency)
             └ gtme-enrich  → prospects.jsonl ┘
                └ gtme-score → scored.jsonl        (waits for signals + tam)
                   └ gtme-research → research.jsonl (tier-1 human_assisted accounts only)
                      └ gtme-write → messages.jsonl ★3 (offer.json = the WHAT-layer menu)
                         └ gtme-sequence → send_plan.jsonl ★4 (dry-run)
                            └ [human sends] → gtme-measure → measure.json ⟲ (feeds icp + score + offer)

gtme-publish → content_plan.jsonl   (parallel off context.json; reads offer.json opportunistically)
```

Run `gtme-signals` and `gtme-enrich` concurrently; `gtme-score` barriers on both. `gtme-publish` runs independently from the moment `context.json` exists.

## The four human gates (hard stops — never skip)

1. **★1 After `gtme-icp`** — hand the user editable `icp.md`. Highest-leverage correction point: a wrong ICP wastes every downstream row. User edits → compile to `icp.json` → continue.
2. **★2 After `gtme-offer`** — user reviews `offer.md` against the 10-question grand-slam gate (offer integrity, guarantee ops can cash, honest scarcity, tier). A wrong offer wastes every row the same way a wrong ICP does. **Re-confirming icp.json invalidates offer.json — re-open ★2.**
3. **★3 After `gtme-write`** — user reviews a sample of `messages.jsonl`. Voice and claims are theirs to vouch for.
4. **★4 Before `gtme-sequence` sends** — dry-run gated by design. Nothing leaves the building until the user runs the gated command. Standing pre-approval does not satisfy this (see `gtme-sequence`).

Between gates, run unattended.

## Blocked-state handling

Stages hard-stop by design when inputs are missing — this is correct, not a crash:
- `gtme-offer` with a thin `context.json` (no capabilities/proof) → `blocked_thin_context`; `gtme-write` with no confirmed `offer.json` → `blocked_no_offer`.
- `gtme-list` with no LinkedIn access → seeded/`blocked`, surfaces "connect + authenticate the LinkedIn MCP".
- `gtme-enrich` with no provider keys → `enrich.status.json` `blocked_no_provider`, empty `prospects.jsonl`.
- `gtme-sequence` with an unwired channel → `blocked`.

The orchestrator **surfaces the blocked stage and what unblocks it, then pauses that branch** — it does not fabricate data to proceed, and it lets independent branches (e.g. `gtme-publish`) continue. Report blocked states to the user with the exact remediation; resume when they unblock.

## The compounding loop

Real replies → `gtme-measure` → `measure.json` patch → applied on the next `gtme-icp` confirm + read as `signal_priors` by `gtme-score` + `offer_verdict` (a `primary_problem` verdict re-opens ★2). Batch two targets tighter than batch one. Inbound (`gtme-publish` engagement) and outbound feed the same score/write/sequence spine.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Skipping a human gate | Four gates are hard stops (icp, offer, messages, send). |
| Keeping a stale offer after an ICP edit | icp.json re-confirm invalidates offer.json; re-run ★2. |
| Fabricating data past a blocked stage | Surface the block + remediation; pause that branch. |
| Re-running completed stages | Skip-if-exists; the artifact is the marker. |
| Running signals→enrich serially | They're parallel; score barriers on both. |
| Treating publish as sequential | It runs off context.json in parallel. |
| Auto-sending | Send is always the human ★3 gate. |

## Related

Each stage is its own skill (`gtme-context` … `gtme-measure`, `gtme-publish`). Gating/handoff cross-cut via `gtme-why` and `gtme-handoff`. Signal/channel doctrine: `docs/build/signals-channels-doctrine.md`.
