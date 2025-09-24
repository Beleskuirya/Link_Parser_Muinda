#!/usr/bin/env python3
"""
Test script for the African News Link Parser
Creates mock HTML content to test the parsing functionality
"""

from link_parser import AfricanNewsParser
import json

def create_mock_html():
    """Create mock HTML content for testing"""
    mock_rfi_html = """
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
    
    mock_france24_html = """
    <html>
    <body>
        <div class="articles">
            <a href="/fr/afrique/20240201-cameroun-sport">Cameroun : football africain</a>
            <a href="/fr/afrique/20240202-ghana-culture">Ghana : culture et traditions</a>
            <a href="/fr/afrique/20240203-egypte-tourisme">Égypte : relance du tourisme</a>
            <a href="/fr/asie/20240204-chine-news">Chine : actualités asiatiques</a>
            <a href="/fr/afrique/20240205-afrique-ouest">Afrique de l'Ouest : coopération régionale</a>
            <a href="/fr/afrique/20240206-madagascar-environnement">Madagascar : protection de l'environnement</a>
        </div>
    </body>
    </html>
    """
    
    return mock_rfi_html, mock_france24_html

def test_african_content_detection():
    """Test the African content detection functionality"""
    parser = AfricanNewsParser()
    
    test_cases = [
        ("Mali : nouvelles du Sahel", True),
        ("Sénégal : élections présidentielles", True),
        ("Nigeria : croissance économique", True),
        ("France : actualités européennes", False),
        ("Afrique de l'Ouest : coopération", True),
        ("Maghreb : développement", True),
        ("Congo RDC situation", True),
        ("Europe actualités", False),
    ]
    
    print("Testing African content detection:")
    for text, expected in test_cases:
        result = parser.is_african_content(text)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text}' -> {result} (expected: {expected})")

def test_parsing_logic():
    """Test the parsing logic with mock HTML"""
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    
    parser = AfricanNewsParser()
    mock_rfi_html, mock_france24_html = create_mock_html()
    
    # Test RFI parsing logic
    print("\nTesting RFI parsing logic:")
    soup = BeautifulSoup(mock_rfi_html, 'html.parser')
    base_url = "https://www.rfi.fr/fr/afrique/"
    articles = []
    
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if not href:
            continue
        
        full_url = urljoin(base_url, href)
        link_text = link.get_text(strip=True)
        
        if (parser.is_african_content(link_text, full_url) and 
            '/fr/afrique/' in full_url and 
            len(link_text) > 10):
            
            articles.append({
                'title': link_text,
                'url': full_url,
                'source': 'RFI'
            })
    
    print(f"Found {len(articles)} RFI articles:")
    for article in articles:
        print(f"  - {article['title']}")
    
    # Test France24 parsing logic
    print("\nTesting France24 parsing logic:")
    soup = BeautifulSoup(mock_france24_html, 'html.parser')
    base_url = "https://www.france24.com/fr/afrique/"
    articles = []
    
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if not href:
            continue
        
        full_url = urljoin(base_url, href)
        link_text = link.get_text(strip=True)
        
        if (parser.is_african_content(link_text, full_url) and 
            '/afrique/' in full_url and 
            len(link_text) > 10):
            
            articles.append({
                'title': link_text,
                'url': full_url,
                'source': 'France24'
            })
    
    print(f"Found {len(articles)} France24 articles:")
    for article in articles:
        print(f"  - {article['title']}")

if __name__ == "__main__":
    print("=== African News Link Parser - Test Suite ===\n")
    test_african_content_detection()
    test_parsing_logic()
    print("\n=== Test completed ===")