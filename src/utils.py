# src/utils.py
import pandas as pd

def load_parquet(path: str) -> pd.DataFrame:
    """Load Parquet file."""
    return pd.read_parquet(path)

def save_csv(df: pd.DataFrame, path: str):
    """Save DataFrame to CSV."""
    df.to_csv(path, index=False)

def summarize_df(df: pd.DataFrame):
    """Print basic summary of DataFrame."""
    print("Shape:", df.shape)
    print("\nColumns info:")
    print(df.info())
    print("\nMissing values:")
    print(df.isnull().sum())
