import re

from markdownify import ATX, markdownify

from wswsmd.parse import Article

_BLANK_LINES = re.compile(r"\n{3,}")


def _yaml_str(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{escaped}"'


def _frontmatter(article: Article) -> str:
    lines = [
        "---",
        f"title: {_yaml_str(article.title)}",
        f"author: {_yaml_str(article.author)}",
        f"date: {_yaml_str(article.date_iso)}",
        f"description: {_yaml_str(article.description)}",
        f"url: {_yaml_str(article.url)}",
        "---",
    ]
    return "\n".join(lines)


def _byline(article: Article) -> str:
    parts = [p for p in (article.author, article.date_display) if p]
    return f"*{' — '.join(parts)}*" if parts else ""


def to_markdown(article: Article, include_frontmatter: bool = True) -> str:
    body = markdownify(article.body_html, heading_style=ATX, bullets="-").strip()
    body = _BLANK_LINES.sub("\n\n", body)

    sections = []
    if include_frontmatter:
        sections.append(_frontmatter(article))
    sections.append(f"# {article.title}")
    byline = _byline(article)
    if byline:
        sections.append(byline)
    sections.append(body)

    return "\n\n".join(sections) + "\n"
