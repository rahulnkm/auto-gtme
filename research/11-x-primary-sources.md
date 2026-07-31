# Section 11: X/Twitter Primary Sources — Operator Threads & Training Docs

**Deep-Research Dossier — Section 11**
*Compiled 2026-07-09. Closes the [Appendix C](00-DOSSIER.md#appendix-c--bird-cli--primary-source-gap) primary-source gap: `bird` CLI authed July 2026; all threads pulled in full including replies. Every claim links to its tweet or archived doc. Reply-thread dissent is preserved — it is part of the data. **CONFIRMS** items point at the dossier section they corroborate; the four **CONFLICTS** are resolved in §8.*

---

## Table of Contents

1. [Method & source inventory](#1-method--source-inventory)
2. [Copywriting from specimens](#2-copywriting-from-specimens)
3. [The coldemailchris training corpus](#3-the-coldemailchris-training-corpus)
4. [Infrastructure & deliverability numbers](#4-infrastructure--deliverability-numbers)
5. [List building on a budget](#5-list-building-on-a-budget)
6. [GTM playbooks by company stage](#6-gtm-playbooks-by-company-stage)
7. [The Attio GTM Atlas](#7-the-attio-gtm-atlas)
8. [GTME systems in production](#8-gtme-systems-in-production)
9. [Conflicts — with the corpus and between sources](#9-conflicts--with-the-corpus-and-between-sources)
10. [Skill-impact map](#10-skill-impact-map)
11. [Open loops](#11-open-loops)
12. [Sources](#sources)

---

## 1. Method & Source Inventory

Threads fetched via `bird thread` (author tweets + full replies), 2026-07-09. One web resource (GTM Atlas) discovered via an X bookmark and read directly. One DM-gated training-doc set (@coldemailchris, 7 Google Docs) unlocked and archived locally at `sources/coldemailchris/` (gitignored — the author's verbatim docs aren't redistributed; the originals are link-rot-prone Docs exports). Classification: **SUBSTANTIVE** (actionable content in the source itself) / **PARTIAL** (real signal, incomplete) / **GATED** (lead magnet, content unreachable).

| # | Author | Date | Class | One-line content | Link |
|---|---|---|---|---|---|
| 1 | @chrispisarski | 2026-05-06 | SUBSTANTIVE | Anti-case-study tactic for stalled prospects, template verbatim | [tweet](https://x.com/chrispisarski/status/2052087576090051064) |
| 2 | @Scav | 2023-03 | SUBSTANTIVE | 5 VC email-pipeline conventions (forwardable blurbs, double opt-in) | [tweet](https://x.com/Scav/status/1639427928873381888) |
| 3 | @StephNass | 2024-04 | SUBSTANTIVE | 6 reasons never to NDA-gate cold investor email | [tweet](https://x.com/StephNass/status/1782229419245085039) |
| 4 | @NickAbraham12 | 2026-06-30 | SUBSTANTIVE | Praised cold-email specimen (screenshot, annotated) | [tweet](https://x.com/NickAbraham12/status/2071957485003395581) |
| 5 | @levelsio | 2023-09 | SUBSTANTIVE | Anti-specimen: mocked cold DM, failure modes | [tweet](https://x.com/levelsio/status/1708159557430653144) |
| 6 | @coldemailchris | 2026-07-07 | GATED→**unlocked** | 9-training copywriting masterclass; 7 docs obtained, archived locally (not committed) | [tweet](https://x.com/coldemailchris/status/2074619017994653712) |
| 7 | @coldemailchris | 2026-06-16 | GATED (video) | Free 2-hr A-Z cold email course, native X video, untranscribed | [tweet](https://x.com/coldemailchris/status/2066926457608356305) |
| 8 | @dimitarangg | 2026-07-04 | GATED (numbers extractable) | Warm-up + deliverability masterclass; TOC + numbers in-thread | [tweet](https://x.com/dimitarangg/status/2073424014664401201) |
| 9 | @fin465 | 2026-05-20 | SUBSTANTIVE | $102/mo outbound stack with prices | [tweet](https://x.com/fin465/status/2057478167426965936) |
| 10 | @coldemailchris | 2026-06-29 | SUBSTANTIVE | TAM-as-owned-dataset workflow (Supabase) | [tweet](https://x.com/coldemailchris/status/2071734259258216484) |
| 11 | @codyschneider | 2026-06-24 | SUBSTANTIVE | TAM mapping playbook, 5-step build | [tweet](https://x.com/codyschneider/status/2069767512888143889) |
| 12 | @kai_cabero | 2026-05-13 | PARTIAL | Competitor-LinkedIn-follower extraction play | [tweet](https://x.com/kai_cabero/status/2054924814150951054) |
| 13 | @MitchellKeller_ | 2026-07-02 | PARTIAL (thin) | Serverless scraping of public JSON endpoints | [tweet](https://x.com/MitchellKeller_/status/2072699095387447522) |
| 14 | @fin465 | 2026-05-15 | SUBSTANTIVE | YC $1M+ ARR LinkedIn outbound playbook | [tweet](https://x.com/fin465/status/2055137077868814804) |
| 15 | @fin465 | 2026-05-23 | SUBSTANTIVE | Conference-only GTM, $0→$2M ARR/6mo | [tweet](https://x.com/fin465/status/2058300451880354071) |
| 16 | @CDTEliot (Sam Blond) | 2026-06-13 | SUBSTANTIVE | Monaco stealth→big-bang launch playbook | [tweet](https://x.com/CDTEliot/status/2065824263916097723) |
| 17 | @LoganTGott | 2026-05-16 | PARTIAL | Clay $0→$30M distribution moves | [tweet](https://x.com/LoganTGott/status/2055778612364579005) |
| 18 | @attio | 2026-05-13 | SUBSTANTIVE (external) | GTM Atlas, 15 chapters, free — tweet deleted, resource live | [atlas.attio.com](https://atlas.attio.com/) |
| 19 | @samdblond | 2023-05-01 | SUBSTANTIVE | Brex billboard campaign case study | [tweet](https://x.com/samdblond/status/1653150044265099265) |
| 20 | @frantzfries | 2023-06-28 | PARTIAL | YC batch winners went sales-first over PLG | [tweet](https://x.com/frantzfries/status/1674031281414258694) |
| 21 | @mattceras | 2026-05-21 | PARTIAL | 70–80% of businesses are referral-only | [tweet](https://x.com/mattceras/status/2057600478859387072) |
| 22 | @codyschneider | 2025-07-31 | PARTIAL | Vibe-marketing volume quotas | [tweet](https://x.com/codyschneider/status/1950949576224985108) |
| 23 | @fin465 | 2026-06-04 | PARTIAL | 8-step GTM Engineer role + Vercel claim | [tweet](https://x.com/fin465/status/2060430268176232709) |
| 24 | @paolo_scales | 2026-07-07 | GATED | $2.5M AI LinkedIn GTM system — DM "GTM" required | [tweet](https://x.com/paolo_scales/status/2074487930832167159) |
| 25 | @chrispisarski | 2026-07-01 | SUBSTANTIVE | Crustdata sales-team Claude skill library | [tweet](https://x.com/chrispisarski/status/2072400619756028210) |
| 26 | @jasonlk | 2026-05-22 | SUBSTANTIVE (recovered) | Anthropic sales-rep ramp system (Eleanor Dorfman, SaaStr AI) | [1](https://x.com/jasonlk/status/2057197923146862621) · [2](https://x.com/jasonlk/status/2060064561508814946) · [3](https://x.com/jasonlk/status/2064634927421767938) |
| 27 | @coreyhainesco | 2026-05-15 | SUBSTANTIVE | marketingskills v2.0 open-source repo, ~50 skills | [tweet](https://x.com/coreyhainesco/status/2055011827600572668) |
| 28 | @mjwoo94 | 2026-05-19 | PARTIAL | AI-GTM follow list | [tweet](https://x.com/mjwoo94/status/2056423069032333510) |
| 29 | @codyschneider | 2026-07-03 | SUBSTANTIVE | Best B2B lead magnet = free AI training (demo-in-disguise) | [tweet](https://x.com/codyschneider/status/2073104495949533667) |

Delta tally vs. the corpus: **19 NEW items, 12 CONFIRMS, 4 CONFLICTS** (§9).

---

## 2. Copywriting from Specimens

### 2.1 The praised specimen — [@NickAbraham12](https://x.com/NickAbraham12/status/2071957485003395581)

Offshore-recruiting pitch Nick Abraham (dossier [Part 2 #9](00-DOSSIER.md#part-2--the-10-frontier-operators)) called "absolutely incredible." Full text, subject `think we should talk`:

> Hey Nick, / Two quick things: / 1. We're able to place a carefully vetted Apollo & LinkedIn Outbound SDR or a Klaviyo & Mailchimp Email Specialist for USD 6–10/hr, working your hours, available within about two weeks. / 2. You don't pay until you've interviewed and hired someone you like. / May I send over some candidate video intros so you can judge the talent level for yourself? / — Head of Partnerships / PS: We are giving you a USD 25 Amazon card just for showing up on the meeting and hearing us out.

| Element | Mechanism | Corpus status |
|---|---|---|
| `think we should talk` subject | Lowercase internal-mimic — reads as colleague, not campaign | **CONFIRMS** [`04` §4.3](04-psychology-nepq-persuasion.md) |
| "Two quick things" | Pre-commits to brevity; scannable numbered list | **CONFIRMS** `04` structural doctrine |
| Exact roles/tools/price/timeline | Specificity IS the personalization (tools matched to recipient's business) | **CONFIRMS** `04` §4.4 |
| "You don't pay until you've hired" | **Risk reversal** — shifts risk to sender | **NEW** — absent from `04`'s skeleton, DO list, CTA hierarchy |
| "May I send candidate videos?" | Permission CTA at touch 1 — prospect judges proof directly | **CONFIRMS** `04` §4.8 (corpus files it at touch 2; specimen runs it at touch 1) |
| $25 Amazon card PS | Paid show-up incentive — pays for the exact behavior wanted | **NEW** — see conflict C4 (§9) |

Reply dissent kept: [@namiquxst] the gift card reads cheap to wealthy targets; [@3povC] the "vetted candidate" may not exist — the copy tactic can outrun operational truth (offer-integrity risk if copied without the inventory).

### 2.2 The anti-specimen — [@levelsio](https://x.com/levelsio/status/1708159557430653144)

Cold DM posted verbatim to be mocked ("Sup Pieter... make you rich in this attention economy..."). Failure modes, three of which are **NEW** (not in [`04` §5.3](04-psychology-nepq-persuasion.md)'s 30-item DON'T list):

| Failure mode | Status |
|---|---|
| Forced casualness to a stranger ("Sup Pieter") | CONFIRMS `04` DON'T list |
| Hype-clause stacking, zero falsifiable specifics | CONFIRMS `04` DON'T list |
| Fake scarcity ("3 business owners" — a replier got the identical email days earlier) | CONFIRMS `04` §3.6 |
| **"I'll keep it short" then isn't** — claimed brevity draws attention to its absence | **NEW** |
| **Negative offer definition** ("it's not lead gen, cold email, or even Facebook ads") — wastes the hook naming what it isn't | **NEW** |
| **Irrelevant name-drops** — logos the recipient doesn't recognize are worse than none; they reveal the blast | **NEW** |

### 2.3 The anti-case study — [@chrispisarski](https://x.com/chrispisarski/status/2052087576090051064) — NEW

Prospects are numb to happy-customer case studies. For a **stalled** prospect, send a post-mortem of a company that made the exact mistake they're about to make. Template verbatim:

> "hey david, knowing you guys are weighing doing this manually vs using our platform, i wanted to send over this post-mortem from a company that tried to scale this manually last year — they ran into a massive data issue in month 4 that broke their CRM. happy to walk you through exactly how to avoid it, even if you don't end up using us"

Structure: names the prospect's actual decision fork; concrete failure detail ("month 4", "broke their CRM") carries the credibility; detached close removes pressure and repositions seller as advisor. Psychology: loss aversion beats gain framing for the stalled — instantiates `04` §2.1 (~2× for real losses) as a tactic the corpus lacked. Sourcing (reply thread): mine onboarding calls of customers who tried the DIY path first. Directly instantiates gtme-write rule 7 ("follow-ups add a new argument").

### 2.4 Intro-pipeline conventions — [@Scav](https://x.com/Scav/status/1639427928873381888) — NEW

Five conventions for referral/intro channels (no intro-channel craft existed anywhere in the corpus): **(1) forwardable blurbs** — write the self-contained paragraph your champion pastes upward (extends [`04` §4.7](04-psychology-nepq-persuasion.md)'s one-sentence-forwardable test to the whole email); **(2) double opt-in intros** — the blurb must sell the *target*, not the introducer; **(3) clear ask** = amount + milestone + timeline, three numbers not vibes; **(4) customize the "why this funder"** explicitly; **(5) bcc-move etiquette** after an intro lands — channel conventions are sophistication signals.

### 2.5 No pre-engagement demands — [@StephNass](https://x.com/StephNass/status/1782229419245085039) — NEW

Six reasons never to NDA-gate a cold investor email (power dynamics, friction kills conversion, wrong stage, unenforceable, untenable at investor scale, outsider-signaling). Generalized: **any demand placed on a cold recipient before they've engaged is friction plus a negative sophistication signal** — confirms `04` §4.8 low-friction doctrine, extends it to channel etiquette. Reply carve-out: deep-tech/R&D may differ; holds for SaaS/services.

### 2.6 Ten cross-source copy principles

1. **Specificity is the new personalization** [2.1, 2.4; anti: 2.2]
2. **Reverse the risk, don't claim the upside** [2.1, 2.3]
3. **Zero pre-engagement friction or demands** [2.5, 2.1, anti: 2.2]
4. **Loss aversion beats gain framing for the stalled** [2.3]
5. **Write the email your reader forwards** [2.4]
6. **Cut the throat-clearing** [2.1, anti: 2.2]
7. **Advisor posture over seller posture** [2.3, 2.1]
8. **Sweeten the specific next step, not the relationship** [2.1 — with C4 caveat]
9. **Social proof only counts if it's proof to THIS reader** [2.1, anti: 2.2]
10. **Know the etiquette of the channel** [2.4, 2.5]

---

## 3. The coldemailchris Training Corpus

Provenance: DM-gated lead magnet ([announcement tweet](https://x.com/coldemailchris/status/2074619017994653712), 5M+ emails claimed), unlocked 2026-07. Seven docs archived locally at `sources/coldemailchris/` (gitignored, not redistributed — Google Docs exports rot, the local copies don't). The TOC promised 9 trainings; 2 are unaccounted (§11).

### 3.1 Offer tiers (doc 1, local archive) — NEW

Expected conversion is conditioned on **offer quality**, not just copy — a prior the corpus's rate-based benchmarks (`04` §4.1) don't have:

| Tier | Offer class | Contacts per lead |
|---|---|---|
| 1 | Incredible (unique + extremely valuable) | 25–200 |
| 2 | Good (TikTok Shop, influencer mktg, PMF SaaS) | 200–500 |
| 3 | Decent (email mktg, ad creative, cold email) | 500–1,000 |
| 4 | Bad/commodity (SEO, cybersecurity, recruiting) | 1,000–10,000 |

Use: goal-backwards volume planning; deciding whether a bad cycle is copy, targeting, or **offer** (feeds gtme-measure).

### 3.2 Messaging principles (doc 1, local archive)

Ten principles; highlights: sub-75-word scripts (→ conflict C1, §9); strong front-end offer for cold traffic; industry-segment × persona tailoring; casual tone; adjacent social proof; persona-level pain; pattern disrupts in preview text; zero filler.

### 3.3 Psychology — the 5-questions gate (doc 2, local archive) — NEW

Pattern disrupt as the core mechanism ("recognizing an unwanted pattern, disrupting it, leading to the desired behavior") — CONFIRMS `04` §4.6 pattern interrupts. NEW: the auditable per-email gate. Prospects care about exactly 5 things, all answered in <50 words:

1. How will you make me money?
2. Have you successfully helped others just like me?
3. Did you research our company?
4. Are you a real person?
5. Is this a waste of my time?

The corpus has a 40-item DO list (`04` §5) but no compact every-email-must-answer test. This is it.

### 3.4 Six script frameworks (doc 3, local archive) — NEW

Fill-in-the-slot frameworks — they operationalize Will Allred's "frameworks not templates" doctrine (dossier [Part 2 #4](00-DOSSIER.md#part-2--the-10-frontier-operators)), which the corpus states but never ships:

1. **Lead-magnet result frame** — "created a {Lead Magnet} covering the {Mechanism} that got {Client} {Result} in {Timeframe} — {CTA}?"
2. **One-liner + P.S.** — "interested in {Free Work/Frontend Offer} for {company}?" + P.S. social proof. *The full email* — shorter than anything the corpus endorses.
3. **Dream result + risk reversal** — "{Mechanism} guarantees {Dream Result} in {Timeframe} or {Risk Reversal}"
4. **Pain-question PAS** — question → solution → interest CTA + P.S. proof
5. **Touchpoint → pain → solution** — three lines
6. **Unique market insight** — question → insight (AI market research) → implementation CTA

### 3.5 The 10-point send checklist (doc 4, local archive) — NEW

<65 words? · validated offer? · industry-relevant wording? · unique angle? · **every sentence spintaxed?** · wording matched to list targeting? · easy to read? · pattern disrupt? · zero filler? · personalization meaningful?

Spintax-per-sentence (unique text per send so filters can't fingerprint the campaign) is entirely absent from the corpus — a deliverability/dedup practice, optional for `fully_auto` volume sends only.

### 3.6 Personalized relevance (doc 5, local archive) — CONFIRMS + NEW

CONFIRMS [`04` §4.4](04-psychology-nepq-persuasion.md) almost verbatim: industry callouts aren't relevance; AI first-lines about "their local sports team" aren't personalization (corpus: personalization without relevance "feels like stalking"). NEW: the deployable 5-line framework the corpus never shipped — `{pain question?} → {personalized solution} → {social proof} → {implementation CTA}` — with a worked example (Eclipse Labs / blockchain proxies / Apify-Apollo-RocketReach proof / 14-day-trial CTA).

### 3.7 The 6-prompt GTM chain (doc 6, local archive) — CONFIRMS + NEW

The chain (deep market research → TAM mapping → ICP modeling → account sourcing → keyword generation → messaging creation) CONFIRMS the canonical pipeline [`01` §3](01-discipline-and-pipeline.md) and dossier [Part 3 Steps 0–7](00-DOSSIER.md#part-3--company-strategy--gtm-engineering-the-operating-playbook). NEW concrete artifacts:

- **NAICS codes per segment** for data sourcing
- **Pain-Qualified Segments (PQS)** — personas grouped by shared pain into campaign segments with trigger/impact/urgency/message-angle fields (deepens gtme-icp's persona model)
- **Keyword targeting strings** in 3 widths — broad 45–50 terms / precision 30–35 / ultra 20–25, ≤2,000 chars, Apollo/Clay-compatible, no near-synonyms
- **Messaging output contract:** subject lines 1–3 words, no punctuation, spintext `{A|B|C}`; length×complexity matrix (30/45/60 words × simple/niche-aware/hyper-specific); word budgets per element — hook 8–12w, social-proof bridge 15–20w, value prop 10–15w, front-end offer 8–12w, soft CTA 5–8w (question-based, never a hard call ask); 25–69 words per script, strict
- **Front-end offer starters:** "[Audit] 5-point deliverability audit (24 hrs)" · "[Playbook] 2-page outreach sequence, ready to paste" · "[Teardown] Loom review with prioritized fixes" · "[Benchmark] peer comparison, 3 charts"

### 3.8 The interested-but-stalled nurture sequence (doc 7, local archive) — NEW

10 emails for prospects who replied *interested* but stalled: 3–5-day gaps, ≤75 words each, phased — 1–3 nurture with value, 4–6 objections + social proof, 7–8 gentle urgency + results, 9–10 final value + soft close. The corpus covers only the *no-reply* cadence ([`01` Stage i](01-discipline-and-pipeline.md)); gtme-sequence currently says "a reply cancels the sequence" with no successor state. This is the missing state.

---

## 4. Infrastructure & Deliverability Numbers

### 4.1 [@dimitarangg](https://x.com/dimitarangg/status/2073424014664401201) — CONFIRMS + NEW

GATED masterclass ($4.8M client pipeline claimed) but the numbers are in the TOC itself, reconciled against [`01` Stage j](01-discipline-and-pipeline.md):

| His number | Corpus (`01` Stage j) | Verdict |
|---|---|---|
| 40 sends/inbox/day | ramp to 40–50/day by wk 4; 40–100/day ceiling | CONFIRMS |
| 12-inbox pods ≈ 480/day | 3–5 inboxes/domain, scale via domains | CONFIRMS (pod framing new) |
| 30-day warm-up | 14–21 days | CONFIRMS — his is the conservative end |
| Main domain never sends | "never cold email from your primary domain" | CONFIRMS |
| Business-hours-only distribution (anti-pattern-matching) | — | **NEW** |
| 3-tier verification (verified/risky/invalid), **each with its own send volume** | verify-before-send only | **NEW** — volume-per-tier framing |
| Weekly 4-metric loop separating deliverability problems from copy problems | — | **NEW** (the 4 metrics unnamed — gap) |

Flag, don't adopt: his character-substitution keyword-filter bypass — spam-filter arms race, likely net-negative against 2026 filters.

Gaps none of the sources fill: exact DNS record syntax, the day-by-day ramp schedule, the 4 monitoring metrics, verification tooling choice.

### 4.2 One-inbox blasting — [@kai_cabero](https://x.com/kai_cabero/status/2054924814150951054) — CONFLICTS

Claims ~5,800 sends from ONE Google Workspace inbox (→ conflict C2, §9). Corpus wins outright; the play *shape* survives in §5.3.

---

## 5. List Building on a Budget

### 5.1 The $102/mo stack — [@fin465](https://x.com/fin465/status/2057478167426965936) — NEW

Framing: Apollo $100 = 5K contact lookups vs Serper $100 = 100K searches — "every standard outbound tool has a 10x-cheaper twin." None of these appear in [`05`](05-repos-and-platforms.md)'s platform landscape, which assumes Clay-tier spend.

| Tool | $/mo | Role |
|---|---|---|
| [Serper.dev](https://serper.dev) | 10 | Scaled Google-search pulls for the initial list (10K queries) |
| [theorg.com](https://theorg.com) | free | Org-chart API — reporting structure, promotions, exits |
| Phantombuster | free→59 | Scrape your LinkedIn post engagers → warm lists |
| Google News RSS | free | Append `/rss` to a news.google.com search → live signal feed |
| [f5bot](https://f5bot.com) | free | Reddit keyword alerts — prospects venting the pain |
| Visualping | 14 | Hourly page-change monitoring, ~200 competitor URLs |
| Origami.chat | 29 | Email + LinkedIn sequencing (author's own product — self-promo flagged in replies) |

Caveat: **zero deliverability line-items** — list+signal+send only; domains/mailboxes/verification/warm-up still required on top.

### 5.2 TAM as owned dataset — [@coldemailchris](https://x.com/coldemailchris/status/2071734259258216484) — CONFIRMS + NEW

ICP boundaries → bulk scrape (Apollo + Google Maps + directories) → **Firecrawl/Serper** crawl → waterfall **LeadMagic → Prospeo → Clay** → **Supabase** ("never start at zero again"). CONFIRMS dossier [Part 3 Step 3](00-DOSSIER.md#part-3--company-strategy--gtm-engineering-the-operating-playbook) (live TAM database) and Step 4 (waterfall); **first primary-source corroboration of gtme-enrich's exact provider order** (LeadMagic first, Prospeo mid). NEW: Firecrawl; Supabase-as-persistence framing.

### 5.3 TAM mapping playbook — [@codyschneider](https://x.com/codyschneider/status/2069767512888143889) — CONFIRMS

Near-1:1 corroboration of the suite's design: ICP in variables + explicit disqualifiers (= gtme-icp/gtme-list hard gates); over-pull then filter (= gtme-list step 2); cheap waterfall naming **LeadMagic, Findymail, Prospeo, PDL** "for pennies" (= gtme-enrich); AI research for soft qualifiers — "this is where the leverage is"; tier 1 human-led / tier 3 fully automated (= gtme-score `effort_mode`); "intent signals are noise without a base map" (= gtme-signals doctrine verbatim). Marginal NEW (reply): Exa + Overture Maps for the universe pull.

### 5.4 Competitor-follower wedge — [@kai_cabero](https://x.com/kai_cabero/status/2054924814150951054) — CONFIRMS shape

Competitor's LinkedIn followers → boolean title filter → enrich (Findymail backstop at $0.05/email; "chasing dead emails tanks your sending domain by Friday") → outreach. Shape CONFIRMS Nick Abraham's competitor-engager play ([`02a` §4](02a-operators-outbound.md)). Red flags: company-page follower lists aren't publicly visible (personal profiles only); claimed 89% hit rate + single-inbox blast = results-marketing, discarded (C2).

### 5.5 Serverless scraping — [@MitchellKeller_](https://x.com/MitchellKeller_/status/2072699095387447522) — NEW (weak)

Undocumented public JSON endpoints via Cloudflare Workers/GCP/Lambda free tiers; named targets GetLatka, LinkedIn, SEC EDGAR. Technique note only: LinkedIn scraping violates ToS (corpus hard rules, [`03`](03-osint-tradecraft.md)/dossier Part 4); EDGAR is free/legit anyway.

---

## 6. GTM Playbooks by Company Stage

### 6.1 Pre-launch — Sam Blond ×2 — NEW

No launch playbook existed in the corpus. Both from one operator, one coherent system:

**Monaco stealth→big-bang** ([via @CDTEliot](https://x.com/CDTEliot/status/2065824263916097723)): real stealth ~1 year, then 0→100 in one day (launch video + fundraise announcement + outbound waves); distribution spreadsheet with **4 tabs** (employees / investors / friends-of-firm / customers), each employee contributes 3–5 influential contacts, each group gets copy + video link + timing; **45 days out**: ~5-person launch committee, 2–3 executable stunts; relaunch at every milestone (beta/GA/each raise); budget-constrained → creative over paid ("$100 poker sets to 100 ideal customers can beat tens of thousands in ads").

**Brex billboards** ([@samdblond](https://x.com/samdblond/status/1653150044265099265)): ~$50k/mo × 3 = $150k, majority of downtown-SF inventory (bus shelters over highway boards — longer impressions, cheaper), all posted launch day + PR + fundraise same day. Fit test: geographic ICP density + one-line message. Craft note: high letter/background contrast (his "biggest mistake ever" was low contrast). Caveat from replies: no CAC/LTV math — land-grab mode.

### 6.2 First customers ($0→$1–2M) — NEW

**YC LinkedIn outbound playbook** ([@fin465](https://x.com/fin465/status/2055137077868814804)): Clay/Origami lists → auto connect+DM sequencer → **200 connects/week** (→ conflict C3, §9) → 2-sentence DMs with a warm thread → **5 posts/week** → AEO (answer-engine optimization — being the cited answer in ChatGPT/Perplexity; tool named: Searchable). ~20 hrs/week → consistent demos. First posting-quota and LinkedIn-first numbers in the corpus; AEO is a genuinely new channel.

**Conference-only GTM** ([@fin465](https://x.com/fin465/status/2058300451880354071)): YC company, $0→$2M ARR/6mo, <$few-K per event. 4 weeks before: public posts + DMs, lock **10 top targets**, everyone else → drip. During: **12×30-min meetings/day** off-booth (café/private room), gifts, film 5 casual customer Q&As. After: **15–20 captioned clips dripped for ~a month**, reused to promote the next event. Transferable core: one event cycle = months of content + warm pipeline. Corpus had no event motion at all.

**Why outbound exists** — motivation-layer evidence the corpus asserted but never sourced: sales-first beat PLG in [@frantzfries](https://x.com/frantzfries/status/1674031281414258694)'s YC batch (his own nuance: PLG takes years; adding sales later is easy, retrofitting PLG is hard); **70–80% of businesses are referral-only** ([@mattceras](https://x.com/mattceras/status/2057600478859387072)) — outbound is contrarian alpha, and referral-only caps around low-$M with no volume/timing control.

### 6.3 Scaling ($2M→$30M)

**Clay distribution** ([@LoganTGott](https://x.com/LoganTGott/status/2055778612364579005)) — CONFIRMS dossier [Part 2 #10](00-DOSSIER.md#part-2--the-10-frontier-operators) and [`02b`](02b-operators-growth.md): one ICP refused to expand, public Slack community, founder-led LinkedIn, user-generated workflow proof, PLG then sales. Reply caveats kept: chronology flattened (founded 2017); Clay also used outbound agencies.

**Vibe-marketing quotas** ([@codyschneider](https://x.com/codyschneider/status/1950949576224985108)) — thesis CONFIRMS his dossier entry + Atlas intro ("AI collapsed the hypothesis→system gap"); the quotas (100 UGC ads, 1,000 BOFU posts, 100 influencer emails, 10 lead magnets, 35 LinkedIn posts/wk) are NEW but quality-control-free — directional only.

Stage-level conflict resolutions (intra-section): **big bang vs drip** — big bang for moments (launch, raise), drip for the ambient motion between; **sales-first vs PLG** — early revenue = sales, durable scale = product-led (Frantz's own reconciliation); **volume vs white-glove** — deal-size fork (automation mid-market, 10-target white-glove enterprise); **paid vs creative** — budget fork (OOH only with dense ICP + funding); **referrals** — PMF signal, not a scaling strategy.

---

## 7. The Attio GTM Atlas

**[atlas.attio.com](https://atlas.attio.com/)** — free, ungated, 15 operator-written chapters (Attio's launch tweet is deleted; the resource is live). Discovered via an X bookmark; the best single scaling-stage reference found in this pass, and absent from [`05`](05-repos-and-platforms.md)'s resource inventory. Seven chapters read deep; the standouts:

**Kyle Norton (CRO, Owner) — "Start with the data"** ([chapter](https://atlas.attio.com/start-with-the-data)) — CONFIRMS + NEW:
- "No training, hiring profile, call volume or slick techniques can overcome giving your team bad data."
- Tier A/B/C at **25/50/25 — and never work tier C** ("who you will never close"; routed out, not deprioritized). Sharper than gtme-score's tier-3-automated.
- BDRs spend **~70% of their day researching**, not selling; AI pre-call research → **150–250 prepared calls/day**; per-rep closed-won ARR **$72k → ~$120k/mo** after fixing the data layer (top performer $174k/mo at $8–10k ACV).
- **Centralized scoring owned by ONE person** — expert-built AI output "20× better" than per-rep hacks.
- **Trade 2 BDR heads for 1 GTM engineer** at ~2× BDR salary — CONFIRMS dossier Parts 1 & 3; defines the auto-gtme buyer persona.

**Roniesha Copeland (Vercel) — "Build the system before the message"** ([chapter](https://atlas.attio.com/build-the-system-before-the-message)): ICP + narrative + timing, in that order; intent is an **effort multiplier on the TAM, never a filter**; altitude failure case — v0 demo apps to enterprise budget owners got high opens, zero conversions (asset pitched at the wrong seniority); qualification = pain exists + urgent now, "enthusiasm is not the same as reason to buy"; pre-register metrics, kill fast, always running something.

**Maja Voje — "Build your GTM brain"** ([chapter](https://atlas.attio.com/build-your-gtm-brain)): describes a Claude Code GTM setup that is the architectural sibling of auto-gtme — CLAUDE.md + context files + markdown skills + workflows + **outputs archived with source context** (six months of archives = the feedback loop). "A team still prompting is running a chatbot. A team doing context engineering is running a brain." Numbers: $2–5M funding round ~3 months post-close = optimal window; proprietary research converts **3–5× (up to 10×)** vs templates against a 70%-AI-slop LinkedIn baseline; ECP before ICP; snow-leopard rule ("don't build your ICP around the one-offs").

**Shreman Shrestha (Granola) — "Attachment is the signal"** ([chapter](https://atlas.attio.com/attachment-is-the-signal)): PLG signal family — seat-growth velocity, **seat composition ("five seats can be a bigger signal than fifty, depending on which five")**, response velocity (hours vs weeks), shadow-IT discovery as the trigger moment; champion ≠ decision-maker, record both.

**Travis Bryant (Anthropic) — "What only a human can deliver"** ([chapter](https://atlas.attio.com/what-only-a-human-can-deliver)): 4,000-account mid-market book; AI owns notes→CRM, MEDDPICC updates, **account-potential scoring across the entire territory**, whole-book research; humans own conversations (target: 8 hrs/day live); leadership manages 3 metrics — live-conversation hours, tasks offloaded to Claude, Gong coaching.

Also mined: Elena Verna (Lovable) — satellite apps over gated PDFs, freemium booked as marketing budget, agents entering the ICP; Emily Kramer (MKT1) — TAM <~1k accounts ⇒ outbound by arithmetic, ungate everything (LLMs harvest it anyway), kill MQL/SQL for activity timelines; Rati Zvirawa (Fin/Intercom) — agent *owns* the funnel (playbook + knowledge + bidirectional data flow), expect legacy metrics to break.

Full chapter-by-chapter skill mapping preserved in the review; the per-skill rollup feeds §10.

---

## 8. GTME Systems in Production

### 8.1 Anthropic's sales ramp — Eleanor Dorfman via [@jasonlk](https://x.com/jasonlk/status/2057197923146862621) — NEW

First primary account of an at-scale internal GTME system; nothing like it in the corpus. (Bookmarked tweet deleted; recovered across [three](https://x.com/jasonlk/status/2057197923146862621) [related](https://x.com/jasonlk/status/2060064561508814946) [tweets](https://x.com/jasonlk/status/2064634927421767938), all reporting SaaStr AI 2026.)

- **Thread Claude through the existing stack, don't buy a new one:** kept Clay, LeanData, Salesforce, Gong, Ironclad, Slack; Claude is the connective tissue.
- **5 skills every new rep gets** (codified from best reps): `/morning brief`, `/call prep`, `/customer follow-up`, `/competitive intel`, `/create-an-asset`. Invoked via `/` from inside Slack/Salesforce — the interface is invisible.
- **Accountability lives in the workflow, not management:** the 24-hr follow-up SLA is enforced by the skill itself — drafts responses, drops them in email, nags in tomorrow's brief if unshipped. Shadow targets, 87% of AEs hit them.
- **Anti-slop is engineered into the skill file** — brand, policy, customer context baked in.
- Results: 54% of new enterprise logos self-serve; new reps skip the six-week ramp; Slack is the front door for legal/deal-desk/RevOps (Claude triages, resolves on precedent, escalates with context). "Sales leaders are becoming systems thinkers over deal strategists."

### 8.2 Crustdata's skill library — [@chrispisarski](https://x.com/chrispisarski/status/2072400619756028210) — CONFIRMS + NEW

Whole sales team on unlimited Claude tokens + a shared internal skill library — structurally validates the auto-gtme suite (skills 1:1 with pipeline steps). Skills: org-chart maker (budget owner, champion vs blocker); **calendar-connected morning pre-call briefs** (company funding/hiring/stack/news + person history/posts/mutuals per demo); follow-up drafts in the rep's voice + CRM notes; inbound triage outputting a **close-probability % calibrated on past closed-won** (= gtme-score + gtme-measure's loop, independently invented); trigger-watching → Instantly; list building via the **Crustdata MCP** (not in `05`). Org pattern: **one full-time skill author, shared git repo, PRs propagate to everyone**.

### 8.3 The role, compressed — [@fin465](https://x.com/fin465/status/2060430268176232709) — CONFIRMS + NEW

8-step GTM Engineer role (infra → TAM → segment → score/route → personalize → automate handoffs → warm mix → optimize) = a compression of [`01` §3](01-discipline-and-pipeline.md)'s 11 stages. "Vercel replaced their 10-person sales team with 1 GTM engineer" — **unverified single-source**; @DBredvick (Vercel) is on the §8.5 follow list, verify before load-bearing use. Reply gold: **P(≥1 sale) = 1 − (1−p)^N** ([@amazingdanray](https://x.com/fin465/status/2060430268176232709)) — goal-backwards volume math, feeds gtme-measure; [@mikemichelin]: "the best GTM Engineers build their own data pipelines, not configure Salesloft — distribution engineering, not sales ops" — CONFIRMS the thin-CLI/own-pipeline bet in dossier [Part 6](00-DOSSIER.md#part-6--platform-stack--existing-code).

### 8.4 marketingskills v2.0 — [@coreyhainesco](https://x.com/coreyhainesco/status/2055011827600572668) — NEW

`npx skills add coreyhaines31/marketingskills` ([repo](https://github.com/coreyhaines31/marketingskills)) — ~50 skills, 52 integrations, **100% evals coverage**, Agent Skills spec (Claude Code/Codex/Cursor/Windsurf). GTM-relevant: `cold-email`, `prospecting`, `emails`, `sales-enablement`, `revops`, `lead-magnets`, `launch`, `competitor-profiling`, `marketing-loops`. Absent from [`05` Part A](05-repos-and-platforms.md)'s inventory and now the **largest open analogue** to auto-gtme — study target for taxonomy and evals practice. (His stated motive: the repo IS his lead magnet — a live demo of §8.6.)

### 8.5 Follow list — [@mjwoo94](https://x.com/mjwoo94/status/2056423069032333510) — NEW (minor)

Extends dossier Part 2's bench: @Carles_Reina (ElevenLabs), @Chris_Orlob (pclub.io), @austinh___, @DBredvick (Vercel — the C8.3 verification path).

### 8.6 The lead-magnet meta-play — [@codyschneider](https://x.com/codyschneider/status/2073104495949533667) — NEW

Best current B2B lead magnet: **"free AI training that gets you [ICP outcome]" — a demo-in-disguise** (VSL structure): teach the implementation, be the bridge to doing it. Teaching-first self-selects better-qualified engagers than pitching-first. Corpus has lead-with-value (Cialdini reciprocity, `04` §3.1) but not this mechanic. Feeds gtme-publish; sources 6 (coldemailchris docs) and 8.4 are both live demonstrations.

---

## 9. Conflicts — With the Corpus and Between Sources

| ID | Conflict | Side A (new) | Side B (corpus) | Resolution |
|---|---|---|---|---|
| **C1-len** | Optimal email length | coldemailchris: <70 words strict (checklist <65; 5 questions in <50; bands 30/45/60) [docs 1, 4, 6 — local archive] | [`04` §4.1](04-psychology-nepq-persuasion.md): optimal 50–125; §4.2 target 75–125; gtme-write cap ≤120 | Not fully reconcilable — Chris's data is agency cold-to-cold at volume; corpus blends warmer motions. **Keep ≤120 as the hard cap; add <75 words as the target band** (30/45/60 variants). Lavender's 25–50-word optimum (dossier Part 2 #4) already sided with Chris against `04` §4.1's floor. |
| **C2-inbox** | Volume per inbox | kai_cabero: ~5,800 sends from ONE Workspace inbox [[tweet](https://x.com/kai_cabero/status/2054924814150951054)] | `01` Stage j: 40–100/day/warmed mailbox; §4.1: 40/day | **Corpus wins outright** — kai's number is results-marketing. Keep the play shape (§5.4), discard the infra claim. |
| **C3-li** | LinkedIn connect volume | fin465: 200 connects/week [[tweet](https://x.com/fin465/status/2055137077868814804)] | `01` Stage i: ~100/wk standard-account limit; gtme-sequence: ≤20/day | **Keep the conservative caps** — ban is unrecoverable (gtme-sequence doctrine). Record 200/wk as the aggressive Sales-Nav+automation datapoint; ban risk raised unanswered in his own replies. |
| **C4-incentive** | Paid show-up incentives | Nick Abraham specimen: $25 gift-card PS praised [[tweet](https://x.com/NickAbraham12/status/2071957485003395581)] | Reply dissent: reads cheap when the target's hour costs more; `04` §3.6: incentives must be real and proportionate | **Segment-dependent, optional element** — if used, scale the incentive to the target's hourly value. Not a rule. |

Intra-source tensions (recorded, resolved): case-study numbness (Pisarski) vs proof-leaning specimen (Abraham) — resolution: *proof formats requiring trust are dead; proof the reader can verify themselves isn't* (candidate videos ≠ claims). Buy-vs-own data (Origami's "prompt for leads live" vs Supabase-owned TAM) — for a compounding engine, owned wins; live-prompt is the fast-start. Offer-integrity: risk-reversal copy is copyable, the inventory behind it may not exist — don't write checks the ops can't cash.

---

## 10. Skill-Impact Map

One line per justified edit; sources in brackets refer to sections above.

| Skill | Edits justified | Source |
|---|---|---|
| gtme-write | Add rule 10: the 5-questions gate as a send-blocker | §3.3 |
| gtme-write | Name risk reversal + touch-1 permission CTA under the CTA rule | §2.1 |
| gtme-write | Body target <75 words (bands 30/45/60), cap stays 120; subject 1–3 words, no punctuation, internal-style | §9 C1, §3.7, §2.1 |
| gtme-write | New "Front-end offer" section with the four starter formats | §3.7 |
| gtme-write | Anti-case-study as the canonical follow-up "new argument"; proof_points should tag failure stories | §2.3 |
| gtme-write | 3 new Common Mistakes rows from the levelsio anti-specimen | §2.2 |
| gtme-write | Forwardable test under deeper copy craft | §2.4 |
| gtme-write | Optional spintax note for `fully_auto` sends | §3.5 |
| gtme-sequence | Two-state reply rule: interested reply → 10-touch nurture track | §3.8 |
| gtme-sequence | Email caps: ≤40/inbox/day, business-hours distribution, volume by verification tier | §4.1 |
| gtme-sequence | Record C3; LinkedIn cap holds at ≤20/day | §9 C3 |
| gtme-list | Budget pull sources: Serper, Firecrawl, theorg, Exa+Overture, GMaps/directories | §5.1–5.3 |
| gtme-list | Competitor-follower wedge (personal profiles only; C2 infra discarded) | §5.4 |
| gtme-list | "TAM is an owned dataset" doctrine line; keyword strings in 3 widths | §5.2, §3.7 |
| gtme-enrich | Provenance note: waterfall order corroborated in production; per-tier volume consequence | §5.2–5.4, §4.1 |
| gtme-signals | detectors.md: Google News RSS, f5bot, Visualping, theorg | §5.1 |
| gtme-signals | PLG-attachment family: seat velocity/composition, response velocity, shadow-IT | §7 (Shrestha) |
| gtme-score | "Never work tier C" (25/50/25); single-owner scoring; persona-weighted signals | §7 (Norton, Shrestha) |
| gtme-measure | Offer-tier baseline as the third attribution branch (channel/step/**offer**) | §3.1 |
| gtme-measure | P(≥1) = 1−(1−p)^N volume math; deliverability-vs-copy diagnostic split | §8.3, §4.1 |
| gtme-icp | PQS + NAICS segmentation; ECP-before-ICP; snow-leopard rule | §3.7, §7 (Voje) |
| gtme-publish | "Free AI training" demo-in-disguise; event→content loop; 5 posts/wk floor; AEO watch | §8.6, §6.2 |
| gtme-company | proof_points carries failure stories; Fin's playbook/knowledge/data-flow triad as completeness check | §2.3, §7 (Zvirawa) |
| research/05 + dossier | Add coreyhaines31/marketingskills, Crustdata MCP, GTM Atlas to inventories | §8.4, §8.2, §7 |

---

## 11. Open Loops

1. **@dimitarangg masterclass doc** — pending via X DM (commented "Inbox" from @gigarahul Jul 5; offer was 24-hr-gated, may be dead). Check DMs.
2. **@paolo_scales LinkedIn system** — still gated; requires follow + DM "GTM" from @gigarahul.
3. **coldemailchris 2-hr A-Z video** ([tweet](https://x.com/coldemailchris/status/2066926457608356305)) — untranscribed; yt-dlp + transcribe skill if the systematic backbone is wanted.
4. **2 of 9 masterclass trainings unaccounted** — the TOC promised 9; the 7 archived docs are missing "How to Clear Email Scripts from Spam Words" and the "Live AI Cold Email Script Writing Walkthrough" (video). Re-check the DM'd doc set for completeness.
5. **Vercel "1 GTM engineer" claim** — single-source (§8.3); verify via @DBredvick before citing anywhere load-bearing.

---

## Sources

**Copy specimens & conventions (§2):**
- @chrispisarski, anti-case study — https://x.com/chrispisarski/status/2052087576090051064
- @Scav, VC email pipeline conventions — https://x.com/Scav/status/1639427928873381888
- @StephNass, no-NDA argument — https://x.com/StephNass/status/1782229419245085039
- @NickAbraham12, praised specimen — https://x.com/NickAbraham12/status/2071957485003395581
- @levelsio, anti-specimen — https://x.com/levelsio/status/1708159557430653144

**coldemailchris corpus (§3):**
- Masterclass announcement — https://x.com/coldemailchris/status/2074619017994653712
- Archived docs (local-only, gitignored): `sources/coldemailchris/` — 1-winning-script · 2-psychology · 3-frameworks · 4-checklist · 5-personalized-relevance · 6-gtm-prompts · 7-followup-prompt
- 2-hr A-Z video (untranscribed) — https://x.com/coldemailchris/status/2066926457608356305

**Infrastructure & lists (§4–5):**
- @dimitarangg, deliverability masterclass TOC — https://x.com/dimitarangg/status/2073424014664401201
- @fin465, $102/mo stack — https://x.com/fin465/status/2057478167426965936
- @coldemailchris, TAM as owned dataset — https://x.com/coldemailchris/status/2071734259258216484
- @codyschneider, TAM mapping playbook — https://x.com/codyschneider/status/2069767512888143889
- @kai_cabero, competitor-follower extraction — https://x.com/kai_cabero/status/2054924814150951054
- @MitchellKeller_, serverless scraping — https://x.com/MitchellKeller_/status/2072699095387447522

**GTM playbooks (§6):**
- @fin465, YC outbound playbook — https://x.com/fin465/status/2055137077868814804
- @fin465, conference GTM — https://x.com/fin465/status/2058300451880354071
- @CDTEliot, Monaco/Sam Blond launch — https://x.com/CDTEliot/status/2065824263916097723
- @samdblond, Brex billboards — https://x.com/samdblond/status/1653150044265099265
- @LoganTGott, Clay distribution — https://x.com/LoganTGott/status/2055778612364579005
- @frantzfries, sales-first vs PLG — https://x.com/frantzfries/status/1674031281414258694
- @mattceras, referral-only markets — https://x.com/mattceras/status/2057600478859387072
- @codyschneider, vibe marketing — https://x.com/codyschneider/status/1950949576224985108

**GTM Atlas (§7):** https://atlas.attio.com/ — chapters cited: [start-with-the-data](https://atlas.attio.com/start-with-the-data) · [build-the-system-before-the-message](https://atlas.attio.com/build-the-system-before-the-message) · [build-your-gtm-brain](https://atlas.attio.com/build-your-gtm-brain) · [attachment-is-the-signal](https://atlas.attio.com/attachment-is-the-signal) · [what-only-a-human-can-deliver](https://atlas.attio.com/what-only-a-human-can-deliver) · [your-product-is-the-pitch](https://atlas.attio.com/your-product-is-the-pitch) · [gen-marketers-do-less-better](https://atlas.attio.com/gen-marketers-do-less-better) · [let-ai-own-not-assist](https://atlas.attio.com/let-ai-own-not-assist)

**GTME systems (§8):**
- @fin465, GTM Engineer role — https://x.com/fin465/status/2060430268176232709 (QT: https://x.com/fin465/status/2060128443304657091)
- @paolo_scales, gated LinkedIn system — https://x.com/paolo_scales/status/2074487930832167159
- @chrispisarski, Crustdata skills — https://x.com/chrispisarski/status/2072400619756028210
- @jasonlk, Anthropic sales ramp — https://x.com/jasonlk/status/2057197923146862621 · https://x.com/jasonlk/status/2060064561508814946 · https://x.com/jasonlk/status/2064634927421767938
- @coreyhainesco, marketingskills — https://x.com/coreyhainesco/status/2055011827600572668 · https://github.com/coreyhaines31/marketingskills
- @mjwoo94, follow list — https://x.com/mjwoo94/status/2056423069032333510
- @codyschneider, lead-magnet play — https://x.com/codyschneider/status/2073104495949533667
