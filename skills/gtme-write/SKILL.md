---
name: gtme-write
description: Use after accounts are scored, when you need to draft the actual outbound copy per prospect per channel. Triggers include "write the messages", "draft the outreach", "write the cold email/DM", or the message step of an auto-gtme run.
---

# gtme-write

## Overview

Draft outbound copy by **diffusion**: four layers, coarse to fine — WHO → WHY → WHAT → HOW. Each layer constrains the next; no copy is written until all four resolve. The one failure this skill exists to prevent is **generic AI slop** — messages that "sound good but could go to anyone." Every message opens with *why you, why now* (the prospect's own signal), or it doesn't send.

Output: `messages.jsonl`, one row per (prospect × channel × touch), structured for `gtme-sequence`.

## When to Use

- After `gtme-score`, before `gtme-sequence`. Input: `scored.jsonl` (order + `top_signal` + `direction` + `effort_mode` + `message_angle`), `prospects.jsonl` (validated contact), `context.json` (proof_points, value_props), **`offer.json` (confirmed — the WHAT layer's menu)**, and optionally `persona.md` (see Layer 1). Output: `runs/<slug>/messages.jsonl`
- Only for accounts with `route: send`. Suppressed accounts get no message.
- **Missing pipeline artifacts:** a manual brief may substitute for `scored.jsonl`/`context.json`, but (a) every substituted field is logged as an explicit assumption in the run notes, and (b) any email row without a validated contact is `send_eligible: false`. Never silently fabricate upstream data. **A manual brief does NOT substitute for `offer.json`** — no confirmed offer → write `blocked_no_offer` status, pause the branch, surface "run gtme-offer" (the ★2 gate is the point).

## Layer 1 — WHO (identity before ink)

Resolve both sides as *people* before drafting a word.

**Sender.** From `persona.md` if present — a local, never-committed artifact with these fields: role identity, nature (where they actually live online), psych (honest self-read → voice calibration), time & place, energy (what they compete on), a one-line **legibility line**, and a **trope map**. Absent `persona.md`, the sender is the company: `config.sender` + `context.json`.

**Reader mirror.** From the ICP + prospect record: role, domain depth, psych (rational/evidence-driven vs. relational), time & place, energy. Write to the person, not the title.

**Two checks before Layer 2** (no persona.md → derive both from `context.json` + channel knowledge):
1. **Legibility** — can the reader place the sender in one line? If not, the message carries an identity problem no copy fixes.
2. **Trope map** — list the patterns both sides are numb to on this channel (merge-tag cold email voice, LinkedIn founder-story cadence, job-seeker resume-attach energy). These become banned patterns enforced in Layer 4.

**Altitude.** Exec gets outcome + cost-of-delay; practitioner gets the how. **Early-stage founders are both** — lead with the outcome, attach the concrete artifact.

## Layer 2 — WHY (three whys, all explicit)

1. **Internal** — what the sender actually wants from *this* message (a reply, a yes). One thing.
2. **Material** — the measurable campaign outcome this message advances (replies → calls → deals/trials/offers).
3. **Reader-side** — why opening this adds value to *them*: they get spoken to about their actual issue, in their internal language, with value up front — delivered through the front-end offer selected in Layer 3. WHY states the intent; WHAT carries the offer.

**Offer mechanics live in `gtme-offer` now** (guarantee menu, collapse-the-funnel, scarcity rules — see that skill). Write consumes the confirmed stack; it never authors offer content. Still write-side: **collapse the funnel in the copy** — sell only the next step; if the ask needs two future yeses, the message carries weight it can't bear.

**Intent fidelity.** When the sender's ultimate intent differs from the surface offer (e.g. the offer is a free deliverable, the intent is a work trial or a hire), the intent must be legible enough that a reply never feels like bait-and-switch — one plain disclosure line. This is what the intent test (Layer 4) checks.

**Proof classes** — pick what the sender actually has; never invent:
| class | form | use when |
|---|---|---|
| case study | client outcome **with the metric**, mapped to this reader's pain, max 2 | sender has clients |
| proof-of-work | the artifact itself: repo, sample rows of the deliverable, a live demo | sender has no clients yet — demonstration of the exact skill being offered beats any promise |
| public track record | in-public campaign results, scoreboard, prior published work | it exists and this reader would recognize it |

## Layer 3 — WHAT (the personalized offer + format and arc)

**Select the offer first.** From confirmed `offer.json`, pick per prospect:
- the `problems` row matching this prospect: `signals` tags vs the account's `top_signal.type`, `persona` vs the prospect's role via the mapping `economic_buyer ↔ decision_maker`, `champion ↔ champion` (`practitioner` prospects take `champion`-tagged rows unless a `practitioner` row exists — the enums never string-match directly);
- the `front_end_offers` row that `reveals` that problem and matches the account's `direction`. No expansion-tagged row for an `expansion` prospect → fall back to rule 6's reframe (capability not yet turned on), never a cold acquire offer;
- the guarantee phrasing and offer name come from offer.json verbatim territory — rephrase for voice, never change terms. Scarcity lines only from `scarcity_facts`.

**Never invent offer elements.** The menu was human-gated at ★2; a write-time "improvement" is an ungated offer change.

**Arc:** hook → body → CTA as setup → shift → resolve. The hook names the signal; the body makes one turn (the offer's reveal); the CTA resolves to a single low-cost yes. State, before drafting: the **change** this message should cause in the reader, and the sender's **point of view** on the reader's situation.

**Big fast value:** if the selected front-end offer has `sampleable: true`, put a plaintext sample (rows of the map, findings of the audit) **in the touch-1 body** instead of asking permission to send it. Plaintext samples are not links; the no-links rule stands. Sample lines are exempt from the <75-word target (the 120 hard cap still binds). Naming an artifact without its URL ("auto-gtme, my open-source stack") is allowed — a curious reader searches. Fall back to the permission CTA ("May I send it over?") when the deliverable can't be excerpted — **no real sample exists → permission CTA, never synthetic rows.**

**Channel format table (hard constraints):**

| channel | touch | limit | links | tone |
|---|---|---|---|---|
| `linkedin_connect` | 1 | ≤300 chars | none | warm, name the signal, **no meeting ask** — earn the accept |
| `linkedin_dm` | 2+ | ≤120 words | sparingly | conversational, after accept |
| `email_cold` | 1 | subject ≤50 chars, lowercase/internal-style, no punctuation, 1–4 words ("think we should talk"); body ≤120 words hard cap, **target <75** (bands ~30/45/60) | **none — links tank first-touch deliverability** | plaintext, one idea |
| `email_followup` | 2+ | shorter than touch 1 | ok | new argument, same thread |
| `x_reply` | public | ≤280 chars | none | value-add in public, not a pitch |
| `x_dm` | warm only | short | none | only if they follow you |

Parallel touch-1s across channels are allowed (email + connect the same day); `gtme-sequence` owns timing. Copy must differ per channel.

## Layer 4 — HOW (anti-slop rules + the two gates)

Every rule is a send-blocker:

1. **Open with the signal** (touch 1). Name the specific trigger from `top_signal` in the first line. Never "I came across your company." In-thread follow-ups open with their *new argument* instead; `opens_with_signal` still records the account's `top_signal.type`.
2. **Kill the tells.** No merge-tag feel, no "hope this finds you well", "I wanted to reach out", "quick question", "circling back". If a phrase appears in every SDR's template, cut it.
3. **One idea per message.** The disclosure line from intent fidelity doesn't count as a second idea; a feature dump does.
4. **Proof mapped to pain, max 2,** from the Layer-2 proof class. No metric exists → use proof-of-work, don't invent one.
5. **CTA specific + low-cost.** One ask. "20 min before your new hire starts" beats "hop on a call."
6. **Match `direction`.** `acquire` = new-logo framing; `expansion` = "you already run us — here's the next thing," reframing proof as *a capability they haven't turned on yet*, never a re-pitch.
7. **Follow-ups add a new argument** — a fresh angle, new proof, cost-of-delay, or the **anti-case-study** (post-mortem of a company that made this exact mistake, with concrete failure detail and a detached close). Never "just bumping this."
8. **Shorter wins.** Cut every sentence that isn't load-bearing.
9. **Answer the five questions** in <75 words, implicitly: *How will you make me money? Have you shown you can do this? Did you research us? Are you a real person? Is this a waste of my time?*
10. **Altitude match** (from Layer 1). **Qualify in the copy** — if the message can't name why now, it's nurture, not outreach.

**The two gates — run on every draft, in order:**

- **Smell test.** Read it aloud. It must sound like a specific human typed it fast: zero AI-tells, zero template cadence, and it trips nothing on the Layer-1 trope map. Sounds like a template → it is one.
- **Intent test.** Restate the Layer-2 internal intent, then reread the draft: does the message still carry that intent, undiluted and legible? A well-written message that lost the actual ask fails.

**Gate failure → re-run from Layer 1.** Do not word-patch a failed draft; the defect is upstream (wrong identity frame, muddy why), and polishing the surface bakes it in.

**The forwardable test:** the email a champion can forward — self-contained, sells someone who's never heard of you.

**REFERENCE:** `research/04-psychology-nepq-persuasion.md` (NEPQ, Cialdini, cold-email craft), `research/11-x-primary-sources.md` (operator specimens, script frameworks, offer tiers).

## effort_mode branch

- `human_assisted` (tier-1) → **bespoke**. Full four-layer pass per prospect; draft goes to a human before send.
- `semi_auto` (tier-2) → signal-anchored, lightly templated; Layers 1–2 resolved once per segment.
- `fully_auto` (tier-3) → templated with variable slots, still opens with the signal, flows straight to `gtme-sequence` — a human never reads it, so the gates matter *more*, not less. Optional at volume: spintax.

## Sender identity

Sender name comes from run config (`config.sender`), inserted as `{{sender_token}}` — except `human_assisted` runs with a `persona.md`, where the real name may be written directly (a bespoke personal email with a merge token is itself a tell). **Never invent or guess a sender name.** No calendar link unless `config.booking_link` is set.

## messages.jsonl schema (fixed)

```json
{"account_id": "domain:mercury.com", "prospect": "Nick Dellis", "role": "champion",
 "channel": "email_cold", "touch": 1,
 "subject": "the revops hire", "body": "Nick — congrats on the Series D...",
 "opens_with_signal": "funding_raised", "direction": "acquire",
 "cta": "20 min before the new hire starts",
 "char_count": 812, "word_count": 118, "has_link": false, "sender_token": "{{sender_name}}",
 "send_eligible": true, "effort_mode": "human_assisted", "drafted_at": "<iso8601>"}
```

- `role` enum: `decision_maker` | `champion` | `practitioner`.
- `subject` is `null` for channels without one (linkedin_*, x_*). `email_followup` reuses the touch-1 subject (same thread).
- Email channels bind on `word_count` (≤120 hard cap, target <75); char-limited channels (linkedin_connect, x_*) bind on `char_count`.
- `send_eligible` — `false` if the channel's contact isn't valid: email channels require `prospects.email_status == validated`; linkedin_* require a known profile URL; x_* require a known handle. `gtme-sequence` refuses `false`.
- `sender_token` — holds `{{sender_name}}` normally; holds the literal name when human_assisted + persona.md (see Sender identity).
- `opens_with_signal` must equal the account's `top_signal.type`. Empty → not signal-anchored → don't emit it.
- `touch` — position in a thread (1, 2, 3…). Public non-thread channels (`x_reply`) always `touch: 1`.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Generic opener | First line names `top_signal`. No signal in line 1 → not sendable. |
| Feature dump | One idea. Max 2 proof points, mapped to pain. |
| Links in first cold email | None — deliverability. Plaintext samples instead. |
| Invented metric or logo | No proof? Use proof-of-work. Fabricated proof is a campaign-killer. |
| Authoring or "improving" offer elements at write time | offer.json is the ★2-gated menu — select and voice it, never change terms, deliverables, or guarantees. |
| Hidden ulterior intent | Fails the intent test on reply, not on send. One disclosure line. |
| Word-patching a failed gate | Defect is upstream — re-run from WHO. |
| Re-pitching a customer | Check `direction`; `expansion` ≠ `acquire`. |
| "Just bumping" follow-up | New argument or no send. |
| Same message across channels | Vary by channel; the sequence is coordinated, not copy-pasted. |
| Negative offer definition ("it's not X, Y, or Z") | Name what it IS in one line. |
| Irrelevant name-drops | Proof only counts if THIS reader recognizes it. |
| "I'll keep it short" then isn't | Never claim brevity; demonstrate it. |
| Wrong altitude | Match asset to seniority; founders get outcome + artifact. |
| Fake urgency | Scarcity only if literally true. |

## Next

`gtme-sequence` reads `messages.jsonl` → orchestrates multi-channel send (dry-run default) via the channel adapters.
