# Why the artifacts look the way they do

The pipeline's state is a set of JSON artifacts: each stage writes one, the next stage reads it, and a human confirms the judgment artifacts at gates before anything downstream consumes them. This document explains the design decisions behind those artifacts - what earns a field a place, what got evicted and where it went, and which failure paid for each rule.

That last part matters. Almost nothing here is a style preference. Each rule exists because a specific failure happened in a real run, and the rule is what makes that failure impossible to repeat silently.

## The file model

```
company.json      who is this company?              (gtme-company)
market-pain.json  what does the buyer's day hurt    (gtme-market-pain)
                  like, in their words, evidenced?
icp.json          which accounts to target, which   (gtme-icp)
                  to exclude on purpose?
offer.json        what would a qualified prospect   (gtme-offer)
                  feel stupid saying no to?
```

Each artifact answers exactly one question. Three companion files per stage carry everything that is not the answer:

- `provenance.md` - numbered citations: verbatim quote, author, link, published date, pulled date. Artifacts reference them as `[n]`.
- `decisions.md` - our reasoning: choices with rejected alternatives, corrections, judgment calls, known weaknesses, method lessons, open decisions.
- `seller-research.json` (company stage) - interpretations and unverified readings, quarantined from the verified fingerprint.

## The admission test

A field belongs in an artifact iff it passes all three; failing any one names where it goes instead:

1. **It answers the artifact's one question.** A market claim in company.json is a fact about the world outside the company - it moves to market-pain.json. A targeting decision is strategy - it moves to icp.json.
2. **A named downstream stage reads it.** Every field holds its seat by a consumer: founders' employer history feeds warmth scoring; competitors' domains are scrape targets for stack-change signals; compliance posture decides which buyer segments are reachable. No consumer, no seat. "Profiles usually have this" is not a consumer.
3. **It matches the artifact's data model.** A fingerprint holds durable identity; a timestamped event with decay belongs in signals. A funding *event* fires as a signal; the financing *history* is identity and stays.

The eviction record shows the test working: `market_verdict` moved to market-pain (a claim about the market, not the company); `candidate_signals` and `personas` moved to the ICP (targeting decisions); `pain_keywords` moved to market-pain (buyer language is market data). One field was never admitted at all: the seller's own claimed target market. Storing the company's self-image would anchor the ICP stage toward it, and the pipeline derives WHO from pain evidence instead.

## Cross-cutting rules, and the failure that bought each

**Artifacts carry data only.** No rationale paragraphs, no revision history, no `note:` fields, no pending decisions. Explanations of each field live in the stage's skill; run history lives in decisions.md; open questions go to the human at the gate. The test: a founder skimming the artifact should see a crisp instrument, not an AI's working notes.

**Strict validation, one spec.** `company.schema.json` is the contract and a validator enforces it. Bought by: the skill once specified the artifact twice, in conflict - a field spec listing 13 fields and extraction steps writing 7 more, with one line forbidding market analysis while a later step wrote it. Nothing validated the output, so the drift was silent. `additionalProperties: false` makes drift loud.

**Every claim is cited.** Claims carry `[n]` references into provenance.md, enforced structurally where it matters most. Bought by: a widely-circulated $5.75 cost-of-fraud figure that could not be verified against its supposed source; the defensible number was $4.41-4.76. A smaller number that survives a skeptical reader beats a bigger one that does not.

**`null` means "searched, not public" - distinct from absent.** An empty rounds array plus a decisions.md note of where you looked reads differently from a field nobody filled. Without this, not-looking and not-finding are indistinguishable, and not-looking is the failure the whole pipeline guards against.

**Evidence classes travel with each claim.** `verified` (read on a primary source) / `secondhand` (a tracker lists it, nothing primary confirms it) / `founder_claimed` (their own posts, unaudited) / `unfindable`. Bought by: funding trackers auto-fill accelerator standard deals as raises and carry stale amounts forever, and a founder-claimed ranking quoted as fact in outreach is a reputation risk. The class travels with the claim so downstream can treat each differently without re-research.

**Identity checks make not-looking impossible to do silently.** Any competitor with a domain requires a `pulled` date and a verbatim line of what the served page *sells*. Bought by: a run shipped a fraud/AML competitor at a domain that actually belongs to an unrelated FX-hedging company sharing the same name. A name-match would have passed it; a verbatim served-page quote cannot. The rule does not make fabrication impossible - it makes not-looking impossible to hide.

**Numbers attach at the level their source attaches them.** A metric the source pins to one feature does not decorate the flagship claim. Bought by: an unreviewed draft that attached platform properties to the wrong product and rested a thesis on metrics the company had removed from its site.

**Confirmed vs claimed, side by side.** Team headcount stores both what was verified and what the company says, because the gap is a finding (network-only hiring, unannounced roles), not an error to reconcile away.

**Hard filters are recall-first.** In the ICP, a hard filter may only encode a provable dead end (a depository charter, fraud fully outsourced, recent acquisition). Everything softer - team size, raise recency, signal strength - is scoring, which ranks but never excludes. When in doubt, score it, don't filter it. Excluding a plausible responder is the worse failure.

**Filters name the constraint, never a proxy.** Bought by: a headcount cap that proxied "bank-style procurement" and would have excluded fast-moving large companies while admitting slow small ones. The rule: for every numeric bound, ask what is actually being excluded; if the answer is a nameable trait, filter on the trait (charter, procurement style), not the proxy (size).

**The ICP carries both halves of "ideal."** The filter is the acquisition half. A `success_criteria` slot holds the retention half: a leading indicator of retention ("P% of customers achieve E event within T time") plus per-account prerequisites to *succeed* rather than to buy. Pre-customer it is a stated hypothesis; once customers exist, an account that matched the filter but missed the indicator counts as evidence against the filter. Without this, the learning loop grades itself on who replies, and optimizes toward repliers forever. (Sources and the full argument: `research/15-icp-canon.md`.)

**Human gates, then learning.** Judgment artifacts are drafts until a human confirms them, and confirmation cascades: re-confirming the ICP invalidates the offer built on it. After sends, the measure stage emits a patch - never an in-place edit - applied at the next confirm. The artifacts are hypotheses under revision, and the revision mechanism is part of the design.

## Where to read further

- `skills/gtme-company/company.schema.json` - the contract itself; most field descriptions carry their own rationale.
- `skills/gtme-company/SKILL.md`, `skills/gtme-icp/SKILL.md`, `skills/gtme-offer/SKILL.md`, `skills/gtme-measure/SKILL.md` - per-field content rules and the review questions each artifact must pass.
- `research/13-attio-atlas-icp-doctrine.md`, `research/15-icp-canon.md` - the external doctrine the ICP design draws from, with sources.
