---
name: gtme-company
description: Use when starting a GTM run from a company website — the first step before defining an ICP, building a list, or writing outreach. Triggers include a URL handed in as the campaign starting point, "build context from this site", or `auto-gtme init --website`.
---

# gtme-company

## Overview

Turn one company website into a structured, machine-readable **company fingerprint** that every downstream skill consumes. This is the entry point of the auto-gtme pipeline.

**The frame is fixed and non-negotiable:** the input website is **the user's OWN company** (the seller). The fingerprint describes *what the seller sells and to whom* — so `gtme-icp` can define *who the seller should target*, and `gtme-write` can personalize using the seller's proof points. Never confuse a description of the seller with an ICP. This skill produces the former; `gtme-icp` produces the latter.

## When to Use

- First step of any run — a website URL is the only required input
- Before `gtme-icp`, `gtme-list`, or any outreach
- Re-run when the seller's positioning/product changes

Not for: profiling a *target* account (that's `gtme-research`).

## Two artifacts: evidence, then contract

This skill writes **two** files, in order:

1. **`seller-research.json`** — the evidence file. Multi-angle research findings with per-claim provenance. Nobody reads it wholesale; downstream skills dip in (`gtme-list` → named buyer targets, `gtme-write` → founder voice/hooks) and humans trace any context claim back to it.
2. **`company.json`** — the contract. Distilled conclusions in the fixed schema below, compiled FROM the research file. Every downstream skill reads this on every step, so it stays small and canonical.

Never write company.json from a website scrape alone. The website is one witness, and often a stale one — a single-shot scrape produces wrong team sizes, wrong competitors, and ingests aggregator hallucinations as fact (all observed in baseline runs).

## Research fan-out (do this BEFORE writing company.json)

Dispatch parallel research subagents, each owning a non-overlapping angle. Default 5; scale to 10-20 when the user asks for depth. Angle menu (pick per relevance):

| Angle | Why it beats the website |
|---|---|
| Founder LinkedIn post-mining | Freshest traction claims, hiring signals, asks, notable commenters — often months ahead of the site |
| Company LinkedIn + X presence | Real channel strategy + follower/engagement reality |
| GitHub / open-source footprint | What's actually built vs claimed; org creation dates; maintainer roles |
| Wayback site evolution | **Removed claims are high-signal** — dropped logos, softened wording, pivots |
| Hiring surfaces (all job boards) | Team trajectory; zero posts + growth = network hiring |
| Funding trackers + press sweep | Verifies or debunks the site's investor claims |
| Competitor/market map | The REAL competitor set, not name-brand guesses |
| Market trajectory | Growing vs dying vertical — hiring trends, category funding flow, incumbent behavior. Findings land in seller-research.json and `gtme-market-pain` turns them into the `market_verdict` gate; a dying market beats a great operator |
| Customer/logo verification | Aggregator "customer lists" are frequently scraped integration walls or pure hallucination — verify against primary + Wayback |
| Infra OSINT (WHOIS, DNS, MX, TXT) | Stack, age, compliance-in-progress signals (e.g. SOC2 vendor TXT records) |
| Community discourse (Reddit/HN/niche) | Whether anyone organically talks about them |
| Regulatory/compliance posture | Which buyer segments are actually reachable |
| Buyer landscape | Named accounts + titles + shopping signals, feeds `gtme-list` |

**Rules for the research file:**
- Every claim marked `verified` (read on primary source) / `secondhand` (tracker, snippet) / `founder-claimed` (their own posts, unaudited) / `unfindable` — never guess.
- Contradictions between sources are surfaced in a `contradictions` section, not silently averaged. (Stale YC page vs live LinkedIn vs CEO claim = three different headcounts; record all three.)
- Include a `founder_hooks` section (specific, verifiable personal details) and a `buyer_landscape_for_list_step` section (named targets, titles by segment, shopping signals).

## Core output — the company fingerprint

`runs/<slug>/company/company.json` answers exactly one question: **who is this company?** Founders (bio, online presence, relationships), what they sell and the urgent pain each feature kills, achievements, stage/funding/investors, warm network. Nothing else — no market analysis, no outreach guidance, no buyer personas (ICP's job), no value-prop list (redundant with per-feature pains), no hypothesis/evolution notes (working notes go in decisions.md).

### Definitions the schema depends on

- **Platform** — the substrate a company operates that products run on. A company can have multiple platforms (Amazon operates AWS and the Amazon retail marketplace — two platforms, different buyers, different fingerprints; capture each).
- **Product** — a sellable thing a buyer adopts on its own (Bedrock is a product on AWS).
- **Feature** — a capability inside a product (Knowledge Bases is a feature of Bedrock). Features never appear as products; products never appear as platforms.

### Field spec

**`company.schema.json` in this folder is the contract.** The table below explains each field — what goes in it and how it's written. The schema decides what's *legal*; this table decides what's *good*. Validate before handing off:

```bash
python3 skills/validate.py runs/<slug> company
```

A stage that fails validation does not hand off. Fix the artifact, don't relax the schema — the schema changes only when you've decided the contract should change, and that decision goes in `decisions.md`.

| Field | Content rule |
|---|---|
| `company` / `domain` / `category` / `one_liner` | identity; one_liner cites its source |
| `socials.company[]` | every platform the company has a presence on: `{platform, handle, status}` — status is active / recently_active / dormant, with one factual clause in `note` |
| `founders[]` | `name`, `role`, `bio` (career arc in 2-3 sentences, cited), `education` (institution + field), `employer_history[]` (feeds `founder_orbit`), `socials[]` (LinkedIn, X, GitHub, Substack, personal site, Medium…), `relationships[]` (named people/communities that constitute warm paths) |
| `team` | the FULL org chart as far as publicly findable: `headcount_confirmed` vs `headcount_claimed` (the gap is a finding, not an error), `members[]` (every non-founder person, same shape as founders), `unidentified[]` (roles claimed but not resolvable to a person), `hiring_style` |
| `platform[]` | the substrate + its properties, each with the pain it kills. **`null` or empty is correct for a single-product company** — never pad this to look complete |
| `products[]` | `product`, `status`, `solves`, `features[]` — each feature paired with a `pain` carrying an `urgency`. `nice_to_have` is legal but is a flag: sharpen it from evidence or cut the feature |
| ids | every platform, property, product and feature carries a stable id: `plat:` / `prop:` / `prod:` / `feat:`. **`gtme-market-pain` links each market pain to a `feat:` id** — rename one and you break the pain→feature spine silently |
| `achievements[]` | traction and outcomes proving the PRODUCT works — every entry cited |
| `credibility[]` | institutions vouching that the COMPANY is real: `marker` (batch/funding/press/award/stage), `claim`, `cites`, and a per-item `verification`. Separate from achievements because this is where puffery lives — `gtme-write` must be able to tell a measured customer result from a founder-claimed ranking |
| `stage` | phase, batch/accelerator, funding, investors (each with its own `verification`), office, compliance posture |
| `warm_universe` | investors, batch, beta users, first-degree contacts, `exhausted` flag, plus `founder_orbit: {employers, schools}` — the places a founder **actually worked or studied**, which `gtme-score` reads to score warmth |
| `competitors[]` | named entities with domain + relation — competitors ARE part of the fingerprint (who they displace defines them) |

**Not in this file, on purpose:** market claims of any kind (→ `market/market-pain.json`, including the `market_verdict` go/no-go), the thesis and founder hooks (→ `seller-research.json` — one is an interpretation, the other an unbounded pile), outreach guardrails (→ `write/guardrails.json`), buyer personas and signal selection (→ `icp/icp.json`). The schema sets `additionalProperties: false` at every level specifically so these cannot drift back in.

### Citations and provenance (applies to company AND icp)

Claims in the JSON carry numbered references (`[1]`, `[2]`…) resolving to `provenance.md` in the same folder. Each provenance entry follows this exact form:

> "<verbatim quote>", Author, Platform (<link>), published <date>, pulled <date>.

Plus an optional one-line caveat (e.g. "founder-claimed, unaudited"). No `provenance` map inside the JSON — the numbered file replaces it. "Published unknown" is allowed; the pull date then bounds the claim.

### Files per stage folder

```
runs/<slug>/company/   company.json  provenance.md  decisions.md  seller-research.json
runs/<slug>/icp/       icp.json      provenance.md  decisions.md
```

`decisions.md` per folder: dated plain-English history + open decisions (see auto-gtme cleanliness standard).

Where each removed field went, so nobody re-adds it: raw market research → `seller-research.json`; the `market_verdict` go/no-go and all market-level pain language, keywords and statistics → `market/market-pain.json`; outreach guardrails → `write/guardrails.json`; buyer personas and `candidate_signals` → `icp/icp.json` (signal selection is the ICP's job). Company-specific pains stay on features here — those describe the product, not the market.

### The company review question

When the 8-subagent artifact review runs on this folder, the eval is: **"Does this present the current state of the company as accurately as possible, excluding market and competition dynamics?"** Concretely: is the org completely mapped — every publicly findable person with bio, college and field of study, and all discoverable socials (LinkedIn, X, GitHub, Substack, personal site)? Are products/features/platforms correctly classified per the definitions? Is every claim cited and current? Missing people or stale socials fail the review.

## Extraction technique

1. **Scrape** the homepage + `/product`, `/customers`, `/pricing`, `/about` via Firecrawl (or WebFetch fallback) — then run the research fan-out above. The scrape seeds the agents' briefs; the agents' findings override the scrape wherever they conflict (the site is usually the stalest source).
2. **founders** — founders only (first hires stay in seller-research.json). Handles as bare slugs; annotate dormant channels inline (`"joe__mcallister (dormant)"`). Bio = relevant professional history in verified facts only — unverified claims stay in the evidence file — ending with a reach note, since downstream the section answers "who is the founder voice and where are they reachable."
3. **team** — enumerate everyone publicly findable, not a headcount. `headcount_confirmed` is who you actually named; `headcount_claimed` is what the company says. When they disagree, record both — the gap is the finding. Roles you can prove exist but can't attach a person to go in `unidentified[]`, which names the hole instead of hiding it.
4. **competitors** — resolve each to `{name, domain, linkedin, x, relation}`. These are scrape targets for competitor-engagement signals; a bare name is useless downstream.
5. **platform → products → features** — the argument spine, and the part most likely to be flattered. Platform holds only what's true across ALL products (deployment model, openness posture); a single-product company gets a thin platform or `null` — never force properties in (founder beliefs → `seller-research.json` founder_hooks; operator consoles are product features; both misplacements happened in baseline). Each feature carries a `pain` written the way the *buyer* ranks it, not the vendor: "institutional memory" is vendor framing; ring-discovery and regulator defensibility are what the buyer pays for. Mark it `urgent` or `nice_to_have` honestly — `nice_to_have` is legal and is the signal to sharpen or cut. Metrics attach at the level their source attaches them; a number the site pins to the tuning loop doesn't decorate the flagship claim. Evidence carries an explicit `window`, or `null` to say the source gave none.
6. **ids** — assign `plat:` / `prop:` / `prod:` / `feat:` ids as you write, from the thing's own name (`feat:end_to_end_investigation`). They are permanent: `gtme-market-pain` links each market pain to a `feat:` id, so renaming one silently unlinks a pain from the capability that kills it. Changing an id is a migration, not an edit.
7. **credibility** — institutional legitimacy, which is a different claim from product evidence: `achievements` say *the product works* (customer outcomes), `credibility` says *the company is real* (accelerator batch, funding, press, awards, conference stages). Every item carries its own `verification` — `verified` / `founder_claimed` / `unfindable` — because this is where puffery lives, and `gtme-write` quoting a founder-claimed ranking as fact is a reputation risk. Founder pedigree stays in `founders`; claims you actively contradicted (e.g. "backed by angels" with zero named angels findable) stay in `seller-research.json`.
8. **warm_universe** — everyone the seller already knows who touches the ICP: investors, accelerator batch, beta users, founders' 1st-degree network. `exhausted` stays `false` until warm outreach has been run or explicitly waived. Feeds `gtme-offer`'s warm-first gate — cold volume before the warm list is the Core Four run backwards. Its `founder_orbit` sub-object (`employers`, `schools`) is the seller's shared-history surface and is the **only** input to `gtme-score`'s `founder_orbit` points: list only employers a founder actually worked at and schools they actually attended. Investors and backers do not belong here — an angel check from a company is not a relationship with everyone who ever worked there, and treating it as one manufactures warmth that doesn't exist. Absent or empty is fine; orbit then scores zero.
9. **cite as you write, and record the negatives** — every claim carries `[n]` refs into `provenance.md`. There is no confidence map; a citation *is* the confidence statement. The failure mode this creates: a field nobody checked looks identical to one that was checked and came up empty. So when you looked and found nothing, say so — `null` on a nullable field means *searched, unfindable*, and the reason goes in `decisions.md` under known weaknesses. Silence is the one thing that must not read as fine.
10. **validate before handing off** — `python3 skills/validate.py runs/<slug> company`. It catches missing citations, bad ids, unknown fields, and duplicate ids. It cannot catch a well-formed lie, which is what the adversarial review below is for.

## Adversarial review (after drafting platform/products, before the human gate)

The platform→product→feature→need→metric→evidence chain is an *argument*, and drafted arguments flatter the seller. Dispatch 3 parallel critics against the draft + seller-research.json:

1. **Skeptical buyer** (in-persona: the ICP's economic buyer, burned by vendors) — verdict per need-claim: REAL / PARTIAL / VENDOR-LOGIC; where they'd push in a first call; what would actually convince them.
2. **Evidence auditor** — grade every metric A–D (A = independently verifiable … D = wishy-washy: vague denominator, cherry-picked window, unfalsifiable counterfactual, rhetorical plural on n≈1). Check problem_stats are scoped to the seller's actual ICP domain. Output safe phrasings for the riskiest claims.
3. **Structure critic** — thesis SUPPORTED / PLAUSIBLE-BUT-OVERREAD / UNSUPPORTED with the steelmanned cynical alternative; category-error placement check; broken links a writer would hit walking the chain left to right.

Fold verdicts back into the draft (rewrite needs to buyer ranking, relocate misattached metrics, demote overread theses to hypothesis + falsifier), archive the panel's findings in seller-research.json, THEN present at the human gate. Baseline evidence this matters: in a live client run, the un-reviewed draft misplaced 2 of 4 platform properties, mis-specified the flagship need, and rested its thesis on a misread of removed site metrics.

## Common Mistakes

| Mistake (seen in baseline) | Fix |
|---|---|
| Hedging "sell TO them vs. use as ICP model" | Input site = the SELLER. Always. Produce seller context, not an ICP. |
| Proposing a schema at the end | Emit the fixed schema above from the start; persist to `company.json`. |
| Competitors as a prose list | `competitors[]` = named entities with domain + handles. |
| Proof stats dumped in a flat list | Attach each metric to the feature/product its source attaches it to, with per-item provenance. |
| Platform level stuffed to look complete | Single-product companies get a thin platform. Founder beliefs → founder_hooks; operator consoles → product features. |
| Feature needs written in vendor logic | Write the need the way the buyer ranks it; the skeptical-buyer critic is the test. |
| Positioning rewrite read as strategy shift | Record what was removed AND what was added; removed-placeholder + added-real-metrics falsifies a "selling faith" thesis. |
| Chain shipped without adversarial review | 3-critic panel (buyer / evidence / structure), fold back, then human gate. |
| Verified and guessed fields blurred | Cite every claim. When you searched and found nothing, write `null` and log why — an absent field and an unfindable one must not look the same. |
| Market claims written into company.json | They belong in market-pain.json. The schema rejects them; that rejection is the feature. |
| `warm_universe` skipped or empty-by-default | Enumerate it — batch, investors, beta users, 1st-degree. The pipeline can't decide to skip warm if it never asked who's warm. |
| company.json written from the website alone | Website = one stale witness. Run the research fan-out; compile the fingerprint from `seller-research.json`. |
| Aggregator/AI-search "customer lists" ingested as fact | Verify against the primary site + Wayback. Scraped logo walls and hallucinated rosters are common. |
| Traction numbers averaged across conflicting sources | Record each source's number with provenance; surface the contradiction. |

## Next

`gtme-icp` reads `company.json` → defines who to target. Never skip this stage; an ICP without a seller fingerprint is vibes.
