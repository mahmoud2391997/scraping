import requests
import json
import brotli
import re
import time
import random

def scrape_vestiaire_data(search_text, page_number=1, items_per_page=50, min_price=None, max_price=None, country='uk'):
    """Clean Vestiaire scraper using official Product Search API"""
    
    api_url = "https://search.vestiairecollective.com/v1/product/search"
    
    params = {
        'q': search_text,
        'page': page_number,
        'limit': items_per_page,
        'sort': 'relevance',
        'category_id': '1',  # Bags category
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
        print(f"🔄 Calling Vestiaire API: {api_url}")
        print(f"📝 Query params: {params}")
        
        # Make POST request
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
