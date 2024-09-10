import requests
import os

# Define your API key and base URL for NewsAPI
# Get API ley from environment variable
api_key = os.getenv('NEWS_API_KEY')
url = 'https://newsapi.org/v2/everything'

# Define the company name you want to search for
company_name = 'Tesla'  # Replace with the desired company name

# Define the keywords for different types of corporate risks, including the company name
risk_types = {
    'operation risk': f'{company_name} operational risk OR {company_name} business disruption',
    'legal risk': f'{company_name} legal risk OR {company_name} lawsuits OR {company_name} compliance',
    'loan risk': f'{company_name} loan risk OR {company_name} credit risk OR {company_name} default',
    'other risks': f'{company_name} corporate risk OR {company_name} business risk OR {company_name} financial risk'
}

# Function to fetch and save news articles for each risk type related to the company
def fetch_news(risk, query):
    # Set up parameters for the API request
    params = {
        'q': query,
        'language': 'en',
        'sortBy': 'relevancy',
        'apiKey': api_key
    }
    
    # Make the request to the API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        articles = data['articles']
        
        # Save articles to a text file
        with open(f'news_data_fetched/news_{risk.replace(" ", "_")}_{company_name}.txt', 'w') as file:
            for article in articles:
                file.write(f"Title: {article['title']}\n")
                file.write(f"Description: {article['description']}\n")
                file.write(f"URL: {article['url']}\n\n")
    else:
        print(f"Failed to retrieve news for {risk} of {company_name}: {response.status_code} {response.text}")

# Fetch news for each risk type related to the company
for risk, query in risk_types.items():
    fetch_news(risk, query)
    print(f"News for {risk} of {company_name} fetched and saved.")
