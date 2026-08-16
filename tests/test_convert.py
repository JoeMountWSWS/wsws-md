from pathlib import Path

import pytest

from wswsmd.convert import to_markdown
from wswsmd.parse import Article, parse_article

FIXTURE = Path(__file__).parent / "fixtures" / "coeq-j03.html"
URL = "https://www.wsws.org/en/articles/2026/07/03/coeq-j03.html"


@pytest.fixture
def markdown():
    html = FIXTURE.read_text()
    article = parse_article(html, URL)
    return to_markdown(article)


def test_frontmatter(markdown):
    assert markdown.startswith("---\n")
    front, _, rest = markdown[4:].partition("\n---\n")
    assert (
        'title: "The Colorado primary and the growing support for socialism"' in front
    )
    assert 'author: "Patrick Martin"' in front
    assert f'url: "{URL}"' in front

    assert "# The Colorado primary and the growing support for socialism" in rest
    assert "*Patrick Martin — 2 July 2026*" in rest


def test_frontmatter_omitted_when_disabled():
    html = FIXTURE.read_text()
    article = parse_article(html, URL)
    markdown = to_markdown(article, include_frontmatter=False)

    assert not markdown.startswith("---\n")
    assert 'title: "' not in markdown
    assert "# The Colorado primary and the growing support for socialism" in markdown
    assert "*Patrick Martin — 2 July 2026*" in markdown


def test_body_is_markdown_paragraphs(markdown):
    assert "Diana DeGette" in markdown
    assert "<p>" not in markdown
    assert "<div" not in markdown


def test_no_leftover_ads_or_navigation(markdown):
    assert "AudioNative" not in markdown
    assert "Read more" not in markdown
    assert "Related Topics" not in markdown


def test_inline_emphasis_preserved(markdown):
    assert (
        "*Washington Post*" in markdown
    )  # <em>Washington Post</em> converts to emphasis


@pytest.fixture
def linked_article():
    return Article(
        title="Linked article",
        author="J. Author",
        date_iso="2026-07-02",
        date_display="2 July 2026",
        url=URL,
        description="",
        body_html=(
            "<p>See <a href='https://www.wsws.org/en/articles/x.html'>"
            "socialist internationalism</a> and <a href='https://example.com'>"
            "this <em>other</em> report</a> for more.</p>"
        ),
    )


def test_links_kept_by_default(linked_article):
    markdown = to_markdown(linked_article)
    assert (
        "[socialist internationalism](https://www.wsws.org/en/articles/x.html)"
        in markdown
    )


def test_no_links_strips_hyperlinks_but_keeps_text(linked_article):
    markdown = to_markdown(linked_article, strip_links=True)
    assert "socialist internationalism" in markdown
    assert "this *other* report" in markdown
    assert "[socialist internationalism]" not in markdown
    assert "https://www.wsws.org/en/articles/x.html" not in markdown
    assert "https://example.com" not in markdown
