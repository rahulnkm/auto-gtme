import sys
from datetime import datetime, timezone
from pathlib import Path

import click

from . import adapter
from .adapter import LinkedInSession
from .errors import EXIT_USAGE, GtmeError
from .format import error_line, to_json, to_jsonl


def _fail(err: GtmeError) -> None:
    click.echo(error_line(err.payload()), err=True)
    sys.exit(err.exit_code)


def _emit_single(result: dict) -> None:
    click.echo(to_json(result))


def run_write(action: str, target: str, send: bool, dry_payload: dict, do):
    if not send:
        _emit_single({"action": action, "target": target, **dry_payload, "would_send": True})
        return
    try:
        with LinkedInSession() as s:
            _emit_single(do(s))
    except GtmeError as e:
        _fail(e)


# ---------------------------------------------------------------------------
# Batch helpers (reused by every command in Task 7+)
# ---------------------------------------------------------------------------

BATCH_OPTIONS = [
    click.option(
        "--batch", "batch_src", default=None,
        help="Run over a list of inputs: a file path, or '-' for stdin.",
    ),
    click.option("--out", "out_path", default=None, help="Batch output file (JSONL)."),
    click.option("--stdout", "force_stdout", is_flag=True, help="Print batch JSONL to stdout."),
]


def batch_options(fn):
    for opt in reversed(BATCH_OPTIONS):
        fn = opt(fn)
    return fn


def _read_batch_inputs(batch_src: str) -> list[str]:
    text = (
        click.get_text_stream("stdin").read()
        if batch_src == "-"
        else Path(batch_src).read_text()
    )
    return [line.strip() for line in text.splitlines() if line.strip()]


def _default_out(noun: str) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    d = Path(".gtme-linkedin")
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{noun}-{ts}.jsonl"


def run_batchable(noun: str, call, positional, batch_src, out_path, force_stdout):
    """call: (session, item) -> dict.  positional: single value when not batching."""
    try:
        with LinkedInSession() as s:
            if batch_src is None:
                _emit_single(call(s, positional))
                return
            items = _read_batch_inputs(batch_src)
            results = [call(s, item) for item in items]
    except GtmeError as e:
        _fail(e)
        return

    if force_stdout:
        click.echo(to_jsonl(results))
        return

    out = Path(out_path) if out_path else _default_out(noun)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(to_jsonl(results) + "\n")
    click.echo(to_json({"written": str(out), "count": len(results)}))


# ---------------------------------------------------------------------------
# CLI groups
# ---------------------------------------------------------------------------

@click.group()
def main() -> None:
    """gtme-linkedin: LinkedIn data + outreach for the auto-gtme agent."""


# ---------------------------------------------------------------------------
# Auth group
# ---------------------------------------------------------------------------

@main.group("auth")
def auth_group() -> None:
    """Session management."""


@auth_group.command("status")
def auth_status_cmd() -> None:
    """Report whether a LinkedIn session profile exists."""
    _emit_single(adapter.auth_status())


@auth_group.command("login")
def auth_login_cmd() -> None:
    """Run the one-time interactive login (opens a browser)."""
    try:
        _emit_single(adapter.auth_login())
    except GtmeError as e:
        _fail(e)


@main.group()
def person() -> None:
    """Person profiles, search, and connection actions."""


@person.command("get")
@click.argument("username", required=False)
@click.option("--sections", default=None, help="Comma-separated extra sections (experience,posts,...).")
@batch_options
def person_get(username: str | None, sections: str | None, batch_src, out_path, force_stdout) -> None:
    """Scrape a person profile (single) or a batch of usernames."""
    if username is None and batch_src is None:
        _fail(GtmeError(EXIT_USAGE, "missing_input", suggestion="pass a username or --batch -"))
        return
    run_batchable(
        "person",
        lambda s, u: s.get_person(u, sections),
        username,
        batch_src,
        out_path,
        force_stdout,
    )


@person.command("search")
@click.argument("keywords")
@click.option("--location", default=None)
@click.option("--network", default=None, help="Comma-separated codes, e.g. F,S,O.")
@click.option("--company", default=None)
def person_search(keywords, location, network, company):
    """Search for people by keywords."""
    net = [c.strip() for c in network.split(",") if c.strip()] if network else None
    try:
        with LinkedInSession() as s:
            _emit_single(s.search_people(keywords, location=location, network=net, company=company))
    except GtmeError as e:
        _fail(e)


@person.command("sidebar")
@click.argument("username", required=False)
@batch_options
def person_sidebar(username, batch_src, out_path, force_stdout):
    """Fetch sidebar profiles for a person (single or batch)."""
    if username is None and batch_src is None:
        _fail(GtmeError(EXIT_USAGE, "missing_input", suggestion="pass a username or --batch -"))
        return
    run_batchable("person-sidebar", lambda s, u: s.sidebar(u), username, batch_src, out_path, force_stdout)


@person.command("me")
@click.option("--sections", default=None)
def person_me(sections):
    """Fetch the authenticated user's own profile."""
    try:
        with LinkedInSession() as s:
            _emit_single(s.me(sections))
    except GtmeError as e:
        _fail(e)


@person.command("connect")
@click.argument("username")
@click.option("--note", default=None)
@click.option("--send", is_flag=True, help="Actually send (omit for dry-run).")
def person_connect(username, note, send):
    """Send a connection request (dry-run unless --send)."""
    run_write("connect", username, send, {"note": note},
              lambda s: s.connect(username, note))


# ---------------------------------------------------------------------------
# Message group
# ---------------------------------------------------------------------------

@main.group()
def message() -> None:
    """Messaging actions."""


@message.command("send")
@click.argument("username")
@click.option("--body", required=True)
@click.option("--send", is_flag=True, help="Actually send (omit for dry-run).")
def message_send(username, body, send):
    """Send a DM (dry-run unless --send)."""
    run_write("send_message", username, send, {"body": body},
              lambda s: s.send_message(username, body, confirm_send=True))


# ---------------------------------------------------------------------------
# Company group
# ---------------------------------------------------------------------------

@main.group()
def company() -> None:
    """Company profiles, posts, employees, and search."""


@company.command("get")
@click.argument("slug", required=False)
@click.option("--sections", default=None)
@batch_options
def company_get(slug, sections, batch_src, out_path, force_stdout):
    """Scrape a company profile (single) or a batch of slugs."""
    if slug is None and batch_src is None:
        _fail(GtmeError(EXIT_USAGE, "missing_input", suggestion="pass a slug or --batch -"))
        return
    run_batchable("company", lambda s, x: s.get_company(x, sections), slug, batch_src, out_path, force_stdout)


@company.command("posts")
@click.argument("slug", required=False)
@batch_options
def company_posts(slug, batch_src, out_path, force_stdout):
    """Fetch posts for a company (single or batch)."""
    if slug is None and batch_src is None:
        _fail(GtmeError(EXIT_USAGE, "missing_input", suggestion="pass a slug or --batch -"))
        return
    run_batchable("company-posts", lambda s, x: s.company_posts(x), slug, batch_src, out_path, force_stdout)


@company.command("employees")
@click.argument("slug", required=False)
@batch_options
def company_employees(slug, batch_src, out_path, force_stdout):
    """Fetch employees for a company (single or batch)."""
    if slug is None and batch_src is None:
        _fail(GtmeError(EXIT_USAGE, "missing_input", suggestion="pass a slug or --batch -"))
        return
    run_batchable("company-employees", lambda s, x: s.company_employees(x), slug, batch_src, out_path, force_stdout)


@company.command("search")
@click.argument("keywords")
def company_search(keywords):
    """Search for companies by keywords."""
    try:
        with LinkedInSession() as s:
            _emit_single(s.search_companies(keywords))
    except GtmeError as e:
        _fail(e)


# ---------------------------------------------------------------------------
# Job group
# ---------------------------------------------------------------------------

@main.group()
def job() -> None:
    """Job listings and search."""


@job.command("get")
@click.argument("id", required=False)
@batch_options
def job_get(id, batch_src, out_path, force_stdout):
    """Fetch a job posting (single) or a batch of IDs."""
    if id is None and batch_src is None:
        _fail(GtmeError(EXIT_USAGE, "missing_input", suggestion="pass a job id or --batch -"))
        return
    run_batchable("job", lambda s, x: s.get_job(x), id, batch_src, out_path, force_stdout)


@job.command("search")
@click.argument("keywords")
def job_search(keywords):
    """Search for jobs by keywords."""
    try:
        with LinkedInSession() as s:
            _emit_single(s.search_jobs(keywords))
    except GtmeError as e:
        _fail(e)


# ---------------------------------------------------------------------------
# Inbox group
# ---------------------------------------------------------------------------

@main.group()
def inbox() -> None:
    """LinkedIn inbox and conversation management."""


@inbox.command("list")
@click.option("--limit", default=20, type=int)
def inbox_list(limit):
    """List inbox threads."""
    try:
        with LinkedInSession() as s:
            _emit_single(s.inbox(limit))
    except GtmeError as e:
        _fail(e)


# ---------------------------------------------------------------------------
# Conversation group
# ---------------------------------------------------------------------------

@main.group()
def conversation() -> None:
    """Read and search conversations."""


@conversation.command("get")
@click.argument("thread", required=False)
@batch_options
def conversation_get(thread, batch_src, out_path, force_stdout):
    """Fetch a conversation thread (single or batch)."""
    if thread is None and batch_src is None:
        _fail(GtmeError(EXIT_USAGE, "missing_input", suggestion="pass a thread id or --batch -"))
        return
    run_batchable("conversation", lambda s, x: s.conversation(x), thread, batch_src, out_path, force_stdout)


@conversation.command("search")
@click.argument("query")
def conversation_search(query):
    """Search conversations by query."""
    try:
        with LinkedInSession() as s:
            _emit_single(s.search_conversations(query))
    except GtmeError as e:
        _fail(e)


# ---------------------------------------------------------------------------
# Feed group
# ---------------------------------------------------------------------------

@main.group()
def feed() -> None:
    """LinkedIn feed."""


@feed.command("get")
@click.option("--limit", default=20, type=int)
def feed_get(limit):
    """Fetch the LinkedIn feed."""
    try:
        with LinkedInSession() as s:
            _emit_single(s.feed(limit))
    except GtmeError as e:
        _fail(e)


if __name__ == "__main__":
    main()
