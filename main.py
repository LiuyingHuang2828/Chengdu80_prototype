from news_fetcher.fetch_news import NewsFetcher
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the company name you want to search for
company_name = 'Tesla'  # Replace with the desired company name

# Instantiate the NewsFetcher with the company name
fetcher = NewsFetcher(company_name)

# Fetch and save news articles for all defined risk types
fetcher.fetch_all_risks(output_dir='news_data_fetched')
