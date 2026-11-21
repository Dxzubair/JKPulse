import hashlib
import hmac
import secrets
import base64
import json
import os
import time

TOKEN_SECRET = os.getenv("JKPULSE_TOKEN_SECRET", "change-this-secret-before-deployment")

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600000)
    return base64.b64encode(salt + hashed).decode()

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        decoded = base64.b64decode(stored_hash)
        salt = decoded[:16]
        expected_hash = decoded[16:]
        actual_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600000)
        return hmac.compare_digest(actual_hash, expected_hash)
    except Exception:
        return False

def generate_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": int(time.time()) + 86400
    }
    encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    signature = hmac.new(TOKEN_SECRET.encode(), encoded.encode(), hashlib.sha256).hexdigest()
    return f"{encoded}.{signature}"

def verify_token(token: str):
    try:
        encoded, signature = token.split(".", 1)
        expected = hmac.new(TOKEN_SECRET.encode(), encoded.encode(), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(signature, expected):
            return None

        payload = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))

        if payload.get("exp", 0) < int(time.time()):
            return None

        return payload.get("sub")
    except Exception:
        return None
