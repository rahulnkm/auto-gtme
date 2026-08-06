# The GTM brain

*Doctrine. What the brain is, where it ends, and why the offer is not in it.*

## The thing

Stages `gtme-company`, `gtme-market-pain` and `gtme-icp` produce three artifacts that
answer three different questions about the same unchanging world:

| Artifact | Answers |
|---|---|
| `01-company/company.json` | who the seller is |
| `02-market/market-pain.json` | what the market hurts about, in buyers' words |
| `03-icp/icp.json` | which companies could respond positively |

Together they are the **GTM brain**: everything a stranger — a person or a model — needs
before it can say anything useful about this company's market. It is the durable half of a
run. Campaigns are built on top of it and thrown away; the brain survives them.

The working test, and the reason the name earns its place: **paste the brain into a fresh
model, ask for outreach, and see whether it writes something usable without asking a
question.** If it comes back with "who's the buyer?", you have a company overview, not a
brain. The brain is the smallest bundle that passes that test.

## Where it ends: after the ICP, before the offer

The brain is waves 01–03. `gtme-offer` is outside it. Four reasons, in the order they
should settle the argument:

**1. Lifetime.** Company, pain map and ICP are facts about the seller and the market.
They change when the world changes — a pivot, a new segment, a market that turns. The
offer changes when *we* change our minds: a re-confirmed ICP invalidates it, `gtme-measure`
returning `offer_verdict: primary_problem` invalidates it, and a new case study in
`proof_inventory` forces a re-tier. Put a per-campaign artifact inside a durable bundle and
the whole bundle expires every time the pitch moves.

**2. The two gates ask different kinds of question.** The brain's stage questions are all
checks on a description of reality: *does this present the company accurately* · *is this
the pain the market actually feels, in words a buyer would nod at* · *does this provide a
reasonable filter*. The offer's question is the Hormozi razor — *would the target be stupid
to say no?* — a judgment about a proposal we invented. A human reviewing "is this true?"
and "is this compelling?" in one sitting does the second one badly.

**3. The dependency is already one-way.** `icp.json` re-confirm invalidates `offer.json`;
nothing about the offer invalidates the ICP. The repo's own invalidation rule puts the
brain strictly upstream. Merging the two into a single gate would make a cycle out of a
DAG.

**4. Reuse is the whole payoff.** One brain, many offers. A seller who tests three offers
against the same market should re-run `gtme-offer` three times and `gtme-company` zero
times. That is only expressible if the brain is a named boundary.

The counter-argument, stated fairly: an ICP without an offer is slightly circular, because
the ICP's own review question is "could these companies respond positively *to the offer*"
— and at ★1 the offer does not exist yet. That is real, and it is handled the way the ICP
skill already handles it: the tiers are justified by `market-pain.json who_feels`, not by a
pitch. The ICP filters for the demonstrably hurting. What we sell them is the next
decision, not this one.

## ★1 is the first human review stage, and it covers all three

The brain is confirmed at one gate. Today ★1 presents `market-pain.json` and `icp.json`
together and `company.json` is never reviewed by a human at all — which is the hole this
doctrine closes. An inaccurate `company.json` corrupts the pain map, the ICP and the offer
in sequence, and every downstream stage treats it as ground truth: `gtme-offer` refuses to
invent a capability that isn't in it, `gtme-write` sources voice and proof from it,
`gtme-score` reads `warm_universe`. It is the single most load-bearing artifact in a run and
it has been the only upstream one nobody signs.

So ★1 presents all three, in dependency order, with the eight-lens review verdicts for
each. The human edits any of them. Re-confirming an upstream artifact invalidates the ones
below it exactly as re-confirming the ICP invalidates the offer.

This does not add a gate. It widens the first one and gives it a name.

## Compared to Voje's version

Maja Voje uses "GTM brain" for a context pack you hand a model — in her framing, literally
a `CLAUDE.md`
([the GTM guide to AI context engineering](https://knowledge.gtmstrategist.com/p/the-gtm-guide-to-ai-context-engineering)).
Her five sections against ours:

| Voje | Here |
|---|---|
| Company & positioning | `company.json` (with `positioning_history`, which she doesn't ask for) |
| ICP — buyers, pains, triggers | `icp.json` + `market-pain.json`, split, both cited |
| Brand voice | **missing** — see below |
| What works — campaigns that hit, angles that died | `12-measure/measure.json`, once a cycle has run |
| Tool stack | `channel-plan.json` |

Her version carries no offer either, which is weak evidence for the cut line but evidence
in the same direction. Where this pipeline is stronger: every claim in the brain traces to
a citation, and the artifacts are schema-checked so a stage fails loudly instead of handing
on a misshapen file. Where hers is stronger: it names brand voice as a first-class part of
the brain, and this pipeline does not.

## The gap: brand voice has no home

`gtme-write` needs voice and currently scavenges for it — `persona.md` if a local one
exists, otherwise `company.json one_liner` plus whatever founder material it can find in
`seller-research.json`. That is why ★3 exists in the shape it does: *voice and claims are
theirs to vouch for*, reviewed one campaign at a time, after the copy is already written.

Voice is a property of the seller, not of a campaign. It belongs in the brain, decided
once, at the gate where the human is already reading the company fingerprint. A `voice`
block on `company.json` — a few concrete rules, the observed evidence for each, and the
patterns to refuse — moves that decision upstream of every message instead of relitigating
it at ★3 on every run.

Concrete rules only. "Professional and friendly" fails the same way a prose disqualifier
fails in an ICP: it can't be checked. "Every claim carries a number or it doesn't ship" can.
