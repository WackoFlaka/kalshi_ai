# models/regression_model.py

import numpy as np


def logistic(x):
    """Basic logistic (sigmoid) function."""
    return 1 / (1 + np.exp(-x))


def regression_predict(features: np.ndarray) -> float:
    """
    Lightweight regression model.
    Input: array of features (e.g., sentiment, news score)
    Output: probability between 0 and 1
    """

    # Placeholder learned weights (you can train these later)
    weights = np.array([1.2, 0.8])  # sentiment weight, news weight
    bias = -0.1

    # Ensure same shape
    features = features[: len(weights)]

    z = np.dot(features, weights) + bias
    return logistic(z)
