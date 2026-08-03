---
name: gtme-send
description: Use when a sequence spec and drafted messages exist and the outreach must be materialized and sent - real timestamps, identity gates, channel adapters, dry-run by default. Triggers include "send the messages", "run the outreach", or the send step of an auto-gtme run.
---

# gtme-send

## Overview

Materialize `05-sequence/sequence.json` against real contacts and real clocks, then hand back gated commands. The spec says "touch 2, recipient-local 09:00-11:00, three days after touch 1"; this resolves that to Tuesday 09:40 New York for a named person, checks the channel is wired and the identity is confirmed, and stops.

One hard rule: **dry-run by default, send only on explicit human approval.** Output: `11-send/send_plan.jsonl` + gated commands. This skill never auto-fires outreach.

The accounts being reached are real, and the sender's own accounts (LinkedIn especially) are precious - a rate-limit strike or a spammy blast is unrecoverable. So the plan is the product; the send is a human act.

## When to Use

- After `gtme-write`, the last pipeline step before measurement. Input: `05-sequence/sequence.json` (confirmed - the shape, the send window, the branch rules), `10-write/messages.jsonl` (the drafted touches), `07-enrich/prospects.jsonl` (validated contacts), `08-score/scored_contacts.jsonl` (`send_rank`, `send_gate`, `touch_order`), and `channel-plan.json` (`sender_identity`, `suppression_list`, daily caps). Output: `runs/<slug>/11-send/send_plan.jsonl` (+ `provenance.md` and `decisions.md`)
- Only `send_eligible: true` messages enter the plan.

## What this stage decides, and what it does not

It does **not** decide the sequence. Touch count, ordering, timing rules, what each touch is for, and the branch conditions are all settled in `05-sequence/sequence.json` and gated there. Re-deciding any of them here would put the campaign's shape downstream of its own messages, which is the arrangement this split exists to end.

It decides the things that can only be known now: what time it actually is where the recipient lives, whether this specific person's identity has been confirmed, whether the channel is wired this morning, and whether an earlier touch's precondition was met.

## Materializing the window

`sequence.json send_window` is a rule, not a timestamp. Resolve it per contact:

- Recipient-local means their location, from `prospects.jsonl`. **When location is unknown, say so in the row** rather than silently substituting the sender's timezone - a 09:00 rule applied in the wrong hemisphere is a 22:00 send.
- Skip weekends and recipient-local public holidays.
- `day_offset` counts from that contact's touch 1, never from a campaign start date. Contacts enter on different days.

## Preconditions between touches

A touch may carry `requires` (the multichannel template's DM steps require the connection request to have been accepted). Check it against real state at send time, and when it is unmet, honor `skip_if_unmet` rather than sending anyway. **Never DM into a pending connection request** - it reaches nobody and burns the touch.

## Branch state

On a `spec: dag/1` sequence this stage is a **state machine over `nodes[]` and `edges[]`**, and it contains no model call — every message was pre-rendered per contact by `gtme-write`, so the only question at send time is which pre-written message goes now. Hold per contact: current node id, when they entered it, and the events seen since. Each tick, evaluate that node's outgoing `edges[]` in `priority` order (lower wins) and take the first that fires — an edge fires when its `when` event has occurred, or when `when` is `timeout` and `after` has elapsed **since the contact entered the node**, not since sequence start. Then send the current node's message if it is a `message` node and the channel's daily cap allows; if the cap is exhausted, defer to the next tick rather than skipping, because a skipped touch silently shortens the sequence. A `terminal` node ends the run and records its `outcome`; `gtme-measure` attributes against those, so "finished unanswered" and "bounced on touch 1" stay distinguishable. On a v1 sequence, read `branches` instead. Either shape, this stage enforces:

- **Any reply cancels the cold sequence, on every channel** - not just the one they replied on. A scheduled follow-up landing after a human answered is the clearest possible tell that nobody is reading.
- **A human reply is never classified here.** `reply_human` routes to a `human_gate` node, where a person chooses. The engine emits no `classified_*` event and must not infer intent from the reply text: "who is this?" and "send me pricing" are the same event and want opposite next moves.
- **`is_final_cold` is enforced, not merely written.** After that node sends, no node with `stage: cold` may be entered. The copy says "this is the last time"; this is what makes it true.
- A **negative** reply stops everything and the contact enters `suppression_list`; `bounce_hard` and `unsubscribe` go straight to terminal with no retry.

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
| `verify_first` | **Not plannable until verified.** Open the profile, confirm the current role, write the evidence back to `07-enrich/prospects.jsonl`, re-run `gtme-score`. Then it is `ready`. |
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

## send_plan.jsonl schema (fixed)

```json
{"account_id": "domain:mercury.com", "prospect": "John Smith", "role": "champion", "first_touch": true,
 "channel": "linkedin_connect", "touch": 1,
 "status": "ready", "reason": "dry-run passed, exit 0", "scheduled": "day 0",
 "requires_human_approval": true,
 "gated_command": "gtme-linkedin person connect john-smith --note '...' --send"}
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

## Rate limits and pacing (protect the sender's accounts)

The sequence spec says when a touch is due. These say whether it may actually go today.

- **Never the same prospect on two channels the same day** - reads as a bot.
- **Email:** <=40 sends/inbox/day, distributed across business hours, never bursted; spam filters pattern-match send timing. Scale means more warmed inboxes (~12-inbox pods ~= 480/day), never more per inbox. Full volume to `email_status: validated` only; `risky` never at volume.
- **LinkedIn:** <=20 connects/day, <=40 DMs/day. Aggressive operators run 200 connects/week on Sales Navigator with automation (fin465, YC playbook); the ban risk is unrecoverable, so the cap holds. This is the same ceiling `research/01` states as ~100 connects/week on a standard account.
- **`first_touch` persona first** - reach the champion before the economic buyer.
- **Reply latency routes cadence.** A reply within hours pulls the next touch in and a human with it; days-to-weeks latency keeps standard spacing. Speed of response is a routing input, not trivia.

When a cap would be exceeded, the row is deferred with the reason recorded - never dropped silently, and never sent anyway.

## Next

`gtme-measure` grades the cycle and attributes outcomes to `sequence.json` `template_id` + `template_version`, which is what lets the template library improve rather than drift.
