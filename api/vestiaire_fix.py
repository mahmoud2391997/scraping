import requests
import json
import gzip
import brotli

def test_vestiaire_api():
    """Test the Vestiaire Product Search API directly"""
    
    api_url = "https://search.vestiairecollective.com/v1/product/search"
    
    # Try both GET and POST
    methods_to_try = ['GET', 'POST']
    
    params = {
        'q': 'chanel',
        'page': 1,
        'limit': 3,
        'sort': 'relevance',
        'category_id': '1',
        'gender': 'women',
        'locale': {'country': 'GB', 'language': 'en', 'currency': 'GBP'},
        'include': ['price', 'brand', 'images', 'seller', 'condition']
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
        print("🔄 Testing Vestiaire API...")
        
        for method in methods_to_try:
            print(f"📡 Trying {method} request...")
            
            if method == 'POST':
                response = requests.post(api_url, json=params, headers=headers, timeout=15)
            else:
                response = requests.get(api_url, params=params, headers=headers, timeout=15)
            
            print(f"📊 {method} Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"📄 Response headers: {dict(response.headers)}")
                print(f"📄 Response content type: {response.headers.get('content-type')}")
                
                # Handle compression decompression
                response_text = response.text
                content_encoding = response.headers.get('content-encoding', '')
                
                if content_encoding == 'gzip':
                    try:
                        response_text = gzip.decompress(response.content).decode('utf-8')
                        print("📄 Decompressed gzip response")
                    except:
                        print("📄 Failed to decompress gzip, using raw text")
                elif content_encoding == 'br':
                    try:
                        response_text = brotli.decompress(response.content).decode('utf-8')
                        print("📄 Decompressed brotli response")
                    except:
                        print("📄 Failed to decompress brotli, using raw text")
                
                print(f"📄 Response text (first 500 chars): {response_text[:500]}")
                
                try:
                    data = json.loads(response_text)
                    print("✅ API Response received!")
                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error: {e}")
                    print(f"❌ Raw response: {response_text[:1000]}")
                    continue
                
                # Print the complete structure to find hidden fields
                print(f"� Complete response structure:")
                for key in data.keys():
                    if key != 'items':
                        print(f"  {key}: {type(data[key])}")
                        if isinstance(data[key], dict):
                            for subkey in data[key].keys():
                                print(f"    {subkey}: {type(data[key][subkey])}")
                
                # Print complete item structure for first product
                if 'items' in data and len(data['items']) > 0:
                    print(f"\n🔍 Complete item structure:")
                    first_item = data['items'][0]
                    for key in first_item.keys():
                        print(f"  {key}: {first_item[key]}")
                        if isinstance(first_item[key], dict):
                            for subkey in first_item[key].keys():
                                print(f"    {subkey}: {first_item[key][subkey]}")
                
                if 'pagination' in data:
                    pagination = data['pagination']
                    print(f"\n📄 Pagination: Page {pagination.get('page')} of {pagination.get('total_pages')}, Total: {pagination.get('total_count')} items")
                
                return data
                
            else:
                print(f"❌ {method} Error: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                continue
        
        print("❌ All methods failed")
        return None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

if __name__ == "__main__":
    test_vestiaire_api()
