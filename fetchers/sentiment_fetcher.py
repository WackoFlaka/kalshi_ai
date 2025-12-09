# fetchers/sentiment_fetcher.py

import requests


def _score_text(text: str) -> float:
    """Tiny sentiment helper."""
    text = text.lower()

    positive = ["great", "good", "win", "success", "increase", "up"]
    negative = ["bad", "fail", "down", "loss", "fraud", "collapse"]

    score = 0
    for word in positive:
        if word in text:
            score += 0.1
    for word in negative:
        if word in text:
            score -= 0.1

    return max(-1, min(1, score))


def fetch_sentiment_score(query: str) -> float:
    """
    Basic sentiment from Reddit threads mentioning the topic.
    More advanced APIs can be added later.
    """

    try:
        url = f"https://www.reddit.com/search.json?q={query}"
        headers = {"User-agent": "Mozilla/5.0"}
        data = requests.get(url, headers=headers, timeout=5).json()

        posts = data.get("data", {}).get("children", [])
        if not posts:
            return 0.0

        score = 0
        for p in posts[:10]:
            title = p["data"]["title"]
            score += _score_text(title)

        return max(-1, min(1, score))

    except Exception:
        return 0.0
