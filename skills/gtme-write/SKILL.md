---
name: gtme-write
description: Use after accounts are scored, when you need to draft the actual outbound copy per prospect per channel. Triggers include "write the messages", "draft the outreach", "write the cold email/DM", or the message step of an auto-gtme run.
---

# gtme-write

## Overview

Draft signal-anchored outbound copy per prospect per channel. The one failure this skill exists to prevent is **generic AI slop** — messages that "sound good but could go to anyone." Every message opens with *why you, why now* (the prospect's own signal), or it doesn't send.

Output: `messages.jsonl`, one row per (prospect × channel × touch), structured for `gtme-sequence`.

## When to Use

- After `gtme-score`, before `gtme-sequence`. Input: `scored.jsonl` (order + `top_signal` + `direction` + `effort_mode` + `message_angle`), `prospects.jsonl` (validated contact), `context.json` (proof_points, value_props). Output: `runs/<slug>/messages.jsonl`
- Only for accounts with `route: send`. Suppressed accounts get no message.

## The anti-slop rules (the heart — every rule is a send-blocker)

1. **Open with the signal.** Name the specific trigger from `top_signal` in the first line. "Saw Mercury's Series D + your open RevOps req" — never "I came across your company" / "I've been following your work."
2. **Kill the tells.** No `{First Name}` merge-tag feel, no "hope this finds you well", "I wanted to reach out", "quick question", "circling back". If a phrase appears in every SDR's template, cut it.
3. **One idea per message.** No feature dump. The baseline that works hangs the whole message on one thought (here: "a CRM choice made now is expensive to reverse").
4. **Proof mapped to pain, max 2.** Pull `proof_points` that map to *this* prospect's implied pain, with the metric. Not a list of logos.
5. **CTA specific + low-cost.** "20 min before your new hire starts" beats "hop on a call". One ask. Two named moves that shift risk to the sender: **risk reversal** ("you don't pay until you've interviewed and hired someone you like") and the **permission CTA at touch 1** ("May I send over some candidate intros so you can judge for yourself?").
6. **Match `direction`.** `acquire` = new-logo framing. `expansion` = "you already run us — here's the next thing", never re-pitch the product to a customer. Getting this wrong is the most embarrassing miss. **Proof for expansion:** most `proof_points` are new-logo case studies — for an `expansion` message, reframe the metric as *a capability they haven't turned on yet* ("Ramp cut CRM admin 40% with the routing agents — the ones you haven't switched on"), not "here's why to buy". Use expansion-specific proof if the seller has it.
7. **Follow-ups add a new argument.** Never "just bumping this". A second touch introduces a fresh angle (cost-of-delay, a new proof) or it doesn't send. The canonical new argument for a stalled tier-1: the **anti-case-study** — a post-mortem of a company that made the exact mistake this prospect is about to make, with concrete failure detail ("month 4, broke their CRM") and a detached close ("even if you don't end up using us"). Source material: `context.json.proof_points` failure stories, not just wins.
8. **Shorter wins.** A VP reads four lines, not twelve. Cut every sentence that isn't load-bearing.
9. **Read it aloud.** If it sounds like a template, it is one. Rewrite.
10. **Answer the five questions.** In <75 words the message must implicitly answer: *How will you make me money? Have you helped others just like me? Did you research us? Are you a real person? Is this a waste of my time?* Miss one → not sendable.
11. **Altitude match.** The asset/message fits the recipient's seniority — a product demo is the wrong asset for a budget owner; an exec gets outcome + cost-of-delay, a practitioner gets the how.
12. **Qualify in the copy.** Write to a pain that exists *and* is urgent now. Enthusiasm is not a reason to buy — if the message can't name why now, it's nurture, not outreach.

## Front-end offer

Propose a specific low-friction deliverable before selling the core service. Starters: *"[Audit] 5-point audit (24 hrs)"*, *"[Playbook] 2-page sequence ready to paste"*, *"[Teardown] Loom review with prioritized fixes"*, *"[Benchmark] peer comparison, 3 charts"*. "Lead with value" means one of these, named, not a sentiment.

## Channel format table (hard constraints)

| channel | touch | limit | links | tone |
|---|---|---|---|---|
| `linkedin_connect` | 1 | ≤300 chars | none | warm, name the signal, **no meeting ask** — earn the accept |
| `linkedin_dm` | 2+ | ≤120 words | sparingly | conversational, after accept |
| `email_cold` | 1 | subject ≤50 chars — prefer 1–3 words, no punctuation, lowercase/internal-style ("think we should talk"); body ≤120 words hard cap, **target <75** (bands ~30/45/60) | **none — links tank first-touch deliverability** | plaintext, one idea |
| `email_followup` | 2+ | shorter than touch 1 | ok | new argument, same thread |
| `x_reply` | public | ≤280 chars | none | value-add in public, not a pitch |
| `x_dm` | warm only | short | none | only if they follow you |

## effort_mode branch

- `human_assisted` (tier-1) → **bespoke**. Reference something specific to *this* company; the draft goes to a human to approve/tweak before send.
- `semi_auto` (tier-2) → signal-anchored, lightly templated.
- `fully_auto` (tier-3) → templated with variable slots, still opens with the signal, flows straight to `gtme-sequence` — a human never reads it, so the anti-slop rules matter *more*, not less. Optional at volume: spintax — vary sentence-level phrasing per send so filters can't fingerprint the campaign. Not a send-blocker.

## Sender identity

The sender name/handle comes from run config (`config.sender`), inserted as `{{sender_name}}`. **Never invent or guess a sender name.** No calendar link unless `config.booking_link` is set.

## messages.jsonl schema (fixed)

```json
{"account_id": "domain:mercury.com", "prospect": "Nick Dellis", "role": "champion",
 "channel": "email_cold", "touch": 1,
 "subject": "the RevOps hire + your CRM stack", "body": "Nick — congrats on the Series D...",
 "opens_with_signal": "funding_raised", "direction": "acquire",
 "cta": "20 min before the new hire starts",
 "char_count": 812, "word_count": 118, "has_link": false, "sender_token": "{{sender_name}}",
 "send_eligible": true, "effort_mode": "human_assisted", "drafted_at": "<iso8601>"}
```

- Both `char_count` and `word_count` are always present. **Email channels bind on `word_count` (≤120 hard cap, target <75); char-limited channels (linkedin_connect, x_*) bind on `char_count`.** Check the one that governs the channel.
- `send_eligible` — `false` if the channel's contact isn't valid (e.g. email channel but `prospects.email_status != validated`). `gtme-sequence` refuses `false`.
- `opens_with_signal` must equal the account's `top_signal.type`. If it's empty, the message isn't signal-anchored — don't emit it.
- `touch` — the numbered position in a DM/email thread (1, 2, 3…). Public non-thread channels (`x_reply`) always use `touch: 1`; they aren't part of the numbered sequence.

## Deeper copy craft

**REFERENCE:** `research/04-psychology-nepq-persuasion.md` — NEPQ, Cialdini, cold-email copywriting for when a message needs more than the rules above. Also `research/11-x-primary-sources.md` — operator specimens, script frameworks, offer tiers.

**The forwardable test:** write the email your champion can forward — self-contained, sells someone who's never heard of you.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Generic opener | First line names `top_signal`. No signal in line 1 → not sendable. |
| Feature dump | One idea. Max 2 proof points, mapped to pain. |
| Links in first cold email | None — deliverability. |
| Re-pitching a customer | Check `direction`; `expansion` ≠ `acquire`. |
| "Just bumping" follow-up | New argument or no send. |
| Guessed sender name | `{{sender_name}}` from config only. |
| Same message across channels | Vary by channel; the sequence is coordinated, not copy-pasted. |
| Negative offer definition ("it's not X, Y, or Z") | Name what it IS in one line. |
| Irrelevant name-drops | Proof only counts if THIS reader recognizes it — unrecognized logos reveal the blast. |
| "I'll keep it short" then isn't | Never claim brevity; demonstrate it. |
| Wrong altitude | Demo for an exec / ROI deck for a practitioner — match the asset to seniority. |

## Next

`gtme-sequence` reads `messages.jsonl` → orchestrates multi-channel send (dry-run default) via the channel adapters.
