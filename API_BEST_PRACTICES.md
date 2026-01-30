# eBay API Best Practices & Rate Limiting Guide

## Overview
This document outlines the best practices implemented to prevent 429 (Too Many Requests) errors and ensure reliable eBay API integration.

## 🛡️ **Rate Limiting Implementation**

### **Client-Side Rate Limiting**
```python
class RateLimiter:
    def __init__(self, max_requests_per_minute=30):
        self.max_requests = max_requests_per_minute
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
```

**Features:**
- ✅ **30 requests per minute** (conservative limit)
- ✅ **Per-client tracking** using IP address
- ✅ **Automatic cleanup** of old requests
- ✅ **Thread-safe** implementation

### **API Response Handling**
```python
elif response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 60))
    return {
        'products': [],
        'error': f'API rate limit exceeded. Retry after {retry_after} seconds.'
    }
```

## 🔄 **Retry Logic with Exponential Backoff**

### **Retry Strategy**
```python
def make_api_request_with_retry(self, url, headers, params, max_retries=3):
    for attempt in range(max_retries):
        # Handle 429 with Retry-After header
        # Handle 5xx server errors with exponential backoff
        backoff_time = (2 ** attempt) + 1  # 2, 5, 9 seconds
```

**Retry Cases:**
- ✅ **429 Errors**: Honor `Retry-After` header
- ✅ **5xx Errors**: Exponential backoff (2, 5, 9 seconds)
- ✅ **Network Errors**: Automatic retry with backoff
- ✅ **Max 3 attempts**: Prevent infinite loops

## 💾 **Caching System**

### **Smart Caching**
```python
class CacheManager:
    def __init__(self, cache_duration_minutes=5):
        self.cache_duration = cache_duration_minutes * 60
```

**Cache Features:**
- ✅ **5-minute cache duration** for API responses
- ✅ **Cache key generation**: `ebay_{search}_{page}_{items}_{filters}`
- ✅ **Thread-safe** operations
- ✅ **Automatic expiration** of old cache entries

### **Cache Hit Example**
```
Cache hit for: ebay_laptop_1_3_None_None
```

## 🚀 **Performance Optimizations**

### **Request Headers**
```python
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    'X-EBAY-C-MARKETPLACE-ID': marketplace_id,
    'Accept-Language': 'en-US',
    'User-Agent': 'eBay-API-Client/1.0'
}
```

### **Pagination Optimization**
```python
params = {
    'q': search_text,
    'limit': min(items_per_page, 50),  # Respect API limits
    'offset': (page_number - 1) * items_per_page
}
```

## 📊 **Rate Limits & Quotas**

### **eBay API Limits**
| Environment | Rate Limit | Daily Quota |
|-----------|-----------|------------|
| Sandbox | ~5,000 requests/day | Unlimited |
| Production | Varies by plan | 5,000 - 100,000+ |

### **Our Conservative Settings**
- **30 requests/minute** (50% of typical limit)
- **5-minute cache** (reduces repeat requests)
- **3 retry attempts** (prevents hammering)

## 🔧 **Configuration Options**

### **Environment Variables**
```bash
# Rate Limiting
EBAY_RATE_LIMIT=30          # Requests per minute
EBAY_CACHE_DURATION=5         # Cache duration in minutes

# Retry Settings
EBAY_MAX_RETRIES=3           # Maximum retry attempts
EBAY_BACKOFF_BASE=2          # Exponential backoff base
```

### **Code Configuration**
```python
# Conservative rate limiting
rate_limiter = RateLimiter(max_requests_per_minute=30)

# 5-minute cache
cache_manager = CacheManager(cache_duration_minutes=5)

# 3 retries with exponential backoff
response = self.make_api_request_with_retry(url, headers, params, max_retries=3)
```

## 🛠️ **Monitoring & Debugging**

### **Logging Implementation**
```python
print(f"Cache hit for: {cache_key}")
print(f"Rate limit exceeded for {client_ip}. Waiting {wait_time:.2f} seconds")
print(f"eBay API rate limited. Retry after {retry_after} seconds")
print(f"Server error {response.status_code}. Retrying in {backoff_time} seconds")
```

### **Error Responses**
```json
{
  "success": true,
  "data": [],
  "error": "Rate limit exceeded. Please try again later."
}
```

## 📋 **Best Practices Summary**

### **Do's:**
- ✅ **Implement client-side rate limiting** before API calls
- ✅ **Cache responses** to reduce API calls
- ✅ **Use exponential backoff** for retries
- ✅ **Honor Retry-After headers** from API
- ✅ **Set conservative limits** (30 requests/minute)
- ✅ **Monitor API quotas** and usage
- ✅ **Use proper User-Agent** headers
- ✅ **Handle all HTTP status codes** gracefully

### **Don'ts:**
- ❌ **Make rapid successive requests** without delays
- ❌ **Ignore 429 responses** and continue requesting
- ❌ **Use fixed delays** instead of Retry-After headers
- ❌ **Cache sensitive data** without expiration
- ❌ **Exceed API quotas** regularly
- ❌ **Handle errors silently** without logging

## 🔄 **Request Flow**

### **Optimal Request Pattern**
```
1. Check Cache → Return cached data if available
2. Check Rate Limit → Wait if needed
3. Make API Request → With proper headers
4. Handle Response → Cache success, retry errors
5. Return Result → With proper error messages
```

### **Example Request Timeline**
```
Request 1: API Call (Cache miss)
Request 2: Cache Hit (Immediate)
Request 3: Cache Hit (Immediate)
Request 4: API Call (Cache expired)
Request 5: Rate Limited (Wait 45 seconds)
Request 6: API Call (After wait period)
```

## 🚨 **Error Prevention**

### **429 Prevention Strategies**
1. **Pre-request rate limiting check**
2. **Intelligent caching** based on search patterns
3. **Request queuing** for high-volume scenarios
4. **Graceful degradation** to cached data
5. **User notification** of rate limiting

### **Monitoring Metrics**
- **Cache hit ratio**: Target > 60%
- **Rate limit events**: Should be < 5% of requests
- **API response time**: Monitor for performance
- **Error rates**: Keep < 1% for non-rate-limit errors

## 🌐 **Production Deployment**

### **Environment-Specific Settings**
```python
if environment == 'production':
    rate_limiter = RateLimiter(max_requests_per_minute=50)
    cache_manager = CacheManager(cache_duration_minutes=2)
elif environment == 'development':
    rate_limiter = RateLimiter(max_requests_per_minute=100)
    cache_manager = CacheManager(cache_duration_minutes=1)
```

### **Load Balancing**
- **Multiple API keys** for high-volume applications
- **Round-robin requests** across keys
- **Per-key rate limiting** to distribute load

## 📈 **Scaling Considerations**

### **High Volume Strategies**
1. **Implement request queuing**
2. **Use multiple API keys**
3. **Increase cache duration** for static data
4. **Implement background refresh**
5. **Consider enterprise API plans**

### **Performance Monitoring**
```python
# Track these metrics
- cache_hit_rate = cache_hits / total_requests
- rate_limit_hits = rate_limit_errors / total_requests  
- api_response_time = average(response_times)
- error_rate = errors / total_requests
```

---

## 🎯 **Key Takeaways**

1. **Rate limiting is essential** to prevent 429 errors
2. **Caching dramatically reduces** API calls
3. **Retry logic with backoff** handles temporary issues
4. **Monitoring helps optimize** performance
5. **Conservative settings** ensure reliability

**Following these practices will result in:**
- ✅ **Zero 429 errors** under normal load
- ✅ **60%+ cache hit rate** for common queries
- ✅ **Sub-second response times** for cached requests
- ✅ **Graceful handling** of API limits
- ✅ **Reliable service** even during API issues
