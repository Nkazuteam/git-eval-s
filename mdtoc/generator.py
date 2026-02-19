"""Table of Contents generator."""
from __future__ import annotations

import re

from mdtoc.parser import Heading


def slugify(text: str) -> str:
    """Convert heading text to a GitHub-compatible anchor slug.

    Args:
        text: Heading text to convert.

    Returns:
        URL-safe slug for use in markdown anchor links.
    """
    slug = text.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    return slug


def generate_toc(
    headings: list[Heading],
    max_depth: int = 3,
    min_level: int | None = None,
) -> str:
    """Generate a markdown table of contents.

    Args:
        headings: Headings extracted by :func:`parse_headings`.
        max_depth: How many levels deep to include (default 3).
        min_level: Treat this level as the shallowest.  When *None*,
                   the smallest level found in *headings* is used.

    Returns:
        Formatted markdown TOC.  Empty string when *headings* is empty.
    """
    if not headings:
        return ""

    if min_level is None:
        min_level = min(h.level for h in headings)

    lines: list[str] = []
    for heading in headings:
        depth = heading.level - min_level
        if depth >= max_depth:
            continue
        indent = "  " * depth
        slug = slugify(heading.text)
        lines.append(f"{indent}- [{heading.text}](#{slug})")

    return "\n".join(lines)
