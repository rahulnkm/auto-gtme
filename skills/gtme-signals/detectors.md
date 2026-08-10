# Signal Detectors — the 34-signal method reference

Per-signal: how to detect it, which tool, the exact query shape, and the false-positive trap. Detect only the ICP's `watch_signals` subset per run. `strength` guidance is the *fresh* value; apply decay by `event_date`.

Tools referenced: `cli/gtme-linkedin` (LinkedIn read/write), `mcp__linkedin__*` (profile/company/posts/search), `bird` (X CLI), Firecrawl/WebFetch (web), WebSearch (news), Crunchbase, BuiltWith/Wappalyzer (tech), Ashby/Greenhouse ATS APIs, RB2B (visitor de-anon), PullPush (Reddit).

---

## LinkedIn signals

| ID | Detect | Tool / query | Trap |
|---|---|---|---|
| `li_job_change` | Prospect switched company/title in last 90d | `mcp__linkedin__get_person_profile` on tracked persons; diff vs last snapshot | Title reword ≠ real move; compare company URN |
| `li_promotion` | Same-company title bump | Same as above; company unchanged, seniority up | Lateral retitle |
| `li_post_engaged_ours` | Prospect liked/commented **our** post | `get_company_posts` on seller page → reactors/commenters | Employees/existing customers engaging |
| `li_post_engaged_competitor` | Engaged a **competitor** post (category-aware = intent) | `get_company_posts` on each `competitors[].linkedin` → reactors | Competitor's own staff; filter to TAM accounts |
| `li_follow_ours` | Followed our page/profile | Seller page followers delta | Bots; require profile completeness |
| `li_new_hire_persona` | TAM account hired into the buyer persona | `search_people` current_company=URN + persona titles, recent start | New hire in unrelated function |
| `li_hiring_spike` | 3+ postings in target dept /30d | `get_company_profile` headcount band + ATS board count (below) | LinkedIn `search_jobs` keyword = junk; use ATS |
| `li_problem_post` | Prospect authored a pain-keyword post | `search_people`/content sweep for `pain_keywords`, author ∈ TAM | **Vendor marketing** — author must work at a TAM account |
| `li_group_activity` | Active in a relevant group | Group member/post scan | Low signal alone; pair with another |
| `li_profile_visit` | Viewed our profile | "Who viewed" (if visible on plan) | Often hidden; opportunistic only |

## Web / tech signals

| ID | Detect | Tool / query | Trap |
|---|---|---|---|
| `web_visit_deanon` | Anon site visitor resolved to a named account | **RB2B** pixel on seller site → webhook; match to TAM | Needs pixel installed; ISP/bot noise |
| `job_posting_intent` | A JD signals buying (SDR post, paid-media hire, "Head of X") | **ATS API**: `api.ashbyhq.com/posting-api/job-board/{slug}` or Greenhouse `boards-api.greenhouse.io/v1/boards/{slug}/jobs`; read JD text | Aggregators stale/inflated; company ATS is truth |
| `tech_stack_change` | Added/dropped a tool | BuiltWith/Wappalyzer diff + JD tooling mentions | Unverified `incumbent_tech` seed; confirm live. **Directionality is load-bearing:** dropped the incumbent the seller displaces → emit `strong`/`acquire` (buying window). Adopted a competitor of the seller → emit `counter`. Decide the sign here; `gtme-score` trusts it and won't reinterpret. |
| `content_downloaded` | Gated-asset interaction | Seller webhook → account match | Personal/junk emails |
| `intent_provider` | G2/Bombora/TrustRadius intent surge (paid) | Provider API if configured | Account-level only; no person |
| `pricing_page_visit` | High-intent page hit | Pixel/analytics event | Competitors/researchers |

## Company signals

| ID | Detect | Tool / query | Trap |
|---|---|---|---|
| `funding_raised` | New round | WebSearch news + company blog, cross-confirm LinkedIn announcement | Old round resurfacing; date it |
| `product_launch` | PH/press launch | Product Hunt + WebSearch | PR ≠ buying intent alone |
| `press_mention` | Category news mention | WebSearch/news RSS by company + category | Negative press; read sentiment |
| `new_exec_hire` | VP+/C-level joined | `search_people` senior titles recent start + press | Interim/advisory titles |
| `layoff_or_expansion` | Team-size delta | Headcount band delta + news | Direction matters; layoff can be counter |

## X / Twitter signals

| ID | Detect | Tool / query | Trap |
|---|---|---|---|
| `x_engaged_ours` | Liked/replied/RT our post | `bird` on seller handle timeline → engagers | Existing customers |
| `x_engaged_competitor` | Engaged competitor tweet | `bird search` competitor handle engagers | Competitor staff |
| `x_follow_ours` | Followed us | Seller followers delta | Bots |
| `x_problem_post` | Tweeted the pain keyword | `bird search "<pain_keyword>"` filter to plausible ICP | Vendors; verify bio/company |
| `x_event_engagement` | Engaged a conference hashtag | `bird search "#<event>"` | Broad; pair with ICP filter |

## PLG / attachment signals (require seller product telemetry; skip if the seller has no free tier)

Attachment is the signal: would removal cause a ruckus? (Shrestha, Granola). Weight by **who** fired, not raw counts — 5 C-level seats > 50 generic.

| ID | Detect | Tool / query | Trap |
|---|---|---|---|
| `plg_seat_velocity` | Seat growth accelerating inside one account (10→20→50 in weeks) | Seller product analytics / billing events → match domain to TAM | Bulk-provisioned pilot seats ≠ organic pull |
| `plg_seat_composition` | High-seniority or 5+ same-company seats appear | Product user list × enriched titles/domains | Contractor/agency emails on the domain |
| `plg_response_velocity` | Account replies in hours, not weeks | Email/CRM thread timestamps per account | One fast reply from a non-buyer persona |
| `plg_shadow_it` | IT/security discovers unsanctioned usage (SSO / domain-capture inquiry) | Support + security inbound, SSO requests | The moment cuts both ways — can be a buy or a shutdown; emit `counter` when it reads shutdown |

## Media / community signals

| ID | Detect | Tool / query | Trap |
|---|---|---|---|
| `podcast_guest` | Recent relevant appearance | WebSearch "<name> podcast" + show RSS | Old episodes; date it |
| `event_speaker` | Speaking at a relevant conf | Conference agenda scrape | Past events |
| `github_star_category` | Starred a repo in our space | GitHub API stargazers of category repos → match | Casual stars; low alone |
| `newsletter_subscribe` | Joined our list | Seller ESP webhook | Junk signups |

---

## Budget detection stack (free/cheap standing feeds)

- **Google News RSS** — run the search on news.google.com, append `/rss` → live per-account/per-keyword feed. Feeds `funding_raised`, `product_launch`, `press_mention`, `new_exec_hire`.
- **f5bot** (free) — Reddit keyword alerts; prospects venting the pain in the wild → `li_problem_post`-class events. Same trap: author must work at a TAM account.
- **Visualping** (~$14/mo) — hourly page-change monitoring on TAM pricing/careers/customers pages → `tech_stack_change` / `job_posting_intent` / repositioning triggers.
- **theorg.com** (free org-chart API) — promotions/exits LinkedIn doesn't expose cleanly → `new_exec_hire` / `li_promotion`.

## Cross-cutting rules

- **Every event needs a `detection` block** (source, method, query) — reproducible or it doesn't count.
- **Date by `event_date`**, not detection time — decay depends on it.
- **Detection gap ≠ absence** — if a source is unavailable (no auth, no pixel), mark unknown/omit, never `none`.
- **Reddit/Substack are signal sources here** (find `x_problem_post`-style pain via PullPush/Substack search), routed onto TAM accounts — not send channels.
- **Preloaded signals** from `gtme-list` (job-post axis) arrive on the map already; don't re-detect, refresh their `detected_at`.
