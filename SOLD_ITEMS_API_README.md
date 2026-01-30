# Sold Items API Endpoints

This document describes the sold items endpoints for both eBay and Vinted platforms.

## Overview

The API provides two new endpoints for retrieving sold items data:
- `/ebay/sold` - Get sold items from eBay
- `/vinted/sold` - Get sold items from Vinted

## Base URL

```
http://localhost:8099
```

## Endpoints

### eBay Sold Items

**Endpoint:** `GET /ebay/sold`

**Description:** Retrieves sold items from eBay using eBay's sold items filter.

**Query Parameters:**
- `search` (string, default: "laptop") - Search term
- `page` (integer, default: 1) - Page number
- `items_per_page` (integer, default: 50) - Number of items per page
- `min_price` (string, optional) - Minimum price filter
- `max_price` (string, optional) - Maximum price filter
- `country` (string, default: "uk") - Country code (uk, us, de, etc.)

**Example Request:**
```bash
curl "http://localhost:8099/ebay/sold?search=nike&items_per_page=10&min_price=100&max_price=500&country=uk"
```

**Example Response:**
```json
{
    "success": true,
    "data": [
        {
            "Title": "Nike Air Jordan 1 Retro High - Sold",
            "Price": "$250.00",
            "Brand": "Nike",
            "Size": "10",
            "Image": "https://i.ebayimg.com/images/g/aaa/s-l500.jpg",
            "Link": "https://www.ebay.com/itm/aaa",
            "Condition": "New",
            "Seller": "sneaker_king",
            "SoldDate": "2024-01-10"
        }
    ],
    "count": 1,
    "pagination": {
        "current_page": 1,
        "total_pages": 1,
        "has_more": false,
        "items_per_page": 1,
        "total_items": 1
    },
    "error": null
}
```

### Vinted Sold Items

**Endpoint:** `GET /vinted/sold`

**Description:** Retrieves sold items from Vinted platform.

**Query Parameters:**
- `search` (string, default: "t-shirt") - Search term
- `page` (integer, default: 1) - Page number
- `items_per_page` (integer, default: 50) - Number of items per page
- `min_price` (string, optional) - Minimum price filter
- `max_price` (string, optional) - Maximum price filter
- `country` (string, default: "uk") - Country code (uk, fr, de, etc.)

**Example Request:**
```bash
curl "http://localhost:8099/vinted/sold?search=jeans&items_per_page=10&min_price=20&max_price=100&country=uk"
```

**Example Response:**
```json
{
    "success": true,
    "data": [
        {
            "Title": "Vintage Levi's 501 Jeans - Sold",
            "Price": "45€",
            "Brand": "Levi's",
            "Size": "32",
            "Image": "https://images.vinted.net/aaa",
            "Link": "https://www.vinted.co.uk/items/aaa",
            "Seller": "vintage_lover",
            "SoldDate": "2024-01-12"
        }
    ],
    "count": 1,
    "pagination": {
        "current_page": 1,
        "total_pages": 1,
        "has_more": false,
        "items_per_page": 1,
        "total_items": 1
    },
    "error": null
}
```

## Response Format

Both endpoints return a consistent JSON response structure:

### Success Response
```json
{
    "success": true,
    "data": [...],           // Array of sold items
    "count": 10,             // Number of items returned
    "pagination": {          // Pagination information
        "current_page": 1,
        "total_pages": 5,
        "has_more": true,
        "items_per_page": 10,
        "total_items": 50
    },
    "error": null
}
```

### Error Response
```json
{
    "success": true,
    "data": [...],           // Fallback sample data
    "count": 3,
    "pagination": {...},
    "error": "Error message describing the issue"
}
```

## Data Fields

Each sold item contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `Title` | string | Item title |
| `Price` | string | Sold price with currency |
| `Brand` | string | Extracted brand name |
| `Size` | string | Item size (if applicable) |
| `Image` | string | Image URL |
| `Link` | string | Item page URL |
| `Condition` | string | Item condition (eBay only) |
| `Seller` | string | Seller name |
| `SoldDate` | string | Date when item was sold |

## Features

### Rate Limiting
- Built-in rate limiting to prevent 429 errors
- Maximum 30 requests per minute per client
- Automatic wait time calculation when rate limited

### Caching
- 5-minute cache duration to reduce API calls
- Cache keys based on search parameters
- Automatic cache expiration

### Error Handling
- Graceful fallback to sample data when scraping fails
- Comprehensive error logging
- Always returns a valid response

### Brand Detection
- Automatic brand extraction from item titles
- Support for major brands across categories
- Fallback to "Unknown" when brand not detected

### Size Detection
- Automatic size extraction for clothing and shoes
- Support for standard size formats (S, M, L, XL, etc.)
- Numeric size detection for various products

## Usage Examples

### Basic Search
```bash
# Search for sold Nike shoes on eBay
curl "http://localhost:8099/ebay/sold?search=nike%20shoes"

# Search for sold dresses on Vinted
curl "http://localhost:8099/vinted/sold?search=dress"
```

### With Price Filters
```bash
# eBay items between $50 and $200
curl "http://localhost:8099/ebay/sold?search=laptop&min_price=50&max_price=200"

# Vinted items between 20€ and 100€
curl "http://localhost:8099/vinted/sold?search=jacket&min_price=20&max_price=100"
```

### Pagination
```bash
# Get page 2 with 20 items per page
curl "http://localhost:8099/ebay/sold?search=iphone&page=2&items_per_page=20"
```

### Different Countries
```bash
# Search eBay Germany
curl "http://localhost:8099/ebay/sold?search=bmw&country=de"

# Search Vinted France
curl "http://localhost:8099/vinted/sold?search=chaussures&country=fr"
```

## Running the Server

To start the API server:

```bash
cd /path/to/templates
python3 test_server.py
```

The server will start on `http://localhost:8099`

## Testing the Endpoints

### Quick Test Commands
```bash
# Test eBay sold items
curl "http://localhost:8099/ebay/sold?search=nike&items_per_page=5"

# Test Vinted sold items
curl "http://localhost:8099/vinted/sold?search=jeans&items_per_page=5"

# Pretty print JSON response
curl "http://localhost:8099/ebay/sold?search=laptop" | python3 -m json.tool
```

## Implementation Details

### eBay Integration
- Uses eBay's sold items filter (`LH_Sold=1` and `LH_Complete=1`)
- Extracts data from eBay search results pages
- Handles different eBay country domains
- Robust HTML parsing with fallback selectors

### Vinted Integration
- Attempts to filter by sold status
- Extracts data from Vinted catalog pages
- Handles different Vinted country domains
- Adaptive parsing for Vinted's HTML structure

### Error Recovery
- Multiple fallback mechanisms
- Sample data when real scraping fails
- Comprehensive logging for debugging
- Graceful degradation of service

## Rate Limits and Best Practices

1. **Respect rate limits**: Built-in rate limiting prevents abuse
2. **Use caching**: Results are cached for 5 minutes
3. **Handle errors gracefully**: Always check the `error` field
4. **Pagination**: Use `has_more` to determine if more pages exist
5. **Country-specific**: Use appropriate country codes for better results

## Troubleshooting

### Common Issues

1. **Empty results**: Try different search terms or check spelling
2. **Rate limiting**: Wait a few seconds between requests
3. **Country not supported**: Use 'uk' as default country
4. **Price filters not working**: Ensure price values are valid numbers

### Debug Mode

The API provides detailed console logs including:
- Search URLs being requested
- Rate limiting information
- Cache hits/misses
- Error details
- Success/failure status

## Future Enhancements

Potential improvements for future versions:
- Real-time sold data streaming
- Advanced filtering options
- Historical price trends
- Seller reputation metrics
- Image analysis for better categorization
- API key authentication for premium features
