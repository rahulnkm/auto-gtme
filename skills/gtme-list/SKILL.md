---
name: gtme-list
description: Use after a confirmed ICP exists (icp.json), when you need to build the account universe to target — the TAM map. Triggers include "build the list", "build the TAM", "pull the accounts", or the third step of an auto-gtme run.
---

# gtme-list

## Overview

Turn a confirmed `icp.json` into the **TAM map**: a deduped, tiered, signal-ready account list persisted as `tam.jsonl`. This is the base layer everything else sits on — signals fire *onto* the map, enrichment runs *over* it, scoring ranks *within* it. Build the map before chasing any signal (see doctrine Part 1: "a signal is noise until it lands on an account you already wanted").

## When to Use

- After `gtme-icp` confirms `icp.json`, before `gtme-enrich`
- Input: `runs/<slug>/icp.json`. Output: `runs/<slug>/tam.jsonl` (machine) + `tam.md` (method + review)
- Re-run to expand the universe or after an ICP edit

## Method — over-pull, gate, tier

1. **LinkedIn is the pull spine.** It is the only source that counts people *by function* per company, so it's the only way to resolve `gtm_headcount` (or whatever `sub_team.metric` names) — the sharpest ICP filter. Use `cli/gtme-linkedin`. Crunchbase / BuiltWith / Apollo layer in `stage` and `incumbent_tech` at the **enrich** step, not here.
2. **Pull = cross-product of ICP axes**, deliberately over-pulled: `category × geo × hiring-intent`. Run as batched CLI calls. You filter down next; a thin pull is the #1 cause of a weak TAM.
3. **Preload signals during the pull.** The job-post axis pre-loads `job_posting_intent` / `li_hiring_spike` so the map arrives signal-ready, not empty.
4. **Gate then tier** (per the ICP contract): apply `disqualifiers` as a hard global filter across the whole pull first — drop failures regardless of fit — then sort survivors into tiers, matching each tier's `allocation`.
5. **Dedupe:** LinkedIn company URN → root domain fallback → cross-run on `account_id`.

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

**Live pull is the default. Seeded data is a marked fallback, never silent.**

- Attempt the live pull via the CLI first. If it can't run — **either** the tooling is broken (CLI not installed / deps missing) **or** auth isn't set up (`gtme-linkedin auth login` is a human step) — STOP and say which, don't quietly fabricate a list.
- Seeded rows have no live LinkedIn URN, so their `account_id` is always the `domain:<root>` form.
- `pass_near_ceiling` is bidirectional: flag an account within 10% of **either** a floor or a ceiling limit, so enrich re-pulls it live.
- If you must seed account values from model knowledge to demonstrate the pipeline, mark **every** such account `firmographic_source: "prior_knowledge"` with a per-account `confidence`, and flag anything near a disqualifier limit `pass_near_ceiling` so `gtme-enrich` re-pulls it live.
- **Never emit a seeded account as `firmographic_source: "live"`.** Outreach fired at a hallucinated account is the worst failure this pipeline can produce.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Thin pull (query once, take what returns) | Over-pull the cross-product; filter down. |
| Filtering to total headcount | Filter to `sub_team_est` — the pain-team count. LinkedIn function-count is why LinkedIn is the spine. |
| Seeded data emitted as live | Mark `firmographic_source` + `confidence` honestly; live-first always. |
| Empty map handed downstream | Preload job-post signals during pull so the map is signal-ready. |
| Invented row fields | Schema is fixed; `gtme-enrich` reads these exact keys. |
| Tiers ignore allocation | Split to each tier's `allocation` (0.7 / 0.3). |

## Next

`gtme-enrich` reads `tam.jsonl` → waterfall-enriches contacts → validates via 1lookup → writes `prospects.jsonl`.
