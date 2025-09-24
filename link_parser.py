#!/usr/bin/env python3
"""
Link Parser for African News
A Python script that scrapes journal pages such as RFI or France24, 
and returns the links of African news articles.
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import argparse
import logging
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AfricanNewsParser:
    """Class to parse African news links from journal websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Keywords to identify African content
        self.african_keywords = {
            'countries': [
                'afrique', 'africa', 'algérie', 'angola', 'bénin', 'botswana', 'burkina', 'burundi',
                'cameroun', 'cap-vert', 'centrafrique', 'tchad', 'comores', 'congo', 'djibouti',
                'égypte', 'érythrée', 'éthiopie', 'gabon', 'gambie', 'ghana', 'guinée', 'kenya',
                'lesotho', 'libéria', 'libye', 'madagascar', 'malawi', 'mali', 'maroc', 'maurice',
                'mauritanie', 'mozambique', 'namibie', 'niger', 'nigéria', 'ouganda', 'rwanda',
                'sénégal', 'seychelles', 'sierra', 'somalie', 'soudan', 'tanzanie', 'togo',
                'tunisie', 'zambie', 'zimbabwe', 'côte', 'ivoire'
            ],
            'regions': [
                'maghreb', 'sahel', 'afrique de l\'ouest', 'afrique centrale', 'afrique de l\'est',
                'afrique australe', 'corne de l\'afrique'
            ]
        }
    
    def is_african_content(self, text: str, url: str = "") -> bool:
        """Check if content is related to Africa"""
        text_lower = text.lower()
        url_lower = url.lower()
        
        # Check for African keywords in text and URL
        all_keywords = self.african_keywords['countries'] + self.african_keywords['regions']
        
        for keyword in all_keywords:
            if keyword in text_lower or keyword in url_lower:
                return True
        
        return False
    
    def scrape_rfi_links(self, base_url: str = "https://www.rfi.fr/fr/afrique/") -> List[Dict[str, str]]:
        """Scrape African news links from RFI"""
        logger.info("Scraping RFI African news...")
        
        try:
            response = self.session.get(base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find article links
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if not href:
                    continue
                
                # Convert relative URLs to absolute
                full_url = urljoin(base_url, href)
                
                # Get link text
                link_text = link.get_text(strip=True)
                
                # Check if it's an African news article
                if (self.is_african_content(link_text, full_url) and 
                    '/fr/afrique/' in full_url and 
                    len(link_text) > 10):
                    
                    articles.append({
                        'title': link_text,
                        'url': full_url,
                        'source': 'RFI'
                    })
            
            # Remove duplicates
            seen_urls = set()
            unique_articles = []
            for article in articles:
                if article['url'] not in seen_urls:
                    seen_urls.add(article['url'])
                    unique_articles.append(article)
            
            logger.info(f"Found {len(unique_articles)} African news articles from RFI")
            return unique_articles
        
        except Exception as e:
            logger.error(f"Error scraping RFI: {e}")
            return []
    
    def scrape_france24_links(self, base_url: str = "https://www.france24.com/fr/afrique/") -> List[Dict[str, str]]:
        """Scrape African news links from France24"""
        logger.info("Scraping France24 African news...")
        
        try:
            response = self.session.get(base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find article links
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if not href:
                    continue
                
                # Convert relative URLs to absolute
                full_url = urljoin(base_url, href)
                
                # Get link text
                link_text = link.get_text(strip=True)
                
                # Check if it's an African news article
                if (self.is_african_content(link_text, full_url) and 
                    '/afrique/' in full_url and 
                    len(link_text) > 10):
                    
                    articles.append({
                        'title': link_text,
                        'url': full_url,
                        'source': 'France24'
                    })
            
            # Remove duplicates
            seen_urls = set()
            unique_articles = []
            for article in articles:
                if article['url'] not in seen_urls:
                    seen_urls.add(article['url'])
                    unique_articles.append(article)
            
            logger.info(f"Found {len(unique_articles)} African news articles from France24")
            return unique_articles
        
        except Exception as e:
            logger.error(f"Error scraping France24: {e}")
            return []
    
    def parse_all_sites(self) -> List[Dict[str, str]]:
        """Parse all configured news sites for African news"""
        all_articles = []
        
        # Scrape RFI
        rfi_articles = self.scrape_rfi_links()
        all_articles.extend(rfi_articles)
        
        # Add delay between requests
        time.sleep(1)
        
        # Scrape France24
        france24_articles = self.scrape_france24_links()
        all_articles.extend(france24_articles)
        
        logger.info(f"Total articles found: {len(all_articles)}")
        return all_articles
    
    def save_to_json(self, articles: List[Dict[str, str]], filename: str = "african_news_links.json"):
        """Save articles to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            logger.info(f"Articles saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Parse African news links from journal websites')
    parser.add_argument('--output', '-o', default='african_news_links.json', 
                       help='Output JSON file (default: african_news_links.json)')
    parser.add_argument('--site', choices=['rfi', 'france24', 'all'], default='all',
                       help='Which site to scrape (default: all)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize parser
    news_parser = AfricanNewsParser()
    
    # Parse based on site selection
    if args.site == 'rfi':
        articles = news_parser.scrape_rfi_links()
    elif args.site == 'france24':
        articles = news_parser.scrape_france24_links()
    else:
        articles = news_parser.parse_all_sites()
    
    # Save results
    if articles:
        news_parser.save_to_json(articles, args.output)
        
        # Print summary
        print(f"\nFound {len(articles)} African news articles:")
        for i, article in enumerate(articles[:10], 1):  # Show first 10
            print(f"{i}. [{article['source']}] {article['title'][:80]}...")
            print(f"   URL: {article['url']}")
        
        if len(articles) > 10:
            print(f"... and {len(articles) - 10} more articles")
        
        print(f"\nAll articles saved to {args.output}")
    else:
        print("No African news articles found.")

if __name__ == "__main__":
    main()