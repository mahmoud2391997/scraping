from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    try:
        data = pd.read_csv('scraped_data.csv')
        return data.to_html()
    except FileNotFoundError:
        return "Scraping API is running! No data file found. Use the API endpoints to scrape data."

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "service": "scraping-api"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
