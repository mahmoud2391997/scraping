"""
Vestiairecollective.com API Scraper using Official API

This scraper uses the official Vestiaire API instead of HTML scraping
for better reliability and performance.
"""

import os
import json
import time
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
import requests
from urllib.parse import urljoin


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
    country: str


class VestiaireAPIScraper:
    """Official Vestiaire API scraper"""
    
    def __init__(self, scrapfly_api_key: str = None):
        """Initialize scraper with optional Scrapfly API key for fallback"""
        self.scrapfly_key = scrapfly_api_key
        self.base_url = "https://search.vestiairecollective.com/v1/product/search"
        self.session = requests.Session()
        
        # Realistic browser headers
        self.headers = {
            'content-type': 'application/json',
            'x-siteid': '6',
            'x-language': 'us',
            'x-currency': 'USD',
            'origin': 'https://us.vestiairecollective.com',
            'referer': 'https://us.vestiairecollective.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
        }
        
        self.session.headers.update(self.headers)
        
    def _get_random_proxy(self):
        """Get a random proxy for residential IP rotation"""
        # This would be configured with actual proxy service
        proxies = [
            # Add residential proxies here
        ]
        return random.choice(proxies) if proxies else None
    
    def _make_api_request(self, payload: Dict, max_retries: int = 3) -> Optional[Dict]:
        """Make API request with retry logic and rate limiting"""
        
        for attempt in range(max_retries):
            try:
                # Rate limiting: 1-2 requests per second
                # time.sleep(random.uniform(0.1, 0.3))  # Reduced delay for testing
                
                # Use proxy if available
                proxies = self._get_random_proxy()
                
                # Add country to headers if provided
                headers = self.headers.copy()
                if country and country.lower() != 'us':
                    headers['x-country'] = country.lower()
                
                response = self.session.post(
                    self.base_url,
                    json=payload,
                    timeout=10,  # Reduced timeout
                    proxies=proxies,
                    headers=headers
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    # Rate limited - wait longer
                    wait_time = 2 ** attempt
                    print(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                elif response.status_code in [403, 401]:
                    print(f"Blocked with status {response.status_code}")
                    if attempt == max_retries - 1:
                        return None
                    time.sleep(5)
                else:
                    print(f"API error {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        
        return None
    
    def _parse_product(self, item: Dict) -> Product:
        """Parse product from API response"""
        try:
            # Extract basic info using correct field names
            product_id = item.get('id', '')
            title = item.get('name', '')
            brand = item.get('brand', '')  # May not be in basic response
            
            # Price information - might not be in basic response
            price_info = item.get('price', {})
            if not price_info:
                price = 0.0
                currency = 'USD'
            else:
                price = float(price_info.get('amount', 0))
                currency = price_info.get('currency', 'USD')
            
            # Original price for discount calculation
            original_price_info = item.get('originalPrice', {})
            original_price = float(original_price_info.get('amount', 0)) if original_price_info else None
            
            # Calculate discount
            discount_percentage = None
            if original_price and original_price > price:
                discount_percentage = round((1 - price / original_price) * 100, 1)
            
            # Images
            images = item.get('images', [])
            image_url = images[0] if images else ''
            
            # Product URL
            product_url = item.get('link', f"https://www.vestiairecollective.com/p-{product_id}")
            
            # Seller information
            seller_info = item.get('seller', {})
            seller = seller_info.get('pseudo', '') if seller_info else ''
            
            # Condition
            condition = item.get('condition', '')
            
            # Size
            size = item.get('size', '')
            
            # Country
            country = item.get('country', '')
            
            return Product(
                id=product_id,
                title=title,
                price=price,
                original_price=original_price,
                currency=currency,
                brand=brand,
                size=size,
                condition=condition,
                image_url=image_url,
                product_url=product_url,
                seller=seller,
                discount_percentage=discount_percentage,
                country=country
            )
            
        except Exception as e:
            print(f"Error parsing product: {e}")
            return None
    
    def scrape_search_page(self, search_query: str, page: int = 1, country: str = "us", 
                         gender: List[str] = None, category: List[str] = None,
                         items_per_page: int = 48) -> List[Product]:
        """
        Scrape search results using official API
        
        Args:
            search_query: Search term (e.g., "chanel bag")
            page: Page number (default: 1)
            country: Country code (default: us)
            gender: Gender filter (e.g., ["Women"])
            category: Category filter (e.g., ["Bags"])
            items_per_page: Items per page (default: 48)
        """
        
        # Build API payload
        payload = {
            "pagination": {
                "page": page,
                "pageSize": items_per_page
            },
            "locale": {
                "country": country.upper(),
                "language": "en",
                "currency": "USD"
            },
            "filters": {
                "gender": gender or ["Women"],
                "categoryParent": category or ["Bags"]
            },
            "sort": {
                "by": "relevance",
                "direction": "desc"
            }
        }
        
        # Add search query if provided
        if search_query and search_query.strip():
            payload["search"] = search_query.strip()
        
        print(f"🔍 Searching Vestiaire API: {search_query} (page {page})")
        
        # Make API request
        response_data = self._make_api_request(payload)
        
        if not response_data:
            print("❌ API request failed")
            return []
        
        # Parse products from response
        products = []
        items = response_data.get('items', [])
        
        for item in items:
            product = self._parse_product(item)
            if product:
                products.append(product)
        
        print(f"✅ Found {len(products)} products on page {page}")
        
        # Check if there are more pages
        total_count = response_data.get('totalCount', 0)
        has_more = page * items_per_page < total_count
        
        if has_more:
            print(f"📄 More pages available (total: {total_count})")
        else:
            print("🏁 Last page reached")
        
        return products
    
    def scrape_with_fallback(self, search_query: str, page: int = 1, country: str = "us") -> List[Product]:
        """
        Scrape using official API with Scrapfly fallback
        """
        try:
            # Try official API first
            products = self.scrape_search_page(search_query, page, country)
            if products:
                return products
        except Exception as e:
            print(f"⚠️ Official API failed: {e}")
        
        # Fallback to Scrapfly HTML scraping
        if self.scrapfly_key:
            try:
                print("🔄 Falling back to Scrapfly HTML scraping...")
                from scrapfly import ScrapeConfig, ScrapflyClient
                
                client = ScrapflyClient(key=self.scrapfly_key)
                
                # Try multiple URL patterns
                urls = [
                    f"https://www.vestiairecollective.com/search/?q={search_query}&page={page}",
                    f"https://www.vestiairecollective.com/search/{search_query}?page={page}",
                    f"https://us.vestiairecollective.com/search/?q={search_query}&page={page}"
                ]
                
                for url in urls:
                    try:
                        config = ScrapeConfig(
                            url=url,
                            headers=self.headers,
                            country=country,
                            render_js=True
                        )
                        
                        response = client.scrape(config)
                        
                        if response.status_code == 200:
                            # Parse HTML response (simplified)
                            products = self._parse_html_response(response.content)
                            if products:
                                return products
                                
                    except Exception as e:
                        print(f"Scrapfly attempt failed: {e}")
                        continue
                
            except Exception as e:
                print(f"❌ Scrapfly fallback failed: {e}")
        
        return []
    
    def _parse_html_response(self, html_content: str) -> List[Product]:
        """
        Parse HTML response as fallback
        This is a simplified version - would need proper HTML parsing
        """
        # This would implement HTML parsing as fallback
        # For now, return empty list
        return []


def main():
    """Main function to test the scraper"""
    api_key = os.getenv('SCRAPFLY_KEY')
    
    if not api_key:
        print("❌ SCRAPFLY_KEY not found in environment")
        return
    
    scraper = VestiaireAPIScraper(scrapfly_api_key=api_key)
    
    # Test search
    print("🚀 Testing Vestiaire API Scraper")
    print("=" * 50)
    
    # Search for Chanel bags
    products = scraper.scrape_search_page(
        search_query="chanel bag",
        page=1,
        country="us",
        gender=["Women"],
        category=["Bags"],
        items_per_page=10
    )
    
    print(f"\n📦 Found {len(products)} products:")
    for i, product in enumerate(products[:5], 1):
        print(f"\n{i}. {product.title}")
        print(f"   💰 Price: {product.currency} {product.price}")
        print(f"   🏷️  Brand: {product.brand}")
        print(f"   📏 Size: {product.size or 'N/A'}")
        print(f"   📊 Condition: {product.condition}")
        print(f"   👤 Seller: {product.seller}")
        if product.discount_percentage:
            print(f"   🏷️  Discount: {product.discount_percentage}%")
        print(f"   🖼️  Image: {product.image_url}")
        print(f"   🔗 Link: {product.product_url}")
    
    # Save results
    if products:
        output_file = "results/vestiaire_api_results.json"
        os.makedirs("results", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump([
                {
                    'id': p.id,
                    'title': p.title,
                    'price': p.price,
                    'original_price': p.original_price,
                    'currency': p.currency,
                    'brand': p.brand,
                    'size': p.size,
                    'condition': p.condition,
                    'image_url': p.image_url,
                    'product_url': p.product_url,
                    'seller': p.seller,
                    'discount_percentage': p.discount_percentage,
                    'country': p.country
                }
                for p in products
            ], f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to {output_file}")


if __name__ == "__main__":
    main()
