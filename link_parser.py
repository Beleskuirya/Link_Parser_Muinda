#!/usr/bin/env python3
"""Link Parser for African News.

This module scrapes African news articles from selected news providers and
stores the results in JSON format.  It exposes a small CLI so the script can be
run manually or scheduled via a cron job / automation tool.
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from typing import Callable, Dict, List, Optional

import requests
from bs4 import BeautifulSoup
from requests import Response
from requests.exceptions import RequestException
from urllib.parse import urljoin

# Configure logging early so library consumers can override the level if needed.
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

REQUEST_DELAY_SECONDS = 1.0
DEFAULT_OUTPUT_FILE = "african_news_links.json"


class AfricanNewsParser:
    """Parse African news links from journal websites."""

    def __init__(self, session: Optional[requests.Session] = None) -> None:
        self.session = session or requests.Session()
        # Be polite and identify ourselves as a regular browser.
        self.session.headers.setdefault(
            "User-Agent",
            (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            ),
        )

        # Keywords to identify African content.
        self.african_keywords = {
            "countries": [
                "afrique",
                "africa",
                "algérie",
                "angola",
                "bénin",
                "botswana",
                "burkina",
                "burundi",
                "cameroun",
                "cap-vert",
                "centrafrique",
                "tchad",
                "comores",
                "congo",
                "djibouti",
                "égypte",
                "érythrée",
                "éthiopie",
                "gabon",
                "gambie",
                "ghana",
                "guinée",
                "kenya",
                "lesotho",
                "libéria",
                "libye",
                "madagascar",
                "malawi",
                "mali",
                "maroc",
                "maurice",
                "mauritanie",
                "mozambique",
                "namibie",
                "niger",
                "nigéria",
                "ouganda",
                "rwanda",
                "sénégal",
                "seychelles",
                "sierra",
                "somalie",
                "soudan",
                "tanzanie",
                "togo",
                "tunisie",
                "zambie",
                "zimbabwe",
                "côte",
                "ivoire",
            ],
            "regions": [
                "maghreb",
                "sahel",
                "afrique de l'ouest",
                "afrique centrale",
                "afrique de l'est",
                "afrique australe",
                "corne de l'afrique",
            ],
        }

    def is_african_content(self, text: str, url: str = "") -> bool:
        """Return ``True`` when ``text`` or ``url`` looks related to Africa."""

        if not text and not url:
            return False

        text_lower = text.lower() if text else ""
        url_lower = url.lower() if url else ""
        all_keywords = self.african_keywords["countries"] + self.african_keywords["regions"]

        return any(keyword in text_lower or keyword in url_lower for keyword in all_keywords)

    def _fetch(self, url: str) -> Optional[Response]:
        """Retrieve ``url`` using the configured session."""

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response
        except RequestException as exc:
            logger.error("Error fetching %s: %s", url, exc)
            return None

    def _extract_articles(
        self,
        soup: BeautifulSoup,
        base_url: str,
        source: str,
        url_filter: Callable[[str], bool],
    ) -> List[Dict[str, str]]:
        """Extract and normalise article data from a BeautifulSoup document."""

        seen_urls = set()
        articles: List[Dict[str, str]] = []

        for link in soup.find_all("a", href=True):
            href = link.get("href")
            if not href:
                continue

            full_url = urljoin(base_url, href)
            link_text = link.get_text(strip=True)

            if not link_text or len(link_text) <= 10:
                continue
            if not url_filter(full_url):
                continue
            if not self.is_african_content(link_text, full_url):
                continue

            if full_url in seen_urls:
                continue

            seen_urls.add(full_url)
            articles.append({"title": link_text, "url": full_url, "source": source})

        return articles

    def _fetch_and_extract(
        self,
        base_url: str,
        source: str,
        url_filter: Callable[[str], bool],
    ) -> List[Dict[str, str]]:
        """Convenience helper that fetches ``base_url`` and extracts articles."""

        response = self._fetch(base_url)
        if response is None:
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        return self._extract_articles(soup, base_url, source, url_filter)

    def scrape_rfi_links(self, base_url: str = "https://www.rfi.fr/fr/afrique/") -> List[Dict[str, str]]:
        """Scrape African news links from RFI."""

        logger.info("Scraping RFI African news from %s", base_url)
        return self._fetch_and_extract(base_url, "RFI", lambda url: "/fr/afrique/" in url)

    def scrape_france24_links(self, base_url: str = "https://www.france24.com/fr/afrique/") -> List[Dict[str, str]]:
        """Scrape African news links from France24."""

        logger.info("Scraping France24 African news from %s", base_url)
        return self._fetch_and_extract(base_url, "France24", lambda url: "/afrique/" in url)

    def parse_all_sites(self) -> List[Dict[str, str]]:
        """Parse all configured news sites for African news."""

        articles = self.scrape_rfi_links()
        time.sleep(REQUEST_DELAY_SECONDS)
        articles.extend(self.scrape_france24_links())
        logger.info("Total articles found: %d", len(articles))
        return articles

    def save_to_json(self, articles: List[Dict[str, str]], filename: str = DEFAULT_OUTPUT_FILE) -> None:
        """Persist the collected ``articles`` to ``filename``."""

        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(articles, file, ensure_ascii=False, indent=2)
            logger.info("Articles saved to %s", filename)
        except OSError as exc:
            logger.error("Error saving to %s: %s", filename, exc)


def build_argument_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""

    parser = argparse.ArgumentParser(
        description="Parse African news links from journal websites",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT_FILE, help="Output JSON file")
    parser.add_argument(
        "--site",
        choices=["rfi", "france24", "all"],
        default="all",
        help="Select which site(s) to scrape",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser


def main() -> None:
    """Entry point for the CLI interface."""

    parser = build_argument_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    news_parser = AfricanNewsParser()

    if args.site == "rfi":
        articles = news_parser.scrape_rfi_links()
    elif args.site == "france24":
        articles = news_parser.scrape_france24_links()
    else:
        articles = news_parser.parse_all_sites()

    if not articles:
        print("No African news articles found.")
        return

    news_parser.save_to_json(articles, args.output)

    print(f"\nFound {len(articles)} African news articles:")
    for index, article in enumerate(articles[:10], start=1):
        print(f"{index}. [{article['source']}] {article['title'][:80]}...")
        print(f"   URL: {article['url']}")

    if len(articles) > 10:
        print(f"... and {len(articles) - 10} more articles")

    print(f"\nAll articles saved to {args.output}")


if __name__ == "__main__":
    main()
