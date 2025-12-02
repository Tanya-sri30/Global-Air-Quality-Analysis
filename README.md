.

🌍 Global Air Quality & Climate Analysis Dashboard

A Python-powered analytical project that explores global temperature patterns, air quality trends, and climate–pollution correlations.
It includes automated preprocessing, visual analytics scripts, and a clean Flask-based dashboard for presenting insights.

🚀 Key Features
🔹 Data Processing & Analysis

Robust CSV loading (handles malformed rows & inconsistent schemas)

Standardizes OpenAQ dataset (column cleaning + missing value treatment)

Extracts time-based features from timestamps

Generates statistical summaries for:

Air quality (AQI / pollutant levels)

Global, country-level, and city-level temperature trends

🔹 Visualization Suite

Automatically stores plots inside the visuals/ directory:

📈 Top 10 Polluted Cities

🌡️ Top 10 Hottest Countries

🌍 Global Temperature Trend (1850–2024)

🧪 Pollutant Distribution

🔗 Temperature vs AQI Correlation

📊 Summary CSV files (city, country, global, AQI)

Each visual is accompanied by a descriptive caption inside the dashboard.

🖥️ Flask Dashboard (UI Layer)

A lightweight, modern UI designed to present all visuals in a professional layout:

Responsive card-style design

Clean light theme for high readability

Caption + short interpretation under every visualization

Simple and fast to deploy (Flask + HTML + CSS)

⚙️ How to Run Locally
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Add datasets

Place your data files inside:

/data


(This folder is Git-ignored to avoid pushing large datasets.)

3️⃣ Generate visuals
python scripts/visualizer.py

4️⃣ Start the dashboard
python app.py


Open your browser at:

👉 http://127.0.0.1:5000/

📡 Data Sources

Berkeley Earth — Global Land & Ocean Temperature Data

OpenAQ Platform — Global Air Quality Observations