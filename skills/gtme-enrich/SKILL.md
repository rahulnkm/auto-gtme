---
name: gtme-enrich
description: Use after signals have qualified accounts, when you need to resolve and validate real contacts before writing outreach. Triggers include "enrich the accounts", "find the contacts", "get emails", or the enrichment step of an auto-gtme run.
---

# gtme-enrich

## Overview

Resolve the ICP's target contacts per qualified account, through a **cost-ordered provider waterfall**, and **validate every contact through 1lookup** before it can enter a send queue. Output: `prospects.jsonl`.

**The one rule that matters: never fabricate a contact.** A guessed email that bounces burns the seller's sending-domain reputation — the one thing a cold pipeline cannot afford. Real emails come only from a provider + validation. A pattern-guess is never sendable.

**Data quality is the performance ceiling.** No copy, volume, or technique overcomes bad data — fixing the data layer alone moved Owner's per-BDR closed-won from ~$72k to ~$120k/month (Kyle Norton, Attio GTM Atlas). This skill's strictness is where that lift lives.

## When to Use

- After `gtme-signals`, before `gtme-write`. Input: qualified `tam.jsonl` accounts + the ICP's `personas` + `contacts_per_account`. Output: `runs/<slug>/prospects.jsonl`
- Re-run to refresh stale contacts or resolve `pass_near_ceiling` accounts live

## Hard-stop guard (non-negotiable)

**If no enrichment provider is reachable, STOP.** Check these env vars: `LEADMAGIC_API_KEY`, `FINDYMAIL_API_KEY`, `PROSPEO_API_KEY`, `PDL_API_KEY`, `LOOKUP_API_KEY`. If none of the four waterfall providers is set, hard-stop. `LEADMAGIC_API_KEY` + `LOOKUP_API_KEY` is the minimum viable pair (one resolver + the validator).

On hard-stop:
- Write `runs/<slug>/enrich.status.json`: `{"status": "blocked_no_provider", "missing_keys": [...], "at": "<iso>"}` and an **empty** `prospects.jsonl`, so the orchestrator knows why nothing advanced.
- **Never pattern-guess an email.** Never invent a contact **name** from memory either — that is the same fabrication.
- A contact may be added `email_status: unvalidated_no_provider` **only** if a real tool resolved a real profile (`mcp__linkedin__get_person_profile` returning an actual person at the account). No such tool reachable → empty output. "Public sources" never means recalled-from-memory.

## The waterfall

Per contact, query providers **in cost order, stop at the first good hit:**

1. **LeadMagic** — strongest B2B work-email + LinkedIn-URL→email; good coverage. Opener.
2. **Findymail** — high accuracy, verifies before returning.
3. **Prospeo** — cheap LinkedIn-URL→email; good filler.
4. **People Data Labs** — broadest DB but noisier/staler; the safety net, not the opener.

**Stop rule:** accept the first provider returning an email with its own confidence ≥ valid/high. On a `catch-all`/`risky` result, **continue the waterfall** rather than accept it. Don't keep spending calls after one clean hit.

Provenance: this order is independently corroborated in production — coldemailchris runs LeadMagic → Prospeo; codyschneider names LeadMagic/Findymail/Prospeo/PDL as the cheap waterfall; Findymail as the ~$0.05/email backstop (kai_cabero).

## 1lookup validation gate (required final step)

Validate **every** resolved email regardless of source: `POST https://app.1lookup.io/api/v1/email` body `{"email": "..."}`, header `Authorization: Bearer $LOOKUP_API_KEY`.

- `deliverable` → `email_status: validated` (send-eligible)
- `undeliverable` → drop the contact from the send list (do not guess a replacement)
- `risky` / `catch-all` → not send-eligible; keep as `email_status: risky` for a human, or drop
- Phone (`/phone`) validate **champion only** — cold-calling the economic buyer isn't the play.

**Only `email_status: validated` is send-eligible.** `gtme-sequence` refuses anything else on email channels.

Verification tier maps to **send volume**, not just eligibility: `validated` = full volume; `risky` = never at volume (human-gated trickle at most); `undeliverable` = dropped — chasing dead emails tanks the sending domain within days.

## prospects.jsonl schema (fixed — gtme-write + gtme-sequence read these)

```json
{"account_id": "domain:ramp.com", "company": "Ramp", "tier": 1,
 "role": "champion", "first_touch": true,
 "name": "Kevin Dzierzawski", "title": "Head of RevOps", "linkedin": "kevin-dzierzawski",
 "email": "kevin@ramp.com", "email_source": "leadmagic", "email_status": "validated",
 "phone": null, "confidence": 0.9, "enriched_at": "<iso8601>", "sources": ["https://..."]}
```

- `email_source` — `leadmagic | findymail | prospeo | pdl | pattern_guess | none`
- `email_status` — `validated | risky | pattern_guess | undeliverable_dropped | unvalidated_no_provider`. Only `validated` sends on email.
- `role` / `first_touch` — carried from the ICP persona; `gtme-sequence` reaches the `first_touch` contact first.
- Map ICP titles to the real org: if the exact title doesn't exist (no "VP Revenue"), pick the closest revenue-owning exec and note it in `sources`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Guessing an email when providers are unreachable | Hard-stop. `unvalidated_no_provider`, never send-eligible. |
| Accepting a `catch-all` result | Continue the waterfall; catch-all ≠ valid. |
| Skipping 1lookup | Validation is required; unvalidated never sends. |
| Emitting pattern-guess as `validated` | `email_source: pattern_guess` can never be `email_status: validated`. |
| Cold-calling the CEO | Phone validate/collect for the champion only. |
| Forcing a nonexistent ICP title | Pick the closest revenue-owner; document the substitution. |

## Next

`gtme-write` reads `prospects.jsonl` (validated contacts) + their account's `signals.jsonl` → signal-aware message per channel.
