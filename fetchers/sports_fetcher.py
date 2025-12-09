# fetchers/sports_fetcher.py

import requests

ESPN_SEARCH = "https://site.web.api.espn.com/apis/search/v2?query="


def fetch_sports_form(team_name: str) -> float:
    """
    Returns a basic 'recent form' score for sports teams.
    Range: -1 → +1
    """
    try:
        url = ESPN_SEARCH + team_name
        data = requests.get(url, timeout=5).json()

        articles = data.get("sports", [])

        score = 0
        for a in articles[:5]:
            headline = a.get("headline", "").lower()

            if "win" in headline:
                score += 0.2
            if "loss" in headline:
                score -= 0.2

        return max(-1, min(1, score))

    except Exception:
        return 0.0
