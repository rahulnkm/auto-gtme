---
name: gtme-linkedin
description: Use to pull LinkedIn data (profiles, posts, people/company/job search, inbox, feed) and run outreach (connect, message) via the LinkedIn MCP. Covers the read spine for gtme-list and gtme-enrich and the softest first touch for gtme-send.
allowed-tools: mcp__linkedin__*
---

# gtme-linkedin

LinkedIn runs on the **LinkedIn MCP** (`mcp__linkedin__*`). Configure it in `.mcp.json`:

```json
{"mcpServers": {"linkedin": {"command": "uvx", "args": ["linkedin-scraper-mcp@latest"],
  "env": {"UV_HTTP_TIMEOUT": "300"}}}}
```

Auth is a one-time interactive browser login handled by the MCP server itself, and it is a human step. If reads return an auth error, stop and say so — never fabricate a profile or a contact to keep moving.

## Reads

| Need | Tool |
|---|---|
| One person | `get_person_profile` |
| Your own profile | `get_my_profile` |
| Find people | `search_people` |
| "People also viewed" | `get_sidebar_profiles` |
| One company | `get_company_profile` (`sections: "posts,jobs"` for more) |
| Company posts | `get_company_posts` |
| Company headcount by function | `get_company_employees` |
| Find companies | `search_companies` |
| Jobs | `search_jobs` → `get_job_details` |
| Inbox / threads | `get_inbox`, `get_conversation`, `search_conversations` |
| Home feed | `get_feed` |

## ⚠️ Context cost is the binding constraint

**There is no batch mode.** Every response lands in the agent's context in full, and a single `get_company_posts` call can run to several thousand words. This is the one place the MCP is materially worse than a CLI, and it is not a small difference — sweeping 50 accounts will exhaust a context window before the stage finishes.

Rules that follow from that:

1. **Never sweep the full TAM.** Ration LinkedIn reads to accounts that have already earned them — `route: send` after `gtme-score`, or the tier-1 set in `gtme-research`.
2. **Pull the narrowest tool that answers the question.** `get_company_profile` without `sections` is far cheaper than with `posts,jobs`.
3. **Extract, then discard.** Take the dated hooks you need into the stage artifact on the first pass. Re-reading a profile because the finding was never written down pays the context twice.
4. **If a stage genuinely needs LinkedIn across hundreds of accounts, that stage needs a different source.** Say so and stop rather than burning the window; `gtme-list` supplements (Serper, Firecrawl, theorg.com) exist for exactly this.

## Writes — require explicit human go-ahead

Both write tools reach a real person from Rahul's real account. The account is job-hunt-critical; a rate-limit block or a spam flag is not recoverable in the timeframe that matters.

**`send_message`** takes a required `confirm_send` boolean. It must be `true` to send, so leaving it `false` is a genuine dry run.

**`connect_with_person` has no such flag.** It is annotated `destructiveHint`, which makes the *client* prompt — the agent does not have to opt in the way `--send` once forced. Treat that as weaker, not equivalent, and impose the gate yourself: never call it without an explicit, in-conversation human approval naming the person.

Rate-limit both. LinkedIn connection requests carry a weekly ceiling, and it is the binding cap on sequence volume — see `05-sequence/sequence.json volume_ceiling`.

## Session

`close_session` releases the browser the MCP drives. Call it when a long read pass finishes.

## History

A typed `gtme-linkedin` CLI previously wrapped this surface and was removed on 2026-08-10. It had a real advantage — `--batch` wrote JSONL straight to disk and kept large pulls out of context — but it could not run: `_run_browser_setup` called `asyncio.run()` from inside an existing event loop, so every command failed at browser startup, including `auth status` on a valid session. Its 28 unit tests passed throughout, because the only test that touched a live session (`test_smoke.py::test_person_me_live`) was marked `smoke` and deselected by default.

The lesson generalizes past LinkedIn: **a connector's test suite must exercise at least one real call in CI, or it certifies a surface that does not work.**
