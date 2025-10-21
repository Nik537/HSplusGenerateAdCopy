import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re

class VigoShopScraper:
    """Scraper for vigoshop.si product pages"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_product(self, url: str) -> Dict:
        """
        Scrape product information from vigoshop.si URL

        Args:
            url: Product URL from vigoshop.si

        Returns:
            Dictionary with product data
        """
        try:
            # Validate URL
            if 'vigoshop.si' not in url:
                raise ValueError("URL must be from vigoshop.si")

            # Fetch page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # Extract product data
            product_data = {
                'url': url,
                'name': self._extract_name(soup),
                'price': self._extract_price(soup),
                'image_url': self._extract_image(soup),
                'features': self._extract_features(soup),
                'description': self._extract_description(soup),
                'category': self._extract_category(url, soup)
            }

            return product_data

        except requests.RequestException as e:
            raise Exception(f"Failed to fetch product page: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to scrape product: {str(e)}")

    def _extract_name(self, soup: BeautifulSoup) -> str:
        """Extract product name"""
        # Try multiple selectors
        selectors = [
            'h1.product_title',
            'h1.entry-title',
            '.product-title',
            'h1'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element and element.get_text(strip=True):
                return element.get_text(strip=True)

        return "Unknown Product"

    def _extract_price(self, soup: BeautifulSoup) -> str:
        """Extract product price"""
        # Try WooCommerce price selectors
        price_selectors = [
            '.woocommerce-Price-amount.amount',
            'span.price ins .woocommerce-Price-amount',
            'span.price .woocommerce-Price-amount',
            '.price',
        ]

        for selector in price_selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text(strip=True)
                # Extract just the number and currency
                match = re.search(r'[\d,\.]+\s*€', price_text)
                if match:
                    return match.group(0)

        return "Price not found"

    def _extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract main product image URL"""
        # Try multiple image selectors
        image_selectors = [
            '.woocommerce-product-gallery__image img',
            '.product-image img',
            'figure.woocommerce-product-gallery__wrapper img',
            '.product-images img'
        ]

        for selector in image_selectors:
            img = soup.select_one(selector)
            if img:
                # Try different attributes
                for attr in ['data-src', 'src', 'data-lazy-src']:
                    img_url = img.get(attr)
                    if img_url and img_url.startswith('http'):
                        return img_url

        return None

    def _extract_features(self, soup: BeautifulSoup) -> str:
        """Extract product features/highlights"""
        features = []

        # Look for features in common sections
        feature_sections = [
            '.woocommerce-product-details__short-description',
            '.product-short-description',
            '.entry-summary .woocommerce-product-details__short-description',
            '#tab-description'
        ]

        for selector in feature_sections:
            section = soup.select_one(selector)
            if section:
                # Extract list items if present
                list_items = section.find_all('li')
                if list_items:
                    features.extend([li.get_text(strip=True) for li in list_items[:5]])
                else:
                    # Get paragraph text
                    paragraphs = section.find_all('p')
                    for p in paragraphs[:3]:
                        text = p.get_text(strip=True)
                        if text and len(text) > 10:
                            features.append(text)

        if not features:
            # Try to get any description text
            desc = soup.select_one('.woocommerce-product-details__short-description')
            if desc:
                text = desc.get_text(strip=True)
                if text:
                    # Split into sentences and take first few
                    sentences = text.split('.')[:3]
                    features = [s.strip() + '.' for s in sentences if s.strip()]

        return ' | '.join(features) if features else "No features available"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract full product description"""
        desc_selectors = [
            '.woocommerce-product-details__short-description',
            '#tab-description',
            '.product-description'
        ]

        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(strip=True)
                if text:
                    return text[:500]  # Limit to 500 chars

        return "No description available"

    def _extract_category(self, url: str, soup: BeautifulSoup) -> str:
        """Extract product category"""
        # Try breadcrumbs
        breadcrumbs = soup.select('.woocommerce-breadcrumb a')
        if breadcrumbs and len(breadcrumbs) > 1:
            return breadcrumbs[-1].get_text(strip=True)

        # Try from URL
        if '/kategorija-izdelka/' in url:
            category = url.split('/kategorija-izdelka/')[-1].split('/')[0]
            return category.replace('-', ' ').title()

        return "General"
