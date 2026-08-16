# WSWS Markdown

[![CI](https://github.com/JoeMountWSWS/wsws-md/actions/workflows/ci.yml/badge.svg)](https://github.com/JoeMountWSWS/wsws-md/actions/workflows/ci.yml)
[![Publish to PyPI](https://github.com/JoeMountWSWS/wsws-md/actions/workflows/publish.yml/badge.svg)](https://github.com/JoeMountWSWS/wsws-md/actions/workflows/publish.yml)

A tool to convert articles from the World Socialist Web Site to Markdown format.

## Why not a generic URL-to-Markdown tool?

Generic converters guess at the main content block, so they often leak WSWS
site chrome (share icons, newsletter widgets, "Read more" blocks) into the
output or strip real content by mistake. This tool targets WSWS's actual
markup (`itemprop="articleBody"`, `/en/authors/` links, `<time datetime>`) for
exact extraction and frontmatter, at the cost of being tied to WSWS's current
template.

## Install

```sh
pip install wsws-md
```

## Usage

```sh
wswsmd "https://www.wsws.org/en/articles/2026/07/03/coeq-j03.html"
```

Prints the article as Markdown (with YAML frontmatter containing title, author,
date, description and source URL) to stdout. Use `-o FILE` / `--output FILE`
to write to a file instead:

```sh
wswsmd "https://www.wsws.org/en/articles/2026/07/03/coeq-j03.html" -o article.md
```
Use `--no-frontmatter` to omit the YAML header and print just the title,
byline and body:

```sh
wswsmd "https://www.wsws.org/en/articles/2026/07/03/coeq-j03.html" --no-frontmatter
```

## Claude Skill

This repo also ships a [Claude Skill](https://github.com/JoeMountWSWS/wsws-md/tree/main/skills/wsws-md)
that wraps the CLI so Claude can convert WSWS articles to Markdown directly. Download the
packaged `wsws-md-skill-*.zip` from the [Releases](https://github.com/JoeMountWSWS/wsws-md/releases)
page and upload it as a Skill in Claude.ai.

## Development

```sh
pip install -e ".[test]"
pytest
```

Pull request titles must follow [Conventional Commits](https://www.conventionalcommits.org/)
— see [CONTRIBUTING.md](CONTRIBUTING.md). Releases are automated with
[release-please](https://github.com/googleapis/release-please).
