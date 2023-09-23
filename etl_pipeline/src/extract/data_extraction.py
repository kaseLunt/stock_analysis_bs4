# Import required libraries and packages
import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import os

# Configure logging settings for debugging and monitoring purposes
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# Define constants: URL format for Google Finance and HTTP headers for web requests
GOOGLE_FINANCE_URL = 'https://www.google.com/finance/quote/{symbol}:{exchange}?hl=en'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Determine the directory path where the script is located and specify the CSV save location
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join(dir_path, '../../data/raw/nasdaq_stocks.csv')

# Function to perform HTTP requests and handle exceptions
def make_request(url):
    """
    Make an HTTP request to a given URL and return the content.
    Log any HTTP errors encountered during the request.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.HTTPError as e:
        logging.error(f"Failed to retrieve {url}, status code: {response.status_code}, error: {e}")
        return None

# Function to fetch stock prices from Google Finance for multiple stock exchanges
def fetch_stock_prices(symbol, exchanges=['NASDAQ', 'NYSE']):
    """
    Fetch the stock price of a given symbol from one of the specified exchanges.
    """
    for exchange in exchanges:
        url = GOOGLE_FINANCE_URL.format(symbol=symbol, exchange=exchange)
        content = make_request(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            stock_price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})
            if stock_price_element:
                return stock_price_element.text
    return None

# Function to fetch financial metrics from Google Finance for multiple stock exchanges
def fetch_financial_metrics(symbol, exchanges=['NASDAQ', 'NYSE']):
    """
    Fetch the financial metrics of a given symbol from one of the specified exchanges.
    """
    for exchange in exchanges:
        url = GOOGLE_FINANCE_URL.format(symbol=symbol, exchange=exchange)
        content = make_request(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            metrics_table = soup.find('table', {'class': 'slpEwd'})
            if metrics_table:
                financial_metrics = {}
                rows = metrics_table.find_all('tr', {'class': 'roXhBd'})
                for row in rows[1:]:
                    metric_name = row.find('td', {'class': 'J9Jhg'}).find('div').text.strip()
                    metric_value = row.find('td', {'class': 'QXDnM'}).text.strip()
                    financial_metrics[metric_name] = metric_value
                return financial_metrics
    return None

# Main function to fetch all data for stocks listed on NASDAQ and NYSE
def fetch_all_data_for_stocks():
    """
    Fetch and store data for the top 100 (by market capitalization) stocks listed on NASDAQ and NYSE by market capitalization.
    """
    # Read the CSV file containing stock symbols and sort by market cap
    df = pd.read_csv(csv_file_path)
    df['Market Cap'] = df['Market Cap'].apply(pd.to_numeric, errors='coerce')
    df = df.nlargest(100, 'Market Cap')

    # Initialize list to store stock data
    stock_data = []

    # Iterate through each stock symbol to fetch data
    for index, row in df.iterrows():
        symbol = row['Symbol']
        name = row['Name']
        logging.info(f"Fetching data for {name} ({symbol})")

        # Fetch stock price and financial metrics
        stock_price = fetch_stock_prices(symbol)
        financial_metrics = fetch_financial_metrics(symbol)

        # Append fetched data to stock_data list
        stock_data.append({
            'Symbol': symbol,
            'Name': name,
            'Stock_Price': stock_price,
            'Financial_Metrics': financial_metrics
        })

    # Convert stock_data list to DataFrame and save as CSV
    stock_data_df = pd.DataFrame(stock_data)
    stock_data_df.to_csv('stock_data.csv', index=False)

# Entry point for script execution
if __name__ == "__main__":
    fetch_all_data_for_stocks()

"""
[Start]
    |
    v
[Configure Logging]
    |
    v
[Read Stock Data from CSV]
    |
    v
[Sort Stocks by Market Cap]
    |
    v
[Initialize Empty List for Stock Data]
    |
    v
[For Each Stock in Sorted List]
    |---------------------------|
    |                           |
    v                           v
[Fetch Stock Price]     [Fetch Financial Metrics]
    |                           |
    v                           v
[Append Stock Data] <--[Merge Stock and Financial Data]
    |                           |
    v                           |
[End of Loop] <----------------|
    |
    v
[Convert List to DataFrame]
    |
    v
[Save DataFrame to CSV]
    |
    v
[End]
"""