---
name: gtme-context
description: Use when starting a GTM run from a company website — the first step before defining an ICP, building a list, or writing outreach. Triggers include a URL handed in as the campaign starting point, "build context from this site", or `auto-gtme init --website`.
---

# gtme-context

## Overview

Turn one company website into a structured, machine-readable **context pack** that every downstream skill consumes. This is the entry point of the auto-gtme pipeline.

**The frame is fixed and non-negotiable:** the input website is **the user's OWN company** (the seller). The context pack describes *what the seller sells and to whom* — so `gtme-icp` can define *who the seller should target*, and `gtme-write` can personalize using the seller's proof points. Never confuse "context about the seller" with "an ICP." This skill produces the former; `gtme-icp` produces the latter.

## When to Use

- First step of any run — a website URL is the only required input
- Before `gtme-icp`, `gtme-list`, or any outreach
- Re-run when the seller's positioning/product changes

Not for: profiling a *target* account (that's `gtme-research`).

## Core output — write exactly this schema

Persist to `runs/<company-slug>/context.json`. Every field present; use `null` + `"unknown"` provenance when a value can't be found. Do NOT invent a schema.

```json
{
  "company": "Attio",
  "domain": "attio.com",
  "category": "AI-native CRM",
  "one_liner": "The AI CRM that builds pipeline and compounds revenue.",
  "what_they_sell": ["flexible CRM data model", "AI workflow agents", "call intelligence"],
  "value_props": ["anti-Salesforce flexibility", "agents work 24/7", "sub-50ms at scale"],
  "buyer_personas": [
    {"label": "economic buyer", "titles": ["Founder", "CEO", "COO"], "cares_about": ["revenue visibility", "no RevOps headcount"]},
    {"label": "champion", "titles": ["Head of Revenue", "RevOps Lead"], "cares_about": ["pipeline health", "clean data"]}
  ],
  "pain_keywords": ["salesforce too complex", "manual lead enrichment", "crm data entry", "renewals slipping"],
  "competitors": [
    {"name": "Salesforce", "domain": "salesforce.com", "linkedin": "salesforce", "x": "salesforce", "relation": "displaces"},
    {"name": "Clay", "domain": "clay.com", "linkedin": "clay-hq", "x": "clay_hq", "relation": "adjacent"}
  ],
  "proof_points": [
    {"customer": "Granola", "metric": "83% faster lead triage", "claim": "cut triage time"},
    {"customer": "Passionfroot", "metric": "25% revenue boost", "claim": "grew revenue"}
  ],
  "candidate_signals": [
    {"signal": "funding_raised", "why": "newly funded co has budget + scaling pain"},
    {"signal": "li_new_hire_persona", "why": "new RevOps hire = mandate to fix CRM"},
    {"signal": "tech_stack_change", "why": "dropping Salesforce = active buying window"}
  ],
  "firmographic_hints": {"size_range": "10-200", "stages": ["seed", "series-a", "series-b"], "verticals": ["b2b-saas", "plg"]},
  "provenance": {"company": "verified", "domain": "verified", "funding": "crunchbase", "firmographic_hints": "inferred"}
}
```

## Extraction technique

1. **Scrape** the homepage + `/product`, `/customers`, `/pricing`, `/about` via Firecrawl (or WebFetch fallback). Pull funding/headcount from Crunchbase.
2. **pain_keywords** — convert every pain into a *short searchable phrase* a prospect would actually type or post (feeds `gtme-signals` problem-post detection). Not sentences.
3. **competitors** — resolve each to `{name, domain, linkedin, x, relation}`. These are scrape targets for competitor-engagement signals; a bare name is useless downstream.
4. **proof_points** — structure as `{customer, metric, claim}` so `gtme-write` can drop them into messages verbatim.
5. **candidate_signals** — map trigger events to signal IDs from the **fixed vocabulary below**, never invented strings. `gtme-signals` matches these IDs exactly; a typo (`hiring_surge` vs `li_hiring_spike`) breaks the pipeline silently.
6. **provenance** — a flat map keyed by **top-level field name only** (not per-array-item). Value = `verified` (seen on their site or Crunchbase), a source name (`crunchbase`), or `inferred`. `competitors` is **expected to be `inferred`** — companies don't list rivals on their own site; inferring them from outside knowledge is correct, not a violation. Outreach built on inferred-as-fact is a reputation risk, so mark honestly.

### Signal ID vocabulary (use these exact strings for candidate_signals)

```
LinkedIn: li_job_change li_promotion li_post_engaged_ours li_post_engaged_competitor
          li_follow_ours li_new_hire_persona li_hiring_spike li_problem_post
          li_group_activity li_profile_visit
Web/tech: web_visit_deanon job_posting_intent tech_stack_change content_downloaded
          intent_provider pricing_page_visit
Company:  funding_raised product_launch press_mention new_exec_hire layoff_or_expansion
X:        x_engaged_ours x_engaged_competitor x_follow_ours x_problem_post x_event_engagement
Media:    podcast_guest event_speaker github_star_category newsletter_subscribe
```
Full definitions in `docs/build/signals-channels-doctrine.md` Part 1.

## Common Mistakes

| Mistake (seen in baseline) | Fix |
|---|---|
| Hedging "sell TO them vs. use as ICP model" | Input site = the SELLER. Always. Produce seller context, not an ICP. |
| Proposing a schema at the end | Emit the fixed schema above from the start; persist to `context.json`. |
| Pain points as prose | `pain_keywords[]` = short searchable phrases. |
| Competitors as a prose list | `competitors[]` = named entities with domain + handles. |
| Proof stats buried in tables | `proof_points[]` = `{customer, metric, claim}`. |
| Trigger events as prose | Map to `candidate_signals[]` using real signal IDs. |
| Verified and guessed fields blurred | `provenance` map on every non-obvious field. |

## Next

`gtme-icp` reads `context.json` → defines who to target. Never skip context; an ICP without seller context is vibes.
