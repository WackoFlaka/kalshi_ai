# core/kalshi_client.py

import time
import hmac
import hashlib
import requests
from config.settings import KALSHI_API_KEY_ID, KALSHI_API_SECRET, BASE_URL


class KalshiClient:
    def __init__(self):
        self.key = KALSHI_API_KEY_ID
        self.secret = KALSHI_API_SECRET

    def _sign(self, method: str, endpoint: str, body: str = ""):
        """Generate HMAC SHA256 signature for Kalshi Elections API."""
        timestamp = str(int(time.time() * 1000))
        message = timestamp + method.upper() + endpoint + body
        signature = hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return timestamp, signature

    def _headers(self, method: str, endpoint: str, body: str = ""):
        ts, sig = self._sign(method, endpoint, body)
        return {
            "KALSHI-ACCESS-KEY": self.key,
            "KALSHI-ACCESS-SIGNATURE": sig,
            "KALSHI-ACCESS-TIMESTAMP": ts,
            "Content-Type": "application/json"
        }

    def request(self, method: str, path: str, body: str = ""):
        """Centralized request handler for GET/POST."""
        endpoint = f"/{path}"
        url = BASE_URL + endpoint
        headers = self._headers(method, endpoint, body)

        if method == "GET":
            resp = requests.get(url, headers=headers)
        else:
            resp = requests.request(method, url, headers=headers, data=body)

        # Unauthorized or invalid signature
        if resp.status_code == 401:
            print("\n❌ Unauthorized — Check LIVE API key or signature.")
            print("Response Body:", resp.text)
            raise Exception("Unauthorized Kalshi API request")

        # Generic API error
        if not resp.ok:
            print(f"\n❌ Kalshi API error {resp.status_code}: {resp.text}")
            raise Exception(f"API error {resp.status_code}")

        return resp.json()

    # Public API wrappers
    def list_markets(self):
        return self.request("GET", "markets")

    def get_market(self, market_id):
        return self.request("GET", f"markets/{market_id}")
