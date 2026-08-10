from gtme_linkedin.errors import GtmeError, EXIT_AUTH


def test_gtme_error_carries_exit_code_and_payload():
    err = GtmeError(EXIT_AUTH, "auth_required",
                    suggestion="run `gtme-linkedin auth login`", input="alice")
    assert err.exit_code == 4
    assert err.payload() == {
        "error": "auth_required",
        "input": "alice",
        "suggestion": "run `gtme-linkedin auth login`",
    }
