import requests
import yfinance as yf
import pandas as pd
from lxml import etree
import requests
import os
import re
import transformers
from openai import OpenAI
from dotenv import load_dotenv
import dask.bag as db
from langchain_openai import OpenAI
from langchain.text_splitter import NLTKTextSplitter

load_dotenv()
api_key = os.getenv('DEEPSEEK_API_KEY')  # Deepseek API key

def search_ticker_exact(dataframe, search_term):
    mask = (
        (dataframe['name'].str.lower() == search_term.lower()) |
        (dataframe['short_name'].str.lower() == search_term.lower()) |
        (dataframe['tiny_name'].str.lower() == search_term.lower())
    )
    return dataframe[mask]["ticker"].values[0] if not dataframe[mask].empty else ""

def get_10k_url(ticker):
    company_data =  yf.Ticker(ticker)
    api_response_10k = list(filter(lambda record: record['type'] == "10-K",company_data.sec_filings)) # 10-K
    return max(api_response_10k, key=lambda x: x['date'])['exhibits']['10-K']

def get_item_content_url(url, item_title, item_suc_title):
    # returns link to section by title
    def get_sublink_by_title(title, tree):
        spans = tree.xpath('//span[a]')
        for span in spans:
            links = span.xpath('.//a')
            for link in links:
                href = link.get('href')
                link_text = link.xpath('string()').strip()
                if link_text == title: return href
                else: continue
        return f"No match found for {title}."
    
    # concate 10K document with only Section of Interest
    def get_para_btw_divs(tree, start_div_id, end_div_id):   
        spans_between = tree.xpath(f'//*[@id="{start_div_id}"]/following::span[following::div[@id="{end_div_id}"]]')
        return spans_between
    
    # clean spans and output text(string)
    def spans_to_text(spans):
        to_remove = ['\xa0\xa0\xa0\xa0', None, '\r', 'Table of Contents']
        lst_spans = [span.text for span in spans if span.text not in to_remove]
        str_spans = "\n".join(lst_spans)
        para_cleaned = str_spans.replace("Class\xa0B", " ").replace("Class\xa0A", " ").replace("•\n", " ").replace("\xa0", " ").replace("  ", " ")
        para_cleaned = re.sub(r"\n\d{1,2}\n", "\n", para_cleaned)
        return para_cleaned

    response = requests.get(url)
    tree = etree.fromstring(response.content, etree.HTMLParser())

    start_div_id = get_sublink_by_title(item_title, tree)[1:]
    end_div_id = get_sublink_by_title(item_suc_title, tree)[1:]

    spans = get_para_btw_divs(tree, start_div_id, end_div_id)

    return spans_to_text(spans)



def chunk_text_nltk(text):
    text_splitter = NLTKTextSplitter()
    docs = text_splitter.split_text(text)
    return docs

def query_deepseek(message, api_key):
    base_url="https://api.deepseek.com"
    client = OpenAI(api_key=api_key, base_url=base_url)

    # results = []
    response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant expertise in corporate risk analysis."},
        {"role": "user", "content": message},
    ],
    stream=False
    )
    result = response.choices[0].message.content
    # print(result)
    return result

def deepseek_by_chunks(chunks):
    b = db.from_sequence(chunks, npartitions=len(chunks))  # Adjust npartitions depending on your data size and available cores
    processed_bag = b.map(lambda x: query_deepseek(x, api_key))
    processed_sentences = processed_bag.compute() 
    print(f"reduced text from {len(''.join(chunks))} to {len(''.join(processed_sentences))} characters")
    return processed_sentences

# cv is short for corporate vulnerabilities
# takes about 1-2 minutes to run
def extract_cv_by_chunks(text):
    print("Corporate Vulnerabilities Extraction in Progress ...")
    sentences = chunk_text_nltk(text)
    prompt = "You are given a portion of the corporate's 10-K Anual Report of Risk Factors section. Please extract the key corporate vulnerabilities described which could be useful for future risk analysis concisely and accurately. Only output the extraction result. Here is the report segment: \n"
    messages = [prompt + sentence for sentence in sentences]
    return "".join(deepseek_by_chunks(messages))

# takes about 1-2 minutes to run
def summarise_cv_by_risk_type(processed_text):
    print("Summarising Corporate Vulnerabilities by Risk Type ...")
    risk_types = ["Operational Risk", "Legal Risk", "Loan Risk", "Other Risk besides operational, legal, and loan"]
    prompts = [f"You are given a corporate vulnerabilities description. Please summarise the most relevant vulnerabilities for future risk analysis on **{risk_type}**. Only output the extraction result. Here is the report: \n" for risk_type in risk_types]
    messages = [prompt + processed_text for prompt in prompts]
    # processed_messages = deepseek_by_chunks(messages)
    processed_messages = list(map(lambda x: query_deepseek(x, api_key), messages))

    result_dict = {}
    for i, risk_type in enumerate(risk_types):
        result_dict[risk_type] = processed_messages[i]
    print("Summarising Corporate Vulnerabilities by Risk Type Completed")
    return result_dict