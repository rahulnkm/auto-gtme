# auto-gtme

**Signal-based GTM automation, as a Claude Code skill suite.** An open-source, agent-native, self-hosted take on the modern outbound stack (Clay / Gojiberry-style motion) — run entirely inside Claude Code, where you control the data and edit the logic by editing markdown.

> **What this is (and isn't).** These are **skills** — structured methodology + agent instructions + fixed data contracts, not a turnkey SaaS. Each skill is a step an AI agent runs, reading the prior step's artifact and writing the next. You bring your own tools and API keys; the skills orchestrate them. There is no hosted service and nothing runs on its own.

## The pipeline

From a company website to a reviewed, dry-run send plan — with human gates at the decisions that matter:

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

## Design principles

- **The map before the signal.** A buying signal is noise until it lands on an account you already wanted. Build the TAM first.
- **Never fabricate.** No guessed emails, no invented contacts, no hallucinated personalization. Missing data hard-stops honestly rather than making something up.
- **Dry-run by default.** Nothing sends without an explicit human action. The plan is the product; the send is your call.
- **Editable by markdown.** Change how ICP scoring or message-writing works by editing a skill file — no code deploy.
- **Contracts between steps.** Each skill has a fixed input/output artifact, so steps compose and any agent can resume a run.

## Integrations (bring your own keys)

The skills orchestrate tools you provide; they are adapters, wired by you:

- **LinkedIn** — via the LinkedIn MCP (`mcp__linkedin__*`) for read + `confirm_send`-gated messaging
- **X** — via a terminal X client (read/reply/follow)
- **Email** — SMTP or Instantly/Smartlead adapter (specced; wire your own)
- **Enrichment** — LeadMagic / Findymail / Prospeo / PDL waterfall + a validation provider
- **Signals** — Firecrawl, Ashby/Greenhouse ATS, Crunchbase, BuiltWith, RB2B, PullPush
- **Inbound** — Postiz (publishing) + ManyChat (compliant comment-to-DM)

Where a tool isn't wired, the relevant stage reports `blocked` and stops — it does not fake output.

## Status

Actively evolving. The pipeline runs end-to-end today; several integration adapters are specced and awaiting your keys. Contributions and issues welcome.

## License

MIT — see [LICENSE](LICENSE). Built on the tradecraft of the operators credited in the research dossier under `research/`.
