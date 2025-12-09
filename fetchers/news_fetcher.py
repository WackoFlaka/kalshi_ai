# fetchers/news_fetcher.py

import requests

NEWS_API = "https://newsapi.org/v2/everything?q={query}&apiKey=demo"  
# Replace 'demo' with a real key later if you want more accuracy.


def fetch_relevant_news(query: str) -> float:
    """
    Returns a relevance score from 0 → 1 based on how much the topic
    is appearing in recent news.
    """
    try:
        url = NEWS_API.format(query=query)
        data = requests.get(url, timeout=5).json()

        total = data.get("totalResults", 0)

        # Normalize to 0-1 range
        return min(1.0, total / 1000)  

    except Exception:
        return 0.0
