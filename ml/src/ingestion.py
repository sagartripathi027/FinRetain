import os
import glob
import pandas as pd
from typing import List

from validation import validate_dataset

def get_raw_csv_files(data_dir: str) -> List[str]:
    """
    Discover all CSV files in the data directory.
    """
    if os.path.isfile(data_dir) and data_dir.endswith('.csv'):
        return [data_dir]
        
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Directory not found: {data_dir}")
        
    files = glob.glob(os.path.join(data_dir, "*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in directory: {data_dir}")
        
    return files

def load_and_combine_csvs(data_dir: str, is_training: bool = True) -> pd.DataFrame:
    """
    Ingest, validate, and combine multiple CSV files from a directory.
    """
    files = get_raw_csv_files(data_dir)
    
    dfs = []
    for file in files:
        try:
            df = pd.read_csv(file)
            # Basic validation on each file individually
            validate_dataset(df, is_training=is_training)
            dfs.append(df)
        except Exception as e:
            raise RuntimeError(f"Error reading or validating {file}: {str(e)}")
            
    # Combine datasets
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Remove duplicates based on customer_id if it exists
    if 'customer_id' in combined_df.columns:
        combined_df = combined_df.drop_duplicates(subset=['customer_id'])
    else:
        combined_df = combined_df.drop_duplicates()
        
    # Basic cleaning
    combined_df = combined_df.dropna(how='all')
    
    return combined_df

