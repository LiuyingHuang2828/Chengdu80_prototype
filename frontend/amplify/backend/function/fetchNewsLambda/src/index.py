import json
import requests
import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

# Load environment variables from .env file
load_dotenv()

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('DYNAMODB_TABLE_NAME', 'chengdu80NewsDynamo-dev')  # Replace with your actual table name
table = dynamodb.Table(table_name)

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
            'loan risk': f'{self.company_name} loan OR {self.company_name} credit OR {self.company_name} debt OR {self.company_name} repayment OR {self.company_name} borrowing OR {self.company_name} financial issues OR {self.company_name} creditworthiness OR {self.company_name} lending',
            'other risks': f'{self.company_name} corporate risk OR {self.company_name} business risk OR {self.company_name} financial risk'
        }

    def fetch_and_store_news(self, risk, query):
        """
        Fetches news articles related to the specified risk type and query, and stores them in DynamoDB.
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
            
            print(f"Fetched {len(articles)} articles for {risk} of {self.company_name}")


            item = {
                'companyName': self.company_name,             # Partition Key
                'riskCategory': risk,                    # Sort Key
                'article': articles
            }
            try:
                table.put_item(Item=item)
            except ClientError as e:
                print(f"Error saving article to DynamoDB: {e.response['Error']['Message']}")
        else:
            print(f"Failed to retrieve news for {risk} of {self.company_name}: {response.status_code} {response.text}")

    def fetch_all_risks(self):
        """
        Fetches and stores news articles for all predefined risk types for the specified company.
        """
        for risk, query in self.risk_types.items():
            self.fetch_and_store_news(risk, query)
            print(f"News for {risk} of {self.company_name} fetched and stored in DynamoDB.")
            
    def get_news_by_company(self):
        """
        Retrieves news articles from DynamoDB for the specified company.
        """
        try:
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('companyName').eq(self.company_name)
            )
            items = response.get('Items', [])
            print(f"Retrieved {len(items)} articles for {self.company_name}.")
            return items
        except ClientError as e:
            print(f"Error retrieving articles from DynamoDB: {e.response['Error']['Message']}")
            return []




def handler(event, context):
    print('Received event:')
    print(json.dumps(event, indent=2))  # Print the full event for debugging

    company_name = None

    # Extract company_name from path parameters
    if event['httpMethod'] == 'GET':
        # Extract company_name from 'proxy' path parameter
        if event.get('pathParameters') and 'proxy' in event['pathParameters']:
            company_name = event['pathParameters']['proxy']
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Missing company_name in request path parameters.')
            }
        
        # Fetch news for the given company
        try:
            news_fetcher = NewsFetcher(company_name)
            articles = news_fetcher.get_news_by_company()  # Fetch news from DynamoDB
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps(articles)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps(str(e))
            }

    # Handle POST requests or other methods
    elif event['httpMethod'] == 'POST':
        # Parse the request body
        try:
            body = json.loads(event.get('body', '{}'))
            company_name = body.get('company_name', 'Default Company')  # Fetch company name from the request body
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps('Invalid JSON format in request body.')
            }

        # Example usage
        try:
            news_fetcher = NewsFetcher(company_name)
            news_fetcher.fetch_all_risks()  # Fetch all risk news and store in DynamoDB
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps(str(e))
            }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('News articles fetched and stored successfully!')
        }

    # Return method not allowed if HTTP method is not supported
    return {
        'statusCode': 405,
        'body': json.dumps('Method not allowed')
    }