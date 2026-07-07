---
name: gtme-research
description: Use before writing outreach to a high-priority account, when firmographics aren't enough and you need per-account soft qualifiers and personalization hooks. Triggers include "research this account", "deep-dive the prospect", "what's the angle", or the per-account research step of an auto-gtme run.
---

# gtme-research

## Overview

Per-account deep research that turns a scored account into sharp, *true* personalization. Produces an account brief of dated hooks the message-writer pulls from directly. The failure this prevents: **hallucinated personalization** — inventing a detail about a prospect, which lands worse than generic because it's visibly wrong.

Output: `research.jsonl`, one brief per account.

## When to Use

- Between `gtme-score` and `gtme-write`, for **tier-1 `human_assisted` accounts** — spend human-grade research where fit is best (codyschneider: tier 1 earns the effort; tier-3 `fully_auto` accounts skip this).
- Input: scored account + contact. Output: `runs/<slug>/research.jsonl`

## The one discipline: every hook ties to a dated source

- **Every hook has a source URL and a date.** No dated source → not a hook, don't use it.
- **Verified fact and inference are separate.** Mark each hook `verified: true` only if seen at a citable source. `gtme-write` puts **only `verified: true` hooks in the copy** — inference guides the angle, never the assertion.
- Anything you can't verify is marked and never stated as fact in a message.

## Where the signal actually lives

- **The job description is the highest-signal document.** A hiring org confesses its pain in the *responsibilities* list, not the title. "Consolidate tooling", "reporting is manual", "own CRM platform" — each is a named pain. Read the JD body, not the headline.
- **The re-platform window:** CRM/tooling decisions get made in the ~6 months after a raise, before the org is too big to move. A raise + a new ops hire = that window is open now.
- Other sources: the contact's posts/comments, podcast/panel appearances, BuiltWith/tech mentions, ex-employee posts, the funding announcement, the CEO's feed.

## Landmines (what makes outreach misfire)

Surface disqualifying context so the writer doesn't step on it:
- JD *requires* the incumbent's admin experience (e.g. "Salesforce admin") → they're committed; don't pitch a rip-out.
- Contact is 4+ years in seat → owns the incumbent, harder; new-in-role → mandate to change.
- Still PLG vs. sales-led changes the whole pitch — don't assume.

## research.jsonl schema (fixed)

```json
{"account_id": "domain:mercury.com", "contact": "Nick Dellis",
 "angle": "hiring a RevOps lead right as the Series D scales the team — CRM becomes leverage or debt",
 "hooks": [
   {"hook": "open Rev Strategy & Ops req owns the CRM platform", "source": "https://.../jobs/...", "date": "2026-06", "confidence": "high", "verified": true},
   {"hook": "$200M Series D", "source": "https://...", "date": "2026-05-20", "confidence": "high", "verified": true}
 ],
 "landmines": ["JD requires Salesforce admin experience — don't pitch rip-out"],
 "researched_at": "<iso8601>"}
```

- `angle` → becomes `gtme-write`'s `message_angle`. `hooks` (verified only) → the specific personalization. `landmines` → what the writer must avoid.
- Order hooks **freshest first** — recency is the whole game.
- One row **per account** in `research.jsonl` (like `scored.jsonl`), not one file per account. `contact` is the resolved name from `prospects.jsonl`; if only a role is known, put the role and add `"needs_contact_resolution": true`.
- **Degraded (no-scrape) mode:** if nothing can be verified to a live source, set `"status": "research_todo"` — the brief is then a list of *leads to confirm* (angle + unverified hooks with `PLACEHOLDER_` sources), and `gtme-write` will not run on it until a human or live pass verifies at least one hook. A brief where every hook is `verified: false` is a to-do, not a usable brief.

## Common Mistakes

| Mistake | Fix |
|---|---|
| A hook with no dated source | Not a hook. Every hook cites a dated source. |
| Stating inference as fact | Only `verified: true` hooks enter the copy. |
| Reading the JD title, not the body | The responsibilities list is the pain confession. |
| Deep-researching tier-3 accounts | Reserve this for tier-1 `human_assisted`. |
| Missing a landmine | Surface disqualifying context (committed to incumbent, long-tenured buyer). |

## Next

`gtme-write` reads the brief → `angle` sets the message frame, `verified` hooks personalize, `landmines` constrain.
