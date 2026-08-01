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

- After `gtme-signals`, before `gtme-write`. Input: qualified `list/tam.jsonl` accounts + the ICP's `personas` + `contacts_per_account`. Output: `runs/<slug>/enrich/prospects.jsonl` (+ the standard folder companions `provenance.md` and `decisions.md`)
- Re-run to refresh stale contacts or resolve `pass_near_ceiling` accounts live

## Hard-stop guard (non-negotiable)

**If no enrichment provider is reachable, STOP.** Check these env vars: `LEADMAGIC_API_KEY`, `FINDYMAIL_API_KEY`, `PROSPEO_API_KEY`, `PDL_API_KEY`, `LOOKUP_API_KEY`. If none of the four waterfall providers is set, hard-stop. `LEADMAGIC_API_KEY` + `LOOKUP_API_KEY` is the minimum viable pair (one resolver + the validator).

On hard-stop:
- Write `runs/<slug>/enrich/status.json`: `{"status": "blocked_no_provider", "missing_keys": [...], "at": "<iso>"}` and an **empty** `prospects.jsonl`, so the orchestrator knows why nothing advanced.
- **Never pattern-guess an email.** Never invent a contact **name** from memory either — that is the same fabrication.
- A contact may be added `email_status: unvalidated_no_provider` **only** if a real tool resolved a real profile (`mcp__linkedin__get_person_profile` returning an actual person at the account). No such tool reachable → empty output. "Public sources" never means recalled-from-memory.

## The waterfall

Per contact, query providers **in cost order, stop at the first good hit:**

1. **LeadMagic** — strongest B2B work-email + LinkedIn-URL→email; good coverage. Opener.
2. **Findymail** — high accuracy, verifies before returning.
3. **Prospeo** — cheap LinkedIn-URL→email; good filler.
4. **Wiza** — LinkedIn Sales Navigator export-backed; batch-first, good when you already have a Sales Nav list (Schneider's step 4).
5. **People Data Labs** — broadest DB but noisier/staler; the safety net, not the opener.

**Stop rule:** accept the first provider returning an email with its own confidence ≥ valid/high. On a `catch-all`/`risky` result, **continue the waterfall** rather than accept it. Don't keep spending calls after one clean hit.

Provenance (corrected 2026-07-25 after a primary-source check): the **primary practitioner source is Nick Abraham (Leadbird)**, speaking on Cody Schneider's podcast — *"the best thing to do when it comes to data right now is you have to do a waterfall... My favorite one by far right now is Lead Magic. They have the highest enrichment percentage that we've seen. And then I think Find[ymail] is a close second. And then there's a whole bunch of other ones like Prospeo"* ([In The Pit, Cold Email State of The Union](https://www.youtube.com/watch?v=4kljkbbfs_8) @08:05). Cody Schneider posts the same cascade on X with Wiza inserted at step 4 ([x.com/codyschneider/status/2043736058567786978](https://x.com/codyschneider/status/2043736058567786978)) — treat as **vendor-adjacent**: those posts pitch his own product (Graphed.com), and the podcast material widely attributed to him is actually his guest's. coldemailchris (LeadMagic → Prospeo) and kai_cabero (Findymail as the ~$0.05/email backstop) are the independent corroboration. The convergence across three unrelated practitioners is why the order stands; no single source here is authoritative.

## The independent-verifier rule (non-negotiable)

*(Practitioner sourcing for this section and the waterfall: `research/14-practitioner-signals-enrichment.md`.)*

**Never trust an enrichment provider's own `verified` flag.** Every resolved email goes through a validator that is not the provider that found it. Nick Abraham's waterfall and Cody Schneider's both bolt an independent check on the end for the same reason — in Cody's words, *"don't trust the 'verified' flag from the enrichment provider itself — they all lie a little. one extra api call saves your sender reputation"* ([x.com/codyschneider/status/2043736058567786978](https://x.com/codyschneider/status/2043736058567786978)).

A provider marking its own result deliverable is a vendor grading its own homework: the flag is an input to the decision, never the decision. One extra call per contact costs cents; a bounce rate spike costs the sending domain, which is unrecoverable on the timescale of a campaign. This applies even when the provider is the validator's parent company — same-vendor verification does not satisfy the rule.

## LinkedIn people-search: two rules learned the hard way

**Never put OR operators in a company-scoped people search.** `<Company> head of fraud OR chief compliance` silently drops the company token and returns unfiltered network noise — two separate agents burned searches on this before noticing. Company-scoped searches must be a single term: `<Company> fraud`. Run the second search only with a different single keyword (`<Company> trust safety`), never a boolean.

Watch the fuzzy-match collisions too: LinkedIn matched `Navan` to the first name *Navin*, `Bitvavo` to *bit avo*, and `Teya` to seven people whose first name is Teya. When a company name is a common word or a near-name (Branch, Coast, Step, Root, Circle, BILL, Swan, Navan), disambiguate with the legal or long form — `Root Insurance` not `Root` — and verify the employer on **every** result.

**Apply the per-account contact cap AFTER sorting by connection degree, not by persona role.** The ICP asks for one champion and one buyer; if you fill those two slots in the order results arrive, you will discard warmer contacts that arrived third. This is not hypothetical — a 2nd-degree Head of Global AML & Sanctions was dropped for two 3rd-degree contacts that happened to match the persona labels first, at the one account where a warm path existed.

Rank the full candidate set by `connection_degree` first, then take the top N while covering both personas if you can. Reachability is the scarce input; persona coverage is the cheap one.

**Capture the mutual connection — it is free and it is the actual intro path.** LinkedIn names a shared connection right in the search result for 2nd-degree people ("Mansi Patel is a mutual connection"). A 2nd degree without a named mutual is a statistic; with one it is a person you can ask. Store it as `mutual_connection`; `gtme-write` opens on the name, and `gtme-sequence` routes the ask through them instead of cold-DMing.

## A 404 is not a dead record (re-resolve before you delete)

**A LinkedIn slug that 404s usually means the person renamed their profile, not that the record was bad.** People shorten a surname, marry, or claim a vanity URL; the profile is untouched and the stored slug is stale. Marking those `not_found` silently deletes real, often senior contacts — in one live run, three of four 404s were live people, including a former head of fraud strategy at a top-10 US bank.

**LinkedIn preserves the trailing suffix across renames.** That is the recovery key:

```
michael-fox-0347503      → michael-f-0347503        (surname shortened)
jason-sharp-709088114    → jason-s-709088114        (surname shortened)
melanie-queiroz-a632b798 → melanie-indalecio-a632b798  (surname changed)
```

On a 404, spend **one** search on `"<name> <company>"` and match on the suffix before writing the record off. One call recovers a contact that took a full research pass to find.

Then set `record_status` from what you actually saw — the five failures are different and must not collapse into one label:

| `record_status` | Meaning | Send? |
|---|---|---|
| `unchecked` | Name resolved from a source that is not the profile; the profile was never opened | no - `verify_first` |
| `verified` | On-profile: current employer and role match the record | yes |
| `stale` | Real person, **left the company** — right human, wrong account | no |
| `wrong_person` | Slug resolves to someone else entirely (name collision) | no |
| `ambiguous` | Exists, but title/seniority unconfirmed or held concurrently | human check |
| `not_found` | Survived a suffix re-resolve and still nothing | no |

`record_status` is required on every record. The schema rejects a record without one and the send gate refuses it - an absent status used to fall through to `ready`, which made an identity nobody checked indistinguishable from one that passed. In one live run that silence covered 111 of 178 send-ready contacts.

`verified` requires evidence, not a claim: an `identity: {pulled, says}` where `says` is the
current-role line verbatim off the profile, plus `employer_history` and `education` present
(empty arrays are legal - some profiles list neither; presence means you scrolled). The schema
rejects `verified` without them. `unchecked` must NOT carry an `identity`: a pull date on a
profile nobody opened is the exact ambiguity this removes.

There is no exemption and no legacy flag. A record that cannot evidence a visit is `unchecked`,
which is not an accusation - it is the honest name for a check that has not happened yet.

Reserve `not_found` for records that survived the re-resolve. It is the only one of the six that means *the record may have been invented*, and it should be rare enough to be alarming.

Capture the same-visit byproducts while you have the profile open — one fetch, four fields: `connection_degree`, `employer_history`, `education`, and the corrected title. Employment history and schools are what `gtme-score` reads for `founder_orbit` (shared employer/school with the seller's founders), and they are **not** in the headline, so a headline-only pass returns nothing and looks like "no warm paths exist."

## Per-attempt logging (the waterfall must reorder itself)

The provider order below is a **starting hypothesis, not a constant.** Log every attempt to `runs/<slug>/enrich/attempts.jsonl`, one row per (contact × provider):

```json
{"contact_id": "...", "account_id": "domain:ramp.com", "provider": "leadmagic",
 "input_type": "linkedin_url", "result": "hit|miss|catch_all|error",
 "cost_usd": 0.006, "latency_ms": 840, "validated": true, "at": "<iso8601>"}
```

After ~2 weeks of real volume, compute hit rate, cost-per-valid-email, and (once replies exist) reply rate **per provider for this ICP**, then reorder the cascade — promote the best first-pass provider, drop any that is actively hurting. Cody's own numbers show why the order can't be frozen: *"you'll find things like leadmagic replies at 2.1%, findymail at 3.4%, pdl at 1.8%. now you know pdl is actively hurting you and you yank it from the cascade"* — and *"mine looks totally different for ecom founders vs post-series-b saas"* (same source). A waterfall frozen in the order a blog post suggested is a guess wearing a process.

`gtme-measure` reads `attempts.jsonl` alongside reply data; the reorder is proposed at the measure cycle, applied by a human edit to this skill's default order or a per-run override.

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
 "phone": null, "confidence": 0.9, "enriched_at": "<iso8601>", "sources": ["https://..."],
 "connection_degree": "2nd", "network_owner": "<whose linkedin session measured it>",
 "employer_history": ["Ramp", "Amazon"], "education": ["University of Chicago"],
 "identity": {"pulled": "2026-07-31", "says": "Head of RevOps at Ramp"},
 "record_status": "verified", "record_note": null}
```

- `email_source` — `leadmagic | findymail | prospeo | pdl | pattern_guess | none`
- `email_status` — `validated | risky | pattern_guess | undeliverable_dropped | unvalidated_no_provider`. Only `validated` sends on email.
- `connection_degree` — **never emit it without `network_owner`.** Degree is a property of the edge between the contact and whoever was logged in, not of the contact. If the operator running enrichment isn't the person who will send, that number describes a path the sender does not have. `gtme-score` demotes it to a tiebreak when the owner and the sender differ; it cannot do that if you didn't record the owner.
- `employer_history` / `education` — feed `founder_orbit`. Free to capture on a profile visit you were making anyway.
- `identity` - the proof you opened the profile: `pulled` is the date you fetched it, `says` is the current-role line copied verbatim off it. The schema holds `says` to a 20-character minimum, so a bare name cannot stand in for a role line. Required on `verified`, forbidden on `unchecked` - a pull date for a page nobody loaded is worse than no field at all. On `not_found`, `says` is `null`: nothing loaded to quote.
- `role` / `first_touch` — carried from the ICP persona; `gtme-sequence` reaches the `first_touch` contact first.
- Map ICP titles to the real org: if the exact title doesn't exist (no "VP Revenue"), pick the closest revenue-owning exec and note it in `sources`.

**`prospects.schema.json` in this folder is the contract.** The bullets above decide what's *good*; the schema decides what's *legal*. Validate before handing off:

```bash
python3 skills/validate.py runs/<slug> enrich
```

A stage that fails validation does not hand off.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Guessing an email when providers are unreachable | Hard-stop. `unvalidated_no_provider`, never send-eligible. |
| Accepting a `catch-all` result | Continue the waterfall; catch-all ≠ valid. |
| Skipping 1lookup | Validation is required; unvalidated never sends. |
| Emitting pattern-guess as `validated` | `email_source: pattern_guess` can never be `email_status: validated`. |
| Cold-calling the CEO | Phone validate/collect for the champion only. |
| Forcing a nonexistent ICP title | Pick the closest revenue-owner; document the substitution. |
| Marking a 404'd slug `not_found` | Re-resolve first — search the name and match the preserved trailing suffix. Most 404s are renames, and deleting them throws away real senior contacts. |
| One flag for every bad record | Five different failures: `unchecked` (never opened), `stale` (left), `wrong_person` (collision), `ambiguous` (unconfirmed), `not_found` (survived re-resolve). Only the last hints at fabrication. |
| `record_status` left off a record | Absent reads exactly like `verified` to anyone skimming, and the send gate used to agree. Write `unchecked`. |
| `verified` set from a search result rather than the profile | The source proves the person exists; it says nothing about the handle. One run marked a CRO `verified` at confidence 0.85 on a slug typed from his name that belonged to someone else. |
| `connection_degree` with no `network_owner` | Degree belongs to whoever was logged in. Unowned, it reads as the sender's warmth and silently mis-ranks the whole queue. |
| Reading employer history off the headline | The headline says where they work **now**. `founder_orbit` needs where they worked **before** — that's the experience section. |
| Storing the headline as the title | Headlines are self-written marketing ("Risk Strategy and Data Science Leader"). The real title is on the current-role line — in one live wave, three of the best contacts would have looked unrelated to the seller's category. |
| Boolean OR in a company-scoped search | LinkedIn drops the company token. Single keyword per search. |
| Filling the contact cap by persona order | Sort by connection degree first, then cap. Warmth is scarce; persona labels are not. |
| Dropping the mutual connection | It is printed free in 2nd-degree search results and it is the intro path. Store `mutual_connection`. |
| Trusting a headline title over the current-role line — in either direction | The headline can hide a real role *or* inflate a departed one. When the two disagree, record both and gate the contact until a human resolves it. |

## Next

`gtme-write` reads `enrich/prospects.jsonl` (validated contacts) + their account's `signals/signals.jsonl` → signal-aware message per channel.
