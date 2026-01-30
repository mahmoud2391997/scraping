from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Assuming the scraped data is in a CSV file named 'scraped_data.csv'
    try:
        data = pd.read_csv('scraped_data.csv')
        return render_template('index.html', tables=[data.to_html(classes='data')], titles=data.columns.values)
    except FileNotFoundError:
        return "Scraped data not found. Please run the scraper first."

if __name__ == '__main__':
    app.run(debug=True, port=5001)
