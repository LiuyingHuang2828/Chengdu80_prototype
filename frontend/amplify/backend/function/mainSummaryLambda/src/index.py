import json
import os
import openai  
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

dynamodb = boto3.resource('dynamodb')
table_summary = dynamodb.Table('riskSummaryDynamo-dev')
table_main_summary = dynamodb.Table('mainSummaryDynamo-dev')

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
        
        texts = ""
        
        
        if len(items) == 0:
            return f'No articles found for the specified {company_name}'
        
        for item in items:
            companyName = item.get('companyName', '')
            riskCategory = item.get('riskCategory', '')
            summary = item.get('summary', '')
            
            overall_text = f"Company Name: {companyName}\nRisk Category: {riskCategory}\nSummary: {summary}\n\n"
            
            texts += overall_text
    
        return texts
    except ClientError as e:
        print(f"Error retrieving articles from DynamoDB: {e.response['Error']['Message']}")
        return []


def get_main_summary_by_company(company_name):
    """
    Retrieves the main summary from DynamoDB for the specified company,
    optionally filtering by the sort key value.
    
    :param company_name: The name of the company.
    :return: The main summary for the specified company and sort key value.
    """
    try:
        response = table_main_summary.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('companyName').eq(company_name)
        )
        items = response.get('Items', [])
        print(f"Retrieved {len(items)} articles for {company_name}.")
        
        if len(items) == 0:
            return f'No articles found for the specified {company_name}'
        
        return items[0].get('summary', '')
    except ClientError as e:
        print(f"Error retrieving articles from DynamoDB: {e.response['Error']['Message']}")
        return []



def relate_risks(summaries, company_name):

    # Create a prompt asking for a structured summary, overall risk score, and risk assessment
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes and relates various types of risks for a company."},
        {"role": "user", "content": f"""
        Summarize how the following risks (legal, loan, operations, and other) for {company_name} are related. Please follow the structure below:
        1. **Risk Relationships**: Describe how the various risks (legal, loan, operations, and other) are interconnected or affect each other.
        2. **Overall Risk Summary**: Provide a high-level summary of the company's overall risk profile.
        3. **Overall Risk Score**: Assign an overall risk score from 1 (low risk) to 10 (high risk). Justify the risk score given.
        4. **Conclusion**: Conclude by explaining whether the company is in a risky situation or relatively stable.
        Make sure to provide a complete and structured summary without omitting any important information.
        Here are the summarized risks for {company_name}:
        \n\n{summaries}
        """}
    ]
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=512  # Increase token limit to allow for a detailed and complete summary
    )
    # Extract the summary from the response
    summary = response.choices[0].message.content
    
    try:
        item = {
            'companyName': company_name,
            'summary': summary
        }
        
        table_main_summary.put_item(Item=item)
    except ClientError as e:
        print(f"Error storing summary in DynamoDB: {e.response['Error']['Message']}")
    
    return



def handler(event, context):
    print('received event:')
    print(event)
    
    if event['httpMethod'] == 'POST':
            # Extract the company name from the request body
            body = json.loads(event['body'])
            company_name = body.get('company_name')
            text = get_summary_by_company(company_name)

            if company_name and text:
                # Summarize and score the content
                relate_risks(text, company_name)
                
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
            articles = get_main_summary_by_company(company_name)  # Fetch news from DynamoDB
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