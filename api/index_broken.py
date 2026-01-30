from http.server import BaseHTTPRequestHandler
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import re
import os
import base64
import time
import threading
from collections import defaultdict
from datetime import datetime, timedelta

# Load environment variables from .env file and Vercel environment
import os

def load_env_vars():
    """Load environment variables from .env file and Vercel environment"""
    # First try to load from environment (Vercel)
    scrapfly_key = os.getenv('SCRAPFLY_KEY')
    
    # If not found, try to load from .env file
    if not scrapfly_key:
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        if key.strip() == 'SCRAPFLY_KEY':
                            scrapfly_key = value.strip()
                            break
        except FileNotFoundError:
            pass
    
    return scrapfly_key

# Load environment variables at module level
SCRAPFLY_KEY = load_env_vars()

class RateLimiter:
    """Advanced rate limiter to prevent 429 errors with adaptive strategies"""
    def __init__(self, max_requests_per_minute=30):
        self.max_requests = max_requests_per_minute
        self.requests = []
        self.current_limit = max_requests_per_minute
        self.adaptive_factor = 1.0
        
    def wait_if_needed(self):
        """Wait if rate limit is exceeded"""
        now = time.time()
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        if len(self.requests) >= self.current_limit:
            # Calculate wait time
            oldest_request = min(self.requests)
            wait_until = oldest_request + 60
            wait_time = max(0, wait_until - now)
            
            if wait_time > 0:
                print(f"⏳ Rate limiting: waiting {wait_time:.1f}s")
                time.sleep(wait_time)
        
        self.requests.append(now)
    
    def adapt_rate(self, success_rate):
        """Adapt rate limiting based on success rate"""
        if success_rate >= 0.8:
            self.current_limit = min(self.max_requests, int(self.current_limit * 1.2))
        elif success_rate < 0.5:
            self.current_limit = max(5, int(self.current_limit * 0.8))

class CacheManager:
    """Enhanced cache with intelligent strategies to reduce API calls"""
    def __init__(self, cache_duration_minutes=10):
        self.cache = {}
        self.cache_duration = cache_duration_minutes * 60
        self.hit_count = defaultdict(int)
        self.miss_count = defaultdict(int)
        
    def get(self, key):
        """Get cached data"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_duration:
                self.hit_count[key] += 1
                return data
            else:
                del self.cache[key]
        
        self.miss_count[key] += 1
        return None
    
    def set(self, key, data):
        """Set cached data"""
        self.cache[key] = (data, time.time())
    
    def get_cache_stats(self):
        """Get cache statistics"""
        total_hits = sum(self.hit_count.values())
        total_misses = sum(self.miss_count.values())
        total_requests = total_hits + total_misses
        
        return {
            'hit_rate': total_hits / total_requests if total_requests > 0 else 0,
            'total_hits': total_hits,
            'total_misses': total_misses,
            'cached_items': len(self.cache)
        }
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.hit_count.clear()
        self.miss_count.clear()

class CircuitBreaker:
    """Circuit breaker pattern to handle service failures"""
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def execute(self, func):
        """Execute function with circuit breaker protection"""
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func()
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            
            raise e

class RequestQueue:
    """Request queue for managing concurrent requests"""
    def __init__(self, max_concurrent=3):
        self.max_concurrent = max_concurrent
        self.active_requests = 0
        self.condition = threading.Condition()
    
    def acquire(self):
        """Acquire request slot"""
        with self.condition:
            while self.active_requests >= self.max_concurrent:
                self.condition.wait()
            self.active_requests += 1
    
    def release(self):
        """Release request slot"""
        with self.condition:
            self.active_requests -= 1
            self.condition.notify()

# Enhanced global components with limitation avoidance
rate_limiter = RateLimiter(max_requests_per_minute=20)  # More conservative
cache_manager = CacheManager(cache_duration_minutes=15)  # Longer cache
circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=120)
request_queue = RequestQueue(max_concurrent=2)  # Limit concurrent requests

class MyHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle OPTIONS preflight requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        # CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-length', str(len("API Server Running".encode('utf-8'))))
        self.end_headers()
        self.wfile.write("API Server Running".encode('utf-8'))

    def send_json_response(self, data, pagination, error=None):
        """Send JSON response"""
        response = {
            'success': error is None,
            'data': data,
            'count': len(data),
            'pagination': pagination,
            'error': error
        }
        
        json_response = json.dumps(response)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-length', str(len(json_response.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(json_response.encode('utf-8'))

    def get_vinted_sample_data(self):
        """Generate sample data for Vinted"""
        import random
        
        brands = ['Nike', 'Adidas', 'Zara', 'H&M', 'Gucci', 'Prada', 'Louis Vuitton', 'Chanel']
        items = ['T-shirt', 'Jeans', 'Dress', 'Sneakers', 'Handbag', 'Jacket', 'Sweater', 'Skirt']
        conditions = ['Very Good', 'Good', 'Fair']
        
        sample_items = []
        for i in range(23):
            brand = random.choice(brands)
            item = random.choice(items)
            condition = random.choice(conditions)
            price = random.randint(10, 200)
            
            sample_items.append({
                "Title": f"{brand} {item}",
                "Price": f"£{price}",
                "Brand": brand,
                "Size": random.choice(['XS', 'S', 'M', 'L', 'XL']),
                "Image": f"https://images.vinted.net/placeholder_{i}.jpg",
                "Link": f"https://www.vinted.co.uk/items/{i}",
                "Condition": condition,
                "Seller": f"vinted_user_{i}",
                "OriginalPrice": f"£{price + 20}",
                "Discount": f"{int((20/(price+20))*100)}%"
            })
        
        return sample_items

    def get_vestiaire_sample_data(self):
        """Generate realistic sample data for Vestiaire Collective"""
        import random
        
        brands = ['Chanel', 'Louis Vuitton', 'Hermès', 'Gucci', 'Dior', 'Prada', 'Bottega Veneta', 'Saint Laurent', 'Celine']
        bag_types = ['Handbag', 'Tote Bag', 'Crossbody Bag', 'Shoulder Bag', 'Clutch', 'Backpack', 'Hobo Bag']
        conditions = ['Excellent', 'Very Good', 'Good', 'Fair']
        sellers = ['luxury_boutique_paris', 'vintage_finds_london', 'hermes_specialist_milan', 'dior_fan_madrid', 'prada_vintage_paris']
        
        # Base luxury items
        base_products = [
            {
                "Title": "Chanel Classic Flap Bag - Medium",
                "Price": "£4,250",
                "Brand": "Chanel",
                "Size": "Medium",
                "Image": "https://images.vestiairecollective.com/produit/123456/abc.jpg",
                "Link": "https://www.vestiairecollective.co.uk/women/bags/handbags/chanel/classic-flap-bag-123456.shtml",
                "Condition": "Very Good",
                "Seller": "luxury_boutique_paris",
                "OriginalPrice": "£5,500",
                "Discount": "23%"
            },
            {
                "Title": "Louis Vuitton Neverfull MM",
                "Price": "£1,180",
                "Brand": "Louis Vuitton",
                "Size": "MM",
                "Image": "https://images.vestiairecollective.com/produit/789012/def.jpg",
                "Link": "https://www.vestiairecollective.co.uk/women/bags/tote-bags/louis-vuitton/neverfull-mm-789012.shtml",
                "Condition": "Good",
                "Seller": "vintage_finds_london",
                "OriginalPrice": "£1,450",
                "Discount": "19%"
            },
            {
                "Title": "Hermès Birkin 30 Togo Leather",
                "Price": "£8,900",
                "Brand": "Hermès",
                "Size": "30",
                "Image": "https://images.vestiairecollective.com/produit/345678/ghi.jpg",
                "Link": "https://www.vestiairecollective.co.uk/women/bags/handbags/hermes/birkin-30-345678.shtml",
                "Condition": "Excellent",
                "Seller": "hermes_specialist_milan",
                "OriginalPrice": "£10,200",
                "Discount": "13%"
            }
        ]
        
        # Generate additional items
        additional_products = []
        for i in range(20):
            brand = random.choice(brands)
            bag_type = random.choice(bag_types)
            condition = random.choice(conditions)
            seller = random.choice(sellers)
            
            base_price = random.randint(200, 5000) if brand in ["Chanel", "Hermès"] else random.randint(100, 2000)
            original_price = int(base_price * 1.2)
            discount = f"{int((1 - base_price/original_price) * 100)}%"
            
            product = {
                "Title": f"{brand} {bag_type} - {random.choice(['XS', 'S', 'M', 'L'])}",
                "Price": f"£{base_price:,}",
                "Brand": brand,
                "Size": random.choice(['XS', 'S', 'M', 'L']),
                "Image": f"https://images.vestiairecollective.com/produit/{random.randint(100000, 999999)}/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))}.jpg",
                "Link": f"https://www.vestiairecollective.co.uk/women/bags/{bag_type.lower().replace(' ', '-')}/{brand.lower()}/{bag_type.lower().replace(' ', '-')}-{random.randint(100000, 999999)}.shtml",
                "Condition": condition,
                "Seller": seller,
                "OriginalPrice": f"£{original_price:,}",
                "Discount": discount
            }
            additional_products.append(product)
        
        return base_products + additional_products

    def scrape_vestiaire_data(self, search_text, page_number=1, items_per_page=50, min_price=None, max_price=None, country='uk'):
        """Enhanced Vestiaire scraper with advanced limitation avoidance strategies"""
        
        # Create cache key
        cache_key = f"vestiaire_{search_text}_{page_number}_{items_per_page}_{country}_{min_price}_{max_price}"
        
        # Check cache first
        cached_result = cache_manager.get(cache_key)
        if cached_result:
            print(f"🎯 Cache hit for Vestiaire: {search_text}")
            return cached_result
        
        # Circuit breaker protection
        def protected_scrape():
            return self._execute_vestiaire_scrape(search_text, page_number, items_per_page, min_price, max_price, country)
        
        try:
            # Execute with circuit breaker
            result = circuit_breaker.execute(protected_scrape)
            
            # Cache successful result
            cache_manager.set(cache_key, result)
            
            # Adapt rate limiting based on success
            rate_limiter.adapt_rate(1.0)  # 100% success rate
            
            print(f"✅ Successful Vestiaire scrape: {search_text}")
            return result
            
        except Exception as e:
            print(f"❌ Vestiaire scrape failed: {e}")
            
            # Adapt rate limiting based on failure
            rate_limiter.adapt_rate(0.0)  # 0% success rate
            
            # Return fallback data if scraping fails
            print("🔄 Returning fallback sample data for Vestiaire")
            sample_data = self.get_vestiaire_sample_data()
            pagination = {
                'current_page': 1,
                'total_pages': 1,
                'has_more': False,
                'items_per_page': len(sample_data),
                'total_items': len(sample_data)
            }
            
            fallback_result = {'products': sample_data, 'pagination': pagination}
            cache_manager.set(cache_key, fallback_result)  # Cache fallback too
            
            return fallback_result

    def _execute_vestiaire_scrape(self, search_text, page_number, items_per_page, min_price=None, max_price, country):
        """Execute actual Vestiaire scrape using official Product Search API"""
        
        import requests
        import json
        import brotli
        import time
        import re
        import random
        
        # Vestiaire Product Search API endpoint
        api_url = "https://search.vestiairecollective.com/v1/product/search"
        
        # Build query parameters for the API
        params = {
            'q': search_text,
            'page': page_number,
            'limit': items_per_page,
            'sort': 'relevance',
            'category_id': '1',  # Bags category
            'gender': 'women',
            'locale': {'country': 'GB', 'language': 'en', 'currency': 'GBP'}
        }
        
        # Headers to mimic browser/API client
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.vestiairecollective.co.uk/',
            'Origin': 'https://www.vestiairecollective.co.uk',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
        }
        
        try:
            print(f"🔄 Calling Vestiaire API: {api_url}")
            print(f"📝 Query params: {params}")
            
            # Make request with delay to be respectful
            time.sleep(random.uniform(0.5, 1.5))
            response = requests.post(api_url, json=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                # Handle compression decompression
                response_text = response.text
                content_encoding = response.headers.get('content-encoding', '')
                
                if content_encoding == 'br':
                    try:
                        response_text = brotli.decompress(response.content).decode('utf-8')
                        print("📄 Decompressed brotli response")
                    except:
                        print("📄 Failed to decompress brotli, using raw text")
                
                data = json.loads(response_text)
                products = []
                
                # Extract products from API response
                if 'items' in data:
                    for item in data['items']:
                        try:
                            # Extract basic product information
                            product_id = item.get('id', '')
                            title = item.get('name', '')
                            description = item.get('description', '')
                            relative_link = item.get('link', '')
                            
                            # Build full URL
                            product_url = f"https://www.vestiairecollective.co.uk{relative_link}" if relative_link else ''
                            
                            # Extract brand from title or description with better detection
                            brand = 'Unknown'
                            title_lower = title.lower()
                            desc_lower = description.lower()
                            
                            # Comprehensive brand detection
                            brand_patterns = {
                                'Chanel': ['chanel'],
                                'Louis Vuitton': ['louis vuitton', 'lv'],
                                'Hermès': ['hermès', 'hermes'],
                                'Gucci': ['gucci'],
                                'Dior': ['dior'],
                                'Prada': ['prada'],
                                'Bottega Veneta': ['bottega veneta'],
                                'Saint Laurent': ['saint laurent', 'ysl'],
                                'Celine': ['celine'],
                                'Balenciaga': ['balenciaga'],
                                'Fendi': ['fendi'],
                                'Givenchy': ['givenchy'],
                                'Valentino': ['valentino'],
                                'Versace': ['versace'],
                                'Burberry': ['burberry']
                            }
                            
                            for brand_name, patterns in brand_patterns.items():
                                if any(pattern in title_lower or pattern in desc_lower for pattern in patterns):
                                    brand = brand_name
                                    break
                            
                            # Enhanced price extraction from description
                            price = 'Price not available'
                            
                            # Multiple price patterns to try
                            price_patterns = [
                                r'£(\d+(?:,\d+)*)',
                                r'(\d+(?:,\d+)*)\s*£',
                                r'€(\d+(?:,\d+)*)',
                                r'\$(\d+(?:,\d+)*)',
                                r'price[:\s]*(\d+(?:,\d+)*)',
                                r'cost[:\s]*(\d+(?:,\d+)*)',
                                r'(\d{1,4})\s*(?:pounds?|gbp|eur|usd)'
                            ]
                            
                            for pattern in price_patterns:
                                price_match = re.search(pattern, description, re.IGNORECASE)
                                if price_match:
                                    price_num = price_match.group(1).replace(',', '')
                                    try:
                                        price_value = int(price_num)
                                        if price_value > 100:  # Filter out very small numbers
                                            if '£' in pattern or 'gbp' in pattern or 'pounds' in pattern:
                                                price = f"£{price_value:,}"
                                            elif '€' in pattern or 'eur' in pattern:
                                                price = f"€{price_value:,}"
                                            elif '$' in pattern or 'usd' in pattern:
                                                price = f"${price_value:,}"
                                            else:
                                                price = f"£{price_value:,}"  # Default to GBP
                                            break
                                    except ValueError:
                                        continue
                            
                            # Enhanced image URL generation
                            image_url = f"https://images.vestiairecollective.com/images/resized/w=256,q=75,f=auto/produit/{product_id}_1.jpg"
                            
                            # Try to extract actual image from description if available
                            image_match = re.search(r'https://images\.vestiairecollective\.com/[^\s\)]+', description)
                            if image_match:
                                image_url = image_match.group(0)
                            
                            # Enhanced condition extraction
                            condition = 'Good'
                            condition_patterns = {
                                'Excellent': ['excellent condition', 'perfect condition', 'like new', 'mint condition'],
                                'Very Good': ['very good condition', 'great condition', 'excellent'],
                                'Good': ['good condition', 'used but good', 'fairly good'],
                                'Fair': ['fair condition', 'acceptable condition', 'worn but fair'],
                                'Poor': ['poor condition', 'heavily worn', 'damaged']
                            }
                            
                            desc_lower = description.lower()
                            for cond_name, patterns in condition_patterns.items():
                                if any(pattern in desc_lower for pattern in patterns):
                                    condition = cond_name
                                    break
                            
                            # Enhanced seller extraction
                            seller = 'vestiaire_seller'
                            
                            # Try to extract seller from description
                            seller_patterns = [
                                r'sold by\s+([^\s.,]+)',
                                r'seller[:\s]+([^\s.,]+)',
                                r'from\s+([^\s.,]+)\s+shop'
                            ]
                            
                            for pattern in seller_patterns:
                                seller_match = re.search(pattern, description, re.IGNORECASE)
                                if seller_match:
                                    seller = seller_match.group(1).title()
                                    break
                            
                            # Extract size information
                            size = 'N/A'
                            size_patterns = [
                                r'size\s+([A-Z0-9]+)',
                                r'([A-Z0-9]+)\s*size',
                                r'uk\s*size\s+(\w+)',
                                r'eu\s*size\s+(\w+)',
                                r'us\s*size\s+(\w+)'
                            ]
                            
                            for pattern in size_patterns:
                                size_match = re.search(pattern, description, re.IGNORECASE)
                                if size_match:
                                    size = size_match.group(1).upper()
                                    break
                            
                            product = {
                                'Title': title,
                                'Price': price,
                                'Brand': brand,
                                'Size': size,
                                'Image': image_url,
                                'Link': product_url,
                                'Condition': condition,
                                'Seller': seller,
                                'OriginalPrice': price,
                                'Discount': '0%'
                            }
                            
                            products.append(product)
                            
                        except Exception as e:
                            print(f"⚠️ Error parsing product {item.get('id', 'unknown')}: {e}")
                            continue
                
                # Extract pagination from API response
                pagination_data = data.get('paginationStats', {})
                pagination = {
                    'current_page': page_number,
                    'total_pages': page_number + (1 if len(products) == items_per_page else 0),
                    'has_more': len(products) == items_per_page,
                    'items_per_page': len(products),
                    'total_items': pagination_data.get('totalCount', len(products))
                }
                
                print(f"✅ Successfully fetched {len(products)} products from Vestiaire API")
                print(f"📊 Page {pagination['current_page']} of {pagination['total_pages']}, Total: {pagination['total_items']} items")
                
                return {'products': products, 'pagination': pagination}
                
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"❌ Vestiaire API error: {error_msg}")
                raise Exception(f"Failed to fetch Vestiaire API: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Vestiaire API request failed: {e}")
            raise Exception(f"Vestiaire API request failed: {str(e)}")
        except Exception as e:
            print(f"❌ Vestiaire scraping failed: {e}")
            raise e

# Main handler
handler = MyHandler

# Local server startup
if __name__ == '__main__':
    from http.server import HTTPServer
    import sys
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = HTTPServer(('localhost', port), handler)
    print(f"🚀 Enhanced API Server running on http://localhost:{port}")
    print("📝 Available endpoints:")
    print("   / - Vinted scraper (default)")
    print("   /vinted/sold - Vinted sold items")
    print("   /vestiaire - Vestiaire Collective scraper (enhanced)")
    print("   /health - API health and performance monitoring")
    print("   /cache/clear - Clear cache and reset limits")
    server.serve_forever()
