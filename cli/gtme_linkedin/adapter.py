"""The only module coupled to linkedin_mcp_server internals. See contract test."""
from __future__ import annotations

import asyncio
import contextlib
import sys

from linkedin_mcp_server import bootstrap, setup
from linkedin_mcp_server.authentication import get_authentication_source
from linkedin_mcp_server.config import reset_config
from linkedin_mcp_server.drivers import browser as _browser
from linkedin_mcp_server.scraping import (
    LinkedInExtractor,
    parse_person_sections,
    parse_company_sections,
)
from linkedin_mcp_server.core.exceptions import AuthenticationError, ProfileNotFoundError
from linkedin_mcp_server.exceptions import CredentialsNotFoundError

from .errors import GtmeError, EXIT_AUTH, EXIT_GENERAL, EXIT_NOT_FOUND, EXIT_USAGE

# Rate-limited sentinel from upstream (matches extractor._RATE_LIMITED_MSG).
# Imported here so company_posts() can apply the same noise filter.
from linkedin_mcp_server.scraping.extractor import _RATE_LIMITED_MSG


@contextlib.contextmanager
def _upstream_argv():
    """Temporarily clear sys.argv[1:] so upstream's argparse-based config loader
    doesn't choke on gtme-linkedin's own subcommand tokens (e.g. 'auth status').
    The upstream config singleton is reset before each call and restored after.
    """
    saved = sys.argv[:]
    sys.argv = sys.argv[:1]   # keep prog name, drop all args
    reset_config()
    try:
        yield
    finally:
        sys.argv = saved
        reset_config()


class LinkedInSession:
    """Boots one warm browser + authenticated extractor, reused across a batch."""

    def __init__(self, headless: bool = True) -> None:
        self._headless = headless
        self._loop: asyncio.AbstractEventLoop | None = None
        self._ex: LinkedInExtractor | None = None

    def __enter__(self) -> "LinkedInSession":
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            with _upstream_argv():
                self._loop.run_until_complete(self._boot())
        except (AuthenticationError, CredentialsNotFoundError) as exc:
            raise GtmeError(EXIT_AUTH, "auth_required",
                            suggestion="run `gtme-linkedin auth login`", input=str(exc)) from exc
        return self

    def __exit__(self, *exc_info) -> None:
        if self._loop is not None:
            try:
                self._loop.run_until_complete(_browser.close_browser())
            finally:
                self._loop.close()

    async def _boot(self) -> None:
        bootstrap.configure_browser_environment()
        bootstrap.ensure_browser_installed()
        get_authentication_source()            # raises CredentialsNotFoundError if no session
        _browser.set_headless(self._headless)
        b = await _browser.get_or_create_browser()
        await _browser.ensure_authenticated()  # raises AuthenticationError if logged out
        self._ex = LinkedInExtractor(b.page)

    def _run(self, coro):
        assert self._loop is not None
        try:
            with _upstream_argv():
                return self._loop.run_until_complete(coro)
        except (AuthenticationError, CredentialsNotFoundError) as exc:
            raise GtmeError(EXIT_AUTH, "session_expired",
                            suggestion="run `gtme-linkedin auth login`", input=str(exc)) from exc
        except ProfileNotFoundError as exc:
            raise GtmeError(EXIT_NOT_FOUND, "not_found", input=str(exc)) from exc
        except GtmeError:
            raise
        except Exception as exc:  # noqa: BLE001 - last-resort classification
            raise GtmeError(EXIT_GENERAL, type(exc).__name__, input=str(exc)) from exc

    # --- reads ---

    def get_person(self, username: str, sections: str | None = None) -> dict:
        requested, _ = parse_person_sections(sections)
        return self._run(self._ex.scrape_person(username, requested))

    def search_people(self, keywords: str, *, location=None, network=None, company=None) -> dict:
        # network must be list[str] | None per upstream signature
        network_list = network if isinstance(network, list) or network is None else [network]
        return self._run(self._ex.search_people(
            keywords, location=location, network=network_list, current_company=company
        ))

    def sidebar(self, username: str) -> dict:
        return self._run(self._ex.get_sidebar_profiles(username))

    def me(self, sections: str | None = None) -> dict:
        requested, _ = parse_person_sections(sections)
        return self._run(self._ex.get_my_profile(sections=requested))

    def get_company(self, slug: str, sections: str | None = None) -> dict:
        requested, _ = parse_company_sections(sections)
        return self._run(self._ex.scrape_company(slug, requested))

    def company_posts(self, slug: str) -> dict:
        # get_company_posts is NOT a method on LinkedInExtractor — it is
        # a standalone MCP tool that calls extract_page directly (tools/company.py:132).
        # We replicate that pattern here.
        url = f"https://www.linkedin.com/company/{slug}/posts/"
        extracted = self._run(self._ex.extract_page(url, section_name="posts"))
        sections: dict = {}
        references: dict = {}
        section_errors: dict = {}
        if extracted.text and extracted.text != _RATE_LIMITED_MSG:
            sections["posts"] = extracted.text
            if extracted.references:
                references["posts"] = extracted.references
        elif extracted.error:
            section_errors["posts"] = extracted.error
        result: dict = {"url": url, "sections": sections}
        if references:
            result["references"] = references
        if section_errors:
            result["section_errors"] = section_errors
        return result

    def company_employees(self, slug: str) -> dict:
        return self._run(self._ex.get_company_employees(slug))

    def search_companies(self, keywords: str) -> dict:
        return self._run(self._ex.search_companies(keywords))

    def get_job(self, job_id: str) -> dict:
        return self._run(self._ex.scrape_job(job_id))

    def search_jobs(self, keywords: str) -> dict:
        return self._run(self._ex.search_jobs(keywords))

    def inbox(self, limit: int = 20) -> dict:
        return self._run(self._ex.get_inbox(limit))

    def conversation(self, thread: str | None = None, *, username: str | None = None) -> dict:
        # Upstream: get_conversation(linkedin_username=None, thread_id=None, index=0)
        if thread is None and username is None:
            raise GtmeError(EXIT_USAGE, "missing_input",
                            suggestion="pass a thread ID or username")
        return self._run(self._ex.get_conversation(
            linkedin_username=username, thread_id=thread
        ))

    def search_conversations(self, query: str) -> dict:
        return self._run(self._ex.search_conversations(query))

    def feed(self, limit: int = 20) -> dict:
        # Upstream extract_feed uses num_posts, not limit
        return self._run(self._ex.extract_feed(num_posts=limit))

    # --- writes ---

    def connect(self, username: str, note: str | None = None) -> dict:
        # note is keyword-only in upstream signature
        return self._run(self._ex.connect_with_person(username, note=note))

    def send_message(self, username: str, body: str, *, confirm_send: bool = False) -> dict:
        # confirm_send is a required keyword-only arg in upstream; we default False (dry-run)
        return self._run(self._ex.send_message(username, body, confirm_send=confirm_send))


# ---------------------------------------------------------------------------
# Auth helpers (no browser boot required)
# ---------------------------------------------------------------------------

def auth_status() -> dict:
    """Return authenticated state without starting a browser."""
    with _upstream_argv():
        try:
            get_authentication_source()
            return {"authenticated": True}
        except CredentialsNotFoundError:
            return {"authenticated": False, "suggestion": "run `gtme-linkedin auth login`"}


def auth_login() -> dict:
    """Run the one-time interactive login via upstream's run_profile_creation.

    interactive_login (the underlying async fn) always opens a visible browser —
    headless is hardcoded False in upstream for the login flow. run_profile_creation
    wraps it synchronously with asyncio.run(), so we call it directly.
    """
    with _upstream_argv():
        success = setup.run_profile_creation()
    if not success:
        raise GtmeError(EXIT_AUTH, "login_failed",
                        suggestion="re-run `gtme-linkedin auth login`")
    return {"authenticated": True}
