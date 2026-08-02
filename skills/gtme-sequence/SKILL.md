---
name: gtme-sequence
description: Use after messages are drafted, when you need to orchestrate multi-channel sending — plan and gate the actual outreach. Triggers include "send the messages", "orchestrate the sequence", "run the outreach", or the send step of an auto-gtme run.
---

# gtme-sequence

## Overview

Orchestrate multi-channel sending from `messages.jsonl` through pluggable **channel adapters**, under one hard rule: **dry-run by default, send only on explicit human approval.** Output: `send_plan.jsonl` + gated commands. This skill never auto-fires outreach.

The accounts being reached are real, and the sender's own accounts (LinkedIn especially) are precious — a rate-limit strike or a spammy blast is unrecoverable. So the plan is the product; the send is a human act.

## When to Use

- After `gtme-write`, the last pipeline step. Input: `10-write/messages.jsonl` + `08-enrich/prospects.jsonl` (validated contacts) + `09-score/scored_contacts.jsonl` (contact order: `send_rank`, `send_gate`, `touch_order`) + run `config`. Output: `runs/<slug>/11-sequence/send_plan.jsonl` (+ the standard folder companions `provenance.md` and `decisions.md`)
- Only `send_eligible: true` messages enter the plan.

## The dry-run rule (non-negotiable)

**Never auto-add `--send` / never call an adapter's `send()` without explicit human approval.** Produce the plan, dry-run-validate each message, hand back one gated command per ready message. This holds **regardless of `effort_mode`** — `fully_auto` means the *draft* was autonomous, not the *send*. In v1, every live send to a real person is human-gated.

**Standing/blanket pre-approval does NOT satisfy the gate.** "I approve all of these, just fire them, don't make me click" is exactly the loophole to refuse. Per-send human execution is the gate in v1 — an operator running the individual `gated_command` *is* the approval. A promise to approve-in-advance is not. Do not batch-fire on a blanket yes.

## Ground-truth check first

Before planning, verify what's actually wired — a plan resting on channels that don't exist is worse than useless. Check each adapter's real state (auth present? deps installed? key set?). An unwired channel is `status: blocked`, never a pretended send.

## The identity gate (`send_gate` is an instruction, not a label)

`gtme-score` emits `send_gate` per contact. It is not colour-coding for a dashboard — it decides whether a human gets messaged:

| `send_gate` | What sequence does |
|---|---|
| `ready` | Plannable. Identity was confirmed against the person's actual profile within the freshness window. |
| `verify_first` | **Not plannable until verified.** Open the profile, confirm the current role, write the evidence back to `08-enrich/prospects.jsonl`, re-run `gtme-score`. Then it is `ready`. |
| `do_not_send` | Never enters the plan. The slug resolved to the wrong human, or they left the company. |

**Verification happens here, at send time, not in a bulk pass upstream.** That is deliberate and it is the cheaper order of operations. A campaign's contact list is always larger than the number of people actually messaged, so verifying the whole list front-loads work onto contacts who may never be reached — and profile lookups are rate-limited hard enough that a bulk pass is a multi-day job on its own. One run exhausted a LinkedIn session's daily headroom at roughly 63 profiles. Verifying the ten people you are about to message this morning never comes close.

What "verify" means concretely, per contact, before it enters the plan:

1. Open their profile. Not a search result, not a cached record — the page.
2. Read the **current role line** in the experience section. The headline is self-written marketing and is wrong often enough to be dangerous: one live run held a contact whose headline still read "at Blockchain.com" while his role there was end-dated four months earlier.
3. Write back `identity: {pulled, says}` with that line verbatim, plus `employer_history` and `education`, and set `record_status`. `prospects.schema.json` rejects a `verified` record missing any of it.
4. Re-run `gtme-score`. A contact that is still `verify_first` does not go in the plan.

A throttled or failed lookup is **not** a verification result. Leave the contact `unchecked` and retry later. Writing `not_found` because the tool errored records a conclusion nobody reached — the precise failure this gate exists to prevent.

## Channel adapters

Common interface (pluggable — new channel = new adapter, no orchestration change):

```
Adapter.can_reach(prospect) -> bool         # valid identifier for this channel?
Adapter.dry_run(message)    -> result       # validate; NEVER sends
Adapter.send(message, approved=True) -> result   # only with explicit human approval
```

| Adapter | State | Sends | Notes |
|---|---|---|---|
| `linkedin` | **built** (`cli/gtme-linkedin`) | connect + DM | already `--send`-gated; dry-run default. Softest first touch. |
| `email_smtp` | needed | cold + follow-up | zero-dep default (Gmail app password). Only `email_status: validated`. |
| `email_instantly` | optional | cold at volume | for warmed-inbox scale. |
| `x_bird` | built (`bird`) | reply + follow only | **no cold DM** (X blocks non-followers). Public warm touch. |
| `manychat` | via `gtme-publish` | IG/FB/WA opt-in | inbound comment-to-DM, not cold. |

Missing adapter → `status: blocked`, honest reason. Never fabricate a send path.

## Sequencing rules

- **One channel-of-record for touch 1.** LinkedIn connect leads (softest); email is the parallel/fallback track. The plan is **multichannel by default** — every wired channel runs as a parallel track across the sequence window, staggered by day.
- **Never the same prospect on two channels the same day** — reads as a bot.
- **Space touches:** email follow-up at day 3–4, gated on *no reply*.
- **Route cadence by reply latency.** A reply within hours → accelerated cadence (next touch sooner, human pulled in); days-to-weeks latency → standard spacing. Speed of response is a routing input, not trivia.
- **Reply = state change, two states.** Any reply cancels the *cold* sequence. An **interested** reply routes to the **nurture track**: up to 10 value-led touches, 3–5-day gaps, ≤75 words each — touches 1–3 nurture with insights/resources, 4–6 address objections + social proof, 7–8 gentle urgency + results, 9–10 final value + soft close. A negative reply ends everything.
- **Email caps:** ≤40 sends/inbox/day, distributed across business hours — never burst; spam filters pattern-match send timing. Scale = more warmed inboxes (~12-inbox pods ≈ 480/day), never more per inbox. Full volume to `email_status: validated` only; `risky` never at volume.
- **Rate limits (protect the sender's accounts):** LinkedIn ≤20 connects/day, ≤40 DMs/day. Aggressive operators run 200 connects/wk on Sales Nav + automation (fin465, YC playbook) — ban risk is unrecoverable; the cap holds. Exceeding these risks an account ban — hard cap.
- **first_touch persona first** — reach the `first_touch` contact (champion) before the economic buyer.

## send_plan.jsonl schema (fixed)

```json
{"account_id": "domain:mercury.com", "prospect": "Nick Dellis", "role": "champion", "first_touch": true,
 "channel": "linkedin_connect", "touch": 1,
 "status": "ready", "reason": "dry-run passed, exit 0", "scheduled": "day 0",
 "requires_human_approval": true,
 "gated_command": "gtme-linkedin person connect nick-dellis --note '...' --send"}
```

- `status` — `ready | blocked | held | sent`. `blocked` = no adapter/invalid contact; `held` = suppressed upstream or gated on a prior touch; `sent` = only after a human ran the command.
- `gated_command` — the exact command a human runs to send. Present (a string) only for `ready`; `null` for every other status. You never run it.
- `role` + `first_touch` — carried from the prospect; sequencing reaches the `first_touch` champion before the economic buyer.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Auto-adding `--send` | Never. Plan + gated command; human sends. |
| `fully_auto` → auto-send | Draft autonomy ≠ send autonomy. All sends gated in v1. |
| Planning against an unwired channel | Ground-truth check first; unwired = `blocked`. |
| Same prospect, two channels, same day | One channel-of-record for touch 1. |
| Ignoring rate limits | Hard caps; a ban is unrecoverable. |
| Sending to an unvalidated email | Email needs `email_status: validated`. |
| Planning a `verify_first` contact | Verify it, write the evidence back, re-score. The gate is an instruction, not a warning label. |
| Verifying off the headline instead of the role line | Headlines are self-written and go stale silently. One contact's headline still claimed a job that ended four months earlier. |
| Marking a contact `not_found` because the lookup errored | A throttled tool is not evidence about a person. Leave it `unchecked` and retry. |
| Treating an interested reply as "done" | Route to the nurture track; the meeting isn't booked until it's booked. |

## Next

`gtme-measure` reads send outcomes (replies, meetings) → re-weights signals + ICP for the next cycle.
