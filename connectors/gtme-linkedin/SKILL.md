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
