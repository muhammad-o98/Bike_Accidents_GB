# src/preprocessing.py
import os
import pandas as pd

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and create features for dashboard."""
    df = df.copy()
    
    # Standardize column names
    df.columns = df.columns.str.lower()
    
    # Strip strings
    string_cols = ['road_conditions', 'weather_conditions', 'road_type', 
                   'light_conditions', 'gender', 'severity', 'age_grp', 'day']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
    
    # Convert dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.day_name()
    
    # Convert time
    df['time'] = pd.to_datetime(df['time'], format='%H:%M', errors='coerce').dt.time
    
    # Encode severity
    severity_map = {'Slight': 1, 'Serious': 2, 'Fatal': 3}
    df['severity_numeric'] = df['severity'].map(severity_map)
    
    return df

def save_parquet(df: pd.DataFrame, path: str):
    """Save DataFrame as Parquet, creating directories if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)  # <-- ensures folder exists
    df.to_parquet(path, index=False, engine='pyarrow')  # specify engine explicitly
