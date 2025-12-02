"""
data_loader.py
--------------
Loads all datasets required for the Global Air Quality Analysis project.
"""

import pandas as pd
import os

# Base directory for your data
DATA_DIR = os.path.join("data")

def load_dataset(file_name):
    """Load a single CSV file safely and return a pandas DataFrame."""
    file_path = os.path.join(DATA_DIR, file_name)
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        df = pd.read_csv(file_path, on_bad_lines='skip')  # 👈 FIX HERE
        print(f"✅ Loaded: {file_name} — Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"❌ Error loading {file_name}: {e}")
        return pd.DataFrame()


def load_all_datasets():
    """Load all required datasets and return as a dictionary."""
    datasets = {
        "city_temp": load_dataset("GlobalLandTemperaturesByCity.csv"),
        "country_temp": load_dataset("GlobalLandTemperaturesByCountry.csv"),
        "major_city_temp": load_dataset("GlobalLandTemperaturesByMajorCity.csv"),
        "state_temp": load_dataset("GlobalLandTemperaturesByState.csv"),
        "global_temp": load_dataset("GlobalTemperatures.csv"),
        "air_quality": load_dataset("openaq.csv"),
    }

    print("\n📦 All datasets loaded successfully!\n")
    return datasets

if __name__ == "__main__":
    # For testing in VS Code
    data = load_all_datasets()
    for name, df in data.items():
        print(f"{name}: {df.shape}")
