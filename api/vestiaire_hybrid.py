import requests
import json
import brotli
import re
from bs4 import BeautifulSoup
import time
import random

def get_vestiaire_product_details(product_url, product_id):
    """Get detailed product information by scraping the product page"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.vestiairecollective.co.uk/',
    }
    
    try:
        print(f"🔍 Scraping product details: {product_url}")
        response = requests.get(product_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract price
            price = 'Price not available'
            price_selectors = [
                '[data-testid="price"]',
                '.price',
                '.product-price',
                '[class*="price"]'
            ]
            
            for selector in price_selectors:
                price_elem = soup.select_one(selector)
                if price_elem:
                    price = price_elem.get_text(strip=True)
                    break
            
            # Extract brand
            brand = 'Unknown'
            brand_selectors = [
                '[data-testid="brand"]',
                '.brand',
                '.product-brand',
                '[class*="brand"]'
            ]
            
            for selector in brand_selectors:
                brand_elem = soup.select_one(selector)
                if brand_elem:
                    brand = brand_elem.get_text(strip=True)
                    break
            
            # Extract images
            images = []
            image_selectors = [
                '[data-testid="product-image"] img',
                '.product-image img',
                '.gallery img',
                'img[src*="vestiairecollective.com"]'
            ]
            
            for selector in image_selectors:
                img_elems = soup.select(selector)
                for img in img_elems:
                    src = img.get('src') or img.get('data-src')
                    if src and 'vestiairecollective.com' in src:
                        images.append(src)
                        break
                if images:
                    break
            
            # Extract condition
            condition = 'Good'
            condition_selectors = [
                '[data-testid="condition"]',
                '.condition',
                '.product-condition'
            ]
            
            for selector in condition_selectors:
                condition_elem = soup.select_one(selector)
                if condition_elem:
                    condition = condition_elem.get_text(strip=True)
                    break
            
            # Extract seller
            seller = 'vestiaire_seller'
            seller_selectors = [
                '[data-testid="seller"]',
                '.seller',
                '.product-seller'
            ]
            
            for selector in seller_selectors:
                seller_elem = soup.select_one(selector)
                if seller_elem:
                    seller = seller_elem.get_text(strip=True)
                    break
            
            return {
                'price': price,
                'brand': brand,
                'images': images,
                'condition': condition,
                'seller': seller
            }
        
        else:
            print(f"❌ Failed to fetch product page: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error scraping product details: {e}")
        return None

def scrape_vestiaire_with_details(search_text, page_number=1, items_per_page=5):
    """Enhanced Vestiaire scraper with detailed product information"""
    
    # First, get basic product list from search API
    api_url = "https://search.vestiairecollective.com/v1/product/search"
    
    params = {
        'q': search_text,
        'page': page_number,
        'limit': items_per_page,
        'sort': 'relevance',
        'category_id': '1',
        'gender': 'women',
        'locale': {'country': 'GB', 'language': 'en', 'currency': 'GBP'}
    }
    
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
        print(f"🔄 Getting product list from Vestiaire API...")
        response = requests.post(api_url, json=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Handle compression
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
            
            if 'items' in data:
                for item in data['items']:
                    try:
                        product_id = item.get('id', '')
                        title = item.get('name', '')
                        description = item.get('description', '')
                        relative_link = item.get('link', '')
                        product_url = f"https://www.vestiairecollective.co.uk{relative_link}" if relative_link else ''
                        
                        # Get detailed information
                        details = get_vestiaire_product_details(product_url, product_id)
                        
                        # Use scraped details or fallback to extracted info
                        price = details['price'] if details else 'Price not available'
                        if price == 'Price not available':
                            # Try to extract price from description
                            price_match = re.search(r'£(\d+(?:,\d+)*)', description)
                            if price_match:
                                price = f"£{price_match.group(1)}"
                        
                        brand = details['brand'] if details else 'Unknown'
                        if brand == 'Unknown':
                            # Extract brand from title/description
                            if 'chanel' in title.lower() or 'chanel' in description.lower():
                                brand = 'Chanel'
                            elif 'louis vuitton' in title.lower() or 'louis vuitton' in description.lower():
                                brand = 'Louis Vuitton'
                            elif 'hermès' in title.lower() or 'hermes' in description.lower():
                                brand = 'Hermès'
                            elif 'gucci' in title.lower() or 'gucci' in description.lower():
                                brand = 'Gucci'
                        
                        image_url = ''
                        if details and details['images']:
                            image_url = details['images'][0]
                        else:
                            # Generate placeholder image URL
                            image_url = f"https://images.vestiairecollective.com/images/resized/w=256,q=75,f=auto/produit/{product_id}_1.jpg"
                        
                        condition = details['condition'] if details else 'Good'
                        seller = details['seller'] if details else 'vestiaire_seller'
                        
                        product = {
                            'Title': title,
                            'Price': price,
                            'Brand': brand,
                            'Size': 'N/A',
                            'Image': image_url,
                            'Link': product_url,
                            'Condition': condition,
                            'Seller': seller,
                            'OriginalPrice': price,
                            'Discount': '0%'
                        }
                        
                        products.append(product)
                        print(f"✅ Processed: {brand} - {title[:50]}...")
                        
                        # Add delay to be respectful
                        time.sleep(random.uniform(1, 2))
                        
                    except Exception as e:
                        print(f"⚠️ Error processing product {item.get('id', 'unknown')}: {e}")
                        continue
            
            pagination_data = data.get('paginationStats', {})
            pagination = {
                'current_page': page_number,
                'total_pages': page_number + (1 if len(products) == items_per_page else 0),
                'has_more': len(products) == items_per_page,
                'items_per_page': len(products),
                'total_items': pagination_data.get('totalCount', len(products))
            }
            
            print(f"✅ Successfully processed {len(products)} products with detailed information")
            return {'products': products, 'pagination': pagination}
            
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            print(f"❌ Vestiaire API error: {error_msg}")
            raise Exception(f"Failed to fetch Vestiaire API: {error_msg}")
            
    except Exception as e:
        print(f"❌ Vestiaire scraping failed: {e}")
        raise e

# Test the function
if __name__ == "__main__":
    result = scrape_vestiaire_with_details("chanel", 1, 3)
    print(f"\n📊 Result: {len(result['products'])} products")
    for i, product in enumerate(result['products']):
        print(f"{i+1}. {product['Brand']} - {product['Title'][:40]}... - {product['Price']} - {product['Image'][:50]}...")
