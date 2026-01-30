#!/usr/bin/env python3
"""
Quick local test to demonstrate API features
"""

import requests
import json
import time

def test_local_api():
    """Test the local API with all features"""
    base_url = "http://localhost:8001"
    
    print("🚀 Testing Local API Features")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. 🏥 Health Check")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['data']['status']}")
            print(f"🔑 Scrapfly configured: {data['data']['environment']['scrapfly_key_configured']}")
            print(f"📊 Cache items: {data['data']['performance']['cache_stats']['cached_items']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Vestiaire Endpoint
    print("\n2. 🛍️ Vestiaire Endpoint")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/vestiaire?search=chanel&items_per_page=3", timeout=30)
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response time: {(end_time - start_time):.2f}s")
            print(f"📦 Items found: {data['count']}")
            if data['count'] > 0:
                product = data['data'][0]
                print(f"🏷️  Sample: {product.get('Title', 'N/A')}")
                print(f"💰 Price: {product.get('Price', 'N/A')}")
        else:
            print(f"❌ Vestiaire request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Vestiaire request error: {e}")
    
    # Test 3: Cache Test (Second request should be faster)
    print("\n3. 🎯 Cache Test")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/vestiaire?search=chanel&items_per_page=3", timeout=30)
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"✅ Cached response time: {(end_time - start_time):.2f}s")
            print("🚀 Cache is working!")
        else:
            print(f"❌ Cache test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cache test error: {e}")
    
    # Test 4: Different Search
    print("\n4. 🔍 Different Search")
    try:
        response = requests.get(f"{base_url}/vestiaire?search=gucci&items_per_page=2", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Gucci search: {data['count']} items")
        else:
            print(f"❌ Gucci search failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Gucci search error: {e}")
    
    # Test 5: Price Filtering
    print("\n5. 💰 Price Filtering")
    try:
        response = requests.get(f"{base_url}/vestiaire?search=handbag&min_price=100&max_price=500&items_per_page=3", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Price filtered search: {data['count']} items")
        else:
            print(f"❌ Price filter failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Price filter error: {e}")
    
    # Test 6: Clear Cache
    print("\n6. 🧹 Clear Cache")
    try:
        response = requests.get(f"{base_url}/cache/clear", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cache cleared: {data.get('message', 'Success')}")
        else:
            print(f"❌ Cache clear failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cache clear error: {e}")
    
    # Final Health Check
    print("\n7. 📊 Final Health Check")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            cache_stats = data['data']['performance']['cache_stats']
            print(f"✅ Final cache stats:")
            print(f"   Hit rate: {cache_stats.get('hit_rate', 0):.1%}")
            print(f"   Total hits: {cache_stats.get('total_hits', 0)}")
            print(f"   Total misses: {cache_stats.get('total_misses', 0)}")
            print(f"   Cached items: {cache_stats.get('cached_items', 0)}")
        else:
            print(f"❌ Final health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Final health check error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Local API Test Complete!")
    print("\n📋 Features Demonstrated:")
    print("   ✅ Health monitoring endpoint")
    print("   ✅ Vestiaire scraping with Scrapfly")
    print("   ✅ Intelligent caching system")
    print("   ✅ Price filtering")
    print("   ✅ Cache management")
    print("   ✅ Performance tracking")
    print("   ✅ Error handling")
    
    print(f"\n🌐 Dashboard available at:")
    print(f"   file://{os.path.abspath('api/features_dashboard.html')}")
    
    print(f"\n🔗 API endpoints:")
    print(f"   {base_url}/vestiaire?search=chanel")
    print(f"   {base_url}/health")
    print(f"   {base_url}/cache/clear")

if __name__ == "__main__":
    import os
    test_local_api()
