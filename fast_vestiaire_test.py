"""
Fast Vestiaire API scraper for testing
"""

import requests
import json
import time

def fast_vestiaire_test(search_query="chanel bag", items_per_page=3):
    """Fast test of Vestiaire API"""
    print(f"🚀 Fast Vestiaire API Test: {search_query}")
    
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
        "pagination": {"page": 1, "pageSize": items_per_page, "limit": items_per_page},
        "locale": {"country": "us", "language": "en", "currency": "USD"},
        "filters": {},  # Remove filters to get more results
        "sort": {"by": "relevance", "direction": "desc"},
        "search": search_query
    }
    
    try:
        print("📡 Making fast request...")
        start_time = time.time()
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        end_time = time.time()
        print(f"⏱️  Response time: {(end_time - start_time):.2f}s")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                items = data.get('items', [])
                print(f"✅ Success! Found {len(items)} items")
                print(f"📊 Full response keys: {list(data.keys())}")
                
                if 'totalCount' in data:
                    print(f"📈 Total count: {data['totalCount']}")
                
                if items:
                    print("\n📋 Results:")
                    for i, item in enumerate(items, 1):
                        print(f"\n{i}. Item keys: {list(item.keys())}")
                        title = item.get('title', item.get('name', 'N/A'))
                        brand = item.get('brand', item.get('brand_name', 'N/A'))
                        price_info = item.get('price', item.get('price_amount', {}))
                        if isinstance(price_info, dict):
                            price = f"{price_info.get('currency', 'USD')} {price_info.get('amount', 0)}"
                        else:
                            price = f"USD {price_info}"
                        
                        print(f"   Title: {title}")
                        print(f"   🏷️  Brand: {brand}")
                        print(f"   💰 Price: {price}")
                        
                        images = item.get('images', item.get('image_urls', []))
                        if images:
                            print(f"   🖼️  Image: {images[0][:60]}...")
                else:
                    print("📦 No items in response")
                    print(f"📄 Raw response: {json.dumps(data, indent=2)[:500]}...")
                
                return True
            except json.JSONDecodeError:
                print("✅ Status 200 but JSON parsing failed")
                print(f"Raw response: {response.text[:500]}...")
                return False
        else:
            print(f"❌ Error {response.status_code}: {response.text[:100]}...")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Fast Vestiaire API Test")
    print("=" * 40)
    
    success = fast_vestiaire_test("", 200)  # Fetch 200 products
    
    if success:
        print("\n🎉 API working! Ready for integration testing")
        print("\n💡 Test with curl:")
        print('curl "http://localhost:8001/vestiaire?search=chanel%20bag&items_per_page=3"')
    else:
        print("\n❌ API test failed")
