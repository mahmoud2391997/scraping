# How to Use This App

This project is a **scraping API** that exposes HTTP endpoints for:
- **Vinted** (default `/`)
- **eBay** (`/ebay` and `/ebay/api`)
- **Sold items** (`/ebay/sold`, `/vinted/sold`)
- **Vestiaire Collective** (`/vestiaire`)

It also includes an optional **CSV viewer** web page (`app.py`) for `scraped_data.csv`.

---

## 1) Requirements

- Python **3.x**
- pip

Install dependencies:

```bash
cd /Users/mahmoudelsayed/Downloads/templates
python3 -m pip install -r requirements.txt
```

---

## 2) (Optional) Configure eBay API credentials

Some eBay functionality can use the official eBay API if credentials are available.

Create a file named `.env` in the project root (`/Users/mahmoudelsayed/Downloads/templates/.env`) with:

```bash
export EBAY_APP_ID="your-ebay-app-id"
export EBAY_CERT_ID="your-ebay-cert-id"
```

Notes:
- The server tries to load `../.env` from `api/index.py`, so placing `.env` in the **project root** is the expected setup.
- If credentials are missing, the server will often fall back to **web scraping** for `/ebay` (when possible).

---

## 3) Run the API server (recommended)

### Option A (recommended): run from project root

This avoids path issues and keeps the HTML UI working:

```bash
cd /Users/mahmoudelsayed/Downloads/templates
python3 api/server.py 8099
```

You should see a message like:
- `Starting server on http://localhost:8099`

### Option B: legacy runner used by README

```bash
cd /Users/mahmoudelsayed/Downloads/templates
python3 test_server.py
```

This runs on `http://localhost:8099`.

---

## 4) Use it in the browser (UI)

Open:
- `http://localhost:8099/`

If you open `/` **without query parameters**, the server serves an HTML page (if available).

---

## 5) Use it as an API (JSON)

### Endpoints

- **Vinted search (JSON when query string is present)**: `GET /`
- **eBay search (API-first, then scraping fallback)**: `GET /ebay`
- **eBay “API endpoint” (production-oriented, falls back to scraping)**: `GET /ebay/api`
- **eBay sold items (real-only; no sample fallback)**: `GET /ebay/sold`
- **Vinted sold items (real-only; no sample fallback)**: `GET /vinted/sold`
- **Vestiaire search**: `GET /vestiaire`

### Common query parameters

Most endpoints accept:
- `search` (string)
- `page` (int, default `1`)
- `items_per_page` (int, default varies; max typically `50`)
- `min_price` (number, optional)
- `max_price` (number, optional)
- `country` (string, default varies)

### Example calls (curl)

Vinted:

```bash
curl "http://localhost:8099/?search=shoes&country=uk&items_per_page=10"
```

eBay:

```bash
curl "http://localhost:8099/ebay?search=iphone&country=us&items_per_page=5"
```

eBay with price range:

```bash
curl "http://localhost:8099/ebay?search=macbook&country=uk&min_price=500&max_price=1500&items_per_page=10"
```

Sold items:

```bash
curl "http://localhost:8099/ebay/sold?search=airpods&country=us&items_per_page=10"
curl "http://localhost:8099/vinted/sold?search=nike&country=uk&items_per_page=10"
```

Vestiaire:

```bash
curl "http://localhost:8099/vestiaire?search=handbag&country=uk&items_per_page=10"
```

---

## 6) Response shape (what you get back)

Successful responses are JSON shaped like:
- `success` (boolean)
- `data` (array of products)
- `count` (number)
- `pagination` (object)
- `error` (string or null)

For full field definitions and examples, see:
- `API_DOCUMENTATION.md`
- `FRONTEND_README.md`

---

## 7) Optional: view `scraped_data.csv` in a browser

There is a separate Flask app in `app.py` that renders `scraped_data.csv` as an HTML table:

```bash
cd /Users/mahmoudelsayed/Downloads/templates
python3 app.py
```

Then open:
- `http://localhost:5001/`

---

## 8) Production / deployment

If you deploy (ex: Vercel), you’ll typically need to configure environment variables there:
- `EBAY_APP_ID`
- `EBAY_CERT_ID`

See:
- `PRODUCTION_DEPLOYMENT.md`

