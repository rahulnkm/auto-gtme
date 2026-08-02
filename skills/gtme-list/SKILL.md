---
name: gtme-list
description: Use after a confirmed ICP exists (icp.json), when you need to build the account universe to target — the TAM map. Triggers include "build the list", "build the TAM", "pull the accounts", or the third step of an auto-gtme run.
---

# gtme-list

## Overview

Turn a confirmed `icp.json` into the **TAM map**: a deduped, tiered, signal-ready account list persisted as `tam.jsonl`. This is the base layer everything else sits on — signals fire *onto* the map, enrichment runs *over* it, scoring ranks *within* it. Build the map before chasing any signal (see doctrine Part 1: "a signal is noise until it lands on an account you already wanted").

The TAM map is an **owned dataset — persist it so you never start at zero again** (coldemailchris). `tam.jsonl` + cross-run `account_id` dedup implement this; the line names why. Practitioners (codyschneider, coldemailchris) independently corroborate the over-pull → disqualify → tier method verbatim.

## When to Use

- After `gtme-offer` confirms `offer.json` (which itself follows the ICP gate), before `gtme-enrich`
- Input: `runs/<slug>/05-icp/icp.json` + `offer.json`. Output: `runs/<slug>/07-list/tam.jsonl` (+ the standard folder companions `provenance.md` and `decisions.md` — no tam.md; method notes go in decisions.md)
- **Volume check before pulling:** `offer_tier` → expected contacts-per-lead (research/11 §3.1 table); combined with the confirmed why's `goal` via P(≥1) = 1−(1−p)^N, it sizes the pull. No confirmed why/goal → skip the check and print "no campaign goal — TAM size unvalidated" (never block, never invent a goal). Tier-4 offer implying a 5,000+-contacts-per-lead pull → surface "fix the offer before scaling volume" and point back to gate ★2.
- Re-run to expand the universe or after an ICP edit

## The TAM is the TOTAL TAM (non-negotiable)

`tam.jsonl` is the **enumerable universe of every account passing the ICP's hard filters** — not a shortlist, not the researched favorites, not "the accounts we found evidence for." For a mid-market B2B ICP that is typically **thousands of accounts**; if the map holds under ~500, treat that as a red flag, not a result. The pipeline's own volume math demands it: a tier-2 offer converts at 200–500 contacts per booked lead, so a small map cannot feed even one quarter of outreach.

Mandatory sizing discipline:
1. **Top-down estimate first**: before pulling, estimate the universe per segment × geo from category counts (directory totals, register counts, funding-database category sizes). Write the estimate and its method into decisions.md.
2. **Bottom-up enumeration**: sweep every enumerable source — LinkedIn category pulls (the spine), funding databases, industry directories, license registers (FCA EMI register, state MTL lists), curated indexes (YC directory, a16z Marketplace 100, Forbes/CB Insights lists), competitor customer rosters, conference sponsor/attendee lists.
3. **Coverage ratio, stated honestly**: the map carries `accounts_on_map / estimated_universe` in decisions.md. Below ~60% coverage the artifact is labeled a PARTIAL map in the gate message — never presented as the TAM.
4. **Layers, not truncation**: coarse directory rows (name, domain, segment, rough size band, low confidence) belong ON the map alongside deeply-researched rows — scoring and enrich refine them later. Cutting an account for lack of research is the thin-pull mistake with extra steps; recall-first applies to the universe exactly as it does to the ICP filters.

## Validation pass (before handing downstream)

**The review question every lens serves: "Would the seller recognize every account on this list as worth their time — and is any plausibly-good account missing?"** A list fails by containing accounts the seller would be embarrassed to have pulled (wrong vertical, dead end, vendor-not-buyer) or by missing accounts a human would have named in the first five minutes.

## Method — over-pull, gate, tier

1. **LinkedIn is the pull spine.** It is the only source that counts people *by function* per company, so it's the only way to resolve `gtm_headcount` (or whatever `sub_team.metric` names) — the sharpest ICP filter. Use `cli/gtme-linkedin`. Crunchbase / BuiltWith / Apollo layer in `stage` and `incumbent_tech` at the **enrich** step, not here. **Budget supplements** for the axes LinkedIn can't cover: Serper.dev ($10/mo, 100K Google queries vs Apollo's 5K lookups at $100), Firecrawl (site crawling), theorg.com (free org-chart API — reporting structure, promotions, exits), Exa + Overture Maps (universe pull), Google Maps + directories for local/SMB verticals. Supplements, never the spine — `gtm_headcount` still needs LinkedIn.
2. **Pull = cross-product of ICP axes**, deliberately over-pulled: `category × geo × hiring-intent`. Run as batched CLI calls. You filter down next; a thin pull is the #1 cause of a weak TAM. For the Apollo/Serper axes, generate query strings in three widths — broad (45–50 terms) / precision (30–35) / ultra (20–25), ≤2,000 chars, no near-synonyms.
3. **Preload signals during the pull.** The job-post axis pre-loads `job_posting_intent` / `li_hiring_spike` so the map arrives signal-ready, not empty. **Verify hiring signals at the ATS, never at aggregator mirrors** (builtin/Indeed/startup.jobs copies stay up months after a req closes — observed: signals "verified" that had been dead for 5 months). Greenhouse/Lever/Ashby expose free JSON endpoints; store the machine-checkable id (`greenhouse:goatgroup:4701901005`) so re-verification is a scripted diff. Downstream must re-verify within 48h of any send that references a posting; a recently-closed req downgrades to "they just staffed up fraud", never zero, never cited as live.
4. **Gate then tier** (per the ICP contract): apply `disqualifiers` as a hard global filter across the whole pull first — drop failures regardless of fit — then sort survivors into tiers, matching each tier's `allocation`.
5. **Dedupe:** LinkedIn company URN → root domain fallback → cross-run on `account_id`.
6. **Competitor-audience wedge (optional segment):** a competitor's LinkedIn follower/engager base, boolean-filtered to ICP titles, is a pre-qualified universe segment. Personal-profile followers only — company-page follower lists aren't publicly visible.

**Small-TAM check:** under ~1k total accounts, the motion is outbound-first by arithmetic — inbound math doesn't work at that population. Say so in `tam.md` so the pipeline weights accordingly.

## tam.jsonl row schema (fixed — gtme-enrich reads these keys)

```json
{"account_id": "urn:li:company:1234", "company": "Clay", "domain": "clay.com", "linkedin": "clay-hq",
 "tier": 1, "category": "b2b-saas", "employee_est": 180, "sub_team_est": 35, "stage": "series-b",
 "incumbent_tech": ["hubspot"], "geo": "US",
 "firmographic_source": "live", "confidence": 0.9,
 "disqualifier_check": "pass", "preloaded_signals": ["job_posting_intent"],
 "pulled_at": "<iso8601>"}
```

- `account_id` — LinkedIn URN preferred; `domain:<root>` fallback. The dedup + cross-run key.
- `sub_team_est` — the count for whatever `icp.sub_team.metric` names.
- `disqualifier_check` — `pass` | `pass_near_ceiling` (within 10% of a limit → enrich re-pulls live and may drop) | `drop` (never written to output).

## Data-provenance discipline (non-negotiable)

**Geo.** Apply `icp.json tiers[].geos`, then `geo_exception` before excluding anyone: a non-US/UK/EU HQ still qualifies on the stated contracting, language and cloud conditions. Dropping those accounts at the HQ field is a silent narrowing of the TAM.

**The warm-first gate.** Read `offer.json warm_first_plan` before pulling anything cold. While its `status` is `proposed` or `approved` and no `named_paths[].state` has reached `delivered`, cold tiers are blocked: a proof problem is not solved by volume, and the circular dependency (no logos -> weak proof -> commodity tier -> weak cold conversion -> no logos) only breaks by delivering warm. A human may waive at the ★2 gate with a logged reason.

**Seed accounts.** `icp.json seed_targets[]` are hand-picked starting accounts, each carrying its tier, the signal that qualified it, and citations. Use them to prime the TAM, and re-check each against `disqualifiers` before use — a hand-picked name can contradict the filter it was picked under. This is a different thing from *seeded* rows below, which are accounts invented from model memory; never let the two words blur.

**Live pull is the default. Seeded data is a marked fallback, never silent.**

- Attempt the live pull via the CLI first. If it can't run — **either** the tooling is broken (CLI not installed / deps missing) **or** auth isn't set up (`gtme-linkedin auth login` is a human step) — STOP and say which, don't quietly fabricate a list.
- Seeded rows have no live LinkedIn URN, so their `account_id` is always the `domain:<root>` form.
- `pass_near_ceiling` is bidirectional: flag an account within 10% of **either** a floor or a ceiling limit, so enrich re-pulls it live.
- If you must seed account values from model knowledge to demonstrate the pipeline, mark every such account honestly: `firmographic_source: "prior_knowledge"` (model memory) or `"researched"` (web-verified this run, with the evidence cited in provenance.md) plus a per-account `confidence`, and flag anything near a disqualifier limit `pass_near_ceiling` so `gtme-enrich` re-pulls it live.
- **Never emit a seeded account as `firmographic_source: "live"`.** Outreach fired at a hallucinated account is the worst failure this pipeline can produce.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Thin pull (query once, take what returns) | Over-pull the cross-product; filter down. |
| Filtering to total headcount | Filter to `sub_team_est` — the pain-team count. LinkedIn function-count is why LinkedIn is the spine. |
| Seeded data emitted as live | Mark `firmographic_source` + `confidence` honestly; live-first always. |
| Empty map handed downstream | Preload job-post signals during pull so the map is signal-ready. |
| Invented row fields | Schema is fixed; `gtme-enrich` reads these exact keys. |
| Tiers ignore allocation | Split to each tier's `allocation` per `icp.tiers[].allocation`. |

## Next

`gtme-enrich` reads `tam.jsonl` → waterfall-enriches contacts → validates via 1lookup → writes `prospects.jsonl`.
