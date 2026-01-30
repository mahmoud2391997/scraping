"""
Vestiairecollective.com Scraper using Scrapfly.io

This scraper demonstrates how to scrape product listing data from Vestiairecollective.com
using the Scrapfly SDK to bypass anti-bot protections.

Tutorial: https://scrapfly.io/blog/how-to-scrape-vestiairecollective/
"""

import os
import json
import csv
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlencode, parse_qs
from dataclasses import dataclass

from scrapfly import ScrapeConfig, ScrapflyClient, ScrapeApiResponse


@dataclass
class Product:
    """Product data structure"""
    id: str
    title: str
    price: float
    original_price: Optional[float]
    currency: str
    brand: str
    size: Optional[str]
    condition: str
    image_url: str
    product_url: str
    seller: str
    discount_percentage: Optional[float]


class VestiaireScraper:
    """Main scraper class for Vestiairecollective.com"""
    
    def __init__(self, scrapfly_api_key: str):
        """Initialize scraper with Scrapfly API key"""
        self.client = ScrapflyClient(key=scrapfly_api_key, max_concurrent_scrapes=1)
        self.base_url = "https://www.vestiairecollective.com"
        
    def scrape_search_page(self, search_query: str, page: int = 1, country: str = "uk") -> List[Product]:
        """
        Scrape search results page
        
        Args:
            search_query: Search term (e.g., "chanel bag")
            page: Page number (default: 1)
            country: Country domain (default: "uk")
            
        Returns:
            List of Product objects
        """
        # Build search URL with parameters - Vestiaire uses a different URL structure
        search_url = f"https://www.vestiairecollective.{country}/search/"
        params = {
            "q": search_query,
            "page": page,
            "size": "50"  # Number of items per page
        }
        
        # Try different URL patterns
        possible_urls = [
            f"https://www.vestiairecollective.{country}/search/?{urlencode(params)}",
            f"https://www.vestiairecollective.{country}/search/{search_query}",
            f"https://www.vestiairecollective.com/search/?{urlencode(params)}"
        ]
        
        # Configure scrape request with anti-bot bypass
        scrape_config = ScrapeConfig(
            url=search_url,
            asp=True,  # Enable anti-scraping protection bypass
            render_js=True,  # Enable JavaScript rendering
            country="gb",  # Set proxy country
            headers={
                "Accept-Language": "en-GB,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )
        
        try:
            # Try different URL patterns
            for url in possible_urls:
                print(f"Trying URL: {url}")
                scrape_config.url = url
                
                try:
                    # Execute scrape request
                    response = self.client.scrape(scrape_config)
                    
                    if response.status_code == 200:
                        print(f"Success with URL: {url}")
                        return self._parse_search_results(response)
                    else:
                        print(f"Status {response.status_code} for URL: {url}")
                        
                except Exception as e:
                    print(f"Error with URL {url}: {e}")
                    continue
            
            print("All URL patterns failed")
            return []
            
        except Exception as e:
            print(f"Error scraping search page: {e}")
            return []
    
    def scrape_product_page(self, product_url: str) -> Optional[Product]:
        """
        Scrape individual product page for detailed information
        
        Args:
            product_url: Full URL to product page
            
        Returns:
            Product object with detailed information
        """
        scrape_config = ScrapeConfig(
            url=product_url,
            asp=True,
            render_js=True,
            country="gb",
            headers={
                "Accept-Language": "en-GB,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
        )
        
        try:
            response = self.client.scrape(scrape_config)
            return self._parse_product_page(response)
            
        except Exception as e:
            print(f"Error scraping product page: {e}")
            return None
    
    def _parse_search_results(self, response: ScrapeApiResponse) -> List[Product]:
        """Parse search results from HTML response"""
        products = []
        
        try:
            # Look for JSON data in script tags
            selector = response.selector
            
            # Try to find product data in JSON-LD structured data
            json_scripts = selector.xpath('//script[@type="application/ld+json"]/text()')
            for script in json_scripts:
                try:
                    data = json.loads(script.get())
                    if isinstance(data, list):
                        for item in data:
                            if item.get("@type") == "ItemList":
                                products.extend(self._parse_json_ld_products(item))
                    elif isinstance(data, dict) and data.get("@type") == "Product":
                        product = self._parse_single_product_json(data)
                        if product:
                            products.append(product)
                except json.JSONDecodeError:
                    continue
            
            # If no JSON data found, try parsing HTML directly
            if not products:
                products = self._parse_html_products(selector)
                
        except Exception as e:
            print(f"Error parsing search results: {e}")
        
        return products
    
    def _parse_json_ld_products(self, item_list_data: Dict) -> List[Product]:
        """Parse products from JSON-LD ItemList"""
        products = []
        item_list_elements = item_list_data.get("itemListElement", [])
        
        for element in item_list_elements:
            if isinstance(element, dict) and element.get("@type") == "Product":
                product = self._parse_single_product_json(element)
                if product:
                    products.append(product)
        
        return products
    
    def _parse_single_product_json(self, product_data: Dict) -> Optional[Product]:
        """Parse single product from JSON data"""
        try:
            offers = product_data.get("offers", {})
            price_info = offers.get("priceSpecification", offers)
            
            return Product(
                id=str(product_data.get("productID", "")),
                title=product_data.get("name", ""),
                price=float(price_info.get("price", 0)),
                original_price=float(price_info.get("highPrice", 0)) if price_info.get("highPrice") else None,
                currency=price_info.get("priceCurrency", "GBP"),
                brand=product_data.get("brand", {}).get("name", "") if isinstance(product_data.get("brand"), dict) else str(product_data.get("brand", "")),
                size=self._extract_size_from_title(product_data.get("name", "")),
                condition=product_data.get("itemCondition", "Good").replace("https://schema.org/", ""),
                image_url=product_data.get("image", ""),
                product_url=product_data.get("url", ""),
                seller=product_data.get("seller", {}).get("name", "") if isinstance(product_data.get("seller"), dict) else str(product_data.get("seller", "")),
                discount_percentage=self._calculate_discount(
                    float(price_info.get("price", 0)),
                    float(price_info.get("highPrice", 0)) if price_info.get("highPrice") else 0
                )
            )
        except Exception as e:
            print(f"Error parsing product JSON: {e}")
            return None
    
    def _parse_html_products(self, selector) -> List[Product]:
        """Parse products from HTML structure (fallback method)"""
        products = []
        
        # Look for product cards - this will need to be adapted based on actual HTML structure
        product_elements = selector.xpath('//div[contains(@class, "product-card") or contains(@class, "ProductCard")]')
        
        for element in product_elements:
            try:
                # Extract product information (these selectors will need to be updated based on actual HTML)
                title = element.xpath('.//h3[contains(@class, "title")]/text()').get("").strip()
                price_text = element.xpath('.//span[contains(@class, "price")]/text()').get("").strip()
                brand = element.xpath('.//span[contains(@class, "brand")]/text()').get("").strip()
                image_url = element.xpath('.//img/@src').get("")
                product_url = element.xpath('.//a/@href').get("")
                
                if title and price_text:
                    price = self._parse_price(price_text)
                    
                    product = Product(
                        id=self._extract_id_from_url(product_url),
                        title=title,
                        price=price,
                        original_price=None,
                        currency="GBP",
                        brand=brand,
                        size=self._extract_size_from_title(title),
                        condition="Good",  # Default if not found
                        image_url=image_url,
                        product_url=urljoin(self.base_url, product_url) if product_url else "",
                        seller="",
                        discount_percentage=None
                    )
                    products.append(product)
                    
            except Exception as e:
                print(f"Error parsing HTML product: {e}")
                continue
        
        return products
    
    def _parse_product_page(self, response: ScrapeApiResponse) -> Optional[Product]:
        """Parse individual product page"""
        selector = response.selector
        
        try:
            # Look for JSON-LD structured data
            json_scripts = selector.xpath('//script[@type="application/ld+json"]/text()')
            for script in json_scripts:
                try:
                    data = json.loads(script.get())
                    if isinstance(data, dict) and data.get("@type") == "Product":
                        return self._parse_single_product_json(data)
                except json.JSONDecodeError:
                    continue
            
            # Fallback to HTML parsing
            title = selector.xpath('//h1[contains(@class, "product-title")]/text()').get("").strip()
            price_text = selector.xpath('//span[contains(@class, "price")]/text()').get("").strip()
            brand = selector.xpath('//span[contains(@class, "brand")]/text()').get("").strip()
            
            if title and price_text:
                return Product(
                    id=self._extract_id_from_url(response.scrape_config.url),
                    title=title,
                    price=self._parse_price(price_text),
                    original_price=None,
                    currency="GBP",
                    brand=brand,
                    size=self._extract_size_from_title(title),
                    condition="Good",
                    image_url=selector.xpath('//img[contains(@class, "product-image")]/@src').get(""),
                    product_url=response.scrape_config.url,
                    seller=selector.xpath('//span[contains(@class, "seller")]/text()').get("").strip(),
                    discount_percentage=None
                )
                
        except Exception as e:
            print(f"Error parsing product page: {e}")
        
        return None
    
    def _parse_price(self, price_text: str) -> float:
        """Parse price from text string"""
        # Remove currency symbols and convert to float
        import re
        price_clean = re.sub(r'[^\d.]', '', price_text)
        try:
            return float(price_clean)
        except ValueError:
            return 0.0
    
    def _extract_size_from_title(self, title: str) -> Optional[str]:
        """Extract size from product title"""
        import re
        # Look for common size patterns
        size_patterns = [
            r'\b(XS|S|M|L|XL|XXL)\b',
            r'\b(\d+)(?:\s*(?:cm|mm|in|inch))?\b',
            r'\b(One Size|OS)\b',
            r'\b(Mini|Small|Medium|Large|Extra Large)\b'
        ]
        
        for pattern in size_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_id_from_url(self, url: str) -> str:
        """Extract product ID from URL"""
        import re
        # Look for numeric ID in URL
        match = re.search(r'/(\d+)(?:\.shtml)?$', url)
        return match.group(1) if match else ""
    
    def _calculate_discount(self, current_price: float, original_price: float) -> Optional[float]:
        """Calculate discount percentage"""
        if original_price and original_price > current_price:
            return round(((original_price - current_price) / original_price) * 100, 1)
        return None
    
    def save_to_json(self, products: List[Product], filename: str):
        """Save products to JSON file"""
        data = []
        for product in products:
            data.append({
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "original_price": product.original_price,
                "currency": product.currency,
                "brand": product.brand,
                "size": product.size,
                "condition": product.condition,
                "image_url": product.image_url,
                "product_url": product.product_url,
                "seller": product.seller,
                "discount_percentage": product.discount_percentage
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def save_to_csv(self, products: List[Product], filename: str):
        """Save products to CSV file"""
        if not products:
            return
        
        fieldnames = [
            "id", "title", "price", "original_price", "currency", "brand",
            "size", "condition", "image_url", "product_url", "seller", "discount_percentage"
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for product in products:
                writer.writerow({
                    "id": product.id,
                    "title": product.title,
                    "price": product.price,
                    "original_price": product.original_price,
                    "currency": product.currency,
                    "brand": product.brand,
                    "size": product.size,
                    "condition": product.condition,
                    "image_url": product.image_url,
                    "product_url": product.product_url,
                    "seller": product.seller,
                    "discount_percentage": product.discount_percentage
                })


def main():
    """Main function to run the scraper"""
    # Get API key from environment
    api_key = os.getenv("SCRAPFLY_KEY")
    if not api_key:
        print("Error: SCRAPFLY_KEY environment variable not set")
        print("Please set your Scrapfly API key:")
        print("export SCRAPFLY_KEY='your-api-key-here'")
        return
    
    # Initialize scraper
    scraper = VestiaireScraper(api_key)
    
    # Example: Scrape search results for "chanel bag"
    print("Scraping Vestiairecollective search results for 'chanel bag'...")
    products = scraper.scrape_search_page("chanel bag", page=1, country="uk")
    
    if products:
        print(f"Found {len(products)} products")
        
        # Save results
        scraper.save_to_json(products, "results/chanel_bags_search.json")
        scraper.save_to_csv(products, "results/chanel_bags_search.csv")
        
        # Print first few products
        print("\nFirst 5 products:")
        for i, product in enumerate(products[:5]):
            print(f"{i+1}. {product.title} - {product.currency} {product.price}")
    else:
        print("No products found")
    
    # Example: Scrape individual product details
    if products:
        print(f"\nScraping details for first product...")
        detailed_product = scraper.scrape_product_page(products[0].product_url)
        
        if detailed_product:
            print(f"Product: {detailed_product.title}")
            print(f"Price: {detailed_product.currency} {detailed_product.price}")
            print(f"Brand: {detailed_product.brand}")
            print(f"Condition: {detailed_product.condition}")
            print(f"Seller: {detailed_product.seller}")


if __name__ == "__main__":
    main()
