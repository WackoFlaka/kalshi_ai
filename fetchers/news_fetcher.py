# fetchers/news_fetcher.py

import requests
import urllib.parse


NEWS_API = "https://newsapi.org/v2/everything?q={query}&apiKey=demo"
# Replace `demo` with real API key later for better accuracy.


def fetch_relevant_news(query: str) -> float:
    """
    Returns a normalized relevance score (0 to 1)
    based on how often the query appears in recent news articles.
    """

    try:
        encoded = urllib.parse.quote(query)
        url = NEWS_API.format(query=encoded)

        resp = requests.get(url, timeout=5)

        # If NewsAPI blocks or rate-limits
        if resp.status_code != 200:
            return 0.0

        data = resp.json()

        articles = data.get("articles", [])
        total_results = data.get("totalResults", 0)

        # No articles → no news relevance
        if not articles:
            return 0.0

        # Score based on article titles/content
        score = 0.0
        count = 0

        for article in articles[:10]:  # Cap for speed
            title = article.get("title", "").lower()
            desc = article.get("description", "").lower()

            # Basic text match → simplistic relevance estimator
            if query.lower().split()[0] in title or query.lower().split()[0] in desc:
                score += 0.1

            count += 1

        if count == 0:
            return 0.0

        # Combine direct scoring and normalized result count
        article_signal = min(1.0, score)
        volume_signal = min(1.0, total_results / 1000)

        # Final weighted score
        final_score = (article_signal * 0.6) + (volume_signal * 0.4)

        return max(0.0, min(1.0, final_score))

    except Exception:
        return 0.0
