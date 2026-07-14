from unittest.mock import Mock, patch

import pytest
import requests

from wswsmd.fetch import TIMEOUT_SECONDS, fetch_html


def test_fetch_html_returns_response_text():
    mock_response = Mock()
    mock_response.text = "<html>ok</html>"
    mock_response.raise_for_status.return_value = None

    with patch("wswsmd.fetch.requests.get", return_value=mock_response) as mock_get:
        result = fetch_html("https://example.com/article")

    assert result == "<html>ok</html>"
    mock_get.assert_called_once_with(
        "https://example.com/article", timeout=TIMEOUT_SECONDS
    )


def test_fetch_html_raises_on_http_error():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404")

    with patch("wswsmd.fetch.requests.get", return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            fetch_html("https://example.com/missing")
