---
name: gtme-icp
description: Use after gtme-context, when a context.json exists and you need to define who the seller should target — before building a list. Triggers include "define the ICP", "who should we target", or the second step of an auto-gtme run.
---

# gtme-icp

## Overview

Turn the seller's `context.json` into a **machine-filterable ICP** plus a **human-editable review gate**. An ICP a person can only read is not done — `gtme-list` runs boolean filters, so the ICP must be structured data, not prose.

You already know how to *reason* about an ICP (tiers, intent-over-firmographics, disqualifiers). This skill's job is the **contract**: fixed schema, canonical field names, signal IDs from the taxonomy, and the review gate. Don't invent field names — downstream skills depend on these exact keys.

## When to Use

- After `gtme-context`, before `gtme-list`
- Input: `runs/<slug>/context.json`. Output: `runs/<slug>/icp.md` (editable) → `icp.json` (machine)
- Re-run when the seller pivots or a run's reply data suggests ICP drift (`gtme-measure` triggers this)

## The review gate (non-negotiable — this is the wedge over Gojiberry)

1. Generate `icp.md` — prose rationale + a single fenced ```yaml block holding all machine fields.
2. **STOP. Tell the user to edit the yaml block** in `icp.md` (tighten size, swap verticals, add disqualifiers).
3. On `confirm`, parse the yaml block → `icp.json`, set `status: confirmed`. Never build a list off an unconfirmed ICP.

The user edits *one yaml block*, not scattered prose. That keeps edits machine-parseable.

## icp.md structure

````markdown
# ICP — <seller>

**Core thesis:** <one sentence: who hurts + who can act fast>

<short prose rationale — this is context for the human reviewer, ignored by the parser>

```yaml
# EDIT THIS BLOCK. Everything below is what the pipeline reads.
tiers:
  - tier: 1
    allocation: 0.7
    firmographics:
      company_type: [b2b-saas, dev-tools, ai-native]
      employee_count: {min: 50, max: 400}
      sub_team: {metric: engineers, min: 15, max: 120}   # the team that feels the pain
      stages: [series-a, series-b]
      last_raise_months: 18
      geos: [US, CA, UK, EU, IL, AU]
    technographics:
      uses: [jira, shortcut, asana]     # incumbent to displace
      ai_native: true
    watch_signals: [job_posting_intent, li_hiring_spike, li_problem_post, funding_raised, tech_stack_change]
disqualifiers:
  sub_team: {exclude_below: 8, exclude_above: 500}
  company_type_excluded: [agency, consultancy, non-software]
  segment_excluded: [regulated-enterprise, pre-seed-no-eng]
personas:
  - role: economic_buyer
    titles: [VP Engineering, CTO, Head of Engineering, Founder]
    cares_about: [team velocity, shipping speed]
  - role: champion
    titles: [Engineering Manager, Staff Engineer, Head of Product]
    cares_about: [dev experience, tracker noise]
    first_touch: true          # highest-converting first contact
contacts_per_account: 2        # one buyer, one champion
score_hint:
  weight_signals_over_firmographics: true   # timing beats fit in cold outbound
```
````

## Rules

| Rule | Why |
|---|---|
| Canonical keys only (schema above) | `gtme-list` + `gtme-score` read these exact keys; new names break them silently |
| `watch_signals` use signal IDs from the taxonomy | Same vocabulary as `context.json`; no invented strings (`li_hiring_spike`, not `hiring_surge`) |
| Disqualifiers as machine filters, not prose | `gtme-list` must be able to `exclude_above: 500`, not parse "too big" |
| `sub_team` separate from `employee_count` | The team that feels the pain (engineers) ≠ total headcount — the sharpest filter |
| Always emit `icp.md` and STOP for review | Building on an unconfirmed ICP wastes enrichment credits on the wrong accounts |
| Carry `score_hint` forward | Encodes the intent-over-firmographics judgment as data `gtme-score` consumes |

## Signal ID vocabulary (use these exact strings for watch_signals)

```
li_job_change li_promotion li_post_engaged_ours li_post_engaged_competitor li_follow_ours
li_new_hire_persona li_hiring_spike li_problem_post li_group_activity li_profile_visit
web_visit_deanon job_posting_intent tech_stack_change content_downloaded intent_provider pricing_page_visit
funding_raised product_launch press_mention new_exec_hire layoff_or_expansion
x_engaged_ours x_engaged_competitor x_follow_ours x_problem_post x_event_engagement
podcast_guest event_speaker github_star_category newsletter_subscribe
```
`watch_signals` is the subset this ICP's accounts realistically throw. No invented strings.

## Two contract rules the schema alone doesn't state

**`sub_team.metric` is an open role-department label, not an enum.** It names *whichever team feels the pain* — `engineers` for a dev tool, `gtm_headcount` for a CRM, `marketing` for an ad tool. `gtme-list` resolves it to a headcount filter (via job-title counts on LinkedIn). Pick the sharpest pain-team; don't force it into a fixed list.

**Disqualifier precedence: global gate first, then tiers.** `gtme-list` applies `disqualifiers` as a hard filter across the *entire* pulled universe first — any account failing any disqualifier is dropped regardless of tier fit. Surviving accounts are then sorted into tiers. So keep tier `sub_team` ranges *inside* the disqualifier range; a tier can be narrower, never wider.

## Common Mistakes

- Emitting a final ICP with no review gate → build starts on a wrong ICP. Always STOP at `icp.md`.
- Prose disqualifiers ("mid-market and up") → not filterable. Encode min/max/enum.
- Inventing per-run field names → downstream can't read them. Schema is fixed.
- Collapsing `sub_team` into `employee_count` → loses the highest-value filter.

## Next

`gtme-list` reads confirmed `icp.json` → over-pulls the universe → filters to the TAM map.
