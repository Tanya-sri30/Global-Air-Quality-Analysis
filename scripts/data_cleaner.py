"""
data_cleaner.py
---------------
Cleans and preprocesses datasets for Global Air Quality Analysis.
"""

import pandas as pd
import numpy as np

def clean_temperature_data(df):
    """Clean temperature datasets: remove nulls, convert dates, and rename columns."""
    if df.empty:
        return df

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Convert date column to datetime if it exists
    if 'dt' in df.columns:
        df['dt'] = pd.to_datetime(df['dt'], errors='coerce')

    # Drop rows where temperature is missing
    temp_cols = [col for col in df.columns if 'average' in col or 'temperature' in col]
    for col in temp_cols:
        df = df[df[col].notna()]

    # Remove duplicates
    df = df.drop_duplicates()

    return df


def clean_air_quality_data(df):
    """Clean OpenAQ dataset, handling malformed rows or incorrect parsing."""
    if df.empty:
        return df

    # If it has only 1 column, try to re-split manually by commas
    if df.shape[1] == 1:
        try:
            df = df[df.columns[0]].astype(str).str.split(',', expand=True)
            print("⚙️ Fixed malformed OpenAQ data by splitting column values.")
        except Exception as e:
            print(f"❌ Error while fixing OpenAQ data: {e}")
            return pd.DataFrame()

    # Ensure column names are strings before cleaning
    df.columns = df.columns.map(str)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    # Drop empty rows
    df = df.dropna(how='all')

    return df



def clean_all_datasets(datasets):
    """Apply cleaning functions to all loaded datasets."""
    cleaned_data = {}

    for name, df in datasets.items():
        if 'air_quality' in name:
            cleaned_data[name] = clean_air_quality_data(df)
        else:
            cleaned_data[name] = clean_temperature_data(df)

    print("\n🧹 All datasets cleaned successfully!\n")
    return cleaned_data


if __name__ == "__main__":
    from data_loader import load_all_datasets

    data = load_all_datasets()
    cleaned = clean_all_datasets(data)

    # Print shapes for verification
    for name, df in cleaned.items():
        print(f"{name}: {df.shape}")
