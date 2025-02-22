from flask import Flask, jsonify
from app.fetch_cookies import get_cookies

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ CookieFetcher API is Running!"

@app.route("/get_cookies", methods=["GET"])
def fetch_cookies():
    return jsonify(get_cookies())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
