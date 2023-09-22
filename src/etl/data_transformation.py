import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import ast

def convert_financial_notation(row: str) -> float:
    if 'B' in row:
        return float(row.replace('B', '')) * 1e9
    elif 'M' in row:
        return float(row.replace('M', '')) * 1e6
    elif 'K' in row:
        return float(row.replace('K', '')) * 1e3
    elif 'T' in row:
        return float(row.replace('T', '')) * 1e12
    else:
        return float(row)

def convert_str_to_dict(row):
    try:
        return ast.literal_eval(row)
    except (ValueError, SyntaxError):
        return {}

def flatten_financial_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df['Financial_Metrics'] = df['Financial_Metrics'].apply(convert_str_to_dict)
    df_metrics = df['Financial_Metrics'].apply(pd.Series)
    df = pd.concat([df.drop(['Financial_Metrics'], axis=1), df_metrics], axis=1)
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df.fillna(0, inplace=True)
    return df

def type_conversion(df: pd.DataFrame) -> pd.DataFrame:
    if 'Revenue' in df.columns:
        df['Revenue'] = df['Revenue'].apply(convert_financial_notation).astype(float)
    return df

def clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    df['Name'] = df['Name'].str.strip().str.upper()
    return df

def handle_outliers(df: pd.DataFrame, column: str) -> pd.DataFrame:
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    df = df[(df[column] >= (Q1 - 1.5 * IQR)) & (df[column] <= (Q3 + 1.5 * IQR))]
    return df

def normalize(df: pd.DataFrame, column: str) -> pd.DataFrame:
    scaler = MinMaxScaler()
    df[column] = scaler.fit_transform(df[[column]])
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = handle_missing_values(df)
    df = type_conversion(df)
    df = clean_strings(df)
    if 'Revenue' in df.columns:
        df = handle_outliers(df, 'Revenue')
        df = normalize(df, 'Revenue')
    return df

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = flatten_financial_metrics(df)
    df = clean_data(df)
    return df

if __name__ == "__main__":
    stock_data_df = pd.read_csv('stock_data.csv')
    transformed_stock_data_df = transform_data(stock_data_df)
    print(transformed_stock_data_df)
