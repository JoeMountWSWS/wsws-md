from pathlib import Path
from unittest.mock import patch

import pytest
import requests

from wswsmd import cli

FIXTURE = Path(__file__).parent / "fixtures" / "coeq-j03.html"
URL = "https://www.wsws.org/en/articles/2026/07/03/coeq-j03.html"


def test_build_parser_requires_url():
    parser = cli.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_build_parser_accepts_output_flag():
    parser = cli.build_parser()
    args = parser.parse_args([URL, "-o", "out.md"])
    assert args.url == URL
    assert args.output == "out.md"


def test_main_prints_markdown_to_stdout(capsys):
    html = FIXTURE.read_text()
    with patch("wswsmd.cli.fetch_html", return_value=html):
        exit_code = cli.main([URL])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "The Colorado primary" in captured.out


def test_main_writes_markdown_to_file(tmp_path):
    html = FIXTURE.read_text()
    output_file = tmp_path / "article.md"
    with patch("wswsmd.cli.fetch_html", return_value=html):
        exit_code = cli.main([URL, "-o", str(output_file)])

    assert exit_code == 0
    assert "The Colorado primary" in output_file.read_text()


def test_main_reports_fetch_errors(capsys):
    with patch("wswsmd.cli.fetch_html", side_effect=requests.ConnectionError("boom")):
        exit_code = cli.main([URL])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "failed to fetch" in captured.err


def test_main_reports_parse_errors(capsys):
    with patch("wswsmd.cli.fetch_html", return_value="<html><body></body></html>"):
        exit_code = cli.main([URL])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "wswsmd:" in captured.err
