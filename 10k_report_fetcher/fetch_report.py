from yf_utils import *

# Load environment variables from .env file
# load_dotenv()

class ReportFetcher:
    def __init__(self, company_ticker):
        """
        Initializes the ReportFetcher with a company code.
        """
        self.company_ticker = company_ticker

    def fetch_report(self, item_title, item_suc_title):
        """
        Fetches full report item.
        """
        url = get_10k_url(self.company_ticker)
        report = get_item_content_url(url, item_title, item_suc_title)
        return report

    def fetch_and_save_report(self, item_title, item_suc_title, output_dir='report_data_fetched'):
        """
        Fetches full report item, and saves them as plaintext files.
        """
        report = self.fetch_report(item_title, item_suc_title)

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
            
        # Define the filename based on the company ticker and item title
        file_name = f"{self.company_ticker}_{item_title.replace(' ', '_')}.txt"
        file_path = os.path.join(output_dir, file_name)
        
        # Save the report content to a text file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(report)

        print(f"Report saved to {file_path}")


    def fetch_and_summarise_cv(self, item_title = "Risk Factors", item_suc_title = "Unresolved Staff Comments"):
        """
        Fetches full report item, and generate Corporate Vulnerability summary for each risk type using DeepSeek-Chat
        """
        report = self.fetch_report(item_title, item_suc_title)
        return summarise_cv_by_risk_type(extract_cv_by_chunks(report))

        