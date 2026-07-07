# 03 — OSINT Tradecraft for B2B GTM Enrichment & Outreach Personalization

**Dossier Section:** Open-Source Intelligence (OSINT) for Sales & GTM Engineering  
**Date:** May 2026  
**Scope:** Practical, agent-executable OSINT workflows for legitimate B2B prospecting  

> **Legal baseline:** All techniques in this document target publicly available information. Gray-area practices are explicitly flagged with `⚠️ GRAY AREA`. Prohibited or high-risk practices are flagged `🚫 DO NOT`. Read Section 6 (Ethics & Legality) before implementing any workflow at scale.

---

## Table of Contents

1. [Google Dorking](#1-google-dorking)
2. [Person OSINT](#2-person-osint)
3. [Company OSINT](#3-company-osint)
4. [Image & Media OSINT](#4-image--media-osint)
5. [Signal Mining & GTM Triggers](#5-signal-mining--gtm-triggers)
6. [Ethics & Legality](#6-ethics--legality)
7. [Sources](#sources)

---

## 1. Google Dorking

Google dorking (also called Google hacking) uses advanced search operators to surface information that standard queries miss — including documents, email addresses, org structures, and publicly exposed files.

### 1.1 Core Operators Reference

| Operator | Syntax | What It Does |
|---|---|---|
| `site:` | `site:acme.com` | Restrict results to a specific domain |
| `intitle:` | `intitle:"VP of Sales"` | Match text in the page title |
| `inurl:` | `inurl:"/team"` | Match text in the URL |
| `filetype:` | `filetype:pdf` | Restrict to a specific file type |
| `intext:` | `intext:"@acme.com"` | Match text anywhere on the page |
| `"exact phrase"` | `"Director of Engineering"` | Force exact phrase match |
| `-exclude` | `-site:linkedin.com` | Exclude a domain or term |
| `OR` | `"CEO" OR "CTO"` | Boolean OR |
| `AROUND(n)` | `"budget" AROUND(5) "Q4"` | Two terms within n words of each other |
| `after:` | `after:2025-01-01` | Results after a specific date |
| `before:` | `before:2026-01-01` | Results before a specific date |
| `cache:` | `cache:acme.com` | View Google's cached version |

**Rate limiting note:** As of early 2025, Google aggressively CAPTCHAs automated-style queries. Space dork queries 10–15 seconds apart in any agent workflow. Consider using the Google Custom Search JSON API (100 free queries/day) for programmatic access.

---

### 1.2 Dork Recipes by Use Case

#### Recipe 1: Find a Person's Social Profiles
```
"Jane Doe" "acme.com" -site:linkedin.com -site:facebook.com -site:twitter.com
```
```
"Jane Doe" site:linkedin.com
```
```
"Jane Doe" (site:twitter.com OR site:x.com OR site:github.com OR site:medium.com)
```

#### Recipe 2: Infer or Find Email Addresses
```
"@acme.com" filetype:pdf
```
```
site:acme.com intext:"@acme.com"
```
```
"@acme.com" filetype:pdf "VP" OR "Director" -site:linkedin.com
```
```
filetype:csv "@acme.com" "email"
```
```
filetype:xlsx "contact" "email" site:acme.com
```
```
"sales@" OR "info@" OR "press@" site:acme.com
```
```
intext:"@acme.com" (intext:"John Doe" OR intext:"J. Doe")
```
```
"@acme.com" filetype:pdf after:2025-01-01
```

#### Recipe 3: Find Decision-Makers at a Company
```
site:linkedin.com "acme.com" "VP of Sales" OR "Chief Revenue Officer"
```
```
site:acme.com intitle:"team" OR intitle:"about" OR intitle:"leadership"
```
```
"acme.com" "Director" OR "VP" OR "Head of" site:crunchbase.com
```
```
inurl:"/about" site:acme.com
```

#### Recipe 4: Find Company Documents / Pricing / Org Info
```
site:acme.com filetype:pdf "pricing" OR "rate card" OR "deck"
```
```
site:acme.com filetype:pdf "employee handbook" OR "org chart"
```
```
site:acme.com "confidential" OR "internal use only" filetype:pdf
```
```
"acme.com" filetype:pptx OR filetype:ppt "strategy" OR "roadmap"
```

> ⚠️ **GRAY AREA:** Dorks that surface documents marked "confidential" or "internal" that were accidentally indexed. The documents are technically public (Google indexed them), but downloading and using them may violate the company's ToS or, in some jurisdictions, computer misuse laws. Use professional judgment — reviewing a leaked pricing PDF for competitive intelligence is different from exploiting exposed employee PII.

#### Recipe 5: Contact Info (Phone, Location, Direct Lines)
```
"acme.com" "direct" OR "mobile" intitle:"contact"
```
```
"Jane Doe" "acme" "+1" OR "tel:" OR "phone:"
```
```
site:acme.com intext:"direct line" OR intext:"direct dial"
```

#### Recipe 6: Conference & Podcast Appearances
```
"Jane Doe" "acme.com" (site:youtube.com OR site:spotify.com OR site:podcasts.apple.com)
```
```
"Jane Doe" "keynote" OR "panelist" OR "speaker" "2025" OR "2026"
```

---

### 1.3 Google Hacking Database (GHDB)

The **Google Hacking Database** at [exploit-db.com/google-hacking-database](https://www.exploit-db.com/google-hacking-database) is a maintained index of thousands of dork recipes organized by category (files containing usernames, error messages, login portals, sensitive data, etc.). Originally popularized by security researcher Johnny Long in 2000 and now maintained by OffSec, it has expanded to include Bing and GitHub searches.

**Agent workflow:** Query the GHDB API or scrape by category tag to find relevant dork templates for any prospecting scenario, then parameterize with target company domain.

---

## 2. Person OSINT

### 2.1 Data Points to Collect

For each prospect, attempt to collect:

| Data Point | Priority | Notes |
|---|---|---|
| Full legal name | High | Verify vs. LinkedIn and email signature |
| Current title & employer | High | LinkedIn + company website |
| Work email | High | See Section 2.3 |
| LinkedIn URL | High | Primary professional identity anchor |
| Phone (direct/mobile) | Medium | Harder to find ethically |
| Location (city/metro) | Medium | Useful for event-based outreach |
| Personal interests/hooks | Medium | Content they've published, podcasts appeared on |
| Social profiles | Low | Twitter/X, GitHub, Substack, personal blog |
| Personal email | 🚫 DO NOT | Out of scope for B2B; GDPR risk |

---

### 2.2 Tool-by-Tool Breakdown

#### OSINT Industries (`osint.industries`)

**What it does:** Real-time pivot tool that accepts an email address, phone number, username, full name, or crypto wallet and returns all associated online accounts from 1,500+ data sources — including Facebook, Instagram, WhatsApp, Telegram, LinkedIn, GitHub, Strava, CashApp, and AirBnB. Integrates with HaveIBeenPwned to flag breached accounts. Exports in PDF, DOC, Excel, or JSON.

**Unique feature:** An interactive timeline that shows the subject's online activity chronologically, helping connect temporal context (e.g., when an account was created, when it was last active).

**When to use:** When you have a prospect's email or phone and want to build a complete social footprint to find personalization hooks — conference attendance (Strava routes from the venue city), side projects (GitHub), interests (Spotify/Strava).

**Access:** Free for government/law enforcement/journalists/nonprofits. Commercial sectors (cyber, legal, insurance) use paid plans. Not a self-serve consumer tool.

> ⚠️ **GRAY AREA:** Using breach data (HaveIBeenPwned integrations) to identify which platforms someone uses is legally complex. Stick to active account discovery, not breach-derived passwords or PII.

---

#### Sherlock (username enumeration)

**What it does:** Open-source CLI tool (Python) that checks a given username across 400+ websites simultaneously and returns all platforms where that username is registered. Version 0.16.0 is the current stable release.

**Installation:** Available at `/opt/homebrew/bin/sherlock` (confirmed installed). Also available via `pip install sherlock-project`.

**Core command syntax:**
```bash
# Basic username search — outputs found profiles to terminal and saves to <username>.txt
sherlock johndoe

# Search for multiple username variations (replaces ? with _, -, .)
sherlock "john{?}doe"

# Limit to specific sites
sherlock johndoe --site github --site twitter

# Export to CSV
sherlock johndoe --csv

# Export to Excel
sherlock johndoe --xlsx

# Save output to specific file
sherlock johndoe --output /path/to/results.txt

# Save multiple username results to a folder
sherlock johndoe janedoe --folderoutput /path/to/folder/

# Include NSFW sites in search
sherlock johndoe --nsfw

# Set custom timeout (default 60s)
sherlock johndoe --timeout 30

# Show all sites checked (including not-found)
sherlock johndoe --print-all

# Show only found profiles
sherlock johndoe --print-found

# Route through Tor for anonymity
sherlock johndoe --tor

# Suppress color output (useful for piping)
sherlock johndoe --no-color
```

**GTM use case:** Infer a prospect's username from their name/email handle, run Sherlock to find their GitHub (for technical prospects — see what they're building), Substack (what they're writing about), Speaker Deck (what talks they've given), or Reddit (what problems they're discussing publicly).

**Agent integration:** Run as a subprocess, parse stdout for URLs, filter by platform relevance (GitHub, Medium, Substack, Speaker Deck prioritized for B2B personalization).

---

#### Hunter.io

**What it does:** Domain search + email finder. Given a company domain, returns all email addresses Hunter has indexed for that domain, along with the inferred email pattern (e.g., `{first}.{last}@domain.com`), confidence scores, and sources. Also provides a name + domain → email finder endpoint.

**API endpoints:**
- `GET /v2/domain-search?domain=acme.com&api_key=KEY` — returns all known emails + pattern
- `GET /v2/email-finder?domain=acme.com&first_name=Jane&last_name=Doe&api_key=KEY` — finds single email

**Rate limits:** 15 req/sec, 500/min. Domain search costs 1 credit per 1–10 emails returned.

**When to use:** Starting point for any company. Run domain search first to determine email pattern. Then use email-finder for specific names. Free tier includes 25 searches/month.

---

#### Prospeo

**What it does:** Email finder and verifier with particular strength on catch-all domains (domains that accept any email regardless of whether the inbox exists). Covers 125M+ verified mobile numbers. Has LinkedIn URL → email enrichment.

**When to use:** When Hunter returns low confidence or catch-all status; when you need mobile numbers alongside email; when you have LinkedIn profile URLs and need emails.

**Benchmark:** In Dropcontact's 2025 test of 20,000 contacts, Prospeo showed strong coverage. Their own benchmark claims industry-leading accuracy on catch-all domains.

---

#### Findymail

**What it does:** Focused email finder and verifier. Guarantees <5% invalid email rate. Specializes in catch-all domain handling and bulk list verification.

**When to use:** When you have a prospect list and need to verify/find emails in bulk. Strong at cleaning lists before sending — pair with your primary finder for verification pass.

**Benchmark:** 39.9% real enrichment rate with 1.1% hard bounce rate in the Dropcontact 2025 benchmark (20,000 contacts). Among the cleanest output of any tool tested.

---

#### LeadMagic

**What it does:** B2B data enrichment API purpose-built for GTM engineers and AI agents. Accepts name + domain, LinkedIn URL, or CSV and returns verified work email (97% accuracy, 5-layer validation: syntax → DNS → SMTP → mailbox → risk score), mobile phone, firmographics, technographics, and funding data. Credits roll over indefinitely on Essential+ plans.

**API access:** REST API + CLI + CSV upload + CRM connector.

**Differentiator:** Explicitly positions as "The B2B Data API for AI Agents & GTM Engineers" — designed for programmatic, agent-driven workflows.

**When to use:** When building automated enrichment pipelines where you need email + phone + company context in a single API call.

---

### 2.3 Email Pattern Inference Workflow (Step-by-Step)

```
STEP 1: Domain search via Hunter.io
  → GET /v2/domain-search?domain=TARGET_DOMAIN
  → Extract: pattern field (e.g., "{first}.{last}")
  → If pattern confidence > 80%: proceed to Step 3
  → If catch-all or low confidence: proceed to Step 2

STEP 2: Manual pattern inference
  → Google dork: site:TARGET_DOMAIN intext:"@TARGET_DOMAIN"
  → Find 2-3 confirmed emails from public pages/docs
  → Infer pattern: firstname.lastname / flastname / firstname+initiallastname
  → Cross-check: run pattern against LinkedIn profile of known employee

STEP 3: Construct candidate email
  → Apply pattern to target name
  → Handle edge cases: hyphened names, accents, middle initials

STEP 4: Verify
  → Run through Findymail or Prospeo verification endpoint
  → Check: SMTP response, catch-all flag, confidence score
  → Accept only if: verified=true AND catch-all=false (or catch-all=true AND confidence > 85%)

CATCH-ALL WARNING: 15–28% of B2B domains accept every email addressed to them.
A catch-all "verify" result means the server accepted the SMTP conversation,
NOT that the mailbox exists. Use risk scoring (LeadMagic's 5-layer validation)
to handle these cases.
```

---

### 2.4 LinkedIn-Based Research

LinkedIn remains the most reliable source of truth for B2B professional identity. Key techniques:

**Without Sales Navigator:**
- `site:linkedin.com/in/ "acme.com" "VP of Sales"` — finds LinkedIn profiles mentioning the company
- `site:linkedin.com/in/ "acme" "revenue operations"` — role-specific search
- Use LinkedIn's own search filters (free) for company + title queries; results limited to ~100/month before soft-block

**With Sales Navigator ($99+/mo):**
- Boolean search across 900M+ profiles
- Filter by seniority, function, company size, geography, tenure, recent job changes
- Save leads and get activity alerts

**Free alternatives to Sales Navigator:**
- Apollo.io (275M contacts, free tier: 50 emails/month)
- RocketReach (free: 5 lookups/month)
- Phantombuster (LinkedIn profile scraper — ⚠️ see ToS note below)

> ⚠️ **GRAY AREA:** Automated scraping of LinkedIn violates LinkedIn's ToS (Section 8.2). LinkedIn v. hiQ Labs (9th Circuit, 2022) established that scraping public data is not a Computer Fraud and Abuse Act violation, but LinkedIn can still terminate accounts and pursue civil action. Use Sales Navigator or API-compliant data providers (Apollo, ZoomInfo) instead of raw scraping for production workflows.

---

### 2.5 People-Search & Data Broker Sites

For additional context on publicly available personal professional data:

| Platform | Best For | Notes |
|---|---|---|
| **Apollo.io** | 275M contacts; email + phone + LinkedIn + firmographics | Best all-in-one for SMB/mid-market GTM |
| **ZoomInfo** | Enterprise; org charts, intent data, direct dials | $15K+/yr; best data depth |
| **Clearbit/Breeze Intelligence** | HubSpot-native enrichment | Acquired by HubSpot 2023; credit-based |
| **People Data Labs** | API-first; raw data infrastructure | For teams building custom enrichment pipelines |
| **Cognism** | GDPR-compliant European B2B data | Strongest EU coverage; phone-verified |
| **Lusha** | Browser extension; quick lookups | Good for individual SDRs |

**Accuracy benchmarks (2026, tested on 1,000 leads):**
- Cleanlist: 98% email accuracy
- Cognism: 90%
- ZoomInfo: 85%
- Clearbit/Breeze: 85%
- Apollo: 80%

---

## 3. Company OSINT

### 3.1 Tech Stack Detection

#### BuiltWith (`builtwith.com`)

**What it does:** Scans 414M+ domains, maintains a weekly-refreshed database of detected technologies, and provides historical data showing exactly when a company added or removed a technology. The only tool that reliably answers "when did they switch from Marketo to HubSpot?"

**Pricing:** Basic plan $295/month (2,000 lookups, 2 tech monitors). Team plan $995/month (full API access).

**GTM use case:** Build prospect lists of "all companies using [competitor CRM]" or "companies that adopted Salesforce in the last 6 months." Historical data enables displacement plays.

**API:** `GET https://api.builtwith.com/v21/api.json?KEY=KEY&LOOKUP=acme.com`

#### Wappalyzer (`wappalyzer.com`)

**What it does:** Real-time tech profiler with daily-updated data. Browser extension for instant lookup; API and list-building for scale. Industry benchmark: ~94% accuracy on JavaScript detection (leading among all tech profilers). Builds prospect lists filtered by tech + company size + revenue + geography.

**GTM use case:** "Show me all Italian e-commerce sites running Shopify Plus with revenue above $5M" — then pair that list with email finders.

**Free tier:** Browser extension is free for individual lookups. List exports require paid plan.

**Alternative:** Wappalyzer + BuiltWith together for maximum coverage — Wappalyzer for current state, BuiltWith for history and competitive intelligence.

---

### 3.2 Hiring & Expansion Signals

**What to monitor:**

| Signal | Source | GTM Implication |
|---|---|---|
| New SDR/AE job postings | LinkedIn Jobs, Greenhouse, Lever, Ashby | Sales headcount expansion → they're scaling GTM |
| RevOps/data analyst postings | Indeed, company ATS | Process investment → open to tooling |
| New C-suite hire | LinkedIn announcement | Vendor relationships being reconsidered |
| Engineering surge | Greenhouse, Lever | Scaling tech → dev tool opportunity |
| Geo-expansion roles | LinkedIn Jobs filter by location | Opening new market → regional products |

**Tools:**
- **PredictLeads** — Monitors 5M+ company career pages and ATS systems directly; provides hiring signal API
- **Tapistro** — Job posting intelligence for GTM signal routing
- **Apify Hiring Signal Detector** — Automated job posting scraper with signal classification
- **LinkedIn Jobs** — Free manual monitoring; filtered RSS feeds via tools like Zapier

**Step-by-step ATS monitoring workflow:**
```
1. Identify target company's ATS (Greenhouse: jobs.lever.co/COMPANY or boards.greenhouse.io/COMPANY)
2. Monitor /jobs endpoint for new postings via RSS or polling
3. Classify new posts by department and seniority
4. Map to GTM signal:
   - "Head of Revenue Operations" → high-intent; they're building the stack now
   - "SDR × 3" → scaling outbound; sequence/tool opportunity
   - "VP of Engineering" → leadership change; infrastructure review likely
5. Trigger enrichment + personalized outreach within 72 hours of posting
```

---

### 3.3 Funding & News Signals

**Sources:**
- **Crunchbase** (`crunchbase.com`) — Funding rounds, investors, company description, headcount estimates
- **PitchBook** — Deeper VC/PE data; paid but more accurate
- **TechCrunch** / **Business Wire** / **PR Newswire** — Press releases with stated use-of-funds

**Outreach timing:** Reach out 3–5 days post-announcement to avoid the initial inbox saturation from every vendor in the space doing the same thing. Week 2–3 is the sweet spot.

**Personalization hook template:**
```
"Saw your Series B — congrats. When [PEER COMPANY] raised at a similar stage,
the biggest unlock was [YOUR VALUE PROP]. Given you mentioned [STATED USE CASE
FROM PRESS RELEASE], that's exactly where we've helped teams like [CUSTOMER]."
```

---

### 3.4 Org Chart & Leadership Research

**Free sources:**
- Company website `/about`, `/team`, `/leadership` pages (Google dork: `site:acme.com intitle:"team" OR intitle:"leadership"`)
- LinkedIn company page → People tab → filter by department/seniority
- Crunchbase → People section
- Press releases (often name key hires)

**Paid sources:**
- ZoomInfo org charts (enterprise)
- Lusha (browser extension, individual lookups)
- RelPro ("who knows who" relationship analytics + org data)

---

### 3.5 Review Sites & Growth Signals

| Source | Signal | How to Use |
|---|---|---|
| **G2** (`g2.com`) | Product reviews mentioning pain points and alternatives considered | Identify what problems buyers articulate in your category |
| **Glassdoor** | Employee sentiment, culture, leadership ratings | Understand internal dynamics; churn/morale signals |
| **Trustpilot** | Customer satisfaction trends | Identify unhappy customers of competitors |
| **SimilarWeb** | Web traffic trends | Confirm company is growing or declining |
| **LinkedIn Company Page** | Follower growth, content engagement | Is the company actively marketing? |

---

### 3.6 Public Filings

- **SEC EDGAR** (`efts.sec.gov`) — 10-K, 10-Q, 8-K filings for public companies. 8-Ks announce material events (new executives, acquisitions, major contracts).
- **Companies House** (UK) — Free director/officer lookups, accounts, filings
- **OpenCorporates** (`opencorporates.com`) — Global company registry aggregator; free API for registered officers
- **State business registries** (US) — Secretary of State databases for registered agent and officer names (varies by state)

---

## 4. Image & Media OSINT

### 4.1 Why Image OSINT Matters for GTM

In B2B prospecting, image and media OSINT serves three purposes:
1. **Identity verification** — Confirming you have the right person before outreach
2. **Profile authenticity** — Detecting fake/synthetic profiles on LinkedIn (growing problem in 2025–2026)
3. **Personalization hooks** — Conference photos, speaking appearances, press coverage that makes outreach feel human

---

### 4.2 Forensically (`29a.ch/photo-forensics/`)

A free, browser-based tool with 13 image analysis modules. No upload required — processes images locally. Key modules for OSINT:

| Tool | What It Does | GTM/OSINT Use Case |
|---|---|---|
| **Error Level Analysis (ELA)** | Recompresses the image and highlights areas with different compression — manipulated regions appear brighter | Detect doctored profile photos or fake press screenshots |
| **Clone Detection** | Finds copy-pasted regions within the same image | Spot synthetically generated or edited faces |
| **Metadata Extraction** | Reads EXIF data embedded in the image | Camera model, software, timestamps |
| **Geo Tags** | Extracts GPS coordinates if embedded | Geolocate where a photo was taken |
| **Noise Analysis** | Isolates image noise to reveal airbrushing/warping | Detect AI-generated or heavily edited profile photos |
| **Magnifier** | Pixel-level zoom with histogram equalization | Inspect fine details (badges, backgrounds, text in images) |
| **String Extraction** | Scans for embedded ASCII strings | Find hidden metadata or watermarks |
| **C2PA Content Authenticity** | Reads signed content authenticity metadata | Verify provenance of AI-generated images via C2PA standard |
| **Thumbnail Analysis** | Reveals hidden preview images stored in the file | Sometimes contains an earlier, unedited version of the image |

**Step-by-step fake profile detection:**
```
1. Download suspect LinkedIn profile photo
2. Load into Forensically → run ELA
3. Run Clone Detection
4. Check Noise Analysis for uniform noise (AI faces have suspiciously flat noise)
5. Cross-reference via reverse image search (Section 4.4)
6. Flag if: ELA shows uneven compression AND reverse search finds no prior web history
```

---

### 4.3 Adobe Photoshop for Image Analysis

Photoshop's forensic capabilities (relevant for teams with access):

- **Image → Image Information / File Info** — Reads EXIF/IPTC/XMP metadata including GPS, camera model, copyright, and edit history
- **Edit → Paste in Place + Frequency Separation** — Separates texture from color; reveals retouching artifacts not visible to ELA
- **Filter → Camera Raw → Histogram** — Exposes non-linear histogram curves that indicate selective editing
- **Scripts → Image Processor** — Batch-processes image sets for metadata extraction

For open-source alternative: **ExifTool** (`exiftool -all filename.jpg`) reads and writes metadata across 100+ file types; the most complete free metadata tool available.

---

### 4.4 Reverse Image Search

| Tool | Best For | Notes |
|---|---|---|
| **Google Images** | Broad web coverage; finding original source | Start here for most searches |
| **Yandex Images** (`yandex.com/images/`) | Facial recognition; best free option for Eastern European subjects | Consistently outperforms Google for face matching |
| **TinEye** (`tineye.com`) | Finding earliest indexed version of an image; detecting image history | 60B+ image index; great for proving a photo has existed since a certain date |
| **PimEyes** (`pimeyes.com`) | Deep facial recognition across 3B+ images; 85–95% accuracy | Paid ($29.99/month); most powerful face search publicly available |
| **FaceCheck.ID** | Face search alternative to PimEyes | Free tier available |

**Recommended workflow:**
```
1. Start with Yandex Images (best free facial match)
2. Confirm with Google Images (different index, broader coverage)
3. Check TinEye (find original source + date)
4. If inconclusive: use PimEyes or FaceCheck.ID
```

> ⚠️ **GRAY AREA:** Facial recognition search on individuals without their knowledge is ethically sensitive. In an EU context, biometric processing requires explicit consent under GDPR Article 9. For B2B prospecting, limit use to **public figures** (executives, speakers, published authors) and **identity verification** (confirming you have the right person), not surveillance.

---

### 4.5 EXIF & Metadata Extraction

**What EXIF data can contain:**
- GPS coordinates (latitude/longitude/altitude)
- Timestamp (date/time photo was taken)
- Camera make and model
- Software used to edit
- Copyright and creator fields
- Device serial number (sometimes)

**Key limitation:** Major social platforms (LinkedIn, Twitter/X, Facebook, Instagram) strip EXIF data from uploaded images. EXIF survives in: direct email attachments, personal websites, corporate blogs, GitHub commits, and images downloaded from smaller platforms.

**Tools:**
- **ExifTool** (CLI): `exiftool -all -GPS* filename.jpg`
- **Forensically** (browser): Metadata + Geo Tags modules
- **Refloow Geo Forensics** (open-source): Batch EXIF extraction with GPS visualization on interactive maps; reconstructs event timelines from image sets
- **forensicosint.com** (free web tool): Forensic Image EXIF Reader with GPS/XMP/metadata output

---

### 4.6 Geolocation & GEOINT

For geolocating where images were taken without embedded GPS:

- **Google Maps / Street View** — Cross-reference architectural details, signage, vegetation
- **Yandex Maps** — Better coverage in Russia/Eastern Europe
- **Bellingcat's OSINT Tools Map** — Interactive map listing country-specific OSINT resources (business registries, court databases, phone directories)
- **Maphub** (`maphub.net`) — Create annotated maps of OSINT findings (points, polygons, labels)

**Note on map-making.app:** Despite the suggestive name, this tool is purpose-built for GeoGuessr map creation (a geography game) — it is NOT an OSINT/GEOINT tool and should not be used for investigative workflows.

---

## 5. Signal Mining & GTM Triggers

The OSINT tradecraft above generates raw data. This section maps findings to concrete outreach triggers.

### 5.1 Signal → Hook Matrix

| Signal | How to Detect | Personalization Hook |
|---|---|---|
| **Job change (new role)** | LinkedIn activity, Apollo alerts, Clay job-change trigger | "Congrats on joining [COMPANY] as [TITLE]. In the first 90 days, new [TITLE]s typically focus on [PAIN POINT] — we help teams do that 2x faster." |
| **Promotion (internal)** | LinkedIn "celebrated a work anniversary" / title change | "Saw you moved into the VP role — congrats. New leaders often reconsider the existing [category] stack. Happy to share what [PEER COMPANY] did at the same inflection point." |
| **New hire (their company)** | Job board monitoring (Greenhouse/Lever ATS) | "Noticed you're hiring a [ROLE] — that usually means [IMPLICATION]. That's exactly when companies like [CUSTOMER] came to us." |
| **Funding round** | Crunchbase, TechCrunch, press releases | "Saw the [ROUND] — congrats. [SPECIFIC USE CASE FROM ANNOUNCEMENT] is where we see the most impact for funded teams at your stage." |
| **Tech add/replacement** | BuiltWith alerts, Wappalyzer | "Looks like you recently added [TOOL] — we integrate directly and have helped [CUSTOMER] get [OUTCOME] within 60 days of onboarding." |
| **Podcast/conference appearance** | Google dork (Section 1.2 Recipe 6), Sherlock | "Listened to your talk at [EVENT] on [TOPIC] — your point about [SPECIFIC QUOTE] is exactly the problem we solve for teams like yours." |
| **Published content** | Google Alert, RSS, LinkedIn posts | "Read your piece on [TOPIC] in [PUBLICATION] — you described [PAIN POINT] really well. We've been helping [PEER COMPANY] solve exactly that." |
| **Social activity** | LinkedIn posts, Twitter/X activity | Reference a specific post or thread: "Saw your question about [TOPIC] on LinkedIn last week — that's in our wheelhouse." |
| **Competitor win/loss** | G2 reviews, Glassdoor, industry news | "Saw [COMPETITOR] announced [THING]. Customers who've switched to us from [COMPETITOR] say [KEY DIFFERENTIATOR] is what pushed them over." |

---

### 5.2 Signal-Based Research Workflow (Agent-Executable)

```
INPUT: Target prospect name + company domain

STEP 1: Company-level signals
  → BuiltWith API: get tech stack + history
  → Crunchbase API: funding history, headcount
  → ATS monitoring: open roles (Greenhouse/Lever endpoint)
  → News search: "[COMPANY]" after:LAST_30_DAYS

STEP 2: Person-level signals
  → LinkedIn profile (manual or Sales Navigator)
  → sherlock [USERNAME GUESS]: find other social profiles
  → Google dork (Recipe 6): podcast/conference appearances
  → Google Alert: "[FIRST LAST]" site:youtube.com OR site:podcasts.apple.com

STEP 3: Email discovery
  → Hunter.io domain search → infer pattern
  → LeadMagic API: name + domain → verified email
  → Findymail: verify catch-all status

STEP 4: Signal ranking
  → Score signals by recency (< 7 days = hot, 7–30 days = warm, > 30 days = cold)
  → Score signals by type (funding > job change > tech add > content)
  → Select top 1–2 signals for hook

STEP 5: Outreach assembly
  → Select email template matching top signal type
  → Inject: specific signal detail + peer company reference + clear CTA
  → Compliance check (Section 6): EU domain? Legitimate interest documented?
```

---

### 5.3 Signal Monitoring Tools

| Tool | Signal Type | Pricing |
|---|---|---|
| **Clay** (`clay.com`) | Job changes, LinkedIn activity, funding, tech; AI enrichment orchestration | $149+/month |
| **Apollo.io** | Job changes, company growth, intent data | Free tier; $49/month for basic |
| **PredictLeads** | Hiring signals from career pages + ATS | API-based; usage pricing |
| **Crunchbase Pro** | Funding, acquisitions, executive changes | $49/month |
| **BuiltWith Monitoring** | Tech stack additions/removals | $295+/month |
| **Google Alerts** | News, content publication | Free |
| **PhantomBuster** | LinkedIn activity automation | $56+/month; ⚠️ ToS gray area |

---

## 6. Ethics & Legality

This section is not optional. Any agent workflow must encode these constraints as hard rules.

### 6.1 Legal Frameworks

#### CAN-SPAM (United States)
- **Coverage:** All commercial email, including B2B. No B2B exemption.
- **Key rules:** Accurate sender ID; honest subject lines; physical address in every email; functional unsubscribe mechanism; honor opt-outs within 10 business days.
- **Penalty:** Up to $53,088 per non-compliant email (effective January 17, 2025).
- **Bottom line:** In the US, you can cold-email any business address — but every email must meet the above requirements.

#### GDPR (European Union)
- **Coverage:** Any EU resident's personal data, regardless of where you are located.
- **B2B nuance:** B2B email addresses (jane.doe@acme.com) are personal data under GDPR. However, **legitimate interest** (Article 6(1)(f)) is a valid legal basis for B2B cold outreach IF the outreach is relevant to the person's professional role and you've completed a Legitimate Interest Assessment (LIA).
- **Key rules:** Document your LIA before launching any campaign. Suppress personal email addresses (@gmail, @yahoo, etc.) from prospect lists. Respond to erasure requests within 30 days. Retain data no longer than 3 years from last interaction (best practice).
- **Penalty:** Up to €20M or 4% of global revenue. European DPAs issued 330+ fines in 2025 alone.
- **Bottom line:** GDPR does not ban B2B cold email — but it requires documented legitimate interest and a clear relevance test. "We sell CRM software and you're a sales manager" clears the bar. "We sell dog food and you once mentioned you have a dog" does not.

#### CCPA/CPRA (California)
- **Coverage:** B2B exemption expired January 2023. California residents' business contact data (work email, direct phone, job title) is now fully covered.
- **Key rules:** Honor deletion requests within 45 days. Provide opt-out of "sale" of personal information. New 2026 regulations require formal risk assessments before processing data at scale.
- **Penalty:** $2,663 per violation; $7,988 per intentional violation.

#### CASL (Canada)
- Stricter than CAN-SPAM: requires **express or valid implied consent** before the first email.
- Implied consent lasts 2 years from last commercial transaction.
- Violations: up to CAD$10M per day.

---

### 6.2 Do / Don't Guide for AI Agent Workflows

**DO:**
- Collect only business contact information from public sources
- Document legal basis (legitimate interest) before sending to EU contacts
- Include physical address, sender identification, and unsubscribe mechanism in every email
- Honor opt-out/unsubscribe requests within 10 business days (US) / immediately (EU best practice)
- Verify emails before sending to minimize bounces (protects sender reputation + reduces chance of hitting real inboxes with wrong data)
- Use only GDPR-compliant data vendors for EU contacts (ask vendors to show their legal basis for data collection)
- Purge EU contacts after 3 years of no interaction
- Suppress California residents' data if they have opted out
- Keep records of data source, collection date, and legal basis for each contact

**DON'T:**
- 🚫 Collect or use personal email addresses (@gmail, @yahoo) for cold B2B outreach — GDPR risk is high, and it's not B2B prospecting anyway
- 🚫 Automate LinkedIn scraping at scale — violates ToS; use API-compliant data providers
- 🚫 Use OSINT to find and target individuals' home addresses, family members, or non-work data
- 🚫 Use breach data (leaked passwords, dark web dumps) to identify contact information
- 🚫 Send to Canadian contacts without confirmed consent
- 🚫 Use facial recognition search (PimEyes/Yandex) to build surveillance profiles of non-public individuals
- 🚫 Access or use accidentally indexed confidential documents for competitive intelligence without legal review
- 🚫 Use purchased lists from vendors who cannot demonstrate GDPR-compliant data sourcing for EU contacts
- 🚫 Omit unsubscribe mechanisms from follow-up sequences in automated email cadences
- 🚫 Re-contact contacts who have previously unsubscribed (even if you acquired them fresh from a new source)

---

### 6.3 ToS Considerations by Platform

| Platform | Key ToS Constraint |
|---|---|
| **LinkedIn** | No automated scraping (ToS Section 8.2). Use Sales Navigator API or compliant third-party data providers. |
| **Google** | No automated search queries without API. Use Google Custom Search JSON API (100 free/day). |
| **Hunter.io** | Data collected from public web; may not be used to spam. Rate limits enforced. |
| **Apollo** | Use of data governed by their Data DPA. EU contacts require GDPR-compliant basis. |
| **BuiltWith / Wappalyzer** | Data about websites (not individuals) — generally lower regulatory risk. |
| **GHDB / Exploit-DB** | Dorks are published for security research; using them to access systems you don't own may violate CFAA (US) or Computer Misuse Act (UK). |

---

### 6.4 Privacy-Respecting Defaults for Agent Design

When building the GTM agent, encode these as non-negotiable defaults:

```python
COMPLIANCE_DEFAULTS = {
    "suppress_personal_email_domains": ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com"],
    "eu_contact_requires_lia_documentation": True,
    "max_data_retention_days": 1095,  # 3 years
    "honor_unsubscribe_within_days": 10,
    "require_physical_address_in_email": True,
    "require_sender_identification": True,
    "canadian_contacts_require_consent_flag": True,
    "facial_recognition_allowed_for": ["public_figures_only"],
    "linkedin_data_source": "api_compliant_only",  # NOT raw scraping
}
```

---

## Sources

- [Google Dork Email Search — Prospeo.io](https://prospeo.io/s/google-dorks-email-search)
- [Find Emails with Google: Advanced Search Operators — LetsExtract](https://letsextract.com/2025/12/03/find-emails-with-google-advanced-search-operators/)
- [Google Hacking Database (GHDB) — Exploit-DB / OffSec](https://www.exploit-db.com/google-hacking-database)
- [What Is Google Dorks? Master Advanced Search Hacks 2026 — Cyble](https://cyble.com/knowledge-hub/google-dorks-master-advanced-search-hacks/)
- [Google Dorking Cheat Sheet — chr3st5an on GitHub](https://github.com/chr3st5an/Google-Dorking)
- [Advanced Google Dorking Commands — Cybrary](https://www.cybrary.it/blog/advanced-google-dorking-commands)
- [OSINT Industries — Official Site](https://www.osint.industries/)
- [OSINT Industries — OSINT Tools Library](https://tools.osintnewsletter.com/osint-tools/osint-industries)
- [Sherlock OSINT Tool — Bellingcat Toolkit](https://bellingcat.gitbook.io/toolkit/more/all-tools/sherlock)
- [Sherlock: Find Usernames Across Social Networks — Medium/Twisted Circuits](https://medium.com/@twistedcircuits/sherlock-the-osint-tool-to-discover-usernames-bdac2d82b431)
- [Sherlock on Kali Linux](https://www.kali.org/tools/sherlock/)
- [Email Finder Benchmark 2025: 15 Tools, 20,000 Contacts — Dropcontact](https://www.dropcontact.com/email-finder-benchmark)
- [Best Email Finder Tools 2026 (Tested & Compared) — Prospeo](https://prospeo.io/s/best-email-finder-tools-2026)
- [Findymail vs Prospeo — Prospeo](https://prospeo.io/s/findymail-vs-prospeo)
- [LeadMagic — B2B Data API for AI Agents & GTM Engineers](https://leadmagic.io/)
- [LeadMagic B2B Data Enrichment API Documentation](https://leadmagic.io/docs/v1/introduction)
- [Hunter.io API Documentation](https://hunter.io/api-documentation)
- [Hunter.io Domain Search](https://hunter.io/domain-search)
- [Hunter.io API Review 2026 — Generect](https://generect.com/blog/hunter-io-api/)
- [How to Detect Any Website's Tech Stack: Wappalyzer and BuiltWith (2026)](https://pasqualepillitteri.it/en/news/2424/how-to-detect-website-tech-stack-wappalyzer-builtwith)
- [Technology Lookup Software Industry 2025–2026 — TechnologyChecker.io](https://technologychecker.io/blog/technology-lookup-software-industry-statistics-insights)
- [Wappalyzer — Official Site](https://www.wappalyzer.com/)
- [Hiring, Funding, and Tech Signals Explained — Landbase](https://www.landbase.com/blog/hiring-funding-and-tech-signals-explained)
- [How Tracking Job Postings Can Be a Game-Changer for Your GTM Strategy — Tapistro](https://www.tapistro.com/blog/how-tracking-job-postings-can-be-a-game-changer-for-your-gtm-strategy)
- [PredictLeads Job Openings Dataset for Sales & Market Intelligence](https://blog.predictleads.com/2026/04/29/predictleads-job-openings-dataset-sales-growth)
- [GTM in the Age of Signals — Maja Voje / GTM Strategist](https://knowledge.gtmstrategist.com/p/gtm-in-the-age-of-signals)
- [Forensically — Photo Forensics by Jonas Wagner](https://29a.ch/photo-forensics/)
- [Analyzing EXIF Metadata in Images for OSINT Geolocation Tracking — Siberoloji](https://www.siberoloji.com/analyzing-exif-metadata-in-images-for-osint-geolocation-tracking/)
- [Refloow Geo Forensics — Batch EXIF & Geolocation OSINT Tool](https://refloow.com/open-source-software/refloow-geo-forensics)
- [Image Metadata: The Hidden Data Inside Your Photos — Medium/Nikhil Patidar](https://medium.com/@nikhilpatidar01/image-metadata-the-hidden-data-inside-your-photos-osint-forensics-privacy-guide-a0c202003e09)
- [Reverse Image Search OSINT: Find Anyone by Photo (2025) — State of Surveillance](https://stateofsurveillance.org/articles/technical/reverse-image-search-osint-guide/)
- [Visual OSINT 2026: The Master Guide to Finding People by Photo — Social Searcher](https://www.social-searcher.com/2026/01/25/visual-osint-2026-the-master-guide-to-finding-people-by-photo/)
- [PimEyes — Reverse Image Search / Face Recognition](https://pimeyes.com/en)
- [Geolocation Tools — OSINT Handbook](https://www.osinthandbook.com/geolocation-tools)
- [Crowd-sourced Mapping Tools for OSINT Investigations — Dutch OSINT Guy](https://www.dutchosintguy.com/post/crowd-sourced-mapping-tools-for-osint-investigations)
- [The GTM Outreach Playbook: From Triggers to Demos — GTM Strategist](https://knowledge.gtmstrategist.com/p/the-gtm-outreach-playbook-from-triggers-to-demos)
- [Warm Outbound: A Guide to Signal-Based GTM — Demandbase](https://www.demandbase.com/blog/warm-outbound/)
- [Cold Email Laws: GDPR, CAN-SPAM, CCPA — Salesforge](https://www.salesforge.ai/blog/cold-email-laws)
- [GDPR, CAN-SPAM, and B2B Email List Compliance — Instantly.ai](https://instantly.ai/blog/b2b-email-list-compliance-gdpr-canspam/)
- [The Sales Leader's Guide to B2B Data Compliance (GDPR, CCPA) — UnifyGTM](https://www.unifygtm.com/explore/b2b-data-compliance-gdpr-ccpa)
- [Email Marketing Compliance in 2026: GDPR, CAN-SPAM & Privacy Laws — Hustler Marketing](https://www.hustlermarketing.com/email-marketing-compliance-in-2026-gdpr-can-spam-privacy-laws-explained/)
- [Best B2B Data Providers 2026: ZoomInfo vs Apollo vs People Data Labs — Starnus](https://starnus.com/blog/best-b2b-data-providers-zoominfo-apollo-pdl)
- [15 B2B Data Providers Tested on 1,000 Leads — Cleanlist](https://www.cleanlist.ai/blog/15-best-b2b-data-enrichment-providers-in-2025-ranked)
- [B2B Data Accuracy Report 2026: ZoomInfo vs Apollo vs Clearbit — Mindcase](https://mindcase.co/blog/b2b-data-accuracy-report-2026)
- [LinkedIn Sales Navigator Alternatives 2026 — Martal](https://martal.ca/linkedin-sales-navigator-alternatives-lb/)
- [LinkedIn Phone Lookup: How OSINT Enhances LinkedIn Networking — OSINT Industries](https://www.osint.industries/post/linkedin-phone-lookup-how-osint-enhances-linkedin-networking)
- [From ICP to Campaign: 15-Step Email Finder Workflow — Instantly.ai](https://instantly.ai/blog/from-icp-to-campaign-the-15-step-company-email-finder-workflow-for-5-replies/)
