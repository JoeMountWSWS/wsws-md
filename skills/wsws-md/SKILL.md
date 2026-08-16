---
name: wsws-md
description: Converts World Socialist Web Site (wsws.org) articles into Markdown with YAML frontmatter (title, author, date, description, source URL). This skill should be used when given a wsws.org article URL and asked to convert, export, save, or archive it as Markdown.
license: MIT
---

# WSWS Markdown

## Overview

Fetch a wsws.org article and convert it to clean Markdown using the `wsws-md` PyPI package
(source: https://github.com/JoeMountWSWS/wsws-md). The output includes YAML frontmatter with
the article's title, author, date, description, and source URL.

## Instructions

1. Install the CLI if it isn't already available:

   ```bash
   pip install --quiet wsws-md
   ```

2. Run it on the article URL to print Markdown to stdout:

   ```bash
   wswsmd "<article-url>"
   ```

   Or write the result directly to a file instead:

   ```bash
   wswsmd "<article-url>" -o article.md
   ```

3. On a non-zero exit code, relay the command's stderr message rather than guessing at the
   cause. The two possible failures are a network error fetching the URL, and the page not
   matching WSWS's expected article structure (wrong domain, removed/paywalled page, or an
   unexpected layout).

4. Return the resulting Markdown to the requester, or confirm the output file was written.

## Notes

- Requires network access to `pypi.org` (to install the package) and `wsws.org` (to fetch the
  article).
- Only wsws.org article pages are supported — other domains will fail to parse.
