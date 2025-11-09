# src/etl.py
import pandas as pd

def load_csv(path: str, low_memory: bool = False) -> pd.DataFrame:
    """
    Load CSV into DataFrame.
    """
    return pd.read_csv(path, low_memory=low_memory)

def merge_accidents_bikers(accidents_path: str, bikers_path: str) -> pd.DataFrame:
    """
    Merge accidents and bikers datasets on Accident_Index.
    Returns merged DataFrame.
    """
    accidents = load_csv(accidents_path)
    bikers = load_csv(bikers_path)
    
    df = pd.merge(accidents, bikers, on='Accident_Index', how='inner')
    return df
