import requests
import json
import brotli

def test_product_details():
    """Test getting detailed product information"""
    
    # Try different product detail endpoints
    product_id = "63420489"
    
    endpoints_to_try = [
        f"https://search.vestiairecollective.com/v1/product/{product_id}",
        f"https://www.vestiairecollective.co.uk/api/v1/product/{product_id}",
        f"https://api.vestiairecollective.com/v1/product/{product_id}",
        f"https://search.vestiairecollective.com/v1/product/details/{product_id}",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.vestiairecollective.co.uk/',
        'Origin': 'https://www.vestiairecollective.co.uk',
    }
    
    for endpoint in endpoints_to_try:
        print(f"\n🔍 Testing endpoint: {endpoint}")
        
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"📊 Status: {response.status_code}")
            
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
                
                print(f"📄 Response (first 300 chars): {response_text[:300]}")
                
                try:
                    data = json.loads(response_text)
                    print(f"✅ JSON Response - Keys: {list(data.keys())}")
                    
                    # Look for price, brand, images
                    for key in data.keys():
                        if 'price' in key.lower():
                            print(f"💰 Price found in {key}: {data[key]}")
                        if 'brand' in key.lower():
                            print(f"🏷️ Brand found in {key}: {data[key]}")
                        if 'image' in key.lower():
                            print(f"🖼️ Image found in {key}: {data[key]}")
                    
                    return data
                    
                except json.JSONDecodeError:
                    print("❌ Not JSON response")
            else:
                print(f"❌ Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    return None

def test_alternative_search():
    """Test alternative search endpoints"""
    
    search_endpoints = [
        "https://www.vestiairecollective.co.uk/api/search",
        "https://api.vestiairecollective.com/v1/search",
        "https://search.vestiairecollective.com/v2/search",
        "https://search.vestiairecollective.com/v1/product/search/extended",
    ]
    
    params = {
        'q': 'chanel',
        'limit': 2,
        'include': ['price', 'brand', 'images']
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Referer': 'https://www.vestiairecollective.co.uk/',
    }
    
    for endpoint in search_endpoints:
        print(f"\n🔍 Testing search endpoint: {endpoint}")
        
        try:
            response = requests.get(endpoint, params=params, headers=headers, timeout=10)
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"📄 Response (first 300 chars): {response.text[:300]}")
                
                try:
                    data = json.loads(response.text)
                    print(f"✅ JSON Response - Keys: {list(data.keys())}")
                    return data
                except json.JSONDecodeError:
                    print("❌ Not JSON response")
            else:
                print(f"❌ Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    return None

if __name__ == "__main__":
    print("🔍 Testing product details endpoint...")
    product_data = test_product_details()
    
    print("\n🔍 Testing alternative search endpoints...")
    search_data = test_alternative_search()
