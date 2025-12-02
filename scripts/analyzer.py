"""
analyzer.py
--------------------
Performs data analysis and visualization for Global Air Quality & Temperature datasets.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# === PATH SETUP ===
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
VISUALS_DIR = os.path.join(os.path.dirname(__file__), "..", "visuals")
os.makedirs(VISUALS_DIR, exist_ok=True)


# ========================
# 1️⃣ Safe Loader
# ========================
def load_dataset(filename):
    """Load CSV safely with fallback options."""
    path = os.path.join(DATA_DIR, filename)
    try:
        df = pd.read_csv(path, on_bad_lines="skip", sep=None, engine="python")
        print(f"✅ Loaded: {filename} — Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
        return pd.DataFrame()


# === Load all datasets ===
city_temp = load_dataset("GlobalLandTemperaturesByCity.csv")
country_temp = load_dataset("GlobalLandTemperaturesByCountry.csv")
major_city_temp = load_dataset("GlobalLandTemperaturesByMajorCity.csv")
state_temp = load_dataset("GlobalLandTemperaturesByState.csv")
global_temp = load_dataset("GlobalTemperatures.csv")
air_quality = load_dataset("openaq.csv")

print("\n📦 All datasets loaded successfully!\n")


# ========================
# 2️⃣ Helper Functions
# ========================
def find_temperature_column(df):
    """Auto-detect temperature column name."""
    candidates = ["AverageTemperature", "LandAverageTemperature", "MeanTemperature"]
    for col in df.columns:
        if col.strip() in candidates:
            return col.strip()
    return None


def dataset_summary(df, name):
    """Generate summary stats and save."""
    if df.empty:
        print(f"⚠️ Skipping {name} — empty dataset.")
        return
    summary = df.describe(include="all")
    summary.to_csv(os.path.join(VISUALS_DIR, f"{name}_summary.csv"))
    print(f"📊 Saved summary for {name}")


# Generate summaries
dataset_summary(city_temp, "city_temp")
dataset_summary(country_temp, "country_temp")
dataset_summary(major_city_temp, "major_city_temp")
dataset_summary(state_temp, "state_temp")
dataset_summary(global_temp, "global_temp")
dataset_summary(air_quality, "air_quality")


# ========================
# 3️⃣ Temperature Trend Plot
# ========================
def plot_temperature_trends(df, name, date_col="dt"):
    """Plot temperature trends (auto-detect column)."""
    if df.empty or date_col not in df.columns:
        print(f"⚠️ Skipping {name} trend plot.")
        return

    temp_col = find_temperature_column(df)
    if not temp_col:
        print(f"⚠️ No temperature column found in {name}.")
        return

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    monthly = df.groupby(df[date_col].dt.to_period("M"))[temp_col].mean().reset_index()
    monthly[date_col] = monthly[date_col].dt.to_timestamp()

    plt.figure()
    plt.plot(monthly[date_col], monthly[temp_col], color="royalblue")
    plt.title(f"{name} - Average Temperature Trend")
    plt.xlabel("Year")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUALS_DIR, f"{name}_temp_trend.png"))
    plt.close()
    print(f"📈 Saved {name} temperature trend plot.")


# Run temperature trend plots
plot_temperature_trends(global_temp, "GlobalTemperatures")
plot_temperature_trends(country_temp, "GlobalLandTemperaturesByCountry")
plot_temperature_trends(city_temp, "GlobalLandTemperaturesByCity")


# ========================
# 4️⃣ Air Quality Distribution
# ========================
if not air_quality.empty:
    numeric_cols = air_quality.select_dtypes(include="number").columns
    if len(numeric_cols) > 0:
        plt.figure()
        sns.histplot(air_quality[numeric_cols[0]], kde=True, color="teal")
        plt.title(f"Distribution of {numeric_cols[0]} (Air Quality)")
        plt.xlabel(numeric_cols[0])
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALS_DIR, "air_quality_distribution.png"))
        plt.close()
        print(f"🌫️ Saved air quality distribution plot.")
    else:
        print("⚠️ No numeric columns found in openaq.csv for AQI analysis.")


# ========================
# 5️⃣ Correlation Analysis
# ========================
def correlation_analysis(df1, df2, label1, label2):
    """Compare average temperature vs AQI mean."""
    if df1.empty or df2.empty:
        print("⚠️ Skipping correlation (missing dataset).")
        return

    try:
        df1 = df1.copy()
        df2 = df2.copy()

        # --- Temperature dataset ---
        df1["dt"] = pd.to_datetime(df1["dt"], errors="coerce")
        temp_col = find_temperature_column(df1)
        if not temp_col:
            print("⚠️ No temperature column found for correlation.")
            return
        temp_avg = df1.groupby(df1["dt"].dt.year)[temp_col].mean()

        # --- Air quality dataset ---
        date_col = "Last Updated" if "Last Updated" in df2.columns else "Date"
        df2[date_col] = pd.to_datetime(df2[date_col], errors="coerce")

        numeric_cols = df2.select_dtypes(include="number").columns
        if len(numeric_cols) == 0:
            print("⚠️ No numeric air quality data found.")
            return
        aqi_avg = df2.groupby(df2[date_col].dt.year)[numeric_cols[0]].mean()

        # --- Correlation ---
        corr = temp_avg.corr(aqi_avg)
        print(f"🔗 Correlation between temperature and AQI: {corr:.3f}")

        combined = pd.DataFrame({"Temp": temp_avg, "AQI": aqi_avg}).dropna()
        plt.figure()
        sns.regplot(x="Temp", y="AQI", data=combined, color="darkorange")
        plt.title(f"{label1} vs {label2} Correlation (r={corr:.2f})")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALS_DIR, "temp_aqi_correlation.png"))
        plt.close()

        print("📊 Saved temperature vs AQI correlation plot.")

    except Exception as e:
        print(f"❌ Correlation analysis failed: {e}")
