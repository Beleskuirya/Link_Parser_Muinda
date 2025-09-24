#!/usr/bin/env python3
"""Unit tests for the African News Link Parser."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import pytest
from bs4 import BeautifulSoup

from link_parser import AfricanNewsParser


@pytest.fixture(name="parser")
def fixture_parser() -> AfricanNewsParser:
    return AfricanNewsParser()


@pytest.fixture(name="mock_rfi_html")
def fixture_mock_rfi_html() -> str:
    return """
    <html>
    <body>
        <div class="content">
            <a href="/fr/afrique/20240101-mali-actualites">Mali : nouvelles du Sahel</a>
            <a href="/fr/afrique/20240102-senegal-politique">Sénégal : élections présidentielles</a>
            <a href="/fr/afrique/20240103-nigeria-economie">Nigeria : croissance économique en 2024</a>
            <a href="/fr/europe/20240104-france-news">France : actualités européennes</a>
            <a href="/fr/afrique/20240105-congo-rdc">RDC : situation politique au Congo</a>
            <a href="/fr/afrique/20240106-burkina-faso">Burkina Faso : développement rural</a>
            <a href="/fr/afrique/20240107-maghreb-tunisie">Tunisie : économie du Maghreb</a>
        </div>
    </body>
    </html>
    """


@pytest.fixture(name="mock_france24_html")
def fixture_mock_france24_html() -> str:
    return """
    <html>
    <body>
        <div class="articles">
            <a href="/fr/afrique/20240201-cameroun-sport">Cameroun : football africain</a>
            <a href="/fr/afrique/20240202-ghana-culture">Ghana : culture et traditions</a>
            <a href="/fr/afrique/20240203-egypte-tourisme">Égypte : relance du tourisme</a>
            <a href="/fr/asie/20240204-chine-news">Chine : actualités asiatiques</a>
            <a href="/fr/afrique/20240205-afrique-ouest">Afrique de l'Ouest : coopération régionale</a>
            <a href="/fr/afrique/20240206-madagascar-environnement">Madagascar : protection de l'environnement</a>
            <a href="/fr/afrique/20240201-cameroun-sport">Cameroun : football africain</a>
        </div>
    </body>
    </html>
    """


def test_is_african_content(parser: AfricanNewsParser) -> None:
    assert parser.is_african_content("Mali : nouvelles du Sahel") is True
    assert parser.is_african_content("France : actualités européennes") is False
    # URL keywords are also taken into account.
    assert parser.is_african_content("Football", "https://example.com/fr/afrique/foot") is True


def _extract_titles(articles: List[dict]) -> List[str]:
    return [article["title"] for article in articles]


def test_extract_articles_rfi(parser: AfricanNewsParser, mock_rfi_html: str) -> None:
    soup = BeautifulSoup(mock_rfi_html, "html.parser")
    articles = parser._extract_articles(
        soup,
        "https://www.rfi.fr/fr/afrique/",
        "RFI",
        lambda url: "/fr/afrique/" in url,
    )

    assert len(articles) == 6
    assert "France : actualités européennes" not in _extract_titles(articles)
    assert articles[0]["url"].startswith("https://www.rfi.fr/fr/afrique/")


def test_extract_articles_france24(parser: AfricanNewsParser, mock_france24_html: str) -> None:
    soup = BeautifulSoup(mock_france24_html, "html.parser")
    articles = parser._extract_articles(
        soup,
        "https://www.france24.com/fr/afrique/",
        "France24",
        lambda url: "/afrique/" in url,
    )

    assert len(articles) == 5
    # Duplicates are removed by URL.
    assert _extract_titles(articles).count("Cameroun : football africain") == 1


def test_save_to_json(tmp_path: Path, parser: AfricanNewsParser) -> None:
    articles = [
        {
            "title": "Mali : nouvelles du Sahel",
            "url": "https://www.rfi.fr/fr/afrique/20240101-mali-actualites",
            "source": "RFI",
        }
    ]
    output_file = tmp_path / "output.json"

    parser.save_to_json(articles, str(output_file))

    assert output_file.exists()
    assert json.loads(output_file.read_text(encoding="utf-8")) == articles


if __name__ == "__main__":
    pytest.main([__file__])
