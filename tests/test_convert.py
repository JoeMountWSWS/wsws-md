from pathlib import Path

import pytest

from wswsmd.convert import to_markdown
from wswsmd.parse import parse_article

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
