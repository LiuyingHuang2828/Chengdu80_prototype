from fetch_report import ReportFetcher
from yf_utils import *

# Change the working directory to the location of this script
# script_directory = os.path.dirname(os.path.abspath(__file__))
# os.chdir(script_directory)

# Load the company codes reference data
code_ref = pd.read_csv('company_code.csv')

# Define the company name you want to search for
company_name = 'tesla'  # Replace with the desired company name
company_ticker = search_ticker_exact(code_ref, company_name)
if company_ticker == "":
    print(f"Company '{company_name}' not found in the company code reference data.")
    exit()

# Instantiate the ReportFetcher with the company name
fetcher = ReportFetcher(company_ticker)

# Fetch and save news articles for
fetcher.fetch_and_save_report("Risk Factors", "Unresolved Staff Comments", output_dir='../report_data_fetched')
