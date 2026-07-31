---
name: gtme-market-pain
description: Use after gtme-company and before gtme-icp, when company.json exists and you need the market's pain mapped in buyers' own words — the VoC evidence layer that ICP tiers, offer construction, and copy all consume. Triggers include "map the pain", "collect VoC", "build the market-pain file", or the stage between context and ICP in an auto-gtme run.
---

# gtme-market-pain

## Overview

Turn public voice-of-customer evidence into a **machine-referenced pain map**: every pain the target market feels (or hasn't yet articulated), in buyer language, with citations, each linked to the company.json feature that kills it. Pain is a property of the *market*, not of the seller or a persona — so it's mapped **before** the ICP filters for who feels it, and before the offer promises against it. With pains mapped and evidenced, offer construction collapses into selection.

Review question: **"would a real practitioner facing this problem read each pain and say 'YES, that's exactly what's wrong' — and is every pain on the map worth solving urgently?"** Two failure modes this guards, in order of damage: (1) breadth at the cost of depth — many shallowly-understood pains are worth less than few pains modeled at the level of the practitioner's actual workflow, recent experiences, and technical vocabulary; showing you understand the problem is half the battle, and the offer then reduces to tailoring the product as solutions to their stated problems; (2) pains that are real but not high-priority AND high-urgency for the company — those get cut or demoted to content material, never carried as copy targets.

**Epistemic status: a model, not a finding.** This map is built *before* talking to customers — it is the best prior public data can produce, and it must say so. Every pain is a hypothesis. What a customer or prospect actually states in a reply, call, or thread is a higher evidence class than anything harvested here and supersedes it row by row (the `gtme-measure` pain_performance loop is the formal correction path; a single real "that's not our problem, THIS is" outranks ten forum quotes). Never present the map as definitive — to the human at the gate or in any downstream copy claim.

Output: `runs/<slug>/market/market-pain.json` (+ `provenance.md`, `decisions.md` per the artifact cleanliness standard).

## When to Use

- After `gtme-company`, before `gtme-icp`. Input: `company/company.json` (features with ids, competitors) + `seller-research.json`.
- **Public sources only** — this pipeline runs without internal access. Never cite the seller's private knowledge or invent a quote.
- Re-run when `gtme-measure` kills or confirms pain hypotheses, or quarterly (VoC goes stale).

## market-pain.json structure

```yaml
# Shown as yaml — emit as JSON. Top-level: status, harvested_at, sources_swept[].
pains:
  - id: "pain:unworked_backlog"        # stable; downstream tags against these ids
    statement: "we only work a fraction of the queue and hope the rest is noise"
    # buyer voice — one sentence a practitioner would nod at; never seller-insight prose
    shape:
      surface: "the backlog never goes to zero"            # said unprompted
      operational: "sampled-out cases are unmeasured loss" # what it costs the org
      personal: "the miss with my name on it"              # what the owner privately fears
    workflow: "where in their actual day/process this bites: the queue tool they sit in, the step that stalls, the metric that punishes them, who they escalate to"
    # step-level, named-tools depth — the practitioner test lives here; required for felt pains
    confidence: high    # high | medium | low — strength of the public evidence; customer statements override regardless
    type: felt          # felt | latent — latent = the hidden gap the seller reveals
    who_feels: [champion, economic_buyer]     # persona roles; icp tiers cite these
    segments: [crypto-exchange, fintech]
    evidence: ["[3]", "[7]", "[12]"]          # provenance.md citation ids — min 2 for felt, 1 for latent
    dream_outcome:
      champion: "every flagged case worked, queue at zero by Friday"
      economic_buyer: "tells the board loss rate is priced, not sampled"
    feature_ref: "feat:end_to_end_investigation"   # company.json feature/property id that kills it
    gap_math:
      observables: [analyst_count, alert_volume]   # per-account inputs research collects
      constants: [{name: cases_per_analyst_day, value: 30, source: "[15]"}]  # conservative, cited
tried_and_failed:      # market-level history, feeds objection pre-handling
  - approach: "rules engines + case management (Unit21/Sift era)"
    disappointment: "still manual casework; scores nobody trusts"   # in buyer words
    evidence: ["[4]"]
predicted_objections:  # ranked per persona; write pre-handles #1 in copy
  - persona: technical_evaluator
    objection: "our risk-eng team will build this in-house"
    evidence: ["[9]"]
awareness:             # per segment: problem_unaware | problem_aware | solution_aware
  crypto-exchange: solution_aware
pain_keywords: []      # DERIVED search vocabulary — publish + signal harvesting read this
market_pain_stats: []  # cited industry stats; conservative figures preferred
```

## Rules

| Rule | Why |
|---|---|
| `statement` in buyer voice | Seller-insight prose ("unmeasured loss is unpriced risk") is copy, not evidence; a buyer must be able to nod at the sentence |
| Every felt pain carries ≥2 independent citations | One quote is an anecdote; the map's credibility (and the showcase's) is clickable evidence |
| `type: latent` requires naming what reveals it | A latent pain with no revealing feature/insight is a guess, not a wedge |
| The `personal` rung is mandatory per pain | Emotional-layer copy is written against it; "N/A" requires a logged reason in decisions.md |
| `feature_ref` maps pain → feature, never feature → pain | Features with no pain mapped = feature in search of a problem (flag it); pains with no feature = content-only or disqualifying (say which) |
| `gap_math.constants` conservative + cited | The reader does the arithmetic; a dramatic number they can refute kills the whole map |
| `dream_outcome` lives HERE only | Offer selects from it; icp.json stays a clean filter; no duplication |
| Pain ids are permanent | messages.jsonl and measure.json tag against them; renaming breaks attribution |

## VoC source classes (sweep all; log each in `sources_swept`)

1. **Review sites** — G2/Capterra/TrustRadius negative+mixed reviews of the competitor set (from company.json): pain + tried_and_failed + objections in one pull.
2. **Practitioner communities** — subreddits, practitioner Slacks/forums, conference session abstracts, podcasts. Personal-rung language lives here.
3. **Job descriptions** — targets' own postings describing the queue/duties; also team-size and gap-math observables.
4. **Public problem posts** — the `li_problem_post` / `x_problem_post` signal classes, harvested retroactively as corpus.
5. **Employee reviews** — Glassdoor/Indeed by people IN the pain-team role (burnout voice).
6. **Industry reports** — cited stats for `market_pain_stats` and `gap_math.constants`.

## Validation pass (before hand-off to gtme-icp)

8 review subagents per the pipeline standard; core lenses: **practitioner simulation per persona** (role-play the economic buyer / champion / technical evaluator reading each pain: does it produce "YES, that's exactly what's wrong" — in their vocabulary, matching their actual workflow — or a polite nod?), **priority/urgency judge** (is each pain high-priority AND high-urgency for the company right now? cut or demote demoted rows), evidence-trace (every quote resolves to a live URL), seller-voice smell (statements that sound like the vendor wrote them), felt/latent audit, gap-math conservatism, downstream contract audit, competitive lens (does the map explain why incumbents leave these pains open?). Depth beats coverage: a missing pain is a smaller defect than a shallow one. Presented at ★1 **alongside** the draft ICP it justifies — one review moment, two artifacts.

## Common Mistakes

- Seller-voice statements → rewrite from a quote, or demote to `latent` with the revealing feature named.
- Pain keywords promoted to pains → keywords are derived search strings, not evidence-backed pains.
- Quoting the seller's site/founders as VoC → that's the seller's claim about the market, not the market.
- Inventing or paraphrasing quotes → provenance.md carries verbatim text + URL + dates; paraphrase only in `statement`.
- One mega-pain → split until each pain maps to exactly one feature and one dream outcome.

## Next

`gtme-icp` reads `who_feels`/`segments` to justify tiers and first_touch; `gtme-offer` builds `problems` + dream outcomes from pain ids; `gtme-write` tags every message with the `pain_id` it's built on; `gtme-measure` attributes replies to pain ids — confirming or killing specific rows here.
