# models/historical_learning.py

import json
import os
import numpy as np


HISTORY_PATH = "data/history.json"


def load_history():
    """Load past predictions."""
    if not os.path.exists(HISTORY_PATH):
        return []

    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_prediction(record: dict):
    """Save new prediction to history."""
    history = load_history()
    history.append(record)

    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


def historical_bias_adjustment(question: str, prob: float) -> float:
    """
    Adjust the AI probability based on past similar predictions.

    Example:
    - If past predictions of similar markets were too optimistic, adjust down.
    - If historically too bearish, adjust upward.
    """

    history = load_history()
    if not history:
        return prob

    # Select similar markets by keyword overlap
    related = [h for h in history if any(word in question.lower() for word in h["question"].lower().split())]

    if not related:
        return prob

    # Compute average error
    errors = [(r["outcome"] - r["prediction"]) for r in related if "outcome" in r]
    if not errors:
        return prob

    bias = np.mean(errors)

    # Apply small correction
    adjusted = prob + (bias * 0.1)

    return max(0.01, min(0.99, adjusted))
