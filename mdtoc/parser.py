"""Markdown heading parser."""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Heading:
    """A parsed markdown heading."""

    level: int
    text: str


def parse_headings(content: str) -> list[Heading]:
    """Extract headings from markdown content.

    Recognises ATX-style headings (lines starting with 1-6 ``#`` followed
    by a space).  Lines inside fenced code blocks are skipped.

    Args:
        content: Raw markdown text.

    Returns:
        Ordered list of headings found in *content*.
    """
    headings: list[Heading] = []
    in_code_block = False

    for line in content.splitlines():
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append(Heading(level=level, text=text))

    return headings
