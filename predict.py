import subprocess
import re
import sqlite3
import pandas as pd
import joblib
from collections import deque

# Load trained model
clf = joblib.load("zone_predictor_rf_model.joblib")


# Scan Wi-Fi networks
def scan_wifi():
    command = "netsh wlan show networks mode=bssid"
    result = subprocess.check_output(command, shell=True, encoding='utf-8', errors='ignore')

    bssids = re.findall(r'BSSID\s+\d+\s*:\s*([\w:]+)', result)
    signals = re.findall(r'Signal\s*:\s*(\d+)%', result)

    wifi_data = []
    for bssid, signal in zip(bssids, signals):
        rssi = int(signal) // 2 - 100  # Convert % to approximate dBm
        wifi_data.append((bssid, rssi))

    return dict(wifi_data)
# Predict current zone using trained model
def predict_zone(wifi_dict):
    all_bssids = clf.feature_names_in_
    row = {bssid: wifi_dict.get(bssid, -100) for bssid in all_bssids}
    df = pd.DataFrame([row])
    predicted_zone = clf.predict(df)[0]
    return predicted_zone





# Main workflow
def navigate():
    print("📡 Scanning Wi-Fi to detect current location...")
    wifi_dict = scan_wifi()

    if not wifi_dict:
        print("❌ No Wi-Fi data found. Try again.")
        return

    current_zone = predict_zone(wifi_dict)
    print(f"📍 Detected current zone: {current_zone}")

if __name__ == "__main__":
    navigate()
