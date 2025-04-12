from flask import Flask, render_template, request, jsonify
import time
import hmac
import hashlib
import requests
import json
import os
from dotenv import load_dotenv

from config import COINDCX_BASE_URL, COINDCX_API_KEY, COINDCX_API_SECRET

# COINDCX_API_KEY='d14f60796736421bab84dbc2899eabe4e8c52514d39bc9d2'
# COINDCX_API_SECRET='7c3c72c1a6e886b75a62b63273fc2a0f85aac497bbb508c1a31d02d0a453c7fe'


print("API credentials loaded." if COINDCX_API_KEY and COINDCX_API_SECRET else "Missing credentials.")

# Check if keys are loaded

if not COINDCX_API_KEY or not COINDCX_API_SECRET:
    raise Exception("API keys not loaded. Check your .env file.")

app = Flask(__name__)

# Helper to generate authentication headers
def get_headers(payload):
    payload_str = json.dumps(payload, separators=(',', ':'))
    signature = hmac.new(
        bytes(COINDCX_API_SECRET, 'utf-8'),
        msg=bytes(payload_str, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': COINDCX_API_KEY,
        'X-AUTH-SIGNATURE': signature
    }

    return headers



# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Open a trade (buy order)
@app.route('/open_trade', methods=['POST'])
def open_trade():
    data = request.get_json()
    payload = {
        "side": "buy",
        "order_type": "market_order",
        "market": data['symbol'],
        "total_quantity": data['quantity'],
        "timestamp": int(time.time() * 1000)
    }
    headers = get_headers(payload)
    response = requests.post(
        f"{COINDCX_BASE_URL}/exchange/v1/orders/create",
        json=payload,
        headers=headers
    )
    return jsonify(response.json())

@app.route('/test_auth')
def test_auth():
    payload = {"timestamp": int(time.time() * 1000)}
    headers = get_headers(payload)
    response = requests.post(
        f"{COINDCX_BASE_URL}/exchange/v1/users/balances",
        json=payload,
        headers=headers
    )
    return jsonify(response.json())


# Close a trade (sell order)
@app.route('/close_trade', methods=['POST'])
def close_trade():
    data = request.get_json()
    payload = {
        "side": "sell",
        "order_type": "market_order",
        "market": data['symbol'],
        "total_quantity": data['quantity'],
        "timestamp": int(time.time() * 1000)
    }
    headers = get_headers(payload)
    response = requests.post(
        f"{COINDCX_BASE_URL}/exchange/v1/orders/create",
        json=payload,
        headers=headers
    )
    return jsonify(response.json())

@app.route('/balance')
def get_balance():
    payload = {
        "timestamp": int(time.time() * 1000)
    }
    headers = get_headers(payload)
    response = requests.post(
        f"{COINDCX_BASE_URL}/exchange/v1/users/balances",
        json=payload,
        headers=headers
    )
    return jsonify(response.json())

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
