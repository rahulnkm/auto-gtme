"""Skill modules are scripts in sibling directories, not an installed package.
Put those directories on the path so tests can import them by module name."""
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parent.parent
for d in ("gtme-score", "gtme-enrich"):
    sys.path.insert(0, str(SKILLS / d))
