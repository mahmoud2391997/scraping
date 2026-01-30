# Vestiairecollective.com Scraper

A Python scraper for Vestiairecollective.com using Scrapfly.io to bypass anti-bot protections.

## Tutorial

Full tutorial available at: https://scrapfly.io/blog/how-to-scrape-vestiairecollective/

## Features

- ✅ Bypass anti-bot protection using Scrapfly.io
- ✅ Scrape search results pages
- ✅ Scrape individual product details
- ✅ Extract comprehensive product data (price, brand, condition, etc.)
- ✅ Support for multiple countries
- ✅ Export to JSON and CSV formats
- ✅ Paginated scraping support
- ✅ Price analysis and discount tracking

## Setup

### Prerequisites

- Python 3.10 or higher
- Poetry package manager
- Scrapfly API key

### Installation

1. **Get Scrapfly API Key**
   ```bash
   # Get your API key from https://scrapfly.io/dashboard
   export SCRAPFLY_KEY="your-api-key-here"
   ```

2. **Install Dependencies**
   ```bash
   poetry install
   ```

3. **Install Development Dependencies (optional)**
   ```bash
   poetry install --with dev
   ```

## Usage

### Basic Usage

```bash
# Set your API key
export SCRAPFLY_KEY="scp-live-204b76afe54344949f0bd3f61970ac4f"

# Run the example scraper
poetry run python run.py
```

### Programmatic Usage

```python
import asyncio
from vestiairecollective import VestiaireScraper

async def scrape_example():
    scraper = VestiaireScraper("your-api-key")
    
    # Scrape search results
    products = await scraper.scrape_search_page("chanel bag", country="uk")
    
    # Save results
    scraper.save_to_json(products, "results.json")
    scraper.save_to_csv(products, "results.csv")

asyncio.run(scrape_example())
```

## API Reference

### VestiaireScraper Class

#### Methods

- `scrape_search_page(search_query, page=1, country="uk")` - Scrape search results
- `scrape_product_page(product_url)` - Scrape individual product details
- `save_to_json(products, filename)` - Save products to JSON file
- `save_to_csv(products, filename)` - Save products to CSV file

#### Product Data Structure

```python
@dataclass
class Product:
    id: str
    title: str
    price: float
    original_price: Optional[float]
    currency: str
    brand: str
    size: Optional[str]
    condition: str
    image_url: str
    product_url: str
    seller: str
    discount_percentage: Optional[float]
```

## Examples

### 1. Search Scraping

```python
# Scrape search results for "chanel bag"
products = await scraper.scrape_search_page("chanel bag", page=1, country="uk")
```

### 2. Product Detail Scraping

```python
# Scrape individual product details
product = await scraper.scrape_product_page("https://www.vestiairecollective.co.uk/...")
```

### 3. Paginated Scraping

```python
# Scrape multiple pages
all_products = []
for page in range(1, 4):
    products = await scraper.scrape_search_page("handbag", page=page)
    all_products.extend(products)
    await asyncio.sleep(2)  # Respectful delay
```

### 4. Price Analysis

```python
# Analyze pricing data
products = await scraper.scrape_search_page("luxury watch")
prices = [p.price for p in products if p.price > 0]
avg_price = sum(prices) / len(prices)
```

## Output Formats

### JSON

```json
[
  {
    "id": "123456",
    "title": "Chanel Classic Flap Bag - Medium",
    "price": 4250.0,
    "original_price": 5500.0,
    "currency": "GBP",
    "brand": "Chanel",
    "size": "Medium",
    "condition": "Very Good",
    "image_url": "https://images.vestiairecollective.com/...",
    "product_url": "https://www.vestiairecollective.co.uk/...",
    "seller": "luxury_boutique_paris",
    "discount_percentage": 23.0
  }
]
```

### CSV

```csv
id,title,price,original_price,currency,brand,size,condition,image_url,product_url,seller,discount_percentage
123456,Chanel Classic Flap Bag - Medium,4250.0,5500.0,GBP,Chanel,Medium,Very Good,https://images.vestiairecollective.com/...,https://www.vestiairecollective.co.uk/...,luxury_boutique_paris,23.0
```

## Configuration

### Scrapfly Options

The scraper uses the following Scrapfly configurations:

- **ASP (Anti-Scraping Protection)**: Enabled
- **JavaScript Rendering**: Enabled
- **Proxy Country**: GB (United Kingdom)
- **Rate Limiting**: 1 concurrent scrape

### Custom Headers

```python
headers = {
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}
```

## Error Handling

The scraper includes comprehensive error handling:

- Network errors are caught and logged
- Invalid product data is skipped
- Rate limiting is respected
- Graceful fallback for missing data

## Testing

```bash
# Run tests
poetry run pytest test.py

# Run specific test
poetry run pytest test.py -k test_product_scraping
poetry run pytest test.py -k test_search_scraping
```

## Results

Check the `./results` directory for output files:

- `chanel_bag_search.json` - Search results
- `chanel_bag_search.csv` - Search results in CSV format
- `product_123456_details.json` - Individual product details
- `handbag_multipage_search.json` - Multi-page search results
- `luxury_handbag_price_analysis.json` - Price analysis data

## Best Practices

1. **Rate Limiting**: Always include delays between requests
2. **Respectful Scraping**: Don't overload the server
3. **Error Handling**: Handle network errors gracefully
4. **Data Validation**: Validate scraped data before use
5. **Monitor Usage**: Keep track of your Scrapfly API usage

## Troubleshooting

### Common Issues

1. **API Key Not Found**
   ```bash
   export SCRAPFLY_KEY="your-api-key-here"
   ```

2. **No Products Found**
   - Check if the search query is valid
   - Verify the country code is correct
   - Check Vestiairecollective.com status

3. **Rate Limiting**
   - Reduce concurrent requests
   - Add longer delays between requests

4. **Parsing Errors**
   - Website structure may have changed
   - Check if selectors need updating

## Legal Notice

This scraper is for educational and research purposes only. Please ensure you comply with:

- Vestiairecollective.com Terms of Service
- Scrapfly.io Terms of Service
- Applicable data protection laws
- Website robots.txt

## Support

For issues related to:
- **Scrapfly.io**: Contact Scrapfly support
- **This scraper**: Check the tutorial at https://scrapfly.io/blog/how-to-scrape-vestiairecollective/

## License

This project is provided as-is for educational purposes. Please refer to the Scrapfly.io terms of service for usage guidelines.
