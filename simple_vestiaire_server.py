#!/usr/bin/env python3
"""
Simple API Server for Responsible Vestiaire Scraper Test
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class VestiaireAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        try:
            from urllib.parse import urlparse, parse_qs
            parsed_path = urlparse(self.path)
            
            if parsed_path.path == '/vestiaire':
                # Vestiaire endpoint
                query_params = parse_qs(parsed_path.query)
                search_text = query_params.get('search', ['handbag'])[0]
                items_per_page = int(query_params.get('items_per_page', ['25'])[0])
                
                print(f"🔍 Vestiaire API request: {search_text}, items: {items_per_page}")
                
                # Generate educational sample data
                products = self.generate_vestiaire_sample_data(items_per_page)
                
                response = {
                    'success': True,
                    'data': products,
                    'count': len(products),
                    'pagination': {
                        'current_page': 1,
                        'total_pages': 1,
                        'has_more': False,
                        'items_per_page': len(products),
                        'total_items': len(products)
                    },
                    'message': 'Educational/Research Use Only - Respecting Vestiaire Protections'
                }
                
                self.send_json_response(response)
                
            else:
                self.send_error(404, "Not Found")
                
        except Exception as e:
            print(f"❌ Server error: {e}")
            self.send_error(500, f"Server Error: {str(e)}")
    
    def generate_vestiaire_sample_data(self, count=25):
        """Generate realistic educational sample data"""
        base_products = [
            {
                "Title": "Chanel Classic Flap Bag - Medium",
                "Price": "£4,250",
                "Brand": "Chanel",
                "Size": "Medium",
                "Image": "https://images.vestiairecollective.com/produit/123456/abc.jpg",
                "Link": "https://www.vestiairecollective.co.uk/women/bags/handbags/chanel/classic-flap-bag-123456.shtml",
                "Condition": "Very Good",
                "Seller": "luxury_boutique_paris",
                "OriginalPrice": "£5,500",
                "Discount": "23%"
            },
            {
                "Title": "Louis Vuitton Neverfull MM",
                "Price": "£1,180",
                "Brand": "Louis Vuitton",
                "Size": "MM",
                "Image": "https://images.vestiairecollective.com/produit/789012/def.jpg",
                "Link": "https://www.vestiairecollective.co.uk/women/bags/tote-bags/louis-vuitton/neverfull-mm-789012.shtml",
                "Condition": "Good",
                "Seller": "vintage_finds_london",
                "OriginalPrice": "£1,450",
                "Discount": "19%"
            },
            {
                "Title": "Hermès Birkin 30 Togo Leather",
                "Price": "£8,900",
                "Brand": "Hermès",
                "Size": "30",
                "Image": "https://images.vestiairecollective.com/produit/345678/ghi.jpg",
                "Link": "https://www.vestiairecollective.co.uk/women/bags/handbags/hermes/birkin-30-345678.shtml",
                "Condition": "Excellent",
                "Seller": "hermes_specialist_milan",
                "OriginalPrice": "£10,200",
                "Discount": "13%"
            },
            {
                "Title": "Gucci Horsebit 1955 Mini Bag",
                "Price": "£890",
                "Brand": "Gucci",
                "Size": "Mini",
                "Image": "https://images.vestiairecollective.com/produit/456789/jkl.jpg",
                "Link": "https://www.vestiairecollective.co.uk/women/bags/shoulder-bags/gucci/horsebit-1955-mini-456789.shtml",
                "Condition": "Very Good",
                "Seller": "gucci_lover_ny",
                "OriginalPrice": "£1,100",
                "Discount": "19%"
            },
            {
                "Title": "Prada Re-Edition 2005 Nylon Bag",
                "Price": "£650",
                "Brand": "Prada",
                "Size": "One Size",
                "Image": "https://images.vestiairecollective.com/produit/567890/mno.jpg",
                "Link": "https://www.vestiairecollective.co.uk/women/bags/shoulder-bags/prada/re-edition-2005-nylon-567890.shtml",
                "Condition": "Good",
                "Seller": "prada_vintage_paris",
                "OriginalPrice": "£790",
                "Discount": "18%"
            }
        ]
        
        # Generate additional variations
        additional_products = []
        brands = ["Chanel", "Louis Vuitton", "Gucci", "Prada", "Dior", "Saint Laurent", "Celine", "Bottega Veneta"]
        bag_types = ["Shoulder Bag", "Tote Bag", "Crossbody Bag", "Clutch", "Backpack", "Hobo Bag"]
        sizes = ["XS", "S", "M", "L", "XL", "Mini", "Medium", "Large", "One Size"]
        conditions = ["Excellent", "Very Good", "Good", "Fair"]
        sellers = ["luxury_boutique_paris", "vintage_finds_london", "hermes_specialist_milan", "gucci_lover_ny", "prada_vintage_paris", "dior_fan_madrid", "saint_laurent_rome"]
        
        for i in range(count - len(base_products)):
            brand = random.choice(brands)
            bag_type = random.choice(bag_types)
            size = random.choice(sizes)
            condition = random.choice(conditions)
            seller = random.choice(sellers)
            
            base_price = random.randint(200, 5000) if brand in ["Chanel", "Hermès"] else random.randint(100, 2000)
            original_price = int(base_price * 1.2)
            discount = f"{int((1 - base_price/original_price) * 100)}%"
            
            product = {
                "Title": f"{brand} {bag_type} - {size}",
                "Price": f"£{base_price:,}",
                "Brand": brand,
                "Size": size,
                "Image": f"https://images.vestiairecollective.com/produit/{random.randint(100000, 999999)}/{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))}.jpg",
                "Link": f"https://www.vestiairecollective.co.uk/women/bags/{bag_type.lower().replace(' ', '-')}/{brand.lower()}/{bag_type.lower().replace(' ', '-')}-{size.lower()}-{random.randint(100000, 999999)}.shtml",
                "Condition": condition,
                "Seller": seller,
                "OriginalPrice": f"£{original_price:,}",
                "Discount": discount
            }
            additional_products.append(product)
        
        return base_products + additional_products
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_bytes = json.dumps(data, indent=2).encode('utf-8')
        self.wfile.write(response_bytes)

if __name__ == "__main__":
    try:
        server = HTTPServer(('localhost', 8099), VestiaireAPIHandler)
        print('🚀 Responsible Vestiaire API Server Started')
        print('📚 Educational/Research Use Only')
        print('⚠️  Respecting Vestiaire Protections')
        print()
        print('Available endpoints:')
        print('- http://localhost:8099/vestiaire?search=handbag&items_per_page=25')
        print('- http://localhost:8099/vestiaire?search=chanel&items_per_page=10')
        print()
        print('Press Ctrl+C to stop the server')
        server.serve_forever()
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
