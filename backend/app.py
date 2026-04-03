from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import json, os, re

app = Flask(__name__)
CORS(app)

FILE = "messages.json"

# ---------------------------
# Utility Functions
# ---------------------------
def load_data():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(new_record):
    data = load_data()
    data.append(new_record)
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def is_valid_email(email):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)


# ---------------------------
# FRONTEND ROUTES (FIXED)
# ---------------------------

# Home + admin-console support
@app.route("/")
@app.route("/admin-console")
@app.route("/admin-console/")
def home():
    return render_template("frontend.html")


# SPA Catch-all (VERY IMPORTANT)
@app.route("/admin-console/<path:path>")
def catch_all(path):
    return render_template("frontend.html")


# ---------------------------
# API ROUTES
# ---------------------------

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        msg = data.get("message", "").strip()

        if not name or not msg:
            return jsonify({"error": "Name and Message are required"}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email address"}), 400

        record = {
            "id": len(load_data()) + 1,
            "name": name,
            "email": email,
            "message": msg,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        save_data(record)

        return jsonify({
            "status": "success",
            "message": "200 OK — Message Sent"
        }), 200

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/messages")
def msgs():
    return jsonify(load_data()), 200


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)