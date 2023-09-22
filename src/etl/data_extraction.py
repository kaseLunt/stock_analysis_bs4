# Import standard libraries and packages
import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import os

# Configure logging for debugging and monitoring
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# Constants for Google Finance URL and HTTP headers
GOOGLE_FINANCE_URL = 'https://www.google.com/finance/quote/{symbol}:{exchange}?hl=en'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Determine the directory path of the current script and where to save the CSV
dir_path = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join(dir_path, '../../data/raw/nasdaq_stocks.csv')

# Function to make HTTP requests and handle potential exceptions
def make_request(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.HTTPError as e:
        logging.error(f"Failed to retrieve {url}, status code: {response.status_code}, error: {e}")
        return None

# Function to fetch stock prices from Google Finance for multiple exchanges
def fetch_stock_prices(symbol, exchanges=['NASDAQ', 'NYSE']):
    for exchange in exchanges:
        url = GOOGLE_FINANCE_URL.format(symbol=symbol, exchange=exchange)
        content = make_request(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            stock_price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})
            if stock_price_element:
                return stock_price_element.text
    return None

# Function to fetch financial metrics from Google Finance for multiple exchanges
def fetch_financial_metrics(symbol, exchanges=['NASDAQ', 'NYSE']):
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

# Main function to fetch all required data for stocks listed on NASDAQ and NYSE
def fetch_all_data_for_stocks():
    df = pd.read_csv(csv_file_path)
    df['Market Cap'] = df['Market Cap'].apply(pd.to_numeric, errors='coerce')
    df = df.nlargest(10, 'Market Cap')
    stock_data = []
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
    stock_data_df.to_csv('stock_data.csv', index=False)

# Script entry point
if __name__ == "__main__":
    fetch_all_data_for_stocks()
