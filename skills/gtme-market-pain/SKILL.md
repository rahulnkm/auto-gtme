---
name: gtme-market-pain
description: Use after gtme-company and before gtme-icp, when company.json exists and you need the market's pain mapped in buyers' own words — the VoC evidence layer that ICP tiers, offer construction, and copy all consume. Triggers include "map the pain", "collect VoC", "build the market-pain file", or the stage between context and ICP in an auto-gtme run.
---

# gtme-market-pain

## Overview

Turn public voice-of-customer evidence into a **machine-referenced pain map**: every pain the target market feels (or hasn't yet articulated), in buyer language, with citations, each linked to the company.json feature that kills it. Pain is a property of the *market*, not of the seller or a persona — so it's mapped **before** the ICP filters for who feels it, and before the offer promises against it. With pains mapped and evidenced, offer construction collapses into selection.

Review question: **"would a real practitioner facing this problem read each pain and say 'YES, that's exactly what's wrong' — and is every pain on the map worth solving urgently?"** Two failure modes this guards, in order of damage: (1) breadth at the cost of depth — many shallowly-understood pains are worth less than few pains modeled at the level of the practitioner's actual workflow, recent experiences, and technical vocabulary; showing you understand the problem is half the battle, and the offer then reduces to tailoring the product as solutions to their stated problems; (2) pains that are real but not high-priority AND high-urgency for the company — those get cut or demoted to content material, never carried as copy targets.

**Epistemic status: a model, not a finding.** This map is built *before* talking to customers — it is the best prior public data can produce, and it must say so. Every pain is a hypothesis. What a customer or prospect actually states in a reply, call, or thread is a higher evidence class than anything harvested here and supersedes it row by row (the `gtme-measure` pain_performance loop is the formal correction path; a single real "that's not our problem, THIS is" outranks ten forum quotes). Never present the map as definitive — to the human at the gate or in any downstream copy claim.

Output: `runs/<slug>/02-market/market-pain.json`, plus four companions — `market-research.json` (the harvest, with a `distillation` block accounting for every section), `provenance.json` (structured sources, generated from the harvest by script), `provenance.md` (rendered for humans), and `decisions.md`. See the auto-gtme evidence-handling rules; all four are checked by `validate.py`.

**Two harvesting rules this stage owns, both bought by live failures:**

- **Classify who is speaking, per source, and carry it through.** Practitioner communities in commercially-sensitive functions are astroturfed by the vendors selling into them. In one run roughly a third of the most attractive threads in the highest-yield subreddit were vendor-seeded promotions for a single product, several with vendor lists appended by edit. The harvesting pass caught them; the compile step then cited three of them anyway as buyer voice. Every source carries `authenticity`, and `validate.py` refuses a citation to a `vendor` or `astroturf` source. Apply the filter to **every** section of the harvest, not the one you happen to be reading — the failure was applying it to pain quotes and not to objections from the same file.
- **Check who owns the media before treating its silence as evidence.** A 220-transcript sweep of practitioner podcasts returned zero named-vendor complaints. The cause was structural: the main show was sponsored by a competitor and its host had joined that competitor, with earlier seasons presented by two others. Vendor-sponsored media cannot produce vendor complaints, and nothing in the feed says so.

## When to Use

- After `gtme-company`, before `gtme-icp`. Input: `01-company/company.json` (features with `feat:` ids, competitors) + `01-company/seller-research.json` (VoC raw material + the market-trajectory findings the `market_verdict` is scored from).
- **Public sources only** — this pipeline runs without internal access. Never cite the seller's private knowledge or invent a quote.
- Re-run when `gtme-measure` kills or confirms pain hypotheses, or quarterly (VoC goes stale).

## market-pain.json structure

**`market-pain.schema.json` in this folder is the contract**, enforced by `skills/validate.py runs/<slug> market`. A stage that fails validation does not hand off.

**The example below is a children's lemonade stand, on purpose.** It is not a plausible market for any real seller, so no field in it can be copied into a real artifact and still look correct. An earlier version of this example was a worked fraud/AML map carried over from a live client run — and a later run copied a whole pain out of it verbatim, including the id, and then described it as the best-attested pain in its corpus. A realistic example is a trap: the closer it sits to the domain you are working in, the more the copy survives review. Read this one for the SHAPE of each field and write every value from your own evidence.

```yaml
# Shown as yaml — emit as JSON. Top-level: status, harvested_at, sources_swept[].
pains:
  - id: "pain:runs_out_of_cups"        # stable; downstream tags against these ids
    statement: "we always run out of cups right when the after-school rush hits"
    # buyer voice — one sentence a practitioner would nod at; never seller-insight prose
    shape:
      surface: "we ran out again"                          # said unprompted
      operational: "the busiest hour is the one we cannot sell in"  # what it costs the org
      personal: "my friends watched me have to close early"  # what the owner privately fears
    workflow: "where in their actual day this bites: the cooler they scoop from, the step that stalls, the moment they notice, who they have to go and ask"
    # step-level, named-things depth — the practitioner test lives here; required for felt pains
    confidence: high    # high | medium | low — strength of the public evidence; customer statements override regardless
    type: felt          # felt | latent — latent = the hidden gap the seller reveals
    felt_evidence: "two stand-runners said it unprompted; one parent confirmed the Tuesday closure"
    who_feels: [champion, economic_buyer]     # persona roles; icp tiers cite these
    segments: [sidewalk-stand, school-fair]
    evidence: ["[3]", "[7]"]                  # provenance citation ids — min 2 for felt, 1 for latent
    dream_outcome:
      champion: "never have to shout for mum in the middle of a queue"
      economic_buyer: "one trip to the shop covers the whole summer"
    feature_ref: "feat:refill_reminder"       # company.json feature/property id that kills it
    gap_math:
      observables:
        - {name: cups_per_afternoon, findable: must_ask}
        - {name: stand_open_hours, findable: public, how: "the handwritten sign on the table"}
      constants:
        - {name: cups_per_jug, value: 12, source: "[15]", evidence_class: primary}
        # a computed value is legal and must SAY it is computed:
        - {name: jugs_per_afternoon, value: 3, source: "[15]", evidence_class: primary,
           derived: true, derived_from: "cups_per_afternoon / cups_per_jug"}
tried_and_failed:      # market-level history, feeds objection pre-handling
  - approach: "buying the big multipack once in June"
    disappointment: "they went soggy in the garage before August"   # in buyer words
    evidence: ["[4]"]
    complaints:        # named-brand gripes at verbatim grain, never a category average
      - {vendor: "BigBox multipack", verbatim: "half of them were bent by the time we opened it", cites: ["[4]"]}
predicted_objections:  # ranked per persona; write pre-handles for #1 in copy
  - id: obj1
    persona: technical_evaluator
    objection: "my big brother says he can just make a tally sheet"
    evidence: ["[9]"]
    answered_by: null
    unanswered_note: "nothing in the offer answers this; do not raise tally sheets in copy"
awareness:             # per segment, each with its own evidence
  default: {level: problem_aware, rationale: "assume they know they run out; do not explain thirst"}
  sidewalk-stand: {level: problem_aware, evidence: ["[3]"]}
pain_keywords: []      # DERIVED search vocabulary — publish + signal harvesting read this
market_pain_stats: []  # cited stats; conservative figures preferred
market_verdict:        # the starving-crowd gate — see below
  pain: 8              # 1-10, each with named evidence
  purchasing_power: 3  # pocket money is a real constraint
  targetability: 4
  growth: flat         # growing | flat | shrinking
  verdict: caution     # proceed | caution | do_not_run
  evidence: ["[2]", "[11]"]
```

### The three fields that carry evidence, not assertion

- **`awareness`** — per segment, `{level, evidence[]}` over Schwartz's five (unaware, problem_aware, solution_aware, product_aware, most_aware). This picks which copy register `gtme-write` opens in: a problem_aware buyer needs the problem named, a solution_aware one is already comparing vendors and needs difference, not education. A bare label is an uncited assertion driving a real decision, so each carries its own cites.
- **`gap_math`** — `{text, cites}`. It is the field that makes a pain *expensive*, which makes it exactly the number the buyer pushes back on. An uncited dollar figure here survives internal review and dies in front of a CRO.
- **`tried_and_failed[].complaints[]`** — `{vendor, verbatim, cites}`, optional. A category-level disappointment averages four products into one sentence and loses the specifics. Named-vendor gripes at verbatim grain are what `gtme-write` quotes for displacement and what `gtme-offer` answers in the incomparability question.

### Citation coverage

`skills/validate.py` fails the stage on any provenance entry never referenced from the artifact. Research collected and then dropped is invisible to every other check: the artifact is well-formed and every claim it makes is cited, so nothing errors — a sweep found a third of one run's citations orphaned, including the only direct proof of a claim the artifact went on to assert bare. An orphan is legal when the entry says why: append `UNUSED: <reason>` to it. The escape hatch is a decision on the record, not silence.

## The starving-crowd gate (`market_verdict`)

Market beats offer beats persuasion, so the pipeline must be able to **refuse** a market rather than only optimize inside one. Four criteria, scored from the market-trajectory research in `seller-research.json`: is the pain severe (1-10), can they pay (1-10), can you reach them (1-10), and is the category growing, flat, or shrinking.

`verdict: do_not_run` **blocks `gtme-icp`**. Only a human override at ★1, with the reason logged in `decisions.md`, proceeds. A flawless ICP inside a dying vertical is still a dead campaign, and the cost of finding that out at the reply stage is a full cycle.

This lives here, not in `company.json`, because it is a claim about the *market* — and it is evaluated at the same gate as the pain map it sits next to, where the human is already looking at market evidence.

## Rules

| Rule | Why |
|---|---|
| `statement` in buyer voice | Seller-insight prose ("unmeasured loss is unpriced risk") is copy, not evidence; a buyer must be able to nod at the sentence |
| Every felt pain carries ≥2 independent citations | One quote is an anecdote; the map's credibility (and the showcase's) is clickable evidence |
| `type: latent` requires naming what reveals it | A latent pain with no revealing feature/insight is a guess, not a wedge |
| The `personal` rung is mandatory per pain | Emotional-layer copy is written against it; "N/A" requires a logged reason in decisions.md |
**`gap_math.observables[]` say whether a stranger can actually get them.** Each is `{name, findable: public|must_ask, how}`. `constants[]` in the same field already carried a source and an evidence class while observables were bare words - and most of them only exist inside the account. Unmarked, the writer either invents the number or drops the math, and inventing a number in an email to a fraud team is the worst failure this pipeline can produce. `public` must say where it is found.

**Every `predicted_objections[]` entry carries an `id` and an `answered_by`.** Point it at the offer element that handles it (`problems:p5`, `front_end_offers:f1`). Null is a legitimate answer and means nothing addresses it: then `unanswered_note` must say so, because `gtme-write` has to know not to raise it and not to write copy that walks into it. Without this the objections were evidenced, written, and read by nothing.

**`awareness` carries a `default`.** Segments enter the ICP faster than awareness gets researched, and the two registers produce opposite emails - `problem_aware` names the problem, `solution_aware` differentiates against an incumbent. A missing level makes the writer guess. The default is the rule that covers segment nine; four of eight targeted segments once had neither an entry nor a fallback.

**`feature_ref` resolves against `company.json`** - either a `products[].features[].id` (`feat:`) or a `platform[].properties[].id` (`prop:`). Platform properties are how the product is delivered (in-VPC deploy, white-box inspectability) rather than what it does, and they carry pains of their own: a security veto is a pain even though no feature solves it. A pain with no resolvable `feature_ref` is a pain this seller cannot address, which is worth stating rather than dropping.

| `feature_ref` maps pain → feature, never feature → pain | Features with no pain mapped = feature in search of a problem (flag it); pains with no feature = content-only or disqualifying (say which) |
| `gap_math.constants` conservative + cited | The reader does the arithmetic; a dramatic number they can refute kills the whole map |
| `dream_outcome` lives HERE only | Offer selects from it; icp.json stays a clean filter; no duplication |
| Pain ids are permanent | messages.jsonl and measure.json tag against them; renaming breaks attribution |

## VoC source classes (sweep all; log each in `sources_swept`)

1. **Review sites** — G2/Capterra/TrustRadius negative+mixed reviews of the competitor set (from company.json): pain + tried_and_failed + objections in one pull.
2. **Practitioner communities** — subreddits, practitioner Slacks/forums. Personal-rung language lives here WHEN the function is one people can talk about publicly.
3. **Long-form audio and interviews — podcasts, conference talks, webinar panels, recorded AMAs. NOT optional, and not a fallback.** Sweep this in the first pass alongside review sites. Where a function is commercially sensitive, its practitioners are silent in text and voluble in audio: a guest talks unguarded for forty minutes, names volumes and tools, and describes the day in their own words, because the register is conversational rather than published. Measured on a real run: r/AMLCompliance yielded dozens of usable quotes in an afternoon while the equivalent crypto, fintech-fraud and marketplace-T&S communities yielded almost nothing — Indeed carried 375 fraud-analyst reviews at one large bank and zero at two large fintechs, and the Trust & Safety subreddit held 71 items across its entire history. The people were not absent, they were in podcasts and on conference stages. Transcribe where no transcript is published.
4. **Job descriptions** — targets' own postings describing the queue/duties; also team-size and gap-math observables.
5. **Public problem posts** — the `li_problem_post` / `x_problem_post` signal classes, harvested retroactively as corpus.
6. **Employee reviews** — Glassdoor/Indeed by people IN the pain-team role (burnout voice).
7. **Industry reports** — cited stats for `market_pain_stats` and `gap_math.constants`.

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
