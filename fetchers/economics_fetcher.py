# fetchers/economics_fetcher.py

import requests

YAHOO_MARKET_SUMMARY = "https://query1.finance.yahoo.com/v6/finance/quote?symbols=^GSPC,^IXIC,^DJI"


def fetch_economic_health_score() -> float:
    """
    Returns an economic stability indicator:
    +1 = strong economy
    -1 = weak economy
    """
    try:
        data = requests.get(YAHOO_MARKET_SUMMARY, timeout=5).json()
        results = data["quoteResponse"]["result"]

        score = 0
        for index in results:
            change = index.get("regularMarketChangePercent", 0)
            score += change / 100  # e.g. +1.5% → 0.015

        return max(-1, min(1, score))

    except Exception:
        return 0.0
