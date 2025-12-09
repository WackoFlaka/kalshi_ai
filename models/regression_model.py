# models/regression_model.py

import numpy as np


def logistic(x: float) -> float:
    """Numerically stable logistic (sigmoid)."""
    # Avoid overflow
    x = np.clip(x, -50, 50)
    return 1 / (1 + np.exp(-x))


def regression_predict(features: np.ndarray) -> float:
    """
    Lightweight regression model for Kalshi AI.
    
    Features vector (expected length = 5):
      0 sentiment_score
      1 news_factor
      2 type_flag
      3 category_flag
      4 rules_length
    """

    # Default placeholder weights — can be replaced with trained values later
    weights = np.array([
        1.2,    # sentiment
        0.8,    # news
        0.4,    # type_flag (binary markets get slight boost)
        0.3,    # category_flag
        0.1     # rules_length effect
    ], dtype=float)

    bias = -0.2  # small negative shift for conservative base probability

    # Ensure feature shape matches expected length
    if len(features) < len(weights):
        padded = np.zeros(len(weights))
        padded[:len(features)] = features
        features = padded
    else:
        features = features[:len(weights)]

    # Linear model → logistic probability
    z = np.dot(features, weights) + bias
    return float(logistic(z))
