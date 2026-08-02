---
name: gtme-why
description: Use at the start of a GTM run, before spending enrichment credits or reaching real people, to gate the campaign with a tested purpose. Triggers include "why this campaign", "is this run worth it", "gate the run", or the why-gate step of an auto-gtme run.
---

# gtme-why

## Overview

Gate the run with a *why* before it spends credits and touches real inboxes. A technically-perfect pipeline pointed at a purposeless campaign generates competent slop at scale — the most expensive failure. This is the layer above `gtme-icp`: `gtme-icp` decides *who*; `gtme-why` decides *whether, and why*.

Output: `runs/<slug>/00-why.md` — a confirmed purpose that gates `gtme-list`.

## When to Use

- At run start, before `gtme-list` (which spends enrichment credits). Optional but recommended — it's the discipline that keeps outbound honest.
- Re-enter when `gtme-measure` suggests the whole premise was wrong (not just the targeting).

## What it does

**REQUIRED SUB-SKILL:** invoke `why-chain` scoped to this run. Produce a why-chain whose leaf decision-rules distinguish *this* campaign from generic outbound:

- **Why reach these people at all?** What do they get — not what you sell. If the honest answer is "we want their money," the messages will read that way.
- **Why now?** The campaign's own why-you-why-now, above any single account's signal.
- **What would falsify it?** The kill-criterion: if X, this run shouldn't happen. (E.g. "the ICP can't actually act on this in the next quarter.")
- **What's the goal, as a number?** why.md carries one fenced yaml block (same gate mechanics as icp/offer): `goal: {metric: meetings|replies|deals, target: <n>, by: <date>}`. Downstream, `gtme-offer` reads it and `gtme-list` sizes the TAM pull against it — a why without a number can't gate volume.

If the why doesn't survive its own decision-rule test, **don't run** — fix the premise or kill the campaign. That's cheaper than a thousand well-crafted irrelevant messages.

## Gate

Emit `why.md` and STOP for confirmation, same as the ICP gate but at the purpose level. `gtme-list` does not run against an unconfirmed why. A confirmed why also seeds `gtme-write`'s framing — the messages inherit the campaign's real reason to exist.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Skipping straight to list-building | Gate the why first; credits + reputation are at stake. |
| A why that fits any campaign | The leaf rules must distinguish *this* one. |
| No kill-criterion | Name what would falsify the premise. |
| Purpose = "we want to sell" | State what the recipient gets; else the copy leaks it. |

## Next

Confirmed `why.md` → `gtme-icp` / `gtme-list` proceed, carrying a purpose the whole run inherits.
