"""No real person appears as example data in this public repo.

Five real individuals shipped before this check existed: a prospect named across
three skills, a second person in `gtme-enrich` by name AND by their actual
LinkedIn slug AND their work email, and two more sitting in test fixtures. Each
was depicted as an outbound target. The repo is public, so a search for any of
their names could land on it.

The first version of this check missed three of the five, in two ways worth
recording because both are ordinary mistakes:

- **It only scanned `gtme-*/SKILL.md`.** Test fixtures are shipped source too,
  and two of the five lived there.
- **Its name pattern was ASCII-only.** `[A-Z][a-z]+` does not match `Aiste`
  spelled with an `e`-with-dot. A privacy check that fails open on non-Latin
  names fails the people most likely to be identifiable from a single hit.

Companies are deliberately NOT covered. A public company named in an
illustrative example is not the same exposure as a private individual, and the
examples need a plausible account id to be legible.

The allowlist is the mechanism, not a regex for "looks real". Any two capitalised
words look like a name, so a pattern would either miss cases or cry wolf. An
allowlist means a new name in an example has to be added here on purpose - the
same escape-hatch-with-a-reason shape as `UNUSED:` in provenance.md and
`UNREAD_OK` in validate.py.
"""
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

ALLOWED_NAMES = {"John Smith", "Ana Müller", "Jane Doe"}
ALLOWED_SLUGS = {"john-smith", "ana-muller", "clay-hq"}   # clay-hq is a company page
ALLOWED_EMAIL_LOCALS = {"john.smith", "jane.doe", "x"}

# Research digests cite public operators for their published work, with links.
# That is attribution, not exposure, and it is the provenance for the doctrine
# those files carry. Skills may cite a practitioner by name in prose for the same
# reason; what they may not do is use a real person as a data example.
EXEMPT_DIRS = {"research", "docs"}

# `\w` under Unicode covers accented and non-Latin letters. The earlier
# ASCII-only pattern is the bug this expression exists to not repeat.
# `prospect`, `contact` and `says` always denote a person. A bare `name` does not:
# templates, certifications and gap-math variables all use it, so it only counts
# when the same line carries person context - a linkedin slug, a title, an email.
PERSON_FIELD = re.compile(r'"(?:prospect|contact|full_name|says)":\s*"([^"]+)"')
NAME_WITH_PERSON_CONTEXT = re.compile(
    r'"name":\s*"([^"]+)"(?=.*"(?:linkedin|title|email)"\s*:)')
SLUG_FIELD = re.compile(r'"linkedin":\s*"([^"]+)"')
EMAIL_FIELD = re.compile(r'"email":\s*"([^"@]+)@')
LOOKS_LIKE_A_PERSON = re.compile(r"^\w+[\w'’-]*\s+\w+[\w'’-]*$", re.UNICODE)


def tracked_source():
    """Every file git actually ships. Untracked and gitignored files cannot leak."""
    out = subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True).stdout
    for rel in out.split("\n"):
        p = REPO / rel
        if not rel or p.suffix not in (".md", ".py", ".json", ".jsonl"):
            continue
        if rel.split("/")[0] in EXEMPT_DIRS:
            continue
        yield rel, p.read_text(errors="ignore")


def test_git_ls_files_is_actually_returning_something():
    """A sweep over an empty file list passes silently and proves nothing - the
    same silent-skip failure that made the distillation check stop running."""
    files = list(tracked_source())
    assert len(files) > 20, f"only {len(files)} files scanned; the sweep is not working"
    assert any(r.startswith("skills/tests/") for r, _ in files), "test fixtures not scanned"
    assert any(r.endswith("SKILL.md") for r, _ in files), "skills not scanned"


def test_no_real_person_is_named_in_example_data():
    bad = []
    for rel, text in tracked_source():
        for line in text.split("\n"):
            names = [n for n in PERSON_FIELD.findall(line) + NAME_WITH_PERSON_CONTEXT.findall(line)
                     if LOOKS_LIKE_A_PERSON.match(n)]
            for n in names:
                if n not in ALLOWED_NAMES:
                    bad.append(f"{rel}: name {n!r}")
            # A slug or an address only points at a real individual when it sits
            # beside a person-shaped name. `no-status` is a hyphenated lowercase
            # string and so is every LinkedIn slug: the PAIR is the signal.
            if names:
                for s in SLUG_FIELD.findall(line):
                    if s not in ALLOWED_SLUGS:
                        bad.append(f"{rel}: linkedin slug {s!r}")
            for e in EMAIL_FIELD.findall(line):
                if e not in ALLOWED_EMAIL_LOCALS:
                    bad.append(f"{rel}: email local-part {e!r}")
    assert not bad, "real people in public example data:\n  " + "\n  ".join(sorted(set(bad)))


def test_the_check_catches_a_non_ascii_name():
    """The specific miss worth pinning: the first version's `[A-Z][a-z]+` pattern
    let a name with a diacritic straight through."""
    assert LOOKS_LIKE_A_PERSON.match("Aistė Stakauskaitė")
    assert LOOKS_LIKE_A_PERSON.match("John Smith")
    assert not LOOKS_LIKE_A_PERSON.match("alert_volume_monthly")


def test_the_allowlist_stays_small():
    """It is an exemption list. If it grows, examples are being written with new
    invented people instead of reusing the placeholder."""
    assert len(ALLOWED_NAMES) <= 5
