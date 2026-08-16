from __future__ import annotations

import argparse
import os
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
    parser.add_argument(
        "--no-links",
        action="store_true",
        help="strip hyperlinks from the body text, keeping only the link text",
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

    markdown = to_markdown(
        article,
        include_frontmatter=not args.no_frontmatter,
        strip_links=args.no_links,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown)
    else:
        try:
            print(markdown, end="")
            sys.stdout.flush()
        except BrokenPipeError:
            # Downstream reader (e.g. `head`) closed the pipe early. Redirect
            # stdout to devnull so the interpreter's shutdown flush doesn't
            # also raise, then exit quietly like other Unix CLI tools do.
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
