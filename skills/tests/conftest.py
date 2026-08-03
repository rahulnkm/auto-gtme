"""Skill modules are scripts in sibling directories, not an installed package.
Put those directories on the path so tests can import them by module name."""
import json
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent
REPO = SKILLS.parent
for d in ("gtme-score", "gtme-enrich"):
    sys.path.insert(0, str(SKILLS / d))

# The committed example run. Every artifact test validates against this, so the
# suite is green on a fresh clone with nothing else present.
#
# It is generated from a real run by keeping the structure - every key, array
# length, enum, id and citation - and replacing the content, so it exercises the
# schemas the same way while naming nobody. Real runs live under runs/, which is
# gitignored; pointing tests there shipped a suite that only passed on one laptop
# and put a client's name in seven source files.
EXAMPLE_RUN = SKILLS / "tests" / "fixtures" / "example-run"


def artifact(*parts):
    """Load a file from the example run, e.g. artifact('01-company', 'company.json')."""
    return json.loads(EXAMPLE_RUN.joinpath(*parts).read_text())


def live_runs():
    """Real runs on this machine, if any. Empty on a fresh clone.

    The example run proves the schema accepts a well-formed artifact. Only a
    real one proves a schema change has not broken work already done - so tests
    that want that signal iterate these and skip when there are none. Discovered
    by shape rather than named, so no client name is written down to go stale.
    """
    runs = REPO / "runs"
    if not runs.is_dir():
        return []
    return sorted(d for d in runs.iterdir()
                  if (d / "01-company" / "company.json").exists())


def seller_names():
    """Every seller this checkout knows about - the example run plus any real
    run present locally.

    Template tests use this to prove a template names no specific seller. Reading
    the names instead of hardcoding one means the check covers every client
    automatically, and no client's name has to be written into a public file to
    assert it is absent - which is what it was doing before.
    """
    names = {"Northwind"}
    for run in live_runs():
        doc = json.loads((run / "01-company" / "company.json").read_text())
        for n in (doc.get("company"), (doc.get("domain") or "").split(".")[0]):
            if n:
                names.add(n)
    return sorted(names)
