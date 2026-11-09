"""Shared helpers for the kit's tools. Reads the 30 checks from the checks folder.

Standard library only. Nothing here touches the network.
"""

from __future__ import annotations

import pathlib
import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

ROOT = pathlib.Path(__file__).resolve().parent.parent

GROUPS: List[Tuple[str, str]] = [
    ("Website and marketing pages", "checks/1-website-and-marketing-pages.md"),
    ("Data vendors and lead lists", "checks/2-data-vendors-and-lead-lists.md"),
    ("Outreach and automation", "checks/3-outreach-and-automation.md"),
]
FIELDS = ["What to look at", "How to check it", "Pass or fail test", "The fix", "Source"]
PRIORITIES = ("Fix first", "Fix soon")
BASES = ("LinkedIn rule", "Law", "Operating practice")

CHECK_HEADING = re.compile(r"^## Check (\d+): (.+)$", re.M)
FIELD_HEADING = re.compile(r"^### (.+)$", re.M)


@dataclass(frozen=True)
class Check:
    number: int
    title: str
    group: str
    path: str
    priority: str
    based_on: str
    sections: Dict[str, str] = field(default_factory=dict)


def _field_value(block: str, name: str) -> str:
    match = re.search(rf"^\*\*{name}:\*\* (.+)$", block, re.M)
    return match.group(1).strip() if match else ""


def _sections(block: str) -> Dict[str, str]:
    heads = list(FIELD_HEADING.finditer(block))
    found: Dict[str, str] = {}
    for index, head in enumerate(heads):
        end = heads[index + 1].start() if index + 1 < len(heads) else len(block)
        found[head.group(1).strip()] = block[head.end():end].strip()
    return found


def load_checks(root: pathlib.Path = ROOT) -> List[Check]:
    """Return every check found in the three group files, in file order."""
    checks: List[Check] = []
    for group, relative in GROUPS:
        path = root / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        heads = list(CHECK_HEADING.finditer(text))
        for index, head in enumerate(heads):
            end = heads[index + 1].start() if index + 1 < len(heads) else len(text)
            block = text[head.end():end]
            checks.append(
                Check(
                    number=int(head.group(1)),
                    title=head.group(2).strip(),
                    group=group,
                    path=relative,
                    priority=_field_value(block, "Priority"),
                    based_on=_field_value(block, "Based on"),
                    sections=_sections(block),
                )
            )
    return checks
