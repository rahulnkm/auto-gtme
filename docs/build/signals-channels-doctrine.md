# auto-gtme — Signals, Channels & Integrations Doctrine

Research synthesis for the open-source Gojiberry build. Sourced from: our own operator dossier (`research/00-02b`), Gojiberry founders' live X posts, @codyschneider TAM playbook (X bookmark), 1lookup API docs, and hands-on MCP/tool capability checks. Snapshot 2026-07-06.

---

## Part 1 — The signal doctrine

### The load-bearing principle (from every operator + Gojiberry)

A signal is **noise until it lands on an account you already wanted.** @codyschneider:
> "everyone's chasing intent. hiring, funding, tech installs, job changes. but a signal is noise until it lands on an account you already wanted. the map turns 'someone got funded' into 'tier 1 account just got funded, route it now.'"

**Implication for auto-gtme architecture:** the TAM map (`gtme-list` + `gtme-icp`) is the base layer. Signals (`gtme-signals`) fire *onto* the map, not into the void. Build the map first, then layer signals. This is the opposite of "detect signal → cold blast."

Jordan Crawford's **"why you, why now" test**: before any outbound fires, there must be a *current public signal* proving this prospect has the problem today. No signal = campaign not ready.

### The signals that top operators actually use (verified from dossier)

Ranked by how often they appear across Nowoslawski, Crawford, Robinson (RB2B), Abraham, Lieben (ColdIQ), Clay:

**Tier 1 — used by nearly everyone, highest conversion:**
| Signal | Source | Who uses it |
|---|---|---|
| **Website visit de-anon** | RB2B / Leadfeeder pixel → resolve anon visitor → LinkedIn within hours | Nowoslawski, Adam Robinson (RB2B's whole thesis), the highest-converting lever named |
| **Competitor content engagement** | Scrape competitor LinkedIn posts → everyone who liked/commented = category-aware buyer | Nowoslawski, Nick Abraham (3-layer), ColdIQ |
| **Own-content engagement** | Auto-track every like/comment on YOUR posts → enrich → score → contextual outreach in 24-48h | ColdIQ (100+ meetings/mo), RB2B |
| **Job change / new hire in persona** | New role = new budget, new tools, new mandate | Nowoslawski recency waterfall, universal |
| **Job posting intent** | Read JDs: SDR posts = small sales team; paid-media hires = ad budget; CTO+layoffs = outsourcing | Jordan Crawford (built a GTM data business on this), Nick Abraham |

**Tier 2 — widely used, strong:**
| Signal | Source |
|---|---|
| **Funding raised** | LinkedIn announcement / Crunchbase / press |
| **Hiring spike** | 3+ postings in target dept in 30d = scaling motion |
| **Tech stack change** | BuiltWith / job posts — added/dropped a tool |
| **Problem post (PQS)** | Prospect publicly wrote about the exact pain (Crawford's Problem Qualification Signal) |
| **Closed-won lookalike** | Feed closed-won into Clay → AI finds firmographic/tech/hiring patterns → build lookalike TAM |

**Tier 3 — situational:**
Product launch, press mention, layoff, new exec hire, office expansion, podcast guest, event speaker, conference-hashtag engagement, G2/Bombora intent (paid), GitHub star in category, newsletter subscribe, content download.

### Gojiberry's actual claimed signal set (for feature parity)

Marketing says "15+" (homepage) / "30+" (Pro plan). Named across their materials + reviews:
job changes · funding rounds · profile visits · post engagement (likes/comments) · competitor engagement · competitor follower tracking · industry trend engagement · group interactions · hiring activity · people discussing your problem.

**Gojiberry is LinkedIn-signal-centric.** Their 30 = mostly LinkedIn-behavior permutations. Our advantage: multi-source signals (web, X, job boards, Crunchbase) not just LinkedIn behavior.

### The 30-signal set for auto-gtme (feature parity + beyond)

Grouped by detection module. **★ = Tier 1 must-have for MVP.**

**LinkedIn (10)** — via `mcp__linkedin__*` + `cli/gtme-linkedin`
1. ★ `li_job_change` — company/title switch
2. `li_promotion` — same-co title bump
3. ★ `li_post_engaged_ours` — liked/commented our post
4. ★ `li_post_engaged_competitor` — engaged competitor post
5. `li_follow_ours` — followed our page
6. ★ `li_new_hire_persona` — target co hired into buyer persona
7. `li_hiring_spike` — 3+ postings target dept/30d
8. ★ `li_problem_post` — authored a pain-keyword post (PQS)
9. `li_group_activity` — active in relevant group
10. `li_profile_visit` — viewed our profile (if visible)

**Web / tech (6)** — via Firecrawl + BuiltWith + pixel
11. ★ `web_visit_deanon` — RB2B-style anon→named (needs pixel on user's site)
12. ★ `job_posting_intent` — JD signals buying (SDR post, paid-media hire, etc.)
13. `tech_stack_change` — BuiltWith/JD delta
14. `content_downloaded` — gated-asset webhook
15. `intent_provider` — G2/Bombora/TrustRadius (paid, optional)
16. `pricing_page_visit` — high-intent page hit (pixel)

**Company (5)** — via Crunchbase + press + RSS
17. ★ `funding_raised`
18. `product_launch` — Product Hunt / press
19. `press_mention` — category news
20. `new_exec_hire` — VP+/C-level joined
21. `layoff_or_expansion` — team-size delta

**X / Twitter (5)** — via `bird`
22. ★ `x_engaged_ours` — like/reply/RT our post
23. `x_engaged_competitor` — engaged competitor tweet
24. `x_follow_ours` — followed us
25. `x_problem_post` — tweeted the pain keyword
26. `x_event_engagement` — engaged conference hashtag

**Media / community (4)** — via web scrape + RSS + GitHub API
27. `podcast_guest` — recent relevant appearance
28. `event_speaker` — speaking at relevant conf
29. `github_star_category` — starred a repo in our space
30. `newsletter_subscribe` — joined our list (webhook)

**MVP core-8 (ship first):** 1, 3, 4, 6, 8, 11, 12, 17, 22 → covers all 5 Tier-1 signals + X + funding + job-posting.

---

## Part 2 — Channel viability for cold outreach

Honest per-channel assessment. Overpromising here gets an OSS project publicly called out.

| Channel | Cold-viable? | Send mechanism available NOW | Notes |
|---|---|---|---|
| **LinkedIn** | ✅ Yes | `mcp__linkedin__send_message` (confirmed, has `confirm_send`) + `cli/gtme-linkedin` write cmds | Connection request + DM. Rate-limit carefully (account is job-hunt-critical). |
| **Email** | ✅ Yes — the workhorse | Adapter needed: SMTP (Gmail/Outlook) + Instantly/Smartlead/Mailgun/Postmark APIs | Cold email is the most established channel. Needs SPF/DKIM/DMARC + warmup. Deliverability tooling (Warmbox, Zerobounce, 1lookup for validation). |
| **X / Twitter** | ⚠️ Partial | `bird` CLI: tweet, reply, follow ✅. **DM = not in bird's current command set**, and X blocks DMs to non-followers unless they opt in | Viable: public reply + follow as a warm-up touch. Not viable: cold DM at scale. |
| **Telegram** | ❌ via our MCP | **`mcp__telegram__*` is READ-ONLY** — only `ListDialogs` + `ListMessages`. No send tool. | Cold Telegram would need Telegram Bot API (recipients must /start the bot first = not cold) OR a Telethon userbot (ban risk, not in current stack). Telegram also design-blocks cold DMs to strangers. **Recommend: defer, or warm-only (existing contacts/groups).** |
| **WhatsApp** | ❌ Deferred (your call) | — | Business Cloud API = opt-in templates only. Unofficial libs = fast ban. Deferred. |
| **Reddit** | ⚠️ Niche-viable | No MCP; browser automation or Reddit API | Cold DMs mostly flagged as spam fast. BUT: PullPush/Reddit API to *find* people discussing the pain (a signal source!) + reply in-thread is viable and high-trust. Better as a **signal source than a send channel.** |
| **Substack** | ⚠️ Warm-only | No API for DM; browser automation | Substack has DMs + Notes. Cold DM viable-ish for creators but low volume, high manual. Better as a **signal source** (who's writing about the pain) feeding LinkedIn/email/X outreach. |

### Recommended channel architecture

**Ship as cold-capable (MVP):** LinkedIn + Email.
**Ship as warm/public touch:** X (reply + follow).
**Ship as signal-source, not send-channel:** Reddit, Substack (find people discussing the pain → route to LinkedIn/email).
**Defer:** Telegram (read-only MCP; would need Bot API or userbot), WhatsApp.

This is honest and still beats Gojiberry, which is **LinkedIn-only + secondary email**. auto-gtme = LinkedIn + email (cold) + X (warm) + Reddit/Substack (signal) = broader multi-channel truth.

### The channel adapter pattern

Every channel = a module implementing a common interface so `gtme-sequence` orchestrates them uniformly:
```
Channel.detect_signals() -> [Signal]
Channel.can_reach(prospect) -> bool
Channel.send(prospect, message, dry_run=True) -> SendResult
```
LinkedIn, Email, X are full adapters. Reddit/Substack implement only `detect_signals()`. Telegram/WhatsApp = stub adapters that raise `NotImplemented` with a roadmap note. New channel = new adapter, no core change.

---

## Part 3 — 1lookup contact validation integration

Wire in for the `gtme-enrich` waterfall's validation step.

- **Base URL:** `https://app.1lookup.io/api/v1`
- **Auth:** `Authorization: Bearer YOUR_API_KEY` (key from app.1lookup.io; store in `.env` as `LOOKUP_API_KEY`, gitignored)
- **Email validation:** `POST /email` body `{"email": "x@y.com"}` — 98.9% accuracy, ~245ms, deliverability check
- **Phone validation:** `POST /phone` body `{"phone_number": "+1..."}` — 97.8% accuracy, carrier info
- **Rate limit:** 1,000 req/min per org (headers: `X-RateLimit-*`)
- **Cache:** 7-day; `bypass_cache: true` to skip
- **Universal credits** — pay-per-use, 7-day free trial, no contract
- Also does IP intelligence (VPN/proxy/fraud, 50+ fraud indicators) — useful for scoring inbound web-visit signals later

**Where it slots:** last step of the enrichment waterfall (`gtme-enrich`). After LeadMagic/Findymail/Prospeo/PDL resolve a contact, 1lookup validates the email/phone before it's allowed into a send queue. Kills bounces = protects deliverability = protects the sending domains.

Ref param `?ref=trustmrr` was on the signup link — that's an affiliate/referral code, not needed for the API itself.

---

## Part 4 — Direct implications for the 13-skill build

| Skill | Role in the Gojiberry-parity pipeline |
|---|---|
| `gtme-company` | Scrape user's website (Firecrawl) → extract product, value prop, customers, competitors, pain keywords |
| `gtme-icp` | Infer ICP from context (variables not vibes — firmographics, technographics, disqualifiers per codyschneider) → editable `icp.md` |
| `gtme-list` | Build the TAM base map: over-pull universe (Crunchbase/BuiltWith/Apollo/scrapers) → filter to ICP → the map signals land on |
| `gtme-signals` | Detect the 30 signals across LinkedIn/web/company/X/media → fire onto TAM accounts → "why you why now" gate |
| `gtme-enrich` | Waterfall (LeadMagic→Findymail→Prospeo→PDL) + **1lookup validation** final step |
| `gtme-score` | Score prospect = ICP-fit × signal-strength × recency → tier 1/2/3 (tier 1 human-led, tier 3 fully auto) |
| `gtme-research` | Per-account soft-qualifier research (do they run paid media? outbound motion? hiring SDRs?) — the codyschneider leverage step |
| `gtme-write` | Signal-aware message gen per (signal, channel, prospect) — names the specific trigger |
| `gtme-sequence` | Multi-channel orchestration via adapter pattern — LinkedIn + email + X, dry-run default |
| `gtme-measure` | Track replies/meetings → weekly re-weight signals + ICP (Gojiberry's "learns every week" loop) |
| `gtme-company` / `gtme-handoff` / `gtme-why` | Cross-cutting: context compaction, run handoffs, why-gating |
| `gtme-linkedin` | Existing CLI — the LinkedIn send + scrape adapter (already 1,156 LOC, contract-tested) |

**The onboarding wedge (beats Gojiberry):** `auto-gtme init --website <url>` → `gtme-company` → `gtme-icp` → user edits `icp.md` → `gtme-list` builds map → `gtme-signals` monitors → full pipeline from one URL. Gojiberry makes users pick signals + define ICP manually; we infer both from the site. (Note: Gojiberry founder Pierre-Eliott is now teasing "enter your website" onboarding too — parity is closing, ship fast.)

---

## Part 5 — Postiz + ManyChat: the inbound content funnel

Gojiberry is **outbound-only**: detect signal → cold DM. Postiz + ManyChat add the **inbound content flywheel** — you *manufacture* the highest-converting signal (own-content engagement) instead of just waiting to detect it. This is exactly the RB2B / ColdIQ motion (post content → capture engagers → route), and it's a genuine feature-parity-PLUS over Gojiberry.

### The closed loop

```
gtme-write ──generates ICP-targeted content──▶ POSTIZ ──publishes across channels on schedule──▶
   content attracts ICP engagement  ═══ this IS Tier-1 signal "own-content engagement" (#3) ═══
        │                                              │
        ├──▶ MANYCHAT comment-to-DM ──▶ opt-in DM sequence (IG / FB / WhatsApp)   [INBOUND capture]
        │                                              │
        └──▶ gtme-signals detects engager ──▶ enrich ──▶ score ──▶ route to cold outreach   [OUTBOUND chase]
                                                       │
                              gtme-measure ──tracks content→pipeline attribution──▶ back to content strategy
```

### Why ManyChat unlocks the channels I said were blocked

Earlier I flagged Instagram / Facebook / WhatsApp cold outreach as **not viable** (Meta blocks cold DMs). ManyChat is the compliant path: **comment-to-DM is opt-in** — the prospect comments a keyword first, which counts as *them* initiating. ManyChat is an official Meta Business Partner using Instagram's official API, so the DM sequence that follows is TOS-safe. auto-gtme + ManyChat = compliant IG + FB + WhatsApp funnels. This is the correct way to reach those channels; the cold-DM path never was.

### Postiz integration (content publishing engine)

Open-source, self-hostable, philosophically aligned with auto-gtme.
- **Base:** cloud `https://api.postiz.com/public/v1` · self-host `{BACKEND_URL}/public/v1`
- **Auth:** API key or OAuth2 (`pos_` token) in `Authorization` header. Store `POSTIZ_API_KEY` in gitignored `.env`.
- **Endpoints:** `POST /posts` (create/schedule) · `POST /upload` (media, upload first — 50MB payload cap) · `GET /integrations` (list connected channels)
- **32 platforms:** X, LinkedIn, Instagram, YouTube, TikTok, Reddit, Discord, Slack, Medium, Dev.to, Bluesky, Mastodon, GMB, etc.
- **Rate:** 90 req/hr post creation (self-host adjustable via `API_LIMIT`)
- **No MCP** → build a thin CLI wrapper (`cli > thin-CLI-around-API > MCP` cascade). `gtme-publish` skill calls it.
- **Privacy win:** Postiz never proxies user tokens — user authenticates directly with each platform. Aligns with auto-gtme's local-first stance.

### ManyChat integration (inbound capture engine)

Closed SaaS but full API; the only compliant IG/FB/WhatsApp path.
- **Docs:** `api.manychat.com/swagger`
- **Auth:** token from Settings > API. Store `MANYCHAT_API_KEY` in gitignored `.env`.
- **Trigger a flow:** `POST /fb/sending/triggerFlow` with `subscriber_id` + `flow_id`
- **Tag mgmt:** add/remove tags on subscribers (route by ICP score → tag → flow)
- **Inbound webhook:** ManyChat fires to `https://hooks.manychat.com/apps/wh` on events; auto-gtme ingests commenter → enrich → score → decide inbound-nurture vs outbound-chase
- **Direction:** bidirectional — auto-gtme can *trigger* ManyChat flows (push scored leads into a nurture) AND *receive* ManyChat captures (webhook → gtme-signals).

### Skill-structure decision

Two clean options (recommend A):
- **A — fold into adapters + 1 new publish skill.** Postiz = a `gtme-publish` skill (content is conceptually distinct from cold sequencing). ManyChat = a capture adapter feeding `gtme-signals` + a send adapter in `gtme-sequence`. Net: **14 skills** (13 + `gtme-publish`).
- **B — 2 new skills.** `gtme-publish` (Postiz) + `gtme-capture` (ManyChat). Net: 15 skills. Cleaner separation, more surface to maintain.

Recommend **A**: `gtme-publish` for the content engine; ManyChat rides the existing channel-adapter pattern (it's just another signal source + send target).

---

## Open questions before build

1. **Web-visit de-anon (signal #11)** needs a pixel on the *user's* website + an RB2B-style resolver. RB2B has a free tier. Integrate RB2B, or defer #11 to a "bring your own pixel data" webhook? (It's a Tier-1 signal, worth getting right.)
2. **Email sending default** — ship SMTP-direct (user's Gmail app password) as zero-dependency default, with Instantly/Smartlead as optional adapters? Recommends yes.
3. **Telegram** — accept read-only (warm-only via manual, or skip entirely in v1)? The MCP can't send. Recommend: stub adapter + roadmap note, don't block DOD on it.
