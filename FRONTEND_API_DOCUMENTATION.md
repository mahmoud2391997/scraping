# Frontend API Documentation
## Complete Guide for Using All Scraping Endpoints

This documentation provides comprehensive guidance for frontend developers to integrate with all three scraping APIs (Vestiaire, eBay, Vinted) with full feature support.

---

## 🏗️ API Architecture Overview

### Base URL
```
https://your-domain.com
```

### Available Endpoints
- **Vestiaire**: `/vestiaire` - Official API integration
- **eBay**: `/ebay` - eBay scraper
- **eBay Sold**: `/ebay/sold` - eBay sold items
- **Vinted**: `/` - Vinted scraper (root endpoint)
- **Vinted Sold**: `/vinted/sold` - Vinted sold items
- **Health**: `/health` - System health monitoring
- **Cache**: `/cache/clear` - Cache management

---

## 👜 Vestiaire Collective API

### Endpoint
```
GET /vestiaire
```

### Features
- ✅ Official Vestiaire API integration
- ✅ 200+ products per request
- ✅ Real-time pricing and availability
- ✅ Advanced filtering options
- ✅ Limitation avoidance (rate limiting, caching, circuit breaker)

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|--------|----------|---------|-------------|
| `search` | string | No | "" | Search query (e.g., "chanel bag") |
| `items_per_page` | integer | No | 48 | Number of items per page (max 200) |
| `page` | integer | No | 1 | Page number for pagination |
| `min_price` | number | No | null | Minimum price filter |
| `max_price` | number | No | null | Maximum price filter |
| `country` | string | No | "us" | Country code (us, uk, fr, etc.) |

### Request Examples

#### Basic Search
```javascript
// Fetch 200 products
const response = await fetch('/vestiaire?items_per_page=200');
const data = await response.json();
```

#### Search with Filters
```javascript
// Search Chanel bags between $100-$1000
const response = await fetch('/vestiaire?search=chanel%20bag&min_price=100&max_price=1000&items_per_page=50');
const data = await response.json();
```

#### Paginated Search
```javascript
// Get page 2 of results
const response = await fetch('/vestiaire?search=bag&page=2&items_per_page=48');
const data = await response.json();
```

### Response Format
```json
{
  "success": true,
  "data": [
    {
      "Title": "Slingback leather ballet flats",
      "Price": "USD 450",
      "Brand": "Chanel",
      "Size": "37",
      "Image": "https://images.vestiairecollective.com/...",
      "Link": "https://www.vestiairecollective.com/p-63095758",
      "Condition": "Very Good",
      "Seller": "LuxuryBoutique",
      "Country": "US",
      "OriginalPrice": "USD 650",
      "Discount": "30%"
    }
  ],
  "count": 200,
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "has_more": true,
    "items_per_page": 200,
    "total_items": 1000
  }
}
```

### Frontend Integration Example

#### React Component
```jsx
import React, { useState, useEffect } from 'react';

function VestiaireSearch() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchProducts = async (searchTerm, minPrice, maxPrice) => {
    setLoading(true);
    setError(null);
    
    try {
      const params = new URLSearchParams({
        search: searchTerm,
        min_price: minPrice,
        max_price: maxPrice,
        items_per_page: 50
      });
      
      const response = await fetch(`/vestiaire?${params}`);
      const data = await response.json();
      
      if (data.success) {
        setProducts(data.data);
      } else {
        setError('Failed to fetch products');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        placeholder="Search Chanel bags..."
        onChange={(e) => fetchProducts(e.target.value)}
      />
      {loading && <div>Loading...</div>}
      {error && <div>{error}</div>}
      {products.map(product => (
        <div key={product.Link}>
          <h3>{product.Title}</h3>
          <p>{product.Price}</p>
          <p>{product.Brand}</p>
          <img src={product.Image} alt={product.Title} />
        </div>
      ))}
    </div>
  );
}
```

---

## 🛒 eBay API

### Endpoint
```
GET /ebay
```

### Features
- ✅ eBay marketplace scraping
- ✅ Price filtering and sorting
- ✅ Multiple category support
- ✅ Sold items tracking
- ✅ Rate limiting and caching

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|--------|----------|---------|-------------|
| `search` | string | No | "" | Search query (e.g., "iphone 13") |
| `items_per_page` | integer | No | 50 | Number of items per page (max 200) |
| `page` | integer | No | 1 | Page number for pagination |
| `min_price` | number | No | null | Minimum price filter |
| `max_price` | number | No | null | Maximum price filter |
| `country` | string | No | "uk" | Country code (uk, us, de, etc.) |

### Request Examples

#### Basic Search
```javascript
// Search for iPhones
const response = await fetch('/ebay?search=iphone%2013&items_per_page=50');
const data = await response.json();
```

#### Price Filtering
```javascript
// iPhones between $200-$800
const response = await fetch('/ebay?search=iphone&min_price=200&max_price=800&items_per_page=25');
const data = await response.json();
```

### Response Format
```json
{
  "success": true,
  "data": [
    {
      "Title": "Apple iPhone 13 Pro - 128GB",
      "Price": "£650.00",
      "Brand": "Apple",
      "Size": "128GB",
      "Image": "https://i.ebayimg.com/...",
      "Link": "https://www.ebay.co.uk/itm/...",
      "Condition": "Used",
      "Seller": "tech_store_uk",
      "Country": "UK"
    }
  ],
  "count": 50,
  "pagination": {
    "current_page": 1,
    "total_pages": 4,
    "has_more": true,
    "items_per_page": 50,
    "total_items": 200
  }
}
```

---

## 🛒 eBay Sold Items

### Endpoint
```
GET /ebay/sold
```

### Request Examples
```javascript
// Search sold iPhones
const response = await fetch('/ebay/sold?search=iphone&items_per_page=50');
const data = await response.json();
```

---

## 🧥 Vinted API

### Endpoint
```
GET /
```

### Features
- ✅ Vinted marketplace scraping
- ✅ Price filtering and size options
- ✅ Sold items tracking
- ✅ Brand and category filtering
- ✅ Rate limiting and caching

### Request Parameters

| Parameter | Type | Required | Default | Description |
|-----------|--------|----------|---------|-------------|
| `search` | string | No | "" | Search query (e.g., "nike jacket") |
| `items_per_page` | integer | No | 50 | Number of items per page (max 200) |
| `page` | integer | No | 1 | Page number for pagination |
| `min_price` | number | No | null | Minimum price filter |
| `max_price` | number | No | null | Maximum price filter |
| `country` | string | No | "uk" | Country code |

### Request Examples

#### Basic Search
```javascript
// Search for Nike items
const response = await fetch('/?search=nike&items_per_page=50');
const data = await response.json();
```

#### Price Filtering
```javascript
// Nike items between $20-$100
const response = await fetch('/?search=nike&min_price=20&max_price=100&items_per_page=25');
const data = await response.json();
```

---

## 🧥 Vinted Sold Items

### Endpoint
```
GET /vinted/sold
```

### Request Examples
```javascript
// Search sold Supreme items
const response = await fetch('/vinted/sold?search=supreme&items_per_page=50');
const data = await response.json();
```

---

## 🏥 Health Monitoring

### Endpoint
```
GET /health
```

### Response Format
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": 1705123456.789,
    "performance": {
      "cache_stats": {
        "hit_rate": 0.75,
        "total_hits": 150,
        "total_misses": 50,
        "cached_items": 25
      },
      "rate_limiter": {
        "current_limit": 20,
        "max_limit": 20
      },
      "circuit_breaker": {
        "state": "CLOSED",
        "failure_count": 0,
        "failure_threshold": 3
      }
    },
    "endpoints": {
      "vestiaire": "operational",
      "ebay": "operational",
      "vinted": "operational"
    },
    "environment": {
      "scrapfly_key_configured": true,
      "ebay_app_id_configured": true,
      "python_version": "3.9.6"
    }
  },
  "count": 5,
  "pagination": null
}
```

---

## 🧹 Cache Management

### Endpoint
```
GET /cache/clear
```

### Response Format
```json
{
  "success": true,
  "message": "Cache cleared successfully",
  "data": {
    "cache_cleared": true,
    "rate_limit_reset": true,
    "circuit_breaker_reset": true
  }
}
```

---

## 🎨 Frontend Implementation Guide

### Universal API Client

#### JavaScript/TypeScript
```typescript
class ScrapingAPI {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  // Universal search method
  async search(
    site: 'vestiaire' | 'ebay' | 'vinted',
    params: {
      search?: string;
      items_per_page?: number;
      page?: number;
      min_price?: number;
      max_price?: number;
      country?: string;
    } = {}
  ) {
    const searchParams = new URLSearchParams();
    
    // Add parameters
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value.toString());
      }
    });

    // Build endpoint URL
    let endpoint = '';
    switch (site) {
      case 'vestiaire':
        endpoint = '/vestiaire';
        break;
      case 'ebay':
        endpoint = '/ebay';
        break;
      case 'vinted':
        endpoint = '/';
        break;
      case 'ebay_sold':
        endpoint = '/ebay/sold';
        break;
      case 'vinted_sold':
        endpoint = '/vinted/sold';
        break;
    }

    const url = `${this.baseURL}${endpoint}?${searchParams}`;
    
    try {
      const response = await fetch(url);
      const data = await response.json();
      
      if (!data.success) {
        throw new Error(`API Error: ${data.error || 'Unknown error'}`);
      }
      
      return data;
    } catch (error) {
      console.error('Search failed:', error);
      throw error;
    }
  }

  // Convenience methods
  async searchVestiaire(params: any) {
    return this.search('vestiaire', params);
  }

  async searchEbay(params: any) {
    return this.search('ebay', params);
  }

  async searchEbaySold(params: any) {
    return this.search('ebay_sold', params);
  }

  async searchVinted(params: any) {
    return this.search('vinted', params);
  }

  async searchVintedSold(params: any) {
    return this.search('vinted_sold', params);
  }

  // Health check
  async healthCheck() {
    const response = await fetch(`${this.baseURL}/health`);
    return await response.json();
  }

  // Cache management
  async clearCache() {
    const response = await fetch(`${this.baseURL}/cache/clear`);
    return await response.json();
  }
}

// Usage
const api = new ScrapingAPI('https://your-domain.com');

// Search Vestiaire for Chanel bags
const vestiaireResults = await api.searchVestiaire({
  search: 'chanel bag',
  items_per_page: 50,
  min_price: 100,
  max_price: 1000
});

// Search eBay for iPhones
const ebayResults = await api.searchEbay({
  search: 'iphone 13',
  items_per_page: 25
});

// Search Vinted for Nike
const vintedResults = await api.searchVinted({
  search: 'nike jacket',
  items_per_page: 50,
  min_price: 20,
  max_price: 100
});
```

#### React Hook
```typescript
import { useState, useCallback } from 'react';
import { ScrapingAPI } from './api';

export function useScrapingAPI() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const api = new ScrapingAPI('https://your-domain.com');

  const search = useCallback(async (site: string, params: any) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.search(site as any, params);
      setLoading(false);
      return result;
    } catch (err) {
      setError(err.message);
      setLoading(false);
      throw err;
    }
  }, [api]);

  return { search, loading, error };
}
```

---

## 🎯 Best Practices

### Rate Limiting
- **Recommended**: 1-2 requests per second per client
- **Implementation**: Add delays between requests
- **Monitoring**: Use `/health` endpoint to check rate limiter status

### Caching Strategy
- **Duration**: 15 minutes for product data
- **Invalidation**: Clear cache when prices might change
- **Monitoring**: Track hit rates via `/health` endpoint

### Error Handling
```typescript
try {
  const result = await api.search('vestiaire', params);
  // Handle success
} catch (error) {
  if (error.message.includes('429')) {
    // Rate limited - wait and retry
    await new Promise(resolve => setTimeout(resolve, 2000));
    return await api.search('vestiaire', params);
  } else if (error.message.includes('503')) {
    // Service unavailable - show user message
    showUserMessage('Service temporarily unavailable');
  } else {
    // Other error - log and show generic message
    console.error('API Error:', error);
    showUserMessage('Search failed. Please try again.');
  }
}
```

### Pagination Implementation
```typescript
interface PaginationData {
  current_page: number;
  total_pages: number;
  has_more: boolean;
  items_per_page: number;
  total_items: number;
}

const loadMore = async (currentPage: number) => {
  const nextPage = currentPage + 1;
  const result = await api.search('vestiaire', {
    search: currentSearch,
    page: nextPage,
    items_per_page: 50
  });
  
  return result;
};
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Required for Vestiaire
SCRAPFLY_KEY=your_scrapfly_api_key

# Required for eBay
EBAY_APP_ID=your_ebay_app_id
EBAY_CERT_ID=your_ebay_cert_id

# Optional: API rate limiting
API_RATE_LIMIT=20
CACHE_DURATION=900
```

### Deployment Notes
- **Production URL**: Update `baseURL` in API client
- **HTTPS**: Use HTTPS in production
- **CORS**: Ensure backend allows frontend domain
- **Monitoring**: Set up health check monitoring

---

## 📱 Mobile App Integration

### React Native Example
```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = new ScrapingAPI('https://your-domain.com');

// Store search history
const saveSearchHistory = async (search: string) => {
  try {
    const history = await AsyncStorage.getItem('searchHistory');
    const searches = history ? JSON.parse(history) : [];
    searches.unshift(search);
    await AsyncStorage.setItem('searchHistory', JSON.stringify(searches.slice(0, 10)));
  } catch (error) {
    console.error('Failed to save search:', error);
  }
};

// Offline caching
const cacheResults = async (key: string, data: any) => {
  try {
    await AsyncStorage.setItem(key, JSON.stringify({
      data,
      timestamp: Date.now(),
      ttl: 15 * 60 * 1000 // 15 minutes
    }));
  } catch (error) {
    console.error('Failed to cache:', error);
  }
};
```

---

## 🎨 UI Components

### Search Bar Component
```jsx
const SearchBar = ({ onSearch, loading }) => {
  const [query, setQuery] = useState('');
  const [filters, setFilters] = useState({
    minPrice: '',
    maxPrice: '',
    site: 'vestiaire'
  });

  const handleSearch = () => {
    onSearch({
      site: filters.site,
      search: query,
      min_price: filters.minPrice || undefined,
      max_price: filters.maxPrice || undefined,
      items_per_page: 50
    });
  };

  return (
    <div className="search-container">
      <select 
        value={filters.site} 
        onChange={(e) => setFilters({...filters, site: e.target.value})}
      >
        <option value="vestiaire">Vestiaire</option>
        <option value="ebay">eBay</option>
        <option value="vinted">Vinted</option>
      </select>
      
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for luxury items..."
        onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
      />
      
      <div className="price-filters">
        <input
          type="number"
          placeholder="Min Price"
          value={filters.minPrice}
          onChange={(e) => setFilters({...filters, minPrice: e.target.value})}
        />
        <input
          type="number"
          placeholder="Max Price"
          value={filters.maxPrice}
          onChange={(e) => setFilters({...filters, maxPrice: e.target.value})}
        />
      </div>
      
      <button onClick={handleSearch} disabled={loading}>
        {loading ? 'Searching...' : 'Search'}
      </button>
    </div>
  );
};
```

---

## 📊 Analytics Integration

### Track API Usage
```typescript
interface AnalyticsEvent {
  event: 'search' | 'filter' | 'pagination';
  site: string;
  params: Record<string, any>;
  response_time: number;
  success: boolean;
}

const trackAPIUsage = (event: AnalyticsEvent) => {
  // Send to your analytics service
  analytics.track('api_usage', {
    event: event.event,
    site: event.site,
    params: event.params,
    response_time: event.response_time,
    success: event.success,
    timestamp: new Date().toISOString()
  });
};

// Wrap API calls
const trackedSearch = async (site: string, params: any) => {
  const startTime = Date.now();
  
  try {
    const result = await api.search(site, params);
    const responseTime = Date.now() - startTime;
    
    trackAPIUsage({
      event: 'search',
      site,
      params,
      response_time: responseTime,
      success: true
    });
    
    return result;
  } catch (error) {
    const responseTime = Date.now() - startTime;
    
    trackAPIUsage({
      event: 'search',
      site,
      params,
      response_time: responseTime,
      success: false
    });
    
    throw error;
  }
};
```

---

## 🚀 Production Deployment

### Environment Setup
```bash
# Production environment variables
export NODE_ENV=production
export API_BASE_URL=https://your-domain.com
export SCRAPFLY_KEY=prod_key_here
export EBAY_APP_ID=prod_ebay_id
export API_RATE_LIMIT=20
```

### Docker Configuration
```dockerfile
FROM node:18-alpine

ENV NODE_ENV=production
ENV API_BASE_URL=https://your-domain.com
ENV API_RATE_LIMIT=20

COPY package*.json ./
RUN npm ci --only=production

EXPOSE 3000
CMD ["npm", "start"]
```

### Monitoring Setup
```typescript
// Health check monitoring
const monitorHealth = async () => {
  try {
    const health = await api.healthCheck();
    
    if (health.data.status !== 'healthy') {
      // Alert monitoring service
      await alertMonitoringService({
        level: 'error',
        message: 'API health check failed',
        details: health
      });
    }
    
    // Check performance metrics
    const cacheHitRate = health.data.performance.cache_stats.hit_rate;
    if (cacheHitRate < 0.5) {
      await alertMonitoringService({
        level: 'warning',
        message: 'Low cache hit rate',
        details: { hit_rate: cacheHitRate }
      });
    }
  } catch (error) {
    await alertMonitoringService({
      level: 'critical',
      message: 'Health monitoring failed',
      details: error
    });
  }
};

// Run every 5 minutes
setInterval(monitorHealth, 5 * 60 * 1000);
```

---

## 📞 Support & Troubleshooting

### Common Issues

#### Rate Limiting (429)
```typescript
// Implement exponential backoff
const retryWithBackoff = async (fn: Function, maxRetries: number = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.status === 429) {
        const waitTime = Math.pow(2, i) * 1000; // 1s, 2s, 4s
        await new Promise(resolve => setTimeout(resolve, waitTime));
        continue;
      }
      throw error;
    }
  }
};
```

#### Empty Results
```typescript
// Handle empty results gracefully
const handleEmptyResults = (data: any) => {
  if (data.count === 0) {
    return {
      hasResults: false,
      message: 'No items found. Try adjusting your search or filters.',
      suggestions: [
        'Try different keywords',
        'Remove price filters',
        'Check spelling'
      ]
    };
  }
  
  return {
    hasResults: true,
    data: data.data
  };
};
```

### Error Codes Reference
| Code | Description | Solution |
|-------|-------------|---------|
| 200 | Success | Continue processing |
| 400 | Bad Request | Check parameters |
| 429 | Rate Limited | Implement backoff |
| 500 | Server Error | Retry with exponential backoff |
| 503 | Service Unavailable | Wait and retry |

---

## 🎯 Quick Start Guide

### 1. Basic Setup
```bash
# Install dependencies
npm install

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Start development server
npm start
```

### 2. First API Call
```javascript
// Test basic functionality
const test = async () => {
  try {
    const result = await api.searchVestiaire({
      search: 'chanel',
      items_per_page: 10
    });
    console.log('Success:', result);
  } catch (error) {
    console.error('Error:', error);
  }
};

test();
```

### 3. Build Features
- Search functionality
- Price filtering
- Pagination
- Error handling
- Loading states
- Result display

---

## 📞 Contact & Support

For technical support:
- **API Issues**: Check `/health` endpoint status
- **Rate Limiting**: Review request patterns
- **Documentation**: This file provides complete integration guide

---

*Last updated: January 2026*
*Version: 1.0.0*
*API Version: v1.0*
