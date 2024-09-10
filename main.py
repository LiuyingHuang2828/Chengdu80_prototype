from news_fetcher.fetch_news import NewsFetcher

# Replace 'Tesla' with the desired company name
company_name = 'Tesla'

# Instantiate the NewsFetcher
fetcher = NewsFetcher(company_name)

# Fetch and save news articles for all defined risk types
fetcher.fetch_all_risks()
