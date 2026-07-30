---
name: gtme-publish
description: Use when running the inbound content funnel — publishing content that attracts ICP engagement to manufacture buying signals. Triggers include "schedule content", "run the content engine", "publish posts", "the inbound funnel", or the publish step of an auto-gtme run.
---

# gtme-publish

## Overview

Manufacture the highest-converting signal instead of only waiting to detect it. Publish **pain-mapped content** via Postiz across channels; the ICP members who engage self-select as feeling the pain, and their engagement becomes a scored `li_post_engaged_ours` / `x_engaged_ours` signal tied to a named person. This is the inbound half of the funnel Gojiberry doesn't have.

Output: `runs/<slug>/publish/content_plan.jsonl` (scheduled) → `publish/published.jsonl` (live, with post IDs the signal step watches), plus the standard folder companions `provenance.md` and `decisions.md`.

## When to Use

- In parallel with outbound — the content engine runs on a weekday cadence; founder-led posting floor ≈ 5 posts/week (fin465, YC outbound playbook)
- Input: `context/context.json` (products' metrics/evidence) + `market/market-pain.json` (pain keywords + market stats) — honor `write/guardrails.json` if it exists, ICP; plus `offer.json` **opportunistically** — publish forks off context.json before the offer exists, so if a confirmed offer is present, content CTAs use its named front-end offers (they *are* lead magnets, research/11 §8.6); if absent, proceed as normal
- Feeds `gtme-signals` (engagers on your posts) and `manychat` (comment-to-DM capture)

## Pain-mapped content discipline

**Each post targets exactly one `pain_keyword`** so the people who engage are self-identifying as feeling that pain — that's what makes the engagement a *qualified* signal, not vanity reach. Generic brand content attracts no usable signal. Name the specific pain, tell on the symptom, end with a question that pulls a comment. Not a product pitch — bait mapped to a pain.

**Strongest bait format: "free AI training that gets you [ICP outcome]"** — a demo-in-disguise with VSL structure: teach the implementation, be the bridge to doing it (codyschneider). Teaching-first self-selects better-qualified engagers than pitching-first. Pairs with comment-to-DM below: the training is the keyword-gated deliverable.

## Lead-magnet format — ungate it, make it interactive

- **Satellite apps beat gated PDFs** (Verna, Lovable): a small interactive tool is the magnet, and its *usage* is exactly the engagement signal this skill exists to manufacture.
- **Ungate everything, LLM-readable** (Kramer): LLMs harvest your content regardless, so structured ungated pages cost nothing and get you cited as the answer in ChatGPT/Perplexity — AEO (answer-engine optimization), an emerging inbound channel to watch, not yet a pipeline stage.

## Event → content loop

A conference cycle is a content mine (fin465): film ~5 casual customer Q&As on-site → 15–20 captioned clips → drip one every couple of days for ~a month, reusing clips to promote the next event. Feeds the weekday cadence as a supply source.

## The publish gate

Public content under the seller's brand is permanent and reputational. **Do not auto-publish.** Schedule as draft / dry-run the Postiz call; a human approves before anything goes live. Same spirit as `gtme-sequence`'s dry-run rule — lighter cadence, same gate.

## The signal linkage (the load-bearing wiring)

A published post is useless to the pipeline unless its engagement is captured. On publish, record the `postiz_id` **and the live post URL**, set `engagement_watch: true`. `gtme-signals` then watches that specific post for engagers (`li_post_engaged_ours` / `x_engaged_ours`), resolves each to a person/company, and fires the signal onto the TAM. The reply later references the exact post they engaged — outreach as continuation, not cold hit.

**Without the post_id → signal-watch linkage, this is just social scheduling.** The linkage is the point.

## ManyChat comment-to-DM (compliant IG/FB/WhatsApp capture)

For channels where cold DM is blocked (Instagram/Facebook/WhatsApp), attach a **comment-to-DM trigger**: the post invites a keyword comment, ManyChat auto-DMs the commenter. Because the prospect commented first, it's opt-in and Meta-TOS-safe — the only compliant path to those channels. Set `comment_to_dm.keyword` + `manychat_flow`; the commenter enters the capture flow, then routes into `gtme-signals` as inbound.

## Postiz integration

- Base: cloud `https://api.postiz.com/public/v1` · self-host `{BACKEND_URL}/public/v1`. Auth `Authorization: Bearer $POSTIZ_API_KEY`.
- `GET /integrations` → channel integration IDs. `POST /posts` → schedule (`{type, date, posts:[{integration:{id}, value:[{content}]}]}`). `POST /upload` media first (50MB cap).
- One `posts` array can fan across channels (each entry its own `integration.id`), or loop per post per date. Rate: 90 posts/hr.
- No MCP → thin CLI wrapper (cli > API > MCP cascade).

## content_plan.jsonl schema (fixed)

```json
{"post_id": "local-001", "channel": "linkedin", "pain_mapped": "salesforce too complex",
 "content": "Your RevOps team spends more time administering Salesforce than closing deals...",
 "scheduled_date": "2026-07-08T14:00:00Z",
 "comment_to_dm": {"enabled": false, "keyword": null, "manychat_flow": null},
 "postiz_id": null, "post_url": null, "status": "draft", "engagement_watch": true}
```

- `status` — `draft | scheduled | published`. `postiz_id` + `post_url` fill on publish (after human approval).
- `scheduled_date` — a **proposed** slot; approval confirms or shifts it. Not binding until `status: scheduled`.
- `engagement_watch` — `true` tells `gtme-signals` to monitor this post's engagers.
- `manychat_flow` — a ManyChat flow **name that must already exist** in the connected ManyChat account; `gtme-publish` references it, doesn't create it.

**Pain → post mapping:** one `pain_keyword` per post; rotate through the keywords across the weekday cadence (keywords usually outnumber a day's posts). When `measure.json` exists, lead the cadence with the pain whose signal has the highest book-rate.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Generic brand content | One `pain_keyword` per post; engagers must self-select. |
| Auto-publishing | Human approves before live; content is permanent. |
| Publishing without the signal linkage | Record `postiz_id` + `post_url`, `engagement_watch: true` — else it's just scheduling. |
| Cold DM on IG/FB/WA | Use `comment_to_dm` (opt-in) via ManyChat; cold is blocked. |
| Pitchy posts | Bait a pain, end on a question — not a product ad. |

## Next

`gtme-signals` watches `engagement_watch` posts → engagers become signals on the TAM → the inbound funnel feeds the same score/write/sequence spine as outbound.
