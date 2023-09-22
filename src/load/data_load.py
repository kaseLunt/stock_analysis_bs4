import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import pandas as pd


# Load environment variables
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def establish_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="StockAnalysisDB",
            user=DB_USER,
            password=DB_PASSWORD,
            port="5432"
        )
        print("Database connection established successfully")
        return conn
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Function to create table schema if it doesn't exist
def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS stock_data (
        id SERIAL PRIMARY KEY,
        Symbol TEXT,
        Name TEXT,
        Stock_Price FLOAT,
        Revenue FLOAT,
        Operating_Expense FLOAT,
        Net_Income FLOAT,
        Net_Profit_Margin FLOAT,
        Earnings_Per_Share FLOAT,
        EBITDA FLOAT,
        Effective_Tax_Rate FLOAT
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()


# Function to load DataFrame into PostgreSQL
def load_data_into_postgresql(df, conn):
    cursor = conn.cursor()
    for index, row in df.iterrows():
        clean_row = [None if x == "—" else x for x in row]  # Replace "—" with None
        insert_query = sql.SQL(
            "INSERT INTO stock_data (Symbol, Name, Stock_Price, Revenue, Operating_Expense, Net_Income, Net_Profit_Margin, Earnings_Per_Share, EBITDA, Effective_Tax_Rate) VALUES ({})"
        ).format(
            sql.SQL(', ').join(sql.Placeholder() for _ in clean_row)
        )
        cursor.execute(insert_query, clean_row)
    conn.commit()
    cursor.close()


def run_data_load(transformed_stock_data_df, conn):
    create_table_if_not_exists(conn)
    load_data_into_postgresql(transformed_stock_data_df, conn)
    close_connection(conn)

# Function to close the PostgreSQL connection
def close_connection(conn):
    if conn is not None:
        conn.close()

