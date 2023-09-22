import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# Function to handle missing values by filling NaNs with zeros
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace NaN values with zeros.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        
    Returns:
        pd.DataFrame: DataFrame with NaN values replaced.
    """
    df.fillna(0, inplace=True)
    return df

# Function to convert data types of columns
def type_conversion(df: pd.DataFrame) -> pd.DataFrame:
    """Convert the data types of specific columns.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        
    Returns:
        pd.DataFrame: DataFrame with converted data types.
    """
    df['Revenue'] = df['Revenue'].astype(float)
    return df

# Function to clean string columns
def clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the strings in the DataFrame.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        
    Returns:
        pd.DataFrame: DataFrame with cleaned strings.
    """
    df['Company'] = df['Company'].str.strip().str.upper()
    return df

# Function to handle outliers based on IQR
def handle_outliers(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Identify and remove outliers in a given column.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column (str): The column to check for outliers.
        
    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(df[column] >= (Q1 - 1.5 * IQR)) & (df[column] <= (Q3 + 1.5 * IQR))]
    return df

# Function to normalize a column
def normalize(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Normalize a specific column using MinMax scaling.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        column (str): The column to normalize.
        
    Returns:
        pd.DataFrame: DataFrame with normalized column.
    """
    scaler = MinMaxScaler()
    df[column] = scaler.fit_transform(df[[column]])
    return df

# Main function to clean data
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Perform all cleaning operations on the DataFrame.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = handle_missing_values(df)
    df = type_conversion(df)
    df = clean_strings(df)
    df = handle_outliers(df, 'Revenue')
    df = normalize(df, 'Revenue')
    return df

if __name__ == "__main__":
    # Read the stock_data.csv generated by data_extraction.py
    stock_data_df = pd.read_csv('stock_data.csv')
    # Apply transformations
    cleaned_stock_data_df = clean_data(stock_data_df)
    print(cleaned_stock_data_df)
