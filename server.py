from flask import Flask, jsonify, render_template  # ⬅️ Add render_template
import subprocess
import re
import pandas as pd
import joblib
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")  # ⬅️ Specify folders
CORS(app)

# Route for homepage
@app.route("/")
def home():
    return render_template("index.html")

# Load model
clf = joblib.load("zone_predictor_rf_model.joblib")

# Wi-Fi scanning function (Windows-based)
def scan_wifi():
    try:
        result = subprocess.check_output("netsh wlan show networks mode=bssid", shell=True, encoding='utf-8', errors='ignore')
        bssids = re.findall(r'BSSID\s+\d+\s*:\s*([\w:]+)', result)
        signals = re.findall(r'Signal\s*:\s*(\d+)%', result)
        wifi_data = {bssid: int(signal) // 2 - 100 for bssid, signal in zip(bssids, signals)}
        return wifi_data
    except:
        return {}

# Prediction endpoint
@app.route("/predict", methods=["GET"])
def predict():
    wifi_dict = scan_wifi()
    if not wifi_dict:
        return jsonify({"error": "No Wi-Fi data"}), 400

    all_bssids = clf.feature_names_in_
    row = {bssid: wifi_dict.get(bssid, -100) for bssid in all_bssids}
    df = pd.DataFrame([row])
    predicted_zone = clf.predict(df)[0]
    return jsonify({"predicted_zone": predicted_zone})

if __name__ == "__main__":
    app.run(debug=True)
