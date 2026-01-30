# Vestiaire Collective API Endpoint

This document describes the Vestiaire Collective scraping endpoint for luxury fashion items.

## Overview

The API provides an endpoint for retrieving luxury fashion items from Vestiaire Collective:
- `/vestiaire` - Get luxury fashion items from Vestiaire Collective

## Base URL

```
http://localhost:8099
```

## Endpoint

### Vestiaire Collective Items

**Endpoint:** `GET /vestiaire`

**Description:** Retrieves luxury fashion items from Vestiaire Collective with comprehensive product information including original prices and discounts.

**Query Parameters:**
- `search` (string, default: "handbag") - Search term for luxury items
- `page` (integer, default: 1) - Page number for pagination
- `items_per_page` (integer, default: 50) - Number of items per page
- `min_price` (string, optional) - Minimum price filter
- `max_price` (string, optional) - Maximum price filter
- `country` (string, default: "uk") - Country code (uk, us, fr, de, it, es)

**Supported Countries:**
- `uk` - United Kingdom (vestiairecollective.co.uk)
- `us` - United States (vestiairecollective.com)
- `fr` - France (vestiairecollective.fr)
- `de` - Germany (vestiairecollective.de)
- `it` - Italy (vestiairecollective.it)
- `es` - Spain (vestiairecollective.es)

**Example Request:**
```bash
curl "http://localhost:8099/vestiaire?search=chanel&items_per_page=10&min_price=1000&max_price=5000&country=uk"
```

**Example Response:**
```json
{
    "success": true,
    "data": [
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

### Success Response
```json
{
    "success": true,
    "data": [...],           // Array of luxury fashion items
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
    "count": 5,
    "pagination": {...},
    "error": "Error message describing the issue"
}
```

## Data Fields

Each Vestiaire Collective item contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `Title` | string | Complete product title |
| `Price` | string | Current selling price with currency |
| `Brand` | string | Extracted luxury brand name |
| `Size` | string | Item size (Medium, MM, 30, Mini, One Size, etc.) |
| `Image` | string | High-resolution product image URL |
| `Link` | string | Direct product page URL |
| `Condition` | string | Item condition (Excellent, Very Good, Good) |
| `Seller` | string | Seller username/store name |
| `OriginalPrice` | string | Original retail price |
| `Discount` | string | Discount percentage |

## Supported Luxury Brands

The endpoint automatically detects and extracts major luxury brands including:

**Handbags & Accessories:**
- Chanel, Louis Vuitton, Hermès, Gucci, Prada, Dior
- Balenciaga, Saint Laurent, Celine, Bottega Veneta, Fendi
- Valentino, Burberry, Versace, Givenchy, Loewe

**Jewelry & Watches:**
- Cartier, Rolex, Van Cleef & Arpels, Tiffany & Co.

**Fashion Houses:**
- Jacquemus, Goyard, Balmain, Alexander McQueen

## Features

### Multi-Country Support
- Automatic domain detection based on country parameter
- Localized pricing and currency
- Country-specific inventory

### Advanced Brand Detection
- Intelligent brand extraction from product titles
- Support for luxury brand variations and special characters
- Fallback to "Unknown" when brand not detected

### Comprehensive Data Extraction
- Multiple fallback selectors for reliable parsing
- Handles Vestiaire's dynamic HTML structure
- Extracts original prices and discount percentages

### Rate Limiting
- Built-in rate limiting to prevent 429 errors
- Maximum 30 requests per minute per client
- Automatic wait time calculation when rate limited

### Caching
- 5-minute cache duration to reduce API calls
- Cache keys based on search parameters
- Automatic cache expiration

### Error Handling
- Graceful fallback to sample luxury items when scraping fails
- Comprehensive error logging
- Always returns a valid response

## Usage Examples

### Basic Search
```bash
# Search for Chanel bags
curl "http://localhost:8099/vestiaire?search=chanel"

# Search for Gucci items
curl "http://localhost:8099/vestiaire?search=gucci"
```

### With Price Filters
```bash
# Items between £500 and £2,000
curl "http://localhost:8099/vestiaire?search=handbag&min_price=500&max_price=2000"

# High-end items above £5,000
curl "http://localhost:8099/vestiaire?search=hermes&min_price=5000"
```

### Different Countries
```bash
# Search Vestiaire France
curl "http://localhost:8099/vestiaire?search=sac%20chanel&country=fr"

# Search Vestiaire US
curl "http://localhost:8099/vestiaire?search=chanel%20bag&country=us"
```

### Pagination
```bash
# Get page 2 with 20 items per page
curl "http://localhost:8099/vestiaire?search=louis%20vuitton&page=2&items_per_page=20"
```

### Complex Search
```bash
# Search for specific bag with price range and country
curl "http://localhost:8099/vestiaire?search=chanel%20classic%20flap&min_price=2000&max_price=8000&country=uk&items_per_page=15"
```

## Running the Server

To start the API server:

```bash
cd /path/to/templates
python3 test_server.py
```

The server will start on `http://localhost:8099`

## Testing the Endpoint

### Quick Test Commands
```bash
# Test basic Vestiaire search
curl "http://localhost:8099/vestiaire?search=chanel&items_per_page=5"

# Test with price filters
curl "http://localhost:8099/vestiaire?search=gucci&min_price=500&max_price=1500"

# Test different country
curl "http://localhost:8099/vestiaire?search=chanel&country=fr"

# Pretty print JSON response
curl "http://localhost:8099/vestiaire?search=chanel" | python3 -m json.tool
```

## Implementation Details

### Vestiaire Collective Integration
- Supports multiple Vestiaire country domains
- Handles Vestiaire's anti-bot measures with realistic headers
- Adaptive parsing for Vestiaire's dynamic HTML structure
- Fallback selectors for reliable data extraction

### Data Extraction Strategy
- Primary selectors for current Vestiaire structure
- Multiple fallback selectors for different page layouts
- Text-based extraction as last resort
- Brand-specific logic for luxury items

### Error Recovery
- Multiple fallback mechanisms
- Sample luxury fashion data when real scraping fails
- Comprehensive logging for debugging
- Graceful degradation of service

## Rate Limits and Best Practices

1. **Respect rate limits**: Built-in rate limiting prevents abuse
2. **Use caching**: Results are cached for 5 minutes
3. **Handle errors gracefully**: Always check the `error` field
4. **Pagination**: Use `has_more` to determine if more pages exist
5. **Country-specific**: Use appropriate country codes for better results

## Sample Data

When real scraping fails, the endpoint returns sample luxury fashion items including:

- **Chanel Classic Flap Bag** - £4,250 (23% discount)
- **Louis Vuitton Neverfull MM** - £1,180 (19% discount)
- **Hermès Birkin 30** - £8,900 (13% discount)
- **Gucci Horsebit 1955 Mini** - £890 (19% discount)
- **Prada Re-Edition 2005** - £650 (18% discount)

All sample items include:
- Realistic luxury pricing
- Original prices and discount percentages
- Proper Vestiaire URL structure
- Authentic seller names
- High-quality image URLs

## Troubleshooting

### Common Issues

1. **Empty results**: Try different search terms or check spelling
2. **Rate limiting**: Wait a few seconds between requests
3. **Country not supported**: Use 'uk' as default country
4. **Price filters not working**: Ensure price values are valid numbers
5. **Currency symbols**: Prices include local currency symbols (£, €, $)

### Debug Mode

The API provides detailed console logs including:
- Search URLs being requested
- Rate limiting information
- Cache hits/misses
- Error details
- Success/failure status
- Number of items found

## Future Enhancements

Potential improvements for future versions:
- Real-time price tracking
- Advanced filtering by condition, seller rating
- Historical price analysis
- Authentication for premium features
- Image recognition for better categorization
- Integration with other luxury marketplaces
- Price comparison across countries
- Alert system for price drops

## Related Endpoints

This Vestiaire endpoint complements other scraping endpoints:

- `/ebay` - General eBay items
- `/ebay/sold` - eBay sold items
- `/vinted` - Vinted items
- `/vinted/sold` - Vinted sold items

All endpoints follow the same response format and parameter structure for consistency.
