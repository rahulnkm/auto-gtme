# auto-gtme

**Signal-based GTM automation as Claude skills.** An open-source, self-hosted take on the modern AI outbound stack — run entirely inside Claude Code, where you control the data and edit the logic by editing markdown.

## Why this exists

Agentic GTM SaaS platforms **rent** you your own pipeline.

$99+/month (and usually MUCH more) to run ICP-to-outbound on *their* cloud, on *their* roadmap, with *their* standard signals — the same signals every one of your competitors is using. 

- Need a channel they don't support? *Feature request.*
- Hit a bug? *Support queue, wait a week.*
- The platform gets acquired, repriced, or dies? *That's your revenue engine they took with them.*

That trade made sense when building this in-house took an engineering team. 

But _AI agents flipped that math_ — extending and repairing software takes minutes now.

And GTM is the *worst* category to rent, because go-to-market is a game of **speed** and **personalization**:

- **Speed:** the team that adds a channel, a signal, or a workflow the same day they think of it beats the team waiting on a vendor's dev timeline. Something breaks? Tell your AI; it's fixed in minutes, not a ticket-week.
- **Personalization:** your best signals are discoveries about *your* ICP that no platform ships. Standard signals are everyone's signals. Here, you just add yours — and they compound.

The code that runs communication with your customers **should be code you own**: self-hosted, on your laptop or your own cloud, extensible in any direction, immune to vendor lock-in. 

## The pipeline

Drop your company website and a get a reviewed, dry-run GTM plan — with human gates at the moments that matter:

```
website
  └─ gtme-company   → who the seller is (product, wedge, proof)
      └─ gtme-market-pain → what the market hurts about, in buyers' own words + the go/no-go
          └─ gtme-icp    → who to target        ★ human gate (edit the ICP + the pain map)
              └─ gtme-offer  → what we're offering them   ★ human gate (the grand-slam test)
                  └─ gtme-sequence → the SHAPE of the campaign: which messages, what order,
                      │              what happens on a reply   ★ human gate (confirm the arc)
                      └─ gtme-list    → the account universe (TAM), capped by the sequence's volume ceiling
                          ├─ gtme-signals → buying intent, fired onto the TAM (30-signal reference)
                          └─ gtme-enrich  → validated contacts (waterfall + validation)
                              └─ gtme-score  → rank + route (fit × decayed-signal), accounts and contacts
                                  └─ gtme-research → per-account personalization hooks
                                      └─ gtme-write  → fills each touch of the arc, per contact  ★ human gate (review messages)
                                          └─ gtme-send → real timestamps, caps, identity gates  ★ human gate (dry-run; you send)
                                              └─ [you send] → gtme-measure → feeds back into pain map/icp/offer/score/templates

gtme-publish runs in parallel: inbound content that manufactures the engagement signal.
Cross-cutting: auto-gtme (orchestrator), gtme-why (purpose gate), gtme-handoff (resume state).
```

**The sequence is chosen before the list is pulled and before a word is written.** How many touches times how many contacts, against the daily sending cap, is what actually bounds list size — so the shape has to exist before the list does. And a writer cannot hit a beat nobody has told them about, so touch 2 knows what it is *for* before anyone drafts it.

Every stage writes into its own folder under `runs/<slug>/<stage>/`: the machine artifact, a `provenance.md` of numbered citations (verbatim quote, link, dates), and a `decisions.md` of what was decided and why. Artifacts are checked against a JSON Schema before they hand off (`python3 skills/validate.py runs/<slug>`), so a stage fails loudly rather than passing a misshapen file to the next one. Artifacts hold data only — no rationale, no revision history — so a founder can skim one without reading an AI's working notes. Before any artifact reaches a human gate or the next stage, it goes through a fixed review pass: eight parallel reviewers, each on a distinct lens, all answering the one question that stage's skill defines. A clean review never skips a human gate.

## The 16 skills + orchestrator

| Skill | Does |
|---|---|
| `auto-gtme` | Orchestrator — chains the pipeline from a URL, enforces the human gates |
| `gtme-company` | Website → the seller fingerprint: who they are, what they sell, the pain each feature kills, who they already know |
| `gtme-market-pain` | Public voice-of-customer → a cited pain map in buyer language, plus `market_verdict`: the pipeline's power to refuse a dying market |
| `gtme-icp` | Company + pain map → machine-filterable ICP (with a human review gate) |
| `gtme-offer` | ICP → the human-gated grand-slam offer: problems→solutions stack, guarantee, honest scarcity, front-end slice, tier |
| `gtme-list` | ICP + offer tier → the TAM account map, capped by the sequence's volume ceiling |
| `gtme-signals` | 30-signal detection fired onto the TAM (+ `detectors.md` method reference) |
| `gtme-enrich` | Waterfall enrichment + contact validation — never fabricates a contact |
| `gtme-score` | Rank + route: fit × decayed-signal, with a learning-prior layer (+ `score.py`, the runnable reference formula) |
| `gtme-research` | Per-account hooks — true, dated, never hallucinated |
| `gtme-write` | Fills each touch of the confirmed arc per contact — signal-anchored, anti-slop |
| `gtme-sequence` | The campaign's shape, chosen before the list: a reusable template bound to this run's pains, objections and offer, as a graph of what gets sent when and what a reply changes |
| `gtme-send` | Materializes the plan — real timestamps, daily caps, identity gates, channel adapters. **Dry-run by default, sends are human-gated** |
| `gtme-measure` | Book-rate learning loop feeding back into ICP, scoring, and the pain map — every message carries the `pain_id` it tests, so a reply confirms or kills a specific evidenced claim |
| `gtme-publish` | Inbound content funnel (Postiz) that manufactures the engagement signal |
| `gtme-why` | Purpose gate — refuses a well-built campaign pointed at nothing |
| `gtme-handoff` | Snapshot run state for resume across sessions/agents |

## Connectors

Channel adapters live in `connectors/`, separate from the core pipeline skills — the pipeline stays channel-agnostic and calls whatever connectors you've wired:

| Connector | Does |
|---|---|
| `gtme-linkedin` | LinkedIn read (profiles, companies, jobs, inbox, feed) + `--send`-gated outreach, wrapping the typed CLI in `cli/gtme_linkedin` |

## Design principles

- **Never fabricate.** No guessed emails, no invented contacts, no hallucinated personalization. Missing data hard-stops honestly rather than making something up.
- **Every claim is clickable.** Pains, stats, and hooks carry numbered citations in a `provenance.md` next to the artifact — verbatim quote, link, published date, pulled date. A number a prospect can refute is worse than no number.
- **Contracts between steps.** Each skill has a fixed input/output artifact, so steps compose and any agent can resume a run.
- **Levels of self-driving.** The user determines how much automation they want — from nothing sends without an explicit human action to complete automation.
- **Editable by markdown.** Change how ICP scoring or message-writing works by editing a skill file.

## Integrations (bring your own keys)

The skills orchestrate tools you provide; they are adapters, wired by you:

- **Email** — SMTP or Instantly/Smartlead adapter (specced; wire your own)
- **LinkedIn** — the `connectors/gtme-linkedin` skill wrapping the bundled typed CLI (`cli/gtme_linkedin`), read + `--send`-gated messaging; LinkedIn MCP (`mcp__linkedin__*`) as fallback
- **Inbound** — Postiz (publishing) + ManyChat (compliant comment-to-DM)
- **X** — via a terminal X client (read/reply/follow)
- **Enrichment** — LeadMagic / Findymail / Prospeo / PDL waterfall + a validation provider
- **Signals** — Firecrawl, Ashby/Greenhouse ATS, Crunchbase, BuiltWith, RB2B, PullPush

Where a tool isn't wired, the relevant stage reports `blocked` and stops — it never fakes output.

## Roadmap

The mission extends beyond outbound into a **unified comms stack**: one engine, one context, every funnel.

- **Content creation** — manage inbound campaigns in the same pipeline that knows your outbound
- **DM funnels** — comment-to-DM conversation flows, owned end-to-end, extending ManyChat
- **Paid UGC + influencer campaigns** - connect to UGC and influencer marketing campaigns
- **Cohesive campaigns in one command** — outbound and content timed to the same live event, updated together, because one AI system holds context across it all

## Status

The pipeline runs end-to-end today; testing and improvements are ongoing.

## Running the checks

```bash
pip install -r requirements.txt
pytest skills/tests
python3 skills/validate.py runs/<slug>
```

`skills/tests/fixtures/example-run/` is a committed example run — a real run with its structure kept and its content replaced, so the schema tests exercise every field while naming nobody. Real runs live under `runs/`, which is gitignored; a few checks pick those up automatically when present and skip when they aren't.

## Contribution — collaborators wanted

I'm actively looking for collaborators — individuals and companies alike. Use it, star it, fork it, build on top of it. If you add a channel connector, a signal detector, or a playbook your business needed, PR it back: that's how this gets better — operators contributing the pieces their own pipelines demanded.

Companies are explicitly welcome to adopt auto-gtme as their in-house GTM stack and extend it commercially.

## License

MIT — see [LICENSE](LICENSE). Built on the tradecraft of the operators credited in the research dossier under `research/`.
