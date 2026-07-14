# wsws-md
A tool to convert articles from the World Socialist Web Site to Markdown format.

## Install

```sh
pip install .
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

## Development

```sh
pip install -e ".[test]"
pytest
```
