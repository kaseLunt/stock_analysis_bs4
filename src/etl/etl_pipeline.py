from data_extraction import fetch_stock_prices, fetch_financial_metrics, fetch_investopedia_news
from data_transformation import clean_data
import pandas as pd

def etl_pipeline(symbol, exchange):
    # Extraction
    stock_price = fetch_stock_prices(symbol, exchange)
    financial_metrics = fetch_financial_metrics(symbol, exchange)
    news_articles = fetch_investopedia_news(symbol, alias=None)  # Replace alias with actual alias if applicable

    # Transformation
    # Assume we have converted the extracted data into a DataFrame named df
    # df = pd.DataFrame(financial_metrics, index=[0])  # Example
    # cleaned_df = clean_data(df)
    
    # TODO: Loading into Database
    ...
