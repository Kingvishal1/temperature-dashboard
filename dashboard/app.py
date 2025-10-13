from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import threading
import json
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "latest.json")
SHARED_TOKEN = "G1egViAPwPWO6x3b9UZIjx5eZcFPmVdQtWS946TjaBxVaUxYQ1u7fhtcSZc1DKyb"

app = Flask(__name__, static_folder="static", static_url_path="/static")

# structure: { "device_name": { "temp_c": float, "ts": iso } }
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except Exception:
        data = {}
else:
    data = {}

data_lock = threading.Lock()

def save_data():
    with data_lock:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

@app.route("/api/temps", methods=["POST"])
def receive_temp():
    payload = request.get_json(force=True)
    token = payload.get("token")
    if token != SHARED_TOKEN:
        return jsonify({"error":"unauthorized"}), 401
    device = payload.get("device")
    temp = payload.get("temp_c")
    ts = payload.get("ts") or datetime.utcnow().isoformat()
    if device is None or temp is None:
        return jsonify({"error":"missing fields"}), 400
    with data_lock:
        data[device] = {"temp_c": float(temp), "ts": ts}
    save_data()
    return jsonify({"ok":True})

@app.route("/api/temps", methods=["GET"])
def get_temps():
    with data_lock:
        return jsonify(data)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
