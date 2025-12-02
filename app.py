from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# --- Path to the visuals folder ---
VISUALS_DIR = os.path.join(os.getcwd(), "visuals")

# --- Serve images dynamically ---
@app.route("/visuals/<path:filename>")
def visuals(filename):
    return send_from_directory(VISUALS_DIR, filename)

# --- Specific Captions & Analytical Descriptions ---
descriptions = {
    "top_10_polluted_cities": {
        "caption": "Top 10 Polluted Cities (Global Overview)",
        "desc": "This visual highlights the most polluted cities worldwide based on particulate matter concentration (PM2.5/PM10). \
        These regions represent critical zones where industrialization, traffic emissions, and lack of air regulations have led to extreme air quality deterioration."
    },
    "top_10_hottest_countries": {
        "caption": "Top 10 Hottest Countries on Record",
        "desc": "This chart presents the countries with the highest average land temperatures. \
        It reflects the intensifying global warming trends, particularly across arid and equatorial regions."
    },
    "global_temperature_trend": {
        "caption": "Global Temperature Trend (1850–2023)",
        "desc": "A time-series visualization of average global land temperatures. \
        The rising trend clearly illustrates the effect of greenhouse gas accumulation and human-induced climate change."
    },
    "pollutant_distribution": {
        "caption": "Pollutant Distribution Analysis",
        "desc": "This distribution chart compares the occurrence frequency of pollutant levels across measurement sites. \
        It provides insight into how often air quality reaches critical thresholds in sampled regions."
    },
    "correlation_heatmap": {
        "caption": "Correlation Between Environmental Factors",
        "desc": "The heatmap represents statistical correlations between pollutants, temperature, and humidity levels. \
        Strong relationships highlight how climate conditions amplify or mitigate air pollution severity."
    }
}

@app.route("/")
def home():
    visuals = []
    if os.path.exists(VISUALS_DIR):
        for file in os.listdir(VISUALS_DIR):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                name = os.path.splitext(file)[0]
                visuals.append({
                    "filename": file,
                    "caption": descriptions.get(name, {}).get("caption", name.replace("_", " ").title()),
                    "desc": descriptions.get(name, {}).get("desc", "This visualization provides analytical insight into air quality and climate interactions.")
                })
    visuals.sort(key=lambda x: x["filename"])
    return render_template("index.html", visuals=visuals)

if __name__ == "__main__":
    app.run(debug=True)
