---
name: auto-gtme
description: Use to start or run the full GTM pipeline from a company website — the orchestrator entry point. Triggers include "get me started", "here's my site", "run auto-gtme", "run the whole pipeline", or `auto-gtme init --website`.
---

# auto-gtme

## Overview

The orchestrator. From one website URL, chain the 15 `gtme-*` skills into a full inbound + outbound GTM pipeline — an open-source, agent-native, self-hosted Gojiberry. Each skill reads the prior artifact and writes the next; the run directory *is* the state. Four human gates, dry-run-safe sends.

## Entry — from just a website

```
auto-gtme init --website https://linear.app
```
Derive the run slug from the domain (`linear.app` → `linear`). All artifacts live under `runs/<slug>/`. Then run `gtme-company` on the URL and proceed down the DAG.

## Run-state model

- **`runs/<slug>/` is the state.** Each stage's output artifact is its completion marker.
- **Skip-if-exists:** a stage whose output already exists is skipped unless the user asks to refresh.
- **Resumable:** stop and restart anytime; the directory says what's done.
- `run.log` records what ran when.

## The DAG (order + parallelism)

```
URL
 └ gtme-company → company/seller-research.json → company/company.json (+ provenance.md)
    └ gtme-market-pain → market/market-pain.json     (VoC pain map; reviewed at ★1 with the ICP)
       └ gtme-icp → icp/icp.json ★1 (draft → confirmed; tiers cite market-pain who_feels)
          └ gtme-offer → offer/offer.json ★2 (draft → confirmed; the campaign's WHAT — grand-slam gate; problems + dream outcomes select from market-pain pain ids)
             └ gtme-list → list/tam.jsonl              (volume plan: offer_tier × goal)
                ├ gtme-signals → signals/signals.jsonl   ┐ (parallel — no mutual dependency)
                └ gtme-enrich  → enrich/prospects.jsonl  ┘
                   └ gtme-score → score/scored.jsonl + score/scored_contacts.jsonl  (waits for signals + enrich)
                      └ gtme-research → research/research.jsonl (tier-1 human_assisted accounts only)
                         └ gtme-write → write/messages.jsonl ★3 (offer.json = the WHAT-layer menu)
                            └ gtme-sequence → sequence/send_plan.jsonl ★4 (dry-run)
                               └ [human sends] → gtme-measure → measure/measure.json ⟲ (feeds icp + score + offer + market-pain)

gtme-publish → publish/content_plan.jsonl   (parallel off company.json; reads offer.json opportunistically)
```

Run `gtme-signals` and `gtme-enrich` concurrently; `gtme-score` barriers on both. `gtme-publish` runs independently from the moment `company.json` exists.

## Artifact cleanliness standard (every stage, every artifact)

Artifacts carry **data only** — the machine fields the next stage reads plus gate state. Never inside an artifact: revision history, rationale paragraphs, methodology notes, "note:" fields, pending decisions, reviewer flags. Those live in three places instead: the stage's SKILL.md (explains each schema field: what goes in it, how it's written, length limits), that stage's own `runs/<slug>/<stage>/decisions.md`, and the gate message to the human (open decisions). **What decisions.md holds — six kinds of information, and only these:**

1. **Choices** — what was decided, what alternatives were considered and rejected, and the trade-off that settled it. A choice with no rejected alternative recorded is a fact, not a decision.
2. **Corrections** — what we believed before, what evidence changed it, what we believe now (e.g. "the $5.75 fraud-cost figure could not be verified; now using $4.41 conservative").
3. **Judgment calls on ambiguous evidence** — the reading we chose, the reading we rejected, and confidence (e.g. "the alternate product name in the demo captions: probably a transcription artifact, possibly an early name; unresolved").
4. **Known weaknesses** — what's thin, unverified, or missing in the artifact, flagged rather than hidden, each with what would firm it up.
5. **Method lessons** — what was tried in the process and failed or worked (e.g. "LinkedIn title-counting infeasible at scale"), plus whether the lesson was promoted into a skill (name it) — a lesson only in decisions.md dies with the run.
6. **Open decisions** — pending human calls, always the last section, each phrased so the human can answer without reading anything else.

The boundary: facts about the WORLD (the company's history, its positioning changes, market stats) belong in the artifact, seller-research, or provenance — decisions.md records OUR reasoning about them. When a `note:`/`evolution_note` field is stripped from an artifact, sort its content by this taxonomy: world-facts → artifact or provenance caveat; reasoning → the matching decisions.md kind. If stripped content lands nowhere, the strip was done wrong. Written for a human reader in plain full sentences — dated sections, ordinary language. No jargon, no arrow-chains, no compressed shorthand; if an entry needs the reader to already know the pipeline's internals, rewrite it. Test: a founder skimming the artifact should see a crisp instrument, not an AI's working notes. Filters in any artifact are recall-first — hard-exclude only provable dead ends; everything softer is scoring. Each stage keeps its files in its own folder (`runs/<slug>/<stage>/`) with three standard companions: the JSON artifact, `provenance.md` (numbered citations — verbatim quote, author, platform link, published date, pulled date — referenced from the JSON as [n]), and `decisions.md`.

## Artifact review standard (every stage, every artifact)

Every stage's review is governed by ONE question, defined in that stage's skill — every lens serves it. Set so far: company → "does this present the current state of the company as accurately as possible, excluding market and competition?"; market-pain → "is this the pain the market actually feels, stated in words a buyer would nod at, with evidence a stranger can click?"; icp → "does this provide a reasonable filter for which companies could respond positively to the offer?"; offer → "is this something the target would be stupid to say no to?" (the Hormozi razor). Stages without a defined question yet get one when their skill is fixed.

Before any artifact is presented at a human gate or consumed by the next stage, dispatch **8 review subagents in parallel**, each with a distinct non-overlapping lens chosen for that artifact type. Standing lenses to draw from: evidence-trace audit (every claim traces to a source artifact — no invented facts), adversarial/devil's-advocate critique, buyer/recipient simulation (would the target act on this?), operational feasibility (can the seller actually fulfill it?), competitive comparison, downstream contract audit (exact keys the next skills read), quality-bar/AI-smell check, and a domain-specific lens per artifact. Synthesize verdicts; surface contradictions between reviewers explicitly. Present the artifact WITH the review verdicts — the human judges both. Reviews never auto-approve: a clean review does not skip a human gate.

## The four human gates (hard stops — never skip)

1. **★1 After `gtme-icp`** — present draft `icp/icp.json` **together with `market/market-pain.json`** (the pain map justifies the tiers; a wrong pain map corrupts everything downstream exactly like a wrong ICP). User edits or corrects either artifact → set confirmed → continue. Re-confirming market-pain after edits invalidates icp.json the same way icp invalidates offer.
2. **★2 After `gtme-offer`** — user reviews draft `offer.json` against the 10-question grand-slam gate (offer integrity, guarantee ops can cash, honest scarcity, tier). A wrong offer wastes every row the same way a wrong ICP does. **Re-confirming icp.json invalidates offer.json — re-open ★2.**
3. **★3 After `gtme-write`** — user reviews a sample of `messages.jsonl`. Voice and claims are theirs to vouch for.
4. **★4 Before `gtme-sequence` sends** — dry-run gated by design. Nothing leaves the building until the user runs the gated command. Standing pre-approval does not satisfy this (see `gtme-sequence`).

Between gates, run unattended.

## Account-first, deliberately (the road not taken)

*(Comparative evidence: `research/14-practitioner-signals-enrichment.md`.)*

This pipeline resolves an **account** first, then finds the **buying committee** inside it — champion (first touch) plus economic buyer, sometimes a technical evaluator. The main alternative in the market is **person-first**: crawl a social graph for individuals showing engagement, check each against the ICP, contact whoever tripped the trigger. Gojiberry AI (YC S26) is the clearest implementation — its Source Agent runs 3–4×/day over LinkedIn, each run using one configured "signal" (a *search surface*, not a pushed event), and the person found IS the person contacted ([help.gojiberry.ai](https://help.gojiberry.ai/en/articles/12953163-how-your-ai-agent-finds-leads-automatically)). No account model, no committee, no multi-threading.

**We do not adopt it, on purpose.** Person-first fits self-serve and low-ACV motions where the engager can buy alone. It breaks where this pipeline operates: a five- or six-figure deal with a *veto holder who never engages publicly*. The person who likes a LinkedIn post about fraud tooling is rarely the CCO whose sign-off the deal actually needs — and a compliance or security veto kills a deal no matter how warm the champion is. Account-first is what lets `gtme-enrich` resolve both layers and `gtme-sequence` multi-thread them.

The honest trade: person-first gets a warmer first touch (they just engaged with something) and needs far less research per lead. Account-first costs more per account and must manufacture its own why-now from signals. Revisit this only if the seller's ACV drops far enough that a single non-executive buyer can sign.

## Blocked-state handling

Stages hard-stop by design when inputs are missing — this is correct, not a crash:
- `gtme-offer` with a thin `company.json` (no capabilities/proof) → `blocked_thin_company`; `gtme-write` with no confirmed `offer.json` → `blocked_no_offer`.
- `gtme-list` with no LinkedIn access → seeded/`blocked`, surfaces "connect + authenticate the LinkedIn MCP".
- `gtme-enrich` with no provider keys → `enrich/status.json` `blocked_no_provider`, empty `enrich/prospects.jsonl`.
- `gtme-sequence` with an unwired channel → `blocked`.

The orchestrator **surfaces the blocked stage and what unblocks it, then pauses that branch** — it does not fabricate data to proceed, and it lets independent branches (e.g. `gtme-publish`) continue. Report blocked states to the user with the exact remediation; resume when they unblock.

## The compounding loop

Real replies → `gtme-measure` → `measure.json` patch → applied on the next `gtme-icp` confirm + read as `signal_priors` by `gtme-score` + `offer_verdict` (a `primary_problem` verdict re-opens ★2). Batch two targets tighter than batch one. Inbound (`gtme-publish` engagement) and outbound feed the same score/write/sequence spine.

**The ICP is an acquisition profile AND a retention profile.** The loop grades on engagement only until the first customer exists; from then on retention (the `success_criteria` LIR in icp.json, graded by measure's `retention_performance`) outranks book-rate as the ICP's report card (research/15).

## Common Mistakes

| Mistake | Fix |
|---|---|
| Skipping a human gate | Four gates are hard stops (icp, offer, messages, send). |
| Keeping a stale offer after an ICP edit | icp.json re-confirm invalidates offer.json; re-run ★2. |
| Fabricating data past a blocked stage | Surface the block + remediation; pause that branch. |
| Re-running completed stages | Skip-if-exists; the artifact is the marker. |
| Running signals→enrich serially | They're parallel; score barriers on both. |
| Treating publish as sequential | It runs off company.json in parallel. |
| Auto-sending | Send is always the human ★4 gate. |

## Related

Each stage is its own skill (`gtme-company` … `gtme-measure`, `gtme-publish`). Gating/handoff cross-cut via `gtme-why` and `gtme-handoff`. Signal/channel doctrine: `docs/build/signals-channels-doctrine.md`.
