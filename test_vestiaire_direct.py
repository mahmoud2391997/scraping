#!/usr/bin/env python3
"""
Simple test of Vestiaire API
"""

import requests
import json

def test_vestiaire_direct():
    """Test Vestiaire API directly"""
    print("🚀 Testing Vestiaire API Directly")
    print("=" * 40)
    
    # API endpoint
    url = "https://search.vestiairecollective.com/v1/product/search"
    
    # Headers
    headers = {
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
    }
    
    # Request body
    payload = {
        "pagination": {
            "page": 1,
            "pageSize": 5
        },
        "locale": {
            "country": "us",
            "language": "en",
            "currency": "USD"
        },
        "filters": {
            "gender": ["Women"],
            "categoryParent": ["Bags"]
        },
        "sort": {
            "by": "relevance",
            "direction": "desc"
        },
        "search": "chanel bag"
    }
    
    try:
        print("📡 Making request to Vestiaire API...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                items = data.get('items', [])
                print(f"✅ Success! Found {len(items)} items")
                
                if items:
                    print("\n📋 Sample items:")
                    for i, item in enumerate(items[:2], 1):
                        title = item.get('title', 'N/A')
                        brand = item.get('brand', 'N/A')
                        price_info = item.get('price', {})
                        price = f"{price_info.get('currency', 'USD')} {price_info.get('amount', 0)}"
                        print(f"\n{i}. {title}")
                        print(f"   Brand: {brand}")
                        print(f"   Price: {price}")
                        
                        # Images
                        images = item.get('images', [])
                        if images:
                            print(f"   Image: {images[0]}")
            except json.JSONDecodeError as e:
                print(f"✅ Success! But JSON parsing failed: {e}")
                print(f"Raw response: {response.text[:500]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_vestiaire_direct()
