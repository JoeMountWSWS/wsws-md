from pathlib import Path

import pytest

from wswsmd.parse import parse_article

FIXTURE = Path(__file__).parent / "fixtures" / "coeq-j03.html"
URL = "https://www.wsws.org/en/articles/2026/07/03/coeq-j03.html"

PHOTO_FIXTURE = Path(__file__).parent / "fixtures" / "yfab-j12.html"
PHOTO_URL = "https://www.wsws.org/en/articles/2026/07/12/yfab-j12.html"


@pytest.fixture
def article():
    html = FIXTURE.read_text()
    return parse_article(html, URL)


@pytest.fixture
def photo_article():
    html = PHOTO_FIXTURE.read_text()
    return parse_article(html, PHOTO_URL)


def test_metadata(article):
    assert article.title == "The Colorado primary and the growing support for socialism"
    assert article.author == "Patrick Martin"
    assert article.date_iso == "2026-07-03T02:01:26.000Z"
    assert article.date_display == "2 July 2026"
    assert article.url == URL
    assert "Democratic Socialists of America" in article.description


def test_body_contains_article_text(article):
    assert "Diana DeGette" in article.body_html
    assert "Socialist Equality Party" in article.body_html


def test_body_excludes_ads_and_widgets(article):
    assert "AudioNative" not in article.body_html
    assert "elevenlabs" not in article.body_html.lower()
    assert "jun25-declaration-of-independence" not in article.body_html


def test_body_excludes_trailing_navigation(article):
    assert "Read more" not in article.body_html
    assert "Related Topics" not in article.body_html
    assert "Contact us" not in article.body_html


def test_body_has_no_duplicate_mobile_images(article):
    assert "dn-m" not in article.body_html


def test_photo_metadata(photo_article):
    assert photo_article.title == (
        "Durham Miners' Gala used by labour and union bureaucracy "
        "to back Andy Burnham as new prime minister"
    )
    assert photo_article.author == "Our reporters"
    assert photo_article.date_iso == "2026-07-12T17:42:21.000Z"
    assert photo_article.url == PHOTO_URL


def test_body_excludes_photos_and_captions(photo_article):
    assert "<figure" not in photo_article.body_html
    assert "<figcaption" not in photo_article.body_html
    assert "<img" not in photo_article.body_html
    assert (
        "Andrea Egan speaking at the Durham Miners' Gala" not in photo_article.body_html
    )
