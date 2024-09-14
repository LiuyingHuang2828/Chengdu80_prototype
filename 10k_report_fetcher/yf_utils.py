import requests
import yfinance as yf
import pandas as pd
from lxml import etree
import requests
import os
import re

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


