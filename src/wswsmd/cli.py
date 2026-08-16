from __future__ import annotations

import argparse
import logging
import os
import sys

import requests

from wswsmd.convert import to_markdown
from wswsmd.fetch import fetch_html
from wswsmd.parse import parse_article

log = logging.getLogger("wswsmd")


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
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="suppress non-error output",
    )
    verbosity.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print fetch/parse diagnostics to stderr",
    )
    return parser


def _configure_logging(*, quiet: bool, verbose: bool) -> None:
    if verbose:
        level = logging.DEBUG
    elif quiet:
        level = logging.ERROR
    else:
        level = logging.WARNING

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("wswsmd: %(message)s"))
    log.handlers = [handler]
    log.propagate = False
    log.setLevel(level)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _configure_logging(quiet=args.quiet, verbose=args.verbose)

    try:
        log.debug("fetching %s", args.url)
        html = fetch_html(args.url)
        log.debug("fetched %d bytes", len(html))
        log.debug("parsing article body")
        article = parse_article(html, args.url)
        log.debug("parsed %r (author=%r)", article.title, article.author)
    except requests.RequestException as exc:
        log.error("failed to fetch %s: %s", args.url, exc)
        return 1
    except ValueError as exc:
        log.error("%s", exc)
        return 1

    markdown = to_markdown(
        article,
        include_frontmatter=not args.no_frontmatter,
        strip_links=args.no_links,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown)
        log.debug("wrote Markdown to %s", args.output)
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
