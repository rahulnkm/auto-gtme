# 14 — Signals & enrichment: what three named practitioners actually do

Primary-source investigation, 2026-07-25. Three parallel research agents, each
instructed to quote verbatim with links and to state explicitly what could not
be verified rather than filling gaps with generic outbound knowledge. This file
exists because the repo was citing one of these people for a method he did not
originate.

---

## Cody Schneider (@codyschneider — note: the old @codyschneiderxx handle 404s)

**Signals — he names exactly two, and they are narrow.**

> "the two best intent signals for cold email
> when somebody gets a new job. and when a company is hiring for a role.
> someone just started as vp of marketing 2 weeks ago? they're evaluating every
> tool in their stack. company just posted 'revenue operations analyst'? they
> have a problem they need solved before that person even starts."
> — [x.com/codyschneider/status/2028606359617388794](https://x.com/codyschneider/status/2028606359617388794), 2026-03-02

The build, notably **without Clay** (he is openly dismissive of it):

> "spin up a postgres database on railway... connect coresignal's api. pull job
> changes last 30 days, new postings last 14 days for your target titles and
> companies... run every email through millionverifier's api. only send to 'ok'
> and 'catch-all' results. push verified leads into instantly."
> — same post

His theory of personalization, which is a **volume** argument, not a research one:

> "keep them under 75 words... the intent signal IS the personalization. you
> don't need to fake relevance when the timing is already real." — same post

> "I'm just trying to touch more people... how do I get in front of as many
> people as cheaply as I can? ... I've seen these sequences where it's like 10
> emails over a four-week period. That's insane. You're only touching 2,000
> people in comparison to being able to touch 50,000."
> — [Cold Email State of The Union](https://www.youtube.com/watch?v=4kljkbbfs_8) @31:32

A third play he does name: scraping engagers of **competitors' LinkedIn ads** —
"if they engage, they are hand raising" ([status/2026311199978131832](https://x.com/codyschneider/status/2026311199978131832)).
Not implemented in this pipeline; parked as a candidate signal.

**Enrichment — the cascade he posts on X:**

> "the order matters. cheapest + highest hit rate first, most expensive last.
> 1. leadmagic 2. findymail 3. prospeo 4. wiza 5. people data labs"
> "stop on first valid result."
> "bolt verification on the end. millionverifier or zerobounce. don't trust the
> 'verified' flag from the enrichment provider itself — they all lie a little.
> one extra api call saves your sender reputation."
> "log every attempt... after 2 weeks you'll know which provider to promote to
> step 1 for your specific icp. mine looks totally different for ecom founders
> vs post-series-b saas."
> — [x.com/codyschneider/status/2043736058567786978](https://x.com/codyschneider/status/2043736058567786978)

**Attribution caveat (load-bearing).** Those posts pitch his own product
(Graphed.com), so they are vendor-adjacent. And the podcast material widely
credited to him — the waterfall, the intent plays, the warm-up/bounce/infra
detail — is **his guest Nick Abraham (Leadbird) speaking**, with Cody as
interviewer. In his own voice on the podcast he says the cheap-scraped-email
market is dying ("50,000 emails for like 200 bucks... that is evaporating"),
Apollo's UI change broke reseller scraping, and he now uses SalesQL with burner
LinkedIn accounts.

---

## Nick Abraham (Leadbird) — the actual waterfall source

> "the best thing to do when it comes to data right now is you have to do a
> waterfall... My favorite one by far right now is Lead Magic. They have the
> highest enrichment percentage that we've seen. And then I think Find[ymail]
> is a close second. And then there's a whole bunch of other ones like Prospeo."
> — [In The Pit w/ Cody Schneider](https://www.youtube.com/watch?v=4kljkbbfs_8) @08:05

Also his (not Cody's): Apollo at ~$60k/yr for ~500k credits/mo; permutation +
Hunter.io + bulk validation for 1-20 headcount companies; scraping engagers of
the last 30 LinkedIn posts and competitor page followers; hiring-intent plays;
warm-up pools and soft/hard bounce handling.

---

## Gojiberry AI (YC Spring 2026, gojiberry.ai)

**Person-first architecture.** A "Source Agent" launches 3-4×/day; each launch
uses one configured Signal, where a Signal is a **place to search**, not an
event pushed at you:

> "Think of a Signal as an instruction telling the AI where it should search
> for contacts." … "Once the Source Agent has gathered potential contacts from
> that Signal, it compares every contact against your configured ICP."
> — [help.gojiberry.ai](https://help.gojiberry.ai/en/articles/12953163-how-your-ai-agent-finds-leads-automatically)

**Published taxonomy — 6 types** (the "30+ signals" figure appears only in
competitor-authored reviews, never in Gojiberry's own material): Keyword
Engagement · People Engaging With Your Market · Companies & Competitors
Engagement · People Aware of Your Brand · Buying Events (job change ≤90d,
hiring, recent funding, top-5% most active in ICP) · Smart Lead Finder.
Sources are LinkedIn-only — no website de-anonymization, no product usage, no
review-site intent. Leads purge after 60 days.

**Enrichment is lazy and just-in-time** — fired at the email step, not at
discovery: "Waterfall Lookup: Gojiberry queries multiple premium B2B data
providers **simultaneously**" (their word — that is a parallel fan-out, not a
cost-ordered waterfall). 15+ providers, **none named anywhere**. Worth
stealing: "If the system cannot find a highly verified contact point for a
specific lead, it safely skips that step to protect your domain sender
reputation."
— [Gojiberry Enrichment System](https://help.gojiberry.ai/en/articles/15937023-gojiberry-enrichment-system)

**Why we don't copy it:** the person who trips the signal IS the person
contacted — no account model, no buying committee, no multi-threading. That
fits self-serve/low-ACV. It breaks on a six-figure sale with a compliance veto,
where the engager is rarely the signer. Doctrine recorded in the auto-gtme
skill.

---

## Alex Hormozi ($100M Leads)

**No signal concept exists in his framework.** List = scrape it, buy it, or
hand-build it. His only quality axis is *freshness in the competitive sense*:

> "If you can search the database, so can everyone else. But if you assemble a
> list of names yourself, it's less likely that person has already received
> many cold reachouts from other companies, so they're the freshest."
> — [$100M Leads audiobook pt.5, Cold Outreach](https://www.deciphr.ai/podcast/100m-leads-audiobook-part-5--cold-outreach-ep-590)

That is saturation, not readiness. List segmentation vocabulary is demographic
or affinity only — no firmographics, tech stack, headcount change, or funding.

**Volume math:** the Rule of 100 — "Don't set a daily goal below 100 and don't
stop for 100 days minimum." His scaled case: one VA sending 2,000 emails/day →
**40 engaged leads/day** (a 2% engaged rate, consistent with untriggered
outbound) → 4 customers/day at a 10% close. Channel guardrail: "the cost of
doing cold outreach is less than three times what you make in profit from a
customer."

**Warm-first prescription (stricter than commonly quoted):** do warm outreach
until roughly **10 paying customers** before scaling a cold channel. 100 warm
reach-outs/day, ~1 in 5 engage, ~1 customer per 100 reach-outs, follow up up to
3× then move on. The ten steps and the ACA framework (Acknowledge, Compliment,
Ask) are in [audiobook pt.3](https://www.deciphr.ai/podcast/100m-leads-audiobook-part-3--warm-outreach-ep-588).
This directly supports the `warm_first_plan` in offer.json.

**Correction to prior repo belief:** there is no "four things that make a good
list" framework in the book. That construct appears in derivative blogs only.

**What he does not address, ranked by how much it matters here:** no trigger or
timing layer at all; no account-vs-contact model (his unit is a flat list of
individuals — his examples are B2C or owner-is-the-committee small business);
no enrichment pipeline or data-quality operations; no prioritization or scoring;
no compliance/channel-legal layer; re-contact logic is time-based ("try again
in 3-6 months") rather than event-based.

---

## What this pipeline adopted (2026-07-25)

| Finding | Where it landed |
|---|---|
| Never trust a provider's own verified flag | `gtme-enrich` — independent-verifier rule |
| Log every attempt; reorder the cascade from evidence | `gtme-enrich` — `attempts.jsonl` schema + measure-cycle reorder |
| Waterfall citation was wrong | `gtme-enrich` — Nick Abraham as primary, Cody marked vendor-adjacent |
| Wiza at step 4 | `gtme-enrich` — added to cascade |
| 30-day job-change / 14-day posting harvest windows | `gtme-signals` — freshness windows table |
| Verify postings at the ATS, never at aggregator mirrors | `gtme-signals` — with the observed 2026-07-21 failure as evidence |
| Closed req = downgrade, not zero | `gtme-signals` — three-state posting signal |
| Account-first over person-first | `auto-gtme` — doctrine + the trade-off recorded |
| Warm-first until ~10 customers | already in `offer.json warm_first_plan` — Hormozi confirms the bar |

**Deferred:** the competitor-ad-engager signal (Cody's third play; for a fraud-tooling
seller it maps to watching who engages with the incumbents' LinkedIn content).
Highest-yield signal neither this pipeline nor Gojiberry implements.

**Rejected:** Cody's volume-over-depth trade ("touch 50,000 instead of 2,000").
Correct for a $200/mo SaaS, wrong for a six-figure in-VPC enterprise sale where
one bad first touch burns the account permanently. We are on the other side of
that trade deliberately, not accidentally.
