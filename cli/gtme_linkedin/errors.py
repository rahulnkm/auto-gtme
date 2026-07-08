EXIT_OK = 0
EXIT_GENERAL = 1
EXIT_USAGE = 2
EXIT_NOT_FOUND = 3
EXIT_AUTH = 4
EXIT_CONFLICT = 5


class GtmeError(Exception):
    """A failure already classified to an exit code and a structured payload."""

    def __init__(self, exit_code: int, error: str, *, suggestion: str = "", input: str = "") -> None:
        self.exit_code = exit_code
        self.error = error
        self.suggestion = suggestion
        self.input = input
        super().__init__(error)

    def payload(self) -> dict:
        return {"error": self.error, "input": self.input, "suggestion": self.suggestion}
