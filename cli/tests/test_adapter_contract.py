"""Guards every upstream symbol the adapter depends on. Run on every version bump."""
import inspect


def test_boot_path_symbols_exist():
    from linkedin_mcp_server import bootstrap, authentication
    from linkedin_mcp_server.drivers import browser
    from linkedin_mcp_server.scraping import (
        LinkedInExtractor, parse_person_sections, parse_company_sections,
    )
    for fn in (bootstrap.configure_browser_environment, bootstrap.ensure_browser_installed,
               authentication.get_authentication_source, browser.set_headless,
               browser.get_or_create_browser, browser.ensure_authenticated, browser.close_browser):
        assert callable(fn)
    assert inspect.isclass(LinkedInExtractor)
    assert callable(parse_person_sections) and callable(parse_company_sections)


def test_login_path_symbols_exist():
    from linkedin_mcp_server import setup
    assert callable(setup.interactive_login)
    assert callable(setup.run_profile_creation)


def test_exception_types_exist():
    from linkedin_mcp_server.core.exceptions import AuthenticationError, ProfileNotFoundError
    from linkedin_mcp_server.exceptions import CredentialsNotFoundError
    assert issubclass(AuthenticationError, Exception)
    assert issubclass(CredentialsNotFoundError, Exception)
    assert issubclass(ProfileNotFoundError, Exception)


def test_extractor_has_expected_methods():
    from linkedin_mcp_server.scraping import LinkedInExtractor
    # NOTE: get_company_posts is NOT a method on LinkedInExtractor — it is
    # implemented as a standalone MCP tool (tools/company.py) that calls
    # extractor.extract_page() directly. The adapter replicates that pattern.
    # extract_page IS the method the adapter uses for company_posts().
    for name in ("scrape_person", "search_people", "get_sidebar_profiles", "get_my_profile",
                 "connect_with_person", "scrape_company", "extract_page",
                 "search_companies", "get_company_employees", "scrape_job", "search_jobs",
                 "get_inbox", "get_conversation", "search_conversations",
                 "send_message", "extract_feed"):
        assert hasattr(LinkedInExtractor, name), f"missing LinkedInExtractor.{name}"


def test_extractor_send_message_requires_confirm_send():
    """send_message has a required keyword-only arg confirm_send: bool."""
    import inspect
    from linkedin_mcp_server.scraping import LinkedInExtractor
    sig = inspect.signature(LinkedInExtractor.send_message)
    params = sig.parameters
    assert "confirm_send" in params, "send_message must have confirm_send param"
    p = params["confirm_send"]
    assert p.kind == inspect.Parameter.KEYWORD_ONLY, "confirm_send must be keyword-only"


def test_extract_feed_takes_num_posts():
    """extract_feed uses num_posts, not limit."""
    import inspect
    from linkedin_mcp_server.scraping import LinkedInExtractor
    sig = inspect.signature(LinkedInExtractor.extract_feed)
    assert "num_posts" in sig.parameters, "extract_feed must have num_posts param"


def test_rate_limited_sentinel_exists():
    """_RATE_LIMITED_MSG is a private symbol imported by company_posts(); guard it explicitly."""
    from linkedin_mcp_server.scraping.extractor import _RATE_LIMITED_MSG
    assert isinstance(_RATE_LIMITED_MSG, str)


def test_config_reset_symbol_exists():
    """reset_config is imported by _upstream_argv(); guard it explicitly."""
    from linkedin_mcp_server.config import reset_config
    assert callable(reset_config)


# ---------------------------------------------------------------------------
# Exception-mapping unit test
# ---------------------------------------------------------------------------

import pytest
from linkedin_mcp_server.core.exceptions import AuthenticationError, ProfileNotFoundError
from linkedin_mcp_server.exceptions import CredentialsNotFoundError
from gtme_linkedin.adapter import LinkedInSession
from gtme_linkedin.errors import GtmeError, EXIT_AUTH, EXIT_NOT_FOUND


def test_run_maps_auth_error_to_exit_4():
    s = LinkedInSession()
    s._loop = __import__("asyncio").new_event_loop()

    async def boom():
        raise AuthenticationError("logged out")

    try:
        with pytest.raises(GtmeError) as ei:
            s._run(boom())
        assert ei.value.exit_code == EXIT_AUTH
    finally:
        s._loop.close()


def test_run_maps_credentials_not_found_to_exit_4():
    s = LinkedInSession()
    s._loop = __import__("asyncio").new_event_loop()

    async def boom():
        raise CredentialsNotFoundError("no creds")

    try:
        with pytest.raises(GtmeError) as ei:
            s._run(boom())
        assert ei.value.exit_code == EXIT_AUTH
    finally:
        s._loop.close()


def test_run_maps_profile_not_found_to_exit_3():
    s = LinkedInSession()
    s._loop = __import__("asyncio").new_event_loop()

    async def boom():
        raise ProfileNotFoundError("profile gone")

    try:
        with pytest.raises(GtmeError) as ei:
            s._run(boom())
        assert ei.value.exit_code == EXIT_NOT_FOUND
    finally:
        s._loop.close()
