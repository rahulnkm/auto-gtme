---
name: gtme-linkedin
description: Use to pull LinkedIn data (profiles, posts, people/company/job search, inbox, feed) and run outreach (connect, message) via the gtme-linkedin CLI. Prefer this over any LinkedIn MCP — it is far cheaper on context.
allowed-tools: Bash(gtme-linkedin *)
---

# gtme-linkedin

Run `gtme-linkedin <noun> <verb>`. Output is JSON on stdout; structured errors on stderr; exit codes: 0 ok, 2 usage, 3 not-found, 4 auth (run `gtme-linkedin auth login`), 5 conflict.

## Reads
- `gtme-linkedin person get <username> [--sections experience,posts]`
- `gtme-linkedin person search "<keywords>" [--location L] [--network F,S,O] [--company URN]`
- `gtme-linkedin person sidebar <username>` · `person me [--sections ...]`
- `gtme-linkedin company get <slug> [--sections ...]` · `company posts <slug>` · `company employees <slug>` · `company search "<kw>"`
- `gtme-linkedin job get <id>` · `job search "<kw>"`
- `gtme-linkedin inbox list [--limit N]` · `conversation get <thread>` · `conversation search "<q>"` · `feed get [--limit N]`

## Batches (use for 2+ prospects — saves your context)
Batchable reads: `person get`, `person sidebar`, `company get`, `company posts`, `company employees`, `job get`, `conversation get`.

Pipe a newline-separated list and read the output file — do NOT inline:
```
printf 'alice\nbob\n' | gtme-linkedin person get --batch -
```
Prints `{"written": ".gtme-linkedin/person-....jsonl", "count": 2}`. Read that file.
Use `--out PATH` to choose the output file, or `--stdout` to force inline JSONL.

## Writes (require explicit human go-ahead)
Dry-run by default — prints the intended action without sending. Add `--send` ONLY when the user has explicitly approved:
- `gtme-linkedin person connect <username> [--note "..."] [--send]`
- `gtme-linkedin message send <username> --body "..." [--send]`

## Auth
- `gtme-linkedin auth status` → `{"authenticated": true|false}`.
- `gtme-linkedin auth login` → opens a browser for the one-time interactive login (run by a human, not the agent).

## ⚠️ Version coupling with the LinkedIn MCP — read before bumping anything

The CLI and the LinkedIn MCP are the **same upstream package** (`linkedin-scraper-mcp`) and they share one state directory, `~/.linkedin-mcp/` — the login profile, the Patchright browser, and `browser-install.json`.

That last file carries a schema version, and upstream bumps it. If the MCP runs `@latest` while the CLI is pinned to an older release, the MCP rewrites the metadata to a schema the CLI does not recognise. The CLI then concludes the browser is not installed and drops into its auto-install path — which crashes, because upstream's `ensure_browser_installed()` calls `asyncio.run()` from inside a running loop.

**What that failure looks like, and why it misleads:**

```
Installing Patchright Chromium browser...
❌ Browser installation failed: asyncio.run() cannot be called from a running event loop
```

Every command fails this way, including `auth status` on a perfectly valid session. It reads like a broken CLI or a dead login. It is neither — the browser is installed and current, and the session is fine. The only thing wrong is one integer in a shared JSON file.

This happened on 2026-08-10: the metadata said `"version": 3`, the pinned `4.13.1` expected `2`, and the CLI had been dead since whenever the MCP last updated. `4.14.0` is the first release that reads schema 3.

**Rules:**

1. **Bump the CLI pin and the MCP together, or pin both.** They cannot be allowed to drift; there is no version negotiation between them, only a silent mismatch.
2. **Diagnose this failure at the metadata, not the traceback.** Compare `~/.linkedin-mcp/browser-install.json`'s `version` against `linkedin_mcp_server.bootstrap._INSTALL_METADATA_SCHEMA`. Reinstalling the browser will not help, because the install is not what is broken.
3. **`patchright install chromium` alone does nothing.** `configure_browser_environment()` points `PLAYWRIGHT_BROWSERS_PATH` at `~/.linkedin-mcp/patchright-browsers`; a default-path install lands in `~/Library/Caches/ms-playwright` where the check never looks.

**Verify a fix with a real call, never with the unit tests.** All 28 pass against a completely non-functional CLI, because the only test that touches a live session (`tests/test_smoke.py::test_person_me_live`) is marked `smoke` and deselected by default. Run it explicitly:

```bash
pytest tests -m smoke        # the one test that would have caught this
gtme-linkedin auth status    # {"authenticated": true}
```
