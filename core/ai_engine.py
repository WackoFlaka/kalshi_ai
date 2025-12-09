# core/ai_engine.py

import numpy as np
from fetchers.sentiment_fetcher import fetch_sentiment_score
from fetchers.news_fetcher import fetch_relevant_news
from models.ensemble_model import ensemble_predict


def generate_ai_probability(question: str, market):
    """
    Combines sentiment, news relevance, and ensemble ML model.
    Returns a probability between 0 and 1.
    """

    sentiment = fetch_sentiment_score(question)
    news_factor = fetch_relevant_news(question)

    # Basic weighting (adjust later)
    features = np.array([sentiment, news_factor])

    model_prob = ensemble_predict(features)

    # Ensure valid bounds
    return max(0.01, min(0.99, float(model_prob)))
