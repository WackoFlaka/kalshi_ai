# fetchers/company_fetcher.py

import requests

YAHOO_FINANCE_NEWS = "https://query1.finance.yahoo.com/v1/finance/search?q="


def fetch_company_sentiment(company_name: str) -> float:
    """
    Returns a sentiment score for a company:
    Range: -1 (very negative) → +1 (very positive)
    """
    try:
        url = YAHOO_FINANCE_NEWS + company_name
        data = requests.get(url, timeout=5).json()

        if "news" not in data:
            return 0.0

        articles = data["news"][:5]

        score = 0
        for article in articles:
            title = article.get("title", "").lower()

            if any(x in title for x in ["lawsuit", "fraud", "fall", "collapse", "down"]):
                score -= 0.2
            if any(x in title for x in ["growth", "beats", "up", "record", "increase"]):
                score += 0.2

        return max(-1, min(1, score))

    except Exception:
        return 0.0
