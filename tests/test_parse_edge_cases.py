import pytest
from bs4 import BeautifulSoup

from wswsmd.parse import (
    _extract_author,
    _extract_body,
    _extract_date,
    _extract_title,
    parse_article,
)


def soup_of(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


def test_extract_title_falls_back_to_html_title_tag():
    soup = soup_of(
        "<html><head><title>Some Article - World Socialist Web Site</title>"
        "</head></html>"
    )
    assert _extract_title(soup) == "Some Article"


def test_extract_title_keeps_full_text_when_no_suffix():
    soup = soup_of("<html><head><title>Some Article</title></head></html>")
    assert _extract_title(soup) == "Some Article"


def test_extract_title_returns_empty_when_no_title_available():
    soup = soup_of("<html><head></head></html>")
    assert _extract_title(soup) == ""


def test_extract_author_returns_empty_without_header():
    soup = soup_of("<html><body><p>no header here</p></body></html>")
    assert _extract_author(soup) == ""


def test_extract_date_returns_empty_without_time_tag():
    soup = soup_of("<html><body><header></header></body></html>")
    assert _extract_date(soup) == ("", "")


def test_extract_body_raises_without_article_body():
    soup = soup_of("<html><body><div>no article body here</div></body></html>")
    with pytest.raises(ValueError, match="articleBody"):
        _extract_body(soup)


def test_extract_body_raises_without_content_div():
    soup = soup_of('<html><body><div itemprop="articleBody"></div></body></html>')
    with pytest.raises(ValueError, match="body content"):
        _extract_body(soup)


def test_extract_body_strips_scripts_styles_and_svgs():
    soup = soup_of(
        '<html><body><div itemprop="articleBody"><div class="content">'
        "<p>Keep me</p>"
        "<script>evil()</script>"
        "<style>.x{}</style>"
        "<svg></svg>"
        "</div></div></body></html>"
    )
    content = _extract_body(soup)
    html = str(content)
    assert "Keep me" in html
    assert "<script" not in html
    assert "<style" not in html
    assert "<svg" not in html


def test_extract_body_strips_mobile_only_images():
    soup = soup_of(
        '<html><body><div itemprop="articleBody"><div class="content">'
        "<p>Text</p>"
        '<img class="dn-m" src="mobile.jpg">'
        '<img class="dn-d" src="desktop.jpg">'
        "</div></div></body></html>"
    )
    content = _extract_body(soup)
    html = str(content)
    assert "mobile.jpg" not in html
    assert "desktop.jpg" in html


def test_parse_article_raises_without_title():
    html = (
        '<html><head></head><body><div itemprop="articleBody">'
        '<div class="content"><p>Body text</p></div></div></body></html>'
    )
    with pytest.raises(ValueError, match="title"):
        parse_article(html, "https://example.com/x")
