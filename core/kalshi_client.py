import time
import hmac
import hashlib
import requests
from config.settings import KALSHI_API_KEY_ID, KALSHI_API_SECRET, BASE_URL


class KalshiClient:
    def __init__(self):
        self.api_key = KALSHI_API_KEY_ID
        self.secret = KALSHI_API_SECRET

    def _headers(self, method, endpoint, body=""):
        timestamp = str(int(time.time() * 1000))
        message = timestamp + method.upper() + endpoint + body
        signature = hmac.new(
            self.secret.encode(), 
            message.encode(), 
            hashlib.sha256
        ).hexdigest()

        return {
            "KALSHI-ACCESS-KEY": self.api_key,
            "KALSHI-ACCESS-SIGNATURE": signature,
            "KALSHI-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json"
        }

    def get(self, path):
        endpoint = f"/{path}"
        url = BASE_URL + endpoint
        headers = self._headers("GET", endpoint)
        r = requests.get(url, headers=headers)
        return r.json()

    def list_markets(self):
        return self.get("markets")

    def get_market(self, market_id):
        return self.get(f"markets/{market_id}")

    def get_contracts(self, market_id):
        return self.get(f"markets/{market_id}/contracts")
