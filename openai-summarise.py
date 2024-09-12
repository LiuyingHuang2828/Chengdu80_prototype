import os
import openai  # Assuming you are using OpenAI API for summarization
from dotenv import load_dotenv
load_dotenv()


# Setup OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
 

def summarize_and_score_content(text, risk_type):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes risk-related news and provides a risk score based on the severity of the risks."},
        {"role": "user", "content": f"""
        Please provide a detailed summary for the following {risk_type} risk news articles. 
        The summary must follow this structure:
        
        1. **Summary**: Provide a detailed summary of the major incidents or events related to the {risk_type} risk, covering all key points. 
        2. **Impact**: Explain the potential impact of these risks, including financial, legal, reputational, and operational consequences.
        3. **Risk Score**: Assign a risk score from 1 (low risk) to 10 (high risk) based on the severity of the risks. Justify the score given.
        
        Use the following format:
        Summary: [Detailed summary here]
        Impact: [Detailed impact explanation here]
        Risk Score: [Risk score out of 10]
        
        Here are the {risk_type} risk news articles:
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
    
    return summary




def relate_risks(summaries, company_name):
    # Combine all summarized risks into one text
    combined_text = "\n\n".join(summaries)
    
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
        \n\n{combined_text}
        """}
    ]
    
    # Generate the response from the model
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=messages,
        max_tokens=350  # Increased token limit for a more detailed response
    )
    
    # Extract and return the response content
    return response.choices[0].message.content


def process_company_risks(company_name, folder_path):
    risk_files = {
        'legal': f"news_legal_risk_{company_name}.txt",
        'loan': f"news_loan_risk_{company_name}.txt",
        'operations': f"news_operation_risk_{company_name}.txt",
        'other': f"news_other_risks_{company_name}.txt"
    }

    summaries = {}
    
    for risk_type, filename in risk_files.items():
        file_path = os.path.join(folder_path, filename)
        
        # Check if file exists and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as f:
                content = f.read().strip()
                
                # Check if content is not empty after reading the file
                if content:
                    summary = summarize_and_score_content(content, risk_type)
                    summaries[risk_type] = summary
                    print(f"Summary for {risk_type} risk:\n{summary}\n")
                else:
                    print(f"Warning: {filename} is empty.")
        else:
            print(f"Warning: {filename} not found or is empty.")
    
    # Summarize how risks are related if any summaries are generated
    if summaries:
        related_summary = relate_risks(list(summaries.values()), company_name)
        print(f"\nHow the risks are related for {company_name}:\n{related_summary}")
    else:
        print(f"No risk data available for {company_name}")




# Set your company and folder details
company_name = "Tesla"  # Change this based on your input
folder_path = "news_data_fetched/"  # Change this to your actual folder path

# Process the risks for the company
process_company_risks(company_name, folder_path)
