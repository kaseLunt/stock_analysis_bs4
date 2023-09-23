# Importing the required modules and functions from other scripts
from extract.data_extraction import fetch_all_data_for_stocks
from transform.data_transformation import transform_data
from load.data_load import establish_connection, create_table_if_not_exists, load_data_into_postgresql
import logging
import pandas as pd
import os
import psycopg2

# Initialize logging for debugging and tracking
logging.basicConfig(level=logging.INFO)

# Function to fetch rows for confirmation
def fetch_and_print_rows(conn):
    cursor = conn.cursor()
    query = "SELECT * FROM stock_data LIMIT 10;"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()

# Get the directory of the currently executing script
dir_path = os.path.dirname(os.path.realpath(__file__))
stock_data_path = os.path.join(dir_path, '../stock_data.csv')

# Define the main function that orchestrates the ETL process
def main():
    logging.info("Starting data extraction process.")
    fetch_all_data_for_stocks()
    logging.info("Data extraction complete.")
    
    logging.info("Starting data transformation process.")
    stock_data_df = pd.read_csv(stock_data_path)
    transformed_stock_data_df = transform_data(stock_data_df)
    logging.info("Data transformation complete.")
    
    logging.info("Starting data loading process.")
    conn = establish_connection()
    if conn:
        create_table_if_not_exists(conn)
        load_data_into_postgresql(transformed_stock_data_df, conn)
        logging.info("Data loading complete.")
        
        # Confirmation Query
        logging.info("Starting confirmation query.")
        fetch_and_print_rows(conn)
        
        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()
