# WSWS Markdown

[![CI](https://github.com/JoeMountWSWS/wsws-md/actions/workflows/ci.yml/badge.svg)](https://github.com/JoeMountWSWS/wsws-md/actions/workflows/ci.yml)
[![Publish to PyPI](https://github.com/JoeMountWSWS/wsws-md/actions/workflows/publish.yml/badge.svg)](https://github.com/JoeMountWSWS/wsws-md/actions/workflows/publish.yml)

A tool to convert articles from the World Socialist Web Site to Markdown format.

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

## Development

```sh
pip install -e ".[test]"
pytest
```

Pull request titles must follow [Conventional Commits](https://www.conventionalcommits.org/)
— see [CONTRIBUTING.md](CONTRIBUTING.md). Releases are automated with
[release-please](https://github.com/googleapis/release-please).
