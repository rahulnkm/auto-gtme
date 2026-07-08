# gtme-linkedin

A thin, agent-grade CLI over [stickerdaniel/linkedin-mcp-server](https://github.com/stickerdaniel/linkedin-mcp-server)'s scraping logic. It exists to give an AI agent structured LinkedIn data — profiles, posts, search, inbox, feed, and outreach — without the context overhead of running that project's MCP server. One JSON object on stdout, structured errors on stderr, zero noise.

---

## Install

```bash
cd cli
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
```

## One-time auth

```bash
gtme-linkedin auth login    # opens a browser; log in once
gtme-linkedin auth status   # confirm: {"authenticated": true}
```

The session is stored in `~/.linkedin-mcp/profile` (the `li_at` cookie). It is never printed to stdout or stderr.

---

## Command reference

All commands follow `gtme-linkedin <noun> <verb> [args]`.

### person

| Command | Description |
|---|---|
| `person get <username> [--sections experience,posts,...]` | Scrape a person profile |
| `person search "<keywords>" [--location L] [--network F,S,O] [--company URN]` | Search people |
| `person sidebar <username>` | Fetch sidebar (related) profiles |
| `person me [--sections ...]` | Fetch the authenticated user's own profile |
| `person connect <username> [--note "..."] [--send]` | Send a connection request (dry-run unless `--send`) |

### company

| Command | Description |
|---|---|
| `company get <slug> [--sections ...]` | Scrape a company profile |
| `company posts <slug>` | Fetch a company's posts |
| `company employees <slug>` | Fetch a company's employees |
| `company search "<keywords>"` | Search companies |

### job

| Command | Description |
|---|---|
| `job get <id>` | Fetch a job posting |
| `job search "<keywords>"` | Search jobs |

### inbox / conversation / feed

| Command | Description |
|---|---|
| `inbox list [--limit N]` | List inbox threads |
| `conversation get <thread>` | Fetch a conversation thread |
| `conversation search "<query>"` | Search conversations |
| `feed get [--limit N]` | Fetch the LinkedIn feed |

### message

| Command | Description |
|---|---|
| `message send <username> --body "..." [--send]` | Send a DM (dry-run unless `--send`) |

### auth

| Command | Description |
|---|---|
| `auth status` | Report whether a session profile exists |
| `auth login` | Open a browser for one-time interactive login |

---

## Output contract

**Single result** (no `--batch`): one JSON object to stdout, exit 0.

**Batch** (batchable reads only): pass `--batch -` for stdin or `--batch FILE` for a newline-separated file. Results are written as JSONL to `./.gtme-linkedin/<noun>-<timestamp>.jsonl` by default (override with `--out PATH`). A pointer is printed to stdout:
```json
{"written": ".gtme-linkedin/person-20260529T120000.jsonl", "count": 2}
```
Pass `--stdout` to force the JSONL inline instead.

Batchable commands: `person get`, `person sidebar`, `company get`, `company posts`, `company employees`, `job get`, `conversation get`. Search, `me`, `inbox list`, and `feed get` are single-result only.

**Writes** (`person connect`, `message send`) are **dry-run by default**. Without `--send` they print the intended action and change nothing:
```json
{"action": "connect", "target": "alice", "note": "...", "would_send": true}
```
Add `--send` only when a human has explicitly approved. Never auto-add `--send`.

**Errors** go to stderr as a single structured JSON line:
```json
{"error": "<code>", "input": "<value>", "suggestion": "<next action>"}
```

**Exit codes:**

| Code | Meaning |
|---|---|
| 0 | OK |
| 1 | General error |
| 2 | Usage / bad arguments |
| 3 | Not found |
| 4 | Auth / session expired — run `gtme-linkedin auth login` |
| 5 | Conflict (reserved) |

---

## Architecture

Three modules carry all the logic:

- `gtme_linkedin/cli.py` — thin Click layer. No import of `linkedin_mcp_server`. Parses args, delegates to adapter, formats output.
- `gtme_linkedin/adapter.py` — **the only module that imports `linkedin_mcp_server`**. All upstream coupling lives here. If the upstream package changes, this is the only file that needs editing.
- `gtme_linkedin/format.py` and `gtme_linkedin/errors.py` — pure functions, no upstream dependency.

The upstream package is pinned (`linkedin-scraper-mcp==4.13.1` in `pyproject.toml`). `tests/test_adapter_contract.py` tests the adapter's expectations against the pinned version, so version drift is caught at the contract boundary before it can silently corrupt output.

---

## Maintenance

When a new upstream version is available:

1. Bump the pin in `pyproject.toml`.
2. Run `pytest tests/test_adapter_contract.py` — this is the canary.
3. If it fails, edit `gtme_linkedin/adapter.py` only to reconcile the new upstream interface.
4. Run the full suite: `pytest`.
5. Commit.

---

## Testing

```bash
pytest            # unit + contract tests; no network required (28 tests)
pytest -m smoke   # live smoke test; requires a logged-in LinkedIn session
```

---

## Credit

Built on [stickerdaniel/linkedin-mcp-server](https://github.com/stickerdaniel/linkedin-mcp-server), copyright Daniel Sticker, Apache-2.0. See `NOTICE`.
