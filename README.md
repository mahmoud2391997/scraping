# eBay & Vinted Scraping API

🚀 **Production-ready REST API for scraping eBay and Vinted marketplaces with advanced search, price filtering, and pagination**

## 📘 How to Use (Quick Guide)

See `HOW_TO_USE.md` for:
- Local setup + install
- How to run the API server
- All endpoints + example requests
- Optional eBay credentials setup

## 🌐 Local Server

**http://localhost:8099** (when running locally)

## ✨ eBay Features

### 🔍 Advanced Search & Filtering
- **Full-text Search**: Search across entire eBay product catalog
- **Price Filtering**: Min/max price range support with real-time filtering
- **Pagination**: Complete pagination with accurate item counts
- **Brand Detection**: Automatic brand identification from titles
- **Country Support**: UK, US, DE, FR, IT, ES, CA, AU with proper domains
- **Image Extraction**: Real eBay product images with proper URLs
- **Condition & Seller**: Product condition and seller information

### 🚀 Production Features
- **Rate Limiting**: 30 requests/minute per IP
- **Caching**: 5-minute cache for identical requests
- **Error Handling**: Structured error responses with retry logic
- **Performance**: Gzip compression, keep-alive connections
- **Security**: Input validation and sanitization
- **Vinted-Style Technique**: Same robust extraction methods as Vinted scraper

## 📡 eBay API Endpoint

```http
GET http://localhost:8099/ebay
```

## 💡 Quick Start

### Start the Server
```bash
# Navigate to project directory
cd /Users/mahmoudelsayed/Downloads/templates

# Start the server
python3 test_server.py

# Server runs on http://localhost:8099
```

### Basic Usage
```bash
# Search eBay for iPhones
curl "http://localhost:8099/ebay?search=iphone&country=uk&items_per_page=5"

# Search eBay for laptops with price filter
curl "http://localhost:8099/ebay?search=laptop&country=us&min_price=200&max_price=500&items_per_page=10"

# Search eBay for shoes with pagination
curl "http://localhost:8099/ebay?search=shoes&country=uk&page=2&items_per_page=8"
```

## 🔧 eBay Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `search` | string | "laptop" | Search query term |
| `country` | string | "uk" | Country code (uk, us, de, fr, it, es, ca, au) |
| `page` | integer | 1 | Page number for pagination |
| `items_per_page` | integer | 50 | Items per page (1-50) |
| `min_price` | float | null | Minimum price filter |
| `max_price` | float | null | Maximum price filter |

## 📊 eBay Response Format

```json
{
  "success": true,
  "data": [
    {
      "Title": "Apple Iphone - Latest Model",
      "Price": "$299.99",
      "Brand": "Apple",
      "Size": "N/A",
      "Image": "https://i.ebayimg.com/images/g/x4YAAOSw~HlkYB3Q/s-l500.jpg",
      "Link": "https://www.ebay.co.uk/sch/i.html?_nkw=iphone",
      "Condition": "Brand New",
      "Seller": "TechStore"
    }
  ],
  "count": 5,
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "has_more": true,
    "items_per_page": 5,
    "total_items": 50,
    "start_index": 0,
    "end_index": 5
  },
  "error": null
}
```

## 🎯 eBay Usage Examples

### 1. Basic Search
```bash
# Search for iPhones in UK
curl "http://localhost:8099/ebay?search=iphone&country=uk&items_per_page=5"
```

### 2. Price Filtering
```bash
# iPhones between $400-$600
curl "http://localhost:8099/ebay?search=iphone&country=uk&min_price=400&max_price=600&items_per_page=10"

# Laptops under $500
curl "http://localhost:8099/ebay?search=laptop&country=us&max_price=500&items_per_page=8"

# Shoes above $100
curl "http://localhost:8099/ebay?search=shoes&country=uk&min_price=100&items_per_page=6"
```

### 3. Pagination
```bash
# Page 1 (default)
curl "http://localhost:8099/ebay?search=phone&country=us&items_per_page=10"

# Page 2
curl "http://localhost:8099/ebay?search=phone&country=us&page=2&items_per_page=10"

# Page 3 with 20 items
curl "http://localhost:8099/ebay?search=phone&country=us&page=3&items_per_page=20"
```

### 4. Country-Specific Searches
```bash
# UK eBay
curl "http://localhost:8099/ebay?search=iphone&country=uk"

# US eBay
curl "http://localhost:8099/ebay?search=iphone&country=us"

# German eBay
curl "http://localhost:8099/ebay?search=iphone&country=de"

# French eBay
curl "http://localhost:8099/ebay?search=iphone&country=fr"
```

### 5. Combined Parameters
```bash
# Complex search: Page 2, 15 items, price range, specific country
curl "http://localhost:8099/ebay?search=macbook&country=us&page=2&items_per_page=15&min_price=800&max_price=1500"
```

## 🔍 eBay Data Fields

| Field | Description | Example |
|-------|-------------|---------|
| `Title` | Product title | "Apple Iphone - Latest Model" |
| `Price` | Price with currency symbol | "$299.99" |
| `Brand` | Detected brand name | "Apple" |
| `Size` | Product size (if available) | "N/A" |
| `Image` | Product image URL | "https://i.ebayimg.com/images/g/..." |
| `Link` | eBay search link | "https://www.ebay.co.uk/sch/i.html?_nkw=iphone" |
| `Condition` | Product condition | "Brand New", "Used", "Excellent" |
| `Seller` | Seller name | "TechStore", "GadgetWorld" |

## 📊 eBay Pagination Details

The pagination object provides complete navigation information:

```json
{
  "pagination": {
    "current_page": 1,        // Current page number
    "total_pages": 10,         // Total pages available
    "has_more": true,          // More pages available
    "items_per_page": 5,        // Items on current page
    "total_items": 50,         // Total items in search
    "start_index": 0,          // Starting item index
    "end_index": 5             // Ending item index
  }
}
```

## 🌍 Country Support

| Country | Code | Domain | Currency |
|---------|------|--------|----------|
| United Kingdom | `uk` | ebay.co.uk | £ |
| United States | `us` | ebay.com | $ |
| Germany | `de` | ebay.de | € |
| France | `fr` | ebay.fr | € |
| Italy | `it` | ebay.it | € |
| Spain | `es` | ebay.es | € |
| Canada | `ca` | ebay.ca | C$ |
| Australia | `au` | ebay.com.au | A$ |

## 💰 Price Filtering Examples

### Price Range Filtering
```bash
# Products between $100 and $300
curl "http://localhost:8099/ebay?search=watch&country=us&min_price=100&max_price=300"

# Products under $50
curl "http://localhost:8099/ebay?search=headphones&country=uk&max_price=50"

# Products above $1000
curl "http://localhost:8099/ebay?search=camera&country=de&min_price=1000"
```

### Price Filtering with Pagination
```bash
# Page 2 of results in price range $200-$400
curl "http://localhost:8099/ebay?search=tablet&country=us&page=2&items_per_page=8&min_price=200&max_price=400"
```

## 🚀 Advanced Features

### Brand Detection
The API automatically detects brands from product titles:

```json
{
  "Title": "Apple MacBook Pro 13-inch",
  "Brand": "Apple"
}
```

### Image Extraction
Real eBay product images are extracted:

```json
{
  "Image": "https://i.ebayimg.com/images/g/x4YAAOSw~HlkYB3Q/s-l500.jpg"
}
```

### Condition & Seller Information

```json
{
  "Condition": "Brand New",
  "Seller": "TechStore"
}
```

## 🔧 Server Management

### Start Server
```bash
cd /Users/mahmoudelsayed/Downloads/templates
python3 test_server.py
```

### Stop Server
```bash
# Find and kill the server process
lsof -ti:8099 | xargs kill -9
```

### Check Server Status
```bash
# Test if server is running
curl -w "Status: %{http_code}\n" "http://localhost:8099/ebay?search=test"
```

## 🐛 Troubleshooting

### Common Issues

#### Server Not Running
```bash
# Check if server is running
ps aux | grep "python.*test_server"

# Start server if not running
python3 test_server.py
```

#### No Results Returned
```bash
# Try broader search terms
curl "http://localhost:8099/ebay?search=phone"  # Instead of specific model

# Check price range isn't too restrictive
curl "http://localhost:8099/ebay?search=phone&min_price=50&max_price=1000"
```

#### Price Filtering Not Working
```bash
# Ensure prices are in correct format (numbers only)
curl "http://localhost:8099/ebay?search=phone&min_price=100&max_price=500"

# Check response for price filtering messages
```

#### Slow Response
```bash
# Reduce items_per_page for faster response
curl "http://localhost:8099/ebay?search=phone&items_per_page=5"
```

### Error Responses

```json
{
  "success": false,
  "data": [],
  "error": "Price filter applied: 0 items remaining from original",
  "pagination": {
    "current_page": 1,
    "total_pages": 0,
    "has_more": false,
    "items_per_page": 0,
    "total_items": 0
  }
}
```

## 📈 Performance Tips

### Optimize Requests
1. **Use appropriate `items_per_page`**: Smaller values = faster responses
2. **Set price ranges**: Reduces data processing time
3. **Use specific search terms**: More targeted results
4. **Cache results**: Identical requests are cached for 5 minutes

### Rate Limiting
- **30 requests per minute per IP**
- **Automatic retry after 60 seconds** if rate limited
- **Structured error responses** with retry information

## 🎯 Best Practices

### Search Optimization
```bash
# ✅ Good: Specific terms
curl "http://localhost:8099/ebay?search=iphone+13+pro&country=us"

# ✅ Good: Price filtering
curl "http://localhost:8099/ebay?search=laptop&country=uk&min_price=500&max_price=1000"

# ❌ Avoid: Too broad
curl "http://localhost:8099/ebay?search=stuff"
```

### Pagination Best Practices
```bash
# ✅ Good: Reasonable page sizes
curl "http://localhost:8099/ebay?search=phone&items_per_page=20"

# ❌ Avoid: Too many items per page
curl "http://localhost:8099/ebay?search=phone&items_per_page=100"
```

## 📞 Support

- **Local Server**: http://localhost:8099
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: This README and inline code comments

---

**🎯 Your eBay scraping API is ready to use!**

*Built with ❤️ using Python, BeautifulSoup, and Vinted-style extraction techniques*

## 🔄 Vinted API (Also Available)

The same server also supports Vinted scraping:

```bash
# Vinted API endpoint
curl "http://localhost:8099/?search=shoes&country=uk&items_per_page=10"
```

Same parameters and response format as eBay API!
