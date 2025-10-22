from flask import Flask, request, jsonify, send_from_directory

import os
import pigpio
import DHT
import time
import threading
from datetime import datetime
from src.api import temp

SHARED_TOKEN = "G1egViAPwPWO6x3b9UZIjx5eZcFPmVdQtWS946TjaBxVaUxYQ1u7fhtcSZc1DKyb"

app = Flask(__name__, static_folder="static", static_url_path="/static")

# DHT22 sensor configuration
DHT_PIN = 26
sensor = DHT.DHTXX

def read_dht22_direct():
    """Read DHT22 sensor data directly and return immediately"""
    try:
        pi = pigpio.pi()
        if not pi.connected:
            print("Failed to connect to pigpio daemon")
            return {"temperature": None, "humidity": None, "timestamp": None, "error": "Failed to connect to pigpio"}

        s = DHT.sensor(pi, DHT_PIN, model=sensor)

        tries = 5
        result = {"temperature": None, "humidity": None, "timestamp": None}

        while tries:
            try:
                timestamp, gpio, status, temperature, humidity = s.read()
                if status == DHT.DHT_GOOD:
                    result["temperature"] = temperature
                    result["humidity"] = humidity
                    result["timestamp"] = datetime.now().isoformat()
                    break
                time.sleep(2)
                tries -= 1
            except KeyboardInterrupt:
                break

        s.cancel()
        pi.stop()
        return result
    except Exception as e:
        print(f"Error reading DHT22: {e}")
        return {"temperature": None, "humidity": None, "timestamp": None, "error": str(e)}


@app.route("/api/temps", methods=["POST"])
def receive_temp():
    return temp.receive_device_info(request.get_json(force=True))


@app.route("/api/temps", methods=["GET"])
def get_temps():
    return temp.return_info()


@app.route("/api/room", methods=["GET"])
def get_room_data():
    """Get DHT22 room temperature and humidity data - reads directly from sensor"""
    return jsonify(read_dht22_direct())


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
