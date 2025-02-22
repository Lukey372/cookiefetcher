from flask import Flask, jsonify, send_file
from fetch_cookies import get_cookies
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ CookieFetcher API is Running!"

@app.route("/get_cookies", methods=["GET"])
def fetch_cookies():
    return jsonify(get_cookies())

@app.route("/screenshot", methods=["GET"])
def get_screenshot():
    screenshot_path = "/app/debug_screenshot.png"
    if os.path.exists(screenshot_path):
        return send_file(screenshot_path, mimetype='image/png')
    return "❌ Screenshot not found!", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
