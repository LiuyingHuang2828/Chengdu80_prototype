from flask import Flask, render_template
import yfinance as yf
import pandas as pd
import json
from datetime import datetime, timedelta

app = Flask(__name__)

def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date']).astype(int) // 10**6  # Convert to milliseconds
    return [[int(date), close] for date, close in zip(data['Date'], data['Close'])]

@app.route('/')
def chart():
    ticker = 'AAPL'
    end_date = datetime.now().strftime('%Y-%m-%d')
    
    # 1 week ago
    start_1w = (datetime.now() - timedelta(weeks=1)).strftime('%Y-%m-%d')
    data_1w = get_stock_data(ticker, start_1w, end_date)
    
    # 1 month ago
    start_1m = (datetime.now() - timedelta(weeks=4)).strftime('%Y-%m-%d')
    data_1m = get_stock_data(ticker, start_1m, end_date)
    
    # 3 months ago
    start_3m = (datetime.now() - timedelta(weeks=12)).strftime('%Y-%m-%d')
    data_3m = get_stock_data(ticker, start_3m, end_date)
    
    # Pass the data for different time periods to the HTML template
    return render_template('chart.html', 
                           data_1w=json.dumps(data_1w), 
                           data_1m=json.dumps(data_1m), 
                           data_3m=json.dumps(data_3m))

if __name__ == '__main__':
    app.run(debug=True)
