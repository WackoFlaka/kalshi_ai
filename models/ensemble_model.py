# models/ensemble_model.py

import numpy as np
from models.regression_model import regression_predict
from models.historical_learning import historical_bias_adjustment


def ensemble_predict(features: np.ndarray, question: str = "") -> float:
    """
    Combine multiple signals into a final probability.
    Currently uses:
    - regression model
    - historical learning adjustment
    """

    # Step 1 — Regression Model
    reg_prob = regression_predict(features)

    # Step 2 — Historical Bias Adjustment
    final_prob = historical_bias_adjustment(question, reg_prob)

    return max(0.01, min(0.99, float(final_prob)))
