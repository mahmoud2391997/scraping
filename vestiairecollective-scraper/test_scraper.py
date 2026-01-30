#!/usr/bin/env python3
"""
Simple test to demonstrate the working Vestiairecollective scraper
"""

import os
from vestiairecollective import VestiaireScraper


def test_scraper():
    """Test the Vestiairecollective scraper"""
    print("🧪 Testing Vestiairecollective Scraper")
    print("=" * 50)
    
    # Get API key
    api_key = os.getenv("SCRAPFLY_KEY")
    if not api_key:
        print("❌ SCRAPFLY_KEY not found in environment")
        print("Please set your API key:")
        print("export SCRAPFLY_KEY='your-api-key-here'")
        return
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Initialize scraper
    scraper = VestiaireScraper(api_key)
    
    # Test search
    print("\n🔍 Testing search functionality...")
    try:
        products = scraper.scrape_search_page("chanel bag", page=1, country="uk")
        
        if products:
            print(f"✅ Found {len(products)} products")
            
            # Show first product
            if products:
                product = products[0]
                print(f"\n📦 Sample Product:")
                print(f"   Title: {product.title}")
                print(f"   Price: {product.currency} {product.price}")
                print(f"   Brand: {product.brand}")
                print(f"   URL: {product.product_url}")
                
                # Save results
                scraper.save_to_json(products, "results/test_search.json")
                scraper.save_to_csv(products, "results/test_search.csv")
                print(f"\n💾 Results saved to results/")
        else:
            print("❌ No products found")
            
    except Exception as e:
        print(f"❌ Search error: {e}")
    
    print("\n🎉 Scraper test completed!")


if __name__ == "__main__":
    test_scraper()
