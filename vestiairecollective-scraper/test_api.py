#!/usr/bin/env python3
"""
Simple test to verify Scrapfly API key and basic functionality
"""

import os
import asyncio
from scrapfly import ScrapeConfig, ScrapflyClient


async def test_scrapfly_api():
    """Test Scrapfly API key with a simple request"""
    api_key = os.getenv("SCRAPFLY_KEY")
    if not api_key:
        print("❌ SCRAPFLY_KEY environment variable not set")
        return False
    
    print("✅ API key found")
    
    client = ScrapflyClient(key=api_key, max_concurrent_scrapes=1)
    
    # Test with a simple website
    test_config = ScrapeConfig(
        url="https://httpbin.org/get",
        asp=False,  # Disable ASP for this test
        headers={"User-Agent": "Scrapfly Test"}
    )
    
    try:
        print("🔍 Testing Scrapfly API...")
        response = client.scrape(test_config)
        print("✅ Scrapfly API working!")
        print(f"📊 Response status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Scrapfly API error: {e}")
        return False


async def test_vestiaire_simple():
    """Test simple Vestiaire request without ASP"""
    api_key = os.getenv("SCRAPFLY_KEY")
    if not api_key:
        print("❌ SCRAPFLY_KEY environment variable not set")
        return False
    
    client = ScrapflyClient(key=api_key, max_concurrent_scrapes=1)
    
    # Test Vestiaire homepage without ASP first
    test_config = ScrapeConfig(
        url="https://www.vestiairecollective.com",
        asp=False,  # Start without ASP
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    )
    
    try:
        print("🔍 Testing Vestiaire homepage...")
        response = client.scrape(test_config)
        print("✅ Vestiaire homepage accessible!")
        print(f"📊 Response status: {response.status_code}")
        print(f"📏 Response size: {len(response.content)} bytes")
        return True
    except Exception as e:
        print(f"❌ Vestiaire homepage error: {e}")
        return False


async def test_vestiaire_with_asp():
    """Test Vestiaire with ASP enabled"""
    api_key = os.getenv("SCRAPFLY_KEY")
    if not api_key:
        print("❌ SCRAPFLY_KEY environment variable not set")
        return False
    
    client = ScrapflyClient(key=api_key, max_concurrent_scrapes=1)
    
    # Test with ASP enabled
    test_config = ScrapeConfig(
        url="https://www.vestiairecollective.com",
        asp=True,  # Enable ASP
        render_js=True,
        country="gb",
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    )
    
    try:
        print("🔍 Testing Vestiaire with ASP...")
        response = client.scrape(test_config)
        print("✅ Vestiaire with ASP working!")
        print(f"📊 Response status: {response.status_code}")
        print(f"📏 Response size: {len(response.content)} bytes")
        return True
    except Exception as e:
        print(f"❌ Vestiaire with ASP error: {e}")
        return False


async def main():
    """Run all tests"""
    print("🧪 Scrapfly & Vestiaire API Tests")
    print("=" * 40)
    
    # Test 1: Basic Scrapfly API
    print("\n1. Testing Scrapfly API...")
    api_works = await test_scrapfly_api()
    
    if not api_works:
        print("\n❌ Basic API test failed. Please check your API key.")
        return
    
    # Test 2: Vestiaire without ASP
    print("\n2. Testing Vestiaire without ASP...")
    vestiaire_simple = await test_vestiaire_simple()
    
    # Test 3: Vestiaire with ASP
    print("\n3. Testing Vestiaire with ASP...")
    vestiaire_asp = await test_vestiaire_with_asp()
    
    # Summary
    print("\n" + "=" * 40)
    print("📋 Test Summary:")
    print(f"   Scrapfly API: {'✅ Working' if api_works else '❌ Failed'}")
    print(f"   Vestiaire (no ASP): {'✅ Working' if vestiaire_simple else '❌ Failed'}")
    print(f"   Vestiaire (with ASP): {'✅ Working' if vestiaire_asp else '❌ Failed'}")
    
    if vestiaire_asp:
        print("\n🎉 All tests passed! The scraper should work.")
    elif vestiaire_simple:
        print("\n⚠️  Vestiaire is accessible but ASP may have issues.")
        print("   Try running the scraper with asp=False")
    else:
        print("\n❌ Vestiaire is not accessible. The site may be blocking requests.")
        print("   This could be due to:")
        print("   - Geographic restrictions")
        print("   - Rate limiting")
        print("   - Site protection changes")


if __name__ == "__main__":
    asyncio.run(main())
