from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag

TITLE_SUFFIX = " - World Socialist Web Site"


@dataclass
class Article:
    title: str
    author: str
    date_iso: str
    date_display: str
    url: str
    description: str
    body_html: str


def _meta_content(soup: BeautifulSoup, **attrs) -> str:
    tag = soup.find("meta", attrs=attrs)
    return tag["content"].strip() if tag and tag.get("content") else ""


def _extract_title(soup: BeautifulSoup) -> str:
    title = _meta_content(soup, property="og:title")
    if title:
        return title
    if soup.title and soup.title.string:
        text = soup.title.string.strip()
        if text.endswith(TITLE_SUFFIX):
            text = text[: -len(TITLE_SUFFIX)]
        return text
    return ""


def _extract_author(soup: BeautifulSoup) -> str:
    header = soup.find("header")
    if not header:
        return ""
    link = header.find("a", href=lambda h: h and h.startswith("/en/authors/"))
    return link.get_text(strip=True) if link else ""


def _extract_date(soup: BeautifulSoup) -> tuple[str, str]:
    header = soup.find("header")
    time_tag = header.find("time") if header else soup.find("time")
    if not time_tag:
        return "", ""
    return time_tag.get("datetime", "").strip(), time_tag.get_text(strip=True)


def _extract_body(soup: BeautifulSoup) -> Tag:
    section = soup.select_one('[itemprop="articleBody"]')
    if section is None:
        raise ValueError(
            "Could not find article body (no [itemprop=articleBody] element)"
        )

    # The real prose lives in a nested div.content; everything above it
    # (share-icon <ul>, layout <style>/<div> wrappers) is chrome, and
    # everything below/around it ("Read more", comments, related topics)
    # is a sibling, not part of the article.
    content = section.select_one("div.content") or section.find("div", recursive=False)
    if content is None:
        raise ValueError("Could not find article body content")

    # Widgets (audio player, newsletter signup, promo banners) are the
    # only direct-child <div>s here; real paragraphs are always <p>.
    for widget in content.find_all("div", recursive=False):
        widget.decompose()
    for aside in content.find_all("aside"):
        aside.decompose()
    # Photos are wrapped as <figure><img/><figcaption>...</figcaption></figure>;
    # dropping the whole <figure> removes the image and its caption together.
    for figure in content.find_all("figure"):
        figure.decompose()
    for tag in content.find_all(["script", "style", "svg"]):
        tag.decompose()
    for img in content.find_all("img"):
        classes = img.get("class") or []
        if "dn-m" in classes:
            img.decompose()

    return content


def parse_article(html: str, url: str) -> Article:
    soup = BeautifulSoup(html, "lxml")

    title = _extract_title(soup)
    if not title:
        raise ValueError(f"Could not find an article title at {url}")

    author = _extract_author(soup)
    date_iso, date_display = _extract_date(soup)
    description = _meta_content(soup, name="description")
    body = _extract_body(soup)

    return Article(
        title=title,
        author=author,
        date_iso=date_iso,
        date_display=date_display,
        url=url,
        description=description,
        body_html=body.decode_contents(),
    )
