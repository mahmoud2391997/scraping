#!/usr/bin/env python3
"""
Fetch 200 products from Vestiaire API
"""

import requests
import json
import time

def fetch_200_products():
    """Fetch 200 products from Vestiaire API"""
    print("🚀 Fetching 200 Products from Vestiaire API")
    print("=" * 50)
    
    url = "https://search.vestiairecollective.com/v1/product/search"
    
    headers = {
        'content-type': 'application/json',
        'x-siteid': '6',
        'x-language': 'us',
        'x-currency': 'USD',
        'origin': 'https://us.vestiairecollective.com',
        'referer': 'https://us.vestiairecollective.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'accept': 'application/json, text/plain, */*',
    }
    
    payload = {
        "pagination": {"page": 1, "pageSize": 200, "limit": 200},
        "locale": {"country": "us", "language": "en", "currency": "USD"},
        "filters": {},
        "sort": {"by": "relevance", "direction": "desc"},
    }
    
    try:
        print("📡 Making request for 200 products...")
        start_time = time.time()
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        end_time = time.time()
        print(f"⏱️  Response time: {(end_time - start_time):.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            print(f"✅ Success! Found {len(items)} products")
            
            # Save to file
            with open('vestiaire_200_products.json', 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Saved to vestiaire_200_products.json")
            
            # Show sample
            if items:
                print(f"\n📋 Sample products:")
                for i, item in enumerate(items[:10], 1):
                    title = item.get('name', 'N/A')
                    product_id = item.get('id', 'N/A')
                    link = item.get('link', 'N/A')
                    
                    print(f"\n{i}. {title}")
                    print(f"   ID: {product_id}")
                    print(f"   🔗: {link}")
            
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    success = fetch_200_products()
    
    if success:
        print(f"\n🎉 Successfully fetched 200 products!")
        print(f"💾 Data saved to: vestiaire_200_products.json")
        print(f"\n💡 Test with API server:")
        print(f'curl "http://localhost:8001/vestiaire?search=&items_per_page=200"')
    else:
        print(f"\n❌ Failed to fetch products")
