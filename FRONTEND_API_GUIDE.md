# 🚀 Frontend API Integration Guide

## 📡 Live Deployment URL
**Base URL**: `https://scraping-iti1.vercel.app`

## � CORS Enabled
✅ **Cross-Origin Resource Sharing (CORS) is enabled** - You can now access this API from any domain, including:
- Local development (`http://localhost:3000`, `http://127.0.0.1:5500`, etc.)
- Production websites
- Mobile applications
- Any frontend framework

No additional configuration needed - just make your API calls!

## � Quick Start

### Basic API Call
```javascript
const response = await fetch('https://scraping-iti1.vercel.app/?search=nike&items_per_page=10');
const data = await response.json();
console.log(data);
```

### Health Check
```javascript
const health = await fetch('https://scraping-iti1.vercel.app/health');
const status = await health.json();
console.log(status.data.status); // "healthy"
```

### CORS Test (Run in Browser Console)
```javascript
// Test CORS from any domain - this will work!
fetch('https://scraping-iti1.vercel.app/?search=test&items_per_page=1')
  .then(response => response.json())
  .then(data => console.log('CORS Test Success:', data))
  .catch(error => console.error('CORS Error:', error));
```

## 📋 Available Endpoints

### 1. Vinted Scraper (Default)
```javascript
// Search for products
const vintedData = await fetch('https://scraping-iti1.vercel.app/?search=nike&items_per_page=5');
```

### 2. Vestiaire Collective Scraper
```javascript
// Search luxury fashion
const vestiaireData = await fetch('https://scraping-iti1.vercel.app/vestiaire?search=chanel&items_per_page=5');
```

### 3. Health Monitor
```javascript
// Check API status
const healthData = await fetch('https://scraping-iti1.vercel.app/health');
```

## 🔧 Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `search` | string | ✅ Yes | - | Search query term |
| `items_per_page` | number | ❌ No | 50 | Number of items (1-50) |
| `page` | number | ❌ No | 1 | Page number for pagination |
| `min_price` | number | ❌ No | - | Minimum price filter |
| `max_price` | number | ❌ No | - | Maximum price filter |
| `country` | string | ❌ No | uk | Country code (uk, us, de, fr, it, es, etc.) |

## 📊 Response Format

### Success Response
```json
{
  "success": true,
  "data": [
    {
      "Title": "Nike beanie",
      "Price": "5.00£",
      "Brand": "Nike",
      "Size": "N/A",
      "Image": "https://images1.vinted.net/...",
      "Link": "https://www.vinted.co.uk/items/...",
      "Condition": "Good",
      "Seller": "seller_name"
    }
  ],
  "count": 5,
  "pagination": {
    "current_page": 1,
    "total_pages": 20,
    "has_more": true,
    "items_per_page": 5,
    "total_items": 96
  },
  "error": null
}
```

### Health Response
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": 1769735091.575767,
    "performance": {
      "cache_stats": { "hit_rate": 0, "total_hits": 0 },
      "rate_limiter": { "current_limit": 20 },
      "circuit_breaker": { "state": "CLOSED" }
    },
    "endpoints": {
      "vestiaire": "operational",
      "vinted": "operational"
    }
  }
}
```

## 💻 Frontend Integration Examples

### React Example
```jsx
import React, { useState, useEffect } from 'react';

function ProductSearch() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const searchProducts = async (query, page = 1) => {
    setLoading(true);
    try {
      const response = await fetch(
        `https://scraping-iti1.vercel.app/?search=${query}&items_per_page=10&page=${page}`
      );
      const data = await response.json();
      
      if (data.success) {
        setProducts(data.data);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('Failed to fetch products');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search products..."
        onChange={(e) => searchProducts(e.target.value)}
      />
      {loading && <div>Loading...</div>}
      {error && <div>Error: {error}</div>}
      <div>
        {products.map((product, index) => (
          <div key={index}>
            <h3>{product.Title}</h3>
            <p>Price: {product.Price}</p>
            <p>Brand: {product.Brand}</p>
            <img src={product.Image} alt={product.Title} />
            <a href={product.Link} target="_blank">View Product</a>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Vanilla JavaScript Example
```html
<!DOCTYPE html>
<html>
<head>
    <title>Fashion Scraper API</title>
</head>
<body>
    <input type="text" id="searchInput" placeholder="Search for products...">
    <button onclick="searchProducts()">Search</button>
    <div id="results"></div>

    <script>
        async function searchProducts() {
            const query = document.getElementById('searchInput').value;
            const resultsDiv = document.getElementById('results');
            
            resultsDiv.innerHTML = '<div>Loading...</div>';
            
            try {
                const response = await fetch(
                    `https://scraping-iti1.vercel.app/?search=${query}&items_per_page=10`
                );
                const data = await response.json();
                
                if (data.success) {
                    resultsDiv.innerHTML = data.data.map(product => `
                        <div style="border: 1px solid #ccc; margin: 10px; padding: 10px;">
                            <h3>${product.Title}</h3>
                            <p><strong>Price:</strong> ${product.Price}</p>
                            <p><strong>Brand:</strong> ${product.Brand}</p>
                            <p><strong>Size:</strong> ${product.Size}</p>
                            <p><strong>Condition:</strong> ${product.Condition}</p>
                            <img src="${product.Image}" alt="${product.Title}" style="max-width: 200px;">
                            <br>
                            <a href="${product.Link}" target="_blank">View Product</a>
                        </div>
                    `).join('');
                } else {
                    resultsDiv.innerHTML = `<div>Error: ${data.error}</div>`;
                }
            } catch (error) {
                resultsDiv.innerHTML = `<div>Failed to fetch: ${error.message}</div>`;
            }
        }
    </script>
</body>
</html>
```

### Vue.js Example
```vue
<template>
  <div>
    <input v-model="searchQuery" @keyup.enter="fetchProducts" placeholder="Search products...">
    <button @click="fetchProducts">Search</button>
    
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    
    <div class="products">
      <div v-for="(product, index) in products" :key="index" class="product-card">
        <h3>{{ product.Title }}</h3>
        <p class="price">{{ product.Price }}</p>
        <p class="brand">{{ product.Brand }}</p>
        <img :src="product.Image" :alt="product.Title" class="product-image">
        <a :href="product.Link" target="_blank" class="product-link">View Product</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      products: [],
      loading: false,
      error: null
    };
  },
  methods: {
    async fetchProducts() {
      if (!this.searchQuery.trim()) return;
      
      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetch(
          `https://scraping-iti1.vercel.app/?search=${this.searchQuery}&items_per_page=10`
        );
        const data = await response.json();
        
        if (data.success) {
          this.products = data.data;
        } else {
          this.error = data.error;
        }
      } catch (err) {
        this.error = 'Failed to fetch products';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
```

## 🎨 Styling Tips

### Product Card CSS
```css
.product-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 16px;
  margin: 16px;
  max-width: 300px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.price {
  font-weight: bold;
  color: #2e7d32;
  font-size: 1.2em;
}

.brand {
  color: #666;
  font-style: italic;
}

.product-link {
  display: inline-block;
  background: #1976d2;
  color: white;
  padding: 8px 16px;
  text-decoration: none;
  border-radius: 4px;
  margin-top: 8px;
}

.product-link:hover {
  background: #1565c0;
}
```

## ⚡ Performance Tips

1. **Debounce Search Input**
```javascript
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

const debouncedSearch = debounce(searchProducts, 300);
```

2. **Implement Pagination**
```javascript
const loadMoreProducts = async () => {
  const nextPage = currentPage + 1;
  const response = await fetch(
    `https://scraping-iti1.vercel.app/?search=${query}&page=${nextPage}&items_per_page=10`
  );
  const data = await response.json();
  setProducts(prev => [...prev, ...data.data]);
};
```

3. **Error Handling**
```javascript
try {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data = await response.json();
  // Handle success
} catch (error) {
  console.error('API Error:', error);
  // Show user-friendly error message
}
```

## 🚨 Rate Limiting

- **Limit**: 20 requests per minute
- **Response**: `429 Too Many Requests` if exceeded
- **Solution**: Implement client-side rate limiting and caching

```javascript
// Simple rate limiter
let lastRequest = 0;
const MIN_REQUEST_INTERVAL = 3000; // 3 seconds

async function rateLimitedFetch(url) {
  const now = Date.now();
  if (now - lastRequest < MIN_REQUEST_INTERVAL) {
    await new Promise(resolve => setTimeout(resolve, MIN_REQUEST_INTERVAL - (now - lastRequest)));
  }
  lastRequest = Date.now();
  return fetch(url);
}
```

## 🌍 Supported Countries

### Vinted
- UK, DE, FR, IT, ES, PL, NL, BE, AT, CZ, SK, HU, RO, BG, HR, SI, EE, LV, LT, PT, GR, CY, MT, LU, IE

### Vestiaire Collective
- UK, US, FR (domains)

## 📞 Support

For issues or questions:
1. Check the [health endpoint](https://scraping-iti1.vercel.app/health) for API status
2. Review this documentation for common integration patterns
3. Test with the provided examples before implementing in production

## 🔒 Security Notes

- No API key required for basic usage
- All requests are rate-limited
- Use HTTPS for all API calls
- Validate and sanitize all user inputs
- Implement proper error handling in your frontend

---

**Made with ❤️ for frontend developers**  
**Live API**: https://scraping-iti1.vercel.app
