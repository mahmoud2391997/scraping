# 📱 Frontend Integration README

**Goal:** this guide shows **frontend developers** how to call the scraping API (locally or in production) from JavaScript/TypeScript apps (React, Next.js, etc.).

---

## 🌐 Base URLs

- **Local development** (when you run the server yourself):
  - `http://localhost:8099`
- **Production demo** (already deployed):
  - `https://vinted-scraping.vercel.app/`

In all examples below:
- Replace `http://localhost:8099` with `https://vinted-scraping.vercel.app` when calling the **live API**.

### Key Endpoints

- **Vinted search**: `GET /`
- **eBay search**: `GET /ebay`
- **eBay sold items**: `GET /ebay/sold`
- **Vinted sold items**: `GET /vinted/sold`
- **Vestiaire**: `GET /vestiaire`

---

## 🚀 Quick Start (Frontend)

### 1. Basic API Call (JavaScript)

```javascript
// eBay Search
const searchEBay = async (query, country = 'uk') => {
  try {
    const response = await fetch(`http://localhost:8099/ebay?search=${query}&country=${country}&items_per_page=10`);
    const data = await response.json();
    
    if (data.success) {
      return data;
    } else {
      throw new Error(data.error || 'Search failed');
    }
  } catch (error) {
    console.error('API Error:', error);
    return null;
  }
};

// Usage
searchEBay('iphone', 'uk').then(result => {
  console.log('Products:', result.data);
  console.log('Pagination:', result.pagination);
});
```

### 2. React Component Example

```jsx
import React, { useState, useEffect } from 'react';

const ProductSearch = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('iphone');
  const [pagination, setPagination] = useState(null);

  const searchProducts = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8099/ebay?search=${searchTerm}&country=uk&items_per_page=12`
      );
      const data = await response.json();
      
      if (data.success) {
        setProducts(data.data);
        setPagination(data.pagination);
      }
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    searchProducts();
  }, [searchTerm]);

  return (
    <div>
      <input 
        type="text" 
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search products..."
      />
      
      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="product-grid">
          {products.map((product, index) => (
            <ProductCard key={index} product={product} />
          ))}
        </div>
      )}
      
      {pagination && (
        <PaginationComponent pagination={pagination} />
      )}
    </div>
  );
};
```

### 3. Product Card Component

```jsx
const ProductCard = ({ product }) => {
  return (
    <div className="product-card">
      <img 
        src={product.Image} 
        alt={product.Title}
        onError={(e) => {
          e.target.src = '/placeholder-image.jpg';
        }}
      />
      <h3>{product.Title}</h3>
      <p className="price">{product.Price}</p>
      <p className="brand">{product.Brand}</p>
      <p className="condition">{product.Condition}</p>
      <p className="seller">Sold by {product.Seller}</p>
      <a href={product.Link} target="_blank" rel="noopener noreferrer">
        View on eBay
      </a>
    </div>
  );
};
```

---

## 📊 API Response Format

### Success Response
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

### Error Response
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

---

## 🔧 Query Parameters

| Parameter | Type | Required | Default | Example |
|-----------|------|----------|---------|---------|
| `search` | string | No | "laptop" | "iphone" |
| `country` | string | No | "uk" | "us", "de", "fr" |
| `page` | integer | No | 1 | 2 |
| `items_per_page` | integer | No | 50 | 10 |
| `min_price` | float | No | null | 100 |
| `max_price` | float | No | null | 500 |

---

## 🎯 Frontend Features Implementation

### 1. Search Functionality

```javascript
// Search with filters
const searchWithFilters = async (filters) => {
  const params = new URLSearchParams();
  
  if (filters.search) params.append('search', filters.search);
  if (filters.country) params.append('country', filters.country);
  if (filters.minPrice) params.append('min_price', filters.minPrice);
  if (filters.maxPrice) params.append('max_price', filters.maxPrice);
  if (filters.page) params.append('page', filters.page);
  if (filters.itemsPerPage) params.append('items_per_page', filters.itemsPerPage);
  
  const response = await fetch(`http://localhost:8099/ebay?${params}`);
  return await response.json();
};

// Usage
const filters = {
  search: 'laptop',
  country: 'us',
  minPrice: 500,
  maxPrice: 1500,
  page: 1,
  itemsPerPage: 20
};

searchWithFilters(filters);
```

### 2. Price Range Filter

```jsx
const PriceFilter = ({ onFilterChange }) => {
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');

  const applyFilter = () => {
    onFilterChange({
      minPrice: minPrice || null,
      maxPrice: maxPrice || null
    });
  };

  return (
    <div className="price-filter">
      <input
        type="number"
        placeholder="Min Price"
        value={minPrice}
        onChange={(e) => setMinPrice(e.target.value)}
      />
      <input
        type="number"
        placeholder="Max Price"
        value={maxPrice}
        onChange={(e) => setMaxPrice(e.target.value)}
      />
      <button onClick={applyFilter}>Apply Filter</button>
    </div>
  );
};
```

### 3. Pagination Component

```jsx
const PaginationComponent = ({ pagination, onPageChange }) => {
  if (!pagination || pagination.total_pages <= 1) return null;

  const { current_page, total_pages, has_more } = pagination;

  return (
    <div className="pagination">
      <button 
        onClick={() => onPageChange(current_page - 1)}
        disabled={current_page <= 1}
      >
        Previous
      </button>
      
      <span className="page-info">
        Page {current_page} of {total_pages}
      </span>
      
      <button 
        onClick={() => onPageChange(current_page + 1)}
        disabled={!has_more}
      >
        Next
      </button>
    </div>
  );
};
```

### 4. Country Selector

```jsx
const CountrySelector = ({ selectedCountry, onCountryChange }) => {
  const countries = [
    { code: 'uk', name: 'United Kingdom' },
    { code: 'us', name: 'United States' },
    { code: 'de', name: 'Germany' },
    { code: 'fr', name: 'France' },
    { code: 'it', name: 'Italy' },
    { code: 'es', name: 'Spain' },
    { code: 'ca', name: 'Canada' },
    { code: 'au', name: 'Australia' }
  ];

  return (
    <select 
      value={selectedCountry} 
      onChange={(e) => onCountryChange(e.target.value)}
    >
      {countries.map(country => (
        <option key={country.code} value={country.code}>
          {country.name}
        </option>
      ))}
    </select>
  );
};
```

---

## 🎨 CSS Styling Examples

### Product Grid Layout
```css
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.product-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 10px;
}

.product-card h3 {
  font-size: 16px;
  margin: 10px 0;
  color: #333;
}

.price {
  font-size: 18px;
  font-weight: bold;
  color: #2c5aa0;
  margin: 5px 0;
}

.brand, .condition, .seller {
  font-size: 14px;
  color: #666;
  margin: 2px 0;
}

.product-card a {
  display: inline-block;
  margin-top: 10px;
  padding: 8px 16px;
  background: #2c5aa0;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  text-align: center;
}
```

### Loading and Error States
```css
.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #666;
}

.error {
  text-align: center;
  padding: 40px;
  color: #d32f2f;
  background: #ffebee;
  border-radius: 4px;
  margin: 20px 0;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

.pagination button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
  background: #f5f5f5;
}
```

---

## 🔄 Advanced Usage

### 1. Custom Hook for API Calls

```javascript
import { useState, useEffect } from 'react';

const useProductSearch = (initialQuery = 'laptop') => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState(null);

  const search = async (query, filters = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const params = new URLSearchParams({
        search: query,
        country: filters.country || 'uk',
        items_per_page: filters.itemsPerPage || 20,
        page: filters.page || 1,
        ...(filters.minPrice && { min_price: filters.minPrice }),
        ...(filters.maxPrice && { max_price: filters.maxPrice })
      });

      const response = await fetch(`http://localhost:8099/ebay?${params}`);
      const data = await response.json();

      if (data.success) {
        setProducts(data.data);
        setPagination(data.pagination);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    search(initialQuery);
  }, [initialQuery]);

  return { products, loading, error, pagination, search };
};

// Usage
const ProductList = () => {
  const { products, loading, error, pagination, search } = useProductSearch('iphone');

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div>
      <div className="product-grid">
        {products.map((product, index) => (
          <ProductCard key={index} product={product} />
        ))}
      </div>
    </div>
  );
};
```

### 2. Debounced Search

```javascript
import { useCallback, useEffect } from 'react';

const useDebounce = (callback, delay) => {
  const [debounceTimer, setDebounceTimer] = useState(null);

  return useCallback((...args) => {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }
    
    const timer = setTimeout(() => {
      callback(...args);
    }, delay);
    
    setDebounceTimer(timer);
  }, [callback, delay, debounceTimer]);
};

// Usage in search component
const SearchComponent = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const { search } = useProductSearch();

  const debouncedSearch = useDebounce((term) => {
    search(term);
  }, 500);

  useEffect(() => {
    if (searchTerm) {
      debouncedSearch(searchTerm);
    }
  }, [searchTerm, debouncedSearch]);

  return (
    <input
      type="text"
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
      placeholder="Search products..."
    />
  );
};
```

---

## 📱 Mobile Responsive Design

```css
/* Mobile-first responsive design */
@media (max-width: 768px) {
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 10px;
    padding: 10px;
  }
  
  .product-card {
    padding: 10px;
  }
  
  .product-card img {
    height: 150px;
  }
  
  .product-card h3 {
    font-size: 14px;
  }
  
  .price {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
  
  .pagination {
    flex-direction: column;
    gap: 10px;
  }
}
```

---

## 🚨 Error Handling

### Frontend Error Handling

```javascript
const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    switch (error.response.status) {
      case 429:
        return 'Rate limit exceeded. Please try again later.';
      case 500:
        return 'Server error. Please try again later.';
      default:
        return 'An error occurred. Please try again.';
    }
  } else if (error.request) {
    // Network error
    return 'Network error. Please check your connection.';
  } else {
    // Other error
    return error.message || 'An unknown error occurred.';
  }
};

// Usage with try-catch
try {
  const response = await fetch('http://localhost:8099/ebay?search=iphone');
  const data = await response.json();
  
  if (!data.success) {
    throw new Error(data.error);
  }
  
  return data;
} catch (error) {
  const errorMessage = handleApiError(error);
  console.error('API Error:', errorMessage);
  // Show error to user
}
```

---

## 🎯 Best Practices

### 1. Loading States
- Show loading indicators during API calls
- Disable buttons during loading
- Provide skeleton loaders for better UX

### 2. Error Handling
- Display user-friendly error messages
- Implement retry mechanisms for failed requests
- Log errors for debugging

### 3. Performance
- Implement pagination to avoid loading too many items at once
- Use image lazy loading
- Cache API responses when appropriate

### 4. User Experience
- Implement search debouncing
- Provide clear feedback for user actions
- Ensure responsive design for all devices

---

## 📞 Support

- **Local Server**: http://localhost:8099
- **API Documentation**: See README.md for complete API reference
- **Issues**: Report bugs and feature requests

---

**🎯 Your frontend integration is ready to go!**

*Built with modern React patterns and best practices*
