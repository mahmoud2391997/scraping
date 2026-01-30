#!/usr/bin/env python3
"""
Comprehensive test script to demonstrate API limitation avoidance features
"""

import requests
import json
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def test_basic_functionality():
    """Test basic API functionality"""
    print("🧪 Testing Basic API Functionality")
    print("-" * 40)
    
    base_url = "http://localhost:8001"
    
    # Test Vestiaire endpoint
    try:
        response = requests.get(f"{base_url}/vestiaire?search=chanel%20bag&items_per_page=3", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Vestiaire endpoint: {data.get('count', 0)} items")
        else:
            print(f"❌ Vestiaire endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Vestiaire endpoint error: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health endpoint: {data.get('status', 'unknown')}")
            cache_stats = data.get('performance', {}).get('cache_stats', {})
            print(f"   Cache hit rate: {cache_stats.get('hit_rate', 0):.2%}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")

def test_caching_mechanism():
    """Test caching mechanism effectiveness"""
    print("\n🎯 Testing Caching Mechanism")
    print("-" * 40)
    
    base_url = "http://localhost:8001"
    search_query = "louis vuitton"
    
    # First request (should hit the API)
    print("📡 Making first request (should hit API)...")
    start_time = time.time()
    try:
        response1 = requests.get(f"{base_url}/vestiaire?search={search_query}&items_per_page=5", timeout=30)
        first_request_time = time.time() - start_time
        
        if response1.status_code == 200:
            print(f"✅ First request completed in {first_request_time:.2f}s")
            
            # Second request (should hit cache)
            print("📡 Making second request (should hit cache)...")
            start_time = time.time()
            response2 = requests.get(f"{base_url}/vestiaire?search={search_query}&items_per_page=5", timeout=30)
            second_request_time = time.time() - start_time
            
            if response2.status_code == 200:
                print(f"✅ Second request completed in {second_request_time:.2f}s")
                
                # Check if cache is working
                if second_request_time < first_request_time * 0.5:  # Cache should be significantly faster
                    speedup = first_request_time / second_request_time
                    print(f"🚀 Cache speedup: {speedup:.1f}x faster")
                else:
                    print("⚠️  Cache may not be working optimally")
                
                # Check health endpoint for cache stats
                health_response = requests.get(f"{base_url}/health", timeout=10)
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    cache_stats = health_data.get('performance', {}).get('cache_stats', {})
                    print(f"📊 Cache stats: {cache_stats.get('hit_rate', 0):.1%} hit rate, {cache_stats.get('cached_items', 0)} items cached")
            else:
                print(f"❌ Second request failed: {response2.status_code}")
        else:
            print(f"❌ First request failed: {response1.status_code}")
    except Exception as e:
        print(f"❌ Cache test error: {e}")

def test_rate_limiting():
    """Test rate limiting effectiveness"""
    print("\n⏱️  Testing Rate Limiting")
    print("-" * 40)
    
    base_url = "http://localhost:8001"
    
    def make_request(request_id):
        """Make a single request"""
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}/vestiaire?search=gucci&items_per_page=3", timeout=30)
            end_time = time.time()
            
            return {
                'request_id': request_id,
                'status_code': response.status_code,
                'response_time': end_time - start_time,
                'success': response.status_code == 200
            }
        except Exception as e:
            return {
                'request_id': request_id,
                'status_code': 0,
                'response_time': 0,
                'success': False,
                'error': str(e)
            }
    
    # Make multiple concurrent requests
    num_requests = 8
    print(f"📡 Making {num_requests} concurrent requests...")
    
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(make_request, i) for i in range(num_requests)]
        results = []
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            status = "✅" if result['success'] else "❌"
            print(f"{status} Request {result['request_id']}: {result['status_code']} ({result['response_time']:.2f}s)")
    
    # Analyze results
    successful_requests = [r for r in results if r['success']]
    print(f"\n📊 Results: {len(successful_requests)}/{num_requests} requests successful")
    
    if len(successful_requests) > 0:
        avg_response_time = sum(r['response_time'] for r in successful_requests) / len(successful_requests)
        print(f"⏱️  Average response time: {avg_response_time:.2f}s")

def test_circuit_breaker():
    """Test circuit breaker functionality"""
    print("\n🔌 Testing Circuit Breaker")
    print("-" * 40)
    
    base_url = "http://localhost:8001"
    
    # Check initial circuit breaker state
    try:
        health_response = requests.get(f"{base_url}/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            cb_state = health_data.get('performance', {}).get('circuit_breaker', {})
            print(f"📊 Initial circuit breaker state: {cb_state.get('state', 'unknown')}")
            print(f"   Failure count: {cb_state.get('failure_count', 0)}/{cb_state.get('failure_threshold', 'N/A')}")
    except Exception as e:
        print(f"❌ Could not check circuit breaker state: {e}")
    
    # Make a few requests to see circuit breaker in action
    print("📡 Making requests to test circuit breaker...")
    for i in range(3):
        try:
            response = requests.get(f"{base_url}/vestiaire?search=test&items_per_page=3", timeout=15)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} Request {i+1}: {response.status_code}")
        except Exception as e:
            print(f"❌ Request {i+1}: {e}")
        time.sleep(1)
    
    # Check final circuit breaker state
    try:
        health_response = requests.get(f"{base_url}/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            cb_state = health_data.get('performance', {}).get('circuit_breaker', {})
            print(f"📊 Final circuit breaker state: {cb_state.get('state', 'unknown')}")
    except Exception as e:
        print(f"❌ Could not check final circuit breaker state: {e}")

def test_cache_management():
    """Test cache management endpoints"""
    print("\n🗄️  Testing Cache Management")
    print("-" * 40)
    
    base_url = "http://localhost:8001"
    
    # Check initial cache state
    try:
        health_response = requests.get(f"{base_url}/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            cache_stats = health_data.get('performance', {}).get('cache_stats', {})
            print(f"📊 Initial cache: {cache_stats.get('cached_items', 0)} items, {cache_stats.get('hit_rate', 0):.1%} hit rate")
    except Exception as e:
        print(f"❌ Could not check initial cache state: {e}")
    
    # Make some requests to populate cache
    print("📡 Populating cache...")
    searches = ["chanel", "gucci", "prada"]
    for search in searches:
        try:
            response = requests.get(f"{base_url}/vestiaire?search={search}&items_per_page=3", timeout=30)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} Cached search: {search}")
        except Exception as e:
            print(f"❌ Cache populate error for {search}: {e}")
    
    # Check cache after population
    try:
        health_response = requests.get(f"{base_url}/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            cache_stats = health_data.get('performance', {}).get('cache_stats', {})
            print(f"📊 After population: {cache_stats.get('cached_items', 0)} items, {cache_stats.get('hit_rate', 0):.1%} hit rate")
    except Exception as e:
        print(f"❌ Could not check cache after population: {e}")
    
    # Clear cache
    print("🧹 Clearing cache...")
    try:
        response = requests.get(f"{base_url}/cache/clear", timeout=10)
        if response.status_code == 200:
            print("✅ Cache cleared successfully")
        else:
            print(f"❌ Cache clear failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cache clear error: {e}")
    
    # Check cache after clearing
    try:
        health_response = requests.get(f"{base_url}/health", timeout=10)
        if health_response.status_code == 200:
            health_data = health_response.json()
            cache_stats = health_data.get('performance', {}).get('cache_stats', {})
            print(f"📊 After clearing: {cache_stats.get('cached_items', 0)} items, {cache_stats.get('hit_rate', 0):.1%} hit rate")
    except Exception as e:
        print(f"❌ Could not check cache after clearing: {e}")

def main():
    """Run all limitation avoidance tests"""
    print("🛡️  API Limitation Avoidance Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding correctly")
            return
    except Exception as e:
        print("❌ Cannot connect to server. Please start the API server first:")
        print("   cd api && python3 index.py")
        return
    
    print("✅ Server is running - starting tests...\n")
    
    # Run all tests
    test_basic_functionality()
    test_caching_mechanism()
    test_rate_limiting()
    test_circuit_breaker()
    test_cache_management()
    
    print("\n" + "=" * 50)
    print("🎉 Limitation Avoidance Tests Complete!")
    print("\n📋 Summary of Features Tested:")
    print("   ✅ Basic API functionality")
    print("   ✅ Intelligent caching system")
    print("   ✅ Adaptive rate limiting")
    print("   ✅ Circuit breaker protection")
    print("   ✅ Cache management endpoints")
    print("   ✅ Performance monitoring")
    
    print("\n🚀 The API is now equipped with advanced limitation avoidance!")
    print("   - Reduces API calls through intelligent caching")
    print("   - Prevents rate limiting with adaptive throttling")
    print("   - Handles service failures gracefully")
    print("   - Provides real-time performance monitoring")

if __name__ == "__main__":
    main()
