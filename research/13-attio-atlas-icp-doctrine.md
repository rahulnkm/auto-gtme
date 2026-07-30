# 13 — Attio GTM Atlas: ICP + signal doctrine

Source: https://atlas.attio.com/ (15 chapters, operator interviews, May 2026). Read in full 2026-07-21 via 3-agent sweep. This file records what Atlas prescribes for ICP construction and signal tracking, and which prescriptions auto-gtme adopted. Quotes are verbatim from page text.

## The two load-bearing chapters

### Maja Voje — "Build your GTM brain" (atlas.attio.com/build-your-gtm-brain)

**ECP before ICP.** "The whole idea of ECP before ICP is that you have to win early to earn the right to go upmarket toward your ICP." ECP = "sub-segments of the market with burning pain points. Usually early adopters, with higher risk tolerance, willing to co-design, not blocked by compliance and negotiations that last a year. You might run out of runway while you're still talking to your ICP."

**The four qualification brackets** ("Every account worth looking at sits inside four brackets"):
1. **Firmographics** — table stakes, insufficient alone: "'Fifty to 250 employees in US tech' is two million companies on LinkedIn. You're spraying and praying."
2. **Behaviors** — "separate conversion-indicative behavior from noise. Visiting your pricing page five times in four days is a signal. Liking your CEO's LinkedIn post is not."
3. **Timing and momentum** — "the 'why now' window. A company that received $2–5M in funding, three months after the round closed, is a sweet spot. You need to harvest that intelligence: funding events, regulation changes, a competitor shifting pricing."
4. **Revenue potential** — effort allocation: "a $100 prospect gets self-serve. A $100K prospect gets proximity and care."

**Weighting from traction, not aspiration.** "Reverse engineer the weighting from your actual traction. If you have even ten clients, ask: which ones do I want 500 more of? Pull their characteristics: deal size, time to close, ease of reaching them. Don't build your ICP around the one-offs (I call these snow leopards). Feed call recordings and win/loss analysis into the brain. ICP isn't a branding exercise. Always bring data, and revisit at least quarterly."

**Proprietary vs commodity signals** ("sea of sameness"): everyone buys the same intent feeds; differentiation comes from "proprietary signals: the ones you define from your product analytics. If an activated account invites five people from the same company, that's the moment sales should reach out."

### Roniesha Copeland — "Build the system before the message" (atlas.attio.com/build-the-system-before-the-message)

**The ICP stack.** "Company and persona are the base. That's your fit layer. Intent goes on top, and that's the layer AI has unlocked… Revenue matters, but not as a filter, as a multiplier on effort. Fit and intent tell you who to pursue. Revenue tells you how much to invest in the pursuit."

**Intent signal types + rationale:** "Intent data tells you something is top of mind. Job postings tell you they're investing in the problem your product solves. Executive hires signal change in the account. These signals don't just tell you who to contact, they tell you what to say and why now."

**Order of operations:** "lay the data foundations for ICP and intent first, or you'll spend the next year retrofitting a system built to acquire the wrong customers."

**Altitude:** buyer ≠ decision-maker as accounts grow — "In a startup, the buyer and the decision-maker are the same person… As soon as you start targeting larger companies, those two roles get further and further apart." Persona attributes must carry seniority/altitude.

**Qualification bar:** "Enthusiasm is not the same as reason to buy." Experiments with pre-committed evaluation: "you decide in advance how you're going to evaluate the outcome."

## Supporting prescriptions (other chapters)

- **Norton (Owner):** "No training, hiring profile, call volume or slick techniques can overcome giving your team bad data." Tier leads 25% A / 50% B / 25% C; "Tier C is who you will never close." "Build a score, deterministic or ML-based." One central data owner (GTM engineer over two BDRs).
- **Kramer (MKT1):** accounts + buying committees over leads; kill MQL/SQL ("milestones, not handoffs"); "You can enrich all that data. Go out and get them."
- **Verna (Lovable):** problem statement before ICP, in customer language; weight daily/weekly-frequency use cases; reserve roadmap for new-persona exploration ("ICP can drift"); "AI agents are becoming part of your ICP."
- **Shrestha (Granola):** attachment over conversion; seats × intensity × WHO ("Five seats can be a bigger signal than fifty, depending on which five"); reply latency as conversion proxy ("hours vs two weeks"); champion (uses it) vs decision-maker (buys it).
- **Epstein (Coder):** deployment speed predicts renewal ("70/80/90"); churn visible 180 days early (tickets stop, calls unanswered).
- **Pastan (Framer) / Singh (Wispr):** one activation metric tied to a retention plateau (D30 asymptote method); ungameable metrics; the signed-up-good-fit-never-returned cohort is "an intent signal."
- **Through-line (all):** no universal playbook; data quality is the single point of failure; measurement is a revision loop, not a scoreboard.

## What auto-gtme adopted (2026-07-21, mousecat run)

| Atlas prescription | Adoption |
|---|---|
| Snow-leopard exclusion | `anchor_accounts` field in icp.json; tiers anchored on repeatable beta lookalikes, whale one-offs flagged |
| Timing sweet spots | `timing_sweet_spots` block (raise 3–12mo ago, fine <6mo, competitor-shift events) layered over loose fit bounds |
| ECP staging | `staging` block: current profile = ECP + explicit graduation criteria to full ICP |
| Behaviors bracket | `behaviors` field, honestly empty where the seller has no telemetry; noise rule demotes social-engagement signals in `signal_notes` |
| Revenue as effort dial | `revenue_potential` per tier drives contacts/effort, not filtering; `review_cadence` quarterly + post-measure |
| Four brackets as checklist | gtme-icp skill: ICP must address all four or state why a bracket is empty |

Not adopted (with reasons): agents-in-ICP (premature for this seller), 25/50/25 tiering (disqualifiers already implement never-close C), activation/product-usage signals (no PLG surface at seller).
