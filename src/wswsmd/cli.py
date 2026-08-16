from __future__ import annotations

import argparse
import sys

import requests

from wswsmd.convert import to_markdown
from wswsmd.fetch import fetch_html
from wswsmd.parse import parse_article


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wswsmd",
        description="Convert a World Socialist Web Site article to Markdown.",
    )
    parser.add_argument("url", help="URL of the WSWS article to convert")
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="write Markdown to FILE instead of printing to stdout",
    )
    parser.add_argument(
        "--no-frontmatter",
        action="store_true",
        help="omit the YAML frontmatter header from the output",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        html = fetch_html(args.url)
        article = parse_article(html, args.url)
    except requests.RequestException as exc:
        print(f"wswsmd: failed to fetch {args.url}: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"wswsmd: {exc}", file=sys.stderr)
        return 1

    markdown = to_markdown(article, include_frontmatter=not args.no_frontmatter)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown)
    else:
        print(markdown, end="")

    return 0


if __name__ == "__main__":
    sys.exit(main())
