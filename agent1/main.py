#!/usr/bin/env python3
"""
Flask server with Ollama query and RSA message signing.

Install dependencies:
    pip install flask requests cryptography

Run:
    python ollama_server.py

Endpoints:
    POST /query   - Send a prompt to Ollama
    POST /sign    - Sign a message with a private RSA SSH key

Examples:
    curl -X POST http://localhost:8000/query \
         -H "Content-Type: application/json" \
         -d '{"prompt": "Why is the sky blue?", "model": "llama3"}'

    curl -X POST http://localhost:8000/sign \
         -H "Content-Type: application/json" \
         -d '{"message": "hello world"}'
"""

import base64
import os
import requests
from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import hashes as crypto_hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as crypto_padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"
PRIVATE_KEY_PATH = "~/.ssh/id_rsa"
PORT = 8000

app = Flask(__name__)

def load_private_key(path: str) -> RSAPrivateKey:
    path = os.path.expanduser(path)
    with open(path, "rb") as f:
        key = serialization.load_ssh_private_key(f.read(), password=None)
    assert isinstance(key, RSAPrivateKey), "Key must be RSA"
    return key

@app.post("/query")
def query():
    data = request.get_json(silent=True) or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "Missing 'prompt'"}), 400

    model = data.get("model", DEFAULT_MODEL)

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"Ollama error: {e}"}), 502

    return jsonify({"response": resp.json().get("response", "")})


@app.post("/sign")
def sign():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Missing 'message'"}), 400

    try:
        key = load_private_key(PRIVATE_KEY_PATH)
        signature = key.sign(message.encode(), crypto_padding.PKCS1v15(), crypto_hashes.SHA256())
        signature_b64 = base64.b64encode(signature).decode()
    except Exception as e:
        return jsonify({"error": f"Signing error: {e}"}), 500

    return jsonify({"message": message, "signature": signature_b64})

if __name__ == "__main__":
    app.run(port=PORT, debug=False)
    