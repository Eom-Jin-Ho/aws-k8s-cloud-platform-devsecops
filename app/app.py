from flask import Flask, jsonify
from datetime import datetime, UTC
import socket
import os

app = Flask(__name__)

APP_NAME = "AWS Kubernetes Cloud Platform & DevSecOps"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Eom Jin Ho"


@app.route("/")
def home():
    return jsonify({
        "project": APP_NAME,
        "author": APP_AUTHOR,
        "service": "Flask API",
        "version": APP_VERSION,
        "status": "running",
        "environment": os.getenv("APP_ENV", "development"),
        "hostname": socket.gethostname(),
        "server_time": datetime.now(UTC).isoformat()
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/version")
def version():
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)