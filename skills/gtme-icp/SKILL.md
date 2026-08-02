---
name: gtme-icp
description: Use after gtme-company, when a company.json exists and you need to define who the seller should target — before building a list. Triggers include "define the ICP", "who should we target", or the second step of an auto-gtme run.
---

# gtme-icp

## Overview

Turn the seller's `company.json` into a **machine-filterable ICP** plus a **human-editable review gate**. An ICP a person can only read is not done — `gtme-list` runs boolean filters, so the ICP must be structured data, not prose.

You already know how to *reason* about an ICP (tiers, intent-over-firmographics, disqualifiers). This skill's job is the **contract**: fixed schema, canonical field names, signal IDs from the taxonomy, and the review gate. Don't invent field names — downstream skills depend on these exact keys.

## When to Use

- After `gtme-market-pain`, before `gtme-list`
- Blocked when `market-pain.json market_verdict.verdict == do_not_run` — a great ICP inside a dying market is a dead campaign; only a human override at the gate (with logged reason) proceeds
- Input: `runs/<slug>/01-company/company.json` + `02-market/market-pain.json` (+ `seller-research.json` for evidence). Two company fields constrain the filter directly: `go_to_market.motion` (a `sales_led` seller with no self-serve cannot reach segments that only buy self-serve, so those tiers are dead on arrival) and `stage.compliance.regulatory_vocabulary` (a seller whose public copy is `absent` of the buyer's regulatory language is not yet reachable in the segments that gate on it: that inference belongs HERE, as a disqualifier or a demotion, never back in company.json). Output: `runs/<slug>/03-icp/icp.json` (`status: draft` → human gate → `status: confirmed`)
- **Tiers derive from the pain map:** a tier's company_types and personas' `first_touch` must be justifiable by `market-pain.json` `who_feels`/`segments` — the ICP filters for the demonstrably hurting, it doesn't guess who suits the product. Present drafts at ★1 together with the pain map. Persona psychology (dream outcomes, pain language, objections) stays in market-pain; the ICP stays a filter.
- Re-run when the seller pivots. `gtme-measure` may propose ICP drift only past the volume bar in `niche_slap_guard`; below it, measure touches offer/message/signals only — switching WHO on one cycle's noise resets all learning to zero. **Derive the bar from `offer_tier`, never a fixed constant** (tier 2 = 200–500 contacts per engaged lead ⇒ below 500, zero replies is the expected output of a *working* ICP). **Carve-out:** entries in `hard_falsifiers_bypass_bar` re-open the ICP at any volume — a filter that provably admits dead accounts, prospects stating they don't do the work in-house, a disqualifier wrong in the field, a seller pivot. Those are facts about the filter, not noise about the response rate; a guard with no falsifier is dogma

## The review gate (non-negotiable — this is the wedge over Gojiberry)

1. Generate `icp.json` directly with `status: "draft"` — data only, per the field spec below. Present the reasoning in the gate message (chat), log it in `decisions.md`; neither goes inside the artifact.
2. **STOP. Present the draft to the user** (tighten size, swap verticals, add disqualifiers — they edit the JSON or reply with corrections).
3. On `confirm`, set `status: "confirmed"` + `confirmed_by` + `confirmed_at`. Never build a list off an unconfirmed ICP.

## icp.json — the artifact is a FILTER, nothing else

icp.json exists to drive `gtme-list`: a technical filter specific enough to source the good leads, loose enough not to lose imperfect matches that could close for untrackable reasons (relationships, timing, luck). Two consequences:

1. **Hard filters are recall-first.** A hard filter may only encode a *provable dead end* (chartered bank, fraud is fully outsourced, company just got acquired, wrong vertical). Everything else — team size, raise recency, signal strength, pain evidence — is SCORING, which ranks but never excludes. When in doubt, score it, don't filter it.
2. **The artifact carries data only.** No notes, no rationale, no revision history, no methodology, no pending decisions. Explanations of each field live HERE (below); run history lives in `runs/<slug>/03-icp/decisions.md`; open decisions go to the human at the gate, not into the file. An artifact a CEO can skim without wincing.

### Field spec (emit exactly these, nothing more)

| Field | Content rule |
|---|---|
| `status` / `confirmed_by` / `confirmed_at` | gate state only |
| `objective` | one sentence, <25 words: source whom, exclude what, rank how |
| `tiers[]` | per tier: `allocation`, `company_type[]`, `employee_count{min,max}` (generous — floors/caps only where a lead is provably unserviceable), `sub_team{metric,min}` (a floor, never a cap — size caps are scoring's job), `stages[]`, `geos[]` |
| `geo_exception` | one sentence deal-mechanics test if HQ-geo alone would wrongly exclude |
| `budget_evidence_any_of[]` | 3-6 short strings; passing ANY keeps the account in |
| `disqualifiers[]` | provable dead ends only, as an ARRAY of `{id, rule, why_impossible, cites}`. `why_impossible` is required so the impossible-vs-improbable distinction has to be argued rather than assumed — improbable belongs in scoring. The earlier keyed-map shape could not be validated, had nowhere to record the reason, and hid the same bank exclusion stated twice under two names |
| `scoring` | `weight_signals_over_firmographics`, `boosts[]` (signal + weight + one-line detail), `demotions[]`, `pain_boost` (one line), `identity_max_age_days` (optional, default 30 — how old a verified prospect identity may be before `gtme-score` downgrades it from `ready` to `verify_first`; recency tolerance is a per-campaign judgment, which is why it sits here and not in the scoring formula) |
| `personas[]` | `role`, `identify_by` (see below), `cares_about` = ordered `pain:` ids from the pain map, `first_touch` on exactly one |
| `seed_targets[]` | `{name, tier, qualifying_signal, cites}` — a bare name cannot say why it was picked, so nothing can tell whether a new company resembles it or that it breaks this ICP's own filter |
| `contacts_per_account` | `{default, high_value, low_value}` |
| `seed_targets[]` | named companies already validated as fits, if any |
| `niche_slap_guard` | `min_contacts_before_icp_edit`, `min_cycles`, `derivation` (how the bar was computed from `offer_tier` — a constant with no derivation is dogma), `edits_allowed_below_bar[]`, `hard_falsifiers_bypass_bar[]`, `on_bar_cleared`, `bypass_rationale`. The volume bar below which `gtme-measure` may not touch WHO |
| `success_criteria` | `{status, lir, e_event, t_window, success_fit_flags[], graded_by}` — optional until first customer, then required. `status: pre_customer_hypothesis` until graded. See "two halves" doctrine below |

Length target: the whole file under ~100 lines. If a field needs a paragraph to justify itself, the justification goes in this skill or decisions.md — not the artifact.

### Methodology that used to live in artifact notes

- **sub_team measurement:** direct LinkedIn title-counting is infeasible at scale (no public hit counts). Stand-in: total headcount × segment prior (consumer fintech/crypto/marketplace ~2-6% of staff in fraud/risk-ops; B2B ~0.5-2%) + live fraud-posting count as existence proof.
- **Signal caveats:** a regulatory fine is a buy signal only above ~10-person fraud orgs (below that, legal freezes budget); funding windows over-capture vendors and tiny infra startups — weighting input, never a list source; social engagement (likes/follows) is noise unless paired with a timing signal.
- **List hygiene:** check for recent acquisition — acquired companies pass filters on paper but buying authority moved to the parent.

## Signal ID vocabulary (use these exact strings for watch_signals)

```
li_job_change li_promotion li_post_engaged_ours li_post_engaged_competitor li_follow_ours
li_new_hire_persona li_hiring_spike li_problem_post li_group_activity li_profile_visit
web_visit_deanon job_posting_intent tech_stack_change content_downloaded intent_provider pricing_page_visit
funding_raised product_launch press_mention new_exec_hire layoff_or_expansion cloud_infra_evidence
x_engaged_ours x_engaged_competitor x_follow_ours x_problem_post x_event_engagement
podcast_guest event_speaker github_star_category newsletter_subscribe
```
`watch_signals`/`scoring.boosts` are the subset this ICP's accounts realistically throw, chosen HERE from the taxonomy (company.json no longer carries a candidate_signals list — signal selection is the ICP's job). No invented strings.

## The four brackets (Atlas doctrine — every ICP addresses all four or states why one is empty)

Per `09-research/13-attio-atlas-icp-doctrine.md` (Voje/Copeland, atlas.attio.com):

1. **Firmographics** — table stakes, never sufficient alone ("50-250 US tech = two million companies") → the `tiers[]` fields.
2. **Behaviors** — conversion-indicative only; a pricing-page visit streak is a signal, a LinkedIn like is not → `scoring.boosts/demotions`. If the seller has no telemetry, don't fake the bracket.
3. **Timing & momentum** — event windows (funding 3-12mo post-close, fine <6mo, competitor shift, new exec 1-6mo) → `scoring.boosts` details. Timing PRIORITIZES, never filters.
4. **Revenue potential** — an effort multiplier → `contacts_per_account` bands, never a filter.

Reason about (but do NOT emit as fields): anchor accounts from real traction (exclude non-repeatable whales — "snow leopards"), ECP-vs-ICP staging and graduation criteria, review cadence. These shape the tiers and go in the gate message + decisions.md.

## The word "ideal" has two halves (canon doctrine — research/15)

The filter is the **acquisition** half of the ICP, and it stays a filter. The canon's other half is **retention**: every canonical source defines the ideal customer by what happens after the sale (Roberge: "we are solving for customer retention, not signed contracts"; Murphy's Success Potential). A loop graded only on engagement optimizes toward *who replies*, not who succeeds — Roberge's exact critique of BANT/MEDDIC.

So the artifact carries a `success_criteria` slot even when empty. Pre-customer it holds a hypothesis (an LIR: "P% of customers achieve E event within T time" — Slack: 70% send 2k msgs/mo); once any customer exists, `gtme-measure` grades ICP-matched accounts against it, and **an account that matched the filter but missed the LIR is evidence against the filter** — same weight as a hard falsifier. `success_fit_flags` name per-account prerequisites to *succeed*, not to buy (Murphy's technical/resource fit); they are scoring boosts, never filters.

## Filters name the constraint, never a proxy

The highest-damage ICP failure mode (observed in baseline): a filter that proxies the real constraint over-excludes the best buyers. Headcount caps proxy "bank-style procurement" (a 4,500-person Adyen moves faster than a 900-person community bank — cap by CHARTER/procurement style, not size). Raise-recency proxies "has budget" (it excludes profitable giants — Brex, Wise, Adyen — whose fraud spend follows fraud loss + regulatory pressure, not funding events; use a `budget_evidence.qualifies_if_any` list instead). For every numeric bound, ask: what am I actually excluding? If the answer is a nameable trait, filter on the trait.

Also mandatory:
- **Pain evidence as `scoring.pain_boost`** — one workflow-based criterion tied to the seller's actual differentiator (e.g. "pays for in-house investigation labor it wants to automate", proxied by 2+ relevant job postings in 6mo). It's a strong BOOST, not a gate — absence of visible evidence isn't absence of pain.
- **Signal maturity thresholds** — some events invert below a size threshold (a regulatory fine opens budget in a mature org and FREEZES it in a 4-person team where legal takes over). Encode the threshold inside the boost's detail line.
- **Identify the person by the job, not the title.** `identify_by` carries `function` (what they are accountable for, in plain words), `seniority` (a band), `title_examples` (real, observed), `title_keywords`, and `not_keywords`. Titles are a search guide and never a filter: enumerating them fails hardest at the companies with distinctive vocabulary, the way a search for "Software Engineer" at Anthropic misses "Member of Technical Staff". `gtme-enrich` substitutes against `function` when no listed title exists, so a persona without it leaves enrich guessing the job from the titles — which is the same failure. `not_keywords` earns its place separately: "risk" at a lending company returns credit, market, enterprise and information-security risk, none of whom hold a fraud queue.
- **`cares_about` points at pains, it does not paraphrase them.** The pain map already assigns pains to roles via `who_feels`; hand-typed phrases were a second copy that had already drifted ("analyst burnout" is a symptom, not a pain id). Order the ids by what matters most to this persona — the ordering is the only thing the prose was adding.
- **Re-check every seed against the disqualifiers before shipping.** A hand-picked name can contradict the filter it was picked under; `validate.py` fails the run if one declares a disqualifier, and a rejected seed belongs in `decisions.md`, not in the list.
- **Persona titles from observed reality** — pull real org charts/job posts for 5-6 in-segment companies; don't emit titles you can't find in the wild (baseline emitted "VP Risk"; zero instances existed across 6 real orgs).

## Validation pass (before the human gate)

**The review question every lens serves: "Does this provide a reasonable filter for which companies could respond positively to the offer?"** Not "is it precise," not "is it complete" — could the companies it admits plausibly say yes, and does it admit every company that plausibly could? A filter fails the review by excluding plausible responders (over-tight) or by admitting companies with no route to a yes (under-specified) — the first failure is worse.

Before presenting the draft, dispatch **9 review subagents** (the pipeline-wide artifact-review standard — see auto-gtme skill) with distinct lenses. For the ICP the core lenses are: lead-pull (~20 real companies passing every filter, with the qualifying signal each; rich/adequate/thin per segment), adversarial shape critique (selectivity, bad-leads-that-pass, good-leads-excluded, proxy-filter check on every numeric bound), downstream contract audit (every field downstream skills read exists, right shape), persona reality-check (titles verified against real org charts), signal abundance check, segment saturation check, buyer simulation, evidence-trace audit, and **success-potential audit** (could the companies this filter admits *succeed and retain* — does anything admitted have no route to a successful month 6? checks `success_fit_flags` coverage). Present the draft WITH the validation verdicts; the human judges both.

## Two contract rules the schema alone doesn't state

**`sub_team.metric` is an open role-department label, not an enum.** It names *whichever team feels the pain* — `engineers` for a dev tool, `gtm_headcount` for a CRM, `marketing` for an ad tool. `gtme-list` resolves it to a headcount filter (via job-title counts on LinkedIn). Pick the sharpest pain-team; don't force it into a fixed list.

**Disqualifier precedence: global gate first, then tiers.** `gtme-list` applies `disqualifiers` as a hard filter across the *entire* pulled universe first — any account failing any disqualifier is dropped regardless of tier fit. Surviving accounts sort into tiers, then scoring ranks within them.

## Common Mistakes

- Emitting a final ICP with no review gate → build starts on a wrong ICP. Always STOP at the draft.
- Prose disqualifiers ("mid-market and up") → not filterable. Encode min/max/enum.
- Inventing per-run field names → downstream can't read them. Schema is fixed.
- Collapsing `sub_team` into `employee_count` → loses the highest-value filter.

## Next

`gtme-list` reads confirmed `icp.json` → over-pulls the universe → filters to the TAM map.
