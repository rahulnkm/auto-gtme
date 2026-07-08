import json
import pytest
from click.testing import CliRunner
from gtme_linkedin import cli

pytestmark = pytest.mark.smoke


def test_person_me_live():
    """Requires a real logged-in session (run: pytest -m smoke)."""
    r = CliRunner().invoke(cli.main, ["person", "me"])
    assert r.exit_code == 0
    assert "url" in json.loads(r.output)
