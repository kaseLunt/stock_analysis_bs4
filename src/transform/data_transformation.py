# Import necessary modules
import pandas as pd
import ast

# Function to convert financial notations to their respective numerical values
def convert_financial_notation(row: str) -> float:
    # Handle NaN values
    if pd.isna(row):
        return row
    
    # Check if the row is a string type
    if isinstance(row, str):
        # Convert Billion notation to numerical form
        if 'B' in row:
            return float(row.replace('B', '')) * 1e9
        # Convert Million notation to numerical form
        elif 'M' in row:
            return float(row.replace('M', '')) * 1e6
        # Convert Thousand notation to numerical form
        elif 'K' in row:
            return float(row.replace('K', '')) * 1e3
        # Convert Trillion notation to numerical form
        elif 'T' in row:
            return float(row.replace('T', '')) * 1e12
        # Remove dollar sign and convert to float
        elif '$' in row:
            return float(row.replace('$', '').replace(',', ''))
        # Convert percentage to float
        elif '%' in row:
            return float(row.replace('%', '')) / 100
    
    # If no special character found, return the row as is
    return row

# Function to convert string representation of dictionaries to actual dictionaries
def convert_str_to_dict(row):
    try:
        return ast.literal_eval(row)
    except (ValueError, SyntaxError):
        return {}

# Function to flatten the Financial_Metrics column into separate columns
def flatten_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df['Financial_Metrics'] = df['Financial_Metrics'].apply(convert_str_to_dict)
    df_metrics = df['Financial_Metrics'].apply(pd.Series)
    df = pd.concat([df.drop(['Financial_Metrics'], axis=1), df_metrics], axis=1)
    return df

# Function to handle missing values in the DataFrame
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df.loc[:, numeric_cols] = df.loc[:, numeric_cols].fillna(0)
    return df

# Function to convert all financial columns to numerical types
def convert_all_to_numeric(df: pd.DataFrame, financial_columns: list) -> pd.DataFrame:
    for col in financial_columns:
        df[col] = df[col].apply(convert_financial_notation)
    return df

# Function to clean string values in the DataFrame
def clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    df['Name'] = df['Name'].str.strip().str.upper()
    return df

# Wrapper function to perform all data cleaning operations
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = handle_missing_values(df)
    financial_columns = ['Stock_Price', 'Revenue', 'Operating expense', 'Net income', 'Net profit margin', 'Earnings per share', 'EBITDA', 'Effective tax rate']
    df = convert_all_to_numeric(df, financial_columns)
    df = clean_strings(df)
    return df

# Wrapper function to perform all data transformation operations
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = flatten_financial_metrics(df)
    df = clean_data(df)
    return df

# Main execution
if __name__ == "__main__":
    stock_data_df = pd.read_csv('stock_data.csv')
    transformed_stock_data_df = transform_data(stock_data_df)
    print(transformed_stock_data_df)
