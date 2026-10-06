import pandas as pd
from features import get_features, TARGET

def validate_columns(df: pd.DataFrame, is_training: bool = True):
    """
    Ensure all required features are present in the dataset.
    """
    missing = [f for f in get_features() if f not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")
        
    if is_training and TARGET not in df.columns:
        raise ValueError(f"Missing target column: {TARGET}")

def validate_data_types_and_ranges(df: pd.DataFrame):
    """
    Check for obvious invalid values in the data.
    """
    if 'tenure' in df.columns and (df['tenure'] < 0).any():
        raise ValueError("tenure cannot be negative")
    
    if 'transaction_frequency' in df.columns and (df['transaction_frequency'] < 0).any():
        raise ValueError("transaction_frequency cannot be negative")
        
    if 'complaints' in df.columns and (df['complaints'] < 0).any():
        raise ValueError("complaints cannot be negative")

def validate_dataset(df: pd.DataFrame, is_training: bool = True):
    """
    Run all validation checks on the dataset.
    """
    validate_columns(df, is_training=is_training)
    validate_data_types_and_ranges(df)
    return True

