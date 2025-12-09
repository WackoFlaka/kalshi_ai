# fetchers/sentiment_fetcher.py

import requests
import urllib.parse


def _score_text(text: str) -> float:
    """Tiny sentiment helper based on keyword matching."""
    text = text.lower()

    positive = ["great", "good", "win", "success", "increase", "up", "approve"]
    negative = ["bad", "fail", "down", "loss", "fraud", "collapse", "scandal"]

    score = 0.0
    for w in positive:
        if w in text:
            score += 0.1

    for w in negative:
        if w in text:
            score -= 0.1

    return max(-1.0, min(1.0, score))


def fetch_sentiment_score(query: str) -> float:
    """
    Attempts to derive sentiment from Reddit searches.
    Returns a normalized score between -1 and 1.
    If Reddit blocks the request or fails, returns 0.
    """

    try:
        encoded = urllib.parse.quote(query)
        url = f"https://www.reddit.com/search.json?q={encoded}"
        headers = {"User-agent": "Mozilla/5.0"}

        resp = requests.get(url, headers=headers, timeout=5)

        # If Reddit blocks or rate limits
        if resp.status_code != 200:
            return 0.0

        data = resp.json()
        posts = data.get("data", {}).get("children", [])

        if not posts:
            return 0.0

        score_total = 0.0
        count = 0

        # Score up to 10 relevant Reddit titles
        for p in posts[:10]:
            title = p.get("data", {}).get("title", "")
            if title:
                score_total += _score_text(title)
                count += 1

        if count == 0:
            return 0.0

        avg_score = score_total / count
        return max(-1.0, min(1.0, avg_score))

    except Exception:
        return 0.0
