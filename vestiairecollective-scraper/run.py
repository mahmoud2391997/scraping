#!/usr/bin/env python3
"""
Example usage of the Vestiairecollective scraper

This file demonstrates how to use the Vestiairecollective scraper
to extract product data from Vestiairecollective.com.
"""

import asyncio
import os
from vestiairecollective import VestiaireScraper


async def example_search_scraping():
    """Example: Scrape search results"""
    print("=== Search Scraping Example ===")
    
    # Get API key from environment
    api_key = os.getenv("SCRAPFLY_KEY")
    if not api_key:
        print("Error: SCRAPFLY_KEY environment variable not set")
        return
    
    scraper = VestiaireScraper(api_key)
    
    # Example searches
    search_queries = [
        "chanel bag",
        "louis vuitton",
        "hermes scarf",
        "gucci belt"
    ]
    
    for query in search_queries:
        print(f"\n🔍 Searching for: {query}")
        
        try:
            products = await scraper.scrape_search_page(query, page=1, country="uk")
            
            if products:
                print(f"✅ Found {len(products)} products")
                
                # Save results
                filename = f"results/{query.replace(' ', '_')}_search.json"
                scraper.save_to_json(products, filename)
                print(f"💾 Saved to: {filename}")
                
                # Show sample products
                print("\nSample products:")
                for i, product in enumerate(products[:3]):
                    print(f"  {i+1}. {product.title}")
                    print(f"     Price: {product.currency} {product.price}")
                    print(f"     Brand: {product.brand}")
                    print(f"     Condition: {product.condition}")
                    print()
            else:
                print("❌ No products found")
                
        except Exception as e:
            print(f"❌ Error: {e}")


async def example_product_scraping():
    """Example: Scrape individual product details"""
    print("\n=== Product Detail Scraping Example ===")
    
    api_key = os.getenv("SCRAPFLY_KEY")
    if not api_key:
        print("Error: SCRAPFLY_KEY environment variable not set")
        return
    
    scraper = VestiaireScraper(api_key)
    
    # First, get some products from search
    print("Getting products from search...")
    search_products = await scraper.scrape_search_page("chanel flap bag", page=1, country="uk")
    
    if search_products:
        # Scrape details for first few products
        for i, product in enumerate(search_products[:3]):
            print(f"\n📦 Scraping details for product {i+1}: {product.title}")
            
            try:
                detailed_product = await scraper.scrape_product_page(product.product_url)
                
                if detailed_product:
                    print(f"✅ Successfully scraped details")
                    print(f"   Title: {detailed_product.title}")
                    print(f"   Price: {detailed_product.currency} {detailed_product.price}")
                    if detailed_product.original_price:
                        print(f"   Original Price: {detailed_product.currency} {detailed_product.original_price}")
                    print(f"   Brand: {detailed_product.brand}")
                    print(f"   Size: {detailed_product.size}")
                    print(f"   Condition: {detailed_product.condition}")
                    print(f"   Seller: {detailed_product.seller}")
                    if detailed_product.discount_percentage:
                        print(f"   Discount: {detailed_product.discount_percentage}%")
                    
                    # Save individual product data
                    filename = f"results/product_{detailed_product.id}_details.json"
                    scraper.save_to_json([detailed_product], filename)
                    print(f"   💾 Saved to: {filename}")
                else:
                    print("❌ Failed to scrape product details")
                    
            except Exception as e:
                print(f"❌ Error scraping product: {e}")
    else:
        print("❌ No products found in search")


async def example_paginated_scraping():
    """Example: Scrape multiple pages"""
    print("\n=== Paginated Scraping Example ===")
    
    api_key = os.getenv("SCRAPFLY_KEY")
    if not api_key:
        print("Error: SCRAPFLY_KEY environment variable not set")
        return
    
    scraper = VestiaireScraper(api_key)
    
    search_query = "handbag"
    max_pages = 3
    all_products = []
    
    print(f"🔍 Scraping up to {max_pages} pages for: {search_query}")
    
    for page in range(1, max_pages + 1):
        print(f"\n📄 Scraping page {page}...")
        
        try:
            products = await scraper.scrape_search_page(search_query, page=page, country="uk")
            
            if products:
                all_products.extend(products)
                print(f"✅ Found {len(products)} products on page {page}")
                
                # Add delay between pages to be respectful
                if page < max_pages:
                    print("⏳ Waiting 2 seconds before next page...")
                    await asyncio.sleep(2)
            else:
                print(f"❌ No products found on page {page}")
                break
                
        except Exception as e:
            print(f"❌ Error scraping page {page}: {e}")
            break
    
    if all_products:
        print(f"\n🎉 Total products scraped: {len(all_products)}")
        
        # Save all results
        json_filename = f"results/{search_query}_multipage_search.json"
        csv_filename = f"results/{search_query}_multipage_search.csv"
        
        scraper.save_to_json(all_products, json_filename)
        scraper.save_to_csv(all_products, csv_filename)
        
        print(f"💾 Saved to: {json_filename}")
        print(f"💾 Saved to: {csv_filename}")
        
        # Show statistics
        brands = {}
        for product in all_products:
            brand = product.brand
            brands[brand] = brands.get(brand, 0) + 1
        
        print(f"\n📊 Brand distribution:")
        for brand, count in sorted(brands.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"   {brand}: {count} products")
    else:
        print("❌ No products found across all pages")


async def example_price_analysis():
    """Example: Scrape and analyze pricing data"""
    print("\n=== Price Analysis Example ===")
    
    api_key = os.getenv("SCRAPFLY_KEY")
    if not api_key:
        print("Error: SCRAPFLY_KEY environment variable not set")
        return
    
    scraper = VestiaireScraper(api_key)
    
    # Scrape luxury handbags
    search_query = "luxury handbag"
    print(f"🔍 Scraping luxury handbags for price analysis...")
    
    try:
        products = await scraper.scrape_search_page(search_query, page=1, country="uk")
        
        if products:
            print(f"✅ Found {len(products)} products")
            
            # Calculate price statistics
            prices = [p.price for p in products if p.price > 0]
            
            if prices:
                avg_price = sum(prices) / len(prices)
                min_price = min(prices)
                max_price = max(prices)
                
                print(f"\n💰 Price Analysis:")
                print(f"   Average price: £{avg_price:.2f}")
                print(f"   Price range: £{min_price:.2f} - £{max_price:.2f}")
                
                # Find products with discounts
                discounted_products = [p for p in products if p.discount_percentage]
                print(f"   Products with discounts: {len(discounted_products)}")
                
                if discounted_products:
                    avg_discount = sum(p.discount_percentage for p in discounted_products) / len(discounted_products)
                    print(f"   Average discount: {avg_discount:.1f}%")
                
                # Save analysis data
                analysis_data = {
                    "search_query": search_query,
                    "total_products": len(products),
                    "price_statistics": {
                        "average": avg_price,
                        "minimum": min_price,
                        "maximum": max_price,
                        "count": len(prices)
                    },
                    "discount_statistics": {
                        "products_with_discounts": len(discounted_products),
                        "average_discount_percentage": avg_discount if discounted_products else 0
                    },
                    "products": [
                        {
                            "title": p.title,
                            "brand": p.brand,
                            "price": p.price,
                            "original_price": p.original_price,
                            "discount_percentage": p.discount_percentage,
                            "condition": p.condition
                        }
                        for p in products
                    ]
                }
                
                import json
                with open(f"results/{search_query}_price_analysis.json", 'w') as f:
                    json.dump(analysis_data, f, indent=2)
                
                print(f"💾 Analysis saved to: results/{search_query}_price_analysis.json")
            
        else:
            print("❌ No products found")
            
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Run all examples"""
    print("🚀 Vestiairecollective Scraper Examples")
    print("=" * 50)
    
    # Check if results directory exists
    os.makedirs("results", exist_ok=True)
    
    try:
        # Run different scraping examples
        await example_search_scraping()
        await example_product_scraping()
        await example_paginated_scraping()
        await example_price_analysis()
        
        print("\n🎉 All examples completed!")
        print("📁 Check the 'results' directory for output files")
        
    except KeyboardInterrupt:
        print("\n⏹️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
