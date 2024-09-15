import json
import yfinance as yf
import requests

def get_ticker(company_name):
    api_url = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=api_url, params=params, headers={'User-Agent': user_agent})
    data = res.json()

    company_code = data['quotes'][0]['symbol']
    return company_code

def get_stock_price(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    history = stock.history(period='1mo')
    if history.empty:
        return None
    return history['Close'].values.tolist()

def handler(event, context):
    print('received event:')
    print(event)
    
    # Define CORS headers
    cors_headers = {
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,GET'
    }
    
    if event['httpMethod'] == 'OPTIONS':
        # Handle CORS preflight request
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps('CORS preflight response')
        }
    
    if event['httpMethod'] == 'GET': 
        if event.get('pathParameters') and 'proxy' in event['pathParameters']:
            company_name = event['pathParameters']['proxy']
        else:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps('Missing company_name in request path parameters.')
            }
        
        # Fetch ticker symbol and stock prices
        try:
            ticker_symbol = get_ticker(company_name)
            if not ticker_symbol:
                return {
                    'statusCode': 404,
                    'headers': cors_headers,
                    'body': json.dumps(f'Ticker symbol not found for company {company_name}.')
                }
            stock_prices = get_stock_price(ticker_symbol)
            if stock_prices is None:
                return {
                    'statusCode': 404,
                    'headers': cors_headers,
                    'body': json.dumps(f'No stock data found for ticker symbol {ticker_symbol}.')
                }
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({
                    'company_name': company_name,
                    'ticker_symbol': ticker_symbol,
                    'stock_prices': stock_prices
                })
            }
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return {
                'statusCode': 500,
                'headers': cors_headers,
                'body': json.dumps('Internal server error.')
            }
    else:
        return {
            'statusCode': 405,
            'headers': cors_headers,
            'body': json.dumps('Method not allowed.')
        }
