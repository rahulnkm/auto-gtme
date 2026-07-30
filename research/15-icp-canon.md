# 15 — ICP canon: what "ideal" means, and the half our filter was missing

Research date: 2026-07-30. Two sweeps: (a) canonical definitions from the people who defined the term; (b) operational practice — what complete industry ICPs contain beyond targeting. Quotes verified against primary text where noted; secondary-sourced claims flagged.

## The finding in one line

auto-gtme's ICP is a complete **acquisition** profile and a nonexistent **retention** profile — and the canon's entire definition of "ideal" lives in the second half. The exposure is not a missing field; it is that a feedback loop graded only on engagement optimizes toward "who replies" forever.

## The four schools of "ideal"

| School | "Ideal" = | Who | auto-gtme status (2026-07-30) |
|---|---|---|---|
| Close-likelihood | ready, willing, able to buy now | Murphy (gating half), BANT tradition | ✅ filter + signals + budget_evidence |
| Value-exchange | max mutual value: LTV, expansion, low cost-to-serve | Clay, ZoomInfo, Murphy's value inputs, Dunford (behaviorally) | 🟡 revenue-as-effort-dial covers half; cost-to-serve unmeasured |
| Staged/temporal | ECP now, ICP later | Voje, Todd Jackson/First Round | 🟡 reasoned at gate ★1; warm_first_plan is de facto ECP |
| Success/retention | most likely to succeed and stay | Roberge, Murphy's Success Potential | ❌ absent — adopted 2026-07-30, see below |

## 1. Lincoln Murphy (Sixteen Ventures, 2014) — the origin definition

[sixteenventures.com/ideal-customer-profile](https://www.sixteenventures.com/ideal-customer-profile/) · [Success Potential](https://sixteenventures.com/success-potential)

> ICP is "the customer type that – over a clearly-defined time frame – you will dedicate Sales and Marketing Resources to acquire."

Structure: three gates + four value inputs.
- **Ready** — acute problem, known to them, urgent. **Willing** — acting on it, "a strong Catalyst driving change." **Able** — money + authority + buying process matches your sales motion.
- Value inputs: **Success Potential**, **Acquisition Efficiency**, **Ascension Potential**, **Advocacy Potential** — LTV, CAC, expansion, referrals, a decade before tools vendors adopted the framing.
- Success Potential = six fits: **Technical, Functional, Resource, Competence, Experience, Cultural**. Reduces to: "is this prospect likely to achieve success in their relationship with us?"

## 2. Mark Roberge — retention IS the fit criterion

*The Science of Scaling* (Wiley 2026) — [free Stage 2 Capital PDF](https://f.hubspotusercontent10.net/hubfs/6575667/Stage%202s%20Science%20of%20Scaling.pdf), quotes verified against pp. 1–20.

> "Customer retention is the best statistical representation of product-market-fit. However, customer retention is a *lagging* indicator."

His fix — the **Leading Indicator of Retention (LIR)**:

> "[Customer Success Leading Indicator] is 'True' if P% of customers achieve E event(s) within T time"

Canonical instances: Slack — 70% of customers send 2,000 messages/month; Dropbox — 85% back up daily; HubSpot — 80% adopt 5+ of 25 features.

The claim that lands on our architecture directly:

> "Qualifying matrices like BANT and MEDDIC... do not help us understand whether the customer will *succeed* with the product and ultimately remain as a customer." … "We are solving for customer retention, not signed contracts."

> "Most customer retention issues originate in sales and marketing. Customer retention is driven by the types of customers targeted by marketing and the expectations set during the sales process."

He pairs the sales-qualifying matrix with a **Customer Success Qualifying Matrix** (content, commitment, user bought in, realistic ROI, IT bought in, tech feasible) and wires comp to LIR achievement, not contract signature. Early-stage corollary: target early adopters; "reflect on how small we can go within our target market definition where our product still creates value and start there."

## 3. April Dunford — best-fit is behavioral, found retrospectively

*Obviously Awesome* (2019), via [Goodreads quotes](https://www.goodreads.com/work/quotes/69868600) / [Nat Eliason notes](https://www.nateliason.com/notes/obviously-awesome-april-dunford).

> "Your target market is the customers who buy quickly, rarely ask for discounts and tell their friends about your offerings."

Segments must be *actionable* — mapped to identifiable characteristics — and pass two tests: big enough to meet business goals, with important specific unmet needs common to the segment. "Target as narrowly as you can to meet your near-term sales objectives."

## 4. Winning by Design — ICP from your best customers, via SPICED

[How to Uncover Your ICP](https://winningbydesign.com/resources/blueprints/how-to-uncover-your-icp/) · [SPICED](https://winningbydesign.com/resources/blueprints/the-spiced-framework/)

> "ICP development starts with identifying customers you want more of, not just more customers."

Components: firmographics + Pain + **Impact** (quantified consequence) + **Critical Event** (the why-now) + **Decision** ("group-driven and must be mapped explicitly"). Explicitly anti-firmographics-only.

## 5. Voje / ECP staging (already adopted via research/13)

[Before there is Ideal, there is Early](https://knowledge.gtmstrategist.com/p/before-there-is-ideal-there-is-early) — "You have to win early to earn the right to go upmarket toward your ICP." ECP = behavioral/JTBD/psychological, must PAY, is "a proxy of ICP," not an accident. Reverse-engineer ICP from traction ("which ones do I want 500 more of"), exclude snow leopards, revisit quarterly.

## 6. Modern operator consensus

- **Clay** ([glossary](https://www.clay.com/glossary/ideal-customer-profile)): "the type of company that would gain the most value from your product and, in turn, provide the most value to your business." Built backward from closed-won.
- **HubSpot/Gong**: ICP = company level; persona = person level. "Personas tell you who you're speaking to. ICPs tell you which companies are worth speaking to in the first place."
- **PostHog** ([newsletter](https://newsletter.posthog.com/p/defining-our-icp-is-the-most-important)): ICP as company-wide alignment artifact driving product, pricing, and channel choice — not just lead filtering. (Wrong stage for us; noted, not adopted.)
- **Schoenfeld/Keyplay** ([PeerSignal templates](https://www.peersignal.org/p/3-proven-icp-definition-templates)): the *base* fit definition is a weighted signal model, not a binary gate with scoring on top. Our recall-first rule ("when in doubt, score it") is substantively compliant; residual cliffs are the numeric bands, policed by the anti-proxy rule.

## 7. Operational-practice checklist (10 components of a complete ICP)

From templates with stated methodology ([Salesmotion rubric](https://salesmotion.io/blog/ideal-customer-profile-template), [Context.dev](https://www.context.dev/blog/ideal-customer-profile-template)) + the canon above:

1. Firmographic tiers ✅ 2. Negative ICP/disqualifiers ✅ (churn-derived variant pending first churn) 3. Weighted fit/signal score 🟡 4. Pain + urgency ✅ (market-pain) 5. Buying committee shape 🟡 (personas yes; decision process partial) 6. Budget evidence ✅ 7. **Success criteria / LIR** ❌→adopted 8. **Cost-to-serve / cycle length** ❌→measure fields adopted 9. Expansion/advocacy potential 🟡 (priced into offer warm_first_plan, correct for stage) 10. **Revision loop graded on retention** ❌→adopted.

## What auto-gtme adopted (2026-07-30)

1. **`success_criteria` slot in icp.json** (gtme-icp field spec) — LIR statement + E-event + T-window + `success_fit_flags[]` (prerequisites to *succeed*, not to buy). Optional until first customer, then required. Worked instance from a live run: escalation-action rate as the natural LIR.
2. **Metric ladder in gtme-measure** — reply → book → close → retain; each rung is the objective only until the next has data. `retention_performance[]` block; an ICP-matched account that misses the LIR counts as evidence against the filter, same weight as a hard falsifier.
3. **Acquisition-efficiency capture** — `avg_days_to_close` + `discount_pressure` per segment in measure.json (Murphy's Acquisition Efficiency; Dunford's behavioral test), replacing static guesses like `heavy_procurement`.
4. **Success-potential review lens** (9th lens at gate ★1) — "could the companies this filter admits succeed and retain?"
5. **`cloud_infra_evidence` boost** — Murphy's technical fit as scoring, never a filter.

**Deliberately not adopted:** continuous-base scoring (substantively present already); retention-derived tiers (n=0 customers — impossible; ECP staging is the stage-appropriate substitute); ICP-as-company-alignment-artifact (needs a product org; our version is artifact mutual-consistency).

## Reliability notes

Roberge quotes verified against the Stage 2 PDF directly. Murphy, WbD, Clay, Voje quotes from their public pages. Dunford via Goodreads/notes compilations (book text, high confidence). Winning by Design's full component list sits in an image-based PDF — public blueprint pages only. Salesmotion/Context.dev are vendor templates: used for the *checklist of components*, not for doctrine. Schoenfeld's weighted-base framework confirmed in shape via search excerpts of PeerSignal; exact quotes not pulled — re-verify before citing externally.
