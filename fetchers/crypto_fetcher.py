# fetchers/crypto_fetcher.py

import requests


def fetch_crypto_price(symbol: str) -> float:
    """
    Get live crypto price (USD).
    symbol = "bitcoin", "ethereum", etc.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        data = requests.get(url, timeout=5).json()

        return float(data[symbol]["usd"])
    except Exception:
        return 0.0


def fetch_crypto_volatility(symbol: str) -> float:
    """
    Approximate volatility factor:
    Higher value = more uncertainty (increases YES/NO unpredictability)
    """
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days=7"
        data = requests.get(url, timeout=5).json()

        prices = [p[1] for p in data["prices"]]

        if len(prices) < 2:
            return 0.0

        avg = sum(prices) / len(prices)
        deviations = [(p - avg) ** 2 for p in prices]
        volatility = (sum(deviations) / len(prices)) ** 0.5

        return volatility / avg  # normalize

    except Exception:
        return 0.0
