import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class NewsFetcher:
    def __init__(self, company_name, api_key=None):
        """
        Initializes the NewsFetcher with a company name and optional API key.
        If the API key is not provided, it will look for it in the environment variables.
        """
        self.company_name = company_name
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        if not self.api_key:
            raise ValueError("API key is missing. Please set it in the environment or pass it explicitly.")
        self.url = 'https://newsapi.org/v2/everything'
        self.risk_types = {
            'operation risk': f'{self.company_name} operational risk OR {self.company_name} business disruption',
            'legal risk': f'{self.company_name} legal risk OR {self.company_name} lawsuits OR {self.company_name} compliance',
            'loan risk': f'{self.company_name} loan risk OR {self.company_name} credit risk OR {self.company_name} default',
            'other risks': f'{self.company_name} corporate risk OR {self.company_name} business risk OR {self.company_name} financial risk'
        }

    def fetch_and_save_news(self, risk, query, output_dir='news_data_fetched'):
        """
        Fetches news articles related to the specified risk type and query, and saves them as plaintext files.
        """
        # Set up parameters for the API request
        params = {
            'q': query,
            'language': 'en',
            'sortBy': 'relevancy',
            'apiKey': self.api_key
        }

        # Make the request to the API
        response = requests.get(self.url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            articles = data['articles']

            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)
            
            # Save articles to a text file
            file_path = os.path.join(output_dir, f'news_{risk.replace(" ", "_")}_{self.company_name}.txt')
            with open(file_path, 'w') as file:
                for article in articles:
                    file.write(f"Title: {article['title']}\n")
                    file.write(f"Description: {article['description']}\n")
                    file.write(f"URL: {article['url']}\n\n")
        else:
            print(f"Failed to retrieve news for {risk} of {self.company_name}: {response.status_code} {response.text}")

    def fetch_all_risks(self, output_dir='news'):
        """
        Fetches and saves news articles for all predefined risk types for the specified company.
        """
        for risk, query in self.risk_types.items():
            self.fetch_and_save_news(risk, query, output_dir=output_dir)
            print(f"News for {risk} of {self.company_name} fetched and saved.")
