#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from index import handler
from http.server import HTTPServer

def run_server(port=8000):
    """Run the scraping API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, handler)
    print(f"🚀 Starting server on http://localhost:{port}")
    print("📡 Available endpoints:")
    print("   /           - Vinted scraping")
    print("   /ebay       - eBay scraping") 
    print("   /ebay/sold  - eBay sold items")
    print("   /vinted/sold - Vinted sold items")
    print("   /vestiaire  - Vestiaire Collective scraping")
    print(f"🎯 Server running on http://localhost:{port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.shutdown()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
