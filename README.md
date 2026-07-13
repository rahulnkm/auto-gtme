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
  └─ gtme-context   → who the seller is (product, wedge, proof)
      └─ gtme-icp    → who to target        ★ human gate (edit the ICP)
          └─ gtme-list    → the account universe (TAM)
              ├─ gtme-signals → buying intent, fired onto the TAM (30-signal reference)
              └─ gtme-enrich  → validated contacts (waterfall + validation)
                  └─ gtme-score  → rank + route (fit × decayed-signal)
                      └─ gtme-research → per-account personalization hooks
                          └─ gtme-write  → signal-anchored copy   ★ human gate (review messages)
                              └─ gtme-sequence → multi-channel plan   ★ human gate (dry-run; you send)
                                  └─ [you send] → gtme-measure → learns → feeds back into icp/score

gtme-publish runs in parallel: inbound content that manufactures the engagement signal.
Cross-cutting: auto-gtme (orchestrator), gtme-why (purpose gate), gtme-handoff (resume state).
```

## The 13 skills + orchestrator

| Skill | Does |
|---|---|
| `auto-gtme` | Orchestrator — chains the pipeline from a URL, enforces the human gates |
| `gtme-context` | Website → structured seller context |
| `gtme-icp` | Context → machine-filterable ICP (with a human review gate) |
| `gtme-list` | ICP → the TAM account map |
| `gtme-signals` | 30-signal detection fired onto the TAM (+ `detectors.md` method reference) |
| `gtme-enrich` | Waterfall enrichment + contact validation — never fabricates a contact |
| `gtme-score` | Rank + route: fit × decayed-signal, with a learning-prior layer |
| `gtme-research` | Per-account hooks — true, dated, never hallucinated |
| `gtme-write` | Signal-anchored copy per channel — anti-slop, direction-aware |
| `gtme-sequence` | Multi-channel orchestration — **dry-run by default, sends are human-gated** |
| `gtme-measure` | Book-rate learning loop feeding back into ICP + scoring |
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

## Contribution — collaborators wanted

I'm actively looking for collaborators — individuals and companies alike. Use it, star it, fork it, build on top of it. If you add a channel connector, a signal detector, or a playbook your business needed, PR it back: that's how this gets better — operators contributing the pieces their own pipelines demanded.

Companies are explicitly welcome to adopt auto-gtme as their in-house GTM stack and extend it commercially.

## License

MIT — see [LICENSE](LICENSE). Built on the tradecraft of the operators credited in the research dossier under `research/`.
