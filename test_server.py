#!/usr/bin/env python3
import sys
import os

# Change to the api directory
os.chdir('api')
sys.path.append('.')

from http.server import HTTPServer, BaseHTTPRequestHandler
from index import handler

if __name__ == "__main__":
    try:
        server = HTTPServer(('localhost', 8099), handler)
        print('Server running on http://localhost:8099')
        print('Try these URLs:')
        print('- http://localhost:8099/')
        print('- http://localhost:8099/?search=dior%20bag&page=1&items_per_page=10')
        print('- http://localhost:8099/?search=bags&page=1&items_per_page=20')
        print('- http://localhost:8099/?search=bags&min_price=50&max_price=100')
        server.serve_forever()
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
