# models/historical_learning.py

import json
import os
import numpy as np

HISTORY_PATH = "data/history.json"


def load_history():
    """Load past predictions safely."""
    if not os.path.exists(HISTORY_PATH):
        return []

    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_prediction(record: dict):
    """
    Save a new prediction record:
      {
        "question": "...",
        "prediction": 0.62,
        "market_price": 0.59,
        "action": "BUY YES"
      }
    """

    history = load_history()
    history.append(record)

    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


def _is_similar(q1: str, q2: str) -> bool:
    """
    Lightweight similarity test:
      - Compare overlapping keywords.
      - Avoid stopwords.
    """

    stopwords = {"the", "will", "on", "in", "at", "a", "or", "and", "to", "be"}

    w1 = {w for w in q1.lower().split() if w not in stopwords}
    w2 = {w for w in q2.lower().split() if w not in stopwords}

    if not w1 or not w2:
        return False

    overlap = w1.intersection(w2)
    return len(overlap) >= 1  # at least 1 meaningful word shared


def historical_bias_adjustment(question: str, prob: float) -> float:
    """
    Adjust probability based on historical performance:
    
        - If historically overconfident → reduce probability
        - If historically underconfident → increase probability

    Uses:
        actual_outcome - predicted_probability

    Only considers similar past questions.
    """

    history = load_history()
    if not history:
        return prob

    related = [h for h in history if _is_similar(h["question"], question)]

    if not related:
        return prob

    # Collect outcome errors only from items that have outcomes recorded
    errors = []
    for r in related:
        if "outcome" in r and isinstance(r["outcome"], (int, float)):
            errors.append(r["outcome"] - r["prediction"])

    # If no scoreable outcomes exist → no adjustment
    if not errors:
        return prob

    avg_bias = float(np.mean(errors))

    # Apply mild correction (keeps model stable)
    adjusted = prob + (avg_bias * 0.15)

    # Clamp to 1–99%
    return max(0.01, min(0.99, adjusted))
