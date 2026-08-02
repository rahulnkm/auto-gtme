---
name: gtme-handoff
description: Use to snapshot a GTM run's state for resume, handoff, or context compaction — mid-run or before ending a session. Triggers include "hand off this run", "snapshot the run", "resume state", or when a run spans sessions/agents.
---

# gtme-handoff

## Overview

Capture a run's state so any session or agent can resume it without re-deriving. A run's artifacts (`runs/<slug>/`) hold the *data*; this holds the *decisions and next action* that the files don't — why the ICP was edited the way it was, what's blocked, what to do next.

Output: `runs/<slug>/99-handoff.md`.

## When to Use

- Mid-run before a context boundary, session end, or agent handoff
- When a stage is blocked and a human needs to pick it up
- Before compaction of a long run

## What it captures

**REQUIRED SUB-SKILL:** invoke `handoff` scoped to the run. Capture:

- **The why** — the confirmed `why.md` purpose (so the resumer inherits it, not just the mechanics).
- **Progress** — which stages have artifacts in `runs/<slug>/`, which are pending. The directory is the state; name what's done.
- **Key decisions** — ICP edits and their reasoning, signal-priors from `measure.json`, any human-gate approvals given.
- **Blocked states + remediation** — the exact unblock (e.g. connect/authenticate the LinkedIn MCP, set `LEADMAGIC_API_KEY`), so the resumer acts, not investigates.
- **Next action** — the single next command or gate.

## Rules

- **Point to artifacts, don't duplicate them.** Reference `scored.jsonl`; don't paste it. The handoff is decisions + pointers, not a data dump.
- **Every blocked state names its remediation** — a handoff that says "enrich failed" without "set these keys" makes the resumer redo the diagnosis.
- **Carry the why forward** — a resumer with the mechanics but not the purpose competently continues the wrong campaign.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Dumping artifact contents | Point to files; capture only decisions + next action. |
| Omitting the why | Carry `why.md` forward; purpose survives the seam. |
| Blocked state with no remediation | Name the exact unblock command. |
| No single next action | End with the one next command or gate. |

## Next

A resumer reads `handoff.md` → inherits purpose + progress + the next action, and continues the run.
