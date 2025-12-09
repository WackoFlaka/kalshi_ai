# models/ensemble_model.py

import numpy as np
from models.regression_model import regression_predict
from models.historical_learning import historical_bias_adjustment


def ensemble_predict(features: np.ndarray, question: str = "") -> float:
    """
    Combines multiple predictive signals to generate a final probability.
    
    Inputs:
      - features: numpy array of numeric inputs (sentiment, news, flags, rules_length)
      - question: text used for historical learning bias correction

    Pipeline:
      1. Regression model → base probability
      2. Historical learning → adjusts based on past performance
      3. Clamped final probability (0.01 → 0.99)
    """

    # --- Step 1: Base regression prediction ---
    try:
        reg_prob = float(regression_predict(features))
    except Exception:
        reg_prob = 0.5  # fallback baseline

    # --- Step 2: Historical bias correction ---
    try:
        adjusted_prob = historical_bias_adjustment(question, reg_prob)
    except Exception:
        adjusted_prob = reg_prob

    # --- Step 3: Clamp to safe range ---
    final_prob = max(0.01, min(0.99, float(adjusted_prob)))

    return final_prob
