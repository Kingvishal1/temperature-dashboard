from flask import Flask, request, jsonify, send_from_directory

import os
from src.api import temp

SHARED_TOKEN = "G1egViAPwPWO6x3b9UZIjx5eZcFPmVdQtWS946TjaBxVaUxYQ1u7fhtcSZc1DKyb"

app = Flask(__name__, static_folder="static", static_url_path="/static")


@app.route("/api/temps", methods=["POST"])
def receive_temp():
    print("received request: " + request.get_json)
    return temp.receive_device_info(request.get_json(force=True))


@app.route("/api/temps", methods=["GET"])
def get_temps():
    return temp.return_info()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
