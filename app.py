"""
========================================================
  KV Reddy Portfolio — Flask Backend
  Author : Kurukunda Venugopal Reddy
  Version: 1.0.0
========================================================

Run:
    pip install flask flask-cors
    python app.py

API:
    POST /api/contact  — saves & (optionally) emails the message
    GET  /api/messages — view all saved messages (dev only)
    GET  /api/health   — health check
========================================================
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os
import re

# ── App Setup ───────────────────────────────────────────
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow frontend requests

# ── Storage ─────────────────────────────────────────────
# All messages are saved to messages.json in the same folder.
MESSAGES_FILE = os.path.join(os.path.dirname(__file__), "messages.json")


def load_messages():
    """Load all messages from the JSON file."""
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r") as f:
        return json.load(f)


def save_message(message: dict):
    """Append a new message to the JSON file."""
    messages = load_messages()
    messages.append(message)
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=2)


# ── Validation ──────────────────────────────────────────
def is_valid_email(email: str) -> bool:
    """Basic email format check."""
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


# ── Routes ──────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    """Quick health check — useful to confirm the server is running."""
    return jsonify({
        "status": "online",
        "server": "KV Reddy Portfolio Backend",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200


@app.route("/api/contact", methods=["POST"])
def contact():
    """
    Receive a contact form submission from the portfolio.

    Expected JSON body:
        {
            "name":    "Recruiter Name",
            "email":   "recruiter@company.com",
            "message": "Hi Venu, we'd like to..."
        }

    Returns 200 on success, 400 on bad input, 500 on server error.
    """
    try:
        data = request.get_json(force=True)

        # ── Validate ──────────────────────────────────
        if not data:
            return jsonify({"error": "No JSON body received"}), 400

        name    = str(data.get("name",    "")).strip()
        email   = str(data.get("email",   "")).strip()
        message = str(data.get("message", "")).strip()

        if not name:
            return jsonify({"error": "Name is required"}), 400
        if not email or not is_valid_email(email):
            return jsonify({"error": "A valid email is required"}), 400
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        if len(message) > 2000:
            return jsonify({"error": "Message too long (max 2000 chars)"}), 400

        # ── Build record ──────────────────────────────
        record = {
            "id":        len(load_messages()) + 1,
            "name":      name,
            "email":     email,
            "message":   message,
            "received":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # ── Save to file ──────────────────────────────
        save_message(record)

        # ── Console log (easy to see in terminal) ─────
        print("\n" + "="*50)
        print(f"  📬 New message #{record['id']}")
        print(f"  From    : {name} <{email}>")
        print(f"  Time    : {record['received']}")
        print(f"  Message : {message[:80]}{'...' if len(message)>80 else ''}")
        print("="*50 + "\n")

        return jsonify({
            "status":  "success",
            "message": f"Thanks {name}! Your message has been received.",
            "id":      record["id"]
        }), 200

    except Exception as e:
        print(f"[ERROR] /api/contact — {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/messages", methods=["GET"])
def get_messages():
    """
    View all saved contact messages.
    Dev route — remove or protect with a password before going live.
    """
    try:
        messages = load_messages()
        return jsonify({
            "count":    len(messages),
            "messages": messages
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Run ─────────────────────────────────────────────────
if __name__ == "__main__":
    # Grab the port from the environment, fallback to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))
    
    print("\n" + "="*50)
    print("  🚀 KV Reddy Portfolio Backend")
    print(f"  Running on  : http://0.0.0.0:{port}")
    print(f"  Health check: http://0.0.0.0:{port}/api/health")
    print(f"  Messages    : http://0.0.0.0:{port}/api/messages")
    print("="*50 + "\n")
    
    # Set host to 0.0.0.0 to expose the server, turn debug off for prod
    app.run(host="0.0.0.0", port=port, debug=False)
