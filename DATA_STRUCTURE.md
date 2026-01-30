# Data Structure Documentation

## Overview
This document outlines the data structures returned by the eBay and Vinted scraping APIs.

## API Endpoints

### 1. eBay API Endpoint
- **URL**: `/ebay`
- **Method**: GET
- **Purpose**: Scrape product data from eBay using eBay Browse API

### 2. Vinted API Endpoint  
- **URL**: `/` (root)
- **Method**: GET
- **Purpose**: Scrape product data from Vinted marketplace

## Query Parameters

Both endpoints support the following parameters:
- `search` (string): Search query term
- `page` (integer): Page number (default: 1)
- `items_per_page` (integer): Number of items per page (default: 50)
- `min_price` (float, optional): Minimum price filter
- `max_price` (float, optional): Maximum price filter

## Response Structure

### Main Response Object
```json
{
  "success": boolean,
  "data": Product[],
  "count": integer,
  "pagination": PaginationObject,
  "error": string | null
}
```

### Product Object

#### eBay Product Structure
```json
{
  "Title": string,
  "Price": string,
  "Brand": string,
  "Size": string,
  "Image": string,
  "Link": string,
  "Condition": string,
  "Seller": string
}
```

#### Vinted Product Structure
```json
{
  "Title": string,
  "Price": string,
  "Brand": string,
  "Size": string,
  "Image": string,
  "Link": string
}
```

### Pagination Object
```json
{
  "current_page": integer,
  "total_pages": integer,
  "has_more": boolean,
  "items_per_page": integer,
  "total_items": integer,
  "start_index": integer,
  "end_index": integer
}
```

## Field Descriptions

### Product Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Title` | string | Product name/title | "ACEMAGIC RX16 16\" Gaming Laptop" |
| `Price` | string | Product price with currency symbol | "$459.00" or "200,00zł" |
| `Brand` | string | Product brand name | "Lenovo", "Nike", "N/A" |
| `Size` | string | Product size information | "16", "M", "N/A" |
| `Image` | string | Product image URL | "http://i.ebayimg.com/images/g/..." |
| `Link` | string | Product page URL | "https://www.ebay.com/itm/..." |
| `Condition` | string | Item condition (eBay only) | "New", "Used", "N/A" |
| `Seller` | string | Seller information (eBay only) | "seller_name", "N/A" |

### Pagination Fields

| Field | Type | Description |
|-------|------|-------------|
| `current_page` | integer | Current page number |
| `total_pages` | integer | Total number of pages available |
| `has_more` | boolean | Whether more pages exist |
| `items_per_page` | integer | Number of items per page |
| `total_items` | integer | Total number of items found |
| `start_index` | integer | Starting index of current page items |
| `end_index` | integer | Ending index of current page items |

## Sample Responses

### eBay API Response Example
```json
{
  "success": true,
  "data": [
    {
      "Title": "ACEMAGIC RX16 16\" Gaming Laptop AMD Ryzen 7 6800H 16GB DDR5 512GB SSD Win 11 Pro",
      "Price": "$459.00",
      "Brand": "N/A",
      "Size": "16",
      "Image": "http://i.ebayimg.sandbox.ebay.com/images/g/9NMAAOSwhONoVpde/s-l225.jpg",
      "Link": "https://cgi.sandbox.ebay.com/itm/ACEMAGIC-RX16-16-Gaming-Laptop/110588318818",
      "Condition": "New",
      "Seller": "N/A"
    }
  ],
  "count": 1,
  "pagination": {
    "current_page": 1,
    "total_pages": 71,
    "has_more": true,
    "items_per_page": 3,
    "total_items": 213,
    "start_index": 0,
    "end_index": 3
  },
  "error": null
}
```

### Vinted API Response Example
```json
{
  "success": true,
  "data": [
    {
      "Title": "Torebka Prada re-edition 2005",
      "Price": "200,00zł",
      "Brand": "Prada",
      "Size": "N/A",
      "Image": "https://example.com/image.jpg",
      "Link": "https://www.vinted.pl/items/123456789"
    }
  ],
  "count": 1,
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "has_more": true,
    "items_per_page": 2,
    "total_items": 10,
    "start_index": 0,
    "end_index": 2
  },
  "error": null
}
```

## Error Handling

### Error Response Structure
```json
{
  "success": true,
  "data": [],
  "count": 0,
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "has_more": false,
    "items_per_page": 0,
    "total_items": 0,
    "start_index": 0,
    "end_index": 0
  },
  "error": "Error message description"
}
```

### Common Error Scenarios
- **Rate Limiting**: "Rate limit exceeded. Please try again later."
- **API Failure**: "eBay API error: 500 - Internal Server Error"
- **Network Issues**: "Error with eBay API: Connection timeout"
- **Invalid Parameters**: "Invalid price range specified"

## Data Notes

### Price Formats
- **eBay**: Uses USD format with dollar sign ($459.00)
- **Vinted**: Uses PLN format with zł suffix (200,00zł)

### Brand Detection
- **Known Brands**: Predefined list of popular brands (Nike, Adidas, etc.)
- **Fallback**: "N/A" when brand cannot be determined

### Image URLs
- **eBay**: Full image URLs provided by API
- **Vinted**: Extracted from page content, may be "N/A" if not found

### Size Information
- **Clothing**: Standard sizes (XS, S, M, L, XL, XXL)
- **Electronics**: Screen sizes in inches
- **Other**: May be "N/A" if not applicable

## Rate Limiting

- **Requests per Minute**: 30 requests per IP address
- **Cache Duration**: 5 minutes for identical requests
- **Retry Logic**: Automatic retry with exponential backoff for server errors

## Environment Configuration

### Required Environment Variables
```bash
EBAY_APP_ID="your-ebay-app-id"
EBAY_CERT_ID="your-ebay-cert-id"
```

### Sandbox vs Production
- **Sandbox**: App ID contains "SBX" prefix
- **Production**: App ID contains "PRD" prefix

## Usage Examples

### Basic Search
```bash
curl "http://localhost:8099/ebay?search=laptop&page=1&items_per_page=10"
```

### Price Filtering
```bash
curl "http://localhost:8099/?search=bag&min_price=50&max_price=200"
```

### Pagination
```bash
curl "http://localhost:8099/ebay?search=iphone&page=2&items_per_page=20"
```
