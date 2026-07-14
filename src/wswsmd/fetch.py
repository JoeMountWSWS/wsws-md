import requests

TIMEOUT_SECONDS = 15


def fetch_html(url: str) -> str:
    """Fetch a URL and return its response body as text.

    Raises requests.RequestException (or a subclass) on network errors
    or non-2xx status codes.
    """
    response = requests.get(url, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.text
