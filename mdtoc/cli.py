"""Command-line interface for mdtoc."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from mdtoc.generator import generate_toc
from mdtoc.parser import parse_headings


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for mdtoc."""
    parser = argparse.ArgumentParser(
        prog="mdtoc",
        description="Generate a table of contents for Markdown files.",
    )
    parser.add_argument(
        "file",
        type=Path,
        help="path to the markdown file",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="maximum heading depth to include (default: 3)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the mdtoc CLI.

    Args:
        argv: Command-line arguments.  Uses *sys.argv* when *None*.

    Returns:
        Exit code — 0 on success, 1 on error.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    path: Path = args.file
    if not path.is_file():
        print(f"Error: '{path}' is not a file.", file=sys.stderr)
        return 1

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Error reading '{path}': {exc}", file=sys.stderr)
        return 1

    headings = parse_headings(content)
    if not headings:
        print("No headings found.", file=sys.stderr)
        return 0

    toc = generate_toc(headings, max_depth=args.max_depth)
    print(toc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
