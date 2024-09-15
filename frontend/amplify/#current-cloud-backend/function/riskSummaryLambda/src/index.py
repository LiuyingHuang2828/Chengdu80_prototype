import json
import os
import openai  
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('DYNAMODB_TABLE_NAME', 'chengdu80NewsDynamo-dev')  # Replace with your actual table name
table = dynamodb.Table(table_name)
table_summary = dynamodb.Table('riskSummaryDynamo-dev')

def summarize_and_score_content(company_name, text, risk_category):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes risk-related news and provides a risk score based on the severity of the risks."},
        {"role": "user", "content": f"""
        Please provide a detailed summary for the following {risk_category} risk news articles, do note that some articles may not be related to the risk category: 
        The summary must follow this structure:
        
        1. **Summary**: Provide a detailed summary of the major incidents or events related to the {risk_category} risk, covering all key points. 
        2. **Impact**: Explain the potential impact of these risks, including financial, legal, reputational, and operational consequences.
        3. **Risk Score**: Assign a risk score from 1 (low risk) to 10 (high risk) based on the severity of the risks. Justify the score given.
        
        Use the following format, with h4 headers in markdown in react-markdown format:
        Summary: [Detailed summary here]
        Impact: [Detailed impact explanation here]
        Risk Score: [Risk score out of 10]/10
        
        Here are the {risk_category} risk news articles:
        \n\n{text}
        
        Ensure the summary is complete and matches the structure, without omitting any key points.
        
        """}
    ]
    
    # Increase max_tokens to ensure the model has enough space to generate a complete response
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=messages,
        max_tokens=500  # Increase token limit to allow for a detailed and complete summary
    )
    
    # Extract the summary from the response
    summary = response.choices[0].message.content
    
    item = {
        'companyName': company_name,
        'riskCategory': risk_category,
        'summary': summary
    }
    
    # Store the summary in DynamoDB
    try:
        table_summary.put_item(Item=item)
        print(f"Stored summary for {company_name} with risk category '{risk_category}'.")
    except ClientError as e:
        print(f"Error storing summary in DynamoDB: {e.response['Error']['Message']}")
        
    return



def get_news_by_company(company_name, sort_key_value=None):
    """
    Retrieves news articles from DynamoDB for the specified company,
    optionally filtering by the sort key value.
    
    :param company_name: The name of the company.
    :param sort_key_value: The sort key value to filter articles by 
                           (e.g., 'legal', 'loan', 'operational', 'others').
    :return: List of news articles for the specified company and sort key value.
    """
    try:
        # Check if sort key value is provided
        if not sort_key_value:
            print("Error: Sort key value must be provided.")
            return []
        
        # Build the key condition expression with both partition and sort key
        key_condition = (
            boto3.dynamodb.conditions.Key('companyName').eq(company_name) &
            boto3.dynamodb.conditions.Key('riskCategory').eq(sort_key_value)
        )
        
        # Perform the query
        response = table.query(
            KeyConditionExpression=key_condition
        )
        
        items = response.get('Items', [])
        print(f"Retrieved {len(items)} articles for {company_name} with risk type '{sort_key_value}'.")
        
        # Extract only the article content from the items
        if len(items) == 0:
            return f'No articles found for the specified {company_name} and risk type {sort_key_value}'
        else:
            articles = items[0].get('article', [])
            texts = ""
            for article in articles:
                title = article.get('title', '')
                description = article.get('description', '')
                author = article.get('author', '')
                source = article.get('source', {
                    'name': 'Not available'
                }).get('name', 'Not available')
                
                # Combine the title, description, author, and source
                overall_text = f"{title}\n{description}\nAuthor: {author}\nSource: {source}\n\n"
                texts += overall_text
            return texts
    
    except ClientError as e:
        print(f"Error retrieving articles from DynamoDB: {e.response['Error']['Message']}")
        return []


def get_summary_by_company(company_name):
    """
    Retrieves the summary from DynamoDB for the specified company,
    optionally filtering by the sort key value.
    
    :param company_name: The name of the company.
    :return: The summary for the specified company and sort key value.
    """
    try:
        response = table_summary.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('companyName').eq(company_name)
        )
        items = response.get('Items', [])
        print(f"Retrieved {len(items)} articles for {company_name}.")
        return items
    except ClientError as e:
        print(f"Error retrieving articles from DynamoDB: {e.response['Error']['Message']}")
        return []


def handler(event, context):
    print('received event:')
    print(event)
  
    if event['httpMethod'] == 'POST':
        # Extract the company name from the request body
        body = json.loads(event['body'])
        company_name = body.get('company_name')
        risk_category = body.get('risk_category')
        text = get_news_by_company(company_name, sort_key_value=risk_category)
        
        if company_name and risk_category and text:
            # Summarize and score the content
            summarize_and_score_content(company_name, text, risk_category)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps('Summary generated and stored successfully.')
            }
        else:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps('Missing required parameters in the request body.')
            }
    elif event['httpMethod'] == 'GET':
        # Extract company_name from path parameters
        if event.get('pathParameters') and 'proxy' in event['pathParameters']:
            company_name = event['pathParameters']['proxy']
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Missing company_name in request path parameters.')
            }
        
        # Fetch news for the given company
        try:
            articles = get_summary_by_company(company_name)  # Fetch news from DynamoDB
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
  
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Hello from your new Amplify Python lambda!')
    }