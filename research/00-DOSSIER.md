# GTM Engineering — Master Research Dossier

**Compiled:** May 2026 · **For:** the `auto-gtme` skill suite · **Status:** review draft

This is the synthesis layer. Six detailed, fully-sourced research files sit underneath it in this folder:

| File | Covers |
|---|---|
| [`01-discipline-and-pipeline.md`](01-discipline-and-pipeline.md) | What GTM-E is, its origin, the role, the 11-stage pipeline, standard vs. frontier |
| [`02a-operators-outbound.md`](02a-operators-outbound.md) | Frontier operators — outbound / cold-email / Clay-ecosystem wing |
| [`02b-operators-growth.md`](02b-operators-growth.md) | Frontier operators — growth / content / AI-tooling / sales-led wing |
| [`03-osint-tradecraft.md`](03-osint-tradecraft.md) | OSINT for people, prospects, companies — agent-executable workflows |
| [`04-psychology-nepq-persuasion.md`](04-psychology-nepq-persuasion.md) | NEPQ, neuroscience, Cialdini, cold-email copywriting that converts |
| [`05-repos-and-platforms.md`](05-repos-and-platforms.md) | Existing GitHub repos/skills + platform landscape + recommended stack |

**Methodology.** Six parallel research agents ran web research (WebSearch/WebFetch) and `gh` GitHub queries. Every non-obvious claim is sourced inline in the underlying files. `bird` (the X CLI) is installed but had no X auth at compile time — see [Appendix C](#appendix-c--bird-cli--primary-source-gap). All operator handles were cross-verified against live profiles; unverified items are marked.

---

## Part 1 — What GTM Engineering Is

**GTM engineering (GTM-E)** is the systematic application of software, automation, AI, and data infrastructure to revenue generation. A GTM engineer is "half commercial thinker, half builder" — they own the *system* that produces pipeline, not the individual deal.

- **The term was coined by Clay in 2023** (co-founders Kareem Amin and Varun Anand, over Slack), crystallizing a hybrid role that had been scattered across RevOps, growth hacking, SDR ops, and sales engineering.
- **Five catalysts converged 2022–2024:** (1) the collapse of spray-and-pray outbound after Google/Yahoo's Feb 2024 bulk-sender enforcement; (2) the post-ZIRP "efficient growth" mandate; (3) Clay's rise as GTM infrastructure ($3.1B valuation, $100M+ ARR); (4) signal/intent data maturing; (5) LLMs making per-prospect personalization economically viable.
- **It is a *build* discipline, not a *run* discipline.** RevOps maintains the system of record; GTM-E builds automations that execute strategy at scale. Job postings grew **205% YoY in 2025**; median US comp **$127K–$176K** (top firms pay $250K+).

**The canonical 11-stage pipeline** — strategy → ICP → TAM/market map → signals → list building → waterfall enrichment → scoring → personalization → multichannel sequencing → deliverability infrastructure → measurement & feedback loops. Each stage has a "standard" version and a "frontier" version; the gap between them is the entire opportunity. Full stage-by-stage detail in [`01`](01-discipline-and-pipeline.md).

**Where the frontier is moving (2026):** agentic enrichment (AI reasoning across the whole pipeline, not column-by-column), **context engineering** as the new moat (persistent organizational memory that compounds), signal-based selling becoming table stakes, GTM-E formalizing as a standalone function, stack consolidation (10–15 tools → 3–5), and a **hybrid human-AI model** winning over "fully autonomous AI SDR" (50–70% of pure-AI-SDR contracts churned within 90 days).

---

## Part 2 — The 10 Frontier Operators

Selection criteria: top-1% measurable results, *consistently* testing and *publicly sharing* frontier tactics, and genuinely pushing the field's standard forward (not recycling frameworks). Drawn from a verified pool of ~15 candidates across both wings. The two you named — Eric Nowoslawski and Cody Schneider — anchor the list.

### 1. Eric Nowoslawski — *Growth Engine X*
Clay's first external marketing contractor; now runs Clay's highest-volume enrichment account (~4M emails/month, 300+ clients). Treats cold email like paid-ads media-buying.
- **Follow:** X [@ENowoslawski](https://x.com/ENowoslawski) · LinkedIn [/in/outboundphd](https://www.linkedin.com/in/outboundphd/) · [YouTube](https://www.youtube.com/channel/UC6ef5yDFz7gm8rARwX3HaDw) · [growthenginex.com](https://www.growthenginex.com/)
- **Signature game:** email-as-ad-platform (20–50 concurrent campaigns); Claude Code for TAM-building → Clay for "final-mile" enrichment; domain-health monitoring (domain "cooked" <0.7% reply rate); the Loom-transcript automation method.

### 2. Cody Schneider — *Graphed / Swell AI*
The frontier voice on content-led GTM. Built a "become-the-media" system: machine-scale content repurposing + branded-search dominance + AI-agent analytics.
- **Follow:** X [@codyschneiderxx](https://x.com/codyschneiderxx) · LinkedIn [/in/codyxschneider](https://www.linkedin.com/in/codyxschneider/) · podcast *In the Pit* · [YouTube](https://www.youtube.com/@codyschneiderx)
- **Signature game:** the "Digital Gravity" framework; podcast-to-everything pipeline (1 interview → 15–20 assets); branded-search growth loop; Claude Code agents that A/B test SEO meta-data autonomously.

### 3. Jordan Crawford — *Blueprint GTM*
The field's highest conceptual innovator. Built "the first GTM data business" by mining job boards as buying-intent signals years before it was mainstream.
- **Follow:** X [@jcraw55](https://x.com/jcraw55) · LinkedIn [/in/jordancrawford](https://www.linkedin.com/in/jordancrawford/) · Substacks [On the Edge](https://edge.blueprintgtm.com/) & [Cannonball GTM](https://cannonballgtm.substack.com/) · [YouTube](https://www.youtube.com/@BlueprintGTM)
- **Signature game:** the FIND framework (Focus → Investigate → Narrate → Deploy); Permissionless Value Propositions; the "why you, why now" test; proprietary-dataset moat thesis (win with data competitors can't buy).

### 4. Will Allred — *Lavender*
The only operator with a genuine statistical dataset — Lavender has analyzed 231K+ cold emails across 50K+ inboxes. He publishes the actual benchmarks.
- **Follow:** X [@WillAllred117](https://x.com/WillAllred117) · LinkedIn [/in/williamallred](https://www.linkedin.com/in/williamallred/) · [lavender.ai/blog](https://www.lavender.ai/blog)
- **Signature game:** "Frameworks not templates" doctrine (50–250% reply lift); the Cold Email Benchmark Report (optimal length 25–50 words); persona-specific scoring; "The Mouse Trap" ultra-short pattern.

### 5. Florin Tatulea — *Common Room*
The clearest public thinker on the volume → precision paradigm shift, with documented plays and disclosed reply rates.
- **Follow:** LinkedIn [/in/florintatulea](https://www.linkedin.com/in/florintatulea/) · Substack [*Prospecting from the Trenches*](https://salesflo.substack.com/)
- **Signature game:** the "Outbound 3.0" framework; signal-vs-intent distinction; job-change play (17% reply / 10% meeting rate); the 10X SDR hiring model; the Buyer Awareness Bucket segmentation.

### 6. Frank Sondors — *Salesforge*
The most complete AI-outbound infrastructure builder — owns the full stack from deliverability rails to AI SDR. Scaled to $3M ARR in <12 months with 3 salespeople.
- **Follow:** X [@franksondors](https://x.com/franksondors) · LinkedIn [/in/franksondors](https://www.linkedin.com/in/franksondors/) · [salesforge.ai/blog](https://www.salesforge.ai/blog)
- **Signature game:** the 5-product Forge suite (own your deliverability rails); Agent Frank (AI SDR); WhatsApp 2-minute trigger sequences (10× email reply rate); Copilot → Autopilot AI-SDR rollout model.

### 7. Michel Lieben — *ColdIQ*
The most prolific publisher of actionable Clay + AI-SDR plays with verified revenue outcomes; scaled ColdIQ to $6M ARR and documents the exact workflows.
- **Follow:** X [@MichLieben](https://x.com/MichLieben) · LinkedIn [/in/michel-lieben](https://www.linkedin.com/in/michel-lieben/) · [YouTube](https://www.youtube.com/@MichLieben) · [coldiq.com/blog](https://coldiq.com/blog/)
- **Signature game:** LinkedIn-engagement → pipeline (7-step autopilot, 100+ meetings/month); 4-provider email waterfall (50% → 85%+ coverage); AI lead-scoring before any send; the 10-step scalable outbound system.

### 8. Adam Robinson — *RB2B / Retention.com*
Invented person-level website de-anonymization for B2B; $0 → $8M ARR in ~15 months on organic LinkedIn alone.
- **Follow:** X [@retentionadam](https://x.com/retentionadam) · LinkedIn [/in/retentionadam](https://www.linkedin.com/in/retentionadam/) · [RB2B newsletter](https://newsletter.rb2b.com/) (100K+ subs)
- **Signature game:** person-level visitor ID → founder outreach within hours; founder-led LinkedIn content engine (Clear/Consistent/Constant); content-market-fit funnel; credit-based PLG pricing (10% free-to-paid).

### 9. Nick Abraham — *Leadbird / Scrubby*
The deepest cold-email-infrastructure and deliverability operator in the field — 90K+ inboxes, 1.5M emails/month, second-most-replied-to account on Smartlead.
- **Follow:** X [@NickAbraham12](https://x.com/NickAbraham12) · LinkedIn [/in/nick-abraham](https://www.linkedin.com/in/nick-abraham/) · [leadbird.io](https://www.leadbird.io/) · [scrubby.io](https://scrubby.io/)
- **Signature game:** catch-all email validation at scale (built Scrubby — reclaims 40–60% of "unusable" lists); domain-as-disposable infrastructure with reply-rate-triggered rotation; 3-layer hyper-personalization (social-follow intent → colleague reference → AI); competitor-content-engager scraping as a buyer-intent signal.

### 10. Kareem Amin — *Clay*
The category's founder — co-coined "GTM engineer," scaled Clay from $1M to $100M ARR in two years, and remains the intellectual anchor of the discipline.
- **Follow:** X [@kareemamin](https://x.com/kareemamin) · LinkedIn [/in/kareemamin](https://www.linkedin.com/in/kareemamin) · [kareemamin.com](https://www.kareemamin.com/) · [clay.com/blog](https://www.clay.com/blog/)
- **Signature game:** waterfall enrichment architecture; "system of action vs. system of record"; Claygent (autonomous research agent, 1B+ runs); signal-triggered Slack alerting; lookalike prospecting from closed-won data; "hire a GTM engineer before your first AE."

### The bench (strong runners-up)
- **Patrick Spychalski** (The Kiln) — creative data sources (Slack-photo enrichment), "offer > personalization," CRM-first enrichment.
- **Jed Mahrle** (Practical Prospecting) — the most reliable *vendor-neutral* voice on what actually books meetings.
- **Armand Farrokh & Nick Cegelski** (30MPC) — the gold standard for cold calling & discovery (adjacent to GTM-E, more sales-craft than systems).
- Also verified & active: **Jesse Ouellette** (LeadMagic), **Stephen Hakami** (Wiza), **Thibaut Souyris** (SalesLabs), **Bruno Estrella** (Clay), **Leslie Venetz**, **Kyle Coleman**.

---

## Part 3 — Company Strategy → GTM Engineering: The Operating Playbook

This is the synthesized "how" — the bridge from a company's strategy and focus to a running GTM engine. It is also the spine of the `auto-gtme` skill suite. Ten steps, each with the frontier standard and which operators it draws from.

**Step 0 — Encode the strategy into a GTM context graph.** Before any list or email, capture positioning, differentiation, value props per segment/persona, top 3–5 objections, and proof assets into a persistent, machine-readable store. This *context graph* is the compounding moat (Kareem Amin's "context engineering"; Clay's frontier section). It is what every downstream AI step queries. In `auto-gtme` this is sourced from Notion + Granola + CRM closed-won data.

**Step 1 — Define a scored ICP with negative criteria.** Not "mid-market SaaS" but explicit firmographic + behavioral + technographic criteria converted to a 0–100 fit score, *plus* disqualifiers. Operationalized as filterable fields, validated quarterly against won/lost data.

**Step 2 — Build the signal library (5–15 signals).** Each signal gets a detection method, routing rule, message template, speed-to-touch SLA, and a metric. Sources: first-party (pricing-page visits), third-party (job changes, funding, hiring, tech installs), dark-funnel (de-anonymized visits). Jordan Crawford's job-board mining and Florin Tatulea's signal-vs-intent distinction live here.

**Step 3 — Build a live TAM database.** A continuously-refreshed Clay table — not a one-time CSV — that auto-populates accounts matching the ICP and fires enrichment per row.

**Step 4 — Waterfall-enrich.** 3–5 providers in sequence (pay only for matches) to push email coverage to 85–95%, always ending in a verification step. Catch-all warning: 15–28% of B2B domains accept any address. Michel Lieben's 4-provider waterfall; Kareem Amin's waterfall architecture.

**Step 5 — Score & prioritize.** Multi-dimensional score = firmographic fit + signal strength + relationship context. Frontier: an ML model retrained on every closed deal (compound feedback loop).

**Step 6 — Research & OSINT per prospect.** Turn the prospect into 1–2 sharp, verifiable personalization hooks (see Part 4). This is the difference between personalization and *relevance*.

**Step 7 — Write the outreach.** Apply the persuasion stack (Part 5): problem-led framing, NEPQ-influenced opening, one low-friction CTA, 75–125 words. Will Allred's data and Lavender scoring gate every message.

**Step 8 — Sequence multichannel with deliverability infra.** Email + LinkedIn (+ phone), event-triggered not calendar-triggered. Secondary domains, 3–5 inboxes/domain, warm-up always on, spam rate <0.1%. Frank Sondors' infrastructure model; Eric Nowoslawski's domain health monitoring.

**Step 9 — Measure with play-level attribution & close the loop.** Attribute pipeline to the *play* (signal + sequence + message), kill losers, scale winners; on every closed deal, update ICP weights and trigger lookalike prospecting. The engine gets smarter with each deal.

**The meta-principle (Eric Nowoslawski's "marshmallow test"):** never automate a step that hasn't been manually verified. Build in micro-steps — one customer → five → all → add suggestion logic.

---

## Part 4 — OSINT Tradecraft (condensed)

OSINT turns a name + domain into verified contact data and sharp personalization hooks. Full agent-executable workflows in [`03`](03-osint-tradecraft.md).

- **Google dorking** — advanced operators (`site:`, `intitle:`, `filetype:`, `intext:`, `AROUND(n)`, `after:`) with copy-pasteable recipe sets for profiles, emails, decision-makers, documents, and conference/podcast appearances. The Google Hacking Database is a recipe library. Rate-limit queries 10–15s apart or use the Custom Search JSON API.
- **Person OSINT** — `osint.industries` (1,500-source pivot engine), `sherlock` (username enumeration across 400+ sites — installed locally), Hunter.io (domain pattern), Prospeo/Findymail/LeadMagic (find + verify, catch-all handling). A 5-step email-pattern inference workflow with catch-all risk scoring.
- **Company OSINT** — BuiltWith/Wappalyzer (tech stack + history → displacement plays), ATS monitoring (Greenhouse/Lever/Ashby hiring signals), funding (Crunchbase — reach out 3–5 days post-announcement), org charts, review-site signals, SEC EDGAR / Companies House.
- **Image & media OSINT** — Forensically's 13 modules (ELA, clone detection, metadata, noise — fake-profile detection); Adobe Photoshop / ExifTool for metadata; reverse image search ranking (Yandex > Google > TinEye free; PimEyes paid). *Correction:* `map-making.app` is a GeoGuessr tool, not an OSINT tool — use Bellingcat's map / Maphub instead.
- **Signal → hook matrix** — a 9-row table mapping each signal type to a concrete outreach hook template.
- **Ethics & legality (hard rules)** — CAN-SPAM (no B2B exemption; $53,088/email penalty), GDPR (legitimate-interest basis + documented LIA; suppress personal-email domains; 3-year retention cap), CCPA (B2B exemption expired 2023), CASL (consent required). A `COMPLIANCE_DEFAULTS` dict to encode directly into the agent.

---

## Part 5 — Sales Psychology, NEPQ & Persuasion (condensed)

The persuasion engine for AI-generated outreach. Full detail in [`04`](04-psychology-nepq-persuasion.md).

- **NEPQ (Jeremy Miner)** — 7 question types (Connecting → Situation → Problem Awareness → Solution Awareness → Consequence → Qualifying → Transition/Commitment), built on "people are most persuaded when they persuade themselves." Designed for live calls; what *translates to written outreach* is: problem-awareness as the opening frame, one pressure-free consequence line, a low-friction commitment CTA, neutral-curious tone, one question per email.
- **Neuroscience — evidence vs. myth.** Supported: emotion is a *prerequisite* for decisions (Damasio's somatic markers), social proof activates conformity circuits, storytelling creates neural coupling, cognitive load degrades decisions, dopamine fires on *anticipation* (curiosity gaps). Moderately supported: SCARF (2025 update — Fairness & Autonomy now rank highest), loss aversion (~2× — but only for *real* losses). **Flagged myths:** the "reptilian/triune brain" model (SalesBrain) is scientifically discredited — never cite it; the "95% subconscious" figure is a marketing round-number.
- **Cialdini's 7 principles** applied to cold outbound — reciprocity (lead with specific value), commitment (micro-yes questions), social proof (peer-matched, never fabricated), authority (third-party, not self-proclaimed), liking (genuine research, not flattery), scarcity (real only), and **Unity** (shared identity — the most underused and most powerful).
- **Copywriting that converts** — ≤50-contact targeted cohorts get **2.76× the reply rate** of 1,000+ blasts; optimal length 50–125 words; single CTA = +28–42%; timeline-hook subject lines = 10% reply vs. 4.4% for problem hooks; deep personalization = +52% (vs. +20–25% for merge tags). PAS structure, pattern interrupts, the one-sentence value prop, low-friction graduated CTAs.
- **The translation layer** — a message-skeleton template, a 40-item DO list, a 30-item DON'T list, and a red-flag taxonomy — all already in agent-executable checklist form, ready to become a skill.

---

## Part 6 — Platform Stack & Existing Code

### Recommended `auto-gtme` stack (integration cascade: CLI > MCP > API)

| Pipeline stage | Tool | Integration path |
|---|---|---|
| Intake / knowledge base | **Notion** | MCP — official [`makenotion/notion-mcp-server`](https://github.com/makenotion/notion-mcp-server) (★4,354) or the official [Claude Code plugin](https://github.com/makenotion/claude-code-notion-plugin) (★388) |
| Meeting notes | **Granola** | MCP — official Granola MCP (launched Feb 2026); Personal API on Business/Enterprise |
| CRM (all 3 supported) | **Salesforce** | **CLI** — official `sf` v2 (`sf data query` runs SOQL; `sf data` does record ops). Zero context bloat. |
| CRM | **HubSpot** | Thin CLI wrapper around the [REST API](https://developers.hubspot.com/docs/api) — the official `@hubspot/cli` is CMS/theme-dev only, not CRM data. MCP `baryhuang/mcp-hubspot` (★123) as alternative. |
| CRM | **Attio** | Thin CLI wrapper around the [REST API](https://developers.attio.com/docs) — no official CLI. MCP `kesslerio/attio-mcp-server` (★68) as alternative. |
| Enrichment / waterfall | **Clay** (hub) | MCP official [`clay-inc/clay-mcp`](https://github.com/clay-inc/clay-mcp) / remote `mcp.clay.earth/mcp`; or thin CLI wrapper around the HTTP API |
| Enrichment fallback | Apollo, Hunter.io, Datagma, LeadMagic | API (no CLI/MCP for the enrichment layer generally) |
| Signals / intent | RB2B, Trigify, Common Room | API |
| Sequencing — email | **Smartlead** / Instantly | API |
| Sequencing — LinkedIn | **HeyReach** | MCP `bcharleson/heyreach-mcp` → API fallback |

Key facts: no enrichment tool has a CLI (API only); sequencers have solid APIs but no MCPs; Koala shut down (Sept 2025). The user has **Clay, Notion, Granola, and all three CRMs** (HubSpot, Attio, Salesforce).

> **Integration-strategy revision (from review).** MCP servers load *every* tool schema into the agent's context window — real context bloat across a 10-skill suite. So the cascade is re-ordered to **CLI > thin-CLI-wrapper-around-API > MCP**. `auto-gtme` ships its own thin CLI wrappers (one per platform, invoked via Bash, zero schema bloat) and reserves MCP for cases where a wrapper is impractical and an official MCP is high-quality (e.g. Notion). This is itself the CLI+MCP dual-surface pattern that `bcharleson/close-crm-cli` validates.

### Existing GitHub code worth referencing
- [`gtm-skills/gtm`](https://github.com/gtm-skills/gtm) (★55, actively maintained) and [`chadboyda/agent-gtm-skills`](https://github.com/chadboyda/agent-gtm-skills) (★42, 18 skills) — the closest existing analogues to `auto-gtme`; study their skill taxonomy and naming.
- [`marketinguys/awesome-gtm-engineering`](https://github.com/marketinguys/awesome-gtm-engineering) (★93) — best ecosystem discovery list.
- [`orchidautomation/kiln-plugins`](https://github.com/orchidautomation/kiln-plugins) — stale, but a structural template for GTM-as-Claude-Code-plugin.
- [`bcharleson/close-crm-cli`](https://github.com/bcharleson/close-crm-cli) — the **CLI+MCP dual-surface pattern** `auto-gtme` should itself adopt.

---

## Part 7 — Implications for the `auto-gtme` Skill Suite

The research points to a clear shape for the build (full design comes next, after this review):

1. **A suite, not one skill.** Map skills 1:1 onto the 10-step playbook in Part 3 — an orchestrator skill + ~8–10 focused sub-skills (intake/context-graph, ICP, signals, list-build, enrich, score, OSINT-research, write-outreach, sequence, measure).
2. **The context graph is the core artifact.** Skill 0 builds and maintains it from Notion/Granola/CRM; every other skill reads it. This is the moat.
3. **Persuasion + OSINT are reusable modules**, not pipeline stages — the writing skill embeds the Part 5 checklist; the research skill embeds the Part 4 workflows + `COMPLIANCE_DEFAULTS`.
4. **Integration favors thin CLI wrappers over MCP** to keep the context window lean across 10 skills — cascade is CLI > thin-CLI-wrapper-around-API > MCP. Salesforce uses the `sf` CLI; HubSpot/Attio/Clay/sequencers get bundled CLI wrappers; Notion/Granola use their high-quality official MCPs.
5. **Ship as a public Claude Code plugin/marketplace** on `rahulnkm`'s GitHub — portable to OpenClaw since skills are plain markdown. Runs through a `pre-publish` secrets check before going live.
6. **Compliance and "marshmallow-test" gating are first-class** — human-in-the-loop checkpoints before anything sends.

---

## Appendix A — Master Source List

Where this dossier learned about GTM-E. Grouped; the full per-claim source lists are in each underlying file.

**Defining the discipline:** Clay blog ([GTM Engineering](https://www.clay.com/blog/gtm-engineering), [Series B](https://www.clay.com/blog/series-b-expansion), [Series C](https://www.clay.com/series-c), [How We Built Clay's GTM-E Function](https://www.clay.com/blog/how-we-built-gtm-engineering-function)) · [Steve Ruiz — "WTF is a GTM Engineer?"](https://steveruiz.substack.com/p/wtf-is-a-gtm-engineer) · [Bloomberry — 1000 GTM-E Jobs Analyzed](https://bloomberry.com/blog/i-analyzed-1000-gtm-engineering-jobs-here-is-what-i-learned/) · [Apollo — What a GTM Engineer Does](https://www.apollo.io/insights/what-does-a-gtm-engineer-do-and-why-is-the-role-emerging-now) · [Factors.ai — GTM-E vs RevOps](https://www.factors.ai/blog/gtm-engineering-vs-revops) & [Trends 2026](https://www.factors.ai/blog/gtm-engineering-trends) · [Cargo — GTM Engineering Playbook 2026](https://www.getcargo.ai/blog/gtm-engineering-playbook-2026-autonomous-workflows) · [Maja Voje — 2026 State of GTM Engineering](https://knowledge.gtmstrategist.com/p/the-2026-state-of-gtm-engineering) · [Betts — Comp Trends 2026](https://bettsrecruiting.com/blog/top-gtm-engineer-compensation-trends-in-tech-for-2026/)

**Pipeline, signals & deliverability:** [Unify — Signal-Based Selling Playbook](https://www.unifygtm.com/explore/signal-based-selling-outbound-playbook) · [Autobound — Signal-Based Selling Guide](https://www.autobound.ai/blog/signal-based-selling-complete-guide) · [Factors.ai — Signal-Based Workflows](https://www.factors.ai/blog/signal-based-outbound-workflows) · [DevCommX — Waterfall Enrichment](https://www.devcommx.com/blogs/waterfall-enrichment-clay-vs-zoominfo-vs-apollo) · [EmailLabs — Google/Yahoo 2024 Requirements](https://emaillabs.io/en/google-and-yahoos-email-sender-requirements-in-2024-updated-enforcement-timeline/) · [Topo — Cold Email Sending Limits](https://www.topo.io/blog/safe-sending-limits-cold-email) · [Mailreach — Deliverability Stats 2025](https://www.mailreach.co/blog/email-deliverability-statistics) · [Landbase — 2026 GTM Stack](https://www.landbase.com/blog/2026-gtm-stack-replacing-apollo-salesloft-outreach)

**Operators — outbound wing:** [The Signal Club — Eric Nowoslawski](https://www.thesignal.club/p/inside-eric-nowoslawskis-ai-powered-cold-outbound-machine) · [Smartlead — Eric Nowoslawski case study](https://www.smartlead.ai/blog/case-study-eric-nowoslawski-growth-engine-x) · [Bootstrappers — Jordan Crawford](https://bootstrappers.com/jordan-crawford-blueprint/) · [Cannonball GTM — Beginner's Guide](https://cannonballgtm.substack.com/p/start-here-the-beginners-guide-to) · [Founderpath — Adam Robinson](https://founderpath.com/blog/how-adam-robinson-grew-retention-com-to-22m-revenue-with-6-employees-the-controversial-linkedin-strategy-that-launched-rb2b) · [Startup Spells — Nick Abraham Masterclass](https://startupspells.com/p/nick-abraham-cold-email-masterclass) · [Sequoia Training Data — Kareem Amin](https://sequoiacap.com/podcast/training-data-kareem-amin/) · [EnterpriseZone — Michel Lieben / ColdIQ](https://enterprisezone.cc/how-michel-liebens-coldiq-uses-linkedin-engagement-to-drive-pipeline/) · [The GTM Engineer — Patrick Spychalski](https://thegtmengineer.substack.com/p/the-biggest-unlock-in-cold-outbound) · [Clay University — Waterfalls](https://university.clay.com/lessons/enrich-people-waterfalls-automated-outbound)

**Operators — growth/sales wing:** [In the Pit (Cody Schneider) — Digital Gravity](https://podcasts.apple.com/ug/podcast/building-digital-gravity-how-startups-create-mass-and/id1669371739?i=1000713865907) · [Mill Agency — Cody Schneider interview](https://mill.agency/podcasts/ai-powered-b2b-marketing-with-cody-schneider-co-founder-of-swell-ai/) · [GTM Engineer — Frank Sondors](https://thegtmengineer.substack.com/p/building-an-ai-agent-first-gtm-machine) · [Piscari — Salesforge to $3M ARR](https://piscari.com/how-salesforge-used-ai-to-grow-to-3-million-arr-in-under-a-year-with-frank-sondors/) · [Lavender — Cold Email Benchmark Report](https://www.lavender.ai/blog/the-cold-email-benchmark-report) · [Practical Prospecting (Jed Mahrle)](https://content.practicalprospecting.io/) · [30MPC — Cold Calling Framework](https://www.30mpc.com/newsletter/the-ultimate-30mpc-cold-calling-framework) · [SalesFlo (Florin Tatulea) — New Outbound Playbook](https://salesflo.substack.com/p/68-this-is-the-new-outbound-playbook) · [Common Room — Plays That Pay: Job Changes](https://www.commonroom.io/blog/track-job-changes-to-fuel-pipeline-growth/) · [Pavilion — Rise of the 10X SDR](https://www.joinpavilion.com/blog/trlp-recap-31) · [Exit Five — Bruno Estrella / Clay](https://www.exitfive.com/podcast/how-clay-is-scaling-top-of-funnel-creator-led-marketing-and-seo)

**OSINT:** [Prospeo — Google Dorks for Email](https://prospeo.io/s/google-dorks-email-search) · [Exploit-DB — Google Hacking Database](https://www.exploit-db.com/google-hacking-database) · [OSINT Industries](https://www.osint.industries/) · [Sherlock — Bellingcat Toolkit](https://bellingcat.gitbook.io/toolkit/more/all-tools/sherlock) · [Dropcontact — Email Finder Benchmark 2025](https://www.dropcontact.com/email-finder-benchmark) · [Hunter.io API Docs](https://hunter.io/api-documentation) · [LeadMagic — B2B Data API for AI Agents](https://leadmagic.io/) · [Forensically — Photo Forensics](https://29a.ch/photo-forensics/) · [Visual OSINT 2026 Guide](https://www.social-searcher.com/2026/01/25/visual-osint-2026-the-master-guide-to-finding-people-by-photo/) · [Salesforge — Cold Email Laws](https://www.salesforge.ai/blog/cold-email-laws) · [UnifyGTM — B2B Data Compliance](https://www.unifygtm.com/explore/b2b-data-compliance-gdpr-ccpa)

**Psychology & persuasion:** [7th Level — NEPQ Methodology](https://7thlevelhq.com/our-methodology/) · [NEPQ Cheat Sheet (PDF)](https://irp.cdn-website.com/3b74b76a/files/uploaded/NEPQ+SALES+SECRETS+CHEAT+SHEET.pdf) · [Buchanan Maldonado — SPIN vs NEPQ](https://buchananmaldonado.com/2024/04/18/spin-vs-nepq/) · [NeuroLeadership — SCARF in 2025](https://www.neuroleadership.com/articles/the-evolution-of-the-social-brain-introducing-scarf-in-2025/) · [NCBI — The Brain Is Adaptive Not Triune](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9010774/) · [CXL — Cialdini's Principles](https://cxl.com/blog/cialdinis-principles-persuasion/) · [ASU — The 7th Principle: Unity](https://news.wpcarey.asu.edu/20250422-gentle-science-persuasion-part-seven-unity) · [The Digital Bloom — Cold Email Reply Benchmarks 2025](https://thedigitalbloom.com/learn/cold-outbound-reply-rate-benchmarks/) · [SmartLead — Cold Email Stats](https://www.smartlead.ai/blog/cold-email-stats)

**Repos & platforms:** [gtm-skills/gtm](https://github.com/gtm-skills/gtm) · [chadboyda/agent-gtm-skills](https://github.com/chadboyda/agent-gtm-skills) · [marketinguys/awesome-gtm-engineering](https://github.com/marketinguys/awesome-gtm-engineering) · [clay-inc/clay-mcp](https://github.com/clay-inc/clay-mcp) · [makenotion/claude-code-notion-plugin](https://github.com/makenotion/claude-code-notion-plugin) · [Granola MCP announcement](https://www.granola.ai/blog/granola-mcp) · platform API docs for Smartlead, Instantly, HeyReach, RB2B, Trigify, Apollo, Hunter, Datagma (full URLs in [`05`](05-repos-and-platforms.md)).

*Each of the six underlying files ends with its own complete, per-claim `## Sources` section — ~150 URLs total.*

---

## Appendix B — Glossary

**Waterfall enrichment** — querying data providers in sequence, paying only for matches, to maximize coverage. **Signal / trigger** — an observable event indicating a buying window. **Context graph** — persistent, machine-readable organizational memory queried by AI at outreach time. **Play** — a signal + sequence + message combination, the unit of attribution. **Catch-all domain** — a mail server that accepts any address, defeating naive verification. **NEPQ** — Neuro-Emotional Persuasion Questioning. **ICP** — Ideal Customer Profile. **Deliverability** — the infrastructure ensuring email reaches the inbox.

## Appendix C — `bird` CLI & Primary-Source Gap

`bird` v0.8.4 (a fast X/Twitter CLI: search, read threads, user timelines) is installed but had **no X auth** at compile time. The dossier therefore relies on web research and verified secondary sources — all operator handles were cross-checked against live profiles. To deepen operator playbooks with primary tweets/threads, enable `bird` by either logging into x.com in Chrome/Safari/Firefox, or exporting `AUTH_TOKEN` and `CT0`. This is tracked as a task and is optional — it would enrich, not gate, the build.
