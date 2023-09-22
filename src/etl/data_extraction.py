# Import necessary libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import os

# Initialize logging for debugging and tracking
logging.basicConfig(level=logging.INFO)

# Constants for API URLs and headers
GOOGLE_FINANCE_URL = 'https://www.google.com/finance/quote/{symbol}:{exchange}?hl=en'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Get the directory of the currently executing script
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join(dir_path, '../../data/raw/nasdaq_stocks.csv')

# Function to make HTTP requests and handle exceptions
def make_request(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.HTTPError as e:
        logging.error(f"Failed to retrieve {url}, status code: {response.status_code}, error: {e}")
        return None

# Function to fetch stock prices from multiple exchanges
def fetch_stock_prices(symbol, exchanges=['NASDAQ', 'NYSE']):
    stock_price = None  # Initialize stock price as None
    for exchange in exchanges:
        url = GOOGLE_FINANCE_URL.format(symbol=symbol, exchange=exchange)
        content = make_request(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            stock_price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})
            if stock_price_element:
                stock_price = stock_price_element.text
                break  # Exit the loop if a stock price is found
    return stock_price

# Function to fetch financial metrics from multiple exchanges
def fetch_financial_metrics(symbol, exchanges=['NASDAQ', 'NYSE']):
    financial_metrics = None  # Initialize financial metrics as None
    for exchange in exchanges:
        url = GOOGLE_FINANCE_URL.format(symbol=symbol, exchange=exchange)
        content = make_request(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            metrics_table = soup.find('table', {'class': 'slpEwd'})
            if metrics_table:
                financial_metrics = {}  # Initialize an empty dictionary for financial metrics
                rows = metrics_table.find_all('tr', {'class': 'roXhBd'})
                for row in rows[1:]:  # Skip the header row
                    metric_td = row.find('td', {'class': 'J9Jhg'})
                    metric_name = metric_td.find('div').text.strip()
                    metric_value = row.find('td', {'class': 'QXDnM'}).text.strip()
                    financial_metrics[metric_name] = metric_value
                break  # Exit loop if metrics are found
    return financial_metrics

# Main function to fetch all stock data for NASDAQ and NYSE stocks
def fetch_all_data_for_stocks():
    df = pd.read_csv(csv_file_path)
    df['Market Cap'] = df['Market Cap'].apply(pd.to_numeric, errors='coerce')
    df = df.nlargest(20, 'Market Cap')  # Filter top 20 stocks by Market Cap
    stock_data = []  # Initialize an empty list for stock data
    for index, row in df.iterrows():
        symbol = row['Symbol']
        name = row['Name']
        logging.info(f"Fetching data for {name} ({symbol})")
        stock_price = fetch_stock_prices(symbol)
        financial_metrics = fetch_financial_metrics(symbol)
        stock_data.append({
            'Symbol': symbol,
            'Name': name,
            'Stock_Price': stock_price,
            'Financial_Metrics': financial_metrics
        })
    stock_data_df = pd.DataFrame(stock_data)
    stock_data_df.to_csv('stock_data.csv', index=False)  # Save data to CSV

# Entry point of the script
if __name__ == "__main__":
    fetch_all_data_for_stocks()
