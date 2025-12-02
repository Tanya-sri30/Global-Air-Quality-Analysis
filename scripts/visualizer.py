import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========== Setup ==========
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
VISUALS_DIR = os.path.join(BASE_DIR, "visuals")
os.makedirs(VISUALS_DIR, exist_ok=True)

sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
print("📊 Starting visualizer...")

# ========== Safe CSV loader ==========
def safe_load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    try:
        # Try normal read
        df = pd.read_csv(path, engine="python", on_bad_lines="skip")
        # If single column -> try other separators
        if df.shape[1] == 1:
            try:
                df = pd.read_csv(path, sep=";", engine="python", on_bad_lines="skip")
            except Exception:
                df = pd.read_csv(path, sep="|", engine="python", on_bad_lines="skip")
        print(f"✅ Loaded: {filename} — Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")
        return pd.DataFrame()

# ========== Load Datasets ==========
air = safe_load_csv("openaq.csv")
temp = safe_load_csv("GlobalTemperatures.csv")

# Stop if both failed
if air.empty and temp.empty:
    print("❌ Both datasets failed to load. Exiting.")
    exit()

print("🔎 Air Quality Columns:", air.columns.tolist())
print("🔎 Temperature Columns:", temp.columns.tolist())

# ========== Clean headers safely ==========
if not air.empty:
    air.columns = air.columns.map(str).str.strip().str.lower()
if not temp.empty:
    temp.columns = temp.columns.map(str).str.strip().str.lower()

# ========== Column detection ==========
def find_col(cols, keywords):
    for key in keywords:
        for c in cols:
            if key in c:
                return c
    return None

city_col = find_col(air.columns, ["city"])
country_col = find_col(temp.columns, ["country"])
pollutant_col = find_col(air.columns, ["pollutant"])
value_col = find_col(air.columns, ["value", "concentration", "pm25", "pm2.5"])
date_col = find_col(air.columns, ["date", "last updated", "utc"])
temp_col = find_col(temp.columns, ["averagetemperature", "landaveragetemperature"])
temp_date_col = find_col(temp.columns, ["dt"])

# ========== VISUAL 1: Top Polluted Cities ==========
try:
    if city_col and value_col:
        air[city_col] = air[city_col].astype(str)
        city_avg = air.groupby(city_col)[value_col].mean().sort_values(ascending=False).head(10)
        plt.figure()
        sns.barplot(x=city_avg.values, y=city_avg.index, palette="rocket")
        plt.title("🌆 Top 10 Most Polluted Cities")
        plt.xlabel("Average AQI Value")
        plt.ylabel("City")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALS_DIR, "top_10_polluted_cities.png"))
        plt.close()
        print("📈 Saved: Top Polluted Cities Plot")
    else:
        raise KeyError(f"Missing columns — city_col: {city_col}, value_col: {value_col}")
except Exception as e:
    print(f"⚠️ Skipped Top Polluted Cities plot: '{e}'")

# ========== VISUAL 2: Hottest Countries ==========
try:
    if country_col and temp_col:
        country_avg = temp.groupby(country_col)[temp_col].mean().sort_values(ascending=False).head(10)
        plt.figure()
        sns.barplot(x=country_avg.values, y=country_avg.index, palette="coolwarm")
        plt.title("🌡️ Top 10 Hottest Countries")
        plt.xlabel("Average Temperature (°C)")
        plt.ylabel("Country")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALS_DIR, "top_10_hottest_countries.png"))
        plt.close()
        print("📈 Saved: Hottest Countries Plot")
    else:
        raise KeyError(f"Missing columns — country_col: {country_col}, temp_col: {temp_col}")
except Exception as e:
    print(f"⚠️ Skipped Hottest Countries plot: '{e}'")

# ========== VISUAL 3: Global Temperature Trend ==========
try:
    if temp_date_col and temp_col:
        temp[temp_date_col] = pd.to_datetime(temp[temp_date_col], errors="coerce")
        yearly = temp.groupby(temp[temp_date_col].dt.year)[temp_col].mean().dropna()
        plt.figure()
        plt.plot(yearly.index, yearly.values, color="orange", linewidth=2.5)
        plt.title("📈 Global Average Temperature Over Years")
        plt.xlabel("Year")
        plt.ylabel("Temperature (°C)")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALS_DIR, "global_temperature_trend.png"))
        plt.close()
        print("📈 Saved: Global Temperature Trend")
    else:
        raise KeyError(f"Missing columns — temp_date_col: {temp_date_col}, temp_col: {temp_col}")
except Exception as e:
    print(f"⚠️ Skipped Global Temperature Trend plot: '{e}'")

# ========== VISUAL 4: AQI vs Temperature Correlation ==========
try:
    if date_col and temp_date_col and value_col and temp_col:
        air[date_col] = pd.to_datetime(air[date_col], errors="coerce")
        temp[temp_date_col] = pd.to_datetime(temp[temp_date_col], errors="coerce")

        air["year"] = air[date_col].dt.year
        temp["year"] = temp[temp_date_col].dt.year

        merged = pd.merge(
            air.groupby("year")[value_col].mean(),
            temp.groupby("year")[temp_col].mean(),
            left_index=True,
            right_index=True,
            how="inner"
        )

        plt.figure()
        sns.regplot(x=temp_col, y=value_col, data=merged, color="green")
        plt.title("🌡️ Temperature vs AQI Correlation")
        plt.xlabel("Average Temperature (°C)")
        plt.ylabel("Average AQI")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALS_DIR, "temp_vs_aqi_correlation.png"))
        plt.close()
        print("📊 Saved: AQI vs Temperature Correlation")
    else:
        raise KeyError(
            f"Missing columns — date_col: {date_col}, temp_date_col: {temp_date_col}, temp_col: {temp_col}, value_col: {value_col}"
        )
except Exception as e:
    print(f"⚠️ Skipped Correlation plot: '{e}'")

# ========== VISUAL 5: Pollutant Distribution ==========
try:
    if pollutant_col:
        plt.figure()
        air[pollutant_col].value_counts().head(10).plot(
            kind="pie", autopct="%1.1f%%", startangle=90, colors=sns.color_palette("pastel")
        )
        plt.title("☁️ Pollutant Type Distribution")
        plt.ylabel("")
        plt.tight_layout()
        plt.savefig(os.path.join(VISUALS_DIR, "pollutant_distribution.png"))
        plt.close()
        print("🌫️ Saved: Pollutant Distribution Pie Chart")
    else:
        raise KeyError(f"Missing pollutant_col: {pollutant_col}")
except Exception as e:
    print(f"⚠️ Skipped Pollutant Distribution: '{e}'")

print("\n✅ All advanced visuals saved successfully in /visuals folder.\n")
