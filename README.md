# Stock Data Scraper

## Project Description

This Python-based project is designed to scrape real-time stock data from Google Finance for companies listed on both the NASDAQ and NYSE. By leveraging BeautifulSoup for web scraping and Pandas for data manipulation, the program fetches key financial metrics as well as the stock prices for selected companies. The fetched data is saved in a CSV format for further financial analysis. The project includes efficient handling of rate limiting and robust logging to facilitate debugging and tracking.

## Features

- **Real-Time Stock Data**: Fetches real-time stock prices and key financial metrics.
- **Multiple Exchanges**: Supports NASDAQ and NYSE listed companies.
- **Data Storage**: Saves the fetched data in a CSV file.
- **Rate Limiting**: Handles rate limits efficiently to prevent overloading the server.
- **Logging**: Comprehensive logging for debugging and data tracking.

## Requirements

- Python 3.x
- Pandas
- BeautifulSoup
- Requests
- Logging

## Installation

1. Clone the repository.
    ```
    git clone https://github.com/YourUsername/StockDataScraper.git
    ```

2. Install the required packages.
    ```
    pip install -r requirements.txt
    ```

## Usage

Run the `data_extraction.py` script.

## License

MIT License